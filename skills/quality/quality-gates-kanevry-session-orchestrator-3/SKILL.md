---
name: quality-gates
description: Use this skill when referencing canonical quality check commands for typecheck, test, and lint. Defines 4 variants (Baseline, Incremental, Full Gate, Per-File) used by session-start, wave-executor, session-end, and session-reviewer. Reference skill — not invoked directly.
metadata:
  user-invocable: "false"
  tags: reference, quality, typecheck, test, lint
  model: haiku
  model-preference: sonnet
  model-preference-codex: gpt-5.4-mini
  model-preference-cursor: claude-sonnet-4-6
---

# quality-gates

> **Portable mirror — generated, do not edit.** The canonical skill body lives at
> [`skills/quality-gates/SKILL.md`](../../../skills/quality-gates/SKILL.md); read that file for the full instructions.
> This mirror carries only agentskills.io-spec-legal frontmatter so harnesses that
> discover skills under `.agents/skills/` can find and route to the skill.
>
> Regenerate with `node scripts/generate-agents-skills.mjs`.
