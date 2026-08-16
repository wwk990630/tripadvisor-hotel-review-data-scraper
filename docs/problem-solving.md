# Problem-solving record

## Initial symptom

A request could appear to work once, then return an error, a different response envelope, a repeated page, or no target records.

## Competing hypotheses

The investigation separated session expiry, request acceptance, GraphQL errors, schema drift, pagination drift, and normalization defects.

## Diagnostic checkpoints

Saved artificial response shapes test the parser; deterministic ID fingerprints test pagination; content-free checkpoints test resumability; the public-tree scanner tests the publication boundary.

## Rejected routes

The one-off cookie script was not a maintainable architecture. Copying the fuller private pipeline was also rejected because it mixed reusable logic with credentials and real research data.

## Engineering result

The public package keeps stable records, explicit errors, page guards, provenance, and privacy-minimized checkpoints. Each claim is bounded by an offline test.

## Maintenance trigger

Change parser logic only when a minimized artificial fixture reproduces a new response shape. Investigate transport failures separately from parser behavior.

