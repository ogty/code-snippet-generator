import unittest

from libs.operator import CodeSnippetFrameOperator


class TestTemplateMethods(unittest.TestCase):
    def test_get_template_length(self):
        template = "This is a template with named format {name}"
        expected_length = len("This is a template with named format ")
        self.assertEqual(
            CodeSnippetFrameOperator.get_template_length(template), expected_length
        )

    def test_get_template_length_with_no_named_format(self):
        template = "This is a template without named format"
        expected_length = len(template)
        self.assertEqual(
            CodeSnippetFrameOperator.get_template_length(template), expected_length
        )
