from abstract.code_snippet import CodeSnippetFrameInterface
from libs.operator import CodeSnippetOperator, CodeSnippetFrameOperator
from schemas.snippet import SnippetConfig
from settings import BOX_DRAWINGS_LIGHT_HORIZONTAL, SPACE, NEWLINE, EMPTY


class SimpleSnippetFrame(CodeSnippetFrameOperator, CodeSnippetFrameInterface):
    def __init__(self, config: SnippetConfig) -> None:
        self.lines = []

        self.language = config["language"]
        self.file_name = config["file_name"]
        self.max_frame_width = config["max_frame_width"]

        self.initial_line_template = self.process_string("╭─{language}─{file_name}─╮")
        self.header_bottom_line_template = self.process_string("├{padding}┤")
        self.code_line_template = self.process_string("│2 {padding}2 │")
        self.final_line_template = self.process_string("╰{padding}╯")

    @classmethod
    def add_padding(self, string: str, n: int = 1) -> str:
        padding = SPACE * n
        return padding + string + padding

    def set_initial_line(self) -> None:
        template = self.initial_line_template
        language = self.add_padding(self.language) if self.language else EMPTY
        file_name = self.add_padding(self.file_name) if self.file_name else EMPTY

        template_length = self.get_template_length(template=template)
        content_length = template_length + len(language + file_name)
        padding_width = self.max_frame_width - content_length
        padding = padding_width * BOX_DRAWINGS_LIGHT_HORIZONTAL

        formatted = template.format(
            language=language,
            file_name=(file_name + padding),
        )
        self.lines.append(formatted)

    def set_code(self, code: str) -> None:
        template = self.code_line_template

        template_length = self.get_template_length(template=template)
        content_length = template_length + len(code)
        padding_width = self.max_frame_width - content_length
        max_remainder_width = self.max_frame_width - template_length

        if padding_width < 0:
            is_first_output = True
            remainder_codes = self.split_string(code, max_remainder_width)
            for remainder_code in remainder_codes:
                if is_first_output:
                    is_first_output = False

                padding_width = max_remainder_width - len(remainder_code)
                padding = padding_width * SPACE
                formatted = template.format(
                    padding=(remainder_code + padding),
                )
                self.lines.append(formatted)
            return

        padding = padding_width * SPACE
        formatted = template.format(
            padding=(code + padding),
        )
        self.lines.append(formatted)

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


class SimpleSnippet(CodeSnippetOperator):
    def __init__(self, config: SnippetConfig) -> None:
        self.config = config
        self.file_path = config["file_path"]

    def generate(
        self, prefix: str = "", is_line_number: bool = False, start_line: int = None
    ) -> str:
        start_line = start_line or 1

        file_content = self.get_file_content(self.file_path)
        file_content_length = len(file_content)
        number_digits = len(str(file_content_length))
        if is_line_number:
            line_numbers = [
                str(i).rjust(number_digits, SPACE)
                for i in range(start_line, file_content_length + start_line)
            ]
            file_content = list(
                map(
                    lambda x: x[0] + (SPACE * 3) + x[1], zip(line_numbers, file_content)
                )
            )
        if prefix:
            file_content = list(map(lambda l: prefix + l, file_content))

        frame = SimpleSnippetFrame(config=self.config)
        frame.set_initial_line()
        frame.set_header_bottom_line()
        for code in file_content:
            frame.set_code(code)
        frame.set_final_line()

        return NEWLINE.join(frame.lines)
