# Strict research execution instructions

This file governs the HRS experiment package. `AGENTS.md` and `agent.md` must remain byte-identical. The uppercase filename supports agent discovery; the lowercase filename is provided as requested. Read this entire file, START_HERE.md, config/sequence.json and docs/REQUIRED_OUTCOMES.md before acting.

## Non-negotiable scientific rules

1. Execute E0 → E1 → E2 → E3 → E4 → E5 → E6 → E7 → E8 → E9 → E10 → E11 → E12 → E13 → E14. E13 alone may be skipped with a recorded reason. Do not skip readiness because the deadline is close. Do not mark a planned experiment as completed.
2. Call `python3 scripts/pipeline.py status` and `audit` before continuing work. Begin only the next eligible stage. Finish through the evidence validator, never by manually editing state/status.json or a receipt. These are audit safeguards, not a tamper-proof security boundary.
3. Each stage needs its named artifacts, complete run manifest when applicable, SHA-256 hashes, checklist evidence, reviewer identity, findings and limitations. A checklist is an attestation that must cite real artifacts; checking boxes is not evidence by itself.
4. Proceed autonomously with reversible implementation, local analysis and validated simulation within the research scope. Missing simulator assets, checkpoints or actual observations are blockers to measurement, not permission to manufacture substitutes. Record the blocker and continue independent documentation or tooling work.
5. Never invent numerical results, contact events, videos, successes, significance, completed runs or a review score. Keep synthetic fixtures under tests only. The production loader rejects synthetic/test data and all nonfinite values. No fixture output may enter results/raw, manuscript results or evidence receipts.
6. Preserve every attempted run, including crashes, timeouts, controller failures, infeasible primitives and aborted tasks. Every attempt has a unique run_id. Link retries to originals in the scenario manifest. Never silently overwrite a run or select the best retry. Resolved primary outcomes require an explicit preregistered attempt-selection rule and a separate complete attempt ledger.
7. At E0 freeze the design/provenance and split procedure. E1–E5 may determine only the pilot choices named in config/final_lock.json. At E5 freeze the primary comparator, actual controller/model hashes, scenario registry, sample sizes, thresholds, horizons, sensor model and analysis. Changing locked design, code, data or model artifacts invalidates dependent evidence; create a documented new protocol version with fresh untouched test scenarios. Do not quietly repair a lock after viewing test results.
8. Split by base scenario and declared layout/object/human-trajectory factors. Never split neighboring frames or branches across train/calibration/development/test. Repeated seeds and conditions stay in the same scenario cluster. Simulator truth is allowed for labels and a declared offline oracle only, not for the deployable supervisor.
9. Keep strong baselines: a competent grip-preserving controlled stop B1, at least one validated learned stopping adaptation, semantic fallback B4, and the equally informed predictive heuristic B5. Document PRISM/Safe-Stop/FORTRESS adaptations. Missing original detail means unavailable, never an invented weak replacement. B0 is diagnostic continuation, not a compliant responder to a mandatory stop.
10. Use common perception, nominal controller, low-level protection, primitive feasibility masks and comparable tuning resources. Replay matched robot/object/contact/controller/RNG state and exogenous human motion. Validate replay before claiming intervention causality.
11. Advance simulated time while reasoning. Log sensing, decision and action timestamps, measured latency and added delay. Run a validated active holding controller while computing. Preserve grasp and balance; motor power-off is not the principal stop baseline. Unresolved or infeasible responses are not safe successes.
12. Keep a fixed observation horizon; do not stop recording when the robot stops. Include object/person motion and required stable follow-up. Human-contact union is the primary hazard; report robot-human and object-human components, drops, falls and severity separately.
13. Analyze M versus development-selected B* with paired scenario units and task-stratified 10,000-resample bootstrap. Use exact paired checks and event-rate bounds for rare/degenerate outcomes. Respect the E6 → E7 safety → E7 utility hierarchy. Use Holm within declared secondary families. Do not choose favorable comparisons, metrics, seeds or thresholds after test.
14. Task utility is noninferior only when the lower 95% paired confidence bound on success(M)-success(B*) is above -0.05, using the frozen margin. A nonsignificant difference is not proof. The 25% relative hazard reduction is a development aspiration, not a demanded result or review guarantee.
15. If the heuristic matches M, report a benchmark or failure study. If no signal exists, revise the question before new testing. If utility worsens, state the trade-off. If severe human/object outcomes worsen, disclose them even when another metric improves. Do not optimize narrative toward a desired 8/10.
16. Simulator contact/force/energy are physical proxies, not injury predictions or certification. Do not claim SIL, standards compliance, formal guarantees for the whole stack, or universal generalization from these experiments.
17. Default to bounded simulation. Hardware and human-subject work need a separately documented authorized safety protocol and suitable supervision; this package does not authorize hazardous contact trials. Do not publish, submit, message collaborators or spend money unless the user has authorized that action.
18. Keep the four-page anonymous workshop manuscript separate from the longer report. Remove identifying metadata/links from the submission copy; preserve private provenance. Write result sentences only after E14 evidence checks.
19. End each work session with a short handoff: last completed stage, current stage, commands/checks run, newly generated artifacts, measured findings, unresolved blockers and exact next action. Never end with an unsupported success claim.

## Required startup and completion commands

```bash
python3 scripts/pipeline.py doctor
python3 scripts/pipeline.py status
python3 scripts/pipeline.py audit
python3 -m unittest discover -s tests -v
# Begin the next eligible stage; initially E0:
python3 scripts/pipeline.py begin E0
# After creating real evidence, copy the template to a new file and fill it.
python3 scripts/pipeline.py finish E0 --evidence evidence/E0_evidence.json
```

Do not use a successful software test as E1 physics validation. The bundled tools govern sequence, record integrity and analysis; a simulator adapter, actual trained policies, real traces and investigator interpretation must still be supplied. Completion of an experimental stage means its protocol and reporting are complete; it never automatically means its scientific hypothesis is supported.
