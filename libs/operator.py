from os.path import abspath
from typing import List

from settings import (
    EMPTY,
    ENCODING,
    NAMED_FORMAT_PATTERN,
    READ,
    RED,
    RESET,
    SPACE,
    WRITE,
)


class CodeSnippetFrameOperator:
    def __init__(self, max_frame_width: int) -> None:
        self.max_frame_width = max_frame_width

    def fill_padding(self, word: str, template: str, character: str, name: str) -> str:
        template_length = self.get_template_length(template=template)
        content_length = template_length + len(word)
        padding_width = self.max_frame_width - content_length
        padding = padding_width * character
        word += padding

        return template.format(**{name: word})

    @staticmethod
    def get_template_length(template: str) -> int:
        return len(NAMED_FORMAT_PATTERN.sub(EMPTY, template))

    @staticmethod
    def process_string(string: str) -> str:
        result = EMPTY
        num_buffer = EMPTY
        for character in string:
            if character.isdigit():
                num_buffer += character
                continue
            if num_buffer:
                result += character * int(num_buffer)
                num_buffer = EMPTY
                continue
            result += character
        if num_buffer:
            result += character * int(num_buffer)
        return result

    @staticmethod
    def split_string(string: str, n: int) -> List[str]:
        return [string[i : i + n] for i in range(0, len(string), n)]


class CodeSnippetOperator:
    @staticmethod
    def get_file_content(file_path: str) -> List[str]:
        absolute_path = abspath(file_path)
        try:
            with open(absolute_path, READ, encoding=ENCODING) as file:
                return [
                    line.rstrip().replace("\t", SPACE * 4) for line in file.readlines()
                ]
        except FileNotFoundError as error:
            print(RED, error, RESET)
            exit(1)

    @staticmethod
    def write_output(output: str, file_path: str) -> None:
        absolute_path = abspath(file_path)
        with open(absolute_path, WRITE, encoding=ENCODING) as file:
            file.write(output)
