---
name: daily
description: "Use this skill when creating today's daily note in the Meta-Vault (03-daily/YYYY-MM-DD.md) with valid vaultFrontmatterSchema-compliant YAML frontmatter. Idempotent: re-running on the same day opens the existing note instead of overwriting. Use when starting a work day, capturing scratch notes, or bootstrapping the inbox flow."
---

# daily

Canonical skill: `skills/daily/SKILL.md`

Read that file and follow it exactly. Resolve relative links against `skills/daily/`, not this wrapper.

Cursor has no Skill tool. Treat "invoke the daily skill" as: Read `skills/daily/SKILL.md`.
