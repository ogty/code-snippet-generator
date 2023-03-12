import tempfile
from unittest import TestCase

from libs.operator import CodeSnippetOperator


class TestCodeSnippetOperator(TestCase):
    def test_get_file_content(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w+t") as temp:
            temp.write("line 1\nline 2\nline 3\n")
            temp.seek(0)
            self.assertEqual(
                CodeSnippetOperator.get_file_content(temp.name),
                ["line 1", "line 2", "line 3"],
            )

    def test_file_not_found(self) -> None:
        with self.assertRaises(SystemExit) as cm:
            CodeSnippetOperator.get_file_content("./non_existing.txt")
        self.assertEqual(cm.exception.code, 1)

    def test_write_output(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w+t") as temp:
            CodeSnippetOperator.write_output("line", temp.name)
            temp.seek(0)
            self.assertEqual(temp.read(), "line")
