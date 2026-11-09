# Preventing Secondary Harm During Humanoid Task Interruption

**Implementation in progress. E0 is open; E1–E14 have not started. No HRS scientific results are available.**

This study investigates an action-conditioned runtime supervisor for human, object and robot hazards during interruption. SIMPLE is the primary environment; HumanoidToolBench is reserved for tool-use transfer. The original task families remain carry/place, shelf retrieval and confined transport.

## Current evidence

- 72 supplied ZIP members inventoried, with no original manifest mismatches.
- 37 original software tests passed; six new MuJoCo instrumentation tests passed on Modal.
- Concurrent H100 and RTX PRO 6000 infrastructure probes succeeded.
- HumanoidToolBench assets and balance/walk controller weights passed upstream setup checks.
- SIMPLE native MuJoCo G1 environment reset succeeded on RTX PRO 6000 after materializing and verifying controller weights and setting the required timing parameters.
- Isaac Sim 4.5 initialization crashed on RTX PRO 6000 and L40S; all diagnostic attempts are retained.

These checks do not establish valid HRS physics, controller competence, safety improvement, or task success.

## Browse the work

- [Required outcomes](study/docs/REQUIRED_OUTCOMES.md)
- [E0–E14 sequence and gates](study/docs/EXPERIMENT_SEQUENCE.md)
- [Current machine-readable state](study/state/status.json)
- [New MuJoCo instrumentation](study/adapters/mujoco_instrumentation.py)
- [Software tests](study/tests/test_instrumentation.py)
- [Modal diagnostic records](verification/modal/)
- [Research plan](study/sources/HRS_Research_Plan.md)
- [25-paper literature review](study/sources/Literature_Review_25_Papers.md)

<details><summary>Execution rules and remaining implementation</summary>

Stages run sequentially; independent trials within an eligible stage may use concurrent sandboxes. E2 cannot precede E1 validation, and E3 cannot precede E2 readiness. Results require actual traces, immutable manifests, validated pairing and gate receipts.

Still required: the three HRS scenarios, task-level nominal policies, perception boundary, complete controller/task replay, four validated recovery primitives, learned and semantic baseline adaptations, predictor training, frozen splits and confirmatory analysis. The new instrumentation is infrastructure, not a complete experiment adapter.

</details>

<details><summary>Reproduce software checks</summary>

Run from `study/`, using Python 3.11+ and the analysis requirements. The instrumentation tests additionally require MuJoCo 3.3.6 and NumPy. The SIMPLE runtime separately uses its upstream Python 3.10 environment.

```bash
python scripts/pipeline.py doctor
python scripts/pipeline.py status
python scripts/pipeline.py audit
python -m unittest discover -s tests -v
```

Modal launchers require credentials supplied through environment variables. No credentials are included. They are E0 diagnostic scripts and are not an E1–E14 experiment runner. Their image IDs refer to the originating Modal workspace.

</details>

The project page and final measured-results release are pending. No zero-filled tables or synthetic test fixtures are presented as scientific measurements.
