---
name: git-hooks-setup
description: Implement Git hooks using Husky, pre-commit, and custom scripts. Enforce code quality, linting, and testing before commits and pushes.
---

# Git Hooks Setup

## Overview

Configure Git hooks to enforce code quality standards, run automated checks, and prevent problematic commits from being pushed to shared repositories.

## When to Use

- Pre-commit code quality checks
- Commit message validation
- Preventing secrets in commits
- Running tests before push
- Code formatting enforcement
- Linting configuration
- Team-wide standards enforcement

## Implementation Examples

### 1. **Husky Installation and Configuration**

```bash
#!/bin/bash
# setup-husky.sh

# Install Husky
npm install husky --save-dev

# Initialize Husky
npx husky install

# Create pre-commit hook
npx husky add .husky/pre-commit "npm run lint"

# Create commit-msg hook
npx husky add .husky/commit-msg 'npx --no -- commitlint --edit "$1"'

# Create pre-push hook
npx husky add .husky/pre-push "npm run test"

# Create post-merge hook
npx husky add .husky/post-merge "npm install"
```

### 2. **Pre-commit Hook (Node.js)**

```bash
#!/usr/bin/env node
# .husky/pre-commit

const { execSync } = require('child_process');
const fs = require('fs');

console.log('🔍 Running pre-commit checks...\n');

try {
  // Get staged files
  const stagedFiles = execSync('git diff --cached --name-only', { encoding: 'utf-8' })
    .split('\n')
    .filter(file => file && (file.endsWith('.js') || file.endsWith('.ts')))
    .join(' ');

  if (!stagedFiles) {
    console.log('✅ No JavaScript/TypeScript files to check');
    process.exit(0);
  }

  // Run linter on staged files
  console.log('📝 Running ESLint...');
  execSync(`npx eslint ${stagedFiles} --fix`, { stdio: 'inherit' });

  // Run Prettier
  console.log('✨ Running Prettier...');
  execSync(`npx prettier --write ${stagedFiles}`, { stdio: 'inherit' });

  // Stage the fixed files
  console.log('📦 Staging fixed files...');
  execSync(`git add ${stagedFiles}`);

  console.log('\n✅ Pre-commit checks passed!');
} catch (error) {
  console.error('❌ Pre-commit checks failed!');
  process.exit(1);
}
```

### 3. **Commit Message Validation**

```bash
#!/bin/bash
# .husky/commit-msg

# Validate commit message format
COMMIT_MSG=$(<"$1")

# Pattern: type(scope): description
PATTERN="^(feat|fix|docs|style|refactor|test|chore|perf)(\([a-z\-]+\))?: .{1,50}"

if ! [[ $COMMIT_MSG =~ $PATTERN ]]; then
    echo "❌ Invalid commit message format"
    echo "Format: type(scope): description"
    echo "Types: feat, fix, docs, style, refactor, test, chore, perf"
    echo ""
    echo "Examples:"
    echo "  feat: add new feature"
    echo "  fix(auth): resolve login bug"
    echo "  docs: update README"
    exit 1
fi

# Check message length
FIRST_LINE=$(echo "$COMMIT_MSG" | head -n1)
if [ ${#FIRST_LINE} -gt 72 ]; then
    echo "❌ Commit message too long (max 72 characters)"
    exit 1
fi

echo "✅ Commit message is valid"
```

### 4. **Commitlint Configuration**

```javascript
// commitlint.config.js
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [2, 'always', ['feat', 'fix', 'docs', 'style', 'refactor', 'test', 'chore']],
    'subject-case': [2, 'never', ['start-case', 'pascal-case', 'upper-case']],
    'type-empty': [2, 'never']
  }
};
```

### 5. **Pre-push Hook (Comprehensive)**

```bash
#!/usr/bin/env bash
# .husky/pre-push
BRANCH=$(git rev-parse --abbrev-ref HEAD)

# Prevent direct pushes to main
if [[ "$BRANCH" =~ ^(main|master)$ ]]; then
  echo "❌ Direct push to $BRANCH not allowed"
  exit 1
fi

npm test && npm run lint && npm run build
```

### 6. **Pre-commit Framework (Python)**

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
        args: ['--maxkb=1000']
      - id: detect-private-key
      - id: check-merge-conflict

  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/PyCQA/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        args: ['--max-line-length=88', '--extend-ignore=E203,W503']

  - repo: https://github.com/PyCQA/isort
    rev: 5.12.0
    hooks:
      - id: isort
        args: ['--profile', 'black']

  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']

  - repo: https://github.com/commitizen-tools/commitizen
    rev: 3.5.2
    hooks:
      - id: commitizen
        stages: [commit-msg]
```

### 7. **Secret Detection Hook**

```bash
#!/bin/bash
# .husky/pre-commit-secrets
git diff --cached | grep -E 'password|api_key|secret|token' && exit 1
echo "✅ No secrets detected"
```

### 8. **Husky in package.json**

```json
{
  "scripts": { "prepare": "husky install" },
  "devDependencies": {
    "husky": "^8.0.0",
    "@commitlint/cli": "^17.0.0"
  },
  "lint-staged": {
    "*.{js,ts}": "eslint --fix"
  }
}
```

## Best Practices

### ✅ DO
- Enforce pre-commit linting and formatting
- Validate commit message format
- Scan for secrets before commit
- Run tests on pre-push
- Skip hooks only with `--no-verify` (rarely)
- Document hook requirements in README
- Use consistent hook configuration
- Make hooks fast (< 5 seconds)
- Provide helpful error messages
- Allow developers to bypass with clear warnings

### ❌ DON'T
- Skip checks with `--no-verify`
- Store secrets in committed files
- Use inconsistent implementations
- Ignore hook errors
- Run full test suite on pre-commit

## Resources

- [Husky Documentation](https://typicode.github.io/husky/)
- [pre-commit Framework](https://pre-commit.com/)
- [Commitlint](https://commitlint.js.org/)
- [lint-staged](https://github.com/okonet/lint-staged)
- [Git Hooks Documentation](https://git-scm.com/docs/githooks)
