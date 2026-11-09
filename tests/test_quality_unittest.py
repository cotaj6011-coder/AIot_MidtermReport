import unittest
from datetime import datetime, timezone

from src.preprocessing import validate_observation

NOW = datetime(2026, 11, 8, 12, 0, tzinfo=timezone.utc)

class QualityTests(unittest.TestCase):
    def test_rejects_capacity_violation(self):
        quality = validate_observation({"facility_id": "x", "observed_at": NOW, "total_spaces": 5, "available_spaces": 6}, NOW)
        self.assertFalse(quality.valid)
        self.assertEqual(quality.reason, "capacity_bounds")

    def test_rejects_missing_schema_field(self):
        quality = validate_observation({"facility_id": "x"}, NOW)
        self.assertFalse(quality.valid)
        self.assertTrue(quality.reason.startswith("missing:"))

