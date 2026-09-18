"""Dependency evidence (weight 30%) from DepMap CRISPR knockout screens.

DepMap (depmap.org) reports a *gene effect* (Chronos) score per gene per cell
line: strongly negative means knocking the gene out kills the cell, i.e. the
cancer depends on it. ONC restricts to pediatric cell lines only and maps the
mean pediatric gene effect onto [0, 1] (stronger dependency -> higher score).

Live mode queries the DepMap download API; offline mode reads the bundled
fixture. See docs/METHODOLOGY.md for the normalisation.
"""

from __future__ import annotations

from onc.sources.base import EvidenceSource, OfflineEvidence

DEPMAP_PORTAL = "https://depmap.org/portal/"


def effect_to_score(gene_effect: float) -> float:
    """Map a Chronos gene-effect value to [0, 1].

    0.0 (no effect) -> 0.0; -1.0 (median common essential) -> ~1.0.
    """
    return max(0.0, min(1.0, -gene_effect))


class DependencySource(EvidenceSource):
    name = "dependency"

    def __init__(self, offline: OfflineEvidence | None = None) -> None:
        self._offline = offline or OfflineEvidence()

    def score(self, symbol: str) -> float:
        return float(self._offline.evidence(symbol).get("dependency", 0.0))
