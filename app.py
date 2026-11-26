"""Reconcile two sets of EUR payments by reference."""
import argparse
import json
from pathlib import Path


def run(data):
    ledger, bank = data["ledger"], data["bank"]
    if any(type(v) is not int for v in [*ledger.values(), *bank.values()]):
        raise ValueError("amounts must be integer cents")
    return {key: ("missing_bank" if key not in bank else "missing_ledger" if key not in ledger else
                  "matched" if ledger[key] == bank[key] else "mismatch")
            for key in sorted(ledger.keys() | bank.keys())}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.input.read_text(encoding="utf-8"))
        print(json.dumps(run(data), ensure_ascii=False, indent=2))
    except (OSError, ValueError, KeyError, TypeError, ArithmeticError, AttributeError) as error:
        parser.exit(2, f"Invalid input: {error}\n")
