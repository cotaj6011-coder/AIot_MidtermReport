from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class QualityResult:
    valid: bool
    freshness_minutes: float
    reason: str = ""


def validate_observation(observation: dict, now: datetime, hard_stale_minutes: int = 30) -> QualityResult:
    required = {"facility_id", "observed_at", "total_spaces", "available_spaces"}
    missing = required.difference(observation)
    if missing:
        return QualityResult(False, float("inf"), f"missing:{','.join(sorted(missing))}")
    observed_at = observation["observed_at"]
    if isinstance(observed_at, str):
        observed_at = datetime.fromisoformat(observed_at.replace("Z", "+00:00"))
    if observed_at.tzinfo is None:
        observed_at = observed_at.replace(tzinfo=timezone.utc)
    freshness = max(0.0, (now - observed_at).total_seconds() / 60)
    total = int(observation["total_spaces"])
    available = int(observation["available_spaces"])
    if total < 0 or not 0 <= available <= total:
        return QualityResult(False, freshness, "capacity_bounds")
    if freshness > hard_stale_minutes:
        return QualityResult(False, freshness, "stale")
    return QualityResult(True, freshness)

