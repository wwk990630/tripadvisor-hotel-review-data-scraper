"""Offline-testable components for TripAdvisor data-pipeline research."""

from .checkpoint import CheckpointState
from .errors import (
    EmptyPageError,
    GraphQLErrorResponse,
    RepeatedPageError,
    ResponseShapeError,
    TripAdvisorPipelineError,
)
from .models import Provenance, ReviewRecord
from .pagination import PageGuard
from .parser import parse_review_page

__all__ = [
    "CheckpointState",
    "EmptyPageError",
    "GraphQLErrorResponse",
    "PageGuard",
    "Provenance",
    "RepeatedPageError",
    "ResponseShapeError",
    "ReviewRecord",
    "TripAdvisorPipelineError",
    "parse_review_page",
]
