class TripAdvisorPipelineError(Exception):
    """Base class for deterministic pipeline failures."""


class GraphQLErrorResponse(TripAdvisorPipelineError):
    """The response contains an explicit GraphQL error."""


class ResponseShapeError(TripAdvisorPipelineError):
    """The response does not match a documented review envelope."""
