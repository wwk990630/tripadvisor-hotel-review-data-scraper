# TripAdvisor Data Pipeline Lab

An offline-testable case study in turning a changing web response into a
reproducible data pipeline.

This repository focuses on the parts that remain useful after a particular
request or session expires: response checkpoints, schema-aware parsing,
pagination guards, privacy-minimized progress state, provenance, and public
release checks. It does not include a live bulk collector or promise current
online access to TripAdvisor.

## What is included

- a small normalized `ReviewRecord` contract;
- parsers for two response envelopes observed during the project;
- explicit GraphQL and response-shape errors;
- overlap, repeated-page, and premature-empty-page detection;
- a durable checkpoint that stores IDs and hashes rather than review content;
- synthetic success and failure fixtures;
- a repository scanner for credentials, personal data, raw outputs, and local
  paths.

All fixtures are artificial. No collected review, reviewer profile, browser
session, proxy credential, or current query identifier is committed.

## Quick start

```bash
python -m pip install -e .[test]
python -m pytest -q
python scripts/check_public_tree.py .
```

The default workflow is completely offline.

## Why this repository changed

The first public version was a cookie-dependent script built around one known
request shape. A later private research implementation grew into a fuller
pipeline: hotel discovery, review pagination, optional enrichment, concurrent
workers, resumable output, and structured cleaning. That implementation also
contained short-lived credentials and real research data, so copying it to a
public repository would have been the wrong engineering decision.

This version extracts the reusable core and makes each claim testable. The
private evidence informs the contracts; it is not redistributed.

## Evidence level

| Component | Evidence | What it does not prove |
|---|---|---|
| Models and checkpoints | Unit tested | Current online acceptance |
| Response parser | Synthetic fixtures derived from documented shapes | A stable live query identifier |
| Pagination guard | Deterministic unit tests | Unlimited or complete collection |
| Public-tree scanner | Self-test against the repository | Legal permission for a separate collection |

See [evidence](docs/evidence.md), [architecture](docs/architecture.md), and the
[research history](docs/research-history.md) for details.

## Responsible use

Publicly visible data is not the same as unrestricted automated access. Review
the applicable terms, permissions, privacy obligations, and rate limits before
using any data source. This repository deliberately provides no target-site
network entrypoint.

## License

MIT. The license covers the code and synthetic fixtures in this repository,
not third-party site content or privately collected datasets.
