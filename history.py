"""Record a reconciliation in a local SQLite database."""
import argparse
import hashlib
import json
from pathlib import Path
import sqlite3

from app import run


def record(db, data):
    outcomes = run(data)
    canonical = json.dumps(data, sort_keys=True, separators=(",", ":"))
    batch = hashlib.sha256(canonical.encode()).hexdigest()
    with db:
        db.execute("""CREATE TABLE IF NOT EXISTS results(
            batch TEXT, reference TEXT, ledger_cents INTEGER, bank_cents INTEGER,
            outcome TEXT NOT NULL, PRIMARY KEY(batch, reference))""")
        db.executemany("INSERT OR IGNORE INTO results VALUES(?, ?, ?, ?, ?)", (
            (batch, ref, data["ledger"].get(ref), data["bank"].get(ref), state)
            for ref, state in outcomes.items()))
    return batch


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("database", type=Path)
    args = parser.parse_args()
    connection = sqlite3.connect(args.database)
    try:
        print(record(connection, json.loads(args.input.read_text(encoding="utf-8"))))
    finally:
        connection.close()
