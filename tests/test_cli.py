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
