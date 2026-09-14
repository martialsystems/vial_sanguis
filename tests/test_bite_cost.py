# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

import numpy as np

from vial_sanguis.config import RunConfig
from vial_sanguis.fitness import energy_channels, phenotype, trait_cost
from vial_sanguis.genome import I_PIERCE, I_RASP, I_SALIVA, I_SEEK, init_population


def test_pierce_costs_when_bite_payoff_is_low() -> None:
    cfg = RunConfig(n=1, seed=1)
    z = np.zeros((1, 12), dtype=np.float64)
    z[0, I_PIERCE] = 0.8
    e = energy_channels(z, 0.0, 1.0)
    assert float(e.bite[0]) < cfg.eps_bite
    cost = trait_cost(z, e.bite, e.host, e.heme_load, cfg)
    z0 = z.copy()
    z0[0, I_PIERCE] = 0.0
    e0 = energy_channels(z0, 0.0, 1.0)
    cost0 = trait_cost(z0, e0.bite, e0.host, e0.heme_load, cfg)
    quad = cfg.c_quad * (0.8 ** 2)
    standing = cfg.c_pierce * 0.8
    assert float(cost[0]) > float(cost0[0])
    assert abs(float(cost[0] - cost0[0]) - (quad + standing)) < 1e-12


def test_pierce_cost_drops_when_bite_pays() -> None:
    cfg = RunConfig(n=1, seed=1)
    z = np.zeros((1, 12), dtype=np.float64)
    z[0, I_RASP] = 1.5
    z[0, I_PIERCE] = 1.2
    z[0, I_SALIVA] = 1.0
    z[0, I_SEEK] = 1.0
    e = energy_channels(z, 0.0, 1.0)
    assert float(e.bite[0]) > cfg.eps_bite
    cost = trait_cost(z, e.bite, e.host, e.heme_load, cfg)
    z0 = z.copy()
    z0[0, I_PIERCE] = 0.0
    e0 = energy_channels(z0, 0.0, 1.0)
    cost0 = trait_cost(z0, e0.bite, e0.host, e0.heme_load, cfg)
    pierce_term = cfg.c_pierce * 1.2
    assert float(cost[0]) < float(cost0[0]) + pierce_term - 1e-9


def test_lethal_homozygote_zeroes_v_load() -> None:
    cfg = RunConfig(n=2, seed=7, lambda_init=0.0)
    pop = init_population(cfg, np.random.default_rng(7))
    pop.load[0, 0, :] = 1
    pop.load[1, 0, 0] = 1
    pop.load[1, 0, 1] = 0
    ph = phenotype(pop, cfg)
    assert float(ph.v_load[0]) == 0.0
    assert float(ph.fertility[0]) == 0.0
    assert float(ph.v_load[1]) == 1.0
