# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

from vial_sanguis.config import RunConfig
from vial_sanguis.population import run_generations


def test_extinction_is_logged_not_padded() -> None:
    cfg = RunConfig(
        n=16,
        generations=20,
        seed=9,
        t_starve=0,
        fruit_init=0.0,
        sigma_init=0.0,
        sigma_mu=0.0,
        p_rare=0.0,
        lambda_init=0.0,
        u=0.0,
        n_floor=8,
        fail_n_min=8,
        fail_viability=0.5,
        n_ceiling=16,
        mating_mode="random",
        arm="random",
    )
    result = run_generations(cfg)
    assert result["extinct"] is True
    last = result["generations"][-1]
    assert last["extinct"] is True
    assert last["n"] < 16
    ns = [g["n"] for g in result["generations"]]
    assert min(ns) <= 8
