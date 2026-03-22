---
name: ln-742-precommit-setup
description: Configures Husky, lint-staged, commitlint, and Python pre-commit
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# ln-742-precommit-setup

**Type:** L3 Worker
**Category:** 7XX Project Bootstrap
**Parent:** ln-740-quality-setup

Sets up Git hooks for automated code quality enforcement before commits.

---

## Purpose & Scope

**Does:**
- Installs hook management tools (Husky or pre-commit)
- Configures staged file linting (lint-staged or pre-commit hooks)
- Sets up commit message validation (commitlint)
- Verifies hooks trigger correctly

**Does NOT:**
- Configure linters themselves (ln-741 does this)
- Set up test infrastructure (ln-743 does this)
- Modify source code

---

## Supported Stacks

| Technology | Hook Manager | Staged Linting | Commit Validation |
|------------|--------------|----------------|-------------------|
| Node.js | Husky | lint-staged | commitlint |
| Python | pre-commit | pre-commit hooks | pre-commit hook |
| Mixed | Both (if needed) | Stack-specific | commitlint |

---

## Phase 1: Check Existing Hooks

Before installing, check for existing hook configurations.

**Files to Check:**

| Tool | Indicators |
|------|------------|
| Husky | `.husky/` directory, `husky` in package.json |
| pre-commit | `.pre-commit-config.yaml` |
| lint-staged | `lint-staged` in package.json or `.lintstagedrc*` |
| commitlint | `commitlint.config.*`, `.commitlintrc*` |

**Decision Logic:**
1. If hooks exist and working: **SKIP** (inform user)
2. If partial setup: **ASK** user to complete or replace
3. If no hooks: **CREATE** from templates

---

## Phase 2: Install Hook Manager

### Node.js Projects (Husky)

```bash
npm install -D husky
npx husky init
```

This creates:
- `.husky/` directory
- `.husky/pre-commit` hook file
- Adds `prepare` script to package.json

### Python Projects (pre-commit)

```bash
pip install pre-commit
# OR with uv:
uv add --dev pre-commit

pre-commit install
```

This creates:
- `.git/hooks/pre-commit` (managed by pre-commit)
- Requires `.pre-commit-config.yaml` for configuration

---

## Phase 3: Configure Staged Linting

### Node.js (lint-staged)

```bash
npm install -D lint-staged
```

Create configuration (`.lintstagedrc.mjs` or in package.json):

**Key Rules:**
- TypeScript files: ESLint + Prettier
- JSON/MD/CSS: Prettier only
- C# files: dotnet format (if mixed project)

> **CRITICAL FIX:** For .NET files, use correct syntax:
> `"*.cs": "dotnet format --include"` is WRONG
> Use: `"*.cs": "dotnet format whitespace --include"` or run dotnet format separately

### Python (pre-commit hooks)

Configuration in `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

---

## Phase 4: Configure Commit Message Validation

### Node.js (commitlint)

```bash
npm install -D @commitlint/cli @commitlint/config-conventional
```

Create `commitlint.config.mjs` with:
- Conventional Commits format
- Allowed types: feat, fix, docs, style, refactor, test, chore, ci
- Max header length: 100 characters

### Update Husky hook

Add commit-msg hook:
```bash
echo 'npx --no -- commitlint --edit "$1"' > .husky/commit-msg
```

### Python (pre-commit hook for commit message)

Add to `.pre-commit-config.yaml`:
```yaml
  - repo: https://github.com/compilerla/conventional-pre-commit
    rev: v3.4.0
    hooks:
      - id: conventional-pre-commit
        stages: [commit-msg]
```

---

## Phase 5: Test Hooks

Verify hooks work correctly.

**Test 1: Lint-staged triggers**
```bash
# Create a file with lint issues
echo "const x=1" > test-file.ts
git add test-file.ts
git commit -m "test: verify hooks"
# Expected: lint-staged runs, either fixes or blocks
```

**Test 2: Commit message validation**
```bash
git commit --allow-empty -m "bad message"
# Expected: commitlint rejects

git commit --allow-empty -m "test: valid message format"
# Expected: commit succeeds
```

**Cleanup:**
```bash
rm test-file.ts
git reset HEAD~1  # If test commit was made
```

---

## Critical Rules

> **RULE 1:** Husky requires Git repository (`git init` first).

> **RULE 2:** lint-staged MUST have linters configured first (run ln-741 before ln-742).

> **RULE 3:** Document `--no-verify` escape hatch for emergency commits.

> **RULE 4:** pre-commit hooks should auto-fix when possible (`--fix` flag).

---

## Definition of Done

- [ ] Hook manager installed (Husky or pre-commit)
- [ ] Staged linting configured and working
- [ ] Commit message validation configured
- [ ] Test commit triggers hooks correctly
- [ ] User informed of:
  - How hooks work
  - How to skip hooks in emergency (`git commit --no-verify`)
  - Commit message format required

---

## Reference Files

| File | Purpose |
|------|---------|
| [husky_precommit_template.sh](references/husky_precommit_template.sh) | Husky pre-commit hook |
| [husky_commitmsg_template.sh](references/husky_commitmsg_template.sh) | Husky commit-msg hook |
| [lintstaged_template.mjs](references/lintstaged_template.mjs) | lint-staged configuration |
| [commitlint_template.mjs](references/commitlint_template.mjs) | commitlint configuration |
| [precommit_config_template.yaml](references/precommit_config_template.yaml) | Python pre-commit config |
| [hooks_guide.md](references/hooks_guide.md) | Detailed hooks guide |

---

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Husky not running | Missing prepare script | Run `npx husky init` again |
| lint-staged fails | Missing linter | Run ln-741 first |
| pre-commit not found | Not in PATH | `pip install pre-commit` |
| Hooks not triggering | Git hooks disabled | Check `.git/hooks/` permissions |
| Windows path issues | Shell script format | Use cross-platform syntax |

---

## Emergency Bypass

Document for users:

```bash
# Skip all hooks (use sparingly!)
git commit --no-verify -m "emergency: bypass hooks"

# Skip only pre-commit (keeps commit-msg)
HUSKY=0 git commit -m "fix: urgent hotfix"
```

---

**Version:** 2.0.0
**Last Updated:** 2026-01-10
