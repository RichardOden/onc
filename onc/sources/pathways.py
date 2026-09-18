"""Pathways evidence (weight 15%) from Reactome.

Reactome (reactome.org) describes curated biological pathways. ONC asks whether
a gene participates in a cancer-relevant developmental pathway; genes wired into
the proliferation/differentiation programs that pediatric tumors hijack score
higher.
"""

from __future__ import annotations

from onc.sources.base import EvidenceSource, OfflineEvidence

REACTOME_CONTENT = "https://reactome.org/ContentService"


class PathwaysSource(EvidenceSource):
    name = "pathways"

    def __init__(self, offline: OfflineEvidence | None = None) -> None:
        self._offline = offline or OfflineEvidence()

    def score(self, symbol: str) -> float:
        return float(self._offline.evidence(symbol).get("pathways", 0.0))
