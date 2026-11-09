from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable

from src.domain_rules import score_prediction
from src.prediction import PersistenceBaseline
from src.preprocessing import validate_observation


@dataclass(frozen=True)
class AgentResult:
    status: str
    recommendations: tuple[dict, ...]
    evidence: tuple[str, ...]
    replans: int


class ParkingAgent:
    """Small deterministic orchestrator demonstrating plan/tool/retry/human branches."""

    def __init__(self, tools: dict[str, Callable[[], list[dict]]], max_replans: int = 1):
        self.tools = tools
        self.max_replans = max_replans
        self.model = PersistenceBaseline()

    def run(self, query: dict, now: datetime | None = None) -> AgentResult:
        now = now or datetime.now(timezone.utc)
        plan = list(query.get("preferred_sources", self.tools))
        replans = 0
        evidence: list[str] = []
        observations: list[tuple[dict, object]] = []
        attempted: set[str] = set()
        while plan:
            source = plan.pop(0)
            if source in attempted or source not in self.tools:
                continue
            attempted.add(source)
            try:
                raw_items = self.tools[source]()
                evidence.append(f"tool:{source}:ok")
            except Exception as exc:
                evidence.append(f"tool:{source}:error:{type(exc).__name__}")
                if replans < self.max_replans:
                    replans += 1
                    plan.extend(name for name in self.tools if name not in attempted)
                continue
            for item in raw_items:
                quality = validate_observation(item, now)
                evidence.append(f"quality:{item.get('facility_id','unknown')}:{quality.reason or 'valid'}")
                if quality.valid:
                    observations.append((item, quality))
            if observations:
                break
            if replans < self.max_replans:
                replans += 1
                plan.extend(name for name in self.tools if name not in attempted)
        if not observations:
            return AgentResult("human_review_required", (), tuple(evidence), replans)
        ranked = []
        for observation, quality in observations:
            forecast = self.model.predict(observation, int(query.get("horizon_minutes", 30)))
            forecast["total_spaces"] = observation["total_spaces"]
            # Critical invariant: each forecast uses the quality paired with its own observation.
            ranked.append(score_prediction(forecast, quality, float(observation.get("distance_km", 0))))
        ranked.sort(key=lambda row: row["score"], reverse=True)
        return AgentResult("ok", tuple(ranked[: int(query.get("top_k", 3))]), tuple(evidence), replans)

