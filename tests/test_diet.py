# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

import numpy as np

from vial_sanguis.config import RunConfig
from vial_sanguis.diet import HOST_CHANNELS, fruit_available
from vial_sanguis.fitness import energy_channels, sigmoid
from vial_sanguis.genome import (
    I_DIGEST,
    I_FLUID,
    I_FRUIT,
    I_PIERCE,
    I_RASP,
    I_SALIVA,
    I_SEEK,
)


def test_fruit_drops_at_starve() -> None:
    cfg = RunConfig(t_starve=5)
    assert fruit_available(4, cfg) == 1.0
    assert fruit_available(5, cfg) == 0.0
    forever = RunConfig(t_starve=5, fruit_forever=True)
    assert fruit_available(400, forever) == 1.0


def test_four_host_channels() -> None:
    assert HOST_CHANNELS == ("tears", "sweat", "wound", "bite")


def test_ladder_formulas() -> None:
    z = np.zeros((1, 12), dtype=np.float64)
    z[0, I_FRUIT] = 1.2
    z[0, I_FLUID] = 0.5
    z[0, I_RASP] = 0.4
    z[0, I_PIERCE] = 0.3
    z[0, I_SALIVA] = 0.2
    z[0, I_SEEK] = 0.1
    z[0, I_DIGEST] = 0.0
    e = energy_channels(z, fruit_avail=1.0, bite_weight=1.0)
    assert abs(float(e.fruit[0]) - 1.2) < 1e-12
    assert abs(float(e.tears[0]) - 0.5 * (0.35 + 0.15 * 0.1)) < 1e-12
    assert abs(float(e.sweat[0]) - 0.5 * 0.4 * (0.25 + 0.10 * 0.1)) < 1e-12
    assert abs(float(e.wound[0]) - 0.5 * 0.4 * (0.40 + 0.20 * 0.2)) < 1e-12
    want_bite = (
        0.4
        * 0.3
        * (0.15 + 0.85 * np.tanh(0.2))
        * (0.20 + 0.80 * np.tanh(0.1))
    )
    assert abs(float(e.bite[0]) - want_bite) < 1e-12
    want_usable = (float(e.wound[0]) + float(e.bite[0])) * float(sigmoid(np.array([0.0]))[0])
    assert abs(float(e.usable_blood[0]) - want_usable) < 1e-12
    assert abs(float(e.host[0]) - float(e.tears[0] + e.sweat[0] + e.usable_blood[0])) < 1e-12
    assert abs(float(e.total[0]) - float(e.fruit[0] + e.host[0])) < 1e-12

    e0 = energy_channels(z, fruit_avail=0.0, bite_weight=1.0)
    assert float(e0.fruit[0]) == 0.0
    assert float(e0.total[0]) < float(e.total[0])


def test_tears_do_not_need_rasp() -> None:
    z = np.zeros((1, 12), dtype=np.float64)
    z[0, I_FLUID] = 1.0
    e = energy_channels(z, 0.0, 1.0)
    assert float(e.tears[0]) == 0.35
    assert float(e.sweat[0]) == 0.0
    assert float(e.wound[0]) == 0.0
    assert float(e.bite[0]) == 0.0
    assert float(e.usable_blood[0]) == 0.0


def test_tear_film_is_finite() -> None:
    z = np.zeros((1, 12), dtype=np.float64)
    z[0, I_FLUID] = 1.0
    full = energy_channels(z, 0.0, 1.0, crowd_n=10, k_tears=40.0)
    crowded = energy_channels(z, 0.0, 1.0, crowd_n=80, k_tears=40.0)
    assert abs(float(full.tears[0]) - 0.35) < 1e-12
    assert abs(float(crowded.tears[0]) - 0.35 * 0.5) < 1e-12
    assert float(crowded.sweat[0]) == float(full.sweat[0])


def test_negative_traits_do_not_feed() -> None:
    z = np.zeros((1, 12), dtype=np.float64)
    z[0, I_FLUID] = -1.0
    z[0, I_RASP] = -1.0
    e = energy_channels(z, 0.0, 1.0)
    assert float(e.tears[0]) == 0.0
    assert float(e.sweat[0]) == 0.0
    assert float(e.wound[0]) == 0.0
    assert float(e.bite[0]) == 0.0
    assert float(e.host[0]) == 0.0
    assert float(e.total[0]) == 0.0
