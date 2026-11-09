# Connecting a real simulator and policies

`hrs/adapter.py` defines the interface. `UnconfiguredAdapter` raises an explicit error. It does not generate fake robot traces, contact outcomes or model scores. Complete this integration at E0/E1 using a simulator and trained controller you can reproduce.

## Implementation obligations

1. Resolve a compatible robot model, nominal controller, collision geometry, contact/solver settings, object inertias/grasp model and human avatar. Record licenses, revisions, hashes and commands in the resource manifest. Pin simulator and driver versions.
2. Export/import complete snapshots: generalized poses/velocities, objects, grasp/contact state, controller recurrent/integrator state, scheduler clock, RNG, human-motion generator and all plugin state. Verify restored rollouts within a defined tolerance at E1.
3. Expose observations through a separate perception interface. Policies may see estimated geometry, human motion, object mass/grasp estimates, proprioception and timestamps. Privileged state is allowed only in outcome labeling or a declared offline oracle. Log which channels each method receives.
4. Maintain one validated active holding controller while a supervisor computes. Advance physics using actual or explicitly emulated processing delay. Log observation, decision and action-onset times. Reject stale responses according to the frozen rule.
5. Generate the same candidate feasibility mask and primitives for comparable arms. Log rejected candidates, prediction scores, chosen response, unavailable actions and unresolved cases.
6. Record raw contact events with both body identities, person body region, force, impulse, contact duration and object velocity/mass at impact. Never infer all contacts from a single distance threshold without validation. Preserve simulator units and solver settings.
7. Run until the locked horizon; do not stop capture at robot standstill. Record stable-state follow-up and any lingering object/person motion. Full-episode runs must meet the locked exposure rule, including approved terminal-state continuation semantics.
8. Save an immutable per-attempt trace before writing its summary record. Use relative paths within this package, with SHA-256. Atomic writes and unique run IDs prevent overwriting. Keep the complete attempt ledger separately from the primary selected outcome set.

## Integration work still required

The package does not train a policy, implement PRISM/Safe-Stop/FORTRESS, supply a physics engine or execute robotics trials. Those are research implementation tasks, not completed results. `scripts/collect_stage.py` invokes a user-provided adapter's `execute_registered_stage` after checking stage eligibility. Its output is validated before it can support a gate.

The registry at E5 must describe the planned selected-outcome cells for E6 and E7: stage_id, scenario_id, task, stratum, method, snapshot_sha256, scenario_sha256 and human_trajectory_sha256. B0 may be retained as diagnostic continuation but never counted as compliant mandatory-stop behavior.

## Snapshot and causality caveat

Shared exogenous human motion makes intervention comparisons interpretable within the simulator. If humans react to robot behavior, freeze and share the response model; realized paths may then differ legitimately. Document the corresponding causal estimand. The starter validator assumes identical exogenous trajectory definitions, not identical realized reactive trajectories.
