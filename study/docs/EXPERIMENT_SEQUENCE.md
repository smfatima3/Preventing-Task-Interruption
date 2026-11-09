# Ordered experiment sequence

This is the operational version of the earlier plan. All counts are starting budgets. The exact register and missing-data policy must be fixed before confirmatory collection. Passing a stage validates completion and reporting, not a positive research outcome.

| Stage | Starting budget | Main output |
| --- | ---: | --- |
| E0 — Protocol and resources | 0 | protocol_report, resource_manifest |
| E1 — Physics, sensors and replay | 36 | physics_report, replay_report, input_access_audit |
| E2 — Nominal controller and primitives | 90 | readiness_report, primitive_report, throughput_report |
| E3 — Disjoint matched-state pilot | 300 | pilot_report, pilot_power_inputs |
| E4 — Prediction data and training | 5040 | dataset_report, training_report, calibration_report |
| E5 — Baseline validation and final lock | 630 | baseline_report, development_report, power_report, final_lock_report |
| E6 — Confirmatory matched interventions | 2100 | matched_results, paired_analysis, causal_report |
| E7 — Full episodes and utility | 4200 | episode_results, paired_analysis, utility_report |
| E8 — Mechanism ablations | 480 | ablation_results, ablation_report |
| E9 — Delay stress | 720 | delay_results, delay_report |
| E10 — Held-out distribution shifts | 360 | ood_results, ood_report |
| E11 — Seed and calibration audit | 240 | seed_results, calibration_results, seed_report |
| E12 — Physics and threshold sensitivity | 240 | physics_results, sensitivity_report |
| E13 — Optional transfer validation | 0 | transfer_report |
| E14 — Final audit and paper assembly | 0 | reproduction_report, claim_evidence_report, manuscript_audit |

## E0 — Protocol and resources

Prerequisite: none. Stage type/split: `protocol`. Optional: False.

Freeze the design and data-splitting procedure. Resolve the robot, trained nominal controller, scene assets and simulator. Record exact revisions, checkpoints, licenses and local hashes. Specify how E1 numerical tolerances and E3/E5 final choices will be derived.

**Outcome needed:** A reproducible design and an executable asset inventory; no physics results yet.

**Required gates:**
- scope and claims defined
- resources and licenses verified
- splits and exclusions defined
- baseline scope honest
- contact validation procedure defined

**Files to produce:**
- `protocol_report`: a nonempty, hashed artifact explaining the measured evidence, denominators, failures and limitations.
- `resource_manifest`: a nonempty, hashed artifact explaining the measured evidence, denominators, failures and limitations.

Use `evidence/E0_evidence.template.json`. Do not set a gate to true before the supporting artifact exists.

## E1 — Physics, sensors and replay

Prerequisite: E0. Stage type/split: `validation`. Optional: False.

Run 12 designed states per task. Cover known separations, contacts, grasp loss, stable placement, stopping and contact transitions. Repeat identical snapshots; compare poses, velocities, contacts, controller memory and RNG. Audit the sensor boundary.

**Outcome needed:** Valid physical measurements and repeatable branching. A failed replay or contact test blocks the causal study.

**Required gates:**
- contact and impulse validated
- grasp and placement validated
- replay within tolerance
- no privileged policy inputs
- compute time advances

**Files to produce:**
- `physics_report`: a nonempty, hashed artifact explaining the measured evidence, denominators, failures and limitations.
- `replay_report`: a nonempty, hashed artifact explaining the measured evidence, denominators, failures and limitations.
- `input_access_audit`: a nonempty, hashed artifact explaining the measured evidence, denominators, failures and limitations.
- `records`: measured JSONL outcome records, validated against the data contract. Keep a separate complete attempt ledger and raw traces, including failed attempts.

Use `evidence/E1_evidence.template.json`. Do not set a gate to true before the supporting artifact exists.

## E2 — Nominal controller and primitives

Prerequisite: E1. Stage type/split: `readiness`. Optional: False.

Run 30 clean nominal episodes per task, plus a documented matrix of every feasible primitive in each task. Keep failures. Confirm active grip/balance control while the supervisor computes. Measure actual throughput.

**Outcome needed:** At least 24 of 30 nominal successes per task, plus separate primitive feasibility evidence. This engineering threshold is not a certification standard.

**Required gates:**
- nominal success at least 80 percent each task
- all applicable primitives executable
- common holding controller validated
- speed benchmarked

**Files to produce:**
- `readiness_report`: a nonempty, hashed artifact explaining the measured evidence, denominators, failures and limitations.
- `primitive_report`: a nonempty, hashed artifact explaining the measured evidence, denominators, failures and limitations.
- `throughput_report`: a nonempty, hashed artifact explaining the measured evidence, denominators, failures and limitations.
- `records`: measured JSONL outcome records, validated against the data contract. Keep a separate complete attempt ledger and raw traces, including failed attempts.

Use `evidence/E2_evidence.template.json`. Do not set a gate to true before the supporting artifact exists.

## E3 — Disjoint matched-state pilot

Prerequisite: E2. Stage type/split: `pilot`. Optional: False.

Generate 20 new states per task and branch the four recovery primitives plus diagnostic continuation where feasible. Use shared snapshots and human motion. Register unavailable primitives before outcomes. Estimate event rates and paired discordance.

**Outcome needed:** A repeated physical failure mechanism, or a documented negative finding. If no useful mechanism exists, stop the superior-method route and revise the question before E4.

**Required gates:**
- pilot disjoint
- feasibility masks shared
- response dependent hazards assessed
- power inputs estimated

**Files to produce:**
- `pilot_report`: a nonempty, hashed artifact explaining the measured evidence, denominators, failures and limitations.
- `pilot_power_inputs`: a nonempty, hashed artifact explaining the measured evidence, denominators, failures and limitations.
- `records`: measured JSONL outcome records, validated against the data contract. Keep a separate complete attempt ledger and raw traces, including failed attempts.

Use `evidence/E3_evidence.template.json`. Do not set a gate to true before the supporting artifact exists.

## E4 — Prediction data and training

Prerequisite: E3. Stage type/split: `train_calibration`. Optional: False.

Per task use 100 training and 40 calibration base states. Branch four modes under three physics perturbations, up to 5,040 rollouts. Fit three independent training seeds; calibrate on the separate calibration set. Record code, features, targets, losses and checkpoints.

**Outcome needed:** An auditable action-conditioned predictor, three trained artifacts, and held-out calibration. This package supplies the interface, not a pretrained predictor.

**Required gates:**
- train calibration disjoint
- outcome labels verified
- three training seeds saved
- no test tuning
- feature access equal

**Files to produce:**
- `dataset_report`: a nonempty, hashed artifact explaining the measured evidence, denominators, failures and limitations.
- `training_report`: a nonempty, hashed artifact explaining the measured evidence, denominators, failures and limitations.
- `calibration_report`: a nonempty, hashed artifact explaining the measured evidence, denominators, failures and limitations.
- `records`: measured JSONL outcome records, validated against the data contract. Keep a separate complete attempt ledger and raw traces, including failed attempts.

Use `evidence/E4_evidence.template.json`. Do not set a gate to true before the supporting artifact exists.

## E5 — Baseline validation and final lock

Prerequisite: E4. Stage type/split: `development`. Optional: False.

Use 30 new states per task across all available configured methods. Select B* with the declared development rule. Validate adaptations, freeze checkpoints and candidate library, and finalize event tolerance, horizons, test sizes, analysis and missing-data policy.

**Outcome needed:** A final lock with B*, artifact hashes, horizons and powered or transparently precision-limited sample sizes. Missing B3 must be declared; it cannot be impersonated.

**Required gates:**
- baselines faithful and fair
- primary comparator selected on development
- test sample sizes justified
- all test choices frozen
- model checkpoints frozen

**Files to produce:**
- `baseline_report`: a nonempty, hashed artifact explaining the measured evidence, denominators, failures and limitations.
- `development_report`: a nonempty, hashed artifact explaining the measured evidence, denominators, failures and limitations.
- `power_report`: a nonempty, hashed artifact explaining the measured evidence, denominators, failures and limitations.
- `final_lock_report`: a nonempty, hashed artifact explaining the measured evidence, denominators, failures and limitations.
- `records`: measured JSONL outcome records, validated against the data contract. Keep a separate complete attempt ledger and raw traces, including failed attempts.

Use `evidence/E5_evidence.template.json`. Do not set a gate to true before the supporting artifact exists.

## E6 — Confirmatory matched interventions

Prerequisite: E5. Stage type/split: `matched_test`. Optional: False.

Start from 100 independent held-out states per task (increase only before the E5 lock if justified). Run every registered arm from the identical snapshot. Keep the fixed post-trigger horizon. Compare introduced and prevented events against continuation, and M against B*.

**Outcome needed:** H1: paired risk difference, confidence interval, counts, component harm and repeated causal mechanisms. A hazard after stopping alone does not establish causation.

**Required gates:**
- pairing and exposure valid
- all primary cells accounted
- primary hazard analysis reproduced
- subtype and severity audited

**Files to produce:**
- `matched_results`: a nonempty, hashed artifact explaining the measured evidence, denominators, failures and limitations.
- `paired_analysis`: a nonempty, hashed artifact explaining the measured evidence, denominators, failures and limitations.
- `causal_report`: a nonempty, hashed artifact explaining the measured evidence, denominators, failures and limitations.
- `records`: measured JSONL outcome records, validated against the data contract. Keep a separate complete attempt ledger and raw traces, including failed attempts.

Use `evidence/E6_evidence.template.json`. Do not set a gate to true before the supporting artifact exists.

## E7 — Full episodes and utility

Prerequisite: E6. Stage type/split: `episode_test`. Optional: False.

Start with 200 new independent episodes per task across registered methods. Use the frozen episode budget and interruption schedule. Do not remove aborted tasks from the denominator. Test the predeclared hazard and utility hierarchy.

**Outcome needed:** H2: full-episode risk and success with paired uncertainty. Claim utility preservation only if the lower 95% bound on success(M)-success(B*) is greater than -0.05.

**Required gates:**
- full episode horizon respected
- all primary cells accounted
- safety and utility reported
- noninferiority interpreted correctly

**Files to produce:**
- `episode_results`: a nonempty, hashed artifact explaining the measured evidence, denominators, failures and limitations.
- `paired_analysis`: a nonempty, hashed artifact explaining the measured evidence, denominators, failures and limitations.
- `utility_report`: a nonempty, hashed artifact explaining the measured evidence, denominators, failures and limitations.
- `records`: measured JSONL outcome records, validated against the data contract. Keep a separate complete attempt ledger and raw traces, including failed attempts.

Use `evidence/E7_evidence.template.json`. Do not set a gate to true before the supporting artifact exists.

## E8 — Mechanism ablations

Prerequisite: E7. Stage type/split: `ablation_test`. Optional: False.

Use 40 new states per task with M and the three ablations. Retrain ablations if required to avoid an out-of-distribution input corruption strawman; freeze that rule and training budget at E5.

**Outcome needed:** Human, object and delay information have measured component effects, or the mechanism is not supported. Report all ablations, not only significant ones.

**Required gates:**
- ablations isolate information
- same primitives and compute budget
- secondary multiplicity reported

**Files to produce:**
- `ablation_results`: a nonempty, hashed artifact explaining the measured evidence, denominators, failures and limitations.
- `ablation_report`: a nonempty, hashed artifact explaining the measured evidence, denominators, failures and limitations.
- `records`: measured JSONL outcome records, validated against the data contract. Keep a separate complete attempt ledger and raw traces, including failed attempts.

Use `evidence/E8_evidence.template.json`. Do not set a gate to true before the supporting artifact exists.

## E9 — Delay stress

Prerequisite: E8. Stage type/split: `delay_test`. Optional: False.

Use 20 new states per task at 0, 100, 300 and 600 ms additional delay, with M, B* and the no-delay ablation. The same base scenario spans delay levels; cluster inference by base scenario.

**Outcome needed:** A response curve over actual end-to-end delay, deadline misses and confidence intervals. Injected delay is additional to real measured latency.

**Required gates:**
- actual and injected delay logged
- time never paused for reasoning
- all four delay levels present

**Files to produce:**
- `delay_results`: a nonempty, hashed artifact explaining the measured evidence, denominators, failures and limitations.
- `delay_report`: a nonempty, hashed artifact explaining the measured evidence, denominators, failures and limitations.
- `records`: measured JSONL outcome records, validated against the data contract. Keep a separate complete attempt ledger and raw traces, including failed attempts.

Use `evidence/E9_evidence.template.json`. Do not set a gate to true before the supporting artifact exists.

## E10 — Held-out distribution shifts

Prerequisite: E9. Stage type/split: `ood_test`. Optional: False.

Use 60 new states per task across prespecified unseen layouts, payload/grasp changes and human trajectories, including a combined shift. Tag the shift type before execution.

**Outcome needed:** Evidence scoped to tested shifts, worst-stratum outcomes and failures; not universal generalization.

**Required gates:**
- held out factors unseen
- shift subgroups reported
- combined shift retained

**Files to produce:**
- `ood_results`: a nonempty, hashed artifact explaining the measured evidence, denominators, failures and limitations.
- `ood_report`: a nonempty, hashed artifact explaining the measured evidence, denominators, failures and limitations.
- `records`: measured JSONL outcome records, validated against the data contract. Keep a separate complete attempt ledger and raw traces, including failed attempts.

Use `evidence/E10_evidence.template.json`. Do not set a gate to true before the supporting artifact exists.

## E11 — Seed and calibration audit

Prerequisite: E10. Stage type/split: `seed_audit`. Optional: False.

Use 120 independent audit states. Budget 240 extra rollouts for two additional M seeds only when the primary seed has already been run on these same states; otherwise budget 360 total. Include learned baseline seeds when consequential.

**Outcome needed:** Seed variability and fresh calibration diagnostics. Repeated seeds are not extra independent scenarios.

**Required gates:**
- three seeds compared on same scenarios
- primary seed reference present
- calibration audit independent
- baseline seed uncertainty disclosed

**Files to produce:**
- `seed_results`: a nonempty, hashed artifact explaining the measured evidence, denominators, failures and limitations.
- `calibration_results`: a nonempty, hashed artifact explaining the measured evidence, denominators, failures and limitations.
- `seed_report`: a nonempty, hashed artifact explaining the measured evidence, denominators, failures and limitations.
- `records`: measured JSONL outcome records, validated against the data contract. Keep a separate complete attempt ledger and raw traces, including failed attempts.

Use `evidence/E11_evidence.template.json`. Do not set a gate to true before the supporting artifact exists.

## E12 — Physics and threshold sensitivity

Prerequisite: E11. Stage type/split: `physics_test`. Optional: False.

Use 20 new states per task, including both random and boundary cases; evaluate two additional contact/timestep parameterizations with M and B*. Include a nominal reference on the same cases; reuse only if it truly exists.

**Outcome needed:** Whether contact event and impulse conclusions survive reasonable physics and measurement changes. Extra nominal runs add to the starting budget.

**Required gates:**
- solver timestep variants prespecified
- random and boundary cases included
- contact threshold sensitivity reported

**Files to produce:**
- `physics_results`: a nonempty, hashed artifact explaining the measured evidence, denominators, failures and limitations.
- `sensitivity_report`: a nonempty, hashed artifact explaining the measured evidence, denominators, failures and limitations.
- `records`: measured JSONL outcome records, validated against the data contract. Keep a separate complete attempt ledger and raw traces, including failed attempts.

Use `evidence/E12_evidence.template.json`. Do not set a gate to true before the supporting artifact exists.

## E13 — Optional transfer validation

Prerequisite: E12. Stage type/split: `transfer`. Optional: True.

Optionally use an independent simulator or bounded hardware feasibility trials only after the preceding stages. Do not induce human contact. If resources are absent, explicitly skip with a reason.

**Outcome needed:** A separately labeled transfer result, or a transparent omission. Hardware is not required for the simulation-only claim.

**Required gates:**
- transfer scope declared
- validation protocol safe and bounded
- transfer limits reported

**Files to produce:**
- `transfer_report`: a nonempty, hashed artifact explaining the measured evidence, denominators, failures and limitations.

Use `evidence/E13_evidence.template.json`. Do not set a gate to true before the supporting artifact exists.

## E14 — Final audit and paper assembly

Prerequisite: E13. Stage type/split: `audit`. Optional: False.

Regenerate results from sealed records. Inspect every failure and unresolved cell. Assemble a four-page anonymous paper with references outside the limit. Run the package audit and archive all manifests and provenance.

**Outcome needed:** A reproducible evidence package and appropriately scoped manuscript. No pass based merely on having code, a proposal or an attractive figure.

**Required gates:**
- tables reproduced from logs
- negative findings retained
- claims match evidence
- anonymity and four pages checked
- archive and provenance verified

**Files to produce:**
- `reproduction_report`: a nonempty, hashed artifact explaining the measured evidence, denominators, failures and limitations.
- `claim_evidence_report`: a nonempty, hashed artifact explaining the measured evidence, denominators, failures and limitations.
- `manuscript_audit`: a nonempty, hashed artifact explaining the measured evidence, denominators, failures and limitations.

Use `evidence/E14_evidence.template.json`. Do not set a gate to true before the supporting artifact exists.
