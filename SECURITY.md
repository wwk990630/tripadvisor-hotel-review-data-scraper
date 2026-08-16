# Security and data boundary

This repository contains offline engineering experiments. It does not accept,
store, or require browser cookies, authorization headers, session identifiers,
proxy credentials, live query identifiers, or collected review datasets.

All committed response fixtures are synthetic. Real response files and
research outputs belong outside the public repository, even when the source
page is publicly visible.

Run the safety check before every commit:

```bash
python scripts/check_public_tree.py .
```

The scanner reports a rule, file, and line number without printing the matched
value. If you find credential material in Git history, rotate or revoke it,
preserve a local backup, and replace the affected public history.

Please report a potential exposure privately to wwk990630@gmail.com. Do not
open a public issue containing a credential or personal record.
