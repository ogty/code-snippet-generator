from unittest import TestCase

from models.diff_snippet import DiffSnippet
from models.shell_snippet import ShellSnippet
from models.simple_snippet import SimpleSnippet
from schemas.snippet import DiffSnippetConfig, ShellSnippetConfig, SnippetConfig
from settings import ENCODING, READ, SPACE


def get_file_content(path: str) -> str:
    file_content = ""
    with open(path, READ, encoding=ENCODING) as f:
        file_content = f.read()
    return file_content


class TestSnippet(TestCase):
    def setUp(self) -> None:
        self.maxDiff = None

        self.max_frame_width_a = 100
        self.max_frame_width_b = 80

    def test_shell_snippet(self) -> None:
        config = ShellSnippetConfig(
            language="bash",
            file_path="tests/data/shell_snippet.txt",
            file_name="",
            output_path="",
        )
        shell_snippet = ShellSnippet(self.max_frame_width_a, config=config)
        output = shell_snippet.generate(prefix="$ ")
        self.assertEqual(
            output, get_file_content("tests/data/shell_snippet_output.txt")
        )

    def test_command_prompt_snippet(self) -> None:
        config = ShellSnippetConfig(
            language="Desktop",
            file_path="tests/data/command_prompt_snippet.txt",
            file_name="",
            output_path="",
        )
        shell_snippet = ShellSnippet(self.max_frame_width_a, config=config)
        output = shell_snippet.generate(
            prefix="C:\\Users\\ogty\\Desktop", is_command_prompt=True
        )
        self.assertEqual(
            output, get_file_content("tests/data/command_prompt_snippet_output.txt")
        )

    def test_simple_sippet(self) -> None:
        path = "tests/data/simple_snippet.txt"
        language = "Markdown"
        file_name = "docs/usage.md"
        is_line_number = True

        config = SnippetConfig(
            language=language,
            file_name=file_name,
            file_path=path,
            output_path="",
        )
        simple_snippet = SimpleSnippet(self.max_frame_width_a, config=config)
        output = simple_snippet.generate(is_line_number=is_line_number)
        self.assertEqual(
            output, get_file_content("tests/data/simple_snippet_output_a.txt")
        )

        config = SnippetConfig(
            language=language,
            file_name=file_name,
            file_path=path,
            output_path="",
        )
        simple_snippet = SimpleSnippet(self.max_frame_width_b, config=config)
        output = simple_snippet.generate(prefix=SPACE, is_line_number=is_line_number)
        self.assertEqual(
            output, get_file_content("tests/data/simple_snippet_output_b.txt")
        )

    def test_diff_snippet(self) -> None:
        file_name = "main.py"
        config = DiffSnippetConfig(
            language="",
            file_name=file_name,
            file_path="tests/data/diff_snippet.txt",
            output_path="",
        )
        diff_snippet = DiffSnippet(self.max_frame_width_a, config=config)
        output = diff_snippet.generate()
        self.assertEqual(
            output, get_file_content("tests/data/diff_snippet_output_a.txt")
        )

        config = DiffSnippetConfig(
            language="",
            file_name=file_name,
            file_path="tests/data/diff_snippet_for_section_title.txt",
            output_path="",
        )
        diff_snippet = DiffSnippet(self.max_frame_width_b, config=config)
        output = diff_snippet.generate()
        self.assertEqual(
            output, get_file_content("tests/data/diff_snippet_output_b.txt")
        )
