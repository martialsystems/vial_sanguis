# Copyright (c) 2026 Martial Systems LLC
"""Diploid autosomal genome, founder IDs, and additive mapping."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from vial_sanguis.config import RunConfig

FEMALE = 0
MALE = 1

QTL_AUTO = (
    "fruit_use",
    "fluid_detect",
    "rasp",
    "pierce",
    "saliva",
    "seek",
    "locomotion",
    "fertility_circuit",
    "stab",
    "fa",
    "digest",
    "heme_safe",
)

I_FRUIT = 0
I_FLUID = 1
I_RASP = 2
I_PIERCE = 3
I_SALIVA = 4
I_SEEK = 5
I_LOCO = 6
I_FERT = 7
I_STAB = 8
I_FA = 9
I_DIGEST = 10
I_HEME = 11

HOST_MOUTHPART = (I_FLUID, I_RASP, I_PIERCE, I_SALIVA, I_SEEK)
BLOOD_QTLS = (I_DIGEST, I_HEME)
S_PRE_STARVE = (I_FRUIT, I_LOCO)
S_POST_STARVE = (I_FLUID, I_RASP, I_PIERCE, I_SEEK)


@dataclass
class Pop:
    t: int
    n: int
    ids: np.ndarray
    sex: np.ndarray
    qtl_auto: np.ndarray
    load: np.ndarray
    founder_qtl_auto: np.ndarray
    founder_load: np.ndarray
    mother_id: np.ndarray
    father_id: np.ndarray
    next_id: int
    next_founder: int

    def take(self, idx: np.ndarray) -> Pop:
        if idx.size == 0:
            return empty_pop(
                t=self.t,
                k_a=int(self.qtl_auto.shape[1]),
                n_load=int(self.load.shape[1]),
                next_id=self.next_id,
                next_founder=self.next_founder,
            )
        return Pop(
            t=self.t,
            n=int(idx.size),
            ids=self.ids[idx],
            sex=self.sex[idx],
            qtl_auto=self.qtl_auto[idx],
            load=self.load[idx],
            founder_qtl_auto=self.founder_qtl_auto[idx],
            founder_load=self.founder_load[idx],
            mother_id=self.mother_id[idx],
            father_id=self.father_id[idx],
            next_id=self.next_id,
            next_founder=self.next_founder,
        )


def empty_pop(
    t: int,
    k_a: int,
    n_load: int,
    next_id: int,
    next_founder: int,
) -> Pop:
    return Pop(
        t=t,
        n=0,
        ids=np.empty(0, dtype=np.uint64),
        sex=np.empty(0, dtype=np.uint8),
        qtl_auto=np.empty((0, k_a, 2), dtype=np.float64),
        load=np.empty((0, n_load, 2), dtype=np.uint8),
        founder_qtl_auto=np.empty((0, k_a, 2), dtype=np.uint32),
        founder_load=np.empty((0, n_load, 2), dtype=np.uint32),
        mother_id=np.empty(0, dtype=np.int64),
        father_id=np.empty(0, dtype=np.int64),
        next_id=next_id,
        next_founder=next_founder,
    )


def clip_qtl(arr: np.ndarray, z_max: float) -> np.ndarray:
    return np.clip(arr, -z_max, z_max)


def additive_z(pop: Pop) -> np.ndarray:
    if pop.n == 0:
        return np.empty((0, pop.qtl_auto.shape[1]), dtype=np.float64)
    return pop.qtl_auto.mean(axis=2)


def draw_sex(n: int, cfg: RunConfig, rng: np.random.Generator) -> np.ndarray:
    sex = np.zeros(n, dtype=np.uint8)
    if n <= 0:
        return sex
    for _ in range(200):
        sex = (rng.random(n) >= cfg.p_female).astype(np.uint8)
        nf = int(np.sum(sex == FEMALE))
        if abs(nf - (n - nf)) <= cfg.sex_imbalance_max:
            return sex
    return sex


def init_population(cfg: RunConfig, rng: np.random.Generator) -> Pop:
    if cfg.k_a < len(QTL_AUTO):
        raise ValueError(f"k_a must be >= {len(QTL_AUTO)}, got {cfg.k_a}")
    n = int(cfg.n)
    k_a, l = int(cfg.k_a), int(cfg.n_load)
    sex = draw_sex(n, cfg, rng)
    qtl_auto = clip_qtl(
        rng.normal(0.0, cfg.sigma_init, size=(n, k_a, 2)),
        cfg.z_max,
    )
    qtl_auto[:, I_FRUIT, :] = clip_qtl(
        cfg.fruit_init + rng.normal(0.0, cfg.sigma_init, size=(n, 2)),
        cfg.z_max,
    )
    load = np.zeros((n, l, 2), dtype=np.uint8)
    for i in range(n):
        n_het = int(rng.poisson(cfg.lambda_init))
        n_het = min(max(n_het, 0), l)
        if n_het == 0:
            continue
        loci = rng.choice(l, size=n_het, replace=False)
        hap = rng.integers(0, 2, size=n_het)
        load[i, loci, hap] = 1

    n_f_auto = n * k_a * 2
    n_f_load = n * l * 2
    founder_qtl_auto = np.arange(1, 1 + n_f_auto, dtype=np.uint32).reshape(n, k_a, 2)
    founder_load = np.arange(
        1 + n_f_auto,
        1 + n_f_auto + n_f_load,
        dtype=np.uint32,
    ).reshape(n, l, 2)
    ids = np.arange(n, dtype=np.uint64)
    mother = np.full(n, -1, dtype=np.int64)
    father = np.full(n, -1, dtype=np.int64)
    return Pop(
        t=0,
        n=n,
        ids=ids,
        sex=sex,
        qtl_auto=qtl_auto,
        load=load,
        founder_qtl_auto=founder_qtl_auto,
        founder_load=founder_load,
        mother_id=mother,
        father_id=father,
        next_id=n,
        next_founder=int(1 + n_f_auto + n_f_load),
    )
