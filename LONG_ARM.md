# Long arm

This file is the only legal path for autonomous continue in this repo.

Autonomous continue is allowed only along LONG_ARM.md.
Curiosity is not a transition.
Unfreezing a diet knob is a halt.

## Status

state: halt
next legal node: none

Origin question closed. Q1 kinship_cap finished. One 10k arm finished.
Q2 (blocks) and Q3 (post-recovery mutation / extra QTLs) stay closed.
An agent that opens Q2/Q3, adds factors, raises z_max, or softens phi_max
because seed 3 died is out of spec.

GraphForge stays unpinned. VBD is the finish gate.
The six-vial origin headline is not obsolete.

## Frozen origin JSON

Do not restamp. Origin seed-1 knn `t_first_biter=211`.

- `logs/vampire_2500_s1.json`
- `logs/vampire_2500_s2.json`
- `logs/vampire_2500_s3.json`
- `logs/random_2500_s1.json`
- `logs/random_2500_s2.json`
- `logs/random_2500_s3.json`
- `logs/fruit_forever_400_s1.json`

## Later-arm JSON

- `logs/knn_kinship_1500_s{1,2,3}.json`
- `logs/knn_kinship_fruit_forever_400_s1.json`
- `logs/knn_kinship_phi025_1500_s{1,2,3}.json`
- `logs/knn_kinship_phi025_fruit_forever_400_s1.json`
- `logs/vampire_10000_s{1,2,3}.json`

## Q1 table (phi_max=0.25)

| seed | arm | min n | held | F@1500 | p_biter |
|-----:|-----|------:|-----:|-------:|--------:|
| 1 | knn kinship-cap | 13 | 930 | 0.244 | 0.791 |
| 2 | knn kinship-cap | 12 | 1,048 | 0.240 | 0.013 |
| 3 | knn kinship-cap | 2 | | extinct t=9 | 0 |

Seed 2 kit was weak at t=1,500 (p_biter=0.013) and only fixed the kit in the 10k tail.

## vampire_10000

| seed | arm | min n | held | F@1500 | F@10000 | p_biter@10000 |
|-----:|-----|------:|-----:|-------:|--------:|--------------:|
| 1 | knn kinship-cap | 13 | 930 | 0.244 | 0.243 | 1.000 |
| 2 | knn kinship-cap | 12 | 1,048 | 0.240 | 0.230 | 1.000 |
| 3 | knn kinship-cap | 2 | | extinct t=9 | | 0 |

Pierce still moved. Saliva did not. F stayed about 0.24. Recipe is 2-of-3.

## Diet knobs (frozen)

t_starve=5, k_tears=40, bite_weight=1.0, c_pierce=0.05, c_digest=0.40,
c_heme=0.40, c_heme_in=0.30, beta_heme=2.0, survive_steep_fruit=8.0,
survive_thresh_fruit=0.40, survive_steep_host=250.0,
survive_thresh_host=0.075, n_floor=8, n_ceiling=1200.

phi_max=0.25 is the Q1 cap (one numerical retune from 0.125), not a diet knob.

Do not invent a Q4.
Do not help random keep a kit.
Do not call F=1 plus more generations long evolution.
