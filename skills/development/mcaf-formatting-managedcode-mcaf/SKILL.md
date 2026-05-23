---
name: mcaf-formatting
description: "Format code and keep style consistent using the repository’s canonical formatting/lint commands from `AGENTS.md`. Use after implementing changes or when formatting drift causes noisy diffs; keep formatting changes intentional and verified with build/tests."
compatibility: "Requires the repository’s formatter/linter tools; uses commands from AGENTS.md."
---

# MCAF: Formatting

## Outputs

- Formatted code changes (consistent with repo style)
- Evidence: formatting command(s) run and any follow-up build/tests

## Workflow

1. Use the canonical `format` command from `AGENTS.md` (do not invent commands).
2. Run the formatter on the smallest scope possible (if your tools allow it).
3. Review the diff:
   - ensure changes are formatting-only
   - if the formatter touched many files, separate the change or confirm it was explicitly requested
4. Verify (follow `AGENTS.md` for sequencing + required commands):
   - for formatting-only changes: run the smallest meaningful verification the repo requires (build/tests/analyze as applicable)
   - for formatting as part of a behaviour change: follow the repo’s normal order (don’t reorder the pipeline)
5. If `format`/linters are missing or flaky:
   - fix `AGENTS.md` to point to a real, repeatable command
   - only then rerun formatting
6. Report what was run and what changed.

## Guardrails

- Do not introduce unrelated refactors under the cover of formatting.
- Keep formatting changes and behaviour changes reviewable.
