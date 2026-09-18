"""Novelty evidence (weight 15%) from PubMed, inverted.

Understudied genes score *higher*: ONC is built to hunt the overlooked. The raw
signal is the PubMed publication count for the gene in a pediatric-cancer
context; it is inverted with a log transform so a gene with few papers scores
near 1.0 and a heavily studied gene scores near 0.0.
"""

from __future__ import annotations

import math

from onc.sources.base import EvidenceSource, OfflineEvidence

PUBMED_ESEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

# publication count at which novelty is considered exhausted (score -> 0)
_SATURATION = 5000


def count_to_novelty(n_papers: int) -> float:
    """Invert a publication count into a novelty score in [0, 1]."""
    n = max(0, int(n_papers))
    return max(0.0, 1.0 - math.log1p(n) / math.log1p(_SATURATION))


class NoveltySource(EvidenceSource):
    name = "novelty"

    def __init__(self, offline: OfflineEvidence | None = None) -> None:
        self._offline = offline or OfflineEvidence()

    def score(self, symbol: str) -> float:
        return float(self._offline.evidence(symbol).get("novelty", 0.0))
