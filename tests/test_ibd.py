# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

from vial_sanguis.config import RunConfig
from vial_sanguis.population import run_generations


def test_ibd_rises_under_tiny_n() -> None:
    cfg = RunConfig(
        n=12,
        generations=24,
        seed=3,
        fruit_forever=True,
        mating_mode="random",
        arm="random",
        n_ceiling=12,
        cap="on",
        n_floor=4,
        fail_n_min=2,
        fail_viability=0.0,
        lambda_init=1.0,
        p_rare=0.0,
        s_let=0.0,
        s_sub=0.05,
    )
    result = run_generations(cfg)
    gens = result["generations"]
    assert gens[0]["F"] == 0.0
    fs = [g["F"] for g in gens]
    f_late = fs[-1]
    n_half = max(3, len(fs) // 3)
    early_mean = sum(fs[:n_half]) / n_half
    late_mean = sum(fs[-n_half:]) / n_half
    assert f_late > 0.15
    assert late_mean > early_mean
