"""Genetics evidence (weight 20%) from Open Targets and COSMIC.

Open Targets (opentargets.org) aggregates gene-disease association scores;
COSMIC (cancer.sanger.ac.uk/cosmic) catalogues somatic mutations in cancer. ONC
combines the pediatric-cancer association strength from both into [0, 1].
"""

from __future__ import annotations

from onc.sources.base import EvidenceSource, OfflineEvidence

OPEN_TARGETS_GRAPHQL = "https://api.platform.opentargets.org/api/v4/graphql"
COSMIC = "https://cancer.sanger.ac.uk/cosmic"


class GeneticsSource(EvidenceSource):
    name = "genetics"

    def __init__(self, offline: OfflineEvidence | None = None) -> None:
        self._offline = offline or OfflineEvidence()

    def score(self, symbol: str) -> float:
        return float(self._offline.evidence(symbol).get("genetics", 0.0))
