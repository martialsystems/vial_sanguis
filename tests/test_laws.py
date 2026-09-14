# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

import inspect

from vial_sanguis import diet, genome, mating, population
from vial_sanguis.genome import HOST_MOUTHPART, S_POST_STARVE, S_PRE_STARVE
from vial_sanguis.mating import mating_indices
from vial_sanguis.config import RunConfig


def test_closed_vial_source() -> None:
    src = inspect.getsource(population)
    assert "immigrat" not in src.lower()
    assert "wildtype" not in src.lower()
    assert "wild_type" not in src.lower()
    assert "restock" not in src.lower()
    assert "Never pads" in src or "never pads" in src.lower()


def test_load_excluded_from_similarity() -> None:
    src = inspect.getsource(mating)
    assert "pop.load" not in src
    assert "ph.v_load" not in src
    assert not any(i in S_PRE_STARVE for i in HOST_MOUTHPART)
    assert genome.I_FLUID in S_POST_STARVE
    assert genome.I_RASP in S_POST_STARVE
    assert genome.I_PIERCE in S_POST_STARVE
    assert genome.I_SEEK in S_POST_STARVE
    cfg = RunConfig(t_starve=5)
    assert mating_indices(0, cfg) == S_PRE_STARVE
    assert mating_indices(5, cfg) == S_POST_STARVE


def test_diet_ladder_not_blood_switch() -> None:
    src = inspect.getsource(diet)
    assert "tears" in src
    assert "HOST_CHANNELS" in src
    assert diet.HOST_CHANNELS == ("tears", "sweat", "wound", "bite")


def test_mouthpart_path_is_rasp_not_stylet() -> None:
    names = " ".join(genome.QTL_AUTO)
    assert "rasp" in names
    assert "mandible" not in names
    assert "stylet" not in names
    assert genome.QTL_AUTO[2] == "rasp"
    assert genome.QTL_AUTO[3] == "pierce"
