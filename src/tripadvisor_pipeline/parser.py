from __future__ import annotations

from typing import Any

from .errors import GraphQLErrorResponse, ResponseShapeError
from .models import Provenance, ReviewRecord


def _first_graphql_error(payload: list[dict[str, Any]]) -> str | None:
    for item in payload:
        errors = item.get("errors")
        if not isinstance(errors, list):
            continue
        for error in errors:
            if isinstance(error, dict) and error.get("message"):
                return str(error["message"])
        if errors:
            return "GraphQL response contained an unspecified error"
    return None


def _review_container(data: dict[str, Any]) -> dict[str, Any] | None:
    container = data.get("ReviewsProxy_getReviewListPageForLocation")
    if isinstance(container, list):
        return container[0] if container and isinstance(container[0], dict) else None
    if isinstance(container, dict):
        return container

    locations = data.get("locations")
    if not isinstance(locations, list) or not locations or not isinstance(locations[0], dict):
        return None
    review_list = locations[0].get("reviewList")
    return review_list if isinstance(review_list, dict) else None


def parse_review_page(
    payload: list[dict[str, Any]],
    *,
    property_id: str,
    provenance: Provenance,
) -> tuple[list[ReviewRecord], int]:
    if not isinstance(payload, list) or not payload or not isinstance(payload[0], dict):
        raise ResponseShapeError("response must be a non-empty list of objects")

    error_message = _first_graphql_error(payload)
    if error_message:
        raise GraphQLErrorResponse(error_message)

    data = payload[0].get("data")
    if not isinstance(data, dict):
        raise ResponseShapeError("response does not contain a data object")
    container = _review_container(data)
    if container is None:
        raise ResponseShapeError("response does not contain a documented review container")

    reviews = container.get("reviews")
    total_count = container.get("totalCount")
    if not isinstance(reviews, list) or not isinstance(total_count, int):
        raise ResponseShapeError("review container must contain reviews and integer totalCount")

    records: list[ReviewRecord] = []
    for review in reviews:
        if not isinstance(review, dict) or not review.get("id"):
            raise ResponseShapeError("every review must contain an id")
        rating = review.get("rating")
        if not isinstance(rating, (int, float)):
            raise ResponseShapeError("every review must contain a numeric rating")
        records.append(
            ReviewRecord(
                property_id=property_id,
                review_id=str(review["id"]),
                title=str(review.get("title") or ""),
                text=str(review.get("text") or ""),
                rating=float(rating),
                published_date=str(review.get("publishedDate") or ""),
                language=str(review.get("language") or ""),
                provenance=provenance,
            )
        )
    return records, total_count
