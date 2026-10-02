"""The ONC hash chain: tamper-evident experiment receipts.

Every experiment produces a :class:`Receipt`. The *prediction* portion of the
receipt is SHA-256 hashed before any test outcome is known, so the prediction
can never be back-dated or edited. Each receipt also records the hash of the
previous receipt, chaining the whole log together: alter any past prediction and
its hash changes, which breaks every link that follows it.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

GENESIS = "0" * 64  # prev_hash of the first receipt


def _canonical(obj: Any) -> str:
    """Deterministic JSON so identical content always hashes identically."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def hash_prediction(prediction: dict) -> str:
    """SHA-256 of the sealed prediction payload."""
    return hashlib.sha256(_canonical(prediction).encode("utf-8")).hexdigest()


@dataclass
class Receipt:
    """An immutable record of one experiment.

    ``prediction_hash`` is computed over ``prediction`` alone, *before* the
    ``outcome`` and ``verdict`` fields are filled in.
    """

    index: int
    prediction: dict
    prediction_hash: str
    outcome: dict
    verdict: str          # "PASS" or "FAIL"
    prev_hash: str
    hash: str = field(default="")

    def __post_init__(self) -> None:
        if not self.hash:
            self.hash = self._compute_hash()

    def _compute_hash(self) -> str:
        body = {
            "index": self.index,
            "prediction_hash": self.prediction_hash,
            "outcome": self.outcome,
            "verdict": self.verdict,
            "prev_hash": self.prev_hash,
        }
        return hashlib.sha256(_canonical(body).encode("utf-8")).hexdigest()

    def recompute(self) -> str:
        return self._compute_hash()

    def to_dict(self) -> dict:
        return asdict(self)


class HashChain:
    """An append-only chain of receipts with full verifiability."""

    def __init__(self) -> None:
        self._receipts: list[Receipt] = []

    def __len__(self) -> int:
        return len(self._receipts)

    def __iter__(self):
        return iter(self._receipts)

    @property
    def head(self) -> str:
        return self._receipts[-1].hash if self._receipts else GENESIS

    def append(self, prediction: dict, outcome: dict, verdict: str) -> Receipt:
        receipt = Receipt(
            index=len(self._receipts),
            prediction=prediction,
            prediction_hash=hash_prediction(prediction),
            outcome=outcome,
            verdict=verdict,
            prev_hash=self.head,
        )
        self._receipts.append(receipt)
        return receipt

    def verify(self) -> bool:
        """Return True only if every link and prediction hash is intact."""
        prev = GENESIS
        for r in self._receipts:
            if r.prev_hash != prev:
                return False
            if r.prediction_hash != hash_prediction(r.prediction):
                return False
            if r.hash != r.recompute():
                return False
            prev = r.hash
        return True

    # --- persistence -----------------------------------------------------

    def save(self, path: str | Path) -> None:
        payload = [r.to_dict() for r in self._receipts]
        Path(path).write_text(_canonical(payload), encoding="utf-8")

    @classmethod
    def load(cls, path: str | Path) -> "HashChain":
        chain = cls()
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        chain._receipts = [Receipt(**r) for r in data]
        return chain
