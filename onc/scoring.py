"""The ONC scoring engine.

Six independent evidence sources, each weighted toward pediatric relevance, are
fused into a single weighted total in [0, 1]. A gene is *confirmed* as a
candidate worth laboratory attention only if it clears two thresholds at once:

    weighted total  > 0.50   AND   dependency score > 0.40

The weights are deliberately public and version-pinned: changing them changes
the science, so they live in one place and are covered by tests.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping

# Evidence source -> weight. Must sum to 1.0.
WEIGHTS: dict[str, float] = {
    "dependency": 0.30,   # DepMap CRISPR knockout screens
    "genetics": 0.20,     # Open Targets + COSMIC
    "novelty": 0.15,      # PubMed publication counts, inverted
    "pathways": 0.15,     # Reactome
    "tractability": 0.10, # ChEMBL
    "clinical": 0.10,     # ClinicalTrials.gov
}

# Confirmation thresholds.
MIN_WEIGHTED = 0.50
MIN_DEPENDENCY = 0.40

assert abs(sum(WEIGHTS.values()) - 1.0) < 1e-9, "ONC weights must sum to 1.0"


@dataclass(frozen=True)
class ScoreCard:
    """The per-source scores and fused total for one gene."""

    symbol: str
    scores: Mapping[str, float]
    weighted: float = field(init=False)

    def __post_init__(self) -> None:
        total = sum(WEIGHTS[k] * self.scores.get(k, 0.0) for k in WEIGHTS)
        object.__setattr__(self, "weighted", round(total, 4))

    @property
    def dependency(self) -> float:
        return self.scores.get("dependency", 0.0)

    @property
    def confirmed(self) -> bool:
        return is_confirmed(self.weighted, self.dependency)

    def as_dict(self) -> dict:
        return {
            "symbol": self.symbol,
            "scores": {k: round(self.scores.get(k, 0.0), 4) for k in WEIGHTS},
            "weighted": self.weighted,
            "confirmed": self.confirmed,
        }


def _clamp(x: float) -> float:
    return max(0.0, min(1.0, float(x)))


def score_gene(symbol: str, evidence: Mapping[str, float]) -> ScoreCard:
    """Build a :class:`ScoreCard` from per-source evidence in [0, 1].

    Unknown sources default to 0.0 (absence of evidence is not evidence).
    """
    scores = {k: _clamp(evidence.get(k, 0.0)) for k in WEIGHTS}
    return ScoreCard(symbol=symbol, scores=scores)


def is_confirmed(weighted: float, dependency: float) -> bool:
    """Apply the two-threshold confirmation rule."""
    return weighted > MIN_WEIGHTED and dependency > MIN_DEPENDENCY
