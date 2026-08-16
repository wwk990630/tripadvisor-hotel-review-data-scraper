from __future__ import annotations

import hashlib
from collections.abc import Sequence

from .errors import EmptyPageError, RepeatedPageError
from .models import ReviewRecord


class PageGuard:
    def __init__(self, *, total_count: int) -> None:
        if total_count < 0:
            raise ValueError("total_count must not be negative")
        self.total_count = total_count
        self.seen_review_ids: set[str] = set()
        self.seen_page_fingerprints: dict[str, int] = {}

    @property
    def complete(self) -> bool:
        return len(self.seen_review_ids) >= self.total_count

    def accept(self, *, offset: int, records: Sequence[ReviewRecord]) -> list[ReviewRecord]:
        if offset < 0:
            raise ValueError("offset must not be negative")
        if not records:
            if self.complete:
                return []
            raise EmptyPageError("empty page arrived before total_count was reached")

        ordered_ids = [record.review_id for record in records]
        fingerprint = hashlib.sha256("\0".join(ordered_ids).encode("utf-8")).hexdigest()
        previous_offset = self.seen_page_fingerprints.get(fingerprint)
        if previous_offset is not None:
            raise RepeatedPageError(
                f"page fingerprint from offset {previous_offset} repeated at offset {offset}"
            )
        self.seen_page_fingerprints[fingerprint] = offset

        new_records = [
            record for record in records if record.review_id not in self.seen_review_ids
        ]
        self.seen_review_ids.update(record.review_id for record in records)
        return new_records
