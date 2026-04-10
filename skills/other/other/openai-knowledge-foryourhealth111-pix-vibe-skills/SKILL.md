---
name: openai-knowledge
description: Compatibility alias for OpenAI platform documentation guidance. Delegate to the canonical local `openai-docs` payload while preserving route compatibility.
---

# openai-knowledge (Compatibility Alias)

## Purpose

Provide a stable compatibility alias for callers that still request
`openai-knowledge`, while canonical OpenAI documentation guidance is maintained
under the sibling `openai-docs` skill directory.

This preserves:

- existing route compatibility for `openai-knowledge`
- `skills-lock` and catalog continuity for legacy callers
- a thin alias surface instead of duplicated docs guidance payload

## Resolution Order

1. Use the canonical local `openai-docs` skill payload first.
2. Reuse its canonical materials:
   - `../openai-docs/SKILL.md`
   - `../openai-docs/references/**`
   - `../openai-docs/scripts/**`
3. Keep this alias directory thin and free of duplicated heavy payload.

## Minimal Workflow

1. Read `../openai-docs/SKILL.md` for the full OpenAI docs workflow.
2. Use canonical references and scripts from `../openai-docs/`.
3. Report under `openai-knowledge` only when a caller explicitly requested this alias.
