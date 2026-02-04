---
name: treido-skillsmith
description: Skill-system maintainer for Treido. Use to create/merge/trim skills, enforce treido-* naming, and keep `.codex/skills` minimal and consistent.
---

# treido-skillsmith

Build and maintain Treido’s skill fleet as a small set of high-signal specialists.

## When to Apply

- Creating a new `treido-*` skill
- Consolidating overlapping skills
- Upgrading a skill to include `references/`, `templates/`, `rules/`, or `scripts/` (optional)
- Cleaning old skills and reducing bloat

## Non-Negotiables

- Treido-maintained skills must be `treido-*`
- Keep skill instructions knowledge-heavy (avoid command spam)
- Prefer progressive disclosure: short core rules in `SKILL.md`, details in `references/`
- Stable documentation belongs in `/docs/`

## Standard Skill Skeleton

Every `treido-*` skill should have:

1. Frontmatter: `name`, `description`
2. When to Apply / When NOT to Apply
3. Non-negotiables (links to `treido-rails` + SSOT docs)
4. Output template (predictable deliverable)
5. Minimal “violations” checklist
6. References section (to `/docs/` + key repo files)

## Cleanup Rules

- Delete vendor/third-party skills from `.codex/skills` once their content is materialized into `treido-*`
- Keep `.agents` out of the critical path (skills must not depend on junction targets)
