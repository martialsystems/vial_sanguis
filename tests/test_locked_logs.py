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
    assert run.get("t_held_biter") is not None
    assert run.get("t_wound_load") is not None
    assert int(run["t_wound_load"]) <= int(run["t_heme_safe_rise"])
    if run["t_heme_safe_rise"] is not None:
        rec_h = next(g for g in run["generations"] if g["t"] == run["t_heme_safe_rise"])
        blood = float(rec_h["mean_energy_wound"]) + float(rec_h["mean_energy_bite"])
        assert blood > 0.05


def test_random_seed1_crash_if_present() -> None:
    run = _load("random_2500_s1.json")
    if run is None:
        pytest.skip("local lock not generated")
    assert run["min_n"] <= 20 or run["extinct"]


def test_seeds_2_and_3_if_present() -> None:
    for seed in (2, 3):
        knn = _load(f"vampire_2500_s{seed}.json")
        rand = _load(f"random_2500_s{seed}.json")
        if knn is None or rand is None:
            pytest.skip("seed 2/3 local locks not generated")
        assert knn["min_n"] <= 20 or knn["extinct"]
        assert rand["min_n"] <= 20 or rand["extinct"]
        if not knn["extinct"]:
            assert knn["t_first_biter"] is not None
            assert knn["t_recover"] is not None
            assert int(knn["t_first_biter"]) > int(knn["t_recover"])
            rec = next(g for g in knn["generations"] if g["t"] == knn["t_first_biter"])
            assert rec["qtl_mean"]["rasp"] > rec["qtl_mean"]["pierce"]
            assert knn.get("t_held_biter") is not None
            assert knn.get("t_wound_load") is not None
            if knn.get("t_heme_safe_rise") is not None:
                assert int(knn["t_wound_load"]) <= int(knn["t_heme_safe_rise"])
                rec_h = next(g for g in knn["generations"] if g["t"] == knn["t_heme_safe_rise"])
                blood = float(rec_h["mean_energy_wound"]) + float(rec_h["mean_energy_bite"])
                assert blood > 0.05
        if not rand["extinct"]:
            last = rand["generations"][-1]
            if float(last["p_biter"]) < 0.05:
                assert rand.get("t_held_biter") is None


def test_fruit_forever_if_present() -> None:
    run = _load("fruit_forever_400_s1.json")
    if run is None:
        pytest.skip("local lock not generated")
    gens = [g for g in run["generations"] if g["t"] <= 400]
    assert max(g["p_biter"] for g in gens) <= 0.05
    first, last = gens[0], gens[-1]
    assert last["qtl_mean"]["digest"] <= first["qtl_mean"]["digest"] + 0.05
    assert last["qtl_mean"]["heme_safe"] <= first["qtl_mean"]["heme_safe"] + 0.05
