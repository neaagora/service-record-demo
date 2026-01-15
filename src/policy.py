from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PolicyDecision:
    allow: bool
    require_human_approval: bool
    reason: str


def decide_policy(descriptors: list[str]) -> PolicyDecision:
    # Record authority does not enforce policy; downstream consumers do.
    if "needs_escalation" in descriptors or "timeout" in descriptors:
        triggers = []
        if "timeout" in descriptors:
            triggers.append("timeout")
        if "needs_escalation" in descriptors:
            triggers.append("needs_escalation")
        trigger_list = ", ".join(triggers) if triggers else "unknown"
        return PolicyDecision(
            allow=False,
            require_human_approval=True,
            reason=f"Blocked because service record contains: {trigger_list}",
        )

    return PolicyDecision(
        allow=True,
        require_human_approval=False,
        reason="No blocking descriptors detected.",
    )
