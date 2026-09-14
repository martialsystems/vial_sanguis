# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

import json
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]


def _load(name: str) -> dict | None:
    path = REPO / "logs" / name
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def test_vampire_seed1_order_if_present() -> None:
    run = _load("vampire_2500_s1.json")
    if run is None:
        pytest.skip("local lock not generated")
    assert run["min_n"] <= 20 or run["extinct"]
    if run["extinct"]:
        return
    assert run["t_first_biter"] is not None
    assert run["t_recover"] is not None
    assert int(run["t_first_biter"]) > int(run["t_recover"])
    rec = next(g for g in run["generations"] if g["t"] == run["t_first_biter"])
    assert rec["qtl_mean"]["rasp"] > rec["qtl_mean"]["pierce"]
    if run["t_heme_safe_rise"] is not None:
        assert int(run["t_heme_safe_rise"]) > int(run["t_first_biter"])


def test_random_seed1_crash_if_present() -> None:
    run = _load("random_2500_s1.json")
    if run is None:
        pytest.skip("local lock not generated")
    assert run["min_n"] <= 20 or run["extinct"]


def test_fruit_forever_if_present() -> None:
    run = _load("fruit_forever_400_s1.json")
    if run is None:
        pytest.skip("local lock not generated")
    gens = [g for g in run["generations"] if g["t"] <= 400]
    assert max(g["p_biter"] for g in gens) <= 0.05
    first, last = gens[0], gens[-1]
    assert last["qtl_mean"]["digest"] <= first["qtl_mean"]["digest"] + 0.05
    assert last["qtl_mean"]["heme_safe"] <= first["qtl_mean"]["heme_safe"] + 0.05
