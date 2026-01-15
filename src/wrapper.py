from __future__ import annotations

from .models import ObservationRecord, now_iso
from .record_authority import RecordAuthority
from .subject_agent import SubjectAgent


class WrapperAgent:
    def __init__(self, wrapper_id: str, authority: RecordAuthority) -> None:
        self.wrapper_id = wrapper_id
        self.authority = authority

    def mediate(self, subject: SubjectAgent, request: dict) -> dict:
        interaction_type = request.get("interaction_type", "unknown")
        complexity = request.get("complexity", "low")

        try:
            response = subject.act(request)
            descriptors = ["success"]
            if request.get("human_approved") is True:
                descriptors.insert(1, "human_approved_override")
            record = ObservationRecord(
                subject_agent_id=subject.agent_id,
                observer_id=self.wrapper_id,
                timestamp_iso=now_iso(),
                interaction_type=interaction_type,
                complexity=complexity,
                descriptors=descriptors,
                observer_confidence=0.9,
                notes=None,
            )
            self.authority.append_observation(record)
            print("[producer] wrote observation to service record authority")
            return response
        except ValueError:
            descriptors = ["hallucinated_confirmation", "needs_escalation"]
            if request.get("human_approved") is True:
                insert_at = 1 if descriptors else 0
                descriptors.insert(insert_at, "human_approved_override")
            record = ObservationRecord(
                subject_agent_id=subject.agent_id,
                observer_id=self.wrapper_id,
                timestamp_iso=now_iso(),
                interaction_type=interaction_type,
                complexity=complexity,
                descriptors=descriptors,
                observer_confidence=0.9,
                notes="ValueError during subject agent action.",
            )
            self.authority.append_observation(record)
            print("[producer] wrote observation to service record authority")
            return {"status": "failed", "error": "hallucination"}
        except TimeoutError:
            descriptors = ["timeout", "needs_escalation"]
            if request.get("human_approved") is True:
                insert_at = 1 if descriptors else 0
                descriptors.insert(insert_at, "human_approved_override")
            record = ObservationRecord(
                subject_agent_id=subject.agent_id,
                observer_id=self.wrapper_id,
                timestamp_iso=now_iso(),
                interaction_type=interaction_type,
                complexity=complexity,
                descriptors=descriptors,
                observer_confidence=0.95,
                notes="Timeout during subject agent action.",
            )
            self.authority.append_observation(record)
            print("[producer] wrote observation to service record authority")
            return {"status": "failed", "error": "timeout"}
