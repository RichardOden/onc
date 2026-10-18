"""The independent verifier.

A core rule of ONC: *the scientist cannot grade its own exam.* The verifier is a
separate component that, given a sealed prediction and the revealed held-out
test data, independently rules PASS or FAIL. It never sees the scoring internals
beyond the single bit ONC committed to (``predicted_dependency``).
"""

from __future__ import annotations

from dataclasses import dataclass

# A gene is a true dependency in the held-out data if its dependency value
# clears this bar. Kept separate from scoring thresholds on purpose.
TRUE_DEPENDENCY_CUTOFF = 0.50


@dataclass(frozen=True)
class Verdict:
    passed: bool
    predicted: bool
    actual: bool
    detail: str

    @property
    def label(self) -> str:
        return "PASS" if self.passed else "FAIL"


def verify(predicted_dependency: bool, held_out_dependency: float) -> Verdict:
    """Independently judge a sealed prediction against revealed test data."""
    actual = held_out_dependency >= TRUE_DEPENDENCY_CUTOFF
    passed = predicted_dependency == actual
    detail = (
        f"predicted={'dep' if predicted_dependency else 'no-dep'}, "
        f"actual={'dep' if actual else 'no-dep'} "
        f"(held-out={held_out_dependency:.2f})"
    )
    return Verdict(passed=passed, predicted=predicted_dependency, actual=actual, detail=detail)
