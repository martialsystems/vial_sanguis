# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

from vial_sanguis.config import RunConfig
from vial_sanguis.population import run_generations


def test_fruit_forever_does_not_evolve_biters() -> None:
    cfg = RunConfig(
        n=60,
        generations=50,
        seed=1,
        fruit_forever=True,
        t_starve=5,
        mating_mode="assortative_knn",
        k=3,
        n_ceiling=60,
        cap="on",
        fail_n_min=2,
        fail_viability=0.0,
        arm="vampire",
    )
    result = run_generations(cfg)
    assert result["extinct"] is False
    ns = [g["n"] for g in result["generations"]]
    assert min(ns) >= 40
    last = result["generations"][-1]
    first = result["generations"][0]
    assert last["p_biter"] <= 0.05
    assert last["mean_energy_fruit"] > 0.5
    max_p = max(g["p_biter"] for g in result["generations"])
    assert max_p <= 0.05
    assert last["qtl_mean"]["digest"] <= first["qtl_mean"]["digest"] + 0.08
    assert last["qtl_mean"]["heme_safe"] <= first["qtl_mean"]["heme_safe"] + 0.08
    assert abs(last["qtl_mean"]["digest"]) < 0.15
    assert abs(last["qtl_mean"]["heme_safe"]) < 0.15
