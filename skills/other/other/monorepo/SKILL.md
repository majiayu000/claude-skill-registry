---
name: monorepo
description: "MUST use for ANY query mentioning packages, monorepo, workspace, catalog, turbo, turborepo, or pnpm in a multi-package context. MUST use when sharing config (ESLint, tsconfig, prettier) across packages, fixing build order between packages, adding new packages, scoping CI installs/caching to changed packages, or debugging pnpm catalog version resolution. This skill OWNS all cross-package coordination problems — even when they look like build, CI, config, or dependency issues. If two or more packages interact in the query, this skill applies. Takes priority over other skills when the problem spans package boundaries."
---

# Monorepo

Project-specific patterns for pnpm workspaces + Turborepo.

## Architecture Decisions

### Workspace Organization
1. **Split apps from packages** — `apps/` for deployables, `packages/` for shared libraries.
2. **Namespace packages** — Prefix with `@org/` to avoid npm conflicts.
3. **Single lockfile** — `pnpm-lock.yaml` at root only. Never commit multiple lockfiles.
4. **No cross-package file access** — Never use `../` to reach into other packages; import via dependencies.

### Dependency Management
5. **Use `workspace:*` protocol** — Always for internal package dependencies.
6. **Hoist common devDependencies** — Shared tooling (TypeScript, ESLint) in root.
7. **Peer dependencies for frameworks** — React, Vue, etc. as peers to avoid version conflicts.
8. **Consider Catalogs (pnpm 9.5+)** — Centralize versions in `pnpm-workspace.yaml` for large repos.

### Turborepo Tasks
9. **Use `^` for build dependencies** — `"dependsOn": ["^build"]` for topological order.
10. **Always define `outputs`** — Without outputs, nothing gets cached.
11. **Mark dev servers as persistent** — `"persistent": true, "cache": false`.
12. **Be explicit about environment** — List all build-affecting vars in `env` or `globalEnv`.

## Gotchas

- Missing `outputs` in turbo.json silently disables caching for that task. The task runs every time and you won't get an error — just slow builds. Always verify outputs are configured.
- `pnpm install` does NOT respect `--filter` for installation — it always installs the entire workspace. Filtering only works for `pnpm run` and `pnpm exec`.
- `workspace:*` resolves to the CURRENT version of the local package, not "latest from npm". If the package has `"version": "0.0.0"`, published packages will have `"dependency": "0.0.0"` — set meaningful versions before publishing.
- Turborepo's `env` field in turbo.json uses GLOB patterns, not exact matches. `"env": ["API_*"]` captures `API_KEY`, `API_URL`, etc. Forgetting this causes over-invalidation.
- `turbo run build --filter=app-a` builds app-a AND all its workspace dependencies. If a dependency fails, app-a won't build. Check transitive deps.
- Adding a package to `packages/` requires running `pnpm install` before the workspace recognizes it. The new package also needs a valid `package.json` with `name` matching the workspace pattern.
- TypeScript project references (`references` in tsconfig.json) must match the workspace dependency graph. Mismatches cause type errors that only appear during `tsc --build`, not in IDE.
- `turbo.json`'s `globalDependencies` invalidates ALL tasks when listed files change. Don't put frequently-changed files here — use task-level `inputs` instead.
- Shared Tailwind configs need `@source` directives pointing to consuming packages' source directories, otherwise classes used in shared packages are purged.
- `pnpm deploy` (for production) copies a single package and its dependencies to a target directory. It does NOT run build scripts — build first, then deploy.
- Remote cache (Vercel or self-hosted) requires `outputs` to be correct. If outputs are wrong, cached artifacts will be incomplete and downstream tasks break silently.
- `persistent: true` tasks prevent `turbo run` from exiting. Don't include persistent tasks in CI pipelines unless they have a timeout.

## References

| When you need... | Read |
|------------------|------|
| workspace.yaml, workspace: protocol, filtering | [pnpm-workspace.md](./references/pnpm-workspace.md) |
| turbo.json schema, tasks, dependsOn | [turborepo.md](./references/turborepo.md) |
| Cache outputs/inputs, remote cache setup | [caching.md](./references/caching.md) |
| Directory layout, package naming, tsconfig | [structure.md](./references/structure.md) |
| Tailwind v4 shared theme package | [tailwind-v4.md](./references/tailwind-v4.md) |

## External Resources

- [pnpm Workspaces](https://pnpm.io/workspaces)
- [Turborepo Docs](https://turborepo.com/docs)
- [Configuring turbo.json](https://turborepo.com/docs/reference/configuration)
