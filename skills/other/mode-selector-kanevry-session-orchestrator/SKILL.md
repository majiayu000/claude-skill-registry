---
name: mode-selector
description: "Use this skill when performing deterministic mode selection for session-start. Reads Phase A STATE.md recommendations + (future) learnings, sessions, backlog, bootstrap signals and returns {mode, rationale, confidence, alternatives}. Pure-function contract — no side effects, no STATE.md writes. Phase B scaffold (issue #276); full heuristic is follow-up sub-issues."
metadata:
  model: haiku
  user-invocable: "false"
  tags: phase-b, autopilot, mode-selection, scaffold
---

# mode-selector

> **Portable mirror — generated, do not edit.** The canonical skill body lives at
> [`skills/mode-selector/SKILL.md`](../../../skills/mode-selector/SKILL.md); read that file for the full instructions.
> This mirror carries only agentskills.io-spec-legal frontmatter so harnesses that
> discover skills under `.agents/skills/` can find and route to the skill.
>
> Regenerate with `node scripts/generate-agents-skills.mjs`.
