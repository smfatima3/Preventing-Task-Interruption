# Outcomes needed, how to obtain them, and how to interpret them

## Main question

Can an action-conditioned runtime supervisor that models nearby people, carried-object dynamics, and observation-to-action delay reduce secondary physical hazards during humanoid task interruption, compared with strong stopping and semantic-fallback baselines, while preserving useful task completion?

The desired contribution is specific joint transition prediction plus evidence of its incremental value. Generic safe stopping, semantic recovery, scene-conditioned recovery and delay-aware planning already exist. Read the original 25-paper review before making novelty claims. Its historical cutoff is September 2026; separately check later work before an actual November submission.

| Claim | Evidence needed | How to obtain it | Decision rule / reporting |
| --- | --- | --- | --- |
| An interruption can introduce collateral hazards | Paired alternative rollouts from identical states; repeated mechanisms across scenes | E1 replay validation; E3 pilot; E6 intervention branches with shared human motion | Report introduced AND prevented hazards and their net difference. A post-stop collision alone is insufficient. |
| M reduces human hazards | Independent paired scenarios versus development-selected B*, with human-contact subtypes | E6, fixed post-trigger window; task-stratified paired bootstrap and exact binary checks | Negative risk difference with interval supporting reduction, plus meaningful magnitude and no hidden harm transfer. Use rare-event safeguards. |
| The improvement survives complete tasks | Full-episode hazard and task outcomes | E7 with frozen episode duration and all aborts retained | Report all counts and paired uncertainty; do not infer utility from interruption-only windows. |
| Task usefulness is preserved | Paired task-success noninferiority | E7: D = success(M)-success(B*) | Lower two-sided 95% CI > -0.05, using the preregistered margin. Otherwise claim a trade-off or uncertainty. |
| Human/object/delay inputs explain the result | Fair ablations with matched controls | E8 with three separately removed components; E9 delay study | All component results, multiplicity adjustment, and mechanism-specific metrics. Null ablations weaken the mechanism claim. |
| Method tolerates latency | Actual timestamps plus injected delay | E9, 0/100/300/600 ms additional delay; no paused physics | Plot hazard and deadline misses versus measured latency, clustered by scene. State the tested range. |
| It transfers within a bounded domain | Unseen layouts, payloads, grasps and trajectories | E10 with factors held out at scenario generation | Report each shift and the worst stratum; no universal generality claim. |
| Findings are stable | Seed, calibration and physics checks | E11–E12 with a matched primary/nominal reference | Show each seed, calibration denominators, numerical sensitivity and any reversal. |
| Results are reproducible | Raw traces → verified records → regenerated tables | E14 with code/config/checkpoint/scenario hashes and independent rerun | Retain failures, exclusions and all baseline adaptations. |

## Metrics to collect

Primary: unintended robot–human OR object–human contact above the E1-validated tolerance. Report counts/N, percentage and paired absolute risk differences in percentage points. Never substitute a weighted robot-damage score for this outcome.

Secondary: subtype contacts, unintended drops, falls, joint/actuator violations, contact impulse (N s), peak force (N), object impact energy (J), contacted body region, task success, safe success, intervention count, repeated switches, recovery time, resumption and deadline misses. Safe success requires task success with no human contact, drop, fall, limit violation, abort or unresolved state. Report raw components so this definition is auditable.

Prediction diagnostics: Brier score, reliability bins with counts, P(hazard | approved), P(approved | hazardous). Pair a prediction with the outcome of the action it predicts. Do not label an unexecuted candidate from the chosen action's outcome. Alternate-action labels require actual matched simulator branches or another explicitly validated estimator.

## Required result displays

1. Main method table: human hazards/N, both contact subtypes, object drops, falls, task success, safe success and measured latency, separately for E6 and E7.
2. Primary paired effect table: M–B* risk difference and CI for E6; E7 hazard and success difference and CI; noninferiority conclusion only after the hierarchy.
3. Introduced/prevented hazard table relative to B0 diagnostic continuation and finite-library offline best response.
4. Ablation table with all three removed components, mechanism-specific outcomes and Holm-adjusted secondary comparisons.
5. Delay plot with actual latency, injected setting, uncertainty, deadline misses and baseline coverage.
6. OOD table with shifts, per-task and worst-stratum outcomes.
7. Seed/calibration figure and table with primary plus two additional seeds; physics/threshold sensitivity table.
8. Failure gallery from actual traces/videos and a claim-evidence register, including negative and unresolved findings.

## Favorable, negative and inconclusive outcomes

The 25% relative hazard reduction is a development aspiration, not a required or predicted experimental finding. A tiny base rate can make relative reductions misleading. Report absolute counts and confidence intervals.

- If B5 matches M, frame the contribution as a strong baseline, benchmark or systematic safety analysis, unless another distinct contribution is demonstrated.
- If utility noninferiority fails, state the observed safety–utility trade-off; do not write "without loss of performance."
- If E3 finds no repeated intervention-specific mechanism, pause the learned-method route and revise the question with a documented protocol amendment.
- If all methods have zero hazards, report event-rate bounds and insufficient evidence of superiority, not guaranteed safety.
- If physics sensitivity changes the conclusion, narrow the physical claim and retain the conflicting outcomes.

An internal 8/10 quality goal requires valid controls, sufficient uncertainty reporting, a distinct contribution and reproducibility. No score or acceptance prediction can be assigned before measurements exist.
