# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

from vial_sanguis.config import RunConfig
from vial_sanguis.metrics import first_times


def _row(t: int, n: int = 200, p_biter: float = 0.0, heme: float = 0.0, wound: float = 0.0, bite: float = 0.0) -> dict:
    return {
        "t": t,
        "n": n,
        "p_biter": p_biter,
        "mean_energy_wound": wound,
        "mean_energy_bite": bite,
        "qtl_mean": {"heme_safe": heme},
    }


def test_heme_clock_ignores_mean_trip_without_blood() -> None:
    cfg = RunConfig(t_starve=5, fruit_forever=False)
    recs = [
        _row(0, n=1000),
        _row(16, n=156, heme=0.13, wound=0.03, bite=0.0),
        _row(40, n=1200, heme=0.13, wound=0.40, bite=0.0),
    ]
    times = first_times(recs, cfg)
    assert times["t_heme_safe_rise_mean"] == 16
    assert times["t_heme_safe_rise"] == 40


def test_held_biter_requires_persistence() -> None:
    cfg = RunConfig(held_biter_p=0.05, held_biter_w=3)
    recs = [
        _row(0),
        _row(10, p_biter=0.001),
        _row(11, p_biter=0.0),
        _row(20, p_biter=0.06),
        _row(21, p_biter=0.07),
        _row(22, p_biter=0.08),
    ]
    times = first_times(recs, cfg)
    assert times["t_first_biter"] == 10
    assert times["t_held_biter"] == 20
    assert times["t_majority_biter"] is None


def test_held_biter_resets_on_gap() -> None:
    cfg = RunConfig(held_biter_p=0.05, held_biter_w=3)
    recs = [
        _row(1, p_biter=0.06),
        _row(2, p_biter=0.06),
        _row(3, p_biter=0.0),
        _row(4, p_biter=0.06),
        _row(5, p_biter=0.06),
    ]
    times = first_times(recs, cfg)
    assert times["t_first_biter"] == 1
    assert times["t_held_biter"] is None
