---
name: list-rfcs
description: >-
  List all architecture RFCs and their status.
  Use when checking RFC pipeline, reviewing open proposals, or tracking architecture decisions.
disable-model-invocation: true
---

# List RFCs

List all architecture RFCs with their current status.

## Instructions

1. Search for RFC files (check all, merge results):
   - `docs/rfcs/*.md`
   - `docs/20-architecture/rfcs/*.md` (jd-docs convention)
   - `.arkhe/rfcs/*.md` (arkhe convention)
   - `arkhe/rfcs/*.md`
2. For each RFC found, extract from the file header:
   - **Number/Filename**: from the file path
   - **Title**: from the `# RFC: [Title]` heading (if non-standard, use the first `#` heading)
   - **Status**: from the `**Status**:` field (Draft, Review, Approved, Rejected, Superseded). If missing, show "Unknown"
   - **Author**: from the `**Author**:` field. If missing, show "—"
   - **Date**: from the `**Date**:` field. If missing, show "—"
3. If no RFCs are found, inform the user and suggest using the `create-rfc` skill to draft one

## Output Format

```markdown
# Architecture RFCs

| # | Title | Status | Author | Date |
|---|-------|--------|--------|------|
| 0001 | [Title] | Draft | [Author] | [Date] |

**Summary**: X total — Y Draft, Z Review, W Approved
```

Sort by number descending (newest first).
