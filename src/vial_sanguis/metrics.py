# Copyright (c) 2026 Martial Systems LLC
"""Generation census: IBD F, pairwise kinship, diet-ladder energies, first times."""

from __future__ import annotations

from typing import Any

import numpy as np

from vial_sanguis.config import RunConfig
from vial_sanguis.fitness import Phenotype
from vial_sanguis.genome import FEMALE, MALE, QTL_AUTO, Pop
from vial_sanguis.mating import Pairing, freeze_sigma0, mating_traits, pairwise_fm_distance


def _py(x: Any) -> Any:
    if isinstance(x, (np.floating, np.integer)):
        return x.item()
    if isinstance(x, np.bool_):
        return bool(x)
    return x


def heterozygosity_qtl(pop: Pop) -> float:
    if pop.n == 0:
        return 0.0
    return float((pop.founder_qtl_auto[:, :, 0] != pop.founder_qtl_auto[:, :, 1]).mean())


def mean_pairwise_phi(founder: np.ndarray) -> float:
    """Mean pairwise kinship from autosomal QTL founder-allele IBD. This is not F."""
    n, k, _ = founder.shape
    if n < 2 or k == 0:
        return 0.0
    acc = np.zeros((n, n), dtype=np.float64)
    for loc in range(k):
        mat = founder[:, loc, 0]
        pat = founder[:, loc, 1]
        acc += (mat[:, None] == mat[None, :]).astype(np.float64)
        acc += (mat[:, None] == pat[None, :]).astype(np.float64)
        acc += (pat[:, None] == mat[None, :]).astype(np.float64)
        acc += (pat[:, None] == pat[None, :]).astype(np.float64)
    acc *= 0.25 / k
    iu = np.triu_indices(n, k=1)
    return float(acc[iu].mean())


class _UF:
    def __init__(self, n: int) -> None:
        self.p = np.arange(n)

    def find(self, x: int) -> int:
        p = self.p
        while p[x] != x:
            p[x] = p[p[x]]
            x = int(p[x])
        return x

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[rb] = ra


def both_sex_clusters(
    pop: Pop,
    ph: Phenotype,
    cfg: RunConfig,
    sigma0: np.ndarray,
) -> int:
    if pop.n == 0:
        return 0
    f_idx = np.flatnonzero(pop.sex == FEMALE)
    m_idx = np.flatnonzero(pop.sex == MALE)
    if f_idx.size == 0 or m_idx.size == 0:
        return 0
    z = mating_traits(ph, pop.t, cfg)
    dist = pairwise_fm_distance(z[f_idx], z[m_idx], sigma0)
    uf = _UF(pop.n)
    ii, jj = np.where(dist < cfg.d_cluster)
    for a, b in zip(f_idx[ii], m_idx[jj], strict=False):
        uf.union(int(a), int(b))
    n_both = 0
    buckets: dict[int, list[int]] = {}
    for i in range(pop.n):
        buckets.setdefault(uf.find(i), []).append(i)
    for members in buckets.values():
        arr = np.asarray(members, dtype=np.int64)
        if np.any(pop.sex[arr] == FEMALE) and np.any(pop.sex[arr] == MALE):
            n_both += 1
    return n_both


def record_generation(
    pop: Pop,
    ph: Phenotype,
    pairing: Pairing | None,
    cfg: RunConfig,
    h0_qtl: float,
    n_eggs: int,
    n_viable: int,
) -> dict:
    n_f = int(np.sum(pop.sex == FEMALE)) if pop.n else 0
    n_m = int(np.sum(pop.sex == MALE)) if pop.n else 0
    extinct = pop.n == 0 or n_f == 0 or n_m == 0
    h_qtl = heterozygosity_qtl(pop)
    f_t = 0.0 if h0_qtl <= 0 else 1.0 - (h_qtl / h0_qtl)
    n_acc = 0 if pairing is None else pairing.n_accepted
    mean_w = float(ph.w.mean()) if pop.n else 0.0
    mean_survive = float(ph.survive.mean()) if pop.n else 0.0
    mean_fertility = float(ph.fertility.mean()) if pop.n else 0.0
    qtl_mean: dict[str, float] = {}
    qtl_p95: dict[str, float] = {}
    n_names = min(len(QTL_AUTO), ph.z.shape[1] if ph.z.ndim == 2 else 0)
    for i, name in enumerate(QTL_AUTO[:n_names]):
        col = ph.z[:, i] if pop.n else np.empty(0)
        qtl_mean[name] = float(col.mean()) if pop.n else 0.0
        qtl_p95[name] = float(np.quantile(col, 0.95)) if pop.n else 0.0
    p_exudate = float(np.mean(ph.exudate > cfg.exudate_threshold)) if pop.n else 0.0
    p_biter = float(np.mean(ph.biter)) if pop.n else 0.0
    max_bite = float(ph.energy_bite.max()) if pop.n else 0.0
    max_rasp = float(ph.z[:, 2].max()) if pop.n else 0.0
    clusters = 0
    if pop.n:
        traits = mating_traits(ph, pop.t, cfg)
        sig = freeze_sigma0(traits, cfg)
        clusters = both_sex_clusters(pop, ph, cfg, sig)
    rec = {
        "t": int(pop.t),
        "n": int(pop.n),
        "n_female": n_f,
        "n_male": n_m,
        "F": float(f_t),
        "mean_pairwise_phi": mean_pairwise_phi(pop.founder_qtl_auto) if pop.n else 0.0,
        "mean_w": mean_w,
        "mean_survive": mean_survive,
        "mean_fertility": mean_fertility,
        "qtl_mean": qtl_mean,
        "qtl_p95": qtl_p95,
        "mean_energy_fruit": float(ph.energy_fruit.mean()) if pop.n else 0.0,
        "mean_energy_tears": float(ph.energy_tears.mean()) if pop.n else 0.0,
        "mean_energy_sweat": float(ph.energy_sweat.mean()) if pop.n else 0.0,
        "mean_energy_wound": float(ph.energy_wound.mean()) if pop.n else 0.0,
        "mean_energy_bite": float(ph.energy_bite.mean()) if pop.n else 0.0,
        "mean_usable_blood": float(ph.usable_blood.mean()) if pop.n else 0.0,
        "mean_heme_load": float(ph.heme_load.mean()) if pop.n else 0.0,
        "mean_v_iron": float(ph.v_iron.mean()) if pop.n else 0.0,
        "p_exudate": p_exudate,
        "p_biter": p_biter,
        "max_bite": max_bite,
        "max_rasp": max_rasp,
        "accepted_pairs": int(n_acc),
        "clusters": int(clusters),
        "n_eggs": int(n_eggs),
        "n_viable": int(n_viable),
        "extinct": bool(extinct),
    }
    return {k: _py(v) if not isinstance(v, dict) else v for k, v in rec.items()}


def first_times(records: list[dict], cfg: RunConfig) -> dict:
    t_crash = None
    t_min_n = None
    t_recover = None
    t_first_biter = None
    t_majority_biter = None
    t_heme_safe_rise = None
    min_n = None
    crashed = False
    for rec in records:
        t = int(rec["t"])
        n = int(rec["n"])
        if t >= cfg.t_starve and not cfg.fruit_forever:
            if t_crash is None and n < 80:
                t_crash = t
                crashed = True
            if min_n is None or n < min_n:
                min_n = n
                t_min_n = t
            if crashed and t_recover is None and n >= 400:
                t_recover = t
        if t_first_biter is None and float(rec["p_biter"]) > 0.0:
            t_first_biter = t
        if t_majority_biter is None and float(rec["p_biter"]) >= 0.5:
            t_majority_biter = t
        mean_heme = float(rec.get("qtl_mean", {}).get("heme_safe", 0.0))
        if t_heme_safe_rise is None and mean_heme > cfg.heme_rise:
            t_heme_safe_rise = t
    return {
        "t_crash": t_crash,
        "t_min_n": t_min_n,
        "min_n": min_n,
        "t_recover": t_recover,
        "t_first_biter": t_first_biter,
        "t_majority_biter": t_majority_biter,
        "t_heme_safe_rise": t_heme_safe_rise,
    }
