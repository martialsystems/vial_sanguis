# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

from vial_sanguis.config import RunConfig
from vial_sanguis.population import run_generations


def test_starve_crashes_census() -> None:
    cfg = RunConfig(
        n=120,
        generations=12,
        seed=1,
        t_starve=3,
        mating_mode="assortative_knn",
        k=3,
        n_ceiling=120,
        n_floor=8,
        fail_n_min=2,
        fail_viability=0.0,
        arm="vampire",
    )
    result = run_generations(cfg)
    gens = result["generations"]
    n_before = [g["n"] for g in gens if g["t"] < cfg.t_starve]
    n_after = [g["n"] for g in gens if g["t"] >= cfg.t_starve]
    assert n_before, "need pre-starve records"
    assert n_after, "need post-starve records"
    assert min(n_after) < min(n_before)
    assert min(n_after) <= 40
    for g in gens:
        if g["t"] >= cfg.t_starve:
            assert g["mean_energy_fruit"] == 0.0 or g["n"] == 0


def test_does_not_invent_adults() -> None:
    cfg = RunConfig(
        n=40,
        generations=8,
        seed=11,
        t_starve=2,
        n_ceiling=4000,
        cap="off",
        fail_n_min=1,
        fail_viability=0.0,
    )
    result = run_generations(cfg)
    for g in result["generations"]:
        if g["t"] > 0:
            assert g["n"] <= g["n_viable"]
            assert g["n_viable"] <= g["n_eggs"]
