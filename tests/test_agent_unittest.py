import unittest
from datetime import datetime, timedelta, timezone

from src.agent import ParkingAgent

NOW = datetime(2026, 11, 8, 12, 0, tzinfo=timezone.utc)

def observation(name, available, age_minutes=1):
    return {"facility_id": name, "observed_at": NOW - timedelta(minutes=age_minutes), "total_spaces": 10, "available_spaces": available}

class AgentTests(unittest.TestCase):
    def test_each_candidate_uses_its_own_quality(self):
        result = ParkingAgent({"primary": lambda: [observation("fresh", 5, 1), observation("older", 5, 20)]}).run({"preferred_sources": ["primary"]}, NOW)
        self.assertEqual([item["facility_id"] for item in result.recommendations], ["fresh", "older"])
        self.assertLess(result.recommendations[0]["full_risk"], result.recommendations[1]["full_risk"])

    def test_replan_to_fallback_tool_after_exception(self):
        def broken():
            raise TimeoutError
        result = ParkingAgent({"primary": broken, "fallback": lambda: [observation("B", 4)]}).run({"preferred_sources": ["primary"]}, NOW)
        self.assertEqual(result.status, "ok")
        self.assertEqual(result.replans, 1)
        self.assertTrue(any("TimeoutError" in entry for entry in result.evidence))

    def test_human_review_when_no_valid_data(self):
        result = ParkingAgent({"primary": lambda: [observation("stale", 4, 60)]}).run({}, NOW)
        self.assertEqual(result.status, "human_review_required")
        self.assertFalse(result.recommendations)

