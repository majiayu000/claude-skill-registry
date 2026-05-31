---
name: ralph-specum-index
description: This skill should be used only when the user explicitly asks to use `$ralph-specum-index`, or explicitly asks Ralph Specum in Codex to generate or refresh index artifacts.
metadata:
  surface: helper
  action: index
---

# Ralph Specum Index

Use this to generate searchable index specs for an existing codebase.

## Contract

- Index output lives under `specs/.index/`
- Use stable Ralph templates for `index.md`, component specs, and external specs
- Keep component and external entries deterministic and easy to diff

## Action

1. Parse the user scope such as path, types, excludes, quick mode, dry run, or force.
2. Scan the requested code areas for controllers, services, models, helpers, migrations, or comparable project structures.
3. Generate or update:
   - `specs/.index/index.md`
   - `specs/.index/components/*.md`
   - `specs/.index/external/*.md`
4. Keep outputs deterministic so start, research, and triage can reuse them.
5. Include external URLs, MCP endpoints, or installed skills only when the user asked for them or they are clearly relevant.
6. In dry run mode, report what would be created without writing files.

## Response Handoff

- After updating the index, name the files that changed and summarize the index scope briefly.
- End with exactly one explicit choice prompt:
  - `approve current artifact`
  - `request changes`
  - `continue to research`
- Treat `continue to research` as approval of the updated index artifacts.
