# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

import numpy as np

from vial_sanguis.config import RunConfig
from vial_sanguis.fitness import phenotype
from vial_sanguis.genome import init_population
from vial_sanguis.mating import freeze_sigma0, mating_traits, pair


def test_knn_pairs_do_not_exceed_males() -> None:
    cfg = RunConfig(n=30, seed=1, mating_mode="assortative_knn", k=3)
    rng = np.random.default_rng(1)
    pop = init_population(cfg, rng)
    ph = phenotype(pop, cfg)
    sigma0 = freeze_sigma0(mating_traits(ph, pop.t, cfg), cfg)
    pairing = pair(pop, ph, cfg, rng, sigma0)
    assert pairing.n_accepted <= int(np.sum(pop.sex == 1))
    assert pairing.n_accepted <= int(np.sum(pop.sex == 0))
    if pairing.n_accepted:
        assert len(set(pairing.male_idx.tolist())) == pairing.n_accepted


def test_random_mode_accepts_pairs() -> None:
    cfg = RunConfig(n=40, seed=2, mating_mode="random")
    rng = np.random.default_rng(2)
    pop = init_population(cfg, rng)
    ph = phenotype(pop, cfg)
    sigma0 = freeze_sigma0(mating_traits(ph, pop.t, cfg), cfg)
    pairing = pair(pop, ph, cfg, rng, sigma0)
    assert pairing.n_accepted > 0
