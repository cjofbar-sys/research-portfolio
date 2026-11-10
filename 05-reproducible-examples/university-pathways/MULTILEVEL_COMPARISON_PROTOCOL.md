# Next controlled extension: GEE versus hierarchical models

**Status:** Design and model-selection protocol; models below are NOT estimated in the currently verified snapshot. Last reviewed: 2026-11-10.

## Why compare models?
The verified case reports Gaussian GEE for semester credits among observed student-semesters. This is a marginal population-average regression with an exchangeable working correlation at student level. It is not itself a multilevel random-effects model. The scientific purpose of this extension is to determine which kinds of temporal and clustering heterogeneity can be identified from the simulation, not simply to add a more sophisticated-sounding technique.

## Analysis units and data-generating process
- Student: stable background and simulated characteristics.
- Semester: repeated credits earned, observed only until the first withdrawal or graduation.
- Campus: six simulated campuses, nested within three cohorts, each containing 65 students per cell (1,170 entrants).
- The generator includes campus-level support shifts and student-specific observed variables but **does not explicitly introduce a residual student random-intercept term** after conditioning on those observed variables.
- Some students withdraw before the first recorded credits; later records after graduation or withdrawal are structurally missing. Thus the observed semester panel is selected by the event process.

The mixed model could estimate near-zero residual variance even when students' unadjusted trajectories differ. That is a substantive diagnostic result, not a software failure to conceal or a reason to invent heterogeneity.

## Primary scientific question
Conditional on simulated preparation, support, first-generation marker, campus and term, how much additional residual variation in semester credits appears to lie between students, versus within them? How does a cluster-specific linear mixed model differ from the population-average GEE already reported?

## Planned analysis sequence
1. Reproduce existing GEE and full data-quality checks on the *same seed and observed panel*. Lock the analysis sample and feature definitions.
2. Fit an ordinary Gaussian marginal linear regression with student-clustered robust standard errors as a descriptive benchmark, clearly distinguishing its working assumptions.
3. Fit a student-level random-intercept linear mixed model for `credits_earned` with fixed `semester + first_gen + preparation + support + C(campus)`, grouped by `student_id`. Report estimation method, convergence, estimated random-intercept variance, residual variance, intraclass correlation (ICC) when defined, coefficients, CIs and fit warnings.
4. Compare fixed-effect estimates and uncertainty with the GEE, **not** using AIC to make direct claims across fundamentally different likelihood and estimating-equation targets. Explain marginal versus conditional estimands.
5. Assess a student random-slope specification for semester **only when** random-intercept diagnostics, number of observed terms per student and convergence support identification. Do not assert it is better merely because it has more parameters.
6. Explore campus heterogeneity descriptively and through fixed effects. A campus random-effects sensitivity analysis may be considered, but **only six campuses** make higher-level variance components and standard errors unstable. Avoid presenting six-campus estimates as robust population variance generalization.
7. Evaluate residual and group-level diagnostics, leverage, changes to temporal functional form, and the stability of inference across plausible estimators.
8. Address informative follow-up explicitly: graduation and withdrawal end the accumulation process. An LMM fitted only to observed semesters does not remove this selection. Use pattern-mixture or inverse-probability-of-observation sensitivity only after defining assumptions and suitability.

## Proposed output schema once code has RUN
Save `results/multilevel_comparison.json` separately from current immutable `results/summary.json`. Required fields: data source, seed, code commit, sample sizes, model formulas, convergence, variance components, interval estimates, diagnostic flags, and explicit failure states. Never fabricate values or fall back to assumed numbers if a fit is unstable. Introduce website visualization only after independent execution and tests are linked.

## What this can and cannot show
Can demonstrate: correct choice of repeated-measures estimands, hierarchical variance decomposition where identifiable, model criticism, convergence diagnostics, uncertainty and comparison with GEE on a common dataset.

Cannot demonstrate: a new institutional empirical finding; psychological motivations behind progression; stable campus-effect generalization from six clusters; causal effects of institutional supports; absence of unmeasured student differences simply because fitted residual ICC approaches zero.

## From statistical evidence to cultural-semiotic research questions
A between-student variance term is not a measure of meaning-making, and a semester coefficient is not the psychology of time. Quantitative patterns can motivate **future mixed-method questions** about the meaning of academic setbacks, revised learning strategies, anticipations of professional participation, academic emotions and the temporal accessibility of assistance.

To examine these questions, a real empirical design would need independently sourced longitudinal interviews/conversations, appropriately governed institutional interactions, documented variation in work and caregiving conditions, and alternative-case analysis. No such qualitative data is part of this synthetic dataset.

## Gate for publication
Require a reproducible executed script, passing test suite, verified numerical export and documented critical interpretation before displaying numerical multilevel results in /research/methods. Until then label this as **planned methodological comparison**.
