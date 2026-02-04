---
name: liftera-architecture
description: >
  Liftera monorepo architecture patterns and best practices.
  Trigger: When making cross-app changes, adding new packages/apps, or deciding where code should live in the monorepo.
license: Apache-2.0
metadata:
  author: liftera
  version: "1.0"
  scope: [root]
  auto_invoke: "General Liftera development questions"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch, Task
---

## Monorepo Boundaries (REQUIRED)

- **ALWAYS** keep application code inside `apps/*`.
- **ALWAYS** keep reusable code inside `packages/*`.
- **NEVER** import app code from another app (e.g. `apps/web` importing from `apps/mobile`). Extract shared logic into a package.

## Package Design (REQUIRED)

- **ALWAYS** design packages as platform-agnostic when possible.
- **ALWAYS** expose stable entrypoints from each package (avoid deep imports across packages).
- **NEVER** duplicate shared UI or utilities across apps; add/extend a package instead.

## Cross-Platform UI Rules (REQUIRED)

- **ALWAYS** prefer shared UI in `packages/ui`.
- **ALWAYS** keep platform-specific implementations behind explicit entrypoints (e.g. `*.native.tsx`, `*.web.tsx`) when needed.
- **NEVER** assume DOM APIs exist in mobile code.

## Dependency & Ownership Rules

- **ALWAYS** keep dependencies as low as possible in packages.
- **ALWAYS** add dependencies at the narrowest scope that needs them (package/app `package.json`, not the root).
- **NEVER** add a dependency to the root unless it is truly repo-wide tooling.

## Repo Structure Quick Reference

- `apps/web`: Next.js app
- `apps/mobile`: Expo app
- `packages/ui`: shared UI (Gluestack UI + shared components)
- `turbo.json`: task orchestration
- `pnpm-workspace.yaml`: workspace boundaries
