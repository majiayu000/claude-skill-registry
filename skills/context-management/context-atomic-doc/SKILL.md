---
name: context:atomic-doc
description: Create/update atomic documentation (blocks, foundations, stacks). Use when user asks to "create atomic doc", "add a block", "add a foundation", "setup a stack", or needs to document reusable knowledge. Creates files in context/ following SWEBOK-aligned structure.
---

# Atomic Documentation

Create or update context documentation following the atomic documentation system.

## Execution Instructions

When this skill is invoked:

**MANDATORY FIRST STEP:** Use the Read tool to read `context/workflows/manage-atomic-doc.md` (relative to project root). DO NOT proceed without reading this file first - it contains the complete workflow including Phase 0 (index check) that you MUST follow.

After reading the workflow file:

1. Parse `$ARGUMENTS`:
   - `create <layer>/<domain>/<name>` → new doc
   - `update <path>` → modify existing
   - No args → ask user what they want to create/update

2. Follow ALL phases in the workflow file, starting with Phase 0.

## Quick Reference

| Layer | Purpose | Examples |
|-------|---------|----------|
| `blocks` | Single units of knowledge (tool-centric) | bun.md, eslint.md, vitest.md |
| `foundations` | Capabilities (combines blocks) | exec-tsx.md, test-unit-vitest.md |
| `stacks` | Complete project setups | cli-bun.md, api-pnpm-fastify.md |

| Domain | SWEBOK Area | What It Covers |
|--------|-------------|----------------|
| `construct` | Software Construction | Build, bundle, package |
| `test` | Software Testing | Unit, E2E, coverage |
| `quality` | Software Quality | Lint, format, style |
| `security` | Software Security | Auth, secrets, hardening |
| `scm` | Config Management | Version, release, publish |
| `ops` | SE Operations | CI/CD, deploy, infra |
| `observe` | Operations (sub-area) | Log, trace, metrics |
| `docs` | Architecture & Design | ADRs, diagrams, prompting |

## Usage

```
/context:atomic-doc create blocks/test/playwright.md
/context:atomic-doc create foundations/construct/bundle-web-esbuild.md
/context:atomic-doc update context/blocks/construct/bun.md
```

## References

- **Full workflow:** @context/workflows/manage-atomic-doc.md
- **Philosophy & naming:** @context/blocks/docs/atomic-documentation.md
- **Maintenance patterns:** @context/blocks/docs/maintenance.md
- **Index of all docs:** @context/README.md
