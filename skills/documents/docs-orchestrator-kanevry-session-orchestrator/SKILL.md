---
name: docs-orchestrator
description: "Use this skill when orchestrating documentation generation and updates within a session. Maps session scope to audience-specific docs tasks (User / Dev / Vault), dispatches the docs-writer agent with source-grounded prompts, and reports coverage gaps to session-end. Gated on `docs-orchestrator.enabled: true` in Session Config. Zero overhead when disabled."
disable-model-invocation: true
---

# docs-orchestrator

Canonical skill: `skills/docs-orchestrator/SKILL.md`

Read that file and follow it exactly. Resolve relative links against `skills/docs-orchestrator/`, not this wrapper.

Cursor has no Skill tool. Treat "invoke the docs-orchestrator skill" as: Read `skills/docs-orchestrator/SKILL.md`.
