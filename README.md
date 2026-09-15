# vial_sanguis

Under an explicit diet ladder and an allowed population crash, does a Drosophila-like sponging labellum evolve prestomal-tooth rasping and then a costly bite, and how many generations / how deep a bottleneck does that take?

This is not an origin of hematophagy.

## Origin

Six vials (k=3, N=1,000, 2,500 generations, t_starve=5). After fruit is gone the census crashes; exudate recovery is repeatable. Random mating flickers a biter and loses it. k-NN reaches a majority bite kit at F=1. Origin seed-1 knn lock: `t_first_biter=211` (mean rasp 0.575, mean pierce 0.027). The census crashed to 3 at t=6, recovered at t=28, heme_safe rose at t=695, majority biters at t=1,468. At t=2,500: n=1,200, F=1.000, p_biter=1. Seed 1 random went extinct at t=11. Fruit-forever to t=400: p_biter=0.

| seed | mate | min n | t_recover | flicker | t_held_biter | t_majority | final F | final p_biter |
|-----:|------|------:|----------:|--------:|-------------:|-----------:|--------:|--------------:|
| 1 | knn | 3 | 28 | 211 | 1,108 | 1,468 | 1.000 | 1.000 |
| 1 | random | 1 | | | | | extinct t=11 | 0 |
| 2 | knn | 18 | 22 | 412 | 638 | 1,211 | 1.000 | 0.914 |
| 2 | random | 6 | 16 | 162 | | | 0.821 | 0 |
| 3 | knn | 13 | 21 | 792 | 1,111 | 1,301 | 1.000 | 0.998 |
| 3 | random | 6 | 22 | 128 | | | 0.830 | 0 |

## Long arm

Kinship cap `phi_max=0.25`. Two of three seeds. F about 0.24 at 10k. Pierce still moved. Saliva did not. Seed 3 extinct at t=9. Seed 2 kit was weak at t=1,500 (p_biter=0.013) and only fixed the kit in the 10k tail.

Halt. Q2 and Q3 stay closed. Opening them, or adding factors, is out of spec.

Cap after recover (`--cap-on-at recover`, phi_max still 0.25): seed 3 survived the crash (min n=13, recover t=16) and held biters at F=0.236, p_biter=0.857 at t=1,500. Seed 2 also held (F=0.238, p_biter=0.980). Seed 1 hit n=68 at t=11, then the cap vetoed all pairs (extinct t=12). Fruit-forever stayed clean. 10k on seeds 2 and 3: F stayed 0.234 / 0.235, p_biter=1, pierce still moved (0.71 to 1.18; 0.44 to 0.78), saliva still negative, rasp/detect/seek still at the ceiling. Immediate-cap 10k had seed 3 dead at t=9. This is a cap schedule test.

## Locks

Frozen origin JSON (do not restamp). Seed-1 knn `t_first_biter=211`:

- `logs/vampire_2500_s1.json`
- `logs/vampire_2500_s2.json`
- `logs/vampire_2500_s3.json`
- `logs/random_2500_s1.json`
- `logs/random_2500_s2.json`
- `logs/random_2500_s3.json`
- `logs/fruit_forever_400_s1.json`

Later arms (new files only):

- `logs/knn_kinship_1500_s{1,2,3}.json` (phi_max=0.125; numerical fail)
- `logs/knn_kinship_fruit_forever_400_s1.json`
- `logs/knn_kinship_phi025_1500_s{1,2,3}.json`
- `logs/knn_kinship_phi025_fruit_forever_400_s1.json`
- `logs/vampire_10000_s{1,2,3}.json`
- `logs/knn_cap_after_recover_1500_s{1,2,3}.json`
- `logs/fruit_forever_cap_after_recover_400.json`
- `logs/knn_cap_after_recover_10000_s{2,3}.json`

Diet knobs (VBD-checked; frozen):

| Knob | Value |
|------|------:|
| t_starve | 5 |
| k_tears | 40 |
| bite_weight | 1.0 |
| c_pierce | 0.05 |
| c_digest | 0.40 |
| c_heme | 0.40 |
| c_heme_in | 0.30 |
| beta_heme | 2.0 |
| survive_steep_fruit | 8.0 |
| survive_thresh_fruit | 0.40 |
| survive_steep_host | 250.0 |
| survive_thresh_host | 0.075 |
| n_floor | 8 |
| n_ceiling | 1,200 |

JSON is local; `logs/` keeps `.gitkeep` only.

## How to run

```text
python3.12 -m venv .venv
.venv/bin/python -m pip install -e ".[dev]"
.venv/bin/python -m pytest
.venv/bin/python -m vial_sanguis run --arm vampire --mode knn --k 3 \
    --generations 2500 --n 1000 --seed 1 --starve-at 5 \
    --out logs/vampire_2500_s1.json
.venv/bin/python -m vial_sanguis run --arm random --mode random \
    --generations 2500 --n 1000 --seed 1 --starve-at 5 \
    --out logs/random_2500_s1.json
```

`--fruit-forever` is the negative control. `--cap off` is default.

## Non-claims

- This does not evolve a real organ in 2500 generations.
- QTLs are scalar proxies, not GRNs or imaginal-disc models.
- No live FlyWire / MaleCNS stepper.
- No pathogen transmission module in v1.
- Success is: crash, exudate recovery, rasp before pierce, bite last.
- Failure is also a result: log extinction instead of silently capping N.

## Files

| Path | Role |
|------|------|
| `src/vial_sanguis/config.py` | Run hyperparameters |
| `src/vial_sanguis/genome.py` | Diploid QTLs, load, founder IDs |
| `src/vial_sanguis/diet.py` | Fruit 0/1 and host stages |
| `src/vial_sanguis/fitness.py` | Energy ladder, blood calories, iron tax |
| `src/vial_sanguis/mating.py` | Random and k-NN pairs |
| `src/vial_sanguis/inheritance.py` | Mendelian haplotypes, mutation |
| `src/vial_sanguis/population.py` | Generation loop, ceiling, extinction |
| `src/vial_sanguis/metrics.py` | F, phi, energies, first times |
| `src/vial_sanguis/cli.py` | `python -m vial_sanguis run` |
| `AGENTS.md` | Five laws; VBD gate; no GraphForge pin |
| `LONG_ARM.md` | Halt. Next legal node: none |
| `tests/` | Init, starve, extinction, IBD, bite cost, digest/heme, clocks, five laws |
