# Implementation status and next development tasks

This is an execution and analysis framework. It is not a completed humanoid policy implementation or an executed empirical study.

| Component | Implemented here | Work still required |
| --- | --- | --- |
| Stage ordering | E0–E14 state machine; prerequisite and optional-stage rules | Produce actual stage evidence |
| Evidence integrity | Required artifacts/checks, SHA-256 receipts, code/config locks, trace checks | Verify measurement authenticity and scientific validity; hashes alone cannot do this |
| Data contract | Strict measured-record validator, JSON Schema, pairing/registry/exposure checks | Simulator-specific contact/event extraction and dataset generation |
| Robot environment | Abstract adapter contract and collector entrypoint | Simulator, robot/object/human assets, trained controller, replay implementation |
| Methods | Precise baseline and supervisor specifications | Implement, train and validate M, B1–B5 and ablations; B0 controller integration |
| Primary analysis | E6/E7 tables; paired bootstrap; exact paired test; binomial event-rate intervals; utility screening | Pilot power analysis, preregistered missing-data handling, scientific interpretation |
| Secondary analysis | Repeated-scenario estimator, Holm adjustment and calibration functions | Experiment-specific E8–E12 drivers, causal/oracle analysis and complete result figures |
| Plotting | Measured primary human-hazard plots | Delay, mechanism, OOD and calibration plots linked to their registered estimands |
| Release | Integrity audit, incomplete/audited archive labeling and manifests | Actual data collection, E14 scientific/manuscript review and anonymization |

## Engineering order inside the research sequence

At E0 resolve resources and write an implementation backlog. At E1 implement the simulator adapter, observation boundary, snapshots and raw event logging. At E2 integrate the nominal controller, holding controller and all four primitives. At E3 generate the pilot and finalize simulator-specific labeling. At E4 implement training, calibration and seeded checkpoint export. At E5 finish every baseline/ablation and experiment-specific analysis driver, validate them on development fixtures and freeze them before confirmatory testing.

No starter function returns plausible-looking robot results when assets are missing. The unconfigured adapter raises an error. Tests use temporary synthetic fixtures solely to establish software behavior; a field labeled measured_simulation is not by itself proof that an experiment happened. Raw traces, asset/model versions, execution logs and independent review are necessary.

The complete file paths for the original research plan and 25-paper review are in sources/. They are retained unchanged as background; the operational clarifications here govern the additional seed/physics reference budgets and executable gate behavior.
