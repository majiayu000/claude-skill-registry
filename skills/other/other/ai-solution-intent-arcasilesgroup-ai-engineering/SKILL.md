---
name: ai-solution-intent
description: "Use when maintaining the solution intent document: scaffolding new projects (init), surgical updates after architectural changes (sync), or completeness validation (validate)."
effort: high
argument-hint: "init|sync|validate"
tags: [documentation, architecture, governance]
---


# Solution Intent

## Purpose

Manage the solution intent document (`docs/solution-intent.md`) lifecycle. The solution intent defines the architectural decisions, technical design, and evolution roadmap of the project. Three modes ensure the document stays accurate, complete, and fresh.

## When to Use

- New project needs a solution intent document -> `init`
- Architectural changes were made (specs closed, stack changes, new agents/skills) -> `sync`
- Pre-release or periodic health check -> `validate`
- Automatically invoked by `/ai-pr` when staged changes include architecture files

## Process

1. **Detect mode** from arguments: `init`, `sync`, or `validate`
2. **Execute handler** -- follow the matching handler in `handlers/`
3. **Report** -- present summary of actions taken

## Quick Reference

```
/ai-solution-intent init       # scaffold from template
/ai-solution-intent sync       # update sections from project state
/ai-solution-intent validate   # completeness and freshness scorecard
```

## Integration

- **Called by**: `/ai-pr` (step 6.7) when architectural changes detected
- **Calls**: `handlers/init.md`, `handlers/sync.md`, `handlers/validate.md`
- **Reads**: `docs/solution-intent.md`, `.ai-engineering/manifest.yml`, `.ai-engineering/state/decision-store.json`

## Governance Notes

**Visual priority**: diagrams > tables > text. Every section MUST have at least one Mermaid diagram or table. Text accompanies but does not substitute visual representation.

**TBD policy**: if a section's data is not defined, implemented, or in scope, mark it explicitly as TBD. NEVER invent data.

**Writing**: use `/ai-write` patterns for document generation. The handler defines WHAT sections and data to gather; `/ai-write` defines HOW to write them.

**Ownership**: `docs/solution-intent.md` is project-managed. Sync updates data fields but never removes user-authored content. `ai-eng update` does not touch this file.

## References

- `.claude/skills/ai-pr/SKILL.md` -- PR workflow that triggers sync automatically
- `.claude/skills/ai-write/SKILL.md` -- documentation writing patterns
- `.ai-engineering/manifest.yml` -- governance surface counts, tooling, providers
$ARGUMENTS
