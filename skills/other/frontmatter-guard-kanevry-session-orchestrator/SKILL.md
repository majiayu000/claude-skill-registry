---
name: frontmatter-guard
description: "Injects the canonical vault frontmatter schema snippet into agent prompts before any vault-write task, preventing malformed YAML frontmatter in Obsidian notes. <example>Context: wave-executor is about to dispatch a vault-mirror agent that writes learning notes under ~/Projects/vault/40-learnings/. user: \"dispatch vault-write agent\" assistant: \"Injecting frontmatter-guard snippet into agent prompt (vault scope detected). Required fields: id, type, created, updated. Enum type: note|daily|project|person|reference|idea|learning|session.\" <commentary>The wave-executor pre-dispatch hook calls detectVaultTaskScope() — the fileScope contains /Projects/vault/40-learnings/ so the guard triggers and the snippet is prepended to the agent system prompt.</commentary></example>"
disable-model-invocation: true
---

# frontmatter-guard

Canonical skill: `skills/frontmatter-guard/SKILL.md`

Read that file and follow it exactly. Resolve relative links against `skills/frontmatter-guard/`, not this wrapper.

Cursor has no Skill tool. Treat "invoke the frontmatter-guard skill" as: Read `skills/frontmatter-guard/SKILL.md`.
