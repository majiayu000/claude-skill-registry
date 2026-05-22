---
name: mern-kit
description: Startup runbook for MERN projects. Establishes stack decisions, scaffolds the project, configures GitHub security, and confirms governing constraints.
---

## Purpose

Initialize a new MERN project with the standard stack, scaffolding, GitHub security, and constraints.

Input: `<app-name>` (optional, default: "app"). Use `.` to scaffold in the current (empty) directory.

## Startup sequence (run in order)

### 1. Confirm stack decisions

```
/mern-stack
```

Establishes: toolchain, monorepo layout, Next.js conventions, database approach, environments.

### 2. Scaffold the project

```
/mern-scaffold <app-name> [--github]
```

Creates: build-green baseline with CI, tests, shared packages, server utilities, tooling.

The scaffold step includes `git init` at the end.

### 3. Set up local Git hooks

**Prerequisite:** The scaffold step must have completed `git init` first.

```
/github-hooks --platform mern
```

Installs: Husky + lint-staged, pre-commit validation (lint, format, secrets), commit message enforcement, pre-push tests.

### 4. Configure GitHub security (if --github was used)

```
/github-secure
```

Applies: branch protection, Dependabot alerts, auto-merge. Skips files already created by scaffold.

### 5. Verify constraints are active

Confirm these always-on skills are enabled:

- `mern-sec` — security policy
- `mern-nfr` — non-functional requirements
- `mern-std` — coding standards
- `mern-styleguide` — design/UX standards

### 6. Verify CI passes (if --github)

Trigger CI and wait for it to complete:
1. `gh workflow run ci.yml --ref main` (or wait for push-triggered run)
2. `gh run watch --exit-status` — blocks until complete, exits non-zero on failure
3. If failed:
   a. Read logs: `gh run view --log-failed`
   b. Fix the issue locally
   c. If push to main is blocked by branch protection, temporarily disable enforcement:
      ```bash
      REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)
      gh api -X PATCH "/repos/$REPO/branches/main/protection/enforce_admins" -f enforcement=false
      git push
      gh api -X POST "/repos/$REPO/branches/main/protection/enforce_admins"
      ```
   d. Push and re-run: `gh run watch --exit-status`
4. Repeat step 3 until CI is green
5. Do NOT mark kit complete until CI is green

## Quality workflows (invoke as needed)

- `/mern-unit-test` — run tests, report failures, fix with approval
- `/mern-code-review` — review against policies, fix with approval
- `/mern-design-review` — visual review with Playwright, fix with approval

## Additional workflows (invoke as needed)

- `/mern-add-feature` — scaffold new features
- `/mern-add-auth` — add authentication
- `/mern-deploy` — prepare for deployment
- `/mern-e2e` — E2E test management
- `/mern-api-docs` — generate API documentation
- `/mern-deps` — dependency management
- `/mern-teardown` — tear down project and optionally delete GitHub repo

## Output

After running this kit, confirm:

- Stack decisions applied
- Project scaffolded and building
- **Local Git hooks installed (pre-commit, commit-msg, pre-push)**
- **GitHub security configured (if --github)**
- **CI passes on GitHub (if --github)**
- Governing constraints active
- Quality workflows available
