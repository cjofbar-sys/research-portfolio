import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from analysis import cumulative_incidence, simulate, N_CAMPUSES, N_COHORTS, PER_CELL


class SyntheticPathwayTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.students, cls.panel = simulate()

    def test_reproducible(self):
        other, _ = simulate()
        self.assertTrue(self.students.equals(other))

    def test_cohort_structure(self):
        self.assertEqual(len(self.students), N_CAMPUSES * N_COHORTS * PER_CELL)
        self.assertEqual(self.students.student_id.nunique(), len(self.students))

    def test_competing_risks(self):
        ci = cumulative_incidence(self.students)
        self.assertTrue((ci.graduation_cif.diff().fillna(0) >= -1e-7).all())
        self.assertTrue((ci.withdrawal_cif.diff().fillna(0) >= -1e-7).all())
        self.assertTrue(((ci.graduation_cif + ci.withdrawal_cif) <= 1.000001).all())
        self.assertAlmostEqual(ci.graduation_cif.iloc[-1],
                               self.students.graduated.mean(), places=5)

    def test_employment_denominator(self):
        self.assertTrue(self.students.loc[self.students.graduated == 0, "employed_6m"].isna().all())


if __name__ == "__main__":
    unittest.main()
