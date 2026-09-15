# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

import json
from pathlib import Path

from vial_sanguis.cli import main


def test_cli_help() -> None:
    try:
        main(["run", "--help"])
    except SystemExit as exc:
        assert exc.code == 0


def test_cli_tiny_run(tmp_path: Path) -> None:
    out = tmp_path / "tiny.json"
    rc = main(
        [
            "run",
            "--arm",
            "vampire",
            "--mode",
            "knn",
            "--k",
            "3",
            "--generations",
            "4",
            "--n",
            "24",
            "--seed",
            "1",
            "--starve-at",
            "2",
            "--out",
            str(out),
        ]
    )
    assert rc == 0
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["seed"] == 1
    assert payload["mate"] == "knn"
    assert out.with_suffix(".jsonl").is_file()
    lines = out.with_suffix(".jsonl").read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == len(payload["generations"])
    assert "t_held_biter" in payload
    assert "t_heme_safe_rise_mean" in payload
    assert payload["config"]["kinship_cap_on"] == "immediate"


def test_cli_reclock(tmp_path: Path) -> None:
    path = tmp_path / "run.json"
    path.write_text(
        json.dumps(
            {
                "config": {"t_starve": 5, "fruit_forever": False},
                "generations": [
                    {
                        "t": 16,
                        "n": 50,
                        "p_biter": 0.0,
                        "mean_energy_wound": 0.01,
                        "mean_energy_bite": 0.0,
                        "qtl_mean": {"heme_safe": 0.2},
                    },
                    {
                        "t": 80,
                        "n": 400,
                        "p_biter": 0.0,
                        "mean_energy_wound": 0.4,
                        "mean_energy_bite": 0.0,
                        "qtl_mean": {"heme_safe": 0.2},
                    },
                ],
            }
        ),
        encoding="utf-8",
    )
    assert main(["reclock", str(path)]) == 0
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["t_heme_safe_rise_mean"] == 16
    assert payload["t_heme_safe_rise"] == 80
    assert payload["t_wound_load"] == 80
