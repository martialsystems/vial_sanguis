# Copyright (c) 2026 Martial Systems LLC
"""Diet-ladder energy, blood digestion, iron tax, load, survival, fertility."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from vial_sanguis.config import RunConfig
from vial_sanguis.diet import fruit_available, survive_params
from vial_sanguis.genome import (
    I_DIGEST,
    I_FLUID,
    I_FRUIT,
    I_HEME,
    I_PIERCE,
    I_RASP,
    I_SALIVA,
    I_SEEK,
    Pop,
    additive_z,
)


def pos(x: np.ndarray) -> np.ndarray:
    return np.clip(x, 0.0, np.inf)


def logistic(energy: np.ndarray, thresh: float, steep: float) -> np.ndarray:
    x = np.clip(steep * (energy - thresh), -60.0, 60.0)
    return 1.0 / (1.0 + np.exp(-x))


def sigmoid(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-np.clip(x, -60.0, 60.0)))


def load_weights(load: np.ndarray, cfg: RunConfig) -> np.ndarray:
    """Per-locus fitness. h = 0: heterozygotes are 1."""
    if load.size == 0:
        return np.ones((0, load.shape[1] if load.ndim == 3 else 0), dtype=np.float64)
    hom = (load[:, :, 0] == 1) & (load[:, :, 1] == 1)
    w = np.ones(load.shape[:2], dtype=np.float64)
    n_let = int(cfg.n_lethal)
    w[:, :n_let] = np.where(hom[:, :n_let], 1.0 - cfg.s_let, 1.0)
    w[:, n_let:] = np.where(hom[:, n_let:], 1.0 - cfg.s_sub, 1.0)
    return w


@dataclass
class Energy:
    fruit: np.ndarray
    tears: np.ndarray
    sweat: np.ndarray
    wound: np.ndarray
    bite: np.ndarray
    usable_blood: np.ndarray
    host: np.ndarray
    total: np.ndarray
    heme_load: np.ndarray


@dataclass
class Phenotype:
    z: np.ndarray
    energy_fruit: np.ndarray
    energy_tears: np.ndarray
    energy_sweat: np.ndarray
    energy_wound: np.ndarray
    energy_bite: np.ndarray
    usable_blood: np.ndarray
    energy_host: np.ndarray
    energy: np.ndarray
    heme_load: np.ndarray
    v_iron: np.ndarray
    cost: np.ndarray
    v_load: np.ndarray
    survive: np.ndarray
    fertility: np.ndarray
    w: np.ndarray
    exudate: np.ndarray
    biter: np.ndarray


def energy_channels(
    z: np.ndarray,
    fruit_avail: float,
    bite_weight: float,
    c_heme_in: float = 1.0,
    crowd_n: int = 0,
    k_tears: float = 0.0,
    skin_tough: float = 1.0,
    clot_without_saliva: bool = False,
) -> Energy:
    """Diet ladder. Wound and bite are blood access; calories go through digest.

    Tear film in the vial is finite (`k_tears`). Sweat, wound, and bite are
    host-body channels and are not share-limited.
    """
    fruit_use = z[:, I_FRUIT]
    fluid = z[:, I_FLUID]
    rasp = z[:, I_RASP]
    pierce = z[:, I_PIERCE]
    saliva = z[:, I_SALIVA]
    seek = z[:, I_SEEK]
    digest = z[:, I_DIGEST] if z.shape[1] > I_DIGEST else np.zeros(z.shape[0])
    fruit = pos(fruit_use) * float(fruit_avail)
    tears = pos(fluid) * (0.35 + 0.15 * pos(seek))
    if k_tears > 0.0 and crowd_n > 0:
        tears = tears * min(1.0, float(k_tears) / float(crowd_n))
    sweat = pos(fluid) * pos(rasp) * (0.25 + 0.10 * pos(seek))
    wound = pos(fluid) * pos(rasp) * (0.40 + 0.20 * pos(saliva))
    bite_access = (
        pos(rasp)
        * pos(pierce)
        * (0.15 + 0.85 * np.tanh(pos(saliva)))
        * (0.20 + 0.80 * np.tanh(pos(seek)))
    )
    tough = max(float(skin_tough), 1e-12)
    bite = bite_access / tough
    blood_access = wound + float(bite_weight) * bite
    usable_blood = blood_access * sigmoid(digest)
    if clot_without_saliva:
        usable_blood = usable_blood * np.tanh(pos(saliva))
    host = tears + sweat + usable_blood
    heme_load = float(c_heme_in) * (wound + bite_access)
    return Energy(
        fruit=fruit,
        tears=tears,
        sweat=sweat,
        wound=wound,
        bite=bite,
        usable_blood=usable_blood,
        host=host,
        total=fruit + host,
        heme_load=heme_load,
    )


def trait_cost(
    z: np.ndarray,
    energy_bite: np.ndarray,
    energy_host: np.ndarray,
    heme_load: np.ndarray,
    cfg: RunConfig,
) -> np.ndarray:
    quad = cfg.c_quad * np.square(pos(z)).sum(axis=1)
    pierce_term = cfg.c_pierce * pos(z[:, I_PIERCE]) * (energy_bite < cfg.eps_bite).astype(
        np.float64
    )
    digest_col = z[:, I_DIGEST] if z.shape[1] > I_DIGEST else np.zeros(z.shape[0])
    heme_col = z[:, I_HEME] if z.shape[1] > I_HEME else np.zeros(z.shape[0])
    digest_term = cfg.c_digest * pos(digest_col) * (energy_host < cfg.eps).astype(np.float64)
    heme_term = cfg.c_heme * pos(heme_col) * (heme_load < cfg.eps).astype(np.float64)
    return quad + pierce_term + digest_term + heme_term


def iron_viability(heme_load: np.ndarray, heme_safe: np.ndarray, cfg: RunConfig) -> np.ndarray:
    denom = 1.0 + pos(heme_safe)
    return np.exp(-cfg.beta_heme * heme_load / denom)


def _empty_ph(z: np.ndarray) -> Phenotype:
    empty = np.empty(0, dtype=np.float64)
    return Phenotype(
        z=z,
        energy_fruit=empty,
        energy_tears=empty,
        energy_sweat=empty,
        energy_wound=empty,
        energy_bite=empty,
        usable_blood=empty,
        energy_host=empty,
        energy=empty,
        heme_load=empty,
        v_iron=empty,
        cost=empty,
        v_load=empty,
        survive=empty,
        fertility=empty,
        w=empty,
        exudate=empty,
        biter=np.empty(0, dtype=bool),
    )


def phenotype(
    pop: Pop,
    cfg: RunConfig,
    crowd_n: int | None = None,
    host_shift: bool = False,
) -> Phenotype:
    z = additive_z(pop)
    if pop.n == 0:
        return _empty_ph(z)
    fruit_avail = fruit_available(pop.t, cfg)
    n_crowd = int(pop.n if crowd_n is None else crowd_n)
    k_tears = float(cfg.k_tears) if fruit_avail <= 0.0 else 0.0
    shift = bool(host_shift) and cfg.host_shift_at != "off"
    e = energy_channels(
        z,
        fruit_avail,
        cfg.bite_weight,
        cfg.c_heme_in,
        crowd_n=n_crowd,
        k_tears=k_tears,
        skin_tough=float(cfg.skin_tough) if shift else 1.0,
        clot_without_saliva=bool(cfg.clot_without_saliva) if shift else False,
    )
    heme_safe = z[:, I_HEME] if z.shape[1] > I_HEME else np.zeros(pop.n)
    v_iron = iron_viability(e.heme_load, heme_safe, cfg)
    cost = trait_cost(z, e.bite, e.host, e.heme_load, cfg)
    v_load = load_weights(pop.load, cfg).prod(axis=1)
    steep, thresh = survive_params(pop.t, cfg)
    survive = logistic(e.total, thresh=thresh, steep=steep) * v_iron
    fertility = pos(cfg.fert_a + cfg.fert_b * e.total - cfg.fert_d * cost) * v_load
    w = survive * fertility * np.exp(-cost) * v_load
    exudate = e.tears + e.sweat + e.wound
    biter = e.bite > cfg.bite_threshold
    return Phenotype(
        z=z,
        energy_fruit=e.fruit,
        energy_tears=e.tears,
        energy_sweat=e.sweat,
        energy_wound=e.wound,
        energy_bite=e.bite,
        usable_blood=e.usable_blood,
        energy_host=e.host,
        energy=e.total,
        heme_load=e.heme_load,
        v_iron=v_iron,
        cost=cost,
        v_load=v_load,
        survive=survive,
        fertility=fertility,
        w=w,
        exudate=exudate,
        biter=biter,
    )


def clutch_sizes(fert_f: np.ndarray, fert_m: np.ndarray, cfg: RunConfig) -> np.ndarray:
    raw = cfg.c0 * fert_f * fert_m
    return np.maximum(0, np.rint(raw)).astype(np.int32)
