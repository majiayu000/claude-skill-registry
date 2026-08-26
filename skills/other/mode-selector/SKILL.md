---
name: mode-selector
description: "Use this skill when performing deterministic mode selection for session-start. Reads Phase A STATE.md recommendations + (future) learnings, sessions, backlog, bootstrap signals and returns {mode, rationale, confidence, alternatives}. Pure-function contract — no side effects, no STATE.md writes. Phase B scaffold (issue #276); full heuristic is follow-up sub-issues."
disable-model-invocation: true
---

# mode-selector

Canonical skill: `skills/mode-selector/SKILL.md`

Read that file and follow it exactly. Resolve relative links against `skills/mode-selector/`, not this wrapper.

Cursor has no Skill tool. Treat "invoke the mode-selector skill" as: Read `skills/mode-selector/SKILL.md`.
