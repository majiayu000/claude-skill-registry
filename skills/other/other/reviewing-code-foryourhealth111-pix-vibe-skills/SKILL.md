---
name: reviewing-code
description: Compatibility alias for legacy reviewing-code routes. Delegate to the canonical local `code-reviewer` payload while preserving route compatibility.
---

# reviewing-code (Compatibility Alias)

## Purpose

Provide a stable compatibility alias for callers that still route to
`reviewing-code`, while canonical review guidance and automation are maintained
under the sibling `code-reviewer` skill directory.

This preserves:

- existing route compatibility for `reviewing-code`
- `skills-lock` and catalog continuity for legacy callers
- a thin alias surface instead of duplicated review payload content

## Resolution Order

1. Use the canonical local `code-reviewer` skill payload first.
2. Reuse canonical supporting files:
   - `../code-reviewer/SKILL.md`
   - `../code-reviewer/references/**`
   - `../code-reviewer/scripts/**`
3. Keep this alias directory thin and free of duplicated heavy payload.

## Minimal Workflow

1. Read `../code-reviewer/SKILL.md` for the full review workflow and tooling.
2. Use canonical references and scripts from `../code-reviewer/`.
3. Report under `reviewing-code` only when a caller explicitly requested this alias.
