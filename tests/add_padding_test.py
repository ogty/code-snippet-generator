import unittest

from settings import SPACE

from models.simple_snippet import SimpleSnippetFrame


class TestStringMethods(unittest.TestCase):
    def test_add_padding(self):
        # Test if padding is added correctly to string
        result = SimpleSnippetFrame.add_padding("test", n=1)
        expected = SPACE + "test" + SPACE
        self.assertEqual(result, expected)

        # Test if padding of n=2 is added correctly to string
        result = SimpleSnippetFrame.add_padding("test", n=2)
        expected = SPACE * 2 + "test" + SPACE * 2
        self.assertEqual(result, expected)

        # Test if default padding is added correctly to string
        result = SimpleSnippetFrame.add_padding("test")
        expected = SPACE + "test" + SPACE
        self.assertEqual(result, expected)
