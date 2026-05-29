---
name: loom-docs-merge-conflicts
description: Resolve git merge conflicts in compound-managed LOOM docs (LOOM_CHANGELOG.md, LOOM_ROADMAP.md) without breaking BEGIN/END fences.
license: MIT
compatibility: opencode,claude
metadata:
  created_at: "2026-01-30T02:25:30.057Z"
  updated_at: "2026-01-30T02:25:30.057Z"
  version: "1"
---
<!-- BEGIN:compound:skill-managed -->
# Purpose
Resolve merge conflicts in compound-managed LOOM docs without breaking compound fences.

# When To Use
- You see `<<<<<<<`, `=======`, or `>>>>>>>` in `LOOM_CHANGELOG.md` or `LOOM_ROADMAP.md`.
- A merge/rebase touched compound-managed blocks and left conflicts.

# Procedure
- Open the conflicted file and locate every conflict hunk.
- Preserve the compound fences exactly:
  - Keep `<!-- BEGIN:compound:... -->` and `<!-- END:compound:... -->` lines unchanged.
  - Do not duplicate or reorder fence lines.
- For conflicted list entries inside fences:
  - Prefer keeping both sides' entries, then dedupe exact duplicates.
  - Maintain consistent bullet formatting: `- <timestamp> <note>`.
  - Keep ordering stable (typically newest-first if the file already uses that pattern).
- Remove all conflict marker lines (`<<<<<<<`, `=======`, `>>>>>>>`) after selecting the final content.
- Sanity check:
  - No conflict markers remain.
  - Markdown renders as a single list (no nested accidental `- -` unless the file intentionally uses it).
  - The file contains exactly one BEGIN and one END for each compound block.
- Run docs sync to refresh derived indexes/managed blocks (so downstream agents don’t learn from broken docs).
<!-- END:compound:skill-managed -->

## Manual notes

_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._
