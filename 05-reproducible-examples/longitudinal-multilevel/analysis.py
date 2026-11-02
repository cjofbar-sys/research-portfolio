"""Synthetic longitudinal demonstration; not empirical student research.

Students are nested in programmes and measured at five occasions.
An informative-missingness stress test removes some later, low-scoring
observations to examine potential changes in estimated time trends.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf


def generate(seed: int = 20261102) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows: list[dict[str, float | int]] = []
    for programme in range(8):
        context = rng.normal(0, 2.0)
        for student in range(18):
            baseline = rng.normal(0, 5.0)
            slope = rng.normal(0, 0.7)
            person_id = programme * 18 + student
            for time in range(5):
                score = 40 + context + baseline + (1.4 + slope) * time + rng.normal(0, 2.1)
                rows.append({"programme": programme, "student": person_id,
                             "time": time, "score": score})
    return pd.DataFrame(rows)


def main() -> None:
    data = generate()
    assert len(data) == 720 and data.student.nunique() == 144
    print("Synthetic observations:", len(data),
          "students:", data.student.nunique(),
          "programmes:", data.programme.nunique())

    naive = smf.ols("score ~ time", data).fit()
    adjusted = smf.ols("score ~ time + C(programme)", data).fit(
        cov_type="cluster", cov_kwds={"groups": data["student"]}
    )
    # Student-level random intercepts and slopes; programme included as fixed effects.
    mixed = smf.mixedlm("score ~ time + C(programme)",
                        data, groups=data["student"],
                        re_formula="~time").fit(method="lbfgs", reml=False)
    print("\nOLS slope:", round(float(naive.params["time"]), 3))
    print("Cluster-robust programme-adjusted slope:",
          round(float(adjusted.params["time"]), 3))
    print("Mixed-model slope:", round(float(mixed.params["time"]), 3))
    print("Mixed-model 95% CI:", mixed.conf_int().loc["time"].round(3).tolist())
    print("Mixed-model converged:", mixed.converged)

    rng = np.random.default_rng(41)
    missing_probability = np.where(
        (data["time"].to_numpy() >= 2) &
        (data["score"].to_numpy() < data["score"].median()), 0.65, 0.04
    )
    observed = data.loc[rng.random(len(data)) >= missing_probability].copy()
    sensitivity = smf.ols("score ~ time", observed).fit()
    print("\nComplete-data OLS slope:", round(float(naive.params["time"]), 3))
    print("Selected-observation OLS slope:",
          round(float(sensitivity.params["time"]), 3))
    print("Retained observations:", len(observed))
    print("Caution: the missingness mechanism depends on values of the outcome.")
    print("Neither slope is evidence about real students.")


if __name__ == "__main__":
    main()
