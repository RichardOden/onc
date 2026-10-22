# The ONC Hash Chain

The hash chain is what makes ONC a *scientist* and not a black box. It
guarantees two things that no promise or policy can:

1. ONC cannot change what it predicted after seeing the answer.
2. Anyone can detect tampering with any past result.

## What gets hashed

Each experiment seals a **prediction** payload *before* any test data exists:

```json
{
  "symbol": "MYCN",
  "cancer": "neuroblastoma (high-risk)",
  "scores": { "dependency": 0.91, "genetics": 0.78, "novelty": 0.22,
              "pathways": 0.85, "tractability": 0.40, "clinical": 0.60 },
  "weighted": 0.73,
  "predicted_dependency": true
}
```

`prediction_hash = SHA256(canonical_json(prediction))`

Canonicalisation sorts keys and strips whitespace, so identical content always
produces an identical hash.

## How receipts chain

Each receipt stores the hash of the previous one. The receipt hash covers the
`prediction_hash`, the revealed `outcome`, the `verdict`, and the `prev_hash`:

```
receipt.hash = SHA256(canonical_json({
    index, prediction_hash, outcome, verdict, prev_hash
}))
```

```
   #000 (prev = 000…0)        #001                       #002
   ┌───────────────┐          ┌───────────────┐          ┌───────────────┐
   │ pred_hash a3f9│          │ pred_hash 7c21│          │ pred_hash e84d│
   │ prev      000…│          │ prev      H₀  │          │ prev      H₁  │
   │ hash  H₀ ─────┼────────▶ │ hash  H₁ ─────┼────────▶ │ hash  H₂      │
   └───────────────┘          └───────────────┘          └───────────────┘
```

## Why tampering is detectable

Change any field of any past prediction and its `prediction_hash` changes, which
changes that receipt's `hash`, which no longer matches the `prev_hash` stored in
the next receipt — and every link after it. `HashChain.verify()` recomputes the
entire chain and returns `False` at the first break.

```python
from onc.hashchain import HashChain
chain = HashChain.load("run.chain.json")
assert chain.verify()   # False if a single byte was altered
```

## What it does *not* do

The chain proves **integrity and ordering**, not correctness. A sealed
prediction can still be wrong — and when it is, the FAIL verdict is published and
chained like any other result. A negative result is still a result.
