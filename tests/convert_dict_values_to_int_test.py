from unittest import TestCase

from models.diff_snippet import DiffSnippetFrame


class TestConvertDictValuesToInt(TestCase):
    def test_convert_dict_values_to_int(self) -> None:
        data = {"key1": "1", "key2": "2", "key3": None}
        expected = {"key1": 1, "key2": 2, "key3": 0}
        result = DiffSnippetFrame.convert_dict_values_to_int(data)
        self.assertEqual(result, expected)
