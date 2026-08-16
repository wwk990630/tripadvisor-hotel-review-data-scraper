# TripAdvisor Hotel Review Data Scraper｜猫途鹰酒店评论爬虫与数据获取

[简体中文](README.zh-CN.md)

A self-taught, project-driven Python study of TripAdvisor hotel review acquisition. The repository preserves the reusable engineering core of a longer investigation: schema-aware parsing, pagination guards, privacy-minimized checkpoints, provenance, and release-safety checks.

## What is included

- normalized review records with author identity excluded;
- parsers for two documented response envelopes;
- explicit GraphQL and response-shape errors;
- overlap, repeated-page, and premature-empty-page detection;
- checkpoints containing IDs and hashes rather than review content;
- artificial success/failure fixtures and a public-tree scanner.

No accounts, cookies, authorization material, live query identifiers, proxy settings, private captures, or collected datasets are included.

## Quick start

\`\`\`bash
python -m pip install -e .[test]
python -m pytest -q
python scripts/check_public_tree.py .
\`\`\`

## Architecture

\`artificial response → parser → normalized records → pagination guard → privacy-minimized checkpoint\`

See [architecture](docs/architecture.md), [evidence](docs/evidence.md), and [research history](docs/research-history.md).

## Technical route

The work evolved from reproducing one request shape in 2025, to a broader private pipeline in April 2026, and finally to an offline-testable public core in August 2026. Request acceptance, response classification, normalization, pagination, and persistence are treated as separate checkpoints.

## Problems and rejected routes

A cookie-dependent one-off script could work once without explaining whether later failure came from session expiry, GraphQL errors, shape drift, or pagination. Publishing the private pipeline was rejected because it contained short-lived credentials and real research data. The public result keeps the tested contracts without redistributing sensitive evidence. See [problem-solving notes](docs/problem-solving.md).

## Validation

The offline suite verifies models, two parser envelopes, failure responses, pagination invariants, checkpoints, and the release scanner. Fixture verification does not prove current live transport acceptance or a stable query identifier.

## Responsible use

Use only data you are permitted to access. Respect platform terms, robots guidance, rate limits, privacy, copyright, and applicable law. Do not paste credentials, cookies, authorization headers, private captures, or personal data into Issues.

## Contact

Use GitHub Issues for reproducible public bugs and documentation questions. For private or disclosure-sensitive matters, email [wwk990630@gmail.com](mailto:wwk990630@gmail.com).

## Author

WenKang — a third-year master's student at Nankai University. This software and protocol work was learned independently through hands-on projects.

## License

MIT for the code and artificial fixtures; third-party content and privately collected datasets are excluded.
