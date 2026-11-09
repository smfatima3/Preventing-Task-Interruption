# Experiments and metrics

## Proposed method and scope

Treat the supervisor as an independently evaluated decision layer over existing skills. Inputs are recent vision or depth, proprioception, estimated human motion, estimated object mass and grasp state where available, timestamps, and the candidate response. Simulator truth may label training and evaluation outcomes but is forbidden as a runtime input in the main condition.

Use four candidate recovery modes after validating their execution: grip-preserving deceleration; grasp-preserving retreat; controlled placement on an available support; and active stabilization or bracing without advancing the task. The last mode must be a real stable controller, not motor shutdown. A mode unavailable in a scene is marked unavailable for every method. Candidate generation and primitive quality must be shared between the proposed method and matched-choice comparators.

The proposed predictor is conditioned on response choice and the state expected when that response will start. It estimates human-contact risk, object loss/impact risk, and balance failure over the transition. Use a modest model initially; the scientific question does not require training a new foundation model. Estimate risk using held-out calibration and evaluate it on executed rollouts. Do not label an uncertainty score as a pointwise guarantee.

Before selecting a response, screen actuator, grasp, support, and balance feasibility. Among feasible candidates, prioritize predicted severe human hazards, then object hazards and robot failure, with task disruption used to choose between comparably safe responses. Freeze the ordering and thresholds before test. Report each component separately so a weighted sum cannot hide a new human hazard behind lower robot damage.

Propagate state uncertainty across observation age, inference time, communication delay, and actuation delay. During computation, a common validated holding controller must remain active. Do not freeze simulator time while a model reasons. Log the state at sensing, decision completion, and action onset. Re-evaluate when a response becomes stale, using hysteresis or a minimum dwell rule to prevent oscillatory switching.

If no candidate meets the declared risk/feasibility conditions, enter a declared degraded mode and record the case as unresolved or least-risk mitigation. Never silently classify an infeasible case as safe. Human assistance is requested only after a physically maintainable state is reached, or explicitly recorded as unavailable.

### Three hypotheses

- H1, consequence modeling: on matched interruption states, the proposed supervisor reduces the probability of unintended human contact versus the strongest development-selected comparator.
- H2, practical utility: in full episodes, the supervisor reduces human hazards while keeping task success within a prespecified noninferiority margin. Safe task completion is reported alongside the two components.
- H3, mechanism and robustness: removing object information, human information, or delay propagation degrades the corresponding outcome under the matched stress condition. These are secondary analyses, not three new headline claims.

### What is and is not novel

The candidate novelty is the combination of an action-conditioned transition model for human/object consequences and a matched-state test of intervention effects. Safe stopping [17,18], learned recovery [2,19,20], predictive fallback feasibility [10], latency handling [11], and semantic fallback planning [25] are foundations. Simply attaching these components without demonstrating an additional mechanism is an integration contribution, which must be described as such.

No new theorem is required for this four-page empirical workshop paper. A theorem about a simplified model must not be presented as a guarantee for the complete learned simulator-to-robot stack. A mathematically explicit problem definition and an honest claim-evidence table are more valuable than an unsupported guarantee.

## Scenarios and experimental controls

| Family | Nominal task and interruption | Competing consequences |
| --- | --- | --- |
| T1 Carry and place | Carry a rigid box; a person enters the route at a scheduled, seeded time. | Deceleration changes load stability; retreat may encounter someone behind; placement needs a clear support. |
| T2 Shelf retrieval | Retrieve an object; a person enters the swept arm region during reach or withdrawal. | Retraction can disturb shelf objects; stopping can leave an unstable load; placement may be unreachable. |
| T3 Confined transport | Move with a load through a narrow passage; the forward route becomes blocked. | Whole-body retreat, grip preservation, balance, and person clearance can conflict. |

Begin with one robot model, rigid-body objects, and a bounded operating domain. Do not begin with hot liquids, soft-body injury models, or arbitrary household tasks. Human avatars represent geometry and motion; they do not establish biomechanical injury predictions. Use physical contact and force/impulse measurements as proxies.

Use one physics stack compatible with a verified pretrained whole-body controller. SPARK is an infrastructure candidate [15]; inspect available backends and manipulation support before choosing. Isaac Sim or MuJoCo can be used if the grasp/contact model passes validation. No simulator or repository was installed or tested as part of this planning report.

Create a frozen generator with three prespecified scenario strata: benign interruption; potentially avoidable hazard; and severe or possibly unrecoverable disturbance. A useful starting mixture is 40%, 50%, and 10%, reported separately and as a deliberately designed benchmark mixture. It is not an estimate of real-world hazard prevalence. Do not discard difficult cases after seeing method results.

Split by layout, object configuration, human trajectory, and base scenario ID. Splitting neighboring video frames is inadequate. Keep development, predictor training, calibration, matched-state testing, and full-episode testing disjoint. Hold out human motion patterns and payload combinations for transfer tests.

For matched-state comparisons, restore robot state, object velocities, grasp/contact state, controller memory, and simulator random state. Confirm numerical replay tolerance. Continue the same exogenous human trajectory. Branch every response from the same pre-intervention state. If a human model reacts differently to each robot action, define and log that shared response model; the trajectories can then diverge legitimately.

Use a fixed 10-second post-trigger observation window for the matched-state study, including at least two seconds after reaching a nominal stable state. Record outcomes over the full 120-second episode separately. These are initial protocol choices to validate in the pilot and freeze; if a task needs longer, change them before confirmatory testing. Stopping must not terminate measurement while objects or people are still moving.

## Baselines and fairness

| ID | Comparator | Purpose and implementation rule |
| --- | --- | --- |
| B0 | Nominal task policy plus common geometric safety filter | Measures what existing low-level protection already achieves. It continues under an informational hazard alarm; an actual mandatory stop experiment excludes it as a valid responder. |
| B1 | Competent fixed controlled-stop policy | Grip-preserving, balance-aware deceleration. Never use power-off as the principal comparator. |
| B2 | PRISM-derived monitor with its fixed fallback [17] | Tests the gain beyond predicting stoppability. Adaptations must retain outcome labeling and state-based monitoring; document changes. |
| B3 | Safe-Stop-derived dual-estimator gate [18] | Tests a recent learned stop/fallback approach. Require adequate implementation detail and validation; if unavailable, report the missing comparison rather than rename a substitute. |
| B4 | FORTRESS-derived semantic fallback planning [25] | Includes cached reasoning and feasible planning, not a deliberately slow on-demand LLM strawman. Share scene inputs and candidate primitives where compatible. |
| B5 | Strong predictive heuristic | Same human/object observations, candidate library, latency budget, and feasible-action screening; hand-designed rollout/risk rules tuned on development data. Tests whether a learned supervisor is necessary. |
| M | Proposed action-conditioned supervisor | Same nominal controller and sensing stack; adds joint consequence prediction and explicit delay propagation. |

B2-B4 are adaptations to a new humanoid setting unless their original code/configuration is actually reproduced. Use labels such as PRISM-derived, not the unqualified paper name. Reproduction failures are not experimental evidence that the published method is inferior. Report unavailable methods as unavailable.

Use the same low-level geometric filter in every applicable arm, with the same parameters. When a native baseline has a distinct controller, report both its native behavior and a matched-primitive adapter if feasible; do not conflate them. Match observation access, primitive quality, tuning budget, and test disturbances. Permit each method its intended planning mechanism and report its actual compute use.

For a full target study, compare all six baselines and M. If resources require a smaller early-work study, retain B1, at least one credible learned stopping baseline, B4, and B5. Disclose the narrower comparison and lower the breadth of the claim. A nominal-policy-only comparison cannot support a strong method contribution.

## Evaluation metrics and their interpretation

The primary outcome is unintended human contact in the fixed post-trigger window, including robot-human and released-object-human contact. Count intended contacts only if they violate a declared task-specific allowance. These three initial tasks do not require intentional human contact. A hazard is not automatically an injury.

| Family | Definition and reporting | Priority |
| --- | --- | --- |
| Human hazard probability | p_H = fraction of independent test scenarios with any unintended robot-human or object-human contact above a numerically validated contact tolerance. Report both subtypes and their union. | Primary |
| Contact severity | Maximum contact impulse in N s, integrated impulse, peak force in N, contacted body region, and relevant impact velocity. Report zeros, p95, and maximum; calibrate solver sensitivity. | Key secondary |
| Object harm proxies | Unintended drop rate, object-person impact rate, and maximum kinetic energy immediately before impact in J. Define intended placement separately. Report mass and drop height. | Key secondary |
| Robot safety | Fall rate, non-foot ground impacts, self-collisions, joint-limit and actuator-limit violations, and time to a stable supported state. | Key secondary |
| Task utility | Task success within fixed episode budget; safe success = task success AND no registered hazard; resumption rate and time after an interruption. Keep aborted tasks in denominator. | Co-primary claim condition |
| Intervention burden | Interventions per episode, repeated switches, benign-episode interruption rate, and fraction of avoidable task aborts. | Secondary |
| Delay and throughput | End-to-end observation-to-action latency p50/p95/p99, deadline misses, sensor age at decision, simulation real-time factor, and supervisor overhead. | Secondary |
| Risk prediction | Brier score; reliability plot; unsafe-approval rate P(hazard given approved); unsafe-state miss rate P(approved given hazardous). Include denominators and calibration sample size. | Diagnostic |
| Generalization | All outcome metrics by task, layout split, payload, human motion, and latency condition, with worst-stratum outcomes. | Secondary |
| Tail robustness | Worst-case observed impulse and CVaR at 90% for a declared physical severity proxy; display tail sample count and uncertainty. | Exploratory if few tail events |

Define contact tolerances using sensor/solver validation, not by choosing thresholds that favor M. Report threshold sensitivity around the locked tolerance. Peak force is particularly solver-dependent; impulse and event occurrence are useful complementary measurements. Never present a universal injury threshold without a validated biomechanical model and appropriate scope.

Prespecify severity ordering and show the raw components. Do not collapse falls, object damage, and human contact into an arbitrary scalar headline. A composite can be exploratory if its units, weights, and sensitivity analysis are explicit.

### Attributing secondary hazards

For one restored scenario, compare the factual rollout under response a with paired rollouts under response b and, when useful in simulation, continuation. The net intervention effect is the mean paired difference in a declared outcome. A hazard after a stop is not enough to say that stopping caused it.

An introduced-hazard fraction can be reported as P(H under a = 1 and H under continuation = 0), together with the prevented-hazard fraction P(H under a = 0 and H under continuation = 1). Their difference equals the paired risk difference for binary H. Also compare against the best feasible response found by a privileged offline oracle. That oracle is a diagnostic upper bound, never a deployable baseline.

Keep human-contact subtype labels so a prevented body collision cannot conceal a new object-human collision. The best-feasible-response diagnostic depends on the finite primitive library and simulator fidelity; it does not prove that an unavoidable case has no physically possible solution.

### Results needed for the main claim

- A clear failure mechanism occurs across multiple independently generated scenes, not only a selected video.
- M improves the primary human-hazard outcome against the preselected strongest comparator, with an interval supporting reduction and a practically meaningful effect.
- Full-episode utility passes the prespecified noninferiority criterion if the paper says without materially reducing task success. If it does not, state the observed safety-utility trade-off.
- No unexplained transfer of risk from robot falls to people or objects. Publish component outcomes even when the total improves.
- The component ablations support the proposed mechanism, and performance does not collapse under the declared deployment delay range.
- Held-out layouts or payloads retain useful behavior, and all baselines receive the same sensing and primitive advantages.

Suggested development goals are at least a 25% relative reduction in human-hazard probability and no more than a five percentage-point task-success loss. These are design preferences, not literature-derived acceptance thresholds, expected results, or workshop rules. Absolute effects and confidence intervals determine interpretation. A relative percentage is misleading when the baseline hazard rate is tiny.

## Statistical analysis and sample planning

The independent unit is a base scenario, not a control timestep, video frame, intervention branch, or repeated model seed. Evaluate paired scenarios across methods. Repeated rollouts, latency settings, and trained-seed variants stay clustered within their base scenario.

Choose the primary comparator on development data, freeze it before opening test results, and retain the complete baseline table. The primary confirmatory comparison is M versus that comparator. Test the matched-state hazard endpoint first; assess full-episode safety and task-success noninferiority in a declared hierarchy. Other pairwise tests and component ablations are secondary, with Holm adjustment within their declared families. Do not select the easiest significant comparator afterward.

Report absolute risk differences in percentage points, relative risk when the denominator is nonzero, and 95% confidence intervals. For one rollout per fixed-policy pair, exact McNemar testing is a suitable check for binary hazard differences. For multiple policy seeds or repeated disturbances, use a paired scenario-cluster bootstrap, stratified by task, with at least 10,000 resamples and a fixed analysis seed. Keep all conditions for a sampled scenario together. With very rare events or degenerate bootstrap samples, also report exact event-rate bounds and refrain from overconfident superiority claims.

Task-success noninferiority: define D = success(M) - success(B*) and the margin delta = 0.05 before testing. Claim noninferiority only if the lower endpoint of a two-sided 95% paired interval is above -0.05, equivalent to a one-sided 97.5% lower bound. A nonsignificant superiority test does not establish noninferiority. Justify the five-point margin as the maximum acceptable loss for this benchmark; change it only before the confirmatory plan is locked.

For severity, report paired differences and bootstrap intervals for event-inclusive quantities. Also provide conditional-on-contact summaries, explicitly noting that conditioning on contact compares different selected subsets. CVaR90 is exploratory when only a few tail observations exist. Do not promote a p99 estimate from a tiny sample as a reliable tail guarantee.

Use at least three independent training seeds for learned supervisors if training is part of the contribution. Report each seed and the mean across seeds; model seeds do not multiply the number of independent scenes. For the confirmatory primary deployment artifact, select a seed/checkpoint using only development rules and freeze it. Additional seeds assess algorithm stability on a prespecified audit set; full multi-seed confirmation is an extension if compute permits.

### Why a pilot is necessary

For a paired binary outcome, an approximate standard error of the mean difference is sqrt((q - D^2)/N), where q is the probability that the two methods disagree and N is the number of independent pairs. Use this only for planning; simulate the final paired test using pilot-estimated discordance and task strata.

For illustration, if true utility difference is zero, margin is 0.05, q = 0.20, and one-sided alpha is 0.025, an 80% power normal approximation gives N about 628. If q = 0.40, it gives about 1,256. These are hypothetical planning calculations, not observed results. Thus 600 pairs is a starting budget, not guaranteed power. For zero hazards in 600 independent trials, the approximate 95% upper rate bound is 3/600 = 0.5%; zero observed failures is not proof of zero risk.

After a disjoint pilot, preregister a fixed N based on an agreed effect and discordance, or use a formally specified sequential design. Do not repeatedly add test runs until a confidence interval passes. If the feasible budget cannot resolve the desired utility margin, report the interval and weaken the utility claim.

## Ordered experiment plan

The sequence below is the recommended execution order. Counts are proposed starting budgets, not completed experiments or a guarantee of adequate power. Stop at a failed prerequisite instead of launching a large uninformative sweep. Readiness, data generation, confirmatory testing, and robustness are distinct phases.

| ID | Experiment and starting budget | Required output and decision |
| --- | --- | --- |
| E0 | Lock hazards, task success, scope, comparator adaptations, split IDs, thresholds, horizons, and metrics. No robot runs. | Protocol and claim-evidence table; verify four-page and blind-review requirements. |
| E1 | Validate physics and replay on 12 designed states per task, including grasp loss, contact, placement, and stable stopping; 36 states total. | Contact/impulse sanity checks, mass/friction checks, replay tolerances, and no privileged runtime inputs. Failures block later studies. |
| E2 | Test nominal task and every applicable recovery primitive on 30 clean episodes per task; 90 nominal episodes plus primitive checks. | Recommended readiness target: at least 80% nominal success per task and reproducible recovery behavior. This is an internal engineering gate. |
| E3 | Disjoint diagnostic pilot: 20 states per task, 60 total; branch four recovery modes and continuation when feasible, up to 300 short rollouts. | Establish whether nontrivial response-dependent human/object hazards exist. Include benign and difficult states, not only failures. |
| E4 | Build predictor data: start with 100 training states and 40 calibration states per task; four modes and three physics perturbations per state, up to 5,040 short rollouts. | Separate train/calibration splits; verified outcome labels. Fit three training seeds. Expand only for a stated learning-curve or coverage reason. |
| E5 | Baseline validation and development tuning: 30 new states per task, 90 paired states across seven configurations. | Up to 630 primary-artifact rollouts. Freeze B*, hyperparameters, seeds, thresholds, and statistically justified test N. |
| E6 | Confirmatory matched-state intervention study: initial budget 100 states per task, 300 paired states across seven configurations. | Up to 2,100 short rollouts; matched human-hazard risk difference, component severity, introduced/prevented hazards, and oracle diagnostic. |
| E7 | Full closed-loop episodes: initial budget 200 per task, 600 paired scenarios across seven configurations. | Up to 4,200 episodes; task success, human hazards, safe success, burden, and utility noninferiority. Recalculate N before test from pilot power. |
| E8 | Three mechanism ablations on 40 held-out states per task, 120 total; compare M with no object state, no human prediction, and no delay propagation. | 480 short rollouts for four variants; matched feature/information removal, fixed control stack, adjusted secondary comparisons. |
| E9 | Delay stress: 20 new states per task, 60 total; 0, 100, 300, and 600 ms added end-to-end delay, comparing M, B*, and the no-delay ablation. | 720 short rollouts. Also report measured latency; injected delay is additional, not a substitute for actual compute cost. |
| E10 | OOD robustness: 60 new states per task, 180 total, across held-out layouts, payload/grasp conditions, and human-motion patterns; M and B*. | 360 short rollouts; separate each shift and include a declared combined-shift stress test. Retain physical plausibility. |
| E11 | Seed stability and calibration audit: 120 independent states, two additional learned-model seeds, plus locked primary-seed predictions. | At least 240 extra M rollouts; score calibration on data not used for calibrating. Add corresponding learned-baseline seeds where training variation affects conclusions. |
| E12 | Simulation sensitivity: 20 boundary cases per task, 60 total; two additional contact/timestep parameterizations, M and B*. | 240 short rollouts. Include a random-case subset as well as boundary cases; failures limit the physical interpretation. |
| E13 | Optional hardware or independent second-simulator validation after all prior gates. | A bounded feasibility/transfer study, clearly separated from aggregate simulation evidence. Never induce hazardous human contact to obtain a result. |
| E14 | Final result audit and manuscript assembly. | Reproduce tables from frozen logs, review failures, enforce anonymity and page limit, and record unresolved limitations. |

E0-E3 are prerequisites. E4-E5 develop and lock the method. E6-E7 provide the primary evidence. E8-E12 support the mechanism and reliability claims. E13 is a valuable extension, not an implied workshop requirement. E14 is mandatory before making claims. Some analysis can reuse predictions from existing held-out rollouts; do not count reused scenes as additional independent evidence.

The listed E3-E12 primary-artifact budgets total about 14,310 rollouts/episodes, excluding E1-E2 checks, added baseline-seed evaluations, and any power-driven increase. Most are short branched rollouts; only E7 requires complete episodes. This is an evaluation and data-generation budget, not a recommendation to train locomotion from scratch. The budget is deliberately staged so a weak pilot can stop further compute.

Benchmark actual speed after E2. Estimate wall time using observed steps per second, environment parallelism, model-call latency, and failure/restart rates. Do not infer a GPU-hour estimate from nominal episode duration. The near submission date makes an already functioning controller especially important; if it is absent, an honest preliminary failure-analysis paper is more credible than fabricated completeness.

### Core versus optional evidence

For the proposed full empirical claim, require physics validation, capable primitives, a matched-state comparison, a full-episode utility study, the three component ablations, delay stress, one genuinely held-out generalization test, and a reproducibility audit. Hardware and a second robot are valuable but optional for a clearly scoped simulation workshop paper. A second foundation model is optional unless model-agnostic generality is claimed. Multi-agent extensions, liquid simulation, and a new locomotion policy are outside the initial scope.

If E3 finds no meaningful additional hazard beyond an established stopper, revise the RQ or publish that negative result. If B5 matches M, the contribution may be a benchmark or safety analysis rather than a superior learned method. If utility noninferiority fails, present a safety-utility curve and state the loss. None of these outcomes should be hidden to chase a rating.

## Four-page manuscript structure

| Component | Page budget including its figures | Required content |
| --- | --- | --- |
| Title and abstract | 0.25 | Concrete problem, intervention method, evaluated scope, and actual measured result with uncertainty. Write result sentences last. |
| 1 Introduction and focused related work | 0.80 | One physical example; why interruption can create collateral hazards; exact distinction from [10,11,17,18,25]; two or three contributions. |
| 2 Problem and evaluation target | 0.45 | State/observations, candidate responses, delay, hazard definitions, operating domain, and matched-state estimand. |
| 3 Supervisor | 0.65 | Action-conditioned consequence prediction, feasibility screen, delay propagation, degraded behavior, and shared controller. |
| 4 Experimental setup | 0.45 | Three task families, held-out splits, baselines, independent sample units, and primary statistical plan. |
| 5 Results | 0.95 | Primary hazard and utility table; mechanism ablations; delay/transfer evidence; representative failure. |
| 6 Discussion limitations and conclusion | 0.45 | What the evidence supports, sim-to-real limits, unresolved harms, and a compact safety argument. |
| Total main text | 4.00 | References follow outside the four-page main-text limit. |

Use the complete 25-paper review to prepare the argument, but do not insert 25 isolated mini-summaries into four pages. Group citations by the specific proposition they support. Do not assume supplementary pages or appendices will be reviewed; the central claim must be assessable from the four-page PDF.

### Figures and tables to reserve space for

- Figure 1: one matched initial state with two recovery outcomes, alongside a compact supervisor schematic. Label it an illustration until generated from real experiment logs.
- Table 1: seven method rows; human hazard count/N, object-impact rate, fall rate, task success, safe success, and latency. Include primary paired difference and interval in the caption or adjacent text.
- Figure 2: hazard versus actual end-to-end delay with uncertainty; a small safety-utility panel if space permits.
- Table 2: M and the three ablations on the matched audit set, with the metrics corresponding to each removed component.

The full report should retain per-task outcomes, severity distributions, calibration diagnostics, implementation details, and all failed runs. The four-page paper should show the essential evidence and link to anonymous artifacts only if the submission system permits it. External artifacts must not be required to understand the result.

### Results writing rules

Do not invent numerical examples inside a manuscript results section. Use an empty table shell labeled not yet measured during drafting. Once experiments are complete, report counts and paired intervals, then state whether each hypothesis is supported, unresolved, or contradicted. A narrow but reproducible negative finding is a legitimate contribution; it is not evidence for an unobserved method improvement.

## A practical rubric for the eight out of ten target

This is an internal quality rubric, not the workshop's published review form.

| Criterion | Maximum | Evidence expected |
| --- | --- | --- |
| Distinct contribution | 2.0 | Clear separation from PRISM, Safe-Stop, AESOP, FORTRESS, and perceptual fall recovery; new mechanism or a valuable systematic failure study. |
| Technical validity | 2.0 | Executable primitives, correct contact/latency modeling, no state leakage, fair adaptations, and explicit infeasibility handling. |
| Empirical evidence | 2.5 | Paired primary comparison, meaningful effect, utility evidence, mechanism ablations, and held-out robustness. |
| Reproducibility | 1.0 | Versioned code/configurations, seeds, scenario generator, raw outcome logs, analysis scripts, and a successful independent rerun of summaries. |
| Workshop relevance and clarity | 1.5 | Four-page coherent story with deployment hazards, monitoring, recovery, and a claim-evidence argument. |
| Limitations and responsible interpretation | 1.0 | Harm proxies, scope, uncertainty, simulator dependence, and failures stated accurately. |
| Total | 10.0 | Aim for at least 8 with no critical validity failure. No score is assigned before results exist. |

Critical failures override the total: fabricated results; comparing against only an incompetent stop; test-set tuning; counting frames as independent trials; privileged simulator state in only M; unsupported injury/certification claims; or hiding a severe harm category that worsens.

## Claim evidence and release checklist

| Intended claim | Required evidence | Limit on interpretation |
| --- | --- | --- |
| Interruption can introduce secondary hazards | Matched states with alternative response rollouts and repeated mechanisms across scenes. | Causal within the declared simulator and intervention model. |
| M reduces hazards | Locked primary comparison, counts, paired confidence interval, and component outcomes. | Scoped to sampled tasks and operating conditions. |
| Task usefulness is preserved | Powered or transparently uncertain paired noninferiority analysis. | A null significance test is insufficient. |
| Delay modeling matters | Controlled injected-delay study plus measured end-to-end runtime. | Does not establish performance beyond the tested delay range. |
| The mechanism generalizes | Held-out layouts, payloads, and human motions. | Does not establish universal humanoid or foundation-model generality. |
| The work informs assurance | Hazard list, declared assumptions, mitigations, logs, and failed cases. | Does not establish certification or an industrial safety integrity rating. |

Store scenario and run IDs, task, split, method/seed/checkpoint, observation timestamps, prompt/model revision if used, response choice, feasibility flags, risk estimates, all contact events, object velocities, falls, task status, runtime, simulator settings, and exclusion reason. Keep a complete run manifest including crashes; a crashed or aborted run is not a safe success. Replace a run only under a prespecified infrastructure-failure policy and retain the original record.

Release task definitions and analysis so a reader can regenerate the main table from raw logs. Include failures and borderline cases in the video set. In the anonymous submission, scrub identifying repository paths, account names, author metadata, and acknowledgments. Before submission, verify that in-person presentation is feasible; this report does not make travel, registration, or submission commitments.

The next research decision is E1-E3 readiness: whether reliable nominal behavior and a repeatable intervention-specific hazard can be demonstrated. That result determines whether the project should proceed as a method paper, a failure-analysis contribution, or a revised question.
