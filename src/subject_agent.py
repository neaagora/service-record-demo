from __future__ import annotations


class SubjectAgent:
    def __init__(self, agent_id: str) -> None:
        self.agent_id = agent_id

    def act(self, request: dict) -> dict:
        if request.get("simulate") == "timeout":
            raise TimeoutError("simulated timeout")
        if request.get("simulate") == "hallucination":
            raise ValueError("simulated hallucination")

        return {"status": "ok", "details": "..."}
