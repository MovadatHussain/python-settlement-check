import sqlite3
import unittest
from history import record


class HistoryTests(unittest.TestCase):
    def test_retry_and_correction(self):
        with sqlite3.connect(":memory:") as db:
            original = {"ledger": {"A": -205}, "bank": {"A": -250}}
            batch = record(db, original)
            self.assertEqual(record(db, dict(reversed(list(original.items())))), batch)
            self.assertEqual(db.execute("SELECT count(*) FROM results").fetchone(), (1,))
            original["bank"]["A"] = -205
            self.assertNotEqual(record(db, original), batch)
            self.assertEqual(db.execute("SELECT outcome FROM results ORDER BY rowid").fetchall(),
                             [("mismatch",), ("matched",)])
