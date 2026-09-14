# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

import numpy as np

from vial_sanguis.config import RunConfig
from vial_sanguis.genome import (
    BLOOD_QTLS,
    FEMALE,
    HOST_MOUTHPART,
    I_FRUIT,
    QTL_AUTO,
    additive_z,
    init_population,
)


def test_qtl_order_and_shape() -> None:
    assert QTL_AUTO[:12] == (
        "fruit_use",
        "fluid_detect",
        "rasp",
        "pierce",
        "saliva",
        "seek",
        "locomotion",
        "fertility_circuit",
        "stab",
        "fa",
        "digest",
        "heme_safe",
    )
    cfg = RunConfig(n=40, seed=1, generations=1)
    pop = init_population(cfg, np.random.default_rng(1))
    assert pop.qtl_auto.shape == (40, 12, 2)
    assert pop.load.shape == (40, 64, 2)
    assert pop.founder_qtl_auto.shape == (40, 12, 2)
    assert pop.n == 40
    assert pop.t == 0


def test_ancestral_fruit_and_host() -> None:
    cfg = RunConfig(n=200, seed=2, generations=1)
    pop = init_population(cfg, np.random.default_rng(2))
    z = additive_z(pop)
    assert abs(float(z[:, I_FRUIT].mean()) - cfg.fruit_init) < 0.05
    host = z[:, list(HOST_MOUTHPART) + list(BLOOD_QTLS)]
    assert abs(float(host.mean())) < 0.03
    assert float(np.abs(host).mean()) < 0.12


def test_load_is_heterozygous_poisson() -> None:
    cfg = RunConfig(n=80, seed=3, lambda_init=4.0, generations=1)
    pop = init_population(cfg, np.random.default_rng(3))
    hom = (pop.load[:, :, 0] == 1) & (pop.load[:, :, 1] == 1)
    het = pop.load[:, :, 0] != pop.load[:, :, 1]
    assert int(hom.sum()) == 0
    mean_het = float(het.sum(axis=1).mean())
    assert 2.0 < mean_het < 6.5


def test_founder_ids_unique() -> None:
    cfg = RunConfig(n=12, seed=4, generations=1)
    pop = init_population(cfg, np.random.default_rng(4))
    ids = pop.founder_qtl_auto.reshape(-1)
    assert len(set(int(x) for x in ids)) == ids.size


def test_sex_ratio_roughly_equal() -> None:
    cfg = RunConfig(n=200, seed=5, sex_imbalance_max=50, generations=1)
    pop = init_population(cfg, np.random.default_rng(5))
    nf = int(np.sum(pop.sex == FEMALE))
    assert abs(nf - (200 - nf)) <= 50
