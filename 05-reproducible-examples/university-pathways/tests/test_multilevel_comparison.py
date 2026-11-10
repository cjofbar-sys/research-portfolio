"""Regression checks for the entirely synthetic multilevel comparison."""
import unittest
from pathlib import Path
import sys
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from analysis import simulate
from multilevel_comparison import run

class MultilevelComparisonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.students, cls.panel = simulate()
        cls.report = run(cls.panel, cls.students)

    def test_same_panel_and_observed_population(self):
        m = self.report["metadata"]
        self.assertEqual((m["students_total"], m["students_observed"], m["student_semesters"]), (1170, 1136, 9674))
        self.assertEqual(m["single_observation_students"], 27)

    def test_reproduces_published_gee(self):
        gee = self.report["gee"]
        self.assertTrue(gee["converged"])
        self.assertAlmostEqual(gee["terms"]["semester"]["estimate"], -0.0183, places=4)
        self.assertAlmostEqual(gee["terms"]["first_gen"]["estimate"], -0.9137, places=4)

    def test_distinct_mixed_model_and_uncertainty(self):
        lmm = self.report["lmm"]
        self.assertTrue(lmm["converged"])
        self.assertEqual(lmm["estimation"], "REML")
        self.assertGreaterEqual(lmm["student_intercept_variance"], 0)
        self.assertGreater(lmm["residual_variance"], 0)
        self.assertTrue(0 <= lmm["residual_icc"] <= 1)
        for model in [lmm, self.report["gee"]]:
            for row in model["terms"].values():
                self.assertTrue(np.all(np.isfinite([
                    row["estimate"], row["standard_error"], *row["ci95"]
                ])))
                self.assertLessEqual(row["ci95"][0], row["estimate"])
                self.assertGreaterEqual(row["ci95"][1], row["estimate"])

if __name__ == "__main__":
    unittest.main()
