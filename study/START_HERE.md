# HRS experiment execution package

Prepared 4 November 2026. Status: software and study package prepared; scientific experiments not run.

This package turns the existing research plan into an ordered, auditable workflow. It includes the full research plan and 25-paper review, strict agent instructions, E0–E14 experiment cards, configuration and evidence templates, a real-data validator, paired analysis tools, plotting tools, and result shells. The simulator adapter and trained robot/supervisor policies are intentionally unimplemented; no robotics results are fabricated.

## Start in this order

1. Read AGENTS.md (identical to agent.md), docs/REQUIRED_OUTCOMES.md and docs/EXPERIMENT_SEQUENCE.md.
2. Use Python 3.11 or later. Run `python3 scripts/pipeline.py doctor`, `status`, and `audit`. The governance CLI uses only the standard library.
3. In your Python environment, install the analysis dependencies with `python3 -m pip install -r requirements-analysis.txt`, then run `python3 -m unittest discover -s tests -v`. For governance-only checks without those dependencies, run `python3 -m unittest discover -s tests -p test_integrity.py -v`. The package does not automatically install or download anything.
4. Resolve the simulator, trained nominal controller, robot/object assets and adapter. Complete config/protocol.json resources and E0 evidence. See docs/ADAPTER_CONTRACT.md. Do not start by training locomotion from scratch.
5. Run `python3 scripts/pipeline.py begin E0`. Prepare real artifacts under evidence/E0, hash them with the CLI, fill evidence/E0_evidence.json from its template, then finish E0. Repeat one stage at a time. A failed prerequisite blocks progression.
6. At E5 complete config/final_lock.json and the scenario registry. Freeze analysis, B*, checkpoint hashes, event tolerance and test N before E6. Subsequent code/config changes are detected by receipt auditing.
7. Produce all run attempts, event traces and the selected outcome records. Use `python3 scripts/validate_records.py PATH` before accepting a stage. Use `python3 scripts/analyze.py --stage E6` and then E7 to generate descriptive and paired result files from measured data.
8. Follow docs/RESULTS_ASSEMBLY.md for all figures/tables, seed and calibration analyses, exclusions and claim checks. Complete E14 before calling the research package publication-ready.

## What is ready and what is missing

| Item | Current state |
| --- | --- |
| Research plan, literature review and evidence targets | Included |
| Ordered workflow, validators, analysis and plotting code | Included; see verification/SOFTWARE_VERIFICATION.md for executed software tests |
| Simulator, robot assets, nominal policy and supervisor checkpoints | Not bundled; must be resolved at E0 |
| Robot simulation, training and measured scientific results | Not executed |
| Scientific results directory | Empty measured-data folders plus clearly marked templates |
| Workshop manuscript | Four-page outline and result-writing rules; no fabricated result sentences |

The execution host had no importable MuJoCo, Isaac Sim or PyTorch at preparation time. This is an environment observation, not a requirement to use any of them. Select one simulator compatible with a verified whole-body controller and valid grasp/contact behavior.

The starting E3–E12 budget is 14,310 rollouts/episodes from the prior plan. It excludes E1/E2, power-driven increases and some reference/extra-seed evaluations. E11 needs 360 total M rollouts if no primary-seed audit already exists; E12 also needs nominal reference runs unless available on the same states. Do not treat 14,310 as an exact all-inclusive compute quote.

The workshop deadline supplied by you is 5 November 2026, 23:59 AoE (6 November, 16:59 Pakistan). Starting a full study from absent robot assets this close to the deadline is not a credible completion commitment. If E1–E3 cannot be completed, keep the output a clearly labeled proposal or preliminary failure study; do not claim the full empirical result.

## Files to use

- `AGENTS.md` / `agent.md`: strict execution and integrity rules.
- `docs/EXPERIMENT_SEQUENCE.md`: exact stage procedures, gates and outputs.
- `docs/REQUIRED_OUTCOMES.md`: what evidence is needed and how it changes the claim.
- `docs/DATA_AND_METRICS.md`: measured record and trace contract.
- `docs/STATISTICAL_ANALYSIS_PLAN.md`: estimands, pairing, uncertainty and limitations of the bundled implementation.
- `sources/HRS_Research_Plan.pdf` and `.md`: full original plan.
- `sources/Literature_Review_25_Papers.md`, `references.bib`: source-backed background.
- `results/`: future measured logs, calculated outputs and empty table shells.
- `verification/`: actual software verification evidence, never robotics evidence.
