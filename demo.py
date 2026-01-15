from __future__ import annotations

import argparse
import os
import time

from pathlib import Path

from src.orchestrator import Orchestrator
from src.record_authority import RecordAuthority
from src.subject_agent import SubjectAgent
from src.wrapper import WrapperAgent


p = Path("data/records.json")
if p.exists():
    p.unlink()
    print("[demo] reset: cleared data/records.json")
else:
    print("[demo] reset: no existing data/records.json")


def _print_summary(authority: RecordAuthority, subject_id: str) -> None:
    export = authority.export_record(subject_id) or {}
    last_obs = export.get("last_two_observations", [])[-1] if export else {}
    fingerprint = authority.get_record_fingerprint(subject_id)
    print(f"[service record] fingerprint={fingerprint}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Service record demo runner.")
    parser.add_argument("--reset", action="store_true", help="Clear persisted records.")
    args = parser.parse_args()

    data_path = Path("data/records.json")
    if args.reset:
        if data_path.exists():
            data_path.unlink()
        print("[demo] reset enabled")

    authority = RecordAuthority()
    wrapper = WrapperAgent("wrapper-1", authority)
    subject = SubjectAgent("agent-gamma")
    orch = Orchestrator(authority)

    print(f"[subject] {subject.agent_id}")
    print("[demo] Service Record Enforcement: timeout -> block -> human override")
    print("=== run #1 ===")
    request_1 = {
        "task": "book_table",
        "simulate": "timeout",
        "interaction_type": "booking",
        "complexity": "medium",
    }
    outcome_1 = orch.run(wrapper, subject, request_1)
    print(f"[outcome] {outcome_1}")
    _print_summary(authority, subject.agent_id)
    path = authority.write_service_record_artifact("agent-gamma")
    print(f"[artifact] wrote {path}")
    time.sleep(2)

    print("=== run #2 ===")
    request_2 = {
        "task": "book_table",
        "interaction_type": "booking",
        "complexity": "medium",
    }
    outcome_2 = orch.run(wrapper, subject, request_2)
    print(f"[outcome] {outcome_2}")
    _print_summary(authority, subject.agent_id)
    time.sleep(2)

    print("=== run #3 ===")
    request_3 = {
        "task": "book_table",
        "interaction_type": "booking",
        "complexity": "medium",
        "human_approved": True,
    }
    outcome_3 = orch.run(wrapper, subject, request_3)
    print(f"[outcome] {outcome_3}")
    _print_summary(authority, subject.agent_id)
    path = authority.write_service_record_artifact("agent-gamma")
    print(f"[artifact] wrote {path}")


if __name__ == "__main__":
    main()
