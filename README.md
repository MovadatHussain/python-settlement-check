# settlement-check

Reconcile two sets of EUR payments by reference.

Pass ledger and bank objects mapping references to integer cents.

## Run

Python 3.10 or newer, standard library only. From this folder:

```sh
python app.py example.json
python -m unittest -v
```

See [the sample input](example.json) and [expected report](expected.json). The tool reads one local file and prints JSON. Calculations are in `run` in [app.py](app.py).

## Keep a reconciliation history

Run `python history.py example.json history.sqlite`. The batch identifier comes from the input contents. Reimporting the same export keeps one result per reference. Correcting an amount creates a new batch and preserves the earlier discrepancy. Missing amounts are SQL NULL, which distinguishes an absent payment from a zero-value payment.

Inspect exceptions in SQLite:

```sql
SELECT batch, reference, ledger_cents, bank_cents FROM results WHERE outcome != 'matched';
```
