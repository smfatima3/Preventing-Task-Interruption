# Literature review of 25 papers

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

