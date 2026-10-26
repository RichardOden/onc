"""Tests for the scoring engine."""

import pytest

from onc.scoring import MIN_DEPENDENCY, MIN_WEIGHTED, WEIGHTS, is_confirmed, score_gene


def test_weights_sum_to_one():
    assert abs(sum(WEIGHTS.values()) - 1.0) < 1e-9


def test_weighted_total_is_linear_combination():
    evidence = {k: 1.0 for k in WEIGHTS}
    card = score_gene("TEST", evidence)
    assert card.weighted == pytest.approx(1.0)

    evidence = {k: 0.0 for k in WEIGHTS}
    assert score_gene("TEST", evidence).weighted == pytest.approx(0.0)


def test_scores_are_clamped():
    card = score_gene("TEST", {"dependency": 5.0, "genetics": -2.0})
    assert card.scores["dependency"] == 1.0
    assert card.scores["genetics"] == 0.0


def test_unknown_source_defaults_to_zero():
    card = score_gene("TEST", {"dependency": 1.0})
    assert card.scores["clinical"] == 0.0


def test_confirmation_requires_both_thresholds():
    # high weighted but low dependency -> not confirmed
    assert not is_confirmed(0.80, 0.30)
    # adequate dependency but low weighted -> not confirmed
    assert not is_confirmed(0.40, 0.90)
    # both cleared -> confirmed
    assert is_confirmed(0.60, 0.50)


def test_threshold_boundaries_are_strict():
    assert not is_confirmed(MIN_WEIGHTED, 0.9)       # must be > not >=
    assert not is_confirmed(0.9, MIN_DEPENDENCY)
