# Agent notes: vial_sanguis

MIT. Closed-form NumPy generation engine. Inspired by `fly_vial`, not a fork.

Question: under an explicit diet ladder and an allowed population crash, does a Drosophila-like sponging labellum evolve prestomal-tooth rasping and then a costly bite, and how many generations / how deep a bottleneck does that take?

## Five laws

1. Closed vial. No immigration, no restock, no wild-type injection.
2. Load required. Hidden recessives exist. Load is excluded from mating similarity.
3. Census may fall. Never invent adults to hold N. Extinction is a logged result.
4. Diet ladder required. Tears, sweat, wound, then bite. No single blood calorie switch. Blood calories go through `digest`; unused blood still loads heme.
5. Mouthpart path is prestomal-tooth / labellar rasp. No new mandibles. No mosquito stylets. `digest` and `heme_safe` are their own QTLs, not a saliva collapse.

These laws live in pytest (`tests/test_five_laws.py`) and in the VBD fixture. They are not a GraphForge pin.

v1 is autosomal-only. Free recombination. Pair-based Mendelian. `--cap off` is the default: ceiling clips from above, shortage is real.

Locked seed-1 commands write `logs/vampire_2500_s1.json` and `logs/random_2500_s1.json`. Those JSON files are local (gitkeep only). Seed 1 knn: min n=3, t_recover=28, t_first_biter=211, t_heme_safe_rise=695, majority biters t=1,468, F=1.000 at t=2,500. Seed 1 random: extinct t=11. Do not restamp those numbers. Seeds 2 and 3 write `logs/vampire_2500_s2.json` and friends. They do not replace seed 1. k-NN seeds 2 and 3 also recovered and ended at F=1.000 with majority biters (min n=18 and 13). Random seeds 2 and 3 recovered from min n=6 with a transient first biter and final p_biter=0.

Do not add plotting UI until the crash / exudate-recovery / rasp-before-pierce / bite-last order is true on a surviving arm, or extinction is logged. `digest` and `heme_safe` are extra QTLs, not a saliva collapse.

Operator answer: verify-before-report only. Do not pin GraphForge. This engine has no FlyWire / MaleCNS template. Do not reuse `vialforge/`. Revisit a sanguis-specific pin only after seeds 2 and 3, and only if a second engine (blocks, X chromosome, pathogens) starts and agents restamp locks.

Verify-before-done is the finish gate.

## Verify

`python3 ~/agent_laws_verify_before_done/vbd_gate.py check --app-root . --claim-done`

`vbd.runtime.json` runs pytest and an 8-generation N=40 fixture. Do not use stock `/usr/bin/python3 -m pytest`.
