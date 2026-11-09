from __future__ import annotations


def score_prediction(prediction: dict, quality, distance_km: float = 0.0) -> dict:
    total = max(1, int(prediction["total_spaces"]))
    availability = int(prediction["available_spaces"]) / total
    freshness_penalty = min(1.0, quality.freshness_minutes / 30.0)
    full_risk = max(0.0, min(1.0, 1.0 - availability + 0.25 * freshness_penalty))
    score = availability - full_risk - 0.05 * max(0.0, distance_km)
    return {**prediction, "full_risk": full_risk, "score": score}

