from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Dict

from .models import ObservationRecord, ServiceRecord, now_iso


def _clone_observation(obs: ObservationRecord) -> ObservationRecord:
    try:
        return obs.model_copy(deep=True)
    except AttributeError:
        return obs.copy(deep=True)


def _record_to_dict(record: ServiceRecord) -> dict:
    try:
        return record.model_dump()
    except AttributeError:
        return record.dict()


class RecordAuthority:
    """In-memory record authority; no persistence yet."""

    def __init__(self, path: str = "data/records.json") -> None:
        self._records: Dict[str, ServiceRecord] = {}
        self._path = Path(path)
        print(f"[authority] persistence_path={self._path}")
        self._load()

    def _load(self) -> None:
        if not self._path.exists():
            return
        data = json.loads(self._path.read_text())
        if not isinstance(data, dict):
            return
        records: Dict[str, ServiceRecord] = {}
        for subject_id, payload in data.items():
            try:
                record = ServiceRecord.model_validate(payload)
            except AttributeError:
                record = ServiceRecord.parse_obj(payload)
            records[subject_id] = record
        self._records = records

    def _save(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        payload = {key: _record_to_dict(record) for key, record in self._records.items()}
        self._path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    def append_observation(self, obs: ObservationRecord) -> None:
        record = self._records.get(obs.subject_agent_id)
        if record is None:
            now = now_iso()
            record = ServiceRecord(
                subject_agent_id=obs.subject_agent_id,
                observations=[],
                created_iso=now,
                updated_iso=now,
            )
            self._records[obs.subject_agent_id] = record

        record.observations.append(_clone_observation(obs))
        record.updated_iso = now_iso()
        self._save()

    def get_service_record(self, subject_agent_id: str) -> ServiceRecord | None:
        return self._records.get(subject_agent_id)

    def get_recent_descriptors(
        self, subject_agent_id: str, limit: int = 5
    ) -> list[str]:
        record = self._records.get(subject_agent_id)
        if record is None:
            return []

        observations = record.observations[-limit:]
        descriptors: list[str] = []
        for observation in observations:
            descriptors.extend(observation.descriptors)
        return descriptors

    def export_record(self, subject_agent_id: str) -> dict | None:
        record = self._records.get(subject_agent_id)
        if record is None:
            return None

        last_two = record.observations[-2:]
        return {
            "subject_agent_id": record.subject_agent_id,
            "created_iso": record.created_iso,
            "updated_iso": record.updated_iso,
            "observation_count": len(record.observations),
            "last_two_observations": [
                {
                    "timestamp_iso": obs.timestamp_iso,
                    "descriptors": list(obs.descriptors),
                    "notes": obs.notes,
                }
                for obs in last_two
            ],
        }

    def get_record_fingerprint(self, subject_agent_id: str) -> str:
        payload = self.export_record(subject_agent_id) or {}
        encoded = json.dumps(payload, sort_keys=True).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

    def write_service_record_artifact(
        self, subject_agent_id: str, out_dir: str = "artifacts"
    ) -> str:
        payload = self.export_record(subject_agent_id) or {}
        output_dir = Path(out_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        path = output_dir / f"service_record__{subject_agent_id}.json"
        path.write_text(json.dumps(payload, indent=2, sort_keys=True))
        return str(path)
