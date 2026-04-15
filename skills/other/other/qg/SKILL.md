---
name: qg
description: Use after making changes to run the project's quality gates and report pass or fail for each relevant check.
argument-hint: [path]
---

Run the project's quality gates — format, lint (auto-fix), typecheck, tests, build — scoped to $ARGUMENTS when provided. Detect configured gates from the project; skip what isn't there.

## Report Format

| Gate      | Status    | Issues               |
| --------- | --------- | -------------------- |
| Format    | PASS/FAIL | — or N files changed |
| Lint      | PASS/FAIL | — or N errors        |
| Typecheck | PASS/FAIL | — or N errors        |
| Tests     | PASS/FAIL | N/M passed           |
| Build     | PASS/FAIL | — or error           |

On failure: top 3 issues as `file:line`. The caller needs actionable locations, not full error dumps.
