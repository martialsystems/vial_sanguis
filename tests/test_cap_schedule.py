# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

from vial_sanguis.config import RunConfig
from vial_sanguis.population import run_generations


def test_recover_schedule_waits_until_n50_after_starve() -> None:
    cfg = RunConfig(
        n=80,
        generations=12,
        seed=1,
        t_starve=2,
        fruit_forever=True,
        mating_mode="assortative_knn",
        k=3,
        kinship_cap=True,
        kinship_cap_on="recover",
        kinship_recover_n=50,
        n_ceiling=80,
        cap="on",
        fail_n_min=1,
        fail_viability=0.0,
        arm="vampire",
    )
    result = run_generations(cfg)
    assert result["t_kinship_on"] == cfg.t_starve
    assert result["config"]["kinship_cap_on"] == "recover"
    assert result["config"]["phi_max"] == 0.25


def test_recover_never_arms_if_n_stays_below_threshold() -> None:
    cfg = RunConfig(
        n=40,
        generations=8,
        seed=1,
        t_starve=1,
        fruit_forever=True,
        mating_mode="assortative_knn",
        k=3,
        kinship_cap=True,
        kinship_cap_on="recover",
        kinship_recover_n=50,
        n_ceiling=40,
        cap="on",
        fail_n_min=1,
        fail_viability=0.0,
    )
    result = run_generations(cfg)
    assert result["t_kinship_on"] is None
    assert result["extinct"] is False


def test_immediate_cap_is_armed_from_start() -> None:
    cfg = RunConfig(
        n=40,
        generations=3,
        seed=1,
        kinship_cap=True,
        kinship_cap_on="immediate",
        fail_n_min=1,
        fail_viability=0.0,
    )
    result = run_generations(cfg)
    assert result["t_kinship_on"] == 0