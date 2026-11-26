import json
import unittest
from pathlib import Path
from app import run


class ExampleTest(unittest.TestCase):
    def test_example(self):
        base = Path(__file__).parent
        def read(name):
            return json.loads((base / name).read_text(encoding="utf-8"))
        self.assertEqual(run(read("example.json")), read("expected.json"))
