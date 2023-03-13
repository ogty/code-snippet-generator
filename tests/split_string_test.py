from unittest import TestCase

from models.diff_snippet import DiffSnippetFrame


class TestSplitString(TestCase):
    def test_split_string(self) -> None:
        result = DiffSnippetFrame.split_string("abcdefghijklm", n=3)
        self.assertEqual(result, ["abc", "def", "ghi", "jkl", "m"])

    def test_split_string_empty_string(self) -> None:
        result = DiffSnippetFrame.split_string("", n=3)
        self.assertEqual(result, [])

    def test_split_string_n_greater_than_string_length(self) -> None:
        result = DiffSnippetFrame.split_string("abc", n=10)
        self.assertEqual(result, ["abc"])
