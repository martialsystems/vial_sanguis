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

Locked seed-1 commands write `logs/vampire_2500_s1.json` and `logs/random_2500_s1.json`. Those JSON files are local (gitkeep only). Seed 1 knn: min n=3, t_recover=28, t_first_biter=211, t_heme_safe_rise=695, majority biters t=1,468, F=1.000 at t=2,500. Seed 1 random: extinct t=11. Do not restamp those numbers. Extra meters: `t_held_biter` (p_biter >= 0.05 for 10 gens), `t_wound_load`, tax-gated `t_heme_safe_rise` (host blood calories and heme_safe). heme_safe tracks wounds as well as bites. Do not force t_heme_safe_rise after t_first_biter. `reclock` restamps meters only.

Hypothesis knobs are frozen. Do not retune k_tears or bite_weight to make random keep the kit. Survival, extinction, F=1, and random losing biters are answers. Change an environment factor only when it is blocking the question (ladder inversion, infinite tears, secret fruit, dirty fruit-forever). The heme clock is a meter.

k-NN is flicker, then a long rare-biter phase, then hold, then majority. Random can flicker and never hold. Do not add generations to seed 1 k-NN (n=3 to F=1 to kit fixed). LONG_ARM.md state is halt. Next legal node is none. Do not open Q2/Q3.

Seeds 2 and 3 write `logs/vampire_2500_s2.json` and friends. They do not replace seed 1. k-NN recovered on seeds 1 to 3, F=1.000, majority bite kit. Random recovered on seeds 2 and 3 from min n=6 with a flicker and no hold.

Do not add plotting UI until the crash / exudate-recovery / rasp-before-pierce / bite-last order is true on a surviving arm, or extinction is logged. `digest` and `heme_safe` are extra QTLs, not a saliva collapse.

Operator answer: verify-before-report only. Do not pin GraphForge. This engine has no FlyWire / MaleCNS template. Do not reuse `vialforge/`. Revisit a sanguis-specific pin only after seeds 2 and 3, and only if a second engine (blocks, X chromosome, pathogens) starts and agents restamp locks.

Verify-before-done is the finish gate.

This repo only (not the home VBD pack):

Autonomous continue is allowed only along LONG_ARM.md.
Curiosity is not a transition.
Unfreezing a diet knob is a halt.

If `LONG_ARM.md` has no live path, stop. Do not invent the next arm. An agent that opens Q2/Q3 or adds factors is out of spec.

## Verify

`python3 ~/agent_laws_verify_before_done/vbd_gate.py check --app-root . --claim-done`

`vbd.runtime.json` runs pytest and an 8-generation N=40 fixture. Do not use stock `/usr/bin/python3 -m pytest`.

See `LONG_ARM.md`.
