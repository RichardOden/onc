"""Clinical evidence (weight 10%) from ClinicalTrials.gov.

Existing *pediatric* trials against a target are supportive evidence, but a
trial that has already failed is a penalty, not a bonus. ONC nets ongoing and
completed-successful trials against terminated/failed ones onto [0, 1].
"""

from __future__ import annotations

from onc.sources.base import EvidenceSource, OfflineEvidence

CTGOV_API = "https://clinicaltrials.gov/api/v2/studies"


def net_trial_score(ongoing: int, succeeded: int, failed: int) -> float:
    """Net supportive trials against failures into [0, 1]."""
    support = ongoing + 2 * succeeded
    penalty = 1.5 * failed
    raw = support - penalty
    if raw <= 0:
        return 0.0
    return min(1.0, raw / 5.0)


class ClinicalSource(EvidenceSource):
    name = "clinical"

    def __init__(self, offline: OfflineEvidence | None = None) -> None:
        self._offline = offline or OfflineEvidence()

    def score(self, symbol: str) -> float:
        return float(self._offline.evidence(symbol).get("clinical", 0.0))
