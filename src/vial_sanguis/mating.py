# Copyright (c) 2026 Martial Systems LLC
"""Random or k-NN pairing. Hidden load is excluded from similarity."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from vial_sanguis.config import RunConfig
from vial_sanguis.diet import fruit_available
from vial_sanguis.fitness import Phenotype
from vial_sanguis.genome import FEMALE, MALE, S_POST_STARVE, S_PRE_STARVE, Pop


@dataclass
class Pairing:
    female_idx: np.ndarray
    male_idx: np.ndarray
    distance: np.ndarray
    n_failed_match: int
    n_accepted: int


def mating_indices(t: int, cfg: RunConfig) -> tuple[int, ...]:
    if fruit_available(t, cfg) > 0.0:
        return S_PRE_STARVE
    return S_POST_STARVE


def mating_traits(ph: Phenotype, t: int, cfg: RunConfig) -> np.ndarray:
    cols = list(mating_indices(t, cfg))
    if ph.z.size == 0:
        return np.empty((0, len(cols)), dtype=np.float64)
    return ph.z[:, cols]


def freeze_sigma0(traits: np.ndarray, cfg: RunConfig) -> np.ndarray:
    floor = max(float(cfg.sigma_init), 1e-6)
    n_col = int(traits.shape[1]) if traits.ndim == 2 else 1
    if traits.ndim != 2 or traits.shape[0] <= 1:
        return np.full(n_col, floor, dtype=np.float64)
    sd = traits.std(axis=0, ddof=1)
    return np.where(sd <= 1e-12, floor, sd).astype(np.float64)


def pairwise_fm_distance(z_f: np.ndarray, z_m: np.ndarray, sigma0: np.ndarray) -> np.ndarray:
    delta = (z_f[:, None, :] - z_m[None, :, :]) / sigma0[None, None, :]
    return np.sqrt(np.square(delta).sum(axis=2))


def _empty_pair(n_fail: int) -> Pairing:
    return Pairing(
        female_idx=np.empty(0, dtype=np.int64),
        male_idx=np.empty(0, dtype=np.int64),
        distance=np.empty(0, dtype=np.float64),
        n_failed_match=int(n_fail),
        n_accepted=0,
    )


def pair(
    pop: Pop,
    ph: Phenotype,
    cfg: RunConfig,
    rng: np.random.Generator,
    sigma0: np.ndarray,
) -> Pairing:
    f_idx = np.flatnonzero(pop.sex == FEMALE)
    m_idx = np.flatnonzero(pop.sex == MALE)
    if f_idx.size == 0 or m_idx.size == 0:
        return _empty_pair(int(f_idx.size))

    z = mating_traits(ph, pop.t, cfg)
    dist = pairwise_fm_distance(z[f_idx], z[m_idx], sigma0)
    remaining = np.full(m_idx.size, int(cfg.m_max), dtype=np.int32)
    order = rng.permutation(f_idx.size)

    chosen_f: list[int] = []
    chosen_m: list[int] = []
    chosen_d: list[float] = []
    n_fail = 0
    knn_mode = cfg.mating_mode != "random"
    k_eff = min(int(cfg.k), int(m_idx.size))
    knn = None
    if knn_mode and k_eff > 0:
        knn = np.argpartition(dist, kth=k_eff - 1, axis=1)[:, :k_eff]

    for local_f in order:
        if knn_mode:
            cands = knn[local_f]
            legal = cands[remaining[cands] > 0]
            if legal.size == 0:
                n_fail += 1
                continue
            pick = int(legal[np.argmin(dist[local_f, legal])])
        else:
            cap = remaining > 0
            if not np.any(cap):
                n_fail += 1
                continue
            legal = np.flatnonzero(cap)
            pick = int(rng.choice(legal))
        chosen_f.append(int(f_idx[local_f]))
        chosen_m.append(int(m_idx[pick]))
        chosen_d.append(float(dist[local_f, pick]))
        remaining[pick] -= 1

    if not chosen_f:
        return _empty_pair(n_fail)
    fi = np.asarray(chosen_f, dtype=np.int64)
    mi = np.asarray(chosen_m, dtype=np.int64)
    d = np.asarray(chosen_d, dtype=np.float64)
    return Pairing(
        female_idx=fi,
        male_idx=mi,
        distance=d,
        n_failed_match=n_fail,
        n_accepted=int(fi.size),
    )
