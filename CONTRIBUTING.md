# Contributing to ONC

ONC is an autonomous research system, but the methodology, scoring weights, gene
pool, and evidence adapters are all open for scrutiny and improvement.

## Ground rules

1. **Never weaken the lock.** The prediction must always be hashed *before* any
   test data is read (pipeline stage 3 before stage 4). PRs that reorder this
   will be rejected.
2. **The verifier stays independent.** Scoring code must not import from
   `onc.verify`, and the verifier must not import scoring internals.
3. **Failures are published.** Do not add any mechanism to hide, edit, or delete
   a receipt after the fact.

## Development setup

```bash
git clone https://github.com/RichardOden/onc.git
cd onc
python -m venv .venv && . .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

## Running the checks

```bash
pytest -q          # test suite (offline, deterministic)
ruff check .       # lint
onc run            # smoke-test a full pass over the gene pool
```

## Adding an evidence source

Evidence sources live in `onc/sources/` and implement
`onc.sources.base.EvidenceSource`: a `name` and a `score(symbol) -> float` in
`[0, 1]`. Add the weight to `onc.scoring.WEIGHTS` (weights must sum to 1.0) and
cover it with a test. Document the normalisation in `docs/METHODOLOGY.md`.

## Adding a gene

Append it to `data/genes.json` with its primary pediatric cancer and a one-line
rationale, and add an evidence row to `data/sample_evidence.json`.
