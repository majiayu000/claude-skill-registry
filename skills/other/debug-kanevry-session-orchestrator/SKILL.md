---
name: debug
description: "Use when encountering any bug, test failure, build break, or unexpected behavior — runs a 4-phase systematic debugging process before proposing any fix. Iron Law: NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST. Produces a `.orchestrator/debug/` artifact the fixer agent must reference."
metadata:
  model: inherit
  color: red
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Write
---

# debug

> **Portable mirror — generated, do not edit.** The canonical skill body lives at
> [`skills/debug/SKILL.md`](../../../skills/debug/SKILL.md); read that file for the full instructions.
> This mirror carries only agentskills.io-spec-legal frontmatter so harnesses that
> discover skills under `.agents/skills/` can find and route to the skill.
>
> Regenerate with `node scripts/generate-agents-skills.mjs`.
