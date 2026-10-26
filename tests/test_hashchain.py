"""Tests for the tamper-evident hash chain."""

from onc.hashchain import GENESIS, HashChain, hash_prediction


def _pred(symbol, dep):
    return {"symbol": symbol, "predicted_dependency": dep}


def test_hash_is_deterministic():
    p = _pred("MYCN", True)
    assert hash_prediction(p) == hash_prediction(dict(reversed(list(p.items()))))


def test_chain_links_and_verifies():
    chain = HashChain()
    assert chain.head == GENESIS
    r0 = chain.append(_pred("MYCN", True), {"held_out_dependency": 0.9}, "PASS")
    r1 = chain.append(_pred("RB1", False), {"held_out_dependency": 0.1}, "PASS")
    assert r0.prev_hash == GENESIS
    assert r1.prev_hash == r0.hash
    assert chain.verify()


def test_tampering_breaks_the_chain():
    chain = HashChain()
    chain.append(_pred("MYCN", True), {"held_out_dependency": 0.9}, "PASS")
    chain.append(_pred("RB1", False), {"held_out_dependency": 0.1}, "PASS")
    assert chain.verify()

    # Alter a sealed prediction after the fact.
    next(iter(chain)).prediction["predicted_dependency"] = False
    assert not chain.verify()


def test_save_and_load_roundtrip(tmp_path):
    chain = HashChain()
    chain.append(_pred("MYCN", True), {"held_out_dependency": 0.9}, "PASS")
    chain.append(_pred("ALK", True), {"held_out_dependency": 0.8}, "PASS")
    path = tmp_path / "run.chain.json"
    chain.save(path)

    reloaded = HashChain.load(path)
    assert len(reloaded) == 2
    assert reloaded.verify()
    assert reloaded.head == chain.head
