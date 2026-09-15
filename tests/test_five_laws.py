# Copyright (c) 2026 Martial Systems LLC
"""Five laws as pytest assertions. No GraphForge pin."""

from __future__ import annotations

import inspect
from pathlib import Path

import numpy as np

from vial_sanguis.config import RunConfig
from vial_sanguis.diet import HOST_CHANNELS
from vial_sanguis.fitness import energy_channels, phenotype
from vial_sanguis.genome import (
    BLOOD_QTLS,
    I_DIGEST,
    I_FLUID,
    I_HEME,
    I_RASP,
    I_SALIVA,
    QTL_AUTO,
    init_population,
)
from vial_sanguis.mating import mating_traits
from vial_sanguis.population import cap_uniform, run_generations

REPO = Path(__file__).resolve().parents[1]


def test_long_arm_continue_is_this_repo_only() -> None:
    text = (REPO / "LONG_ARM.md").read_text(encoding="utf-8")
    assert "Autonomous continue is allowed only along LONG_ARM.md." in text
    assert "Curiosity is not a transition." in text
    assert "Unfreezing a diet knob is a halt." in text
    assert "state: halt" in text
    assert "next legal node: none" in text
    assert "out of spec" in text
    assert "vampire_10000" in text
    assert "only fixed the kit in the 10k tail" in text
    assert "t_first_biter=211" in text
    agents = (REPO / "AGENTS.md").read_text(encoding="utf-8")
    assert "Autonomous continue is allowed only along LONG_ARM.md." in agents
    assert "Curiosity is not a transition." in agents
    assert "Unfreezing a diet knob is a halt." in agents
    assert "This repo only (not the home VBD pack):" in agents


def test_no_graphforge_pin() -> None:
    assert not (REPO / "engine_pin.json").exists()
    assert not (REPO / "product_laws.py").exists()
    assert not (REPO / "vialforge").exists()
    assert not (REPO / "sanguisforge").exists()
    agents = (REPO / "AGENTS.md").read_text(encoding="utf-8")
    assert "Verify-before-done is the finish gate." in agents
    assert "Do not pin GraphForge" in agents
    assert "vialforge" in agents.lower()
    assert "do not reuse" in agents.lower() and "vialforge" in agents.lower()


def test_law1_closed_vial_never_invents_adults() -> None:
    cfg = RunConfig(
        n=40,
        generations=8,
        seed=7,
        t_starve=2,
        n_ceiling=4000,
        cap="off",
        fail_n_min=1,
        fail_viability=0.0,
    )
    result = run_generations(cfg)
    for g in result["generations"]:
        if g["t"] > 0:
            assert g["n"] <= g["n_viable"]
            assert g["n_viable"] <= g["n_eggs"]
    rng = np.random.default_rng(0)
    pop = init_population(RunConfig(n=12, seed=0, generations=1), rng)
    capped = cap_uniform(pop, 100, rng)
    assert capped.n == pop.n
    src = inspect.getsource(run_generations)
    assert "immigrat" not in src.lower()
    assert "restock" not in src.lower()


def test_law2_load_required_and_hidden_from_mating() -> None:
    cfg = RunConfig()
    assert cfg.n_load >= 64
    assert cfg.n_lethal >= 1
    assert cfg.s_let == 1.0
    rng = np.random.default_rng(1)
    pop = init_population(cfg, rng)
    assert pop.load.shape == (cfg.n, cfg.n_load, 2)
    ph = phenotype(pop, cfg)
    traits = mating_traits(ph, pop.t, cfg)
    assert traits.shape[1] == 2
    src = inspect.getsource(mating_traits)
    assert "load" not in src.lower()


def test_law3_census_may_fall() -> None:
    cfg = RunConfig(
        n=80,
        generations=10,
        seed=1,
        t_starve=3,
        n_ceiling=80,
        cap="off",
        fail_n_min=1,
        fail_viability=0.0,
    )
    result = run_generations(cfg)
    after = [g["n"] for g in result["generations"] if g["t"] >= cfg.t_starve]
    before = [g["n"] for g in result["generations"] if g["t"] < cfg.t_starve]
    assert after
    assert min(after) < min(before)


def test_law4_diet_ladder_digest_not_a_blood_switch() -> None:
    assert HOST_CHANNELS == ("tears", "sweat", "wound", "bite")
    z = np.zeros((1, 12), dtype=np.float64)
    z[0, I_FLUID] = 1.0
    z[0, I_RASP] = 1.0
    z[0, I_SALIVA] = 0.4
    e0 = energy_channels(z, 0.0, 1.0)
    z_d = z.copy()
    z_d[0, I_DIGEST] = 2.0
    e_d = energy_channels(z_d, 0.0, 1.0)
    z_s = z.copy()
    z_s[0, I_SALIVA] = 2.0
    e_s = energy_channels(z_s, 0.0, 1.0)
    assert float(e_d.wound[0]) == float(e0.wound[0])
    assert float(e_d.usable_blood[0]) > float(e0.usable_blood[0])
    assert float(e_s.wound[0]) != float(e0.wound[0])
    assert float(e_d.heme_load[0]) == float(e0.heme_load[0])
    assert I_DIGEST not in (I_SALIVA,)
    assert I_DIGEST in BLOOD_QTLS
    assert I_HEME in BLOOD_QTLS


def test_law5_prestomal_path_not_stylet() -> None:
    assert QTL_AUTO[2] == "rasp"
    assert QTL_AUTO[3] == "pierce"
    assert QTL_AUTO[4] == "saliva"
    assert QTL_AUTO[10] == "digest"
    assert QTL_AUTO[11] == "heme_safe"
    joined = " ".join(QTL_AUTO)
    assert "mandible" not in joined
    assert "stylet" not in joined
    src_root = REPO / "src" / "vial_sanguis"
    blob = "\n".join(p.read_text(encoding="utf-8") for p in src_root.glob("*.py"))
    assert "stylet" not in blob.lower()
    assert "mandible" not in blob.lower()
    assert "flywire" not in blob.lower()
    assert "malecns" not in blob.lower()
