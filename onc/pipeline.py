"""The six-stage ONC research pipeline.

    1. SCREEN   pick a candidate gene
    2. SCORE    query the six evidence sources, compute the weighted total
    3. LOCK     SHA-256 hash the prediction (sealed before any test data)
    4. TEST     reveal the held-out dependency value
    5. VERIFY   independent verifier rules PASS / FAIL
    6. RECEIPT  append an immutable, hash-chained record

The ordering guarantee is enforced in code: the prediction dict is hashed in
stage 3 and the held-out value is only read in stage 4.
"""

from __future__ import annotations

from dataclasses import dataclass

from onc.genes import Gene, Pool, pool as _pool
from onc.hashchain import HashChain, Receipt, hash_prediction
from onc.scoring import ScoreCard, score_gene
from onc.sources.base import OfflineEvidence
from onc.verify import verify


@dataclass
class Experiment:
    gene: Gene
    scorecard: ScoreCard
    prediction: dict
    receipt: Receipt

    @property
    def passed(self) -> bool:
        return self.receipt.verdict == "PASS"


def run_experiment(
    symbol: str,
    chain: HashChain,
    evidence: OfflineEvidence | None = None,
) -> Experiment:
    """Run one gene end-to-end and append its receipt to ``chain``."""
    evidence = evidence or OfflineEvidence()

    # 1. SCREEN + resolve the gene's metadata
    gene = _pool().by_symbol(symbol)

    # 2. SCORE
    scorecard = score_gene(symbol, dict(evidence.evidence(symbol)))

    # 3. LOCK — seal the prediction before any test data is touched
    prediction = {
        "symbol": symbol,
        "cancer": gene.cancer,
        "scores": scorecard.as_dict()["scores"],
        "weighted": scorecard.weighted,
        "predicted_dependency": scorecard.confirmed,
    }
    sealed = hash_prediction(prediction)

    # 4. TEST — only now may we look at the held-out value
    held_out = evidence.held_out_dependency(symbol)

    # 5. VERIFY — independent judge
    verdict = verify(scorecard.confirmed, held_out)

    # 6. RECEIPT
    outcome = {
        "held_out_dependency": round(held_out, 4),
        "actual_dependency": verdict.actual,
        "detail": verdict.detail,
    }
    receipt = chain.append(prediction=prediction, outcome=outcome, verdict=verdict.label)
    assert receipt.prediction_hash == sealed  # lock integrity

    return Experiment(gene=gene, scorecard=scorecard, prediction=prediction, receipt=receipt)


def run_pass(chain: HashChain, evidence: OfflineEvidence | None = None) -> list[Experiment]:
    """Run one full pass over the gene pool."""
    evidence = evidence or OfflineEvidence()
    p: Pool = _pool()
    results: list[Experiment] = []
    for _ in range(len(p)):
        gene = p.next()
        results.append(run_experiment(gene.symbol, chain, evidence))
    return results
