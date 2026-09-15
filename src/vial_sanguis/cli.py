# Copyright (c) 2026 Martial Systems LLC
"""CLI for the closed-vial host-fluid engine."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from vial_sanguis.config import RunConfig
from vial_sanguis.metrics import stamp_clocks
from vial_sanguis.population import run_generations, write_run

BANNER = (
    "Closed vial. Diet ladder. Prestomal-tooth rasp. Recessive load. Census may fall."
)

REPO = Path(__file__).resolve().parents[2]


def _parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="vial-sanguis", description=BANNER)
    sub = p.add_subparsers(dest="cmd", required=True)
    run = sub.add_parser("run", help="run a closed-vial experiment")
    run.add_argument("--arm", default="vampire", choices=["vampire", "random"])
    run.add_argument("--mode", default="knn", choices=["knn", "random"])
    run.add_argument("--k", type=int, default=3)
    run.add_argument("--generations", type=int, default=2500)
    run.add_argument("--n", type=int, default=1000)
    run.add_argument("--seed", type=int, default=1)
    run.add_argument("--starve-at", type=int, default=5)
    run.add_argument("--out", type=Path, default=REPO / "logs" / "run.json")
    run.add_argument("--cap", choices=["on", "off"], default="off")
    run.add_argument("--fruit-forever", action="store_true")
    run.add_argument("--bite-weight", type=float, default=1.0)
    run.add_argument("--n-floor", type=int, default=8)
    rec = sub.add_parser(
        "reclock",
        help="recompute first-time meters on an existing summary JSON",
    )
    rec.add_argument("path", type=Path)
    return p


def _mode_name(arm: str, mode: str) -> str:
    if arm == "random" or mode == "random":
        return "random"
    return "assortative_knn"


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.cmd == "reclock":
        path = Path(args.path)
        payload = json.loads(path.read_text(encoding="utf-8"))
        stamp_clocks(payload)
        write_run(payload, path)
        print(
            f"t_first_biter={payload.get('t_first_biter')} "
            f"t_held_biter={payload.get('t_held_biter')} "
            f"t_majority_biter={payload.get('t_majority_biter')} "
            f"t_heme_safe_rise={payload.get('t_heme_safe_rise')} "
            f"t_heme_safe_rise_mean={payload.get('t_heme_safe_rise_mean')}"
        )
        return 0
    if args.cmd != "run":
        return 2
    out = Path(args.out)
    cfg = RunConfig(
        n=args.n,
        generations=args.generations,
        seed=args.seed,
        t_starve=args.starve_at,
        fruit_forever=bool(args.fruit_forever),
        mating_mode=_mode_name(args.arm, args.mode),
        k=args.k,
        arm=args.arm,
        cap=args.cap,
        n_floor=args.n_floor,
        fail_n_min=args.n_floor,
        bite_weight=args.bite_weight,
        n_ceiling=args.n if args.cap == "on" else 1200,
    )
    jsonl = out.with_suffix(".jsonl")
    result = run_generations(cfg, jsonl_path=jsonl)
    write_run(result, out)
    last = result["generations"][-1]
    print(
        f"t={last['t']} n={last['n']} F={last['F']:.4f} "
        f"p_exudate={last['p_exudate']:.3f} p_biter={last['p_biter']:.3f} "
        f"t_crash={result['t_crash']} min_n={result['min_n']} "
        f"t_recover={result['t_recover']} t_first_biter={result['t_first_biter']} "
        f"t_held_biter={result['t_held_biter']} "
        f"t_heme_safe_rise={result['t_heme_safe_rise']} "
        f"extinct={result['extinct']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
