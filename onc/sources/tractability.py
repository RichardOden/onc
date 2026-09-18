"""Tractability evidence (weight 10%) from ChEMBL.

A perfect target is useless if no drug can reach it. ChEMBL
(ebi.ac.uk/chembl) tracks bioactive molecules and target druggability. ONC maps
the best available tractability bucket (small molecule / antibody / clinical
precedent) onto [0, 1].
"""

from __future__ import annotations

from onc.sources.base import EvidenceSource, OfflineEvidence

CHEMBL_API = "https://www.ebi.ac.uk/chembl/api/data"

# tractability bucket -> score
BUCKETS = {
    "clinical_precedent": 1.0,
    "discovery_precedent": 0.6,
    "predicted_tractable": 0.3,
    "unknown": 0.0,
}


class TractabilitySource(EvidenceSource):
    name = "tractability"

    def __init__(self, offline: OfflineEvidence | None = None) -> None:
        self._offline = offline or OfflineEvidence()

    def score(self, symbol: str) -> float:
        return float(self._offline.evidence(symbol).get("tractability", 0.0))
