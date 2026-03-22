---
name: fci
description: >-
  Fix CI pipeline failures blocking PR merge. Use when CI checks fail,
  'pipeline broken', 'build failing', 'fix CI', or 'checks not passing'.
  NOT for debugging runtime bugs (use /dbg), NOT for code review (use /sr).
argument-hint: [workflow-name or run-id]
allowed-tools: Bash, Read, Edit, Write, Grep, Glob
disable-model-invocation: true
---

# Fix CI Issues Command

## PRIMARY OBJECTIVE
Fix all CI pipeline failures blocking the PR merge while maintaining code quality and test integrity.

## SCOPE
- Currently supports: `backend/` CI pipeline (Backend CI workflow)
- If `$ARGUMENTS` specifies a workflow outside `backend/`, inform the user and suggest manual investigation

## CONTEXT & CONSTRAINTS
- CI pipeline failed during merge attempt to main branch
- Must resolve all failures without compromising code quality
- Preserve existing test coverage and validation logic
- CI includes: Node.js backend checks (`npm run lint`, `npm run test:ci`), Prisma migrations, and Docker build with a Postgres test database
- **NEVER** use `any` type, `@ts-ignore`, `// eslint-disable`, or architectural shortcuts to make CI pass
- Follow project DDD and Clean Architecture rules (see `.claude/rules/backend.md`)

## RELATED SKILLS
- `/dbg` - Runtime bugs requiring instrumentation and evidence gathering
- `/sr` - Post-fix code review before re-attempting merge
- `/prc` - Addressing reviewer comments on the PR

## ANALYSIS REQUIREMENTS
1. **Identify CI Failures:**
   - Run `gh workflow list` if you are unsure of the workflow name
   - Run `gh run list --workflow="Backend CI" --limit=3` to check recent CI status
   - Review failure logs (`gh run view <run-id> --log`) to identify specific issues
   - Categorize failures by type (linting, tests, database/migrations, docker)

2. **Execute Diagnostic Checks:**
   - Ensure dependencies are installed: `npm install` (run inside `backend/`)
   - Start the Dockerised Postgres test DB: `npm run test:db:start`
   - Apply test migrations: `npm run test:db:migrate`
   - `npm run lint:check` – ESLint validation without autofix (use `npm run lint` if you want the same behaviour as CI's autofix step)
   - `npm run test:ci` – Runs Jest test suite with `dotenv` loading `test-env/.env.test`
   - Stop the database once diagnostics are complete: `npm run test:db:stop`

## RESOLUTION PROCESS
1. **Fix Formatting Issues First:**
   - Run `npm run format` (Prettier) if style violations are reported
   - Let ESLint autofix with `npm run lint` when practical; re-run `npm run lint:check` afterwards to confirm clean output

2. **Address Type Errors:**
   - Resolve TypeScript or Prisma typing errors surfaced by ESLint/Jest/tsc output
   - Add precise typings rather than suppressing warnings; avoid `// eslint-disable` unless absolutely necessary

3. **Resolve Test Failures:**
   - Fix failing tests by correcting implementation bugs
   - DO NOT simplify tests or reduce assertions
   - Maintain or improve test coverage (>=80% target)

4. **Fix Linting Issues:**
   - Address ESLint violations
   - Update tests/fixtures when necessary rather than suppressing rules

5. **Security Issues:**
   - Address any `npm audit` or dependency vulnerability findings that surface during investigation

6. **Docker Build Issues:**
   - Ensure Docker build succeeds and smoke test passes
   - Fix any import or runtime errors in containerized environment

## VERIFICATION REQUIREMENTS
Before completion, execute ALL checks (from the `backend/` directory) and confirm passing:
```bash
# Start & migrate the test database once
npm run test:db:start && \
npm run test:db:migrate && \
# Run full CI validation suite (matches .github/workflows/backend-ci.yml)
npm run lint:check && \
npm run test:ci && \
# Always stop the DB afterwards
npm run test:db:stop
```

Optional additional checks (if security/docker jobs are failing):
```bash
# Docker build test
docker build -t app:ci .

# Security checks
npm audit
```

## TROUBLESHOOTING
- `gh` auth failure: Run `gh auth status`; prompt user to run `gh auth login` if needed
- Docker not running: Run `docker info`; inform user to start Docker Desktop
- DB connection refused: Verify `npm run test:db:start` succeeded; check port conflicts on 5433
- Node version mismatch: Check `.nvmrc` or `engines` in `package.json`; run `nvm use` if available

## DEFINITION OF DONE
- [ ] All CI checks pass (lint, typing, format, tests, security, docker)
- [ ] Test coverage maintained at >=80%
- [ ] No test logic simplified or removed
- [ ] Security vulnerabilities resolved (npm audit or equivalent)
- [ ] Docker build and smoke test pass
- [ ] GitHub CI status shows green checkmark
- [ ] Ready for clean merge to main branch
