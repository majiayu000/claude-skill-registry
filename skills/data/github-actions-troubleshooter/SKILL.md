---
name: github-actions-troubleshooter
description: Diagnose and fix GitHub Actions workflow failures, CI/CD pipeline issues,
  YAML syntax errors, and workflow configuration problems. Use when debugging failed
  CI runs, fixing workflow errors, or optimiz
---

---
name: github-actions-troubleshooter
description: Diagnose and fix GitHub Actions workflow failures, CI/CD pipeline issues, YAML syntax errors, and workflow configuration problems. Use when debugging failed CI runs, fixing workflow errors, or optimizing GitHub Actions. Keywords: github actions, CI, workflow, pipeline, yml, yaml, actions failure, CI failure, workflow error
---

# GitHub Actions Troubleshooter

Diagnoses and fixes GitHub Actions workflow failures and configuration issues.

## Instructions

When activated, follow this systematic troubleshooting approach:

### 1. Identify the Failure

**Get workflow status:**
```bash
gh run list --limit 5                    # Recent runs
gh run view <run-id>                     # Specific run details
gh run view <run-id> --log-failed        # Failed job logs only
```

**Analyze the failure:**
- Parse error messages from logs
- Identify which job/step failed
- Note the exit code and error type
- Check if it's intermittent or consistent

### 2. Common Failure Categories

#### **YAML Syntax Errors**
- Invalid indentation (must use spaces, not tabs)
- Missing required fields (`name`, `on`, `jobs`)
- Invalid step format
- Quote escaping issues

**Fix approach:**
- Read the workflow file with Read tool
- Validate YAML structure
- Check GitHub Actions syntax documentation
- Use Edit tool to fix syntax

#### **Dependency/Setup Issues**
- Node/Python/etc version mismatches
- Missing dependencies in package.json/requirements.txt
- Cache invalidation needed
- Setup action version incompatibility

**Fix approach:**
```yaml
# Pin versions explicitly
- uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'pnpm'
```

#### **Test/Build Failures**
- Tests failing in CI but passing locally
- Environment variable differences
- File path issues (case sensitivity on Linux)
- Missing environment secrets

**Fix approach:**
- Compare local vs CI environment
- Check for hardcoded paths
- Verify secrets are configured
- Add debugging output

#### **Permission Errors**
- `GITHUB_TOKEN` insufficient permissions
- File permission issues
- Branch protection violations

**Fix approach:**
```yaml
permissions:
  contents: write
  pull-requests: write
  checks: read
```

#### **Timeout/Performance Issues**
- Jobs exceeding 6-hour limit
- Slow dependency installation
- Missing caching
- Inefficient matrix strategies

**Fix approach:**
- Add caching for dependencies
- Parallelize independent jobs
- Optimize test suites
- Use workflow artifacts efficiently

### 3. Diagnostic Workflow

**Step 1: Read the workflow file**
```bash
# Find workflow files
fd -e yml -e yaml . .github/workflows
```

**Step 2: Get recent run logs**
```bash
# View latest failed run
gh run view --log-failed

# Or specific run by ID
gh run view 1234567890 --log
```

**Step 3: Identify root cause**
- Parse error messages
- Check for known patterns
- Review recent changes with git log
- Compare with working runs

**Step 4: Apply fix**
- Use Edit tool for workflow changes
- Test locally if possible
- Create PR for review
- Monitor next run

### 4. Common Fixes

#### **Format Check Failures (Prettier/ESLint)**
```yaml
# Before commit, run formatters
- name: Format code
  run: pnpm exec prettier --write .

# Or enforce in CI
- name: Check formatting
  run: pnpm exec prettier --check .
```

#### **Missing Environment Variables**
```yaml
env:
  NODE_ENV: production
  API_URL: ${{ secrets.API_URL }}

jobs:
  build:
    env:
      CUSTOM_VAR: value
```

#### **Caching Dependencies**
```yaml
- uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'pnpm'  # or 'npm', 'yarn'

# Or manual cache
- uses: actions/cache@v4
  with:
    path: ~/.cache
    key: ${{ runner.os }}-cache-${{ hashFiles('**/pnpm-lock.yaml') }}
```

#### **Matrix Strategy for Multiple Versions**
```yaml
strategy:
  matrix:
    node-version: [18, 20, 22]
    os: [ubuntu-latest, windows-latest]
jobs:
  test:
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
```

### 5. Project-Specific Context

**This project uses:**
- **Package Manager**: pnpm
- **Pre-commit checks**: `pnpm run pre-commit` (format + lint + typecheck)
- **Common CI tasks**: format check, typecheck, build, test

**Standard workflow pattern:**
```yaml
name: CI
on: [push, pull_request]
jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
        with:
          version: 8
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'pnpm'
      - run: pnpm install
      - run: pnpm run pre-commit
      - run: pnpm run test
      - run: pnpm run build
```

### 6. Output Format

Present findings as:

**🔍 Diagnosis**
- Job: `format-check`
- Step: `Run prettier --check`
- Error: `Code style issues found in 11 files`
- Root Cause: Files not formatted with Prettier

**🔧 Fix Applied**
```yaml
# File: .github/workflows/ci.yml:15
- name: Format check
  run: pnpm exec prettier --config .config/.prettierrc --check .
```

**✅ Verification**
- Run locally: `pnpm exec prettier --write .`
- Commit formatted files
- Monitor next CI run

### 7. Prevention & Best Practices

**Pre-commit hooks:**
- Run formatters before commit
- Validate locally before pushing
- Use `pnpm run pre-commit`

**Workflow best practices:**
- Pin action versions (`actions/checkout@v4` not `@main`)
- Use caching for dependencies
- Set explicit timeouts
- Add descriptive step names
- Use `if: failure()` for debugging steps

**Security:**
- Minimize `GITHUB_TOKEN` permissions
- Don't log secrets
- Use `secrets` context, not env vars for sensitive data
- Review third-party actions before use

## Tools to Use

- **Read**: View workflow YAML files
- **Edit**: Fix workflow configuration
- **Bash(gh:*)**: Get run logs, workflow status
- **Bash(git:*)**: Check recent changes, blame
- **Grep**: Search for patterns in logs/workflows
- **WebFetch**: Check GitHub Actions documentation

## Example Activation

These user requests will trigger this skill:
- "Why is my GitHub Actions workflow failing?"
- "Fix the CI pipeline error"
- "The format check is failing in CI"
- "Help debug this workflow YAML"
- "My tests pass locally but fail in GitHub Actions"
