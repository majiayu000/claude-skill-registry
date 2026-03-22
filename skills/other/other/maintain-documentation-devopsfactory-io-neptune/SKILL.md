---
name: maintain-documentation
description: Ensures human and AI documentation stay in sync with code and config. Use when changing behavior, adding features, refactoring, or when the user asks to update docs. Delegates the actual updates to the documentation-maintainer subagent.
---

# Maintain Documentation

## When to Use

Use this skill when:
- Changing user-facing behavior, CLI commands, or flags
- Adding or changing config or env vars
- Refactoring project structure or conventions
- Modifying CI or release workflows
- The user asks to update or review documentation

## What to Do

**Delegate documentation updates to the documentation-maintainer subagent** (`.cursor/agents/documentation-maintainer.md`).

When this skill applies, invoke the **documentation-maintainer** subagent with a prompt that describes what changed (e.g. code, config, CI, or structure) so it can run its full checklist and update README, docs/, examples/, AGENTS.md, .cursor/rules, .cursor/commands, and .cursor/skills as needed. The subagent owns the detailed checklist and the "where things live" / "when to update" mapping; do not duplicate that work—delegate it.
