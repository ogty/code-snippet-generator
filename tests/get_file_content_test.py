import unittest
import tempfile

from libs.operator import CodeSnippetOperator


class TestFileMethods(unittest.TestCase):
    def test_get_file_content(self):
        with tempfile.NamedTemporaryFile(mode="w+t") as temp:
            temp.write("line 1\nline 2\nline 3\n")
            temp.seek(0)
            self.assertEqual(
                CodeSnippetOperator.get_file_content(temp.name),
                ["line 1", "line 2", "line 3"],
            )
