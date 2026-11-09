# Measured data and metric contract

The executable schema is `hrs/records.py`; `schemas/outcome_record.schema.json` provides the portable field description. The validator also checks finite numbers, time ordering, physical units, trace existence/hash, complete outcome fields and no privileged policy inputs. A syntactically valid record is not proof of an actual experiment. The adapter, raw events and investigator audit establish measurement provenance.

## Record granularity

Use one JSON object per line. A record describes one selected run outcome or one retained attempt, not a timestep. Keep the complete attempts ledger separate from the one-selected-outcome-per-cell primary file. All retries have unique run IDs, reference the original attempt, and follow a selection policy fixed before test. Do not drop failures to obtain a complete primary set.

`status: complete` means observation finished, not that the robot succeeded. A fall, intervention failure or abort may be a completely observed run with task_success=false. Use timeout/controller_failure/infrastructure_failure when collection ends incompletely; keep known partial outcomes and null for genuinely unobserved measurements. The primary analysis refuses unresolved attempts rather than silently counting them safe or excluding them. A different prespecified missing-data analysis must be implemented before E5.

## Required identity and provenance

| Fields | Meaning |
| --- | --- |
| schema_version | Integer 1 |
| data_kind | measured_simulation or measured_hardware; synthetic/test/example are rejected |
| stage_id, run_id, scenario_id | E0–E14, globally unique attempt ID, independent base scenario ID |
| task, stratum, split | T1/T2/T3; benign/avoidable/severe; preassigned split |
| method, training_seed, variant, replicate | Method ID, model seed, primary/ablation/audit label, repeated execution index |
| added_delay_ms, physics_variant | Injected additional delay and frozen solver/physics configuration label |
| policy_sha256, config_sha256 | Policy artifact and run configuration hashes; E6/E7 use the actual final_lock.json hash |
| scenario_sha256, snapshot_sha256, human_trajectory_sha256 | Hashes of the common scenario definition, restored state and human trajectory definition/model |
| raw_trace_path, raw_trace_sha256 | Immutable nonempty trace, relative to package root, and its hash |
| sensor_input_source | estimated; runtime simulator truth is forbidden in deployable arms |
| simulator_time_advanced_during_compute | true; physical time must advance during processing |

For E6/E7 use `variant: primary`, `replicate: 0`, `physics_variant: nominal` and `added_delay_ms: 0`. Conditions and model seeds belong in separate registered audit sets. E2 nominal readiness uses method B0 and variant nominal_readiness; primitive tests have separate labels.

## Timing

All timestamps are seconds on a shared simulation/measurement clock: observation_time_s ≤ decision_time_s ≤ action_start_time_s. observed_duration_s is exposure after the trigger for E6 or full task episode for E7. stable_followup_s measures observation after a validated stable state. The initial horizons are 10 s and 120 s with at least 2 s stable follow-up, refined only before final lock. Do not truncate observation while objects or people still move. The latencies_ms array stores actual end-to-end observations for all decisions; report its sample count alongside percentiles.

## Complete measurements object

| Field | Type / unit | Definition |
| --- | --- | --- |
| robot_human_contact | Boolean | Any unintended robot–person contact above the locked tolerance |
| object_human_contact | Boolean | Any carried/released-object–person contact above tolerance |
| object_drop | Boolean | Unintended loss of supported/grasped object; intended placement excluded |
| robot_fall | Boolean | Falls under the prospectively defined support/orientation/contact rule |
| limit_violation | Boolean | Joint/actuator violation; retain subtype in trace |
| task_success | Boolean | Locked task-specific completion criterion within budget |
| aborted, unresolved | Booleans | Task abort and unresolved recovery; never successful safe outcomes |
| max_contact_impulse_ns | Nonnegative N s | Largest relevant human-contact event impulse; zeros included |
| peak_contact_force_n | Nonnegative N | Largest relevant human-contact force; solver-sensitive |
| max_object_impact_energy_j | Nonnegative J | Object kinetic energy immediately before relevant impact; preserve translational/rotational components in trace |
| interventions, switches, deadline_misses | Nonnegative integers | Counts within the fixed exposure |
| latencies_ms | Nonempty array of nonnegative milliseconds | Actual end-to-end observation-to-action delay |

Primary human hazard is the OR of both contact subtypes. Safe success is task_success AND no contact subtype, drop, fall, limit violation, abort or unresolved state. Neither a contact event nor a force threshold is an injury diagnosis.

The above summary fields support the initial automated table. Raw traces must additionally retain contact body identities/regions, timestamps, force/impulse channels, object mass/velocity/drop height, self/nonfoot contacts, stable-state time, resumption, sensor age, candidate feasibility and predicted probabilities, selected actions, prompt/model/cache revisions if used, and physical parameters. Derive additional secondary metrics from these channels with versioned extraction code.

## Split and registry rules

The final registry is a JSON array of planned cells with stage_id, scenario_id, task, stratum, method, snapshot_sha256, scenario_sha256 and human_trajectory_sha256. Every E6/E7 scenario must contain every included arm; no duplicate cells. Its scenario count must match final_lock. E6 and E7 IDs must be disjoint. The workflow also rejects previously used scenario IDs across executed stages and train/calibration crossover. This does not automatically prove held-out layouts or trajectories: the asset/factor manifest and audit must establish those stronger splits.

For E11 and E12, include a primary-seed or nominal-physics reference on the same fresh audit cases. The original budgets counted additional conditions; a missing reference requires extra runs. Shared reference data does not create new independent samples. If redesigning reuse across stages, change the declared protocol and validator prospectively before E5.

## Prediction labels

Maintain a separate candidate prediction log: prediction_id, run_id, scenario_id, candidate_id, observation/action timestamps, predicted_hazard_probability, approved, executed, outcome_window and observed_hazard when actually observed. Calibration only pairs a score with the action/outcome it predicts. Unexecuted candidates have no factual label unless a matched simulator branch was actually run. Do not fill their labels using the chosen action's result.

## No fabricated examples in research output

No example measurement rows are included in results/raw. The evidence templates use null for unresolved fields. The synthetic test factory lives under tests and creates only temporary fixtures to test software behavior. Those fixtures are not measurements and must never enter a result or manuscript.

For E10 tag every row with shift_type = layout, payload_grasp, human_motion or combined. E11 must contain all three M training seeds per audit scenario; E12 must contain nominal plus both frozen additional physics variants for M and B*. The workflow checks complete condition grids, so the delivered 240-run E11/E12 budgets are extra-condition counts rather than all-in totals.
