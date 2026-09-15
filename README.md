# vial_sanguis

Under an explicit diet ladder and an allowed population crash, does a Drosophila-like sponging labellum evolve prestomal-tooth rasping and then a costly bite, and how many generations / how deep a bottleneck does that take?

Diet ladder plus crash: exudate recovery is repeatable. Majority bite kit, on this engine, is k-NN plus founder IBD going to 1. Random can flicker and lose it.

Six default vials (k=3, N=1,000, 2,500 generations, t_starve=5). Environment knobs are frozen. GraphForge is unpinned. VBD is the finish gate.

`t_first_biter` is any generation with p_biter > 0 (a flicker). `t_held_biter` is the first generation of a run with p_biter >= 0.05 for 10 consecutive generations. `t_wound_load` is first t with mean energy_wound above `eps_heme`. `t_heme_safe_rise` requires mean wound+bite calories above `eps_heme` and mean heme_safe >= 0.12. heme_safe tracks heme load, which includes wounds. t_first_biter tracks the bite threshold. Do not force heme to wait on flicker.

Seed 1 knn lock, do not restamp: census crashed to 3 at t=6, recovered at t=28, first biter at t=211 (mean rasp 0.575, mean pierce 0.027), heme_safe rose at t=695, majority biters at t=1,468. At t=2,500: n=1,200, F=1.000, p_biter=1. Seed 1 random went extinct at t=11 (min n=1). Fruit-forever to t=400: p_biter=0; digest and heme_safe did not increase. Logs are local: `logs/vampire_2500_s{1,2,3}.json`, `logs/random_2500_s{1,2,3}.json`.

| seed | mate | min n | t_recover | flicker | t_held_biter | t_majority | t_wound_load | t_heme_safe_rise | final F | final p_biter |
|-----:|------|------:|----------:|--------:|-------------:|-----------:|-------------:|-----------------:|--------:|--------------:|
| 1 | knn | 3 | 28 | 211 | 1,108 | 1,468 | 28 | 695 | 1.000 | 1.000 |
| 1 | random | 1 | | | | | | | extinct t=11 | 0 |
| 2 | knn | 18 | 22 | 412 | 638 | 1,211 | 21 | 297 | 1.000 | 0.914 |
| 2 | random | 6 | 16 | 162 | | | 15 | | 0.821 | 0 |
| 3 | knn | 13 | 21 | 792 | 1,111 | 1,301 | 19 | 901 | 1.000 | 0.998 |
| 3 | random | 6 | 22 | 128 | | | 22 | | 0.830 | 0 |

k-NN does not go flicker to majority. It goes flicker, then a long rare-biter phase, then hold, then majority:

| seed | flicker to held | held to majority |
|-----:|----------------:|-----------------:|
| 1 | 211 to 1,108 (897 gen) | 360 gen |
| 2 | 412 to 638 (226 gen) | 573 gen |
| 3 | 792 to 1,111 (319 gen) | 190 gen |

The bite kit is a late fixation on an already recovered, already inbreeding census. Random can hit the flicker column and never enter the hold column.

On every surviving flicker generation, mean rasp exceeded mean pierce. Seed 2 knn: wound-load t=21, heme tax t=297 (wound+bite 0.376, p_biter=0), bite flicker t=412. That heme clock is wound iron, not the t=16 mean-drift trip and not a bite-kit story. Seeds 1 and 3 are wound-first too (t_wound_load 28 and 19, before heme tax). Seed 1 knn is one inbred line after a 3-fly bottleneck. Seeds 2 and 3 show the same k-NN end-state with milder crashes (n=18, n=13). Random recovered on seeds 2 and 3 from min n=6 with a flicker and no hold.

Do not add generations to seed 1 k-NN. It is done: n=3 to F=1 to kit fixed.

## Long arm

Halt. Q2 and Q3 stay closed. The origin headline above is not obsolete.

Under kinship cap `phi_max=0.25`, a rasp-first kit can persist off F=1, and pierce can keep rising through 10,000 generations. That is the thing the F=1 vials could not show. Rasp, detect, and seek sat at the ceiling (clipped, not more deep time). Saliva stayed negative: antihemostasis was not selected on this ladder. This is not an origin of hematophagy, not saliva evolution, and not a claim that random would do the same.

Q1 (knn, kinship-cap on, 1,500 generations): seeds 1 and 2 held with F@1500 = 0.244 and 0.240. Seed 3 extinct at t=9 (2-fly crash under a kinship veto; biological, logged). Fruit-forever stayed clean. Unlock used `t_held_biter` set and F@1500 < 0.9 on 2 of 3 seeds. Seed 2 was below the hold threshold at t=1,500 (p_biter=0.013) and only fixed the kit in the 10k tail.

10k traces (seeds 1 and 2): F stayed about 0.24 to 0.23. Pierce deepened (0.40 to 0.90; -0.13 to 1.43) and bite energy rose. Seed 3 died at t=9 again. Graph said one 10k arm, then halt. Raising `z_max` or softening `phi_max` to save seed 3 is a new experiment, not a continue.

Closed vial of diploid cyclorrhaphan flies. Fruit is removed at `t_starve` (default 5). Most of the census starves. A rare tail can live on host exudates (tears, sweat, wounds). Additive QTLs for labellar rasp, fluid detection, saliva, host-seeking, a costly pierce, midgut proteolysis (`digest`), and heme/iron detox (`heme_safe`) can assemble a shallow-biting feeding mode. Hematophagy here is host-fluid feeding, including blood from wounds or shallow cuts.

The engine is vectorized NumPy, one generation per step. Ancestral mouthparts are sponging. The only morphological path is labellum plus pseudotracheae to enlarged sclerotized prestomal teeth to rasp / pool feeding. Census may fall to `n_floor` (default 8) or to 0. Inbreeding is measured.

## Diet and fitness

Fruit energy is `clip(fruit_use, 0, inf) * fruit_available` with `fruit_available` in `{0, 1}`. Host intake is staged:

- tears: `fluid_detect`
- sweat: `fluid_detect * rasp`
- wound: `fluid_detect * rasp` and some saliva
- bite: `rasp * pierce * saliva * seek` on intact skin

Tear film in the vial is finite (`k_tears`, default 40). Sweat, wound, and bite are host-body channels. Wound and bite are blood access. Calories are `usable_blood = (energy_wound + energy_bite) * sigmoid(digest)`. Unused blood is not calories; it still adds to `heme_load`. Iron tax: `v_iron = exp(-beta_heme * heme_load / (1 + clip(heme_safe, 0, inf)))`, and viability is multiplied by `v_iron`.

Bite carries a standing pierce cost while `energy_bite` is below `eps`. `digest` costs while host energy is below `eps`. `heme_safe` costs while `heme_load` is below `eps`. Fitness is `survive * fertility * exp(-cost) * v_load`, with `v_load` the product of `(1-s)` at homozygous hidden recessives. Survival is a logistic of energy times `v_iron`; the energy threshold hardens after starve.

Default QTL order: fruit_use, fluid_detect, rasp, pierce, saliva, seek, locomotion, fertility_circuit, stab, fa, digest, heme_safe. `digest` is not saliva. Mating is random or k-NN (`k=3`) on fruit_use plus locomotion before starve, and on `{fluid_detect, rasp, pierce, seek}` after. Load is excluded from similarity.

Hypothesis knobs (no fruit after t_starve, no immigration, finite tears, digest on wound/bite calories, unused blood loads heme, unused pierce/digest/heme_safe cost, census may hit 0) are frozen after seed 1. Changing one is a new experiment with new lock names. Meter gates (`t_wound_load`, `t_heme_safe_rise`, `t_held_biter`) may be recomputed on existing logs.

## Defaults

`n=1000`, `generations=2500`, `seed=1`, `t_starve=5`, `mating_mode=assortative_knn`, `k=3`, `n_floor=8`, `n_ceiling=1200`, `n_load=64`, `n_lethal=16`, `s_let=1.0`, `s_sub=0.25`. Cap default is off: never invent adults.

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
.venv/bin/python -m vial_sanguis reclock logs/vampire_2500_s1.json
```

Seeds 2 and 3 use the same flags with `--seed 2` or `--seed 3` and matching `--out` names. `--fruit-forever` is the negative control. `--cap off` is default. `--bite-weight` and `--n-floor` are flags.

Each run writes the summary JSON and a sibling `.jsonl`. JSON is local; `logs/` keeps `.gitkeep` only. `reclock` restamps only first-time meters, not generation rows.

Success on seed 1 is: crash after starve (`min n <= 20` or extinction); if surviving, `t_first_biter > t_recover`; mean rasp at `t_first_biter` above mean pierce at that generation. Tax-gated `t_heme_safe_rise` needs host blood calories, not a mean trip at tiny n. Fruit-forever must not reach `p_biter > 0.05` by t=400, and neither `digest` nor `heme_safe` increases. Failure (extinction) is a result.

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
| `src/vial_sanguis/cli.py` | `python -m vial_sanguis run` and `reclock` |
| `AGENTS.md` | Five laws in pytest/VBD, no GraphForge pin |
| `LONG_ARM.md` | Only legal autonomous continue; currently none |
| `tests/` | Init, starve, extinction, IBD, bite cost, digest/heme, clocks, five laws, fruit-forever |
