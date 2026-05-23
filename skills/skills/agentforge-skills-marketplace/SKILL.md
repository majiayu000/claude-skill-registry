---
name: agentforge-skills-marketplace
description: Work on skill discovery, parsing, registry behavior, install flows, and marketplace UI/data paths in AgentForge.
version: 1.0.0
metadata:
  author: agentforge
---

# AgentForge Skills Marketplace

Use this skill for skill system work across core, CLI, Convex, and dashboard.

## Primary surfaces

- `packages/core/src/skills/`
- `packages/cli/src/commands/skill.ts`
- `packages/cli/src/commands/skills.ts`
- Convex `skills` and `skillMarketplace` functions
- dashboard skills pages

## Rules

- `SKILL.md` is the contract. Parsing behavior matters.
- Keep install and discovery behavior consistent across local, GitHub, and marketplace sources.
- Check both project skills paths and global skill flows before changing command behavior.
