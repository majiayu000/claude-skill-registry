---
name: diagnose-clickhouse-errors
description: Diagnose ClickHouse query failures when the user provides a numeric error code, symbolic error name such as UNKNOWN_SETTING, or raw DB::Exception text and wants a cause and fix.
metadata:
  author: DataStoria
---

## Workflow

1. Extract the numeric error code from the error text (e.g. `Code: 60`).
2. Load `references/<code>.md` with `skill_resource` (e.g. `references/60.md`) and follow its workflow.
3. If `skill_resource` returns nothing, use the error message and your ClickHouse knowledge to provide a best-effort Cause / Fix / Example response.

## Response format

Always respond with exactly these sections (omit ## Example only when no corrected SQL is useful):

- **## Cause** — One short sentence explaining why the error occurred.
- **## Fix** — Bullet list of concrete steps or changes.
- **## Example** — A single fenced SQL block with the corrected query; omit if no example applies.

If the user message includes a line `Response language (BCP-47): …`, write **Cause**, **Fix**, and **Example** (including localized `##` headings) in that language. Keep SQL, numeric codes, setting names, and identifiers as in the error or reference material.

Keep answers brief and action-first. Do not repeat the raw error verbatim. Do not add extra headings.
