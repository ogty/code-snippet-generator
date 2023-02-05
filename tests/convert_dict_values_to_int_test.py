import unittest

from models.diff_snippet import DiffSnippetFrame


class TestConvertDictValuesToInt(unittest.TestCase):
    def test_convert_dict_values_to_int(self):
        data = {"key1": "1", "key2": "2", "key3": None}
        expected = {"key1": 1, "key2": 2, "key3": 0}
        result = DiffSnippetFrame.convert_dict_values_to_int(data)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
