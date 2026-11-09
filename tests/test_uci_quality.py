import unittest
from tools.analyze_uci import analyze

class UciQualityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = analyze()

    def test_authoritative_counts(self):
        self.assertEqual((self.report["rows"], self.report["facilities"], self.report["exact_duplicate_rows"]), (35717, 30, 216))

    def test_required_columns(self):
        self.assertEqual(self.report["columns"], ["SystemCodeNumber", "Capacity", "Occupancy", "LastUpdated"])

