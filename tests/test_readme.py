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
    assert "prestomal" in text.lower()
    assert "digest" in text
    assert "heme_safe" in text
    assert "census crashed to 3 at t=6" in text
    assert "first biter at t=211" in text
    assert "mean rasp 0.575" in text
    assert "mean pierce 0.027" in text
    assert "heme_safe rose at t=695" in text
    assert "majority biters at t=1,468" in text
    assert "extinct at t=11" in text
    assert "p_biter=0" in text or "p_biter=0;" in text
    agents = (REPO / "AGENTS.md").read_text(encoding="utf-8")
    assert "—" not in agents
    assert "Closed vial" in agents
    assert "Load required" in agents
    assert "Census may fall" in agents
    assert "Diet ladder required" in agents
    assert "prestomal-tooth" in agents
