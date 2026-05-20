---
name: nean-scaffold
description: Scaffold an Nx monorepo with NestJS API, Angular frontend, and shared libraries.
argument-hint: "[app-name] [--github] [--public] [--org <org>] [--repo <n>] [--no-push]"
allowed-tools: Bash, Write, Read, Glob, Grep
---

## Purpose
Create a fully working NEAN repo (NestJS + Angular + Nx + TypeORM + PrimeNG) with tooling configured and runnable immediately.

## Arguments
- `app-name` — Project folder name (default: "app")
- `--github` — Create GitHub repo and push (requires `gh auth`)
- `--public` — Make GitHub repo public (default: private)
- `--org <n>` — Create under org instead of personal account
- `--repo <n>` — Override repo name (default: app-name)
- `--no-push` — Create repo and commit but don't push

## Template-first rule
Copy files from `templates/` into the project. If a template doesn't exist, generate equivalent content.

Templates provide:
- Root configs (nx.json, tsconfig, eslint, prettier, CI)
- API utilities (exception filters, validation pipes, response helpers)
- Shared types structure
- Database module with TypeORM config
- Docker configuration
- CLAUDE.md for the new repo
- VS Code workspace settings and extension recommendations

## What gets created

```
<app-name>/
├── apps/
│   ├── api/                      # NestJS backend
│   │   └── src/
│   │       ├── app/              # Root module
│   │       ├── modules/health/   # Health check endpoint
│   │       └── main.ts           # Bootstrap with security
│   └── web/                      # Angular frontend
│       └── src/
│           ├── app/              # Root component
│           └── main.ts           # Bootstrap
├── libs/
│   ├── shared/types/             # DTOs, interfaces, enums
│   ├── api/common/               # Filters, pipes, interceptors
│   └── api/database/             # TypeORM config, entities
├── docs/                         # Documentation
│   └── PRD-TEMPLATE.md           # Product requirements template for Ralph
├── docker/
│   ├── Dockerfile.api
│   ├── Dockerfile.web
│   └── docker-compose.yml
├── .vscode/                      # VS Code workspace config (from templates)
│   ├── settings.json
│   └── extensions.json
├── .github/
│   ├── workflows/
│   │   ├── ci.yml                  # CI pipeline
│   │   ├── security.yml            # Dependency review + TruffleHog
│   │   └── pr-check.yml            # PR validation
│   ├── CODEOWNERS                  # Code ownership rules
│   ├── SECURITY.md                 # Vulnerability reporting
│   ├── dependabot.yml              # Dependency updates
│   └── pull_request_template.md    # PR checklist
├── CLAUDE.md                     # Repo context for Claude Code
├── nx.json
├── package.json
└── tsconfig.base.json
```

## Scaffold steps
1. Create Nx workspace from parent dir (creates subdirectory): `npx create-nx-workspace@latest <app-name> --preset=apps --nxCloud=skip --interactive=false --skipGit --packageManager=npm`
1a. Copy VS Code config from templates: `.vscode/settings.json` and `.vscode/extensions.json`
2. Install Nx plugins: `npm install -D @nx/nest @nx/angular @nx/js`
3. Add NestJS: `npx nx g @nx/nest:application apps/api --e2eTestRunner=none`
   > The NestJS generator does NOT create jest config. Add API test infrastructure manually after generation (see step 3a).
3a. Add API test infrastructure (NestJS generator omits this):
   - `apps/api/jest.config.cts` — copy pattern from `libs/shared/types/jest.config.cts`, change `displayName`, adjust `preset` path to `../../jest.preset.js`, add `moduleNameMapper` for all `@<app-name>/*` aliases
   - `apps/api/.spec.swcrc` — copy verbatim from `libs/shared/types/.spec.swcrc` (enables decorator metadata for NestJS DI)
   - `apps/api/tsconfig.spec.json` — standard Nx spec tsconfig with `jest` + `node` types, referencing `tsconfig.app.json`
   - `apps/api/tsconfig.json` — add `{ "path": "./tsconfig.spec.json" }` to references array
4. Add Angular: `NX_IGNORE_UNSUPPORTED_TS_SETUP=true npx nx g @nx/angular:application apps/web --style=scss --routing --e2eTestRunner=playwright --prefix=app`
   > Set `NX_IGNORE_UNSUPPORTED_TS_SETUP=true` before running Angular generators when Nx uses TypeScript project references.
5. Override Angular tsconfig: Set `composite: false`, `declaration: false`, `declarationMap: false`, `isolatedModules: false` in `apps/web/tsconfig.json` and add `"dom"` to `lib`. Angular's compiler is incompatible with TypeScript project references settings.
6. Add shared libraries from templates
7. Configure TypeORM and database module
8. Add PrimeNG 21+ and Tailwind CSS v4 to Angular:
   - Create `apps/web/postcss.config.js` with `@tailwindcss/postcss` plugin
   - Create `apps/web/src/styles.css` with `@import "tailwindcss"` (NOT in .scss)
   - Update `apps/web/src/styles.scss` for primeicons only (`@use "primeicons/primeicons.css"`)
   - Add both `styles.scss` and `styles.css` to project.json styles array
   - Configure `providePrimeNG({ theme: { preset: Aura } })` in `app.config.ts`
9. Copy server utilities from templates
10. Configure webpack resolve aliases in `apps/api/webpack.config.js` for all `@<app-name>/*` path mappings. Required because Nx 22 project references don't auto-resolve tsconfig paths for webpack builds.
11. Create docs/ folder from templates (PRD template for Ralph)
12. Set up Docker configuration
    > For local development, Homebrew-managed PostgreSQL (`brew services start postgresql@14`) is simpler than Docker. The docker-compose.yml is for CI and production deployment.
13. Create `.github/` config files (CODEOWNERS, SECURITY.md, dependabot.yml, PR template, workflows)
14. Clean up generator artifacts after Nx generators run
15. Run quality gates until all pass

## Quality gates (must pass before done)
```bash
npm install
npm run lint
npm run test
npm run build
npm run e2e
```

## Teardown after E2E / smoke tests

If the dev server ran against a live database (TypeORM `synchronize: true` creates tables automatically), clean up afterward:

1. **Stop the dev server** — kill the `nx serve` process
2. **Drop smoke-test tables** — `psql -U postgres -d <db> -c 'DROP TABLE IF EXISTS <table>;'`
3. **Verify clean state** — `psql -U postgres -d <db> -c '\dt'` should show only pre-existing tables (e.g. `migrations`)
4. **Confirm port is free** — `lsof -i :3000` should return nothing

This prevents leftover tables from interfering with future migration-based workflows.

## GitHub setup (if --github)
- Requires `gh auth status` to succeed
- Creates repo: `gh repo create <owner>/<repo> --<visibility> --source . --remote origin`
- Commits and pushes unless `--no-push`

## Post-scaffold: GitHub security (recommended)

After scaffolding, run these skills to complete GitHub security setup:

1. **`/github-hooks --platform nean`** — Install local Git hooks
   - Husky + lint-staged for pre-commit validation
   - Commit message enforcement (conventional commits)
   - Secret scanning (gitleaks)
   - Pre-push test runs

2. **`/github-secure`** (if `--github` was used) — Configure repo security via API
   - Branch protection rules
   - Dependabot alerts & security updates
   - Auto-merge enablement
   - (Note: `.github/` config files are created during scaffold, not github-secure)

These are invoked automatically by `/nean-kit`.

## Output
Summarize: structure created, commands available, what tooling is included, GitHub status if applicable, **and remind to run github-hooks/github-secure if not using nean-kit**.
