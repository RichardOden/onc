# Changelog

All notable changes to ONC are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/); this project uses semantic
versioning.

## [0.5.0] - 2026-10-24
### Added
- `onc.verify` independent verifier — the scientist can no longer grade its own exam.
- `onc chain verify` CLI command to validate a saved hash chain.
- Offline evidence fixture so `onc run` works with no network or API keys.
- Test suite covering scoring, hash-chain tamper-evidence, and the full pipeline.

### Changed
- Confirmation rule tightened to require **both** weighted > 0.50 and dependency > 0.40.

## [0.4.0] - 2026-10-02
### Added
- Six-stage pipeline (Screen → Score → Lock → Test → Verify → Receipt).
- SHA-256 hash chain linking every experiment to its predecessor.

## [0.3.0] - 2026-09-14
### Added
- Weighted scoring engine fusing six evidence sources.
- Evidence-source adapter interface + DepMap / Open Targets / PubMed / Reactome / ChEMBL / ClinicalTrials.gov stubs.

## [0.2.0] - 2026-08-28
### Added
- 30-gene pediatric cancer gene pool loaded from `data/genes.json`.
- Resettable pool semantics.

## [0.1.0] - 2026-08-09
### Added
- Project scaffold, package layout, and the ONC narrative.
