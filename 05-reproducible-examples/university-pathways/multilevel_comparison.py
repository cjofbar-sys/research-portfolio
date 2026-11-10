"""Reproducible, fully synthetic GEE vs student-intercept mixed model.
Run from university-pathways directory. No participant or institutional data.
"""
from __future__ import annotations
import argparse
import json
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from analysis import SEED, simulate

FORMULA = "credits_earned ~ semester + first_gen + preparation + support + C(campus)"
TERMS = ["semester", "first_gen", "preparation", "support"]

def coefficient(fit, term):
    ci = fit.conf_int().loc[term]
    return {
        "estimate": float(fit.params[term]),
        "ci95": [float(ci.iloc[0]), float(ci.iloc[1])],
        "standard_error": float(fit.bse[term]),
    }

def run(panel: pd.DataFrame, students: pd.DataFrame):
    assert panel.student_id.nunique() <= len(students)
    assert panel.student_id.isin(students.student_id).all()
    counts = panel.groupby("student_id").size()
    gee = smf.gee(
        FORMULA, groups="student_id", data=panel,
        family=sm.families.Gaussian(),
        cov_struct=sm.cov_struct.Exchangeable(),
    ).fit()
    attempts = []
    fit = None
    for method in ("lbfgs", "powell", "bfgs"):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            try:
                candidate = smf.mixedlm(
                    FORMULA, panel, groups=panel["student_id"], re_formula="1"
                ).fit(reml=True, method=method, maxiter=350, disp=False)
                attempts.append({
                    "optimizer": method, "converged": bool(candidate.converged),
                    "warnings": [str(w.message) for w in caught],
                })
                if (candidate.converged and np.isfinite(candidate.scale)
                        and np.isfinite(candidate.cov_re.iloc[0, 0])):
                    fit = candidate
                    break
            except (np.linalg.LinAlgError, ValueError) as exc:
                attempts.append({
                    "optimizer": method, "converged": False,
                    "error": str(exc), "warnings": [str(w.message) for w in caught],
                })
    if fit is None:
        raise RuntimeError("No converged LMM: do not publish numeric estimates.")
    student_var = max(0.0, float(fit.cov_re.iloc[0, 0]))
    residual_var = float(fit.scale)
    return {
        "metadata": {
            "synthetic": True, "seed": SEED,
            "students_total": len(students),
            "students_observed": int(counts.size),
            "student_semesters": len(panel),
            "campuses": int(panel.campus.nunique()),
            "single_observation_students": int((counts == 1).sum()),
            "model_formula": FORMULA,
            "sample_note": "Credit records end at graduation or withdrawal; observation may be selective.",
        },
        "gee": {
            "type": "marginal gaussian GEE",
            "working_correlation": "exchangeable",
            "correlation": float(gee.cov_struct.dep_params),
            "converged": bool(gee.converged),
            "terms": {term: coefficient(gee, term) for term in TERMS},
        },
        "lmm": {
            "type": "Gaussian student random-intercept mixed model",
            "group": "student_id", "estimation": "REML",
            "converged": bool(fit.converged),
            "optimizer": attempts[-1]["optimizer"],
            "student_intercept_variance": student_var,
            "residual_variance": residual_var,
            "residual_icc": student_var / (student_var + residual_var),
            "near_boundary": student_var < 0.001 * residual_var,
            "terms": {term: coefficient(fit, term) for term in TERMS},
            "optimizer_attempts": attempts,
        },
        "interpretation_guards": [
            "Entirely synthetic observations; no real institutional finding.",
            "GEE population-average and mixed-model conditional interpretations are not interchangeable.",
            "Simulator does not impose a residual student-level random intercept after covariate adjustment.",
            "Only six campus levels; campus modeled as a fixed effect.",
            "Graduation and withdrawal end observed semester credits: the mixed model does not correct selection.",
            "Residual ICC is not a measurement of psychological meaning-making.",
        ],
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output", type=Path, default=Path("results/multilevel_comparison.json"))
    p.add_argument("--verify-snapshot", type=Path)
    args = p.parse_args()
    students, panel = simulate()
    report = run(panel, students)
    if args.verify_snapshot:
        stored = json.loads(args.verify_snapshot.read_text(encoding="utf-8"))
        for model in ("gee", "lmm"):
            for term in TERMS:
                for key in ("estimate", "standard_error"):
                    value = stored[model]["terms"][term][key]
                    computed = report[model]["terms"][term][key]
                    if not np.isclose(value, computed, atol=0.01, rtol=0):
                        raise SystemExit(f"Snapshot mismatch: {model}.{term}.{key}")
        if stored["metadata"]["seed"] != SEED or stored["metadata"]["student_semesters"] != len(panel):
            raise SystemExit("Snapshot metadata mismatch.")
        print("Snapshot values validated against executed source.")
        return
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({"metadata": report["metadata"], "gee": report["gee"], "lmm": {
        k: v for k, v in report["lmm"].items() if k != "optimizer_attempts"
    }}, indent=2))

if __name__ == "__main__":
    main()
