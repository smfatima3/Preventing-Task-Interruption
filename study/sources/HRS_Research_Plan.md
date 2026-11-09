# Humanoid task interruption research plan

Literature review, four-page paper design, and evaluation protocol

Prepared 3 November 2026. Literature window: publications from 2020 through 30 September 2026, with preprints explicitly labeled. No experiments have been run for this report and no results are asserted.

## Recommended research question

Can an action-conditioned runtime supervisor that models nearby people, carried-object dynamics, and observation-to-action delay reduce secondary physical hazards during humanoid task interruption, compared with strong stopping and semantic-fallback baselines, while preserving useful task completion?

Working paper title: Preventing Secondary Harm During Humanoid Task Interruption.

The specific contribution is a tested supervisor and a reproducible evaluation of the consequences of switching from an autonomous task to recovery. Generic safe stopping, semantic fallbacks, perceptual recovery, and latency-aware planning are established research areas. The novelty must lie in joint human-object-humanoid transition prediction and the evidence that it improves outcomes beyond capable, equally informed alternatives.

The recommended initial domain is one humanoid performing three ordinary tasks with rigid objects. Use a frozen nominal task policy and a small set of validated recovery primitives. Keep task-level language reasoning if it is already available, but do not require a large model to issue each fast control command. This supports a research profile in runtime assurance for autonomous physical agents.

An 8/10 is a quality target, not an acceptance prediction or an official workshop score. The evidence gates later in this report define what would make a strong submission credible. A proposal with no executed physics evaluation would not meet that target under this rubric.

## Workshop constraints and positioning

The following requirements come from the workshop description supplied in this conversation. This report does not assume that a later deadline extension exists.

| Item | Requirement and consequence |
| --- | --- |
| Submission | Extended abstract, PDF, up to four pages excluding references. This longer planning report is not the submission manuscript. |
| Review | Double-blind. Remove names, affiliations, acknowledgments, identifying links, and identifying PDF metadata from the submitted manuscript. |
| Template | No specific template required. A readable two-column format is a reasonable choice; do not compress fonts to fit. |
| Presentation | In person only, poster with possible spotlight. Registration is through Humanoids. |
| Deadline | November 5 2026, 23:59 AoE; equivalent to November 6 2026, 16:59 in Pakistan. |
| Main fit | Runtime monitoring and fallbacks; whole-body contact; balance and impact mitigation; HRI safety; simulation and safety evaluation. |
| Standards relevance | Supply explicit claims, assumptions, hazards, mitigations, and evidence. Do not claim certification, compliance, or a Safety Integrity Level from classification accuracy. |

The motivating deployment question is whether an interruption mechanism protects the surrounding scene as well as the robot. A useful case study produces a concrete safety argument: within specified tasks, perception errors, contact models, and latency bounds, a supervisor reduces measured hazards relative to declared baselines. The scope must remain visible even if the results are favorable.

## Why the literature leads to this question

First, safe control and reach-avoid research show that the desired terminal state must be reached without violating safety on the way [1-6]. That distinction matters when a humanoid ends upright but releases a payload or swings an arm into a person during recovery.

Second, language-grounded skills, closed-loop feedback, and uncertainty-aware planning enable autonomous decisions but address different success conditions [7-9]. A valid instruction, plausible recovery plan, or calibrated choice of skill does not by itself establish the physical safety of the executed transition.

Third, fallback-safe MPC, AESOP, and FORTRESS already connect runtime monitoring, fallback feasibility, semantics, and delay [10,11,25]. Therefore, the proposed paper cannot claim that adding semantic reasoning or accounting for inference latency is new. The important extension is the joint transition of the humanoid and manipulated object near a moving person, including grasp/contact changes and stale information.

Fourth, recent humanoid methods address residual safety filtering, versatile whole-body control, dynamics mismatch, geometric constraints, stopping feasibility, and fall recovery [12-20]. PRISM already studies object transport and unsafe stop collisions. Safe-Stop already selects a stopping or damping response. VIGOR already uses scene context for recovery. A method that merely monitors robot balance or adds a second fallback would have weak novelty.

Finally, SafeAgentBench, SafeVLA, and the two ASIMOV studies make physical-agent safety and safety-utility trade-offs explicit [21-24]. Their contributions motivate independent hazard labels and separate task-success reporting. They do not remove the need for a targeted, executed humanoid interruption test.

The resulting gap is a synthesis from these 25 papers, not a proven absence across all literature: how much additional protection is obtained by explicitly predicting human contact and object consequences throughout a delayed humanoid interruption, relative to strong existing recovery and planning approaches? A matched-state experiment can answer that question even if the proposed supervisor does not outperform a well-designed heuristic.

## Literature inclusion and verification policy

This is a focused narrative review, not an exhaustive systematic review. Sources are author manuscripts, official proceedings, author project pages, and publisher records. Each entry distinguishes the contribution reported by the source from our implication for this project. Publication year is used for peer-reviewed work; first public release and version dates are noted where relevant. Taylor et al. [1] is a 2020 proceedings paper whose preprint appeared in 2019.

Exactly 25 distinct papers are included. Two surveys provide foundations; HOVER and ASAP provide implementation and validity context rather than direct safety-supervisor baselines. The two ASIMOV entries are different papers. VIGOR uses its March 2026 version, excluding its October revision. Safe-Stop is supported by primary metadata and its author project description; its full text could not be retrieved, so detailed method claims are intentionally limited.

VAPS and SIREN, mentioned or encountered in the earlier discussion, first appeared in October 2026 and are outside this requested review window. They are not counted among the 25 or used to claim a September state of the art. Before an actual November submission, run a separate current-literature novelty check; a historical cutoff does not justify ignoring a known overlapping contribution in the submitted paper.

## Annotated review of 25 papers

Window: 2020 through September 2026. Publication years and preprint versions are distinguished. Implications are the analysis in this report, not claims made by the cited authors.

## Safe control and recovery foundations

### [1] Learning for Safety-Critical Control with Control Barrier Functions

Andrew Taylor, Andrew Singletary, Yisong Yue, Aaron Ames. 2020. Learning for Dynamics and Control.

Contribution: Learns the effect of model uncertainty on control barrier conditions and iteratively updates a safety controller. Simulation and Segway experiments demonstrate the value of adapting the model used for safety enforcement.

Implication for this RQ: A barrier protects the safety conditions encoded by its designer. This motivates specifying human contact and object-related hazards explicitly, while retaining a common low-level shield across comparisons.

Role: Control foundation.

The cited proceedings publication is June 2020; its earlier preprint was released in 2019. Inclusion follows publication year.

Primary source: [Learning for Safety-Critical Control with Control Barrier Functions](https://proceedings.mlr.press/v120/taylor20a.html).

### [2] Recovery RL: Safe Reinforcement Learning with Learned Recovery Zones

Brijen Thananjeyan, Ashwin Balakrishna, Suraj Nair, Michael Luo, Krishnan Srinivasan, Minho Hwang, Joseph E. Gonzalez, Julian Ibarz, Chelsea Finn, Ken Goldberg. 2021. IEEE Robotics and Automation Letters; ICRA presentation.

Contribution: Separates a reward-seeking task policy from a learned recovery policy. Offline constraint-violation data support a safety critic and recovery behavior; evaluation includes contact-rich manipulation and a physical robot.

Implication for this RQ: Separating task and recovery policies is established. The proposed study must show better selection and execution of recovery under coupled human, object, and humanoid dynamics.

Role: Recovery architecture.

First preprint October 2020; revised May 2021.

Primary source: [Recovery RL: Safe Reinforcement Learning with Learned Recovery Zones](https://arxiv.org/abs/2010.15920v2).

### [3] Safety and Liveness Guarantees through Reach-Avoid Reinforcement Learning

Kai-Chieh Hsu, Vicenc Rubies-Royo, Claire Tomlin, Jaime F. Fisac. 2021. Robotics Science and Systems.

Contribution: Develops a discounted reach-avoid Bellman formulation and uses approximate learned solutions within a supervisory framework. It connects reaching a desired condition to avoiding failure along the path.

Implication for this RQ: A safe final posture is insufficient when the transition collides with a person or drops an object. Reach-avoid structure motivates evaluating the complete intervention trajectory.

Role: Problem formulation.

Primary source: [Safety and Liveness Guarantees through Reach-Avoid Reinforcement Learning](https://roboticsproceedings.org/rss17/p077.html).

### [4] Safe Learning in Robotics: From Learning-Based Control to Safe Reinforcement Learning

Lukas Brunke, Melissa Greeff, Adam W. Hall, Zhaocong Yuan, Siqi Zhou, Jacopo Panerati, Angela P. Schoellig. 2022. Annual Review of Control Robotics and Autonomous Systems.

Contribution: Surveys control and reinforcement-learning approaches to safe decision making under uncertainty, separating performance improvement, robustness, and certification. It emphasizes realistic benchmarks and shared terminology.

Implication for this RQ: Provides the vocabulary for stating what is assumed, monitored, and empirically demonstrated. A finite simulation study supports a bounded safety claim, not universal safe deployment.

Role: Survey and framing.

Author preprint available at https://arxiv.org/abs/2108.06266v2.

Primary source: [Safe Learning in Robotics: From Learning-Based Control to Safe Reinforcement Learning](https://www.annualreviews.org/content/journals/10.1146/annurev-control-042920-020211).

### [5] Safe-Control-Gym: A Unified Benchmark Suite for Safe Learning-Based Control and Reinforcement Learning in Robotics

Zhaocong Yuan, Adam W. Hall, Siqi Zhou, Lukas Brunke, Melissa Greeff, Jacopo Panerati, Angela P. Schoellig. 2022. IEEE Robotics and Automation Letters.

Contribution: Introduces common environments, dynamics interfaces, constraints, and repeatable disturbances for comparing control and reinforcement-learning approaches. Its systems include cart-pole and quadrotors.

Implication for this RQ: The transferable lesson is experimental discipline: share dynamics, observations, disturbances, and constraints. The benchmark itself is not a humanoid interruption benchmark.

Role: Evaluation design.

Primary source: [Safe-Control-Gym: A Unified Benchmark Suite for Safe Learning-Based Control and Reinforcement Learning in Robotics](https://arxiv.org/abs/2109.06325v4).

### [6] Safe Control With Learned Certificates: A Survey of Neural Lyapunov, Barrier, and Contraction Methods for Robotics and Control

Charles Dawson, Sicun Gao, Chuchu Fan. 2023. IEEE Transactions on Robotics.

Contribution: Reviews learned certificates for safety and stability, including verification and their use during policy learning. It explains how a learned model can be connected to mathematical conditions.

Implication for this RQ: A calibrated risk predictor is not automatically a barrier certificate. The workshop paper should claim empirical risk reduction unless its dynamics, uncertainty, and verification assumptions justify a theorem.

Role: Assurance boundary.

Open author version: https://arxiv.org/abs/2202.11762v2.

Primary source: [Safe Control With Learned Certificates: A Survey of Neural Lyapunov, Barrier, and Contraction Methods for Robotics and Control](https://doi.org/10.1109/TRO.2022.3232542).

## Grounded autonomous planning

### [7] Do As I Can, Not As I Say: Grounding Language in Robotic Affordances

Michael Ahn et al.. 2022. arXiv preprint.

Contribution: Combines language-based task relevance with the affordances of pretrained robot skills. Real mobile-manipulation experiments demonstrate how language instructions can be grounded in executable actions.

Implication for this RQ: Skill feasibility is essential but does not by itself establish safety during interruption. Use a grounded skill interface and keep the language planner outside the fast safety loop.

Role: Autonomous-agent grounding.

Primary source: [Do As I Can, Not As I Say: Grounding Language in Robotic Affordances](https://arxiv.org/abs/2204.01691v2).

### [8] Inner Monologue: Embodied Reasoning through Planning with Language Models

Wenlong Huang et al.. 2022. CoRL 2022; cited author preprint.

Contribution: Feeds success signals, scene descriptions, and human feedback back into a language-model planner. Closed-loop feedback improves instruction completion in simulated and real manipulation settings.

Implication for this RQ: Task repair through feedback motivates resumption after interruption. Completion improvements alone cannot establish reduced human contact or safe switching dynamics.

Role: Closed-loop autonomy.

Primary source: [Inner Monologue: Embodied Reasoning through Planning with Language Models](https://arxiv.org/abs/2207.05608v1).

### [9] Robots That Ask For Help: Uncertainty Alignment for Large Language Model Planners

Allen Z. Ren, Anushri Dixit, Alexandra Bodrova, Sumeet Singh, Stephen Tu, Noah Brown, Peng Xu, Leila Takayama, Fei Xia, Jake Varley, Zhenjia Xu, Dorsa Sadigh, Andy Zeng, Anirudha Majumdar. 2023. Conference on Robot Learning.

Contribution: KnowNo calibrates language-planner uncertainty with conformal prediction and asks for help when ambiguity requires it. Its guarantees concern task completion under specified conditions and human assistance.

Implication for this RQ: Uncertainty should influence intervention, but asking or waiting also consumes physical time. Planning-confidence guarantees cannot be transferred directly to collision-free humanoid recovery.

Role: Calibration and abstention.

Primary source: [Robots That Ask For Help: Uncertainty Alignment for Large Language Model Planners](https://proceedings.mlr.press/v229/ren23a.html).

## Runtime monitoring and predictive fallbacks

### [10] Closing the Loop on Runtime Monitors with Fallback-Safe MPC

Rohan Sinha, Edward Schmerling, Marco Pavone. 2023. IEEE Conference on Decision and Control.

Contribution: Maintains a feasible fallback while using learned perception, and calibrates monitoring to detect perception degradation. The framework connects monitor assumptions to controller tolerance and conditional safety.

Implication for this RQ: Preserving a fallback before failure is established. The proposed extension concerns coupled humanoid, object, and human outcomes during switching, including what happens when no modeled response is feasible.

Role: Closest runtime foundation.

Primary source: [Closing the Loop on Runtime Monitors with Fallback-Safe MPC](https://arxiv.org/abs/2309.08603).

### [11] Real-Time Anomaly Detection and Reactive Planning with Large Language Models

Rohan Sinha, Amine Elhafsi, Christopher Agia, Matthew Foutter, Edward Schmerling, Marco Pavone. 2024. Robotics Science and Systems.

Contribution: AESOP combines a fast anomaly classifier and slower semantic reasoning with a predictive controller that maintains fallback options while reasoning takes place. It explicitly accounts for language-model latency.

Implication for this RQ: Latency-aware fallback selection is already prior art. The new contribution must demonstrate why contact transitions and carried-object consequences require more than latency handling alone.

Role: Closest latency-aware baseline.

Official author project: https://sites.google.com/view/aesop-LLM.

Primary source: [Real-Time Anomaly Detection and Reactive Planning with Large Language Models](https://arxiv.org/abs/2407.08735).

## Humanoid control stopping and recovery

### [12] ResSafe: Learning Safety Filtering with Residual Reinforcement Learning for Humanoids

Gechen Qu, Tong Zhang, Bike Zhang, Yen-Jen Wang, Koushil Sreenath, Claire Tomlin, Jason Jangho Choi. 2026. arXiv preprint September 14.

Contribution: Learns residual corrections to a nominal humanoid policy, separating tracking performance from safety optimization. The author project evaluates balance tasks and payload conditions.

Implication for this RQ: Payload-aware robustness and performance-safety trade-offs are already studied. Reduced falls do not establish safe outcomes for bystanders or released objects; measure these separately.

Role: Humanoid filtering.

Abstract and author project checked; no claim that this review independently verified all experiments. Project: https://sciautonomy.github.io/ResSafe_Web/.

Primary source: [ResSafe: Learning Safety Filtering with Residual Reinforcement Learning for Humanoids](https://arxiv.org/abs/2609.15988v1).

### [13] HOVER: Versatile Neural Whole-Body Controller for Humanoid Robots

Tairan He, Wenli Xiao, Toru Lin, Zhengyi Luo, Zhenjia Xu, Zhenyu Jiang, Jan Kautz, Changliu Liu, Guanya Shi, Xiaolong Wang, Linxi Fan, Yuke Zhu. 2025. IEEE International Conference on Robotics and Automation.

Contribution: Distills multiple whole-body command modes into a common humanoid controller, supporting transitions among locomotion and manipulation interfaces.

Implication for this RQ: Provides a possible reusable control foundation, not a plug-and-play safety supervisor or proof of grasp competence. Verify robot, checkpoint, command-mode, and manipulation compatibility before committing.

Role: Implementation background.

First preprint 2024; conference publication 2025. Code/checkpoint suitability for this study remains an implementation gate.

Primary source: [HOVER: Versatile Neural Whole-Body Controller for Humanoid Robots](https://hover-versatile-humanoid.github.io/).

### [14] ASAP: Aligning Simulation and Real-World Physics for Learning Agile Humanoid Whole-Body Skills

Tairan He et al.. 2025. Robotics Science and Systems.

Contribution: Uses real-world rollout data to learn residual action corrections and align simulation with robot dynamics. It evaluates transfer between simulators and to a Unitree G1.

Implication for this RQ: Shows why simulated impact or recovery improvements require sensitivity checks and cannot automatically establish hardware safety. A second physics configuration is useful, but is not equivalent to hardware validation.

Role: Dynamics validity.

Primary source: [ASAP: Aligning Simulation and Real-World Physics for Learning Agile Humanoid Whole-Body Skills](https://arxiv.org/abs/2502.01143v3).

### [15] SPARK: Safe Protective and Assistive Robot Kit

Yifan Sun, Rui Chen, Kai S. Yun, Yikuan Fang, Sebin Jung, Feihan Li, Bowei Li, Weiye Zhao, Changliu Liu. 2025. IFAC Symposium on Robotics.

Contribution: Provides modular safety constraints, control algorithms, simulation comparisons, and hardware interfaces, including Unitree G1 examples.

Implication for this RQ: Offers relevant infrastructure and baseline implementations. A secondary-harm interruption suite would be an extension with new contact and object-state validation, not an existing SPARK benchmark result.

Role: Benchmark and implementation foundation.

Cited revision January 14 2026, within cutoff. Repository: https://github.com/intelligent-control-lab/spark.

Primary source: [SPARK: Safe Protective and Assistive Robot Kit](https://arxiv.org/abs/2502.03132v3).

### [16] Dexterous Safe Control for Humanoids in Cluttered Environments via Projected Safe Set Algorithm

Rui Chen, Yifan Sun, Changliu Liu. 2025. arXiv preprint February 5.

Contribution: p-SSA handles many limb-level external and self-collision constraints by relaxing conflicts to retain feasible control. It is evaluated in simulation and on a Unitree G1.

Implication for this RQ: A strong geometric-control comparator is needed. Constraint relaxation can admit violations; neither feasibility nor collision avoidance of modeled links proves safe handling of an unstable payload.

Role: Low-level comparator.

Primary source: [Dexterous Safe Control for Humanoids in Cluttered Environments via Projected Safe Set Algorithm](https://arxiv.org/abs/2502.02858v1).

### [17] Learning Safe-Stoppability Monitors for Humanoid Robots

Yifan Sun, Yiyuan Pan, Shangtao Li, Caiwu Ding, Tao Cui, Lingyun Wang, Changliu Liu. 2026. arXiv preprint March 24.

Contribution: PRISM learns whether a fixed fallback reaches a minimum-risk condition without failure, using targeted sampling. Its G1 study includes grasping, transporting, and releasing an object; stopping collisions are explicitly considered.

Implication for this RQ: Do not claim that prior work ignores unsafe stops or manipulation. The proposed distinction is selecting among alternatives with explicit object and bystander consequences, and testing complete closed-loop interventions.

Role: Closest humanoid prior work.

Full-text Sections VI-A, VI-B, and VII checked. Cited as the March preprint rather than relying on later conference reporting.

Primary source: [Learning Safe-Stoppability Monitors for Humanoid Robots](https://arxiv.org/abs/2603.22703v1).

### [18] Humanoid Safe Stop via Learned Stoppability Value

Junfeng Long, Pieter Abbeel, Koushil Sreenath, Roberto Horowitz, Guanya Shi, C. Karen Liu. 2026. arXiv preprint September 2.

Contribution: Pairs a learned stop policy with stop-probability and reach-avoidance estimates, switching to a damping fallback when the stopping gate fails. The design transfers across upstream behaviors.

Implication for this RQ: A learned stop-versus-fallback gate is already available by September. Compare against this family where implementation permits, and avoid presenting a binary stopping selector as a new contribution.

Role: Closest recent stop comparator.

ArXiv metadata and indexed author project verified; full manuscript could not be retrieved. Claims are restricted to the abstract and project description: https://junfeng-long.github.io/safestop/.

Primary source: [Humanoid Safe Stop via Learned Stoppability Value](https://arxiv.org/abs/2609.02358).

### [19] Unified Humanoid Fall-Safety Policy from a Few Demonstrations

Zhengjie Xu, Ye Li, Kwan-Yee Lin, Stella X. Yu. 2026. IEEE International Conference on Robotics and Automation.

Contribution: Combines demonstrations, reinforcement learning, and a memory of reactions to address fall prevention, impact mitigation, and recovery in one humanoid policy, with G1 experiments.

Implication for this RQ: The full fall-and-recovery process is an existing safety target. Extend evaluation to collateral effects on people and objects instead of treating lower robot impact alone as the contribution.

Role: Impact and recovery metrics.

First public version November 2025; ICRA 2026 publication verified on author page.

Primary source: [Unified Humanoid Fall-Safety Policy from a Few Demonstrations](https://arxiv.org/abs/2511.07407v1).

### [20] VIGOR: Visual Goal-In-Context Inference for Unified Humanoid Fall Safety

Osher Azulay, Zhengjie Xu, Andrew Scheffer, Stella X. Yu. 2026. arXiv preprint version 2 March 3.

Contribution: Distills a teacher into a student using egocentric depth and proprioception to coordinate fall mitigation and recovery on varied terrain. Context-dependent perceptual recovery is already central to the method.

Implication for this RQ: Do not claim the first visual or context-aware humanoid recovery method. Focus on interruption of productive tasks, human/object consequence prediction, and causal comparison of response choices.

Role: Perceptual recovery and transfer.

The October 15 version changed the title to Unified Perceptive Fall Safety for Humanoids. That post-cutoff revision and its expanded results are excluded.

Primary source: [VIGOR: Visual Goal-In-Context Inference for Unified Humanoid Fall Safety](https://arxiv.org/abs/2602.16511v2).

## Embodied safety evaluation

### [21] SafeAgentBench: A Benchmark for Safe Task Planning of Embodied LLM Agents

Sheng Yin, Xianghe Pang, Yuanzhuo Ding, Menglan Chen, Yutong Bi, Yichen Xiong, Wenhao Huang, Zhen Xiang, Jing Shao, Siheng Chen. 2024. arXiv preprint; revision October 2025.

Contribution: Evaluates embodied agents on safe and hazardous instructions in interactive simulation, with execution-level and semantic assessments across 750 tasks.

Implication for this RQ: Its hazard taxonomy informs scenario design. Task rejection and symbolic execution metrics do not directly quantify impact impulses or balance during humanoid recovery; a physics-grounded endpoint is needed.

Role: Embodied safety benchmark.

Initial release December 2024. Revision used is October 2025, not October 2026.

Primary source: [SafeAgentBench: A Benchmark for Safe Task Planning of Embodied LLM Agents](https://arxiv.org/abs/2412.13178v5).

### [22] SafeVLA: Towards Safety Alignment of Vision-Language-Action Model via Constrained Learning

Borong Zhang, Yuhao Zhang, Jiaming Ji, Yingshan Lei, Juntao Dai, Yuanpei Chen, Yaodong Yang. 2025. Advances in Neural Information Processing Systems 38.

Contribution: Uses constrained learning and targeted risk elicitation for VLA alignment, assessing safety-performance trade-offs, extreme failures, and distribution shifts in mobile manipulation.

Implication for this RQ: Safety and utility must be reported jointly, including tail failures. This is a relevant training-based comparison class, but retraining a general VLA is unnecessary for a focused runtime-interruption workshop study.

Role: Evaluation and alignment.

Primary source: [SafeVLA: Towards Safety Alignment of Vision-Language-Action Model via Constrained Learning](https://proceedings.neurips.cc/paper_files/paper/2025/hash/e185c7be603426028c32ae1003a59d78-Abstract-Conference.html).

### [23] Generating Robot Constitutions & Benchmarks for Semantic Safety

Pierre Sermanet, Anirudha Majumdar, Alex Irpan, Dmitry Kalashnikov, Vikas Sindhwani. 2025. Conference on Robot Learning.

Contribution: Introduces ASIMOV semantic-safety data grounded in visual situations and injury reports, together with generated robot constitutions for behavioral guidance.

Implication for this RQ: Useful for deriving interpretable hazards and semantic constraints. Agreement with a constitution does not establish that a recovery motion is dynamically feasible or physically harmless.

Role: Hazard vocabulary.

Primary source: [Generating Robot Constitutions & Benchmarks for Semantic Safety](https://proceedings.mlr.press/v305/sermanet25a.html).

### [24] Can AI Perceive Physical Danger and Intervene?

Abhishek Jindal, Dmitry Kalashnikov, R. Alex Hofer, Oscar Chang, Divya Garikapati, Anirudha Majumdar, Pierre Sermanet, Vikas Sindhwani. 2025. arXiv preprint; ASIMOV version 2 study.

Contribution: Benchmarks perception of physical danger and intervention reasoning using images and videos grounded in injury narratives and operational constraints; it also explores safety-focused post-training.

Implication for this RQ: Recognizing danger is a necessary component. The proposed evaluation must execute the selected intervention and measure its physical outcome rather than relying on the model to judge its own safety.

Role: Physical risk understanding.

Distinct paper from [23], not a duplicate version of the same manuscript. Cited revision November 2025 is within cutoff.

Primary source: [Can AI Perceive Physical Danger and Intervene?](https://arxiv.org/abs/2509.21651v2).

## Semantic fallback planning

### [25] Real-Time Out-of-Distribution Failure Prevention via Multi-Modal Reasoning

Milan Ganai, Rohan Sinha, Christopher Agia, Daniel Morton, Luigi Di Lillo, Marco Pavone. 2025. Conference on Robot Learning.

Contribution: FORTRESS precomputes semantic fallback goals and safety representations, then performs dynamics-aware fallback planning. It evaluates semantic recognition and drone fallback execution and includes an example of replanning around moving concepts.

Implication for this RQ: Semantic fallback planning, caching, latency mitigation, and some dynamic replanning are already addressed. The distinct test is coupled contact-mode transitions, load retention, and bystander outcomes during humanoid interruption.

Role: Closest semantic fallback comparator.

Full-text Sections 4, 5, 7 and Appendix E checked. Avoid describing FORTRESS as purely static or as ignoring humans.

Primary source: [Real-Time Out-of-Distribution Failure Prevention via Multi-Modal Reasoning](https://arxiv.org/abs/2505.10547v2).


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

## References

[1] Andrew Taylor, Andrew Singletary, Yisong Yue, Aaron Ames (2020). [Learning for Safety-Critical Control with Control Barrier Functions](https://proceedings.mlr.press/v120/taylor20a.html). Learning for Dynamics and Control.

[2] Brijen Thananjeyan, Ashwin Balakrishna, Suraj Nair, Michael Luo, Krishnan Srinivasan, Minho Hwang, Joseph E. Gonzalez, Julian Ibarz, Chelsea Finn, Ken Goldberg (2021). [Recovery RL: Safe Reinforcement Learning with Learned Recovery Zones](https://arxiv.org/abs/2010.15920v2). IEEE Robotics and Automation Letters; ICRA presentation.

[3] Kai-Chieh Hsu, Vicenc Rubies-Royo, Claire Tomlin, Jaime F. Fisac (2021). [Safety and Liveness Guarantees through Reach-Avoid Reinforcement Learning](https://roboticsproceedings.org/rss17/p077.html). Robotics Science and Systems.

[4] Lukas Brunke, Melissa Greeff, Adam W. Hall, Zhaocong Yuan, Siqi Zhou, Jacopo Panerati, Angela P. Schoellig (2022). [Safe Learning in Robotics: From Learning-Based Control to Safe Reinforcement Learning](https://www.annualreviews.org/content/journals/10.1146/annurev-control-042920-020211). Annual Review of Control Robotics and Autonomous Systems.

[5] Zhaocong Yuan, Adam W. Hall, Siqi Zhou, Lukas Brunke, Melissa Greeff, Jacopo Panerati, Angela P. Schoellig (2022). [Safe-Control-Gym: A Unified Benchmark Suite for Safe Learning-Based Control and Reinforcement Learning in Robotics](https://arxiv.org/abs/2109.06325v4). IEEE Robotics and Automation Letters.

[6] Charles Dawson, Sicun Gao, Chuchu Fan (2023). [Safe Control With Learned Certificates: A Survey of Neural Lyapunov, Barrier, and Contraction Methods for Robotics and Control](https://doi.org/10.1109/TRO.2022.3232542). IEEE Transactions on Robotics.

[7] Michael Ahn et al. (2022). [Do As I Can, Not As I Say: Grounding Language in Robotic Affordances](https://arxiv.org/abs/2204.01691v2). arXiv preprint.

[8] Wenlong Huang et al. (2022). [Inner Monologue: Embodied Reasoning through Planning with Language Models](https://arxiv.org/abs/2207.05608v1). CoRL 2022; cited author preprint.

[9] Allen Z. Ren, Anushri Dixit, Alexandra Bodrova, Sumeet Singh, Stephen Tu, Noah Brown, Peng Xu, Leila Takayama, Fei Xia, Jake Varley, Zhenjia Xu, Dorsa Sadigh, Andy Zeng, Anirudha Majumdar (2023). [Robots That Ask For Help: Uncertainty Alignment for Large Language Model Planners](https://proceedings.mlr.press/v229/ren23a.html). Conference on Robot Learning.

[10] Rohan Sinha, Edward Schmerling, Marco Pavone (2023). [Closing the Loop on Runtime Monitors with Fallback-Safe MPC](https://arxiv.org/abs/2309.08603). IEEE Conference on Decision and Control.

[11] Rohan Sinha, Amine Elhafsi, Christopher Agia, Matthew Foutter, Edward Schmerling, Marco Pavone (2024). [Real-Time Anomaly Detection and Reactive Planning with Large Language Models](https://arxiv.org/abs/2407.08735). Robotics Science and Systems.

[12] Gechen Qu, Tong Zhang, Bike Zhang, Yen-Jen Wang, Koushil Sreenath, Claire Tomlin, Jason Jangho Choi (2026). [ResSafe: Learning Safety Filtering with Residual Reinforcement Learning for Humanoids](https://arxiv.org/abs/2609.15988v1). arXiv preprint September 14.

[13] Tairan He, Wenli Xiao, Toru Lin, Zhengyi Luo, Zhenjia Xu, Zhenyu Jiang, Jan Kautz, Changliu Liu, Guanya Shi, Xiaolong Wang, Linxi Fan, Yuke Zhu (2025). [HOVER: Versatile Neural Whole-Body Controller for Humanoid Robots](https://hover-versatile-humanoid.github.io/). IEEE International Conference on Robotics and Automation.

[14] Tairan He et al. (2025). [ASAP: Aligning Simulation and Real-World Physics for Learning Agile Humanoid Whole-Body Skills](https://arxiv.org/abs/2502.01143v3). Robotics Science and Systems.

[15] Yifan Sun, Rui Chen, Kai S. Yun, Yikuan Fang, Sebin Jung, Feihan Li, Bowei Li, Weiye Zhao, Changliu Liu (2025). [SPARK: Safe Protective and Assistive Robot Kit](https://arxiv.org/abs/2502.03132v3). IFAC Symposium on Robotics.

[16] Rui Chen, Yifan Sun, Changliu Liu (2025). [Dexterous Safe Control for Humanoids in Cluttered Environments via Projected Safe Set Algorithm](https://arxiv.org/abs/2502.02858v1). arXiv preprint February 5.

[17] Yifan Sun, Yiyuan Pan, Shangtao Li, Caiwu Ding, Tao Cui, Lingyun Wang, Changliu Liu (2026). [Learning Safe-Stoppability Monitors for Humanoid Robots](https://arxiv.org/abs/2603.22703v1). arXiv preprint March 24.

[18] Junfeng Long, Pieter Abbeel, Koushil Sreenath, Roberto Horowitz, Guanya Shi, C. Karen Liu (2026). [Humanoid Safe Stop via Learned Stoppability Value](https://arxiv.org/abs/2609.02358). arXiv preprint September 2.

[19] Zhengjie Xu, Ye Li, Kwan-Yee Lin, Stella X. Yu (2026). [Unified Humanoid Fall-Safety Policy from a Few Demonstrations](https://arxiv.org/abs/2511.07407v1). IEEE International Conference on Robotics and Automation.

[20] Osher Azulay, Zhengjie Xu, Andrew Scheffer, Stella X. Yu (2026). [VIGOR: Visual Goal-In-Context Inference for Unified Humanoid Fall Safety](https://arxiv.org/abs/2602.16511v2). arXiv preprint version 2 March 3.

[21] Sheng Yin, Xianghe Pang, Yuanzhuo Ding, Menglan Chen, Yutong Bi, Yichen Xiong, Wenhao Huang, Zhen Xiang, Jing Shao, Siheng Chen (2024). [SafeAgentBench: A Benchmark for Safe Task Planning of Embodied LLM Agents](https://arxiv.org/abs/2412.13178v5). arXiv preprint; revision October 2025.

[22] Borong Zhang, Yuhao Zhang, Jiaming Ji, Yingshan Lei, Juntao Dai, Yuanpei Chen, Yaodong Yang (2025). [SafeVLA: Towards Safety Alignment of Vision-Language-Action Model via Constrained Learning](https://proceedings.neurips.cc/paper_files/paper/2025/hash/e185c7be603426028c32ae1003a59d78-Abstract-Conference.html). Advances in Neural Information Processing Systems 38.

[23] Pierre Sermanet, Anirudha Majumdar, Alex Irpan, Dmitry Kalashnikov, Vikas Sindhwani (2025). [Generating Robot Constitutions & Benchmarks for Semantic Safety](https://proceedings.mlr.press/v305/sermanet25a.html). Conference on Robot Learning.

[24] Abhishek Jindal, Dmitry Kalashnikov, R. Alex Hofer, Oscar Chang, Divya Garikapati, Anirudha Majumdar, Pierre Sermanet, Vikas Sindhwani (2025). [Can AI Perceive Physical Danger and Intervene?](https://arxiv.org/abs/2509.21651v2). arXiv preprint; ASIMOV version 2 study.

[25] Milan Ganai, Rohan Sinha, Christopher Agia, Daniel Morton, Luigi Di Lillo, Marco Pavone (2025). [Real-Time Out-of-Distribution Failure Prevention via Multi-Modal Reasoning](https://arxiv.org/abs/2505.10547v2). Conference on Robot Learning.

