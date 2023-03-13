from unittest import TestCase

from models.diff_snippet import DiffSnippetFrame


class TestConvertDictValuesToInt(TestCase):
    def test_convert_dict_values_to_int(self) -> None:
        result = DiffSnippetFrame.convert_dict_values_to_int(
            {"key1": "1", "key2": "2", "key3": None}
        )
        self.assertEqual(result, {"key1": 1, "key2": 2, "key3": 0})
