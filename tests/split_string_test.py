from unittest import TestCase

from models.diff_snippet import DiffSnippetFrame


class TestSplitString(TestCase):
    def test_split_string(self) -> None:
        string = "abcdefghijklm"
        n = 3
        expected = ["abc", "def", "ghi", "jkl", "m"]
        result = DiffSnippetFrame.split_string(string, n)
        self.assertEqual(result, expected)

    def test_split_string_empty_string(self) -> None:
        string = ""
        n = 3
        expected = []
        result = DiffSnippetFrame.split_string(string, n)
        self.assertEqual(result, expected)

    def test_split_string_n_greater_than_string_length(self) -> None:
        string = "abc"
        n = 10
        expected = ["abc"]
        result = DiffSnippetFrame.split_string(string, n)
        self.assertEqual(result, expected)
