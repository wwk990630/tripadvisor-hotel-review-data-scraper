from datetime import datetime, timezone

import pytest

from tripadvisor_pipeline.models import Provenance, ReviewRecord


def provenance() -> Provenance:
    return Provenance(
        source_type="synthetic_fixture",
        observed_at=datetime(2026, 8, 16, tzinfo=timezone.utc),
        parser_version="0.1.0",
        fixture_version="tripadvisor-review-page-v1",
    )


def test_review_record_serializes_without_reviewer_identity() -> None:
    record = ReviewRecord(
        property_id="property-001",
        review_id="review-001",
        title="A synthetic stay",
        text="Synthetic fixture text.",
        rating=4.0,
        published_date="2026-01-02",
        language="en",
        provenance=provenance(),
    )

    payload = record.to_dict()

    assert payload["review_id"] == "review-001"
    assert payload["provenance"]["source_type"] == "synthetic_fixture"
    assert not ({"username", "display_name", "user_profile_id"} & payload.keys())


@pytest.mark.parametrize("rating", [-0.1, 5.1])
def test_review_record_rejects_rating_outside_zero_to_five(rating: float) -> None:
    with pytest.raises(ValueError, match="rating"):
        ReviewRecord(
            property_id="property-001",
            review_id="review-001",
            title="Synthetic title",
            text="Synthetic text.",
            rating=rating,
            published_date="2026-01-02",
            language="en",
            provenance=provenance(),
        )


def test_provenance_rejects_naive_timestamp() -> None:
    with pytest.raises(ValueError, match="timezone-aware"):
        Provenance(
            source_type="synthetic_fixture",
            observed_at=datetime(2026, 8, 16),
            parser_version="0.1.0",
            fixture_version="tripadvisor-review-page-v1",
        )
