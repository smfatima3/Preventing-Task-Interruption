# Frozen analysis plan

## Estimands and order

The independent unit is a base scenario. H1 is E6 mean paired human-hazard difference M minus the development-selected B*. H2 first considers E7 human-hazard difference, then E7 task-success noninferiority. Use the sequence E6 hazard → E7 hazard → E7 success; if an earlier confirmatory claim is unsupported, later estimates remain descriptive. All baseline rows and secondary outcomes still appear.

The starter analysis implements the equal-weight empirical benchmark mixture, task-stratified paired percentile bootstrap (10,000 resamples, fixed seed) for risk differences, exact two-sided McNemar checks, per-method exact Clopper–Pearson event-rate intervals, and one-rollout-per-scenario primary pairing. Task counts follow the locked sample registry. It reports raw and paired counts and does not multiply sample size by frames, conditions or seeds.

This is a bounded initial implementation, not an automatic solution for every statistical design. It deliberately refuses duplicate primary cells, missing pairs, noncomplete primary outcomes, synthetic inputs, changed locks and insufficient exposure. If a prespecified failure-handling policy needs missing-outcome bounds or repeated rollout aggregation, implement and validate that analysis before freezing E5; do not edit it after seeing tests. A full attempt ledger remains mandatory even when the primary selected-outcome file is complete.

For repeated latency, physics and seed conditions, use the scenario-cluster bootstrap utility in hrs/analysis.py. Every bootstrap draw samples base IDs within task and brings all repeated rows for each selected scenario together; set the aggregation and target weights before test. The supplied generic function produces paired mean differences for registered comparable keys, not a universal mixed-effects analysis.

## Rare events and uncertainty

Bootstrap intervals collapse when all paired differences are identical, especially zero-event sets. Mark those results degenerate; do not claim certainty. Use exact event-rate bounds and the exact paired test. The generated flags are screening aids, not an automatic publication decision. For a primary superiority statement require the specified direction, interval support and the prespecified inferential check, plus validity and harm-component review.

The utility margin is 0.05 unless prospectively justified otherwise. The criterion is lower 95% CI for success(M)-success(B*) > -0.05. Merely obtaining p > .05 in a difference test is not noninferiority. The initial 600 pairs is not guaranteed to resolve this margin; calculate N from disjoint pilot discordance and desired power, then freeze it before E6/E7.

Report absolute differences in percentage points and relative risk only when the baseline rate is nonzero. Severity summaries include zeros and conditional-on-contact subsets, clearly distinguished. Force/impulse distributions and CVaR90 are secondary; tail estimates require adequate counts and uncertainty.

## Secondary analyses

Register the E8 three-ablation family, E9 planned delay comparisons and E10 shift comparisons before tests. Apply Holm to the declared p-value family using the included holm_adjust utility. Do not construct the family after excluding unfavorable results. Calibration bins must be prespecified and show denominators; unsafe approval and unsafe-state miss are different conditional probabilities.

## Analysis limits and review

The starter scripts generate primary tables, exact checks, descriptive summaries, generic repeated-scenario intervals, calibration summaries and measured-data plots. Scientist-authored scripts are still needed for experiment-specific causal/oracle analyses, detailed event extraction, secondary family selection, matched inference across special missing-data designs and the final paper. These must be versioned and frozen before confirmatory testing. A successful script does not establish physics validity, baseline fidelity or a supported scientific claim.
