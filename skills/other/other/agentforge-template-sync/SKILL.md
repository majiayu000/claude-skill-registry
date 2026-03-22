---
name: agentforge-template-sync
description: Keep template-backed files aligned across canonical template, dist template, and local convex copies.
version: 1.0.0
metadata:
  author: agentforge
---

# AgentForge Template Sync

Use this skill when changing scaffolded template files or anything under the synchronized Convex template set.

## Rules

- `packages/cli/templates/default/convex/` is the canonical source.
- Matching files must remain aligned in:
  - `packages/cli/dist/default/convex/`
  - `templates/default/convex/`
  - `convex/`
- Run `pnpm sync-templates` after template changes.

## Do not forget

- generated files may exist, but hand-edited source of truth still matters,
- tests and docs should reflect the template behavior users actually scaffold.
