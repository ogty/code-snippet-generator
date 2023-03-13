from unittest import TestCase

from libs.operator import CodeSnippetFrameOperator


class TestStringMethods(TestCase):
    def test_process_string(self) -> None:
        self.assertEqual(
            CodeSnippetFrameOperator.process_string("3a2bc3d"), "aaabbcddd"
        )

    def test_process_string_with_no_multiplier(self) -> None:
        self.assertEqual(CodeSnippetFrameOperator.process_string("abcde"), "abcde")
