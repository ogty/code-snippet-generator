import unittest

from models.diff_snippet import DiffSnippet
from models.simple_snippet import SimpleSnippet
from models.shell_snippet import ShellSnippet
from schemas.snippet import DiffSnippetConfig, SnippetConfig, ShellSnippetConfig
from settings import ENCODING, READ


class TestSnippet(unittest.TestCase):
    def test_shell_snippet(self):
        with open("tests/data/shell_snippet_output.txt", READ, encoding=ENCODING) as f:
            expected_output = f.read()

        path = "tests/data/shell_snippet.txt"
        prefix = "$ "
        shell_name = "bash"
        max_frame_width = 100

        config = ShellSnippetConfig(
            language=shell_name,
            file_path=path,
            output_path="",
            max_frame_width=max_frame_width,
        )
        shell_snippet = ShellSnippet(config=config)
        output = shell_snippet.generate(prefix=prefix)

        self.assertEqual(output, expected_output)

    def test_simple_sippet(self):
        with open("tests/data/simple_snippet_output.txt", READ, encoding=ENCODING) as f:
            expected_output = f.read()

        path = "tests/data/simple_snippet.txt"
        language = "Markdown"
        file_name = "docs/usage.md"
        is_line_number = True
        max_frame_width = 100

        config = SnippetConfig(
            language=language,
            file_name=file_name,
            file_path=path,
            output_path="",
            max_frame_width=max_frame_width,
        )
        simple_snippet = SimpleSnippet(config=config)
        output = simple_snippet.generate(is_line_number=is_line_number)

        self.assertEqual(output, expected_output)

    def test_diff_snippet(self):
        with open("tests/data/diff_snippet_output.txt", READ, encoding=ENCODING) as f:
            expected_output = f.read()

        path = "tests/data/diff_snippet.txt"
        file_name = "main.py"
        max_frame_width = 100

        config = DiffSnippetConfig(
            language="",
            file_name=file_name,
            file_path=path,
            output_path="",
            max_frame_width=max_frame_width,
        )
        diff_snippet = DiffSnippet(config=config)
        output = diff_snippet.generate()

        self.assertEqual(output, expected_output)
