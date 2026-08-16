# Architecture

The public project separates durable facts from transient network context.

```text
synthetic response fixture
        |
        +--> response checkpoint --> explicit error type
        |
        +--> parser --> ReviewRecord + Provenance
                         |
                         +--> PageGuard --> new records
                                          + checkpoint state

repository tree --> safety scanner --> publish decision
```

`parser.py` accepts only documented response envelopes and returns normalized
records. It never exports reviewer-profile subtrees. `pagination.py` tracks
record IDs and ordered-page fingerprints separately, allowing overlap to be
deduplicated without confusing it with a repeated page. `checkpoint.py` stores
only property IDs, offsets, review IDs, page hashes, and a timestamp.

There is no writer or target-site client in the public architecture. That is a
deliberate boundary: an offline parser can be reproduced without pretending
that an old browser session or live query remains valid.
