# Copyright (c) 2026 Martial Systems LLC
"""Non-overlapping generation loop. Census may fall. Never invents adults."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from dataclasses import replace

from vial_sanguis.config import RunConfig
from vial_sanguis.fitness import phenotype
from vial_sanguis.genome import FEMALE, MALE, Pop, init_population
from vial_sanguis.inheritance import meiosis_mutate
from vial_sanguis.mating import freeze_sigma0, mating_traits, pair
from vial_sanguis.metrics import first_times, heterozygosity_qtl, record_generation


def cap_uniform(live: Pop, n_cap: int, rng: np.random.Generator) -> Pop:
    """Hard ceiling. Never pads. n < n_cap is a floating census."""
    if live.n <= n_cap:
        return live
    idx = rng.choice(live.n, size=n_cap, replace=False)
    idx.sort()
    return live.take(idx)


def extinct_rule(pop: Pop, ph_mean_survive: float, cfg: RunConfig) -> bool:
    if pop.n == 0:
        return True
    n_f = int(np.sum(pop.sex == FEMALE))
    n_m = int(np.sum(pop.sex == MALE))
    if n_f == 0 or n_m == 0:
        return True
    if pop.n < cfg.fail_n_min and ph_mean_survive < cfg.fail_viability:
        return True
    return False


def run_generations(
    cfg: RunConfig,
    rng: np.random.Generator | None = None,
    jsonl_path: Path | None = None,
) -> dict:
    if cfg.cap not in ("on", "off"):
        raise ValueError(f"cap must be on or off, got {cfg.cap!r}")
    if cfg.mating_mode not in ("random", "assortative_knn"):
        raise ValueError(f"unknown mating_mode {cfg.mating_mode!r}")

    rng = rng or np.random.default_rng(cfg.seed)
    pop = init_population(cfg, rng)
    ph = phenotype(pop, cfg)
    h0 = heterozygosity_qtl(pop)

    jsonl_fp = None
    if jsonl_path is not None:
        jsonl_path.parent.mkdir(parents=True, exist_ok=True)
        jsonl_fp = jsonl_path.open("w", encoding="utf-8")

    records: list[dict] = []
    rec0 = record_generation(
        pop, ph, pairing=None, cfg=cfg, h0_qtl=h0, n_eggs=pop.n, n_viable=pop.n
    )
    records.append(rec0)
    if jsonl_fp is not None:
        jsonl_fp.write(json.dumps(rec0) + "\n")
        jsonl_fp.flush()

    ceiling = cfg.ceiling()
    cap_armed = bool(cfg.kinship_cap) and cfg.kinship_cap_on != "recover"
    t_kinship_on = 0 if cap_armed else None

    for _step in range(cfg.generations):
        if extinct_rule(pop, float(ph.survive.mean()) if pop.n else 0.0, cfg):
            records[-1]["extinct"] = True
            break
        if (
            cfg.kinship_cap
            and cfg.kinship_cap_on == "recover"
            and not cap_armed
            and pop.t >= cfg.t_starve
            and pop.n >= int(cfg.kinship_recover_n)
        ):
            cap_armed = True
            t_kinship_on = int(pop.t)
        # Mating axes switch at starve; refresh scale from living adults.
        sigma0 = freeze_sigma0(mating_traits(ph, pop.t, cfg), cfg)
        mate_cfg = replace(cfg, kinship_cap=bool(cfg.kinship_cap and cap_armed))
        pairing = pair(pop, ph, mate_cfg, rng, sigma0)
        eggs, _pair_of, _clutch = meiosis_mutate(pop, ph, pairing, cfg, rng)
        n_eggs = eggs.n
        if n_eggs == 0:
            pop = eggs
            ph = phenotype(pop, cfg)
            rec = record_generation(
                pop, ph, pairing, cfg, h0, n_eggs=0, n_viable=0
            )
            rec["extinct"] = True
            records.append(rec)
            if jsonl_fp is not None:
                jsonl_fp.write(json.dumps(rec) + "\n")
            break
        # Tear-film crowding uses living adults, never the egg pile.
        host_crowd = pop.n if (pop.t >= cfg.t_starve and not cfg.fruit_forever) else 0
        egg_ph = phenotype(eggs, cfg, crowd_n=host_crowd)
        draw = rng.random(eggs.n)
        survive = (draw < egg_ph.survive) & (egg_ph.v_load > 0.0)
        n_viable = int(survive.sum())
        live = eggs.take(np.flatnonzero(survive))
        nxt = cap_uniform(live, ceiling, rng)
        pop = nxt
        live_crowd = pop.n if (pop.t >= cfg.t_starve and not cfg.fruit_forever) else 0
        ph = phenotype(pop, cfg, crowd_n=live_crowd)
        rec = record_generation(
            pop, ph, pairing, cfg, h0, n_eggs=n_eggs, n_viable=n_viable
        )
        records.append(rec)
        if jsonl_fp is not None:
            jsonl_fp.write(json.dumps(rec) + "\n")
            jsonl_fp.flush()
        if rec["extinct"] or extinct_rule(pop, float(ph.survive.mean()) if pop.n else 0.0, cfg):
            records[-1]["extinct"] = True
            break

    if jsonl_fp is not None:
        jsonl_fp.close()

    last = records[-1]
    times = first_times(records, cfg)
    return {
        "config": cfg.payload(),
        "seed": cfg.seed,
        "arm": cfg.arm,
        "mate": "random" if cfg.mating_mode == "random" else "knn",
        "k": cfg.k,
        "cap": cfg.cap,
        "h0_qtl": h0,
        "generations": records,
        "final_t": last["t"],
        "extinct": bool(last["extinct"]),
        "t_kinship_on": t_kinship_on,
        **times,
    }


def write_run(result: dict, out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
