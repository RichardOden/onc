"""Tests for the end-to-end pipeline and gene pool."""

from onc.genes import GENE_POOL, pool
from onc.hashchain import HashChain, hash_prediction
from onc.pipeline import run_experiment, run_pass
from onc.sources.base import OfflineEvidence


def test_gene_pool_has_thirty_unique_genes():
    assert len(GENE_POOL) == 30
    symbols = [g.symbol for g in GENE_POOL]
    assert len(set(symbols)) == 30


def test_pool_resets_when_exhausted():
    p = pool()
    n = len(p)
    for _ in range(n):
        p.next()
    assert len(p) == 0
    p.next()                      # triggers reset
    assert len(p) == n - 1


def test_single_experiment_produces_sealed_receipt():
    chain = HashChain()
    exp = run_experiment("MYCN", chain)
    # prediction never contains the held-out test value
    assert "_test_dependency" not in exp.prediction["scores"]
    assert exp.receipt.prediction_hash == hash_prediction(exp.prediction)
    assert exp.receipt.verdict in {"PASS", "FAIL"}
    assert chain.verify()


def test_lock_precedes_test_outcome_is_recorded_separately():
    chain = HashChain()
    exp = run_experiment("MYCN", chain)
    # outcome (test data) is stored outside the sealed prediction
    assert "held_out_dependency" in exp.receipt.outcome
    assert "held_out_dependency" not in exp.prediction


def test_full_pass_scores_every_gene_and_chain_stays_intact():
    chain = HashChain()
    results = run_pass(chain)
    assert len(results) == len(GENE_POOL)
    assert chain.verify()
    # there should be a realistic mix of confirmations and verdicts
    confirmed = sum(1 for e in results if e.scorecard.confirmed)
    failures = sum(1 for e in results if not e.passed)
    assert confirmed > 0
    assert failures > 0          # ONC publishes its failures


def test_offline_evidence_covers_whole_pool():
    ev = OfflineEvidence()
    for g in GENE_POOL:
        assert {"dependency", "genetics"}.issubset(ev.evidence(g.symbol).keys())
