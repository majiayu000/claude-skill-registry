---
name: domain-model
description: Use when the user wants to stress-test a plan against the existing domain model and documented decisions. Grilling session that interviews the user one question at a time, sharpens fuzzy terminology inline, updates CONTEXT.md lazily, and offers ADRs sparingly under a 3-criteria gate. Reads docs/adr/ and CONTEXT.md if present.
disable-model-invocation: true
---

# domain-model

Canonical skill: `skills/domain-model/SKILL.md`

Read that file and follow it exactly. Resolve relative links against `skills/domain-model/`, not this wrapper.

Cursor has no Skill tool. Treat "invoke the domain-model skill" as: Read `skills/domain-model/SKILL.md`.
