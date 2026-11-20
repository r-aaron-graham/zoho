import unittest
import json
from pathlib import Path
import subprocess
import sys
import tempfile
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

    def test_cli_preserves_output_on_invalid_input(self):
        script = str(Path(__file__).with_name("contacts.py"))
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "input.json"
            target = Path(directory) / "output.json"
            target.write_text("existing")
            source.write_text("[{}]")
            result = subprocess.run([sys.executable, script, "--input", str(source),
                                     "--output", str(target)], capture_output=True)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(target.read_text(), "existing")
            source.write_text('[{"id":"1","Last_Name":"Example"}]')
            subprocess.run([sys.executable, script, "--input", str(source),
                            "--output", str(target)], check=True)
            self.assertEqual(json.loads(target.read_text())[0]["external_id"], "1")

    def test_empty_batch(self):
        self.assertEqual(normalize_batch([]), [])


if __name__ == "__main__":
    unittest.main()
