# Long arm

This file is the only legal path for autonomous continue in this repo.

Autonomous continue is allowed only along LONG_ARM.md.
Curiosity is not a transition.
Unfreezing a diet knob is a halt.

## Status

state: halt
next legal node: none
Successor engine: https://github.com/martialsystems/vial_sanguis2
Do not add a third host here.

Origin closed. Q1 immediate-cap finished. Immediate-cap 10k finished.
Cap-after-recover (user-opened; not Q2/Q3) finished. 10k on surviving seeds finished.
Host-shift after hold (user-opened; not Q2/Q3) finished.
Wound scab after hold (user-opened; not Q2/Q3) finished.
Scab plus exudate cap (user-opened; not Q2/Q3) finished. Halt. FAIL: both seeds died after shift.

Q2 (blocks) and Q3 (extra QTLs) stay closed.
An agent that opens Q2/Q3, adds factors, raises z_max, or cuts phi_max
because a seed died is out of spec.

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
- `logs/knn_cap_after_recover_1500_s{1,2,3}.json`
- `logs/fruit_forever_cap_after_recover_400.json`
- `logs/knn_cap_after_recover_10000_s{2,3}.json`
- `logs/knn_hostshift_held_10000_s{2,3}.json`
- `logs/fruit_forever_hostshift_held_400.json`
- `logs/knn_scab_held_10000_s{2,3}.json`
- `logs/fruit_forever_scab_held_400.json`
- `logs/knn_scab_exudate_cap_10000_s{2,3}.json`
- `logs/fruit_forever_scab_exudate_cap_400.json`

## Q1 immediate cap (phi_max=0.25)

| seed | arm | min n | held | F@1500 | p_biter |
|-----:|-----|------:|-----:|-------:|--------:|
| 1 | knn kinship-cap | 13 | 930 | 0.244 | 0.791 |
| 2 | knn kinship-cap | 12 | 1,048 | 0.240 | 0.013 |
| 3 | knn kinship-cap | 2 | | extinct t=9 | 0 |

Seed 2 kit was weak at t=1,500 (p_biter=0.013) and only fixed the kit in the 10k tail.

## Cap after recover (phi_max=0.25, n>=50 post-starve)

| seed | min n | t_kinship_on | held | F@1500 | p_biter@1500 | F@10000 | p_biter@10000 |
|-----:|------:|-------------:|-----:|-------:|-------------:|--------:|--------------:|
| 1 | 0 | 11 | | extinct t=12 | 0 | | |
| 2 | 16 | 8 | 517 | 0.238 | 0.980 | 0.234 | 1.000 |
| 3 | 13 | 8 | 884 | 0.236 | 0.857 | 0.235 | 1.000 |

Seed 3 survived the crash (not t=9). Seed 1 recovered to n=68 then the cap vetoed all pairs. Fruit-forever: p_biter=0, digest and heme_safe did not increase.

10k readout vs immediate-cap 10k (F about 0.23 to 0.24, pierce moved, saliva negative, seed 3 dead): rasp/detect/seek still at the ceiling. Pierce still moved (seed 2: 0.71 to 1.18; seed 3: 0.44 to 0.78). Saliva still negative. F stayed off 1. Seed 3 lived. This is a cap schedule test, not added factors.

## Host shift after hold (skin-tough 2.0, clot without saliva)

Delayed-cap seeds 2 and 3. Frozen diet until t_held, then tougher intact skin and clotting.

| seed | t_held | t_host_shift | F@10000 | p_biter | pierce | saliva | heme_load |
|-----:|-------:|-------------:|--------:|--------:|-------:|-------:|----------:|
| 2 | 517 | 527 | 0.236 | 0.005 | -0.347 | 1.465 | 0.764 |
| 3 | 884 | 894 | 0.234 | 0.007 | -0.445 | 1.553 | 0.782 |

No-shift 10k pierce was 1.176 / 0.778. Pierce did not keep rising. Saliva left the negative region with heme load still on. F stayed under 0.9. Fruit-forever: p_biter=0, shift never armed. Success on the saliva clause. Halt. Do not invent hosts 2 to 4.

## Wound scab after hold (close the wound niche)

`--wound-after-hold scab --clot-without-saliva on`, skin-tough 1.0. Delayed-cap seeds 2 and 3.

| seed | t_held | t_host_shift | F@10000 | p_biter | pierce@shift | pierce@10k | saliva@10k |
|-----:|-------:|-------------:|--------:|--------:|-------------:|-----------:|-----------:|
| 2 | 517 | 527 | 0.236 | 0.000 | 0.223 | -0.485 | 0.387 |
| 3 | 884 | 894 | 0.234 | 1.000 | -0.017 | 1.768 | 1.719 |

Wounds closed after hold, pierce rose with saliva on one seed; the other dropped pierce and stayed on exudate. Seed 3 could already clear intact skin. Seed 2 could not, and exudate still pays. 1 of 2. Do not average them into scabs creating vampires. Do not raise bite_weight. Graph closed. Halt.

## Scab plus exudate cap after hold

`--exudate-after-hold cap` with scab and clot. Delayed-cap seeds 2 and 3. skin_tough=1.0. bite_weight=1.0.

| seed | t_held | t_host_shift | last live t | last n | extinct | pierce last live |
|-----:|-------:|-------------:|------------:|-------:|---------|-----------------:|
| 2 | 517 | 527 | 526 | 1,200 | t=527 | 0.216 |
| 3 | 884 | 894 | 894 | 5 | t=895 | 0.292 |

Scab-only headline unchanged: 1 of 2 seeds raised pierce while exudate stayed open.
Exudate-cap headline: closing wounds and tears/sweat together extincts both lines in one generation. Seed 2 never had a reachable bite (died with pierce 0.22). Seed 3's pierce rise required the exudate bridge (died with p_biter=1 and n=5). That is a cliff, not a host. FAIL. Do not raise bite_weight. Origin t_first_biter=211. bite_weight=1.0. Halt. No 20k. No seed 1.

## Diet knobs (frozen)

t_starve=5, k_tears=40, bite_weight=1.0, c_pierce=0.05, c_digest=0.40,
c_heme=0.40, c_heme_in=0.30, beta_heme=2.0, survive_steep_fruit=8.0,
survive_thresh_fruit=0.40, survive_steep_host=250.0,
survive_thresh_host=0.075, n_floor=8, n_ceiling=1200.

phi_max=0.25 is the Q1 cap, not a diet knob. Default `--cap-on-at immediate`.

Do not invent a Q4.
Do not help random keep a kit.
Do not call F=1 plus more generations long evolution.
