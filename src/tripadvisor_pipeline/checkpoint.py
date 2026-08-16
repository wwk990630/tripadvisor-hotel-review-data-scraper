from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen=True, slots=True)
class CheckpointState:
    schema_version: int
    property_id: str
    next_offset: int
    seen_review_ids: tuple[str, ...]
    seen_page_fingerprints: tuple[str, ...]
    updated_at: datetime

    def __post_init__(self) -> None:
        if self.schema_version != 1:
            raise ValueError("unsupported schema_version")
        if self.next_offset < 0:
            raise ValueError("next_offset must not be negative")
        if self.updated_at.tzinfo is None or self.updated_at.utcoffset() is None:
            raise ValueError("updated_at must be timezone-aware")

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "property_id": self.property_id,
            "next_offset": self.next_offset,
            "seen_review_ids": list(self.seen_review_ids),
            "seen_page_fingerprints": list(self.seen_page_fingerprints),
            "updated_at": self.updated_at.isoformat(),
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, sort_keys=True)

    @classmethod
    def from_json(cls, raw: str) -> CheckpointState:
        payload = json.loads(raw)
        if not isinstance(payload, dict):
            raise ValueError("checkpoint must be a JSON object")
        return cls(
            schema_version=int(payload["schema_version"]),
            property_id=str(payload["property_id"]),
            next_offset=int(payload["next_offset"]),
            seen_review_ids=tuple(str(item) for item in payload["seen_review_ids"]),
            seen_page_fingerprints=tuple(
                str(item) for item in payload["seen_page_fingerprints"]
            ),
            updated_at=datetime.fromisoformat(str(payload["updated_at"])),
        )
