from unittest import TestCase

from libs.operator import CodeSnippetFrameOperator


class TestStringMethods(TestCase):
    def test_process_string(self):
        string = "3a2bc3d"
        expected_result = "aaabbcddd"
        self.assertEqual(
            CodeSnippetFrameOperator.process_string(string), expected_result
        )

    def test_process_string_with_no_multiplier(self):
        string = "abcde"
        expected_result = "abcde"
        self.assertEqual(
            CodeSnippetFrameOperator.process_string(string), expected_result
        )
