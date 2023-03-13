from unittest import TestCase

from libs.operator import CodeSnippetFrameOperator


class TestTemplateMethods(TestCase):
    def test_get_template_length(self) -> None:
        template = "This is a template with named format {name}"
        self.assertEqual(
            CodeSnippetFrameOperator.get_template_length(template),
            len("This is a template with named format "),
        )

    def test_get_template_length_with_no_named_format(self) -> None:
        template = "This is a template without named format"
        self.assertEqual(
            CodeSnippetFrameOperator.get_template_length(template), len(template)
        )
