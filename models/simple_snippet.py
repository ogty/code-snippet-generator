from typing import List

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

        self.initial_line_template = self.process_string("┌─{language}─{file_name}─┐")
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

    def set_code(self, codes: List[str]) -> None:
        for code in codes:
            formatted = self.fill_padding(
                word=code,
                template=self.code_line_template,
                character=SPACE,
                name="padding",
            )
            self.lines.append(formatted)

    def set_header_bottom_line(self) -> None:
        formatted = self.fill_padding(
            word=EMPTY,
            template=self.header_bottom_line_template,
            character=BOX_DRAWINGS_LIGHT_HORIZONTAL,
            name="padding",
        )
        self.lines.append(formatted)

    def set_final_line(self) -> None:
        formatted = self.fill_padding(
            word=EMPTY,
            template=self.final_line_template,
            character=BOX_DRAWINGS_LIGHT_HORIZONTAL,
            name="padding",
        )
        self.lines.append(formatted)


class SimpleSnippet(CodeSnippetOperator):
    def __init__(self, config: SnippetConfig) -> None:
        self.config = config
        self.file_path = config["file_path"]

    def generate(self) -> str:
        file_content = self.get_file_content(self.file_path)

        frame = SimpleSnippetFrame(config=self.config)
        frame.set_initial_line()
        frame.set_header_bottom_line()
        frame.set_code(file_content)
        frame.set_final_line()

        return NEWLINE.join(frame.lines)
