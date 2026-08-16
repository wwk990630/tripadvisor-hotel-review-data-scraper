# Evidence and limits

Verified on 2026-08-16:

- all four April 2026 private Python files parse successfully;
- the hotel table contains 3,248 rows and 3,248 unique hotel IDs;
- eleven cleaned review files contain 274 parseable rows;
- every cleaned file has unique review IDs within that hotel;
- eleven raw JSONL evidence files contain valid JSON records;
- the clean public tests and safety scanner run without network access.

These checks support the field mappings, pagination model, checkpoint design,
and error categories used here. They do not establish that an old request can
still be sent, that a current platform session will accept it, or that bulk
collection is permitted.

Evidence labels used by this project:

- `fixture verified`: synthetic payloads exercise a stable parser contract;
- `private evidence reviewed`: private results support a design choice without
  being redistributed;
- `upstream unverified`: no claim is made about current live behavior.
