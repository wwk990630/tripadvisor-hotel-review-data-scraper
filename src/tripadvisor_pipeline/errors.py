class TripAdvisorPipelineError(Exception):
    """Base class for deterministic pipeline failures."""


class GraphQLErrorResponse(TripAdvisorPipelineError):
    """The response contains an explicit GraphQL error."""


class ResponseShapeError(TripAdvisorPipelineError):
    """The response does not match a documented review envelope."""


class RepeatedPageError(TripAdvisorPipelineError):
    """A page fingerprint was observed at more than one offset."""


class EmptyPageError(TripAdvisorPipelineError):
    """Pagination ended before the advertised total was reached."""
