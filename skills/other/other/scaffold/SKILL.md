---
name: scaffold
description: Detect project stack, apply architecture patterns, wire quality gates, and scaffold features. Use when bootstrapping a project, adding a vertical slice, wiring CI/CD, adding Docker compose, or setting up quality gates.
---

# Scaffold

Detect the current project's stack and apply toolkit architecture patterns, quality gates, and scaffolding.

## When to Apply

- Scaffolding a new vertical slice or feature module
- Wiring or updating CI/CD pipelines
- Adding or modifying Docker Compose services
- Refactoring shared utilities or extracting common code
- Setting up or running quality gates (lint, type-check, test, build)
- Applying layered architecture (routes -> services -> repositories)
- Reviewing code against SOLID and clean-code principles
- Bootstrapping a new project with toolkit standards

## Step 1: Detect Project Context

Before making any changes, inspect the current repository:

1. Read `package.json`, `*.csproj`, `Cargo.toml`, `go.mod`, or equivalent to determine language and framework
2. Check for existing `CLAUDE.md`, `.claude/rules/`, `.claude/settings.json`
3. Scan for `docker-compose*.yml`, `Dockerfile`, `.github/workflows/`
4. Identify the package manager (`npm`, `yarn`, `pnpm`, `bun`)
5. Identify the test runner (`jest`, `vitest`, `pytest`, `go test`)
6. Check for monorepo indicators (`workspaces`, `turbo.json`, `nx.json`, `lerna.json`)

Summarize findings before proceeding.

## Step 2: Apply Architectural Patterns

Based on project type, enforce these layered architecture rules:

### Backend (Node.js / TypeScript)
- **HTTP layer** (routes/controllers): thin adapters only, no business logic, no direct DB access
- **Service layer**: business logic, orchestration, validation
- **Repository layer**: data access, ORM encapsulation, query building
- **Dependency direction**: routes -> services -> repositories (never reverse)

### Frontend (React / TypeScript)
- **Components**: presentational, no direct API calls in render
- **Hooks**: data fetching, state management, side effects
- **Services**: API client wrappers, data transformation
- **State**: colocate state; lift only when shared

### General
- TypeScript strict mode, explicit return types on public APIs
- ES modules everywhere (never CommonJS)
- Named exports preferred over default exports
- Error types over generic throws

## Step 3: Quality Gate Checklist

Run these checks in order (fast-fail):

```
1. [ ] TypeScript / type-check passes     (npx tsc --noEmit OR equivalent)
2. [ ] Linting passes                      (npm run lint OR equivalent)
3. [ ] Tests pass                          (npm test OR equivalent)
4. [ ] Build succeeds                      (npm run build OR equivalent)
5. [ ] No new lint warnings introduced
6. [ ] Coverage >= project threshold
```

If any check fails, stop and fix before proceeding.

## Step 4: Verify and Report

After completing changes:

1. Re-run the quality gate checklist
2. Summarize what was changed and why
3. List any remaining TODOs or follow-up items
4. If creating a PR, ensure title is concise (<70 chars) and body includes a test plan

## Available Toolkit Skills

The toolkit provides specialized skills for common tasks. Invoke them when relevant:

- **quality-gate**: Full quality validation (tests + lint + types + build + audit)
- **validate-build**: Build-only validation
- **validate-typescript**: Type-checking only
- **validate-lint**: Lint-only validation
- **run-comprehensive-tests**: Test execution with coverage
- **commit-with-validation**: Git commit with pre-flight checks
- **create-pull-request**: PR creation with template
- **audit-dependencies**: Security audit of dependencies
- **infrastructure**: Deployment orchestration (DNS, VPS, Docker)

## Adaptation Notes

This skill adapts to any project. If the project uses:
- **Python**: substitute `mypy` for tsc, `ruff`/`black` for eslint, `pytest` for jest
- **Go**: substitute `go vet` for tsc, `golangci-lint` for eslint, `go test` for jest
- **Rust**: substitute `cargo check` for tsc, `cargo clippy` for eslint, `cargo test` for jest
- **Other**: detect and adapt tooling from project config files
