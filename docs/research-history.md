# Research history

## 2025: request reproduction

The first implementation reproduced a known review request, accepted a browser
session through configuration, paginated hotel URLs, and wrote JSONL progress.
It proved that the response could be collected at that time, but it coupled the
repository to transient identifiers and one request shape.

## April 2026: pipeline expansion

The private follow-up separated hotel discovery, regional pagination, cleaning,
review collection, optional contribution and interaction enrichment, caches,
concurrency, progress recovery, raw evidence, and CSV projection. Offline
inspection in August 2026 found 3,248 unique hotel records and 274 valid review
records across 11 hotel samples. Review IDs were unique within every result.

The larger implementation was more capable, but also made the public boundary
clearer: proxy credentials, browser state, changing query identifiers, raw
responses, and reviewer-level fields belong in a private research environment.

## August 2026: reproducible public core

The repository was rebuilt around synthetic fixtures and offline assertions.
The reusable result is not a frozen request. It is a set of testable boundaries:
response shape, normalized schema, error taxonomy, page identity, checkpoint
state, provenance, and release safety.
