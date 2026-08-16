from datetime import datetime, timezone

import pytest

from tripadvisor_pipeline.errors import EmptyPageError, RepeatedPageError
from tripadvisor_pipeline.models import Provenance, ReviewRecord
from tripadvisor_pipeline.pagination import PageGuard


PROVENANCE = Provenance(
    source_type="synthetic_fixture",
    observed_at=datetime(2026, 8, 16, tzinfo=timezone.utc),
    parser_version="0.1.0",
    fixture_version="tripadvisor-review-page-v1",
)


def review(review_id: str) -> ReviewRecord:
    return ReviewRecord(
        property_id="property-001",
        review_id=review_id,
        title=f"Title {review_id}",
        text=f"Text {review_id}",
        rating=4.0,
        published_date="2026-01-02",
        language="en",
        provenance=PROVENANCE,
    )


def test_accepts_first_page_and_filters_overlap_from_later_page() -> None:
    guard = PageGuard(total_count=3)

    first = guard.accept(offset=0, records=[review("r1"), review("r2")])
    second = guard.accept(offset=2, records=[review("r2"), review("r3")])

    assert [item.review_id for item in first] == ["r1", "r2"]
    assert [item.review_id for item in second] == ["r3"]
    assert guard.complete is True


def test_rejects_same_page_fingerprint_at_a_new_offset() -> None:
    guard = PageGuard(total_count=4)
    page = [review("r1"), review("r2")]
    guard.accept(offset=0, records=page)

    with pytest.raises(RepeatedPageError, match="fingerprint"):
        guard.accept(offset=2, records=page)


def test_rejects_empty_page_before_total_is_reached() -> None:
    guard = PageGuard(total_count=2)

    with pytest.raises(EmptyPageError, match="before total_count"):
        guard.accept(offset=0, records=[])


def test_accepts_empty_page_after_total_is_reached() -> None:
    guard = PageGuard(total_count=1)
    guard.accept(offset=0, records=[review("r1")])

    assert guard.accept(offset=1, records=[]) == []
