"""Tests for synthetic seed and observed-panel selection audit."""
import sys
import unittest
from pathlib import Path
import math
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from stability_selection_audit import run

class SelectionAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result=run([20261108, 20261109])

    def test_all_synthetic_and_reproducible(self):
        r=self.result
        self.assertTrue(r["metadata"]["synthetic"])
        self.assertEqual(r["metadata"]["seeds"],[20261108,20261109])
        self.assertEqual(r["summary"]["n_converged_full"],2)
        self.assertEqual(r["summary"]["n_converged_early"],2)

    def test_event_based_observation(self):
        for iteration in self.result["iterations"]:
            c=iteration["composition"]
            self.assertEqual(c["entrants"],1170)
            self.assertGreater(c["never_observed_credits"],0)
            self.assertGreater(c["term1_observed"],c["term9plus_observed_unique"])
            self.assertTrue(all(math.isfinite(iteration[key]["first_gen"]) for key in ["full_gee","early_gee"]))

if __name__=="__main__":
    unittest.main()
