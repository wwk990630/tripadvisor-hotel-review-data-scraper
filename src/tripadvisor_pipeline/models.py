from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen=True, slots=True)
class Provenance:
    source_type: str
    observed_at: datetime
    parser_version: str
    fixture_version: str

    def __post_init__(self) -> None:
        if self.observed_at.tzinfo is None or self.observed_at.utcoffset() is None:
            raise ValueError("observed_at must be timezone-aware")

    def to_dict(self) -> dict[str, str]:
        return {
            "source_type": self.source_type,
            "observed_at": self.observed_at.isoformat(),
            "parser_version": self.parser_version,
            "fixture_version": self.fixture_version,
        }


@dataclass(frozen=True, slots=True)
class ReviewRecord:
    property_id: str
    review_id: str
    title: str
    text: str
    rating: float
    published_date: str
    language: str
    provenance: Provenance

    def __post_init__(self) -> None:
        if not 0 <= self.rating <= 5:
            raise ValueError("rating must be between 0 and 5")

    def to_dict(self) -> dict[str, Any]:
        return {
            "property_id": self.property_id,
            "review_id": self.review_id,
            "title": self.title,
            "text": self.text,
            "rating": self.rating,
            "published_date": self.published_date,
            "language": self.language,
            "provenance": self.provenance.to_dict(),
        }
