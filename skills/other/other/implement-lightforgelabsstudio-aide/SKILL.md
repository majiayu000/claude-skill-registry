---
name: implement
description: Execute a GitHub issue or spec end-to-end. Inline two-layer plan, code, verify.
---

# Implement

Execute a GitHub issue or spec. Read AGENTS.md if not in context.

## Inputs

Issue number (`gh issue view <n>`) or pasted spec text. If no spec exists, use `/design` first.

## Review-aware

Before starting: check if `<issue-slug>.findings.md` exists. If it does, read it and incorporate findings before proceeding.

## Before touching code

1. Confirm: Goal / Success Criteria / Scope. Ask if missing or ambiguous.
2. State which files you plan to read before reading them.
3. **Layer 1** — filter applicable constraints from AGENTS.md (≤8 bullets): which invariants, authoritative systems, and boundaries govern this task.
4. **Layer 2** — ordered steps with exit criteria: `[Step] → Exit: [how to verify]`. State this plan explicitly before writing any code.

## Implementation

- Follow patterns in AGENTS.md. Load Tier 2 refs only when the task requires them.
- Do not modify existing tests without explicit approval.
- Keep diffs small and single-purpose.

## After coding

- Verify each Layer 2 exit criterion is met.
- Run: `{{RUN_ALL_TESTS_COMMAND}}` and `{{LINT_COMMAND}}`
- Report: what changed, which criteria are satisfied, any gaps.
