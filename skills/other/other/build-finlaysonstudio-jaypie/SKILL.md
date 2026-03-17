---
name: build
description: Build commands, CI/CD workflows, branching strategy, npm publishing
---

# Build

How to build, deploy, and publish in this monorepo.

## Local Build

```bash
npm run build                              # Build all packages (core deps first)
npm run build -w packages/<name>           # Build a specific package
npm run build -w workspaces/<name>         # Build a specific workspace
npm run build:core-deps                    # Build types, errors, fabric (dependency order)
npm run clean                              # Remove all dist/ directories
```

Build order matters: `types` -> `errors` -> `fabric` -> everything else. The top-level `npm run build` handles this automatically via `build:core-deps`.

## Typecheck and Lint

```bash
npm run typecheck                          # Typecheck all workspaces
npm run typecheck -w packages/<name>       # Typecheck a specific package
npm run lint                               # Lint everything (quiet mode)
npm run format                             # Auto-fix lint + sort package.json
```

## CI/CD Workflows

### NPM Check (`npm-check.yml`)

Runs on pushes to feature branches. Validates code quality before merge.

| Trigger | Branches/Tags |
|---------|---------------|
| Push | `branch/*`, `claude/*`, `codex/*`, `devin/*`, `fix/*`, `feat/*` |
| Tag | `check-*` |

Jobs (all parallel):
- **Lint**: Node 24, `npm run lint`
- **Typecheck**: Node 24, `npm run typecheck` (continue-on-error)
- **Unit Test**: Matrix [Node 22, 24, 25], `npm test` with optional Datadog tracing
- **LLM Client Test**: Conditional, only when `packages/llm/**` changes

### NPM Deploy (`npm-deploy.yml`)

Publishes packages to npm. Skips already-published versions automatically.

| Trigger | Effect |
|---------|--------|
| Push to `main` | Publish stable versions |
| Tag `deploy-*` | Publish stable versions |
| Tag `dev-*` | Publish with `--tag dev` (only `-dev.N` versions) |
| Tag `rc-*` | Publish with `--tag rc` (only `-rc.N` versions) |

### Stack Deployments

CDK infrastructure deploys via separate workflows:

| Workflow | Trigger | Environment |
|----------|---------|-------------|
| `deploy-env-sandbox.yml` | `branch/*`, `claude/*`, `feat/*`, `fix/*`, `sandbox/*` branches; `sandbox-*` tags; only `workspaces/**` path changes | sandbox |
| `deploy-env-development.yml` | `main` branch, `development/*` branches, `development-*` tags; only `workspaces/**` path changes | development |
| `deploy-env-production.yml` | `production-*` tags, `v0.*`/`v1.*` tags | production |
| `deploy-stacks.yml` | Manual (`workflow_dispatch`) | sandbox/development/production |
| `deploy-stack-documentation.yml` | `main`/`feat/*`/`sandbox/*` branches when `workspaces/documentation/**` changes; `stack-documentation-*`/`sandbox-*` tags; manual | sandbox/development/production |

## Branching Strategy

| Branch Pattern | Purpose | Triggers |
|---------------|---------|----------|
| `main` | Stable releases | npm-deploy, stack deploy to development |
| `feat/*` | Feature development | npm-check, stack deploy to sandbox |
| `fix/*` | Bug fixes | npm-check, stack deploy to sandbox |
| `branch/*` | General work | npm-check, stack deploy to sandbox |
| `claude/*` | AI agent work | npm-check, stack deploy to sandbox |
| `codex/*` | AI agent work | npm-check |
| `devin/*` | AI agent work | npm-check |
| `sandbox/*` | Sandbox testing | stack deploy to sandbox |
| `development/*` | Development testing | stack deploy to development |

## Tags

| Tag Pattern | Purpose |
|-------------|---------|
| `check-*` | Trigger npm-check manually |
| `deploy-*` | Trigger npm publish (stable) |
| `dev-*` | Publish with `dev` dist-tag |
| `rc-*` | Publish with `rc` dist-tag |
| `sandbox-*` | Deploy stacks to sandbox |
| `development-*` | Deploy stacks to development |
| `production-*` | Deploy stacks to production |
| `v0.*`, `v1.*` | Deploy stacks to production |
| `stack-documentation-*` | Deploy documentation stack only |

## Publishing Packages

Packages publish automatically when merged to `main`. The workflow:

1. Iterates over all `packages/*/`
2. Skips `private: true` packages
3. Compares local version to npm registry
4. Publishes only if version is new (with `--provenance`)

To publish a pre-release:
1. Bump version to include `-rc.0` or `-dev.0` suffix
2. Run `npm i --package-lock-only`
3. Push a tag: `git tag rc-description && git push origin rc-description`

## Completion Criteria

See `.claude/skills/green/SKILL.md`.
