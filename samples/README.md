# Sample run

`example_run.json` is a real, committed hash chain produced by one full pass over
the gene pool:

```bash
onc run --out samples/example_run.json
```

It contains 30 receipts (one per gene). Each receipt carries the sealed
`prediction_hash`, the revealed `outcome`, the independent `verdict`, and the
`prev_hash` linking it to the previous experiment.

Verify that nothing in it was tampered with:

```bash
onc chain verify samples/example_run.json
#   30 receipts · chain intact: True
```

Change a single character in any prediction and re-run `chain verify` — it will
report the chain as broken. This file is the kind of permanent, auditable record
ONC publishes for every experiment, including the ones it gets wrong (look for
the `"verdict": "FAIL"` receipts).
