---
name: spec-driven-development
description: Enforces strict Spec-Driven Development. Prevents direct coding and ensures spec → generate → review loops.
---

# Spec-Driven Development Rules

## Golden Rule
Never write or modify code directly.
All changes must originate from specifications.

## Mandatory Workflow
1. Analyze requirement
2. Write or update spec (Markdown)
3. Generate code via Claude Code
4. Review output
5. Refine spec if needed
6. Regenerate

## Required Spec Artifacts
Depending on feature scope:
- spec.md
- plan.md
- tasks.md
- checklist.md
- ADR (if architectural)

## Forbidden Actions
- Manual code patches
- Guessing requirements
- Skipping specification step

## Success Criteria
- Specs are the single source of truth
- Code exactly matches specs
