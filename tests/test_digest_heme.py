# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

import numpy as np

from vial_sanguis.config import RunConfig
from vial_sanguis.fitness import energy_channels, iron_viability, sigmoid, trait_cost
from vial_sanguis.genome import (
    BLOOD_QTLS,
    I_DIGEST,
    I_FLUID,
    I_HEME,
    I_RASP,
    I_SALIVA,
    QTL_AUTO,
)


def test_digest_is_not_saliva() -> None:
    assert QTL_AUTO[4] == "saliva"
    assert QTL_AUTO[10] == "digest"
    assert QTL_AUTO[11] == "heme_safe"
    assert I_DIGEST not in (4,)
    assert I_DIGEST in BLOOD_QTLS
    assert I_HEME in BLOOD_QTLS


def test_usable_blood_uses_digest_sigmoid() -> None:
    z = np.zeros((2, 12), dtype=np.float64)
    z[:, I_FLUID] = 1.0
    z[:, I_RASP] = 1.0
    z[:, I_SALIVA] = 0.5
    z[0, I_DIGEST] = 0.0
    z[1, I_DIGEST] = 2.0
    e = energy_channels(z, 0.0, 1.0)
    access = e.wound + e.bite
    assert abs(float(e.usable_blood[0]) - float(access[0] * sigmoid(np.array([0.0]))[0])) < 1e-12
    assert abs(float(e.usable_blood[1]) - float(access[1] * sigmoid(np.array([2.0]))[0])) < 1e-12
    assert float(e.usable_blood[1]) > float(e.usable_blood[0])
    # Unused blood is not calories; heme_load still sees full wound+bite.
    assert abs(float(e.heme_load[0]) - float(access[0])) < 1e-12
    assert abs(float(e.heme_load[1]) - float(access[1])) < 1e-12


def test_digest_costs_when_host_energy_is_low() -> None:
    cfg = RunConfig(n=1)
    z = np.zeros((1, 12), dtype=np.float64)
    z[0, I_DIGEST] = 0.7
    e = energy_channels(z, 0.0, 1.0)
    assert float(e.host[0]) < cfg.eps
    cost = trait_cost(z, e.bite, e.host, e.heme_load, cfg)
    z0 = z.copy()
    z0[0, I_DIGEST] = 0.0
    e0 = energy_channels(z0, 0.0, 1.0)
    cost0 = trait_cost(z0, e0.bite, e0.host, e0.heme_load, cfg)
    extra = cfg.c_quad * (0.7 ** 2) + cfg.c_digest * 0.7
    assert abs(float(cost[0] - cost0[0]) - extra) < 1e-12


def test_heme_safe_costs_when_heme_load_is_low() -> None:
    cfg = RunConfig(n=1)
    z = np.zeros((1, 12), dtype=np.float64)
    z[0, I_HEME] = 0.6
    e = energy_channels(z, 0.0, 1.0)
    assert float(e.heme_load[0]) < cfg.eps
    cost = trait_cost(z, e.bite, e.host, e.heme_load, cfg)
    z0 = z.copy()
    z0[0, I_HEME] = 0.0
    e0 = energy_channels(z0, 0.0, 1.0)
    cost0 = trait_cost(z0, e0.bite, e0.host, e0.heme_load, cfg)
    extra = cfg.c_quad * (0.6 ** 2) + cfg.c_heme * 0.6
    assert abs(float(cost[0] - cost0[0]) - extra) < 1e-12


def test_iron_tax_falls_with_heme_safe() -> None:
    cfg = RunConfig(n=1)
    load = np.array([0.8])
    v0 = iron_viability(load, np.array([0.0]), cfg)
    v1 = iron_viability(load, np.array([1.5]), cfg)
    assert float(v1[0]) > float(v0[0])
    assert float(v0[0]) == np.exp(-cfg.beta_heme * 0.8 / 1.0)
