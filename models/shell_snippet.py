from typing_extensions import override

from abstract.code_snippet import CodeSnippetInterface
from libs.operator import CodeSnippetOperator
from models.simple_snippet import SimpleSnippetFrame
from schemas.snippet import ShellSnippetConfig
from settings import BOX_DRAWINGS_LIGHT_HORIZONTAL, NEWLINE, SPACE


class ShellSnippetFrame(SimpleSnippetFrame):
    def __init__(self, max_frame_width: int, config: ShellSnippetConfig) -> None:
        super().__init__(max_frame_width, config)

        self.command_prompt_header_line_template = self.process_string(
            "│▕  ▭ {tab} ×  ▏ +  {padding}  -   □   ×  │"
        )
        self.terminal_header_line_template = self.process_string(
            "│ ● ◍ ○ {left_padding} {shell_name} {right_padding} │"
        )  #   ▔▔▔▔▔└───────────────▽
        self.header_buttons_width = 5
        self.initial_line_template = "╭─{padding}─╮"

    @override
    def set_initial_line(self) -> None:
        template = self.initial_line_template

        template_length = self.get_template_length(template=template)
        padding_width = self.max_frame_width - template_length
        padding = padding_width * BOX_DRAWINGS_LIGHT_HORIZONTAL

        formatted = template.format(padding=padding)
        self.lines.append(formatted)

    def set_command_prompt_header_line(self) -> None:
        template = self.command_prompt_header_line_template
        template_length = self.get_template_length(template=template)
        tab_name = self.language
        padding_width = self.max_frame_width - (template_length + len(tab_name))
        padding = padding_width * SPACE

        formatted = template.format(tab=tab_name, padding=padding)
        self.lines.append(formatted)

    def set_terminal_header_line(self) -> None:
        shell_name = self.language
        shell_name_length = len(shell_name)

        template = self.terminal_header_line_template
        template_length = self.get_template_length(template=template)
        content_length = template_length + shell_name_length
        one_side_padding_width = round((self.max_frame_width - content_length) / 2)

        left_padding_width = one_side_padding_width - self.header_buttons_width
        left_padding = left_padding_width * SPACE
        right_padding = (one_side_padding_width + self.header_buttons_width) * SPACE

        remaining_width = self.max_frame_width - (
            content_length + len(left_padding) + len(right_padding)
        )

        if remaining_width > 0:
            right_padding += SPACE
        elif remaining_width < 0:
            right_padding = right_padding[:-1]

        formatted = template.format(
            shell_name=shell_name,
            left_padding=left_padding,
            right_padding=right_padding,
        )

        self.lines.append(formatted)


class ShellSnippet(CodeSnippetOperator, CodeSnippetInterface):
    def __init__(self, max_frame_width: int, config: ShellSnippetConfig) -> None:
        self.max_frame_width = max_frame_width
        self.config = config
        self.file_path = config["file_path"]

    @override
    def generate(self, prefix: str = "", is_command_prompt: bool = False) -> str:
        file_content = self.get_file_content(self.file_path)

        if prefix:
            file_content = list(map(lambda line: prefix + line, file_content))

        frame = ShellSnippetFrame(self.max_frame_width, self.config)
        frame.set_initial_line()
        if is_command_prompt:
            frame.set_command_prompt_header_line()
        else:
            frame.set_terminal_header_line()
        frame.set_header_bottom_line()
        for code in file_content:
            frame.set_code(code)
        frame.set_final_line()

        return NEWLINE.join(frame.lines)
