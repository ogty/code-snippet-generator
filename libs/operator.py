import os
from typing import List

from settings import ENCODING, READ, NAMED_FORMAT_PATTERN, EMPTY


class CodeSnippetFrameOperator:

    def fill_padding(self, word: str, template: str, character: str, name: str) -> str:
        template_length = self.get_template_length(template=template)
        content_length = template_length + len(word)
        padding_width = self.max_frame_width - content_length
        padding = padding_width * character
        word += padding

        return template.format(**{name: word})

    @classmethod
    def get_template_length(self, template: str) -> int:
        return len(NAMED_FORMAT_PATTERN.sub(EMPTY, template))

    @classmethod
    def process_string(self, string: str) -> str:
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


class CodeSnippetOperator:

    @classmethod
    def get_file_content(self, file_path: str) -> List[str]:
        absolute_path = os.path.abspath(file_path)
        with open(absolute_path, READ, encoding=ENCODING) as diff_file:
            return [line.rstrip() for line in diff_file.readlines()]
