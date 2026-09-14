# Copyright (c) 2026 Martial Systems LLC
"""Staged host-fluid diet. Fruit is a 0/1 availability, not a blood switch."""

from __future__ import annotations

from vial_sanguis.config import RunConfig

HOST_CHANNELS = ("tears", "sweat", "wound", "bite")


def fruit_available(t: int, cfg: RunConfig) -> float:
    """1 while fruit remains, 0 after t_starve. fruit_forever is the negative control."""
    if cfg.fruit_forever:
        return 1.0
    return 1.0 if int(t) < int(cfg.t_starve) else 0.0


def survive_params(t: int, cfg: RunConfig) -> tuple[float, float]:
    if fruit_available(t, cfg) > 0.0:
        return float(cfg.survive_steep_fruit), float(cfg.survive_thresh_fruit)
    return float(cfg.survive_steep_host), float(cfg.survive_thresh_host)
