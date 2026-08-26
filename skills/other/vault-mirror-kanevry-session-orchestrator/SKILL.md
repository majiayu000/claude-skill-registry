---
name: vault-mirror
description: "Use when you need to populate the Meta-Vault with machine-generated notes derived from session-orchestrator JSONL records. Converts entries from `.orchestrator/metrics/sessions.jsonl` and `.orchestrator/metrics/learnings.jsonl` into vault-conformant Markdown under `50-sessions/` and `40-learnings/`. Called automatically at session-end Phase 3.7 and after evolve Phase 3.5 — only when `vault-integration.enabled=true` and `vault-integration.mode != \"off\"`. Idempotent: re-runs safely; skips hand-authored notes. Triggers: \"mirror to vault\", \"sync session notes to vault\", \"write learning notes to vault\", \"vault-mirror failed at session close\". <example>Context: session-end is finalizing, vault-integration.mode is \"warn\". user: \"/close\" assistant: \"Running vault-mirror to write 50-sessions/session-2026-05-17.md from the closing session record — 1 created, 0 skipped.\"</example>"
disable-model-invocation: true
---

# vault-mirror

Canonical skill: `skills/vault-mirror/SKILL.md`

Read that file and follow it exactly. Resolve relative links against `skills/vault-mirror/`, not this wrapper.

Cursor has no Skill tool. Treat "invoke the vault-mirror skill" as: Read `skills/vault-mirror/SKILL.md`.
