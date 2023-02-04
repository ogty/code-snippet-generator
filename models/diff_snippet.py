from typing import List, Dict

from abstract.code_snippet import CodeSnippetInterface, CodeSnippetFrameInterface
from settings import (
    PLUS,
    MINUS,
    SPACE,
    NEWLINE,
    ADDITION_PATTERN,
    DELETION_PATTERN,
    WELL_KNOWN_SYMBOLS_PATTERN,
    BOX_DRAWINGS_LIGHT_HORIZONTAL,
    BOX_DRAWINGS_LIGHT_DOWN_AND_HORIZONTAL,
    BOX_DRAWINGS_LIGHT_VERTICAL_AND_HORIZONTAL,
)
from schemas.snippet import DiffSnippetConfig, Changes
from libs.operator import CodeSnippetOperator, CodeSnippetFrameOperator
from libs.graph import ChangesGraph


class DiffSnippetFrame(CodeSnippetFrameOperator, CodeSnippetFrameInterface):

    def __init__(self, config: DiffSnippetConfig) -> None:
        self.lines = []

        self.file_name = config["file_name"]
        self.max_frame_width = config["max_frame_width"]
        self.number_digits = config.get("number_digits", 3)

        self.initial_line_template = "╭─ {file_name}─╮"
        self.frame_title_template = self.process_string("│2 {changes_title}│")
        self.section_title_template = self.process_string("│2 {column_word} │3 {section_title}│")
        self.section_connecting_line_template = self.process_string("├13─{joint_component}┤")
        self.code_line_template = self.process_string("│2 {before}4 {after} │{prefix} {code}2 │")
        self.final_line_template = self.process_string("╰13─┴{padding}╯")

    def convert_dict_values_to_int(self, data: Dict[str, str]) -> Dict[str, int]:
        for key in data:
            data[key] = int(0 if data[key] is None else data[key])
        return data

    def all_zeros(self, data: List[int]) -> bool:
        return all(x == 0 for x in data)

    def set_final_line(self) -> None:
        formatted = self.fill_padding(
            word='',
            template=self.final_line_template,
            character=BOX_DRAWINGS_LIGHT_HORIZONTAL,
            name="padding",
        )
        self.lines.append(formatted)

    def set_section_connecting_line(self, is_start: bool = False) -> None:
        words = [
            BOX_DRAWINGS_LIGHT_VERTICAL_AND_HORIZONTAL,
            BOX_DRAWINGS_LIGHT_DOWN_AND_HORIZONTAL,
        ]
        formatted = self.fill_padding(
            word=words[is_start],
            template=self.section_connecting_line_template,
            character=BOX_DRAWINGS_LIGHT_HORIZONTAL,
            name="joint_component",
        )
        self.lines.append(formatted)

    def set_section_title(self, section_title: str, is_start: bool = False) -> None:
        template = self.section_title_template
        column_word = self.process_string("3.4 3.") if is_start else self.process_string("3 3.4 ")

        template_length = self.get_template_length(template=template)
        content_length = template_length + len(section_title + column_word)
        padding_width = self.max_frame_width - content_length
        padding = padding_width * SPACE

        formatted = template.format(
            section_title=(section_title + padding),
            column_word=column_word
        )
        self.lines.append(formatted)

    def set_code(
        self,
        after_line_number: str,
        before_line_number: str,
        code: str,
        prefix: str
    ) -> None:
        template = self.code_line_template

        template_length = self.get_template_length(template=template)
        content_length = template_length + len(after_line_number
            + before_line_number
            + prefix
            + code
        )
        padding_width = self.max_frame_width - content_length
        max_remainder_width = self.max_frame_width - (template_length
            + len((SPACE * self.number_digits)
            + (SPACE * self.number_digits)
            + (SPACE * 2)
        ))

        if padding_width < 0:
            remainder_codes = self.split_string(code, max_remainder_width)
            for remainder_code in remainder_codes:
                padding_width = max_remainder_width - len(remainder_code)
                padding = padding_width * SPACE
                formatted = template.format(
                    before=SPACE * self.number_digits,
                    after=SPACE * self.number_digits,
                    prefix=(SPACE * 2),
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

    def split_string(self, string: str, n: int) -> List[str]:
        return [string[i:i + n] for i in range(0, len(string), n)]

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
        addition_end = start_end["addition_end"]
        deletion_start = start_end["deletion_start"]
        deletion_end = start_end["deletion_end"]

        no_addition = self.all_zeros([addition_start, addition_end])
        no_deletion = self.all_zeros([deletion_start, deletion_end])
        is_one_zero = self.all_zeros([no_addition, no_deletion])

        is_addition_only = None
        if not is_one_zero and no_deletion:
            is_addition_only = True
        elif not is_one_zero and no_addition:
            is_addition_only = False

        # TODO: Rename
        def tmp(start: int, end: int, is_addition: bool = True) -> None:
            prefix = PLUS if is_addition else MINUS
            for code, line_number in zip(codes, range(start, end)):
                before = (SPACE * number_digits)
                after = str(line_number).rjust(number_digits, SPACE)
                before_after = [before, after]

                code = code[0].replace(prefix, '') + code[1:]
                self.set_code(
                    code=code,
                    before_line_number=before_after[not is_addition],
                    after_line_number=before_after[is_addition],
                    prefix=(SPACE + prefix)
                )

        if is_addition_only is not None:
            if not is_addition_only:
                tmp(deletion_start, deletion_end, False)
            else:
                tmp(addition_start, addition_end)
            return

        # TODO: Display line number
        for code in codes:
            code = code[0].replace(PLUS, PLUS + SPACE).replace(MINUS, MINUS + SPACE) + code[1:]
            self.set_code(
                code=(SPACE + code if code[0].startswith(SPACE) else code),
                before_line_number=SPACE.rjust(number_digits, SPACE),
                after_line_number=SPACE.rjust(number_digits, SPACE),
                prefix=''
            )

    def set_initial_line(self) -> None:
        formatted = self.fill_padding(
            word=(self.file_name + SPACE),
            template=self.initial_line_template,
            character=BOX_DRAWINGS_LIGHT_HORIZONTAL,
            name="file_name",
        )
        self.lines.append(formatted)

    def set_title(self, title: str) -> None:
        formatted = self.fill_padding(
            word=title,
            template=self.frame_title_template,
            character=SPACE,
            name="changes_title",
        )
        self.lines.append(formatted)


class DiffSnippet(CodeSnippetOperator, CodeSnippetInterface):

    def __init__(self, config: DiffSnippetConfig) -> None:
        self.config = config

        self.language = config["language"]
        self.file_name = config["file_name"]
        self.file_path = config["file_path"]
        self.max_frame_width = config.get("max_frame_width")
        self.number_digits = config.get("number_digits", 3)

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

    def plural_form(self, word: str, number: int) -> str:
        if number > 1:
            return word + 's'
        return word

    def format_title(self, data: Changes) -> str:
        number_of_additions = data["additions"]
        number_of_deletions = data["deletions"]
        number_of_changes = number_of_additions + number_of_deletions

        change_graph = ChangesGraph()
        graph = change_graph.generate(
            number_of_additions=number_of_additions,
            number_of_deletions=number_of_deletions
        )

        additions = f"{number_of_additions} {self.plural_form('addition', number_of_additions)}"
        deletions = f"{number_of_deletions} {self.plural_form('deletion', number_of_deletions)}"
        changes = "{changes} {graph} {changes} {string_change}".format(
            changes=number_of_changes,
            graph=graph,
            string_change=self.plural_form("change", number_of_changes)
        )

        title = "{changes}: {additions} & {deletions}".format(
            changes=changes,
            additions=additions,
            deletions=deletions,
        )
        return title

    def generate(self) -> str:
        file_content = self.get_file_content(self.file_path)
        diff_section_start_indexes = [index
            for index, line in enumerate(file_content)
                if WELL_KNOWN_SYMBOLS_PATTERN.match(line)
        ]
        changes = self.count_changes(file_content[diff_section_start_indexes[0]:])

        diff_sections = []
        number_of_diff_sections = len(diff_section_start_indexes)
        for index, section_start_index in enumerate(diff_section_start_indexes, start=1):
            if number_of_diff_sections == index:
                diff_sections.append(file_content[section_start_index:])
                break
            next_section_index = diff_section_start_indexes[index]
            diff_sections.append(file_content[section_start_index:next_section_index])

        frame = DiffSnippetFrame(self.config)
        frame.set_initial_line()
        frame.set_title(self.format_title(changes))
        frame.set_diff_sections(diff_sections)
        frame.set_final_line()
        return NEWLINE.join(frame.lines)
