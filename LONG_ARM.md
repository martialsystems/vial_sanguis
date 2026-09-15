# Long arm

This file is the only legal path for autonomous continue in this repo.

Autonomous continue is allowed only along LONG_ARM.md.
Curiosity is not a transition.
Unfreezing a diet knob is a halt.

## Status

halt (10k arm finished)
  origin_done headline unchanged
  Q1 kinship_cap passed at phi_max=0.25 (2 of 3 seeds)
  unlocked_long ran; Q2 and Q3 not opened

legal_next: none. Stop.

### Q1 table (phi_max=0.25)

| seed | arm | min n | held | F@1500 | p_biter |
|-----:|-----|------:|-----:|-------:|--------:|
| 1 | knn kinship-cap | 13 | 930 | 0.244 | 0.791 |
| 2 | knn kinship-cap | 12 | 1,048 | 0.240 | 0.013 |
| 3 | knn kinship-cap | 2 | | extinct t=9 | 0 |

phi_max=0.125: seed 3 F@1500=0.120, flicker 598, no hold; seeds 1-2 extinct t=8. Fruit-forever (0.25): p_biter=0, digest and heme_safe did not increase.

Advance: 2 of 3 seeds held biters with F@1500<0.9. Unlock long.

### vampire_10000 (knn, kinship-cap on, phi_max=0.25)

| seed | arm | min n | held | F@1500 | F@10000 | p_biter@10000 |
|-----:|-----|------:|-----:|-------:|--------:|--------------:|
| 1 | knn kinship-cap | 13 | 930 | 0.244 | 0.243 | 1.000 |
| 2 | knn kinship-cap | 12 | 1,048 | 0.240 | 0.230 | 1.000 |
| 3 | knn kinship-cap | 2 | | extinct t=9 | | 0 |

Past t=1,500 with F off 1: rasp/fluid/seek already near the ceiling (flat). Pierce deepened (seed 1: 0.40 to 0.90; seed 2: -0.13 to 1.43). Bite energy rose. Saliva stayed negative. Digest and heme_safe were already high. Kit is background; pierce still moved. Halt. Do not invent Q4.

Claim ban: this is not an origin of hematophagy. The six-vial headline is not obsolete.

## Frozen

t_starve, k_tears, bite_weight, c_pierce, c_digest, c_heme,
c_heme_in, beta_heme, survive thresholds, n_floor, n_ceiling,
seed-1 origin locks, five laws, no immigration, no stylet,
no saliva collapse, no FlyWire/MaleCNS, no GraphForge pin.

phi_max default 0.25 is a Q1 cap, not a diet knob. 0.125 refused all pairs
after the crash (numerical). One retune allowed; freeze 0.25.

## Graph

Q1 kinship_cap
Q2 blocks (linkage), only if Q1 failed to hold biters at F<0.9
Q3 post-recovery mutation / extra QTLs, only if Q1 and Q2 failed
halt_no_long_evo if Q1 to Q3 all fail

unlocked_long only if some new arm has t_held_biter set AND F(t=1500)<0.9
on at least 2 of 3 seeds, fruit-forever clean, five laws green.
Then one arm vampire_10000 on that recipe, seeds 1 to 3, stop.

Do not start vampire_10000 until unlocked_long.
Do not invent a Q4.
Do not help random keep a kit.
Do not call F=1 plus more generations long evolution.

## Q1 CLI

```text
.venv/bin/python -m vial_sanguis run --arm knn --mode knn --kinship-cap on \
    --phi-max 0.25 --generations 1500 --n 1000 --seed S --starve-at 5 \
    --out logs/knn_kinship_1500_sS.json
```

Fruit-forever: same plus `--fruit-forever --generations 400 --out logs/knn_kinship_fruit_forever_400_s1.json`.

New locks only. Never overwrite logs/vampire_2500_s1.json.

## Halt

If F(t=1500)>=0.9 on every holding arm after Q1 to Q3, or biters do not hold,
or fruit-forever is dirty, or a diet knob changed, or a lock was restamped,
or immigration appeared: halt. Leave the six-vial headline unchanged.

## Meters

Leave the first-crossing LESSONS.md note as-is. No further meter work is required for the origin headline.
