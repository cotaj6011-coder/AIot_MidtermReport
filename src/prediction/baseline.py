from __future__ import annotations


class PersistenceBaseline:
    """Predict the most recent observed availability."""

    def predict(self, observation: dict, horizon_minutes: int) -> dict:
        available = max(0, min(int(observation["available_spaces"]), int(observation["total_spaces"])))
        return {
            "facility_id": observation["facility_id"],
            "horizon_minutes": horizon_minutes,
            "available_spaces": available,
            "model": "persistence",
        }

