"""Fully synthetic university pathways demonstration.

All variables and relationships are invented for methodological illustration.
No empirical university data or individual records enter the simulation.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

SEED = 20261108
N_CAMPUSES, N_COHORTS, PER_CELL = 6, 3, 65
MAX_SEMESTERS, TIMELY_SEMESTERS = 12, 10
CREDITS_REQUIRED = 200


def logistic(x):
    return 1.0 / (1.0 + np.exp(-np.clip(x, -30, 30)))


def simulate(seed: int = SEED):
    rng = np.random.default_rng(seed)
    campus_support = rng.normal(0, 0.26, N_CAMPUSES)
    profiles, records = [], []
    sid = 0
    for campus in range(N_CAMPUSES):
        for cohort in range(N_COHORTS):
            for _ in range(PER_CELL):
                sid += 1
                first_gen = int(rng.random() < logistic(0.45 - 0.20 * campus))
                preparation = float(rng.normal(-0.25 * first_gen, 0.9))
                support = float(rng.normal(0.15 + campus_support[campus], 0.7))
                internship = int(rng.random() < logistic(-0.15 + 0.55 * support + 0.35 * preparation))
                credits = 0.0
                event, event_time = "censored", MAX_SEMESTERS
                for semester in range(1, MAX_SEMESTERS + 1):
                    if rng.random() < logistic(-4.5 + 0.12 * semester +
                                               0.75 * first_gen - 0.65 * support -
                                               0.30 * preparation):
                        event, event_time = "withdrawal", semester
                        break
                    earned = float(np.clip(rng.normal(
                        22 + 2.6 * preparation + 1.8 * support -
                        1.1 * first_gen + 0.65 * campus_support[campus], 4.4), 0, 35))
                    credits = min(CREDITS_REQUIRED, credits + earned)
                    records.append({
                        "student_id": sid, "campus": campus, "cohort": cohort,
                        "semester": semester, "credits_earned": earned,
                        "credits_total": credits, "first_gen": first_gen,
                        "preparation": preparation, "support": support,
                    })
                    if credits >= CREDITS_REQUIRED:
                        event, event_time = "graduation", semester
                        break
                employed = None
                if event == "graduation":
                    employed = int(rng.random() < logistic(
                        -0.2 + 0.62 * internship + 0.38 * preparation +
                        0.2 * support - 0.22 * first_gen))
                profiles.append({
                    "student_id": sid, "campus": campus, "cohort": cohort,
                    "first_gen": first_gen, "preparation": preparation,
                    "support": support, "internship": internship,
                    "event": event, "event_time": event_time,
                    "timely_graduation": int(event == "graduation" and event_time <= TIMELY_SEMESTERS),
                    "graduated": int(event == "graduation"), "employed_6m": employed,
                })
    return pd.DataFrame(profiles), pd.DataFrame(records)


def cumulative_incidence(students: pd.DataFrame):
    """Aalen-Johansen-style life table for two first-event competing risks."""
    at_risk = len(students)
    survival = 1.0
    cif_grad = cif_withdraw = 0.0
    rows = []
    for semester in range(1, MAX_SEMESTERS + 1):
        events = students.loc[students.event_time == semester, "event"]
        ng = int((events == "graduation").sum())
        nw = int((events == "withdrawal").sum())
        if at_risk > 0:
            cif_grad += survival * ng / at_risk
            cif_withdraw += survival * nw / at_risk
            survival *= 1 - (ng + nw) / at_risk
        rows.append({
            "semester": semester, "at_risk": at_risk,
            "new_graduations": ng, "new_withdrawals": nw,
            "graduation_cif": round(cif_grad, 6),
            "withdrawal_cif": round(cif_withdraw, 6),
            "event_free_survival": round(survival, 6),
        })
        at_risk -= ng + nw
    return pd.DataFrame(rows)


def fit_logistic(formula: str, df: pd.DataFrame, term: str):
    fit = smf.glm(formula, data=df, family=sm.families.Binomial()).fit()
    low, high = fit.conf_int().loc[term]
    return {
        "n": int(fit.nobs), "term": term,
        "log_odds": round(float(fit.params[term]), 4),
        "odds_ratio": round(float(np.exp(fit.params[term])), 4),
        "or_ci95": [round(float(np.exp(low)), 4), round(float(np.exp(high)), 4)],
        "p_value": round(float(fit.pvalues[term]), 6),
        "converged": bool(fit.converged),
    }, fit


def analyze(students: pd.DataFrame, panel: pd.DataFrame):
    ci = cumulative_incidence(students)
    timely, graduation_fit = fit_logistic(
        "timely_graduation ~ first_gen + preparation + support + C(campus) + C(cohort)",
        students, "first_gen")
    # An adjusted absolute contrast by standardizing over the same covariate distribution.
    data_zero, data_one = students.copy(), students.copy()
    data_zero["first_gen"], data_one["first_gen"] = 0, 1
    standardized = {
        "predicted_probability_first_gen_0": round(float(graduation_fit.predict(data_zero).mean()), 4),
        "predicted_probability_first_gen_1": round(float(graduation_fit.predict(data_one).mean()), 4),
    }
    standardized["risk_difference_1_minus_0"] = round(
        standardized["predicted_probability_first_gen_1"] -
        standardized["predicted_probability_first_gen_0"], 4)
    # Semester observations are correlated within each student.
    gee = smf.gee(
        "credits_earned ~ semester + first_gen + preparation + support + C(campus)",
        groups="student_id", data=panel, family=sm.families.Gaussian(),
        cov_struct=sm.cov_struct.Exchangeable()).fit()
    employed = students.loc[students.graduated == 1].copy()
    job, _ = fit_logistic(
        "employed_6m ~ internship + first_gen + preparation + support + C(campus)",
        employed, "internship")
    by_group = students.groupby("first_gen").agg(
        entrants=("student_id", "size"),
        timely=("timely_graduation", "sum"),
        graduates=("graduated", "sum")).reset_index()
    by_group["timely_rate"] = (by_group.timely / by_group.entrants).round(4)
    by_group["graduation_rate"] = (by_group.graduates / by_group.entrants).round(4)
    out = {
        "metadata": {"synthetic": True, "seed": SEED, "source": "analysis.py",
                     "students": int(len(students)), "campuses": N_CAMPUSES,
                     "cohorts": N_COHORTS, "followup_semesters": MAX_SEMESTERS},
        "descriptive": {
            "timely_graduation_rate": round(float(students.timely_graduation.mean()), 4),
            "graduation_by_12_rate": round(float(students.graduated.mean()), 4),
            "withdrawal_rate": round(float((students.event == "withdrawal").mean()), 4),
            "employed_among_graduates_rate": round(float(employed.employed_6m.mean()), 4),
            "employment_denominator": int(len(employed)),
            "first_generation_groups": by_group.to_dict(orient="records"),
        },
        "models": {
            "timely_graduation_first_gen": timely,
            "standardized_timely_graduation": standardized,
            "semester_credit_progression": {
                "n_observations": int(gee.nobs), "n_students": int(panel.student_id.nunique()),
                "semester_coefficient": round(float(gee.params["semester"]), 4),
                "semester_ci95": [round(float(v), 4) for v in gee.conf_int().loc["semester"]],
                "first_gen_coefficient": round(float(gee.params["first_gen"]), 4),
                "first_gen_ci95": [round(float(v), 4) for v in gee.conf_int().loc["first_gen"]],
            },
            "employment_internship_conditional_on_graduation": job,
        },
        "competing_risks": ci.to_dict(orient="records"),
        "limitations": [
            "All data and effects are simulated; no estimates describe actual students.",
            "Standardized associations are not causal effects.",
            "Employment is observed only for simulated graduates (selection).",
            "Graduation and withdrawal are competing first events.",
            "Unmeasured factors and designed simulation assumptions shape estimates.",
        ],
    }
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("results"))
    args = parser.parse_args()
    students, panel = simulate()
    assert len(students) == N_CAMPUSES * N_COHORTS * PER_CELL
    assert students.student_id.is_unique
    assert not (students.graduated.eq(0) & students.employed_6m.notna()).any()
    assert (panel.credits_earned >= 0).all()
    report = analyze(students, panel)
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "summary.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    students.to_csv(args.output / "synthetic_students.csv", index=False)
    panel.to_csv(args.output / "synthetic_semesters.csv", index=False)
    print(json.dumps({"metadata": report["metadata"], "descriptive": report["descriptive"],
                      "models": report["models"]}, indent=2))


if __name__ == "__main__":
    main()
