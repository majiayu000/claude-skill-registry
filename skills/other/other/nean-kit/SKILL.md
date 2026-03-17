---
name: nean-kit
description: Startup runbook for NEAN projects. Establishes stack decisions, scaffolds the project, configures GitHub security, and confirms governing constraints.
---

## Purpose

Initialize a new NEAN project with the standard stack, scaffolding, GitHub security, and constraints.

Input: `<app-name>` (optional, default: "app")

## Startup sequence (run in order)

### 1. Confirm stack decisions

```
/nean-stack
```

Establishes: toolchain, Nx monorepo layout, NestJS/Angular conventions, database approach, environments.

### 2. Scaffold the project

```
/nean-scaffold <app-name> [--github]
```

Creates: build-green baseline with CI, tests, shared libraries, API utilities, Docker configuration.

### 3. Set up local Git hooks

```
/github-hooks --platform nean
```

Installs: Husky + lint-staged, pre-commit validation (lint, format, secrets), commit message enforcement, pre-push tests.

### 4. Configure GitHub security (if --github was used)

```
/github-secure
```

Applies: branch protection, Dependabot, CodeQL, CODEOWNERS, SECURITY.md, PR templates, security workflows.

### 5. Verify constraints are active

Confirm these always-on skills are enabled:

- `nean-sec` — security policy
- `nean-nfr` — non-functional requirements
- `nean-std` — coding standards
- `nean-styleguide` — design/UX standards

## Quality workflows (invoke as needed)

- `/nean-unit-test` — run tests, report failures, fix with approval
- `/nean-code-review` — review against policies, fix with approval
- `/nean-design-review` — visual review with Playwright, fix with approval

## Additional workflows (invoke as needed)

- `/nean-add-feature` — scaffold new feature modules
- `/nean-add-auth` — add authentication
- `/nean-api-docs` — generate OpenAPI documentation
- `/nean-e2e` — E2E test management
- `/nean-deps` — dependency management
- `/nean-deploy` — prepare for deployment

## Output

After running this kit, confirm:

- Stack decisions applied
- Project scaffolded and building
- **Local Git hooks installed (pre-commit, commit-msg, pre-push)**
- **GitHub security configured (if --github)**
- Governing constraints active
- Quality workflows available
