---
name: monorepo-scaffold
description: "Convert single-app repos into a Turborepo monorepo using pnpm workspaces. Use when splitting apps into apps/ and shared code into packages/ with cached pipelines."
---

# Monorepo Scaffold

Convert a single-app repository into a Turborepo + pnpm workspace monorepo, without breaking builds or release flow.

## Purpose

- Standardize on `pnpm` workspaces + `turbo`
- Split runnable apps into `apps/`
- Move shared code and config into `packages/`
- Add reliable caching, fast CI, and clear ownership boundaries

## Target Structure

Use this shape unless the repo already has stronger constraints.

```text
.
├─ apps/
│  ├─ web/
│  ├─ mobile/
│  └─ api/
├─ packages/
│  ├─ shared/
│  ├─ ui-web/
│  ├─ ui-mobile/
│  └─ config/
├─ pnpm-workspace.yaml
├─ turbo.json
└─ package.json
```

## CLI Commands

Prefer explicit, reproducible commands.

```bash
# Workspace baseline
pnpm add -D turbo
pnpm install

# Optional: scaffold common layout quickly
pnpm dlx create-turbo@latest --package-manager pnpm

# Run tasks
pnpm turbo run build
pnpm turbo run dev --filter=web
pnpm turbo run test --continue
```

## Workflow

Follow this order. Keep diffs small and reversible.

1. Audit current scripts, build outputs, and deploy entrypoints.
2. Create `apps/` and `packages/` folders.
3. Move the existing app into `apps/<name>/` with minimal edits.
4. Add `pnpm-workspace.yaml` and include `apps/*` and `packages/*`.
5. Add root `turbo.json` with a small, strict pipeline.
6. Normalize scripts so each app/package exposes `build`, `dev`, `lint`, `test`, and `typecheck` when relevant.
7. Extract shared code into `packages/shared` and wire via workspace deps.
8. Extract shared config into `packages/config` and reference it explicitly.
9. Update CI to run `pnpm install` then `pnpm turbo run build lint test typecheck`.
10. Verify with targeted filters, then full pipeline.

## Verification Checklist

Do not trust the migration until all checks pass.

- `pnpm install` completes without hoist hacks
- `pnpm turbo run build` succeeds from repo root
- `pnpm turbo run dev --filter=<app>` starts the expected app
- Each app builds from a clean checkout
- Shared packages are consumed via `workspace:*` ranges
- Outputs are declared in `turbo.json` for cache hits
- CI runs from root and matches local commands

## References

- Setup guide: `skills/monorepo-scaffold/references/turborepo-setup.md`
- Migration checks: `skills/monorepo-scaffold/references/migration-checklist.md`

