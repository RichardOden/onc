"""Base classes for evidence sources."""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Mapping

# Canonical order of the six evidence sources.
SOURCE_NAMES = (
    "dependency",
    "genetics",
    "novelty",
    "pathways",
    "tractability",
    "clinical",
)

_SAMPLE = Path(__file__).resolve().parents[2] / "data" / "sample_evidence.json"


class EvidenceSource(ABC):
    """One line of evidence for a gene, normalised to [0, 1]."""

    #: short key used in the score card, e.g. "dependency"
    name: str

    @abstractmethod
    def score(self, symbol: str) -> float:
        """Return a score in [0, 1] for ``symbol`` (higher = stronger)."""
        raise NotImplementedError


class OfflineEvidence:
    """Bundled offline evidence for every gene in the pool.

    Reads ``data/sample_evidence.json`` and exposes the full six-source evidence
    dict for a gene. This is what lets ``onc run`` work out of the box.
    """

    def __init__(self, path: str | Path | None = None) -> None:
        self._data: dict[str, dict[str, float]] = json.loads(
            Path(path or _SAMPLE).read_text(encoding="utf-8")
        )

    def evidence(self, symbol: str) -> Mapping[str, float]:
        try:
            return self._data[symbol.upper()]
        except KeyError as exc:  # pragma: no cover - defensive
            raise KeyError(f"no offline evidence for {symbol!r}") from exc

    def held_out_dependency(self, symbol: str) -> float:
        """The 'true' dependency used as held-out test data.

        In the offline fixture this is stored under ``_test_dependency`` and is
        deliberately *not* returned by :meth:`evidence`, mirroring how the live
        pipeline keeps test data sealed away during scoring.
        """
        return float(self._data[symbol.upper()].get("_test_dependency", 0.0))

    def symbols(self) -> list[str]:
        return list(self._data.keys())
