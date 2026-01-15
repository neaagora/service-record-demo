from __future__ import annotations

from .policy import decide_policy
from .record_authority import RecordAuthority
from .subject_agent import SubjectAgent
from .wrapper import WrapperAgent


class Orchestrator:
    def __init__(self, authority: RecordAuthority) -> None:
        self.authority = authority

    def run(
        self, wrapper: WrapperAgent, subject: SubjectAgent, request: dict
    ) -> dict:
        descriptors = self.authority.get_recent_descriptors(subject.agent_id, limit=5)
        print(f"[consumer] fetched service record descriptors: {descriptors}")
        if not descriptors:
            print("[service record] empty: no prior observations")
        policy = decide_policy(descriptors)
        print(
            f"[policy] allow={policy.allow} "
            f"require_human_approval={policy.require_human_approval} "
            f"reason={policy.reason}"
        )

        if policy.require_human_approval:
            if request.get("human_approved") is True:
                print("[orchestrator] override: human approved")
                response = wrapper.mediate(subject, request)
                return response or {"status": "ok"}
            print("[orchestrator] blocked: human approval required")
            print(
                "[enforcement] authority reduced: requires human approval due to service record"
            )
            return {
                "status": "blocked",
                "reason": policy.reason,
                "next": "human_approval",
            }

        response = wrapper.mediate(subject, request)
        return response or {"status": "ok"}
