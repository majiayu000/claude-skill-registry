---
name: docs-refresh
description: Auto-generate skill reference docs and keep CLAUDE.md skills table in sync. Use when user says /docs-refresh.
user-invocable: true
allowed-tools:
  - Read
  - Bash
  - Glob
  - Grep
  - Edit
  - Write
hooks:
  Stop:
    - type: command
      command: "task claude:validate-skill -- --skill docs-refresh"
---

# Docs Refresh

## Purpose

Auto-generate `docs/skills/REFERENCE.md` from skill.yaml files and keep the CLAUDE.md skills table in sync between `<!-- SKILLS_TABLE_START -->` / `<!-- SKILLS_TABLE_END -->` markers.

## Quick Reference

```bash
task docs:refresh          # Generate REFERENCE.md + update CLAUDE.md table
task docs:refresh-check    # Verify docs are in sync (CI gate)
task claude:skills-reference  # Generate REFERENCE.md only
```

## Pipeline

1. `generate-skill-reference.sh` reads all `.claude/skills/*/skill.yaml` and writes `docs/skills/REFERENCE.md`
2. `update-claude-md.sh` reads skill.yaml files and updates the table between CLAUDE.md markers
3. `docs-refresh-check.sh` regenerates both to temp and diffs against committed versions

## When to Run

- After creating, renaming, or removing a skill
- After changing a skill's `description`, `kind`, or `when_to_use` in skill.yaml
- Before committing skill changes (Stop hook runs automatically)

## Automation

See `skill.yaml` for patterns, ownership, and anti-patterns.
See `sharp-edges.yaml` for common failure modes.
