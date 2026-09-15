# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

import numpy as np

from vial_sanguis.config import RunConfig
from vial_sanguis.fitness import energy_channels, phenotype
from vial_sanguis.genome import I_DIGEST, I_FLUID, I_PIERCE, I_RASP, I_SALIVA, I_SEEK, init_population


def _blood_z() -> np.ndarray:
    z = np.zeros((1, 12), dtype=np.float64)
    z[0, I_FLUID] = 1.0
    z[0, I_RASP] = 1.0
    z[0, I_PIERCE] = 1.0
    z[0, I_SALIVA] = 0.8
    z[0, I_SEEK] = 1.0
    z[0, I_DIGEST] = 1.0
    return z


def test_skin_and_clot_are_opt_in_on_energy_channels() -> None:
    z = _blood_z()
    base = energy_channels(z, 0.0, 1.0)
    tough = energy_channels(z, 0.0, 1.0, skin_tough=2.0)
    assert float(tough.bite[0]) < float(base.bite[0])


def test_skin_tough_halves_bite_payoff_not_heme_access() -> None:
    z = _blood_z()
    easy = energy_channels(z, 0.0, 1.0, skin_tough=1.0)
    hard = energy_channels(z, 0.0, 1.0, skin_tough=2.0)
    assert abs(float(hard.bite[0]) - 0.5 * float(easy.bite[0])) < 1e-12
    assert float(hard.heme_load[0]) == float(easy.heme_load[0])


def test_clot_zeros_usable_blood_when_saliva_nonpositive() -> None:
    z = _blood_z()
    z[0, I_SALIVA] = -0.4
    open_pool = energy_channels(z, 0.0, 1.0, clot_without_saliva=False)
    clotted = energy_channels(z, 0.0, 1.0, clot_without_saliva=True)
    assert float(open_pool.usable_blood[0]) > 0.0
    assert float(clotted.usable_blood[0]) == 0.0
    assert float(clotted.heme_load[0]) == float(open_pool.heme_load[0])


def test_scab_zeros_wound_keeps_bite_and_heme_from_bite() -> None:
    z = _blood_z()
    open_w = energy_channels(z, 0.0, 1.0)
    scab = energy_channels(z, 0.0, 1.0, wound_scab=True, clot_without_saliva=True)
    assert float(open_w.wound[0]) > 0.0
    assert float(scab.wound[0]) == 0.0
    assert float(scab.bite[0]) > 0.0
    assert float(scab.heme_load[0]) < float(open_w.heme_load[0])
    z_neg = z.copy()
    z_neg[0, I_SALIVA] = -0.5
    scab_neg = energy_channels(z_neg, 0.0, 1.0, wound_scab=True, clot_without_saliva=True)
    assert float(scab_neg.usable_blood[0]) == 0.0


def test_exudate_cap_zeros_tears_and_sweat() -> None:
    z = _blood_z()
    open_e = energy_channels(z, 0.0, 1.0)
    capped = energy_channels(z, 0.0, 1.0, wound_scab=True, exudate_cap=True)
    assert float(open_e.tears[0]) > 0.0
    assert float(open_e.sweat[0]) > 0.0
    assert float(capped.tears[0]) == 0.0
    assert float(capped.sweat[0]) == 0.0
    assert float(capped.wound[0]) == 0.0
    assert float(capped.bite[0]) > 0.0
    assert float(capped.host[0]) == float(capped.usable_blood[0])


def test_phenotype_shift_off_ignores_cfg_skin() -> None:
    cfg = RunConfig(n=8, seed=1, host_shift_at="held", skin_tough=2.0, clot_without_saliva=True)
    rng = np.random.default_rng(1)
    pop = init_population(cfg, rng)
    pop.qtl_auto[:, I_RASP, :] = 1.0
    pop.qtl_auto[:, I_PIERCE, :] = 1.0
    pop.qtl_auto[:, I_SALIVA, :] = 0.8
    pop.qtl_auto[:, I_SEEK, :] = 1.0
    off = phenotype(pop, cfg, host_shift=False)
    on = phenotype(pop, cfg, host_shift=True)
    assert float(on.energy_bite.mean()) < float(off.energy_bite.mean())
