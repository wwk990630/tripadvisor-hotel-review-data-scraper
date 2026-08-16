import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from tripadvisor_pipeline.errors import GraphQLErrorResponse, ResponseShapeError
from tripadvisor_pipeline.models import Provenance
from tripadvisor_pipeline.parser import parse_review_page


FIXTURES = Path(__file__).parent / "fixtures"


def provenance() -> Provenance:
    return Provenance(
        source_type="synthetic_fixture",
        observed_at=datetime(2026, 8, 16, tzinfo=timezone.utc),
        parser_version="0.1.0",
        fixture_version="tripadvisor-review-page-v1",
    )


def load(name: str) -> list[dict]:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_parses_current_review_proxy_envelope_without_identity_fields() -> None:
    payload = load("review_page_success.json")
    payload[0]["data"]["ReviewsProxy_getReviewListPageForLocation"][0]["reviews"][0][
        "userProfile"
    ] = {"id": "identity-must-not-be-exported", "displayName": "Synthetic Person"}
    records, total = parse_review_page(
        payload,
        property_id="property-001",
        provenance=provenance(),
    )

    assert total == 2
    assert [record.review_id for record in records] == ["review-001", "review-002"]
    assert records[0].rating == 4.0
    assert "identity-must-not-be-exported" not in json.dumps(
        [record.to_dict() for record in records]
    )


def test_parses_legacy_locations_review_list_envelope() -> None:
    current = load("review_page_success.json")[0]["data"]
    target = current["ReviewsProxy_getReviewListPageForLocation"][0]
    legacy = [{"data": {"locations": [{"reviewList": target}]}}]

    records, total = parse_review_page(
        legacy,
        property_id="property-001",
        provenance=provenance(),
    )

    assert total == 2
    assert [record.review_id for record in records] == ["review-001", "review-002"]


def test_raises_a_specific_error_for_graphql_errors() -> None:
    with pytest.raises(GraphQLErrorResponse, match="Synthetic GraphQL failure"):
        parse_review_page(
            load("review_page_graphql_error.json"),
            property_id="property-001",
            provenance=provenance(),
        )


def test_raises_a_specific_error_for_unknown_response_shape() -> None:
    with pytest.raises(ResponseShapeError, match="review container"):
        parse_review_page(
            [{"data": {"unrelated": []}}],
            property_id="property-001",
            provenance=provenance(),
        )
