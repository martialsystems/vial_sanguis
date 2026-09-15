# Copyright (c) 2026 Martial Systems LLC
"""Run hyperparameters for the closed vial."""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class RunConfig:
    n: int = 1000
    generations: int = 2500
    seed: int = 1
    t_starve: int = 5
    fruit_forever: bool = False
    p_female: float = 0.5
    sex_imbalance_max: int = 50
    k_a: int = 12
    n_load: int = 64
    n_lethal: int = 16
    s_let: float = 1.0
    s_sub: float = 0.25
    h_load: float = 0.0
    lambda_init: float = 4.0
    sigma_init: float = 0.08
    fruit_init: float = 1.15
    z_max: float = 2.0
    sigma_mu: float = 0.02
    p_rare: float = 0.004
    rare_mu: float = 0.18
    rare_sigma: float = 0.06
    u: float = 0.002
    mating_mode: str = "assortative_knn"
    k: int = 3
    kinship_cap: bool = False
    phi_max: float = 0.25
    d_cluster: float = 2.0
    m_max: int = 1
    arm: str = "vampire"
    cap: str = "off"
    n_floor: int = 8
    n_ceiling: int = 1200
    fail_n_min: int = 8
    fail_viability: float = 0.08
    bite_weight: float = 1.0
    bite_threshold: float = 0.08
    exudate_threshold: float = 0.15
    eps_bite: float = 0.002
    eps: float = 0.05
    c0: float = 8.0
    c_quad: float = 0.010
    c_pierce: float = 0.05
    c_digest: float = 0.40
    c_heme: float = 0.40
    c_heme_in: float = 0.30
    beta_heme: float = 2.0
    heme_rise: float = 0.12
    eps_heme: float = 0.05
    held_biter_p: float = 0.05
    held_biter_w: int = 10
    k_tears: float = 40.0
    survive_steep_fruit: float = 8.0
    survive_thresh_fruit: float = 0.40
    survive_steep_host: float = 250.0
    survive_thresh_host: float = 0.075
    fert_a: float = 1.0
    fert_b: float = 0.35
    fert_d: float = 0.90

    def payload(self) -> dict:
        return asdict(self)

    def ceiling(self) -> int:
        if self.cap == "on":
            return int(self.n)
        return int(self.n_ceiling)
