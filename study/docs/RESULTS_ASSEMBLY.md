# Assemble the measured results package

## Directory and provenance

Each scientific stage writes `results/raw/E#/records.jsonl` and a separate `attempts.jsonl`, plus immutable trace files under `results/raw/E#/traces/`. Keep scenario definitions, snapshot assets, observation-access logs, models and simulator settings available through hashed manifests. Large assets may be stored separately if an exact, accessible version and checksum are documented; do not publish private credentials or machine secrets.

The result shells under results/templates contain no measurements. `results/RESULTS_STATUS.md` records that status. Fill only from measured, validated logs; never type a convenient number into a manuscript table.

## Commands and artifacts

```bash
python3 scripts/validate_records.py results/raw/E6/records.jsonl
python3 scripts/analyze.py --stage E6
python3 scripts/analyze.py --stage E7
python3 scripts/plot_results.py --stage E6
python3 scripts/plot_results.py --stage E7
python3 scripts/analyze.py --stage E6 --reproduce-to verification/reproductions/E6_rerun
python3 scripts/analyze.py --stage E7 --reproduce-to verification/reproductions/E7_rerun
python3 scripts/pipeline.py audit
python3 scripts/package_results.py
```

`analyze.py` refuses missing input and writes no zero-filled scientific table. It emits method_summary.csv, paired_primary.json and an interpretation report only for a complete frozen measured primary dataset. `plot_results.py` reads these generated outputs and labels event-rate uncertainty. It does not draw expected improvements. E8–E12 tables must retain their repeated-condition structure; use the generic analysis utilities and document the exact estimand.

`package_results.py` produces a dated release archive and manifest. Before E14 it labels the archive INCOMPLETE and lists incomplete stages. It never changes stage state or converts pending results into completed findings. The initial delivery archive is an execution package, not a measured-results release. Generate analysis and plots before sealing each stage. After sealing, use a new `--reproduce-to verification/reproductions/...` directory to rerun analysis and compare output hashes; this never overwrites the sealed files.

## Full result inventory

| Output | Inputs | Where used |
| --- | --- | --- |
| T1 Methods and outcomes (E6) | Paired interruption records | Main paper / full report |
| T2 Full task utility (E7) | Full-episode records | Main paper |
| T3 Introduced / prevented hazards | Matched branch pairs and continuation | Full report; key example in paper |
| T4 Mechanism ablations | E8 matched cells | Main paper |
| F1 Physical failure mechanism | Actual matched traces, two response outcomes | Main paper |
| F2 Delay response | E9 measured and injected delay, clustered intervals | Main paper |
| T5 OOD strata | E10 prespecified shift tags | Main or full report |
| F3 / T6 Calibration and seeds | E11 executed-action predictions, outcomes, all three seeds | Full report |
| T7 Numerical sensitivity | E12 nominal and variant parameterizations, threshold sweep | Full report |
| T8 Failures and exclusions | Complete attempts ledger and unresolved cases | Full report |
| T9 Claim–evidence table | E0–E14 artifacts and actual findings | Full report / concise paper argument |

## Final writing rules

Give numerator/denominator, paired effect and interval, then the interpretation. Distinguish supported, contradicted and unresolved hypotheses. Do not present a safety score as certification. Include failure cases and severe outcomes even if they weaken the headline. Keep the abstract blank of numerical claims until the final audit.

Four-page allocation: title/abstract 0.25; introduction/focused literature 0.80; problem 0.45; supervisor 0.65; setup 0.45; results 0.95; limitations/conclusion 0.45. References follow outside the four-page main-text limit. The full 25-paper review remains background; the four-page paper must make a coherent argument, not contain 25 isolated summaries.
