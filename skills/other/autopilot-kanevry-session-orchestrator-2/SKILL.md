---
name: autopilot
description: "Use this skill when running an autonomous session-orchestration loop. Chains session-start → session-plan → wave-executor → session-end for N iterations with all 10 kill-switches (SPIRAL, FAILED wave, carryover > 50%, max-hours, max-sessions, resource-overload, token-budget, stall-timeout, sub-threshold confidence, user-abort). Reads Mode-Selector output (Phase B) to decide auto-execute vs. fallback. Writes one autopilot.jsonl record per loop run. Phase C scaffold (issue #277); implementation lives in scripts/lib/autopilot.mjs (Phase C-1 follow-up)."
metadata:
  user-invocable: "true"
  tags: phase-c, autopilot, autonomous, loop
  model: sonnet
---

# autopilot

> **Portable mirror — generated, do not edit.** The canonical skill body lives at
> [`skills/autopilot/SKILL.md`](../../../skills/autopilot/SKILL.md); read that file for the full instructions.
> This mirror carries only agentskills.io-spec-legal frontmatter so harnesses that
> discover skills under `.agents/skills/` can find and route to the skill.
>
> Regenerate with `node scripts/generate-agents-skills.mjs`.
