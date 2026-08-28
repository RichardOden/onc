"""The ONC gene pool.

Thirty genes with known or emerging roles in pediatric malignancies. Each gene
carries the primary childhood cancer it is implicated in and a one-line
rationale for why it is on the board. As a gene is investigated it is removed
from the active pool; when the pool is exhausted it resets for a fresh pass.

The pool is loaded from ``data/genes.json`` so it can be audited and extended
without touching code.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

_DATA = Path(__file__).resolve().parent.parent / "data" / "genes.json"


@dataclass(frozen=True)
class Gene:
    """A single candidate gene."""

    symbol: str
    cancer: str
    rationale: str

    def __str__(self) -> str:  # pragma: no cover - cosmetic
        return f"{self.symbol} ({self.cancer})"


def _load_pool() -> list[Gene]:
    raw = json.loads(_DATA.read_text(encoding="utf-8"))
    return [Gene(**g) for g in raw]


GENE_POOL: list[Gene] = _load_pool()


class Pool:
    """A resettable pool of genes drawn one at a time.

    >>> p = Pool()
    >>> first = p.next()
    >>> first in GENE_POOL
    True
    >>> len(p) == len(GENE_POOL) - 1
    True
    """

    def __init__(self, genes: list[Gene] | None = None) -> None:
        self._all: list[Gene] = list(genes if genes is not None else GENE_POOL)
        self._active: list[Gene] = list(self._all)

    def __len__(self) -> int:
        return len(self._active)

    def __iter__(self) -> Iterator[Gene]:
        return iter(self._active)

    def next(self) -> Gene:
        """Pop the next candidate; reset the pool when exhausted."""
        if not self._active:
            self.reset()
        return self._active.pop(0)

    def reset(self) -> None:
        self._active = list(self._all)

    def by_symbol(self, symbol: str) -> Gene:
        for g in self._all:
            if g.symbol.upper() == symbol.upper():
                return g
        raise KeyError(f"{symbol!r} is not in the ONC gene pool")


def pool() -> Pool:
    """Return a fresh pool over the full gene set."""
    return Pool()
