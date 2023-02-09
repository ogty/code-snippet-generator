from typing import List, Dict

from abstract.code_snippet import CodeSnippetInterface, CodeSnippetFrameInterface
from libs.graph import ChangesGraph
from libs.operator import CodeSnippetOperator, CodeSnippetFrameOperator
from settings import (
    PLUS,
    MINUS,
    SPACE,
    EMPTY,
    NEWLINE,
    ELLIPSIS,
    ADDITION_PATTERN,
    DELETION_PATTERN,
    WELL_KNOWN_SYMBOLS_PATTERN,
    BOX_DRAWINGS_LIGHT_HORIZONTAL,
    BOX_DRAWINGS_LIGHT_DOWN_AND_HORIZONTAL,
    BOX_DRAWINGS_LIGHT_VERTICAL_AND_HORIZONTAL,
)
from schemas.snippet import DiffSnippetConfig, Changes


class DiffSnippetFrame(CodeSnippetFrameOperator, CodeSnippetFrameInterface):
    def __init__(self, config: DiffSnippetConfig) -> None:
        self.lines = []

        self.file_name = config["file_name"]
        self.max_frame_width = config["max_frame_width"]
        self.number_digits = config.get("number_digits", 3)

        self.initial_line_template = "╭─ {file_name}─╮"
        self.frame_title_template = self.process_string("│2 {changes_title}│")
        self.header_bottom_line_template = self.process_string("├{padding}┤")
        self.section_title_template = self.process_string(
            "│2 {column_word} │3 {section_title}│"
        )
        self.section_connecting_line_template = self.process_string(
            "├13─{joint_component}┤"
        )
        self.code_line_template = self.process_string(
            "│2 {before}4 {after} │{prefix} {code}2 │"
        )
        self.final_line_template = self.process_string("╰13─┴{padding}╯")

    @classmethod
    def convert_dict_values_to_int(self, data: Dict[str, str]) -> Dict[str, int]:
        for key in data:
            data[key] = int(0 if data[key] is None else data[key])
        return data

    def set_header_bottom_line(self) -> None:
        formatted = self.fill_padding(
            word=EMPTY,
            name="padding",
            template=self.header_bottom_line_template,
            character=BOX_DRAWINGS_LIGHT_HORIZONTAL,
        )
        self.lines.append(formatted)

    def set_final_line(self) -> None:
        formatted = self.fill_padding(
            word=EMPTY,
            name="padding",
            template=self.final_line_template,
            character=BOX_DRAWINGS_LIGHT_HORIZONTAL,
        )
        self.lines.append(formatted)

    def set_section_connecting_line(self, is_start: bool = False) -> None:
        words = [
            BOX_DRAWINGS_LIGHT_VERTICAL_AND_HORIZONTAL,
            BOX_DRAWINGS_LIGHT_DOWN_AND_HORIZONTAL,
        ]
        formatted = self.fill_padding(
            word=words[is_start],
            name="joint_component",
            template=self.section_connecting_line_template,
            character=BOX_DRAWINGS_LIGHT_HORIZONTAL,
        )
        self.lines.append(formatted)

    def set_section_title(self, section_title: str, is_start: bool = False) -> None:
        template = self.section_title_template
        column_word = (
            self.process_string("3.4 3.") if is_start else self.process_string("3 3.4 ")
        )

        template_length = self.get_template_length(template=template)
        content_length = template_length + len(section_title + column_word)
        padding_width = self.max_frame_width - content_length
        if padding_width < 0:
            section_title = section_title[: (padding_width - 5)] + ELLIPSIS
            padding_width = 2
        padding = padding_width * SPACE

        formatted = template.format(
            section_title=(section_title + padding), column_word=column_word
        )
        self.lines.append(formatted)

    def set_code(
        self, after_line_number: str, before_line_number: str, code: str, prefix: str
    ) -> None:
        template = self.code_line_template

        template_length = self.get_template_length(template=template)
        content_length = template_length + len(
            after_line_number + before_line_number + prefix + code
        )
        padding_width = self.max_frame_width - content_length
        max_remainder_width = self.max_frame_width - (
            template_length
            + len(
                (SPACE * self.number_digits)
                + (SPACE * self.number_digits)
                + (SPACE * 2)
            )
        )

        if padding_width < 0:
            is_first_output = True
            remainder_codes = self.split_string(code, max_remainder_width)
            for remainder_code in remainder_codes:
                before = SPACE * self.number_digits
                after = SPACE * self.number_digits
                remainder_prefix = SPACE * 2
                padding_width = max_remainder_width - len(remainder_code)
                padding = padding_width * SPACE

                if is_first_output:
                    after = after_line_number
                    before = before_line_number
                    padding += SPACE * 2
                    is_first_output = False
                    remainder_prefix = ""

                formatted = template.format(
                    before=before,
                    after=after,
                    prefix=remainder_prefix,
                    code=(remainder_code + padding),
                )
                self.lines.append(formatted)
            return

        padding = padding_width * SPACE
        formatted = template.format(
            before=before_line_number,
            after=after_line_number,
            prefix=prefix,
            code=(code + padding),
        )
        self.lines.append(formatted)

    def set_diff_sections(self, diff_sections: List[List[str]]) -> None:
        for index, diff_section in enumerate(diff_sections):
            is_start = True if not index else False

            self.set_section_connecting_line(is_start=is_start)
            self.set_section_title(section_title=diff_section[0], is_start=is_start)
            self.set_section_connecting_line()
            self.set_diff_section(diff_section=diff_section)

    def set_diff_section(self, diff_section: List[str]) -> None:
        number_digits = self.number_digits
        section_title = diff_section[0]
        codes = diff_section[1:]
        matched = WELL_KNOWN_SYMBOLS_PATTERN.match(section_title)
        start_end = self.convert_dict_values_to_int(matched.groupdict())

        addition_start = start_end["addition_start"]
        deletion_start = start_end["deletion_start"]

        diff = []
        count_for_deletion = deletion_start
        count_for_addition = addition_start
        for code in codes:
            if not code or code[0] == SPACE:
                diff.append([str(count_for_deletion), str(count_for_addition), code])
                count_for_deletion += 1
                count_for_addition += 1
                continue

            prefix = code[0]
            if prefix == PLUS:
                diff.append([None, str(count_for_addition), code])
                count_for_addition += 1
                continue
            diff.append([str(count_for_deletion), None, code])
            count_for_deletion += 1

        for before_line_number, after_line_number, code in diff:
            before_line_number = (
                SPACE if before_line_number is None else before_line_number
            )
            after_line_number = (
                SPACE if after_line_number is None else after_line_number
            )

            if not code:
                code = SPACE
            else:
                code = (
                    code[0].replace(PLUS, PLUS + SPACE).replace(MINUS, MINUS + SPACE)
                    + code[1:]
                )

            self.set_code(
                code=(SPACE + code if code[0].startswith(SPACE) else code),
                prefix=EMPTY,
                before_line_number=before_line_number.rjust(number_digits, SPACE),
                after_line_number=after_line_number.rjust(number_digits, SPACE),
            )

    def set_initial_line(self) -> None:
        formatted = self.fill_padding(
            word=(self.file_name + SPACE),
            name="file_name",
            template=self.initial_line_template,
            character=BOX_DRAWINGS_LIGHT_HORIZONTAL,
        )
        self.lines.append(formatted)

    def set_title(self, title: str) -> None:
        formatted = self.fill_padding(
            word=title,
            name="changes_title",
            template=self.frame_title_template,
            character=SPACE,
        )
        self.lines.append(formatted)


class DiffSnippet(CodeSnippetOperator, CodeSnippetInterface):
    def __init__(self, config: DiffSnippetConfig) -> None:
        self.config = config
        self.file_path = config["file_path"]

    @classmethod
    def plural_form(self, word: str, number: int) -> str:
        if number > 1:
            return word + "s"
        return word

    def count_changes(self, diff_sections_only: List[str]) -> Changes:
        additions = 0
        deletions = 0
        for line in diff_sections_only:
            if DELETION_PATTERN.match(line):
                deletions += 1
            if ADDITION_PATTERN.match(line):
                additions += 1

        changes = additions + deletions
        return Changes(
            changes=changes,
            additions=additions,
            deletions=deletions,
        )

    def format_title(self, data: Changes) -> str:
        number_of_additions = data["additions"]
        number_of_deletions = data["deletions"]
        number_of_changes = number_of_additions + number_of_deletions

        change_graph = ChangesGraph()
        graph = change_graph.generate(
            number_of_additions=number_of_additions,
            number_of_deletions=number_of_deletions,
        )

        additions = (
            f"{number_of_additions} {self.plural_form('addition', number_of_additions)}"
        )
        deletions = (
            f"{number_of_deletions} {self.plural_form('deletion', number_of_deletions)}"
        )
        changes = "{changes} {graph} {changes} {string_change}".format(
            graph=graph,
            changes=number_of_changes,
            string_change=self.plural_form("Change", number_of_changes),
        )

        title = "{changes}: {additions} & {deletions}".format(
            changes=changes,
            additions=additions,
            deletions=deletions,
        )
        return title

    def generate(self) -> str:
        file_content = self.get_file_content(self.file_path)
        diff_section_start_indexes = [
            index
            for index, line in enumerate(file_content)
            if WELL_KNOWN_SYMBOLS_PATTERN.match(line)
        ]
        changes = self.count_changes(file_content[diff_section_start_indexes[0] :])

        diff_sections = []
        number_of_diff_sections = len(diff_section_start_indexes)
        for index, section_start_index in enumerate(
            diff_section_start_indexes, start=1
        ):
            if number_of_diff_sections == index:
                diff_sections.append(file_content[section_start_index:])
                break
            next_section_index = diff_section_start_indexes[index]
            diff_sections.append(file_content[section_start_index:next_section_index])

        frame = DiffSnippetFrame(self.config)
        frame.set_initial_line()
        frame.set_header_bottom_line()
        frame.set_title(self.format_title(changes))
        frame.set_diff_sections(diff_sections)
        frame.set_final_line()

        return NEWLINE.join(frame.lines)
