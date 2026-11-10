# GEE versus mixed-model results — executed synthetic comparison

**Updated 2026-11-10.** This report discusses a reproducible computation against the **same synthetic simulator** as the University Pathways case (seed 20261108). It is not an empirical university study. The associated executable code is [multilevel_comparison.py](multilevel_comparison.py), the regression checks are [tests/test_multilevel_comparison.py](tests/test_multilevel_comparison.py), and the saved numeric output is [results/multilevel_comparison.json](results/multilevel_comparison.json). [GitHub Actions run 42754180525](https://github.com/cjofbar-sys/research-portfolio/actions/runs/42754180525) **completed successfully** for the new comparison (head SHA `82c90c812f2a3171fb4ff1d7320042ba24e51ce6`). Its jobs passed the original/multilevel tests, independent model re-execution against the pinned JSON and numeric sanity checks, as verified from GitHub's job-step status.

## Scientific question and sample

What residual between-student heterogeneity in semester credits remains after conditioning on modeled simulated covariates? Does a student-level random-intercept linear mixed model lead to materially different substantive conclusions than the existing marginal Gaussian GEE?

**Same simulated panel:** 1,170 entrants, 1,136 students with at least one recorded semester, 9,674 student-semester observations, six campuses; 27 students contribute only one recorded semester. Semester credits end at first graduation/withdrawal; follow-up is selected by the event processes.

Both use `credits_earned ~ semester + first_gen + preparation + support + C(campus)`. The GEE uses a student exchangeable working correlation and robust sandwich uncertainty; the linear mixed model uses a random intercept by student and REML estimation. Campus indicators remain **fixed**, not random.

## Computed comparison

| Quantity | Gaussian GEE | Student random-intercept LMM |
| --- | ---: | ---: |
| Semester coefficient (95% CI) | −0.0183 [−0.0490, 0.0124] | −0.0202 [−0.0513, 0.0110] |
| Simulated first-generation indicator (95% CI) | −0.9137 [−1.0968, −0.7305] | −0.9135 [−1.0932, −0.7338] |
| Preparation coefficient (95% CI) | 2.4722 [2.3687, 2.5757] | 2.4705 [2.3718, 2.5692] |
| Simulated support coefficient (95% CI) | 1.8437 [1.7191, 1.9684] | 1.8422 [1.7158, 1.9686] |
| Correlation / residual ICC | Working correlation 0.006304 | Residual ICC 0.001527 |
| LMM variance components | Not estimated | Student variance 0.02972; residual variance 19.42642 |
| Estimation | GEE converged | REML with L-BFGS optimizer reported convergence; singular covariance warning |

**Important:** GEE's working exchangeable correlation and LMM's conditional residual ICC are different statistical quantities, not interchangeable indicators. Under Gaussian identity-link models, fixed-effect estimates can be similar despite different estimands. The LMM emitted the optimizer warning **"Random effects covariance is singular"**, even though it reported convergence. This is a substantive diagnostic flag: confidence in the estimated small random-effect variance is limited and boundary/sensitivity checks are warranted. Near-zero clustering should not be overstated as precise identification of zero between-person variation.

The numerical ICC corresponds to approximately **0.15%** of residual variance under the fitted model, after observed covariates, in the **simulated, event-selected panel**. It does not imply that only 0.15% of real university experiences differ between students; it is not a psychological measure.

## Why the result makes sense

The generator introduces preparation, support, a simulated first-generation indicator, and campus-level systematic effects, plus independent semester credit shocks. **It does not impose an additional residual student random intercept** after conditioning on its specified covariates. The limited residual clustering is therefore expected from the simulation architecture. Fitting a more complex model does not make that model automatically better or more truthful.

No random-slope model was included in this validated release. A further specification must justify within-person observation counts, fixed/temporal functional form, convergence and variance identifiability. Six campuses do not support strong inference on a randomly sampled campus distribution.

## Critical interpretation

- Neither model corrects selective observation caused by graduation and withdrawal. The observed repeated-credits panel is not a random sample of all student-term opportunities.
- Small differences in coefficients do not verify an absent causal effect, nor do they validate random-effects assumptions.
- Statements about simulated group differences reflect deliberately programmed relationships.
- Model comparison is about statistical structure and assumptions. Do not use AIC to compare the GEE estimating-equation fit directly with the mixed-model likelihood.
- P-values are not the whole argument; compare effect size, interval width, assumptions and substantive research question.

## Bridge to cultural-semiotic inquiry — research directions, not findings

A student-level residual variance component cannot tell us how difficulty, recognition, learning strategies, emotions or anticipated professional life become meaningful to an individual. The quantitative panel instead motivates possible follow-up data collection:

| Quantitative question | Psychological process to investigate | Additional evidence required |
| --- | --- | --- |
| When does credit progression slow? | Reinterpretation of setbacks and self-regulation | Longitudinal interviews, contemporaneous study practices, relevant course records |
| How are interruptions distributed? | Work, care, institutionally constrained participation | Support access, documented work/care constraints, institutional sequences |
| How do similar progressions diverge? | Shifts in meaning, perceived possibilities and future orientation | Idiographic records across multiple episodes, alternative interpretations and negative cases |
| What is unobserved after withdrawal/graduation? | Transitions into other forms of participation | Ethically governed follow-up, no automatic interpretation of missing credits as disengagement |

**Scientific stopping point:** publish the executed, caution-qualified comparison as a **methods case**, not as evidence about actual student psychology. Any real mixed-method conclusion requires an independently designed empirical study.
