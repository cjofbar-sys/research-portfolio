# Verified execution: simulated university pathways

**Validation date:** 2026-11-08. **Public source:** [Python analysis](analysis.py), [generated results](results/summary.json), [automated tests](tests/test_analysis.py), [GitHub Actions run](https://github.com/cjofbar-sys/research-portfolio/actions/runs/42448072233).

These figures describe **1170 deliberately simulated entrants**, in six fictional institutions and three cohorts (seed 20261108). They do not estimate outcomes or disparities in any real university.

## Descriptive analysis and denominators

| Outcome | Synthetic estimate | Denominator |
| --- | ---: | --- |
| Degree obtained through semester 10 | 55.21% | All 1170 entrants |
| Degree obtained through semester 12 | 69.32% | All 1170 entrants |
| Withdrawn through semester 12 | 28.89% | All 1170 entrants |
| Employed by six months after degree | 52.90% | 811 simulated graduates only |

The 12-semester first-event graduation cumulative incidence is 0.6932 and the competing withdrawal incidence is 0.2889. The remainder is still without either recorded event at the simulated horizon. The competing-events analysis is preferable to treating withdrawal as independent noninformative censoring when interpreting the probability of graduation for a starting cohort.

The timely-graduation proportions by first-generation indicator are 66.23% (406 of 613) versus 43.09% (240 of 557). This contrast is intentionally built into the synthetic data-generating process. It cannot substantiate a substantive claim about real first-generation students.

## Adjusted associations

The simulated first-generation indicator has an adjusted odds ratio of **0.332** for graduation by semester 10, with 95% Wald confidence interval **[0.247, 0.447]**, from a binomial model incorporating preparation, support, campus and cohort. Model-standardized simulated probabilities are 0.6401 versus 0.4591, a difference of -0.1810 in the generated population. These are descriptive/model-based standardized associations under the assumed regression, **not causal effects**. The generator explicitly affects selection into withdrawal and credit accumulation.

The GEE for semester credits includes **9674 observations from 1136 students**, fewer than all entrants because some simulated students withdraw before any semester credit is recorded. Its first-generation coefficient is -0.914 credits (95% CI [-1.097, -0.731]) conditional on modeled variables. It describes an observed-student-semester association and may be influenced by differential observation.

Among the **811 simulated graduates**, an internship indicator is associated with employment within six months at OR 2.160 (95% CI [1.610, 2.897]) conditional on simulated covariates. Restriction to graduates can induce selection bias. This coefficient is not an effect of internships on employment for all entrants.

## Methodological decisions and criticism

1. State explicit cohort, time horizon, event definitions and denominators.
2. Model graduation and withdrawal as mutually exclusive first events; retain those without either event at the horizon.
3. Use repeated-measure correlation structures for semester credits, while examining selection and missingness separately.
4. Interpret odds ratios, model-standardized absolute probability contrasts and their uncertainties without converting an association into an intervention effect.
5. Investigate sensitivity to generator assumptions: withdrawal processes, campus variability, omitted financial constraints, internship selection, and observability of psychological constructs.

P-values in the machine-readable summary are rounded to six decimals; a displayed zero is a rounding artifact, not a literal probability of zero. Prefer effect sizes, interval estimates and the substantive meaning of the model assumptions.

## Psychological and educational questions that remain unanswered

How do institutional support, social recognition, academic responsibilities and anticipated employment influence students' interpretations of possible trajectories? Which events alter perceived possibilities, and what kinds of conversational or longitudinal material would support an account of those processes? How does an aggregate statistical pattern differ from the situated meaning of a transition for a particular student?

The synthetic case is an exercise in constructing and criticizing statistical explanations. Real answers would require permissions, appropriate operationalization, ethical data governance and mixed forms of evidence.

## Reproduction status

Python automated pipeline and four source tests completed successfully in the linked GitHub Actions run. [The verified summary JSON](results/summary.json) is committed for consumption by the personal website. The R script [validation.R](validation.R) is available for independent reproduction on the generated student CSV but has **not** been certified by an executed R validation in this record.
