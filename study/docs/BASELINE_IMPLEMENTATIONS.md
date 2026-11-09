# Baselines and implementation completion checklist

| ID | Required behavior | Before E5 |
| --- | --- | --- |
| B0 | Nominal controller plus common geometric filter; diagnostic continuation | Record whether an alarm is informational or a mandatory stop. Exclude B0 from compliant-response claims. |
| B1 | Competent grip-preserving, balance-aware controlled stop | Demonstrate stopping/recovery competence; no power-off strawman. |
| B2 | PRISM-derived stoppability monitor plus its fixed fallback | Implement documented labels and state-based monitoring; preserve a fair fallback; name all adaptations. |
| B3 | Safe-Stop-derived dual-estimator gate | Use adequate verified implementation detail; if unavailable, mark unavailable with reason rather than relabeling a substitute. |
| B4 | FORTRESS-derived semantic fallback with caching and feasible planning | Include intended reasoning/caching behavior, human/dynamic context and actual runtime cost; do not force a deliberately slow implementation. |
| B5 | Equally informed predictive heuristic | Same candidate library, sensing, delay budget and feasibility filter; tune on development only. |
| M | Joint action-conditioned human/object/robot consequence predictor | Three training seeds, separate calibration, delayed action-onset state, feasibility, uncertainty and explicit degraded mode. |

For each method produce a card with: source URL and revision; implemented scope; deviations from the source; inputs; output/action space; training/tuning data and budget; model/checkpoint hash; validation cases; primitive/controller differences; cache/precomputation behavior; compute hardware and runtime; limitations. Do not claim unqualified reproduction when adapting a paper.

If B3 cannot be reproduced, change included_methods and record the missing baseline before final lock. A reduced method claim still requires B1, B4, B5 and at least one credible learned stopping baseline B2 or B3. Record a reduction in comparison breadth; do not silently use seven-method counts after removing an arm.

This package intentionally does not assign fabricated baseline outputs. All scientific implementations must pass E2/E5 and produce measured traces.
