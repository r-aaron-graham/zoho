import unittest
from contacts import normalize_batch


class ContactTests(unittest.TestCase):
    def test_normalization(self):
        result = normalize_batch([{"id": " 1 ", "Last_Name": " Example ", "Email": None}])
        self.assertEqual(result, [{"external_id": "1", "last_name": "Example", "email": None}])

    def test_invalid_input(self):
        for value in (None, {}, [None], [{"id": "1"}],
                      [{"id": "1", "Last_Name": "Example", "Email": 42}]):
            with self.subTest(value=value), self.assertRaises(ValueError):
                normalize_batch(value)

    def test_duplicate_ids(self):
        with self.assertRaises(ValueError):
            normalize_batch([{"id": "1", "Last_Name": "A"}, {"id": " 1 ", "Last_Name": "B"}])

    def test_empty_batch(self):
        self.assertEqual(normalize_batch([]), [])


if __name__ == "__main__":
    unittest.main()
