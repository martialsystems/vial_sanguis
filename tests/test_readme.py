# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def test_readme_question_first() -> None:
    text = (REPO / "README.md").read_text(encoding="utf-8")
    assert text.startswith("# vial_sanguis\n")
    body = text.split("\n", 1)[1].lstrip()
    assert body.startswith(
        "Under an explicit diet ladder and an allowed population crash"
    )
    first_para = body.split("\n## ", 1)[0]
    assert "This is not an origin of hematophagy." in first_para
    assert "## Origin" in text
    assert "## Long arm" in text
    assert "## Locks" in text
    assert "What it is not" not in text
    assert "—" not in text
    assert "Non-claims" in text
    assert "This does not evolve a real organ in 2500 generations." in text
    assert "QTLs are scalar proxies" in text
    assert "No live FlyWire / MaleCNS stepper." in text
    assert "No pathogen transmission module in v1." in text
    assert "log extinction instead of silently capping N." in text
    assert ".venv/bin/python -m pytest" in text
    assert "logs/vampire_2500_s1.json" in text
    assert "logs/random_2500_s1.json" in text
    assert "--fruit-forever" in text
    assert "AGENTS.md" in text
    assert "t_first_biter=211" in text
    assert "mean rasp 0.575" in text
    assert "mean pierce 0.027" in text
    assert "census crashed to 3 at t=6" in text.lower()
    assert "heme_safe rose at t=695" in text
    assert "majority biters at t=1,468" in text
    assert "extinct at t=11" in text
    assert "F=1.000" in text
    assert "phi_max=0.25" in text
    assert "only fixed the kit in the 10k tail" in text
    assert "Saliva did not" in text or "saliva did not" in text
    assert "t_starve | 5" in text or "t_starve | 5 |" in text
    assert "logs/vampire_10000_s{1,2,3}.json" in text
    assert "knn_cap_after_recover_1500" in text
    assert "--cap-on-at recover" in text
    assert "hostshift_held" in text
    assert "clot-without-saliva" in text
    assert "vampire flies evolve" not in text.lower()
    agents = (REPO / "AGENTS.md").read_text(encoding="utf-8")
    assert "—" not in agents
    assert "Closed vial" in agents
    assert "Load required" in agents
    assert "Census may fall" in agents
    assert "Diet ladder required" in agents
    assert "prestomal-tooth" in agents
    assert "Do not pin GraphForge" in agents
    assert "Do not reuse `vialforge/`" in agents or "Do not reuse vialforge" in agents
    assert "Verify-before-done is the finish gate." in agents
    assert "LONG_ARM.md" in agents
    assert (REPO / "LONG_ARM.md").is_file()
    assert "Curiosity is not a transition." in agents
