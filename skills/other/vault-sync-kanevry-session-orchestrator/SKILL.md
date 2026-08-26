---
name: vault-sync
description: "Use when you need to validate the Meta-Vault's Markdown frontmatter and wiki-link integrity before closing a session or after vault edits. Runs as a hard gate at session-end Phase 1 — blocks close if any `.md` file fails the Zod frontmatter schema or has dangling `[[wiki-links]]`. Supports three modes: `hard` (blocks on errors), `warn` (reports without blocking), `off` (skip). Reads `vault-sync.*` from Session Config; respects per-vault exclude globs from `CLAUDE.md`. Triggers: \"vault validation failed at session close\", \"fix vault frontmatter errors\", \"check vault wiki-links\", \"why is session-end blocked by vault-sync\". <example>Context: session-end Phase 1 quality gate, vault-sync.enabled=true, vault-sync.mode=\"hard\". user: \"/close\" assistant: \"vault-sync found 2 frontmatter errors in vault/40-learnings/ml-notes.md — missing required `id` field. Fixing before close.\"</example>"
disable-model-invocation: true
---

# vault-sync

Canonical skill: `skills/vault-sync/SKILL.md`

Read that file and follow it exactly. Resolve relative links against `skills/vault-sync/`, not this wrapper.

Cursor has no Skill tool. Treat "invoke the vault-sync skill" as: Read `skills/vault-sync/SKILL.md`.
