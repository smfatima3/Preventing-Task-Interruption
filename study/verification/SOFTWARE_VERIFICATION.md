# Software verification — 4 November 2026

**37 tests passed; 0 failures, 0 errors, 0 skipped.** The measured test execution took 3.944 seconds on Python 3.12.14 with NumPy 2.3.5, SciPy 1.17.0 and Matplotlib 3.10.8. Python compilation and the initial evidence-integrity audit also passed.

The tests cover sequential stage enforcement, missing evidence, altered locks and trace hashes, synthetic-data rejection, nonfinite outcomes, missing/duplicate pairs, exposure duration, registry coverage, readiness thresholds, complete ablation/seed/physics grids, hazard union/safe-success definitions, known-answer paired statistics, exact rate bounds, rare-event flags, calibration denominators, Holm adjustment and scenario-level repeated-condition inference.

An end-to-end CLI test generated analysis and plots inside a disposable fixture package, then reproduced the primary CSV/JSON/report byte-for-byte. All such inputs were synthetic software fixtures and were deleted with their temporary directory. They were not humanoid simulations and are not scientific results.

The delivered scientific state remains E0–E14 pending. results/raw and results/computed contain no measured robot records or figures. The unconfigured adapter and confirmatory analysis both refuse to invent missing results.

These checks establish the tested software behavior, not safety, baseline fidelity, physics validity, a supported hypothesis, certification, publication readiness or an 8/10 review score. Additional tests are required when a simulator, policies and event-extraction implementation are added. The exact tested source hashes and test names are recorded in software_verification.json.
