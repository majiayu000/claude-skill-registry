---
name: robotframework-results
description: Parse Robot Framework output.xml results into JSON summaries, detailed suite/test breakdowns, tag and criticality stats, execution errors, failed test messages, keyword-level errors, and timing. Use when asked to read/merge output.xml, compute pass/fail counts, tag stats, criticality, error messages, elapsed time, slowest tests/keywords, or combine/merge multiple outputs via rebot.
---

# Robot Framework Results

Use the bundled script to read Robot Framework `output.xml` and return JSON. It supports:
- summary totals
- detailed suite/test breakdowns
- tag statistics and criticality grouping
- execution errors, failed test messages, and keyword-level errors
- timing (keyword timing is opt-in)
- single or multiple outputs (merge or combine with rebot)

## Quick start

Single file summary:

```bash
python scripts/rf_results.py --output output.xml --sections summary
```

Multiple outputs, merged (`--merge` replaces earlier results when tests overlap):

```bash
python scripts/rf_results.py --outputs out1.xml out2.xml --merge --sections summary,details
```

Multiple outputs, combined under a new top-level suite (no `--merge`):

```bash
python scripts/rf_results.py --outputs out1.xml out2.xml --name Combined --sections summary
```

Include keyword timing in timing output:

```bash
python scripts/rf_results.py --output output.xml --sections timing --include-keyword-timing
```

## Output sections

- `summary`: totals, suite/test counts, overall status
- `details`: suites, tests, failed tests, tag stats, criticality stats
- `errors`: execution errors, failed test messages, keyword errors
- `timing`: totals and slowest tests; keyword timing requires `--include-keyword-timing`

## Notes

- Criticality grouping: prefer `test.critical` when available; otherwise infer from tags `critical`, `noncritical`, or `non-critical`. If neither is set, group as `unspecified`.
- For multiple outputs, use `--merge` to mirror `rebot --merge` behavior. Without `--merge`, rebot combines outputs under a new top-level suite (name via `--name`).
- JSON output is written to stdout. Use `--pretty` for indented JSON.
