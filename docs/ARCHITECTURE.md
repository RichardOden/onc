# ONC Architecture

```
                         ┌──────────────────────────────┐
                         │          onc.cli             │
                         │   list-genes · run · chain   │
                         └───────────────┬──────────────┘
                                         │
                         ┌───────────────▼──────────────┐
                         │        onc.pipeline          │
                         │  SCREEN→SCORE→LOCK→TEST→      │
                         │  VERIFY→RECEIPT              │
                         └───┬────────┬────────┬─────────┘
                             │        │        │
             ┌───────────────▼─┐  ┌───▼──────┐ ┌▼────────────┐
             │   onc.scoring   │  │ onc.hash │ │  onc.verify │
             │ weights + card  │  │  chain   │ │  (separate  │
             └────────┬────────┘  └──────────┘ │   judge)    │
                      │                         └─────────────┘
             ┌────────▼─────────────────────────────┐
             │             onc.sources              │
             │ dependency genetics novelty pathways │
             │ tractability clinical   (+ offline)  │
             └────────┬─────────────────────────────┘
                      │
             ┌────────▼────────┐
             │   data/*.json   │  gene pool + offline evidence fixture
             └─────────────────┘
```

## Modules

| Module | Responsibility |
|--------|----------------|
| `onc.genes` | The 30-gene pool and resettable `Pool` draw semantics. |
| `onc.scoring` | Weights, the `ScoreCard`, and the two-threshold confirmation rule. |
| `onc.sources` | Evidence-source adapters (live + bundled offline fixture). |
| `onc.hashchain` | SHA-256 prediction sealing and the tamper-evident receipt chain. |
| `onc.verify` | The **independent** verifier — deliberately isolated from scoring. |
| `onc.pipeline` | Orchestrates the six stages and enforces the lock-before-test ordering. |
| `onc.cli` | Thin command-line surface. |

## Key invariants (enforced in code and tests)

- **Lock before test:** `pipeline.run_experiment` hashes the prediction dict and
  only then reads `held_out_dependency`.
- **Separation of powers:** `scoring` never imports `verify`; `verify` never
  imports scoring internals.
- **Append-only:** `HashChain` exposes no mutation of existing receipts; tampering
  is detected by `HashChain.verify()`.
- **Weights sum to 1.0:** asserted at import time.

## Offline-first

The default `OfflineEvidence` adapter reads `data/sample_evidence.json`, so the
whole pipeline — and the test suite — runs deterministically with no network
access. Live adapters document their real API endpoints and swap in behind the
same `EvidenceSource` interface.
