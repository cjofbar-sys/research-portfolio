# Scientific audit — stability, observed-panel selection and inference

**Date:** 2026-11-10. **Status:** completed reproducible **synthetic** sensitivity audit and critical methodological interpretation. Nothing in this report estimates effects in actual university populations or psychological experience.

**Evidence:** [auditing script](stability_selection_audit.py) · [checks](tests/test_stability_selection_audit.py) · [GitHub Actions run 42757420628](https://github.com/cjofbar-sys/research-portfolio/actions/runs/42757420628) · [downloadable run artifact](https://github.com/cjofbar-sys/research-portfolio/actions/runs/42757420628/artifacts) (`stability_selection_audit.json`, artifact ID 13735199633) · [base analysis](analysis.py) · [GEE vs LMM report](MULTILEVEL_RESULTS_INTERPRETATION.md). GitHub's workflow status and job steps report successful execution. The artifact was retrieved and its numerical summary inspected.

## Scientific problem

Computational reproducibility (re-executing fixed code and seed) is not the same as statistical robustness (stability across simulated samples and assumptions), identifiability, or empirical validity. The previously published GEE and LMM use observations of semester credits collected only until graduation or withdrawal. This audit asks which features of the conclusions persist across seeds **under the same synthetic mechanism** and what observation changes remain invisible in the original coefficients.

## Scope and comparison

Ten generated datasets, using seeds 20261108–20261117, each with 1,170 entrants in six simulated campuses and three cohorts. Per iteration, Gaussian exchangeable student-clustered GEE with `credits_earned ~ semester + first_gen + preparation + support + C(campus)` was fitted (a) to all observed student-semester rows and (b) to observed semesters 1–6. The audit also records the baseline and late-observation composition and first-event withdrawal separately for two synthetic first-generation categories. It **does not** estimate an LMM in every seed, change the data-generating model, reweight selection, or recover student outcomes after an observed first event.

## Verified numerical results

| Quantity | Across ten simulations |
| --- | ---: |
| GEE fitting success, full and early panels | 10/10 for each |
| Full-panel first_gen coefficient, mean | −1.09250 |
| Full-panel first_gen coefficient, min to max | −1.29777 to −0.91369 |
| Full-panel first_gen coefficient, between-seed SD | 0.11697 |
| Early-panel first_gen coefficient, mean | −1.07923 |
| Early minus full first_gen coefficient, min to max | −0.05443 to +0.06909 |
| Full-panel semester coefficient, min to max | −0.02416 to +0.00907 |
| Full-panel semester coefficient, mean | −0.00798 |
| Baseline first_gen share, mean across simulations | 48.42% |
| Share of first_gen in observed semester 9+ **rows**, mean | 49.51% |
| Withdrawal proportion, first_gen=0 (mean) | 20.71% |
| Withdrawal proportion, first_gen=1 (mean) | 41.03% |
| Mean number of entrants with no recorded semester credits | 25.7 |

The GEE `first_gen` coefficient is negative in all ten draws, as expected from the **programmed** data-generating process. Its magnitude changes between draws. The semester coefficient changes sign across draws (six negative, four positive), so it is not appropriate to portray a robust linear semester trend. Ten draws provide a **limited demonstration**, not a comprehensive Monte Carlo evaluation of bias, statistical power or coverage.

## The selection mechanism and its scientific consequences

1. Withdrawal is tested **before** the credit value is generated each semester. Thus some entrants have no credit rows at all and never enter the repeated-credit models, although they remain in the entrant-level graduation model.
2. Graduation occurs when cumulative recorded credits reach a threshold. That threshold depends on the very credits being modeled. Future terms are therefore structurally unobserved after graduation. This can alter the distribution of observed term outcomes even when residual shocks are independent at generation.
3. The simulator's withdrawal hazard explicitly depends on `first_gen`, `support`, `preparation` and semester. In the ten simulated draws, mean withdrawal proportions are about 41.03% versus 20.71% for the first-generation categories by the follow-up horizon. This is an imposed simulation relationship and is a warning about differential observation, **not evidence about real students**.
4. The fraction of `first_gen` among rows observed from semester 9 onward is approximately 49.51% on average, versus 48.42% of entrants. The small aggregate difference does **not** establish that the selection mechanism is ignorable; category balance alone cannot test the conditional selection assumption, and repeated rows weight students by observed time.
5. Comparing the first six observed semesters with all observed semesters mixes at least two changes: observation time and event-based selection. The range [−0.05443, +0.06909] in their contrast is **not an estimate of selection bias**.

### Target of inference and limits of remedies

The current estimand is an **association in observed semester credit records** under a specified marginal model. Extending it to the original entrant cohort through a common fixed follow-up horizon would require an outcome definition even after graduation or withdrawal, which does not exist as a measured semester-credit variable here. Simply imputing zeros, last observations, or an unobserved counterfactual is not justified. Weighted methods require well-defined observation probabilities, positivity, conditioning assumptions and a meaningful target outcome.

For institutional process research, one could instead explicitly model **transitions among enrolled, withdrawn and graduated states**, or define accumulation up to first event. These are different scientific questions and need different estimands. An informative-dropout model, joint model, or inverse-probability weighting is only warranted when its assumptions can be defended.

## LMM stability is a separate unresolved question

The previous single-seed student random-intercept LMM fit reported convergence **and** a singular random-effects covariance warning, with estimated residual ICC around 0.15%. This sensitivity audit recomputes only GEE across ten seeds; **it does not resolve random-effect boundary stability, model identifiability or coverage for LMM variance components**. The simulator includes no residual student random intercept after covariate adjustment. A diagnostic follow-up could compare multiple optimizers, profile variance at the boundary, and repeat fits on selected seeds, always reporting failure and warnings rather than selecting only successful fits.

## Data-quality check proposed before expanding the analysis

The generator records a raw `credits_earned` value but clips `credits_total` to 200 at the graduation threshold. Consequently, recorded earned credits in the final term may exceed the remaining credits credited toward the 200 threshold. The column should be explicitly defined as attempted/earned semester credits **before degree-cap accounting**, or an alternative `credits_credited` field should be created in a new version without silently overwriting the pinned snapshot. This distinction matters for interpretation of average progression.

## Cultural-semiotic psychological research questions — evaluate, do not answer from simulation

**Strong question:** How do changes in academic progression become consequential for students' imagined professional participation, and how do situated interpretations, actual constraints and later actions co-develop? It is not sufficient to describe a slow term as a loss of motivation.

| Statistical signal / limitation | Rival explanations or mechanism questions | Needed empirical material |
| --- | --- | --- |
| Slower recorded credits for some trajectories | Different financial constraints, changes in care/work responsibilities, changing study strategies, altered academic valuation | Time-stamped academic records, work/care constraints, longitudinal conversations and observed strategy revisions |
| Withdrawal before credit observation | Procedural/financial exclusion, institutional incompatibility, changed desired trajectory, unobserved interruption | Enrolment and institutional process records, ethically consented follow-up with non-continuing students |
| Similar administrative trajectories | Distinct interpretations of difficulty, competence and recognition | Repeated situated accounts and interaction records; negative and alternative-case analysis |
| End of credits after graduation | Completion of the institutional pathway but potentially different subsequent work and future orientation | Graduation-to-work transition records and distinct prospective evidence, not extrapolation of credit trends |

Five conceptual interlocutions: **Tinto** on persistence and experienced participation; **Zimmerman** on self-regulated learning and cycles of strategy change; **Pekrun** on control-value appraisal and epistemic/achievement emotions; **Muis** on epistemic beliefs and learning strategies; **Valsiner** on cultural-semiotic development and temporality. Do not imply that these frameworks were operationalized in the synthetic dataset.

A mixed-method future study would require instrument definitions, temporal alignment, interpretation procedures, ethical governance, and a plan for evidentiary triangulation and disconfirming cases. It remains a research design, not a report of conducted interviews.

## Open-science record: what has been demonstrated and what has not

**Demonstrated:** public version-controlled simulator and analysis scripts; programmatically generated synthetic data; documented assumptions; accessible tests; cross-language base-R checks for the original analysis; Python GEE–LMM comparison; independent GitHub Actions runs; downloadable machine-readable audit artifact; code-linked dashboard; explicit unfavorable diagnostic flags.

**Not demonstrated by this repository:** prior preregistration of a human-participant study; validation of psychometric instruments; open real participant datasets or ethically governed data harmonization; independent replication using an external study; application of the synthetic conclusions to real university cohorts; a comprehensive simulation of mixed-model estimation bias. The current audit was designed and run as a public methods exercise, not a registered confirmatory analysis.

**Next scientific gate:** keep this report public; revise simulation variable semantics in a new controlled version if necessary; choose whether the target of the next demonstration is hierarchical-variance stability, event-process inference, or an entirely different phenomenon concerning human judgment and cultural variation. Do not add many statistical methods without an estimand-driven question.
