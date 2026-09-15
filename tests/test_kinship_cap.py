# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

import numpy as np

from vial_sanguis.config import RunConfig
from vial_sanguis.fitness import phenotype
from vial_sanguis.genome import init_population
from vial_sanguis.mating import freeze_sigma0, mating_traits, pair, pairwise_fm_phi


def test_kinship_cap_off_is_default() -> None:
    cfg = RunConfig()
    assert cfg.kinship_cap is False
    assert cfg.phi_max == 0.25
    assert cfg.t_starve == 5
    assert cfg.k_tears == 40.0
    assert cfg.bite_weight == 1.0
    assert cfg.c_pierce == 0.05
    assert cfg.c_digest == 0.40
    assert cfg.c_heme == 0.40
    assert cfg.c_heme_in == 0.30
    assert cfg.beta_heme == 2.0
    assert cfg.survive_thresh_host == 0.075
    assert cfg.n_floor == 8
    assert cfg.n_ceiling == 1200
    assert cfg.kinship_cap_on == "immediate"
    assert cfg.kinship_recover_n == 50
    assert cfg.host_shift_at == "off"
    assert cfg.skin_tough == 1.0
    assert cfg.clot_without_saliva is False
    assert cfg.wound_after_hold == "open"


def test_kinship_cap_rejects_high_phi_pairs() -> None:
    cfg = RunConfig(n=24, seed=1, mating_mode="assortative_knn", k=3, kinship_cap=True, phi_max=-0.01)
    rng = np.random.default_rng(1)
    pop = init_population(cfg, rng)
    ph = phenotype(pop, cfg)
    sigma0 = freeze_sigma0(mating_traits(ph, pop.t, cfg), cfg)
    pairing = pair(pop, ph, cfg, rng, sigma0)
    assert pairing.n_accepted == 0
    assert pairing.n_kinship_reject > 0


def test_kinship_cap_allows_unrelated_founders() -> None:
    cfg = RunConfig(n=40, seed=2, mating_mode="assortative_knn", k=3, kinship_cap=True, phi_max=0.25)
    rng = np.random.default_rng(2)
    pop = init_population(cfg, rng)
    ph = phenotype(pop, cfg)
    sigma0 = freeze_sigma0(mating_traits(ph, pop.t, cfg), cfg)
    pairing = pair(pop, ph, cfg, rng, sigma0)
    assert pairing.n_accepted > 0
    f_idx = pairing.female_idx
    m_idx = pairing.male_idx
    phi = pairwise_fm_phi(pop.founder_qtl_auto[f_idx], pop.founder_qtl_auto[m_idx])
    for i in range(pairing.n_accepted):
        assert float(phi[i, i]) <= cfg.phi_max + 1e-12
