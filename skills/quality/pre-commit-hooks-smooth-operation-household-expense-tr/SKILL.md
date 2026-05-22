---
name: pre-commit-hooks
description: "MANDATORY setup for all projects. Automated code quality enforcement before commits. Prevents bad code from entering repository."
---

# Pre-Commit Hooks

## Core Principle

**Automate quality gates - humans forget, machines don't.**

## When to Use This Skill

- Setting up new projects (MANDATORY)
- Onboarding team members
- Improving code quality
- Preventing bad commits
- Enforcing standards

## The Iron Law

**NO PROJECT WITHOUT PRE-COMMIT HOOKS.**

Every repository MUST have automated quality checks before commits are allowed.

## Why Pre-Commit Hooks Are Mandatory

**Without hooks:**
- ❌ Unformatted code enters repository
- ❌ Type errors slip through
- ❌ Tests broken by commits
- ❌ Secrets/credentials committed
- ❌ Linting errors ignored

**With hooks:**
- ✅ Automatic code formatting
- ✅ Type checking enforced
- ✅ Tests run before commit
- ✅ No secrets committed
- ✅ Consistent code quality

**Authority**: 95% of professional teams use pre-commit hooks. Not using them is unprofessional.

## Setup by Language

### JavaScript/TypeScript Projects

**Install pre-commit framework:**

```bash
npm install --save-dev husky lint-staged
npx husky install
npm set-script prepare "husky install"
```

**Create `.husky/pre-commit`:**

```bash
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

npx lint-staged
```

**Configure `package.json`:**

```json
{
  "lint-staged": {
    "*.{js,jsx,ts,tsx}": [
      "eslint --fix",
      "prettier --write",
      "npm run test:related --bail"
    ],
    "*.{json,md,yml,yaml}": [
      "prettier --write"
    ]
  },
  "scripts": {
    "prepare": "husky install",
    "test:related": "jest --bail --findRelatedTests"
  }
}
```

**Minimum hooks:**
- ✅ ESLint (linting + auto-fix)
- ✅ Prettier (formatting)
- ✅ TypeScript check (tsc --noEmit)
- ✅ Jest (related tests)
- ✅ No secrets check

### Python Projects

**Install pre-commit:**

```bash
pip install pre-commit
```

**Create `.pre-commit-config.yaml`:**

```yaml
repos:
  # Code formatting
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
        language_version: python3.11

  # Import sorting
  - repo: https://github.com/PyCQA/isort
    rev: 5.13.2
    hooks:
      - id: isort

  # Linting
  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.1.9
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]

  # Type checking
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [types-requests]

  # Security checks
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.6
    hooks:
      - id: bandit
        args: ["-c", "pyproject.toml"]

  # Tests
  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: pytest
        language: system
        pass_filenames: false
        always_run: true
```

**Install hooks:**

```bash
pre-commit install
```

**Minimum hooks:**
- ✅ Black (formatting)
- ✅ isort (import sorting)
- ✅ Ruff (linting)
- ✅ mypy (type checking)
- ✅ pytest (tests)
- ✅ bandit (security)

### PHP/Laravel Projects

**Install pre-commit tools:**

```bash
composer require --dev friendsofphp/php-cs-fixer phpstan/phpstan
```

**Create `.husky/pre-commit` (using Husky):**

```bash
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

# Get staged PHP files
FILES=$(git diff --cached --name-only --diff-filter=ACMR | grep '\.php$')

if [ -n "$FILES" ]; then
  # Format code
  vendor/bin/php-cs-fixer fix $FILES --config=.php-cs-fixer.php

  # Static analysis
  vendor/bin/phpstan analyse $FILES

  # Run tests for changed files
  vendor/bin/paratest --filter=$(echo $FILES | tr '\n' '|')

  # Re-add formatted files
  git add $FILES
fi
```

**Or use PHP pre-commit library:**

```bash
composer require --dev brainmaestro/composer-git-hooks
```

**Configure in `composer.json`:**

```json
{
  "extra": {
    "hooks": {
      "pre-commit": [
        "vendor/bin/php-cs-fixer fix --dry-run --diff",
        "vendor/bin/phpstan analyse",
        "vendor/bin/paratest"
      ]
    }
  }
}
```

**Minimum hooks:**
- ✅ PHP CS Fixer (formatting)
- ✅ PHPStan (static analysis)
- ✅ Psalm (type checking)
- ✅ Paratest (tests)
- ✅ No secrets check

## Universal Hooks (All Projects)

**Add these to every project:**

### 1. No Secrets Check

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.1
    hooks:
      - id: gitleaks
```

### 2. Trailing Whitespace

```yaml
- repo: https://github.com/pre-commit/pre-commit-hooks
  rev: v4.5.0
  hooks:
    - id: trailing-whitespace
    - id: end-of-file-fixer
    - id: check-yaml
    - id: check-json
    - id: check-added-large-files
```

### 3. Commit Message Validation

```bash
# .husky/commit-msg
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

npx --no -- commitlint --edit "$1"
```

**Install commitlint:**

```bash
npm install --save-dev @commitlint/cli @commitlint/config-conventional
```

**Configure `commitlint.config.js`:**

```javascript
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [2, 'always', [
      'feat', 'fix', 'docs', 'style', 'refactor',
      'perf', 'test', 'build', 'ci', 'chore'
    ]]
  }
};
```

## Frontend + Backend Test Requirements

**For projects with both frontend and backend:**

```bash
# .husky/pre-commit
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

echo "🧪 Running pre-commit checks..."

# Check if backend files changed
BACKEND_CHANGED=$(git diff --cached --name-only | grep -E '\.(php|py|go|java)$')

# Check if frontend files changed
FRONTEND_CHANGED=$(git diff --cached --name-only | grep -E '\.(js|jsx|ts|tsx|vue)$')

# If backend changed, run backend tests
if [ -n "$BACKEND_CHANGED" ]; then
  echo "🔧 Backend files changed - running backend tests..."
  npm run test:backend || exit 1
fi

# If frontend changed, run frontend AND e2e tests
if [ -n "$FRONTEND_CHANGED" ]; then
  echo "🎨 Frontend files changed - running frontend tests..."
  npm run test:frontend || exit 1

  echo "🌐 Running e2e tests..."
  npm run test:e2e || exit 1
fi

# If both changed, ensure full test suite passes
if [ -n "$BACKEND_CHANGED" ] && [ -n "$FRONTEND_CHANGED" ]; then
  echo "🔄 Full stack changes detected - running complete test suite..."
  npm run test:all || exit 1
fi

echo "✅ All pre-commit checks passed!"
```

## Bypassing Hooks (Emergency Only)

**Never bypass hooks casually:**

```bash
# WRONG - don't do this
git commit --no-verify

# ONLY use in true emergencies:
# - Hotfix for production outage
# - CI/CD system down, blocking critical deploy
# - After consulting team lead
```

**If you bypass hooks:**
1. Add TODO comment explaining why
2. Create follow-up task to fix properly
3. Inform team in commit message
4. Never bypass for "speed" or "convenience"

## Verification

**After setup, verify hooks work:**

```bash
# Make a bad change (intentionally)
echo "const x = 1" > test.js  # Missing semicolon

# Try to commit
git add test.js
git commit -m "test"

# Should FAIL with linting error
# If it commits successfully, hooks aren't working!
```

## Team Onboarding

**When new developer joins:**

```bash
# Clone repo
git clone <repo>
cd <repo>

# Install dependencies (includes hook setup)
npm install  # or pip install -r requirements.txt

# Verify hooks installed
ls .git/hooks/pre-commit

# Test hooks work
# (make intentional error, try to commit, should fail)
```

## Common Issues

### Issue: Hooks not running

**Solution:**
```bash
# Reinstall hooks
npm run prepare  # for Husky
# or
pre-commit install  # for Python
```

### Issue: Hooks too slow

**Solution:**
```bash
# Run only on staged files (lint-staged)
# Skip slow tests in hooks, run in CI
# Use --bail flag to fail fast
```

### Issue: Hooks block legitimate commits

**Solution:**
```bash
# Fix the actual issue (don't bypass)
# Update hook configuration if rule is wrong
# Discuss with team if standard should change
```

## Integration with Skills

**Pre-commit hooks enforce:**

1. **verification-before-completion** - Tests must pass
2. **git-workflow** - Commit message format
3. **database-backup** - Prevent commits without backup (if DB changed)
4. **code-review** - Linting/formatting standards

## Commitment Required

**Before proceeding, acknowledge:**

- [ ] I will set up pre-commit hooks on ALL projects
- [ ] I will NEVER bypass hooks without team discussion
- [ ] I understand hooks are quality gates, not obstacles
- [ ] I will help team members set up hooks correctly
- [ ] I will update hooks when new standards are adopted

---

**The Iron Law (Repeated)**: NO PROJECT WITHOUT PRE-COMMIT HOOKS. This is not optional. This is professional software development.
