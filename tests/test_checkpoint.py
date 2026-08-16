from datetime import datetime, timezone

import pytest

from tripadvisor_pipeline.checkpoint import CheckpointState


def valid_state() -> CheckpointState:
    return CheckpointState(
        schema_version=1,
        property_id="property-001",
        next_offset=20,
        seen_review_ids=("review-001", "review-002"),
        seen_page_fingerprints=("sha256-value",),
        updated_at=datetime(2026, 8, 16, tzinfo=timezone.utc),
    )


def test_checkpoint_json_round_trip_is_privacy_minimized() -> None:
    restored = CheckpointState.from_json(valid_state().to_json())

    assert restored == valid_state()
    payload = restored.to_dict()
    assert set(payload) == {
        "schema_version",
        "property_id",
        "next_offset",
        "seen_review_ids",
        "seen_page_fingerprints",
        "updated_at",
    }


def test_checkpoint_rejects_unknown_schema_version() -> None:
    with pytest.raises(ValueError, match="schema_version"):
        CheckpointState.from_json(valid_state().to_json().replace('"schema_version": 1', '"schema_version": 2'))


def test_checkpoint_rejects_negative_offset() -> None:
    with pytest.raises(ValueError, match="next_offset"):
        CheckpointState(
            schema_version=1,
            property_id="property-001",
            next_offset=-1,
            seen_review_ids=(),
            seen_page_fingerprints=(),
            updated_at=datetime(2026, 8, 16, tzinfo=timezone.utc),
        )


def test_checkpoint_rejects_naive_timestamp() -> None:
    with pytest.raises(ValueError, match="timezone-aware"):
        CheckpointState(
            schema_version=1,
            property_id="property-001",
            next_offset=0,
            seen_review_ids=(),
            seen_page_fingerprints=(),
            updated_at=datetime(2026, 8, 16),
        )
