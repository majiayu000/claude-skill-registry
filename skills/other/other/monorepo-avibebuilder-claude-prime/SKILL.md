---
name: monorepo
description: "Monorepo development patterns for pnpm workspaces and Turborepo. Use this skill when configuring workspaces, setting up task pipelines, managing cross-package dependencies, or optimizing CI/CD with remote caching. Covers package organization and shared design systems."
---

# Monorepo

pnpm workspaces + Turborepo for scalable monorepo development.

## Core Principles (Must Remember)

### Workspace Organization

1. **Split apps from packages** - Use `apps/` for deployables, `packages/` for shared libraries
2. **Namespace packages** - Prefix with `@org/` to avoid npm conflicts (e.g., `@acme/utils`)
3. **Single lockfile** - Never commit multiple lockfiles; `pnpm-lock.yaml` at root only
4. **No cross-package file access** - Never use `../` to reach into other packages; import via dependencies

### Dependency Management

5. **Use `workspace:*` protocol** - Always use `workspace:*` for internal package dependencies
6. **Hoist common devDependencies** - Shared tooling (TypeScript, ESLint) belongs in root
7. **Peer dependencies for frameworks** - React, Vue, etc. should be peers to avoid version conflicts
8. **Consider Catalogs (pnpm 9.5+)** - Centralize versions in `pnpm-workspace.yaml` for large repos

### Turborepo Tasks

9. **Use `^` for build dependencies** - `"dependsOn": ["^build"]` ensures correct topological order
10. **Always define `outputs`** - Without outputs, nothing gets cached
11. **Mark dev servers as persistent** - Use `"persistent": true, "cache": false` for long-running tasks
12. **Be explicit about environment** - List all build-affecting vars in `env` or `globalEnv`

### Caching

13. **Enable remote cache early** - Even solo devs benefit from shared CI/local cache
14. **Use `--summarize` for debugging** - Compare task summaries when cache misses unexpectedly
15. **Skip cache for fast tasks** - Tasks faster than network round-trip shouldn't use remote cache

## Anti-Patterns (Avoid)

- Cross-package imports via `../` paths (use proper dependency declarations)
- Missing `outputs` in turbo.json (breaks caching entirely)
- Using `latest` tag for dependencies (non-reproducible builds)
- Hardcoded paths in scripts (use workspace root variables)
- Running `pnpm install` with `--filter` expecting isolated install (single lockfile)
- Forgetting `persistent: true` on dev servers (causes task hangs)

## References

| Reference | Content |
|-----------|---------|
| [pnpm-workspace.md](./references/pnpm-workspace.md) | workspace.yaml, workspace: protocol, filtering, catalogs |
| [turborepo.md](./references/turborepo.md) | turbo.json schema, tasks, dependsOn, env vars |
| [caching.md](./references/caching.md) | outputs/inputs, remote cache setup, Vercel, self-hosted |
| [structure.md](./references/structure.md) | Directory layout, package naming, tsconfig sharing |
| [tailwind-v4.md](./references/tailwind-v4.md) | @source directives, shared theme package, CSS-first config |

## External Resources

- [pnpm Workspaces](https://pnpm.io/workspaces)
- [Turborepo Docs](https://turborepo.com/docs)
- [Configuring turbo.json](https://turborepo.com/docs/reference/configuration)
