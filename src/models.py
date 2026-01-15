from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from pydantic import BaseModel


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def short_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:8]}"


class ObservationRecord(BaseModel):
    subject_agent_id: str
    observer_id: str
    timestamp_iso: str
    interaction_type: str
    complexity: str
    descriptors: list[str]
    observer_confidence: float
    notes: str | None = None


class ServiceRecord(BaseModel):
    subject_agent_id: str
    observations: list[ObservationRecord]
    created_iso: str
    updated_iso: str
