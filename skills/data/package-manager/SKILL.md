---
name: package-manager
description: >
  pnpm workspace rules for Liftera.
  Trigger: When adding dependencies, modifying workspace configuration, or troubleshooting installs/lockfile issues.
license: Apache-2.0
metadata:
  author: liftera
  version: "1.0"
  scope: [root]
  auto_invoke: "Adding/updating dependencies in the monorepo"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch, Task
---

## Workspace Rules (REQUIRED)

- **ALWAYS** keep workspace boundaries defined by `pnpm-workspace.yaml`.
- **ALWAYS** add dependencies to the narrowest scope that needs them:
  - app deps in `apps/*/package.json`
  - package deps in `packages/*/package.json`
  - tooling-only deps in root `package.json`

## Installing Dependencies (REQUIRED)

- **ALWAYS** use `pnpm` (repo is configured with `packageManager: pnpm@9.0.0`).
- **NEVER** use `npm install` or `yarn` in this repository.

## Lockfile & Consistency

- **ALWAYS** commit `pnpm-lock.yaml` when dependencies change.
- **NEVER** hand-edit the lockfile.

## Filtering & Commands

- **ALWAYS** use pnpm filters for app-specific work.
- Prefer:
  - `pnpm dev --filter=web`
  - `pnpm dev --filter=mobile`
