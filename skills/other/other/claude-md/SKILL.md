---
name: claude-md
description: "Methodology for authoring and maintaining CLAUDE.md. Enforces brevity, relevance, and structure."
user-invocable: false
allowed-tools:
  - Read
  - Edit
  - Bash
  - Grep
  - Glob
hooks:
  Stop:
    - type: command
      command: "task claude:validate-skill -- --skill claude-md"
---

# CLAUDE.md Authoring

## Purpose

Methodology for editing CLAUDE.md that keeps it concise, high-signal, and structurally sound. The guide (patterns/anti-patterns in `skill.yaml`) is the primary value; the linter (`lint-claude-md.sh`) is a safety net for quantifiable rules.

## Quick Reference

- **Target:** <120 lines, 80% relevance per line
- **Structure:** Title, behavioral, "Built with:", dirs-only structure, auto-gen table, commands, conventions
- **Rule:** Reference material lives in `docs/` — CLAUDE.md links to it

```bash
task docs:lint-claude-md    # Validate CLAUDE.md structure
```

## Key Principle

Every line in CLAUDE.md must be useful in 80%+ of sessions. If it's reference material, move it to `docs/` and link. If Claude can discover it with tools, omit it.

## Automation

See `skill.yaml` for patterns, anti-patterns, and editing procedure.
See `collaboration.yaml` for boundaries with `docs-refresh`.
See `sharp-edges.yaml` for common pitfalls.
