---
name: autopilot
description: "Use this skill when running an autonomous session-orchestration loop. Chains session-start → session-plan → wave-executor → session-end for N iterations with all 10 kill-switches (SPIRAL, FAILED wave, carryover > 50%, max-hours, max-sessions, resource-overload, token-budget, stall-timeout, sub-threshold confidence, user-abort). Reads Mode-Selector output (Phase B) to decide auto-execute vs. fallback. Writes one autopilot.jsonl record per loop run. Phase C scaffold (issue #277); implementation lives in scripts/lib/autopilot.mjs (Phase C-1 follow-up)."
---

# autopilot

Canonical skill: `skills/autopilot/SKILL.md`

Read that file and follow it exactly. Resolve relative links against `skills/autopilot/`, not this wrapper.

Cursor has no Skill tool. Treat "invoke the autopilot skill" as: Read `skills/autopilot/SKILL.md`.
