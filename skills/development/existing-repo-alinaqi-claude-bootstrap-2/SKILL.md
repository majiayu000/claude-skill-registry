---
name: existing-repo
description: Analyze existing repositories, maintain structure, setup guardrails and best practices
---

# Existing Repository Skill

*Load with: base.md + security.md*

For working with existing codebases - analyze structure, respect conventions, and set up proper guardrails without breaking anything.

**Sources:** [Husky](https://typicode.github.io/husky/) | [lint-staged](https://github.com/lint-staged/lint-staged) | [pre-commit](https://pre-commit.com/) | [commitlint](https://commitlint.js.org/)

---

## Core Principle

**Understand before modifying.** Existing repos have conventions, patterns, and history. Your job is to work within them, not reorganize them.

---

## Phase 1: Repository Analysis

**ALWAYS run this analysis first when joining an existing repo.**

### 1.1 Basic Detection

```bash
# Check git status
git remote -v 2>/dev/null
git branch -a 2>/dev/null
git log --oneline -5 2>/dev/null

# Check for existing configs
ls -la .* 2>/dev/null | head -20
ls *.json *.toml *.yaml *.yml 2>/dev/null
```

### 1.2 Tech Stack Detection

```bash
# JavaScript/TypeScript
ls package.json tsconfig.json 2>/dev/null

# Python
ls pyproject.toml setup.py requirements*.txt 2>/dev/null

# Mobile
ls pubspec.yaml 2>/dev/null          # Flutter
ls android/build.gradle 2>/dev/null   # Android
ls ios/*.xcodeproj 2>/dev/null        # iOS

# Other
ls Cargo.toml 2>/dev/null             # Rust
ls go.mod 2>/dev/null                 # Go
ls Gemfile 2>/dev/null                # Ruby
```

### 1.3 Repo Structure Type

| Pattern | Detection | Meaning |
|---------|-----------|---------|
| **Monorepo** | `packages/`, `apps/`, `workspaces` in package.json | Multiple projects, shared tooling |
| **Full-Stack Monolith** | `frontend/` + `backend/` in same repo | Single team, tightly coupled |
| **Separate Concerns** | Only frontend OR backend code | Split repos, separate deploys |
| **Microservices** | Multiple `service-*` or domain dirs | Distributed architecture |

```bash
# Detect repo structure type
if [ -d "packages" ] || [ -d "apps" ]; then
    echo "MONOREPO detected"
elif [ -d "frontend" ] && [ -d "backend" ]; then
    echo "FULL-STACK MONOLITH detected"
elif [ -d "src" ] || [ -d "app" ]; then
    # Check if it's frontend or backend
    grep -q "react\|vue\|angular" package.json 2>/dev/null && echo "FRONTEND detected"
    grep -q "fastapi\|express\|django" package.json pyproject.toml 2>/dev/null && echo "BACKEND detected"
fi
```

### 1.4 Directory Mapping

```bash
# Get directory structure (max 3 levels)
find . -type d -maxdepth 3 \
    -not -path "*/node_modules/*" \
    -not -path "*/.git/*" \
    -not -path "*/venv/*" \
    -not -path "*/__pycache__/*" \
    -not -path "*/dist/*" \
    -not -path "*/build/*" \
    2>/dev/null | head -50

# Identify key directories
for dir in src app lib core services api routes components pages hooks utils models; do
    [ -d "$dir" ] && echo "Found: $dir/"
done
```

### 1.5 Entry Points

```bash
# Find main entry points
ls index.ts index.js main.ts main.py app.py server.ts server.js 2>/dev/null
cat package.json 2>/dev/null | grep -A1 '"main"'
cat pyproject.toml 2>/dev/null | grep -A1 'scripts'
```

---

## Phase 2: Convention Detection

**Identify and document existing patterns before making changes.**

### 2.1 Code Style

```bash
# Check for formatters
ls .prettierrc* .editorconfig .eslintrc* biome.json 2>/dev/null  # JS/TS
ls pyproject.toml | xargs grep -l "ruff\|black\|isort" 2>/dev/null  # Python

# Check indent style from existing files
head -20 src/**/*.ts 2>/dev/null | grep "^\s" | head -1  # tabs vs spaces
```

### 2.2 Testing Setup

```bash
# JS/TS testing
grep -l "jest\|vitest\|mocha\|playwright" package.json 2>/dev/null
ls jest.config.* vitest.config.* playwright.config.* 2>/dev/null

# Python testing
grep -l "pytest\|unittest" pyproject.toml 2>/dev/null
ls pytest.ini conftest.py 2>/dev/null

# Test directories
ls -d tests/ test/ __tests__/ spec/ 2>/dev/null
```

### 2.3 CI/CD Setup

```bash
# Check existing workflows
ls -la .github/workflows/ 2>/dev/null
ls .gitlab-ci.yml Jenkinsfile .circleci/ 2>/dev/null

# Check deploy configs
ls vercel.json render.yaml fly.toml railway.json Dockerfile 2>/dev/null
```

### 2.4 Documentation Style

```bash
# Find README pattern
head -30 README.md 2>/dev/null

# Find existing docs
ls -la docs/ documentation/ wiki/ 2>/dev/null
ls CONTRIBUTING.md CHANGELOG.md 2>/dev/null
```

---

## Phase 3: Guardrails Audit

**Check what guardrails exist and what's missing.**

### 3.1 Pre-commit Hooks Status

```bash
# Check for hook managers
ls .husky/ 2>/dev/null && echo "Husky installed"
ls .pre-commit-config.yaml 2>/dev/null && echo "pre-commit framework installed"
ls .git/hooks/pre-commit 2>/dev/null && echo "Manual pre-commit hook exists"

# Check what hooks run
cat .husky/pre-commit 2>/dev/null
cat .pre-commit-config.yaml 2>/dev/null
```

### 3.2 Linting Status

```bash
# JS/TS linting
grep -q "eslint" package.json && echo "ESLint configured"
grep -q "biome" package.json && echo "Biome configured"
ls .eslintrc* biome.json 2>/dev/null

# Python linting
grep -q "ruff" pyproject.toml && echo "Ruff configured"
grep -q "flake8" pyproject.toml setup.cfg && echo "Flake8 configured"
```

### 3.3 Type Checking Status

```bash
# TypeScript
ls tsconfig.json 2>/dev/null && echo "TypeScript configured"
grep "strict" tsconfig.json 2>/dev/null

# Python type checking
grep -q "mypy" pyproject.toml && echo "mypy configured"
grep -q "pyright" pyproject.toml && echo "pyright configured"
ls py.typed 2>/dev/null
```

### 3.4 Commit Message Enforcement

```bash
# commitlint
ls commitlint.config.* 2>/dev/null && echo "commitlint configured"
cat .husky/commit-msg 2>/dev/null
grep "conventional" package.json 2>/dev/null
```

### 3.5 Security Scanning

```bash
# Check for security tools
grep -q "detect-secrets\|trufflehog" .pre-commit-config.yaml package.json 2>/dev/null
ls .github/workflows/*.yml | xargs grep -l "security\|audit" 2>/dev/null
```

---

## Phase 4: Guardrails Setup

**Only add missing guardrails. Never overwrite existing configurations.**

### 4.1 JavaScript/TypeScript Projects

#### Husky + lint-staged (if not present)

```bash
# Check if already installed
if [ ! -d ".husky" ]; then
    # Install Husky
    npm install -D husky lint-staged
    npx husky init

    # Create pre-commit hook
    echo 'npx lint-staged' > .husky/pre-commit
    chmod +x .husky/pre-commit
fi
```

**lint-staged config** (add to package.json if missing):

```json
{
  "lint-staged": {
    "*.{ts,tsx,js,jsx}": [
      "eslint --fix",
      "prettier --write"
    ],
    "*.{json,md,yml,yaml}": [
      "prettier --write"
    ]
  }
}
```

#### ESLint (if not present)

```bash
# Check if eslint exists
if ! grep -q "eslint" package.json; then
    npm install -D eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin
fi
```

**eslint.config.js** (ESLint 9+ flat config):

```javascript
import eslint from '@eslint/js'
import tseslint from 'typescript-eslint'

export default tseslint.config(
  eslint.configs.recommended,
  ...tseslint.configs.recommended,
  {
    rules: {
      '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
      '@typescript-eslint/explicit-function-return-type': 'off',
      'no-console': ['warn', { allow: ['warn', 'error'] }]
    }
  },
  {
    ignores: ['dist/', 'node_modules/', 'coverage/']
  }
)
```

#### Prettier (if not present)

```bash
if ! grep -q "prettier" package.json; then
    npm install -D prettier
fi
```

**.prettierrc** (respect existing style or use sensible defaults):

```json
{
  "semi": false,
  "singleQuote": true,
  "trailingComma": "es5",
  "tabWidth": 2,
  "printWidth": 100
}
```

#### commitlint (if not present)

```bash
if [ ! -f "commitlint.config.js" ]; then
    npm install -D @commitlint/cli @commitlint/config-conventional
    echo "npx commitlint --edit \$1" > .husky/commit-msg
    chmod +x .husky/commit-msg
fi
```

**commitlint.config.js**:

```javascript
export default {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [
      2,
      'always',
      ['feat', 'fix', 'docs', 'style', 'refactor', 'test', 'chore', 'ci', 'perf', 'revert']
    ],
    'subject-case': [2, 'always', 'lower-case'],
    'subject-max-length': [2, 'always', 72]
  }
}
```

### 4.2 Python Projects

#### pre-commit framework (if not present)

```bash
# Install pre-commit
if [ ! -f ".pre-commit-config.yaml" ]; then
    pip install pre-commit
    pre-commit install
fi
```

**.pre-commit-config.yaml**:

```yaml
repos:
  # Ruff - linting and formatting (replaces black, isort, flake8)
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.14.13
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format

  # Type checking
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.16.0
    hooks:
      - id: mypy
        additional_dependencies: [types-requests]
        args: [--ignore-missing-imports]

  # Security
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.5.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']

  # General
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict

  # Commit messages
  - repo: https://github.com/compilerla/conventional-pre-commit
    rev: v4.0.0
    hooks:
      - id: conventional-pre-commit
        stages: [commit-msg]
```

#### pyproject.toml additions (if not present)

```toml
[tool.ruff]
target-version = "py312"
line-length = 100

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "F",   # pyflakes
    "I",   # isort
    "B",   # flake8-bugbear
    "UP",  # pyupgrade
    "S",   # flake8-bandit (security)
]
ignore = ["E501"]  # line length handled by formatter

[tool.mypy]
python_version = "3.12"
strict = true
ignore_missing_imports = true

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --cov=src --cov-report=term-missing --cov-fail-under=80"
```

### 4.3 Branch Protection (Document for User)

Recommend these GitHub branch protection rules:

```markdown
## Recommended Branch Protection (main branch)

1. **Require pull request before merging**
   - Require 1 approval
   - Dismiss stale reviews on new commits

2. **Require status checks**
   - Lint
   - Type check
   - Tests
   - Security scan

3. **Require signed commits** (optional but recommended)

4. **Do not allow bypassing above settings**
```

---

## Phase 5: Structure Preservation Rules

### NEVER Do These

- **Don't reorganize directory structure** - Work within existing patterns
- **Don't rename files for "consistency"** - Match existing naming conventions
- **Don't add new patterns** - Use patterns already in the codebase
- **Don't change import styles** - Match existing (relative vs absolute, etc.)
- **Don't change formatting** - Match existing style or use existing formatter config
- **Don't add new dependencies lightly** - Check if equivalent exists

### ALWAYS Do These

- **Read existing code first** - Understand patterns before writing new code
- **Match existing conventions** - Naming, structure, error handling
- **Use existing utilities** - Don't reinvent what exists
- **Follow existing test patterns** - Match test file naming and structure
- **Preserve existing configs** - Only add, don't modify unless fixing bugs

### Convention Detection Checklist

Before writing any code, identify:

| Convention | Example | Where to Check |
|------------|---------|----------------|
| Naming | camelCase vs snake_case | Existing file names |
| File structure | feature/ vs type/ | Directory layout |
| Export style | default vs named | Existing modules |
| Error handling | throw vs return Error | Existing functions |
| Logging | console vs logger | Existing code |
| Testing | describe/it vs test() | Existing tests |
| Comments | JSDoc vs inline | Existing code |

---

## Phase 6: Analysis Report Template

After running analysis, generate this report:

```markdown
# Repository Analysis Report

## Overview
- **Repo Type**: [Monorepo | Full-Stack | Frontend | Backend | Microservices]
- **Primary Language**: [TypeScript | Python | ...]
- **Framework**: [React | FastAPI | ...]
- **Age**: [X commits, Y contributors]

## Directory Structure
```
[tree output]
```

## Tech Stack
| Category | Technology | Config File |
|----------|------------|-------------|
| Language | TypeScript | tsconfig.json |
| Framework | React | - |
| Testing | Vitest | vitest.config.ts |
| Linting | ESLint | eslint.config.js |
| Formatting | Prettier | .prettierrc |

## Guardrails Status

### Present
- [x] ESLint configured
- [x] Prettier configured
- [x] TypeScript strict mode

### Missing (Recommended)
- [ ] Pre-commit hooks (Husky + lint-staged)
- [ ] Commit message validation (commitlint)
- [ ] Security scanning in CI

## Conventions Detected
| Pattern | Observed | Example |
|---------|----------|---------|
| Naming | camelCase | `getUserById.ts` |
| Imports | Absolute | `@/components/Button` |
| Testing | Colocated | `Button.test.tsx` |
| Exports | Named | `export { Button }` |

## Recommendations
1. Add Husky + lint-staged for pre-commit hooks
2. Add commitlint for conventional commits
3. Add security workflow to GitHub Actions

## Files to Review First
- `src/index.ts` - Main entry point
- `src/utils/` - Shared utilities
- `tests/setup.ts` - Test configuration
```

---

## Gradual Implementation Strategy

Don't add all guardrails at once. Follow this timeline:

| Week | Focus | Why |
|------|-------|-----|
| 1 | Formatting (Prettier/Ruff) | Non-breaking, easy wins |
| 2 | Linting (ESLint/Ruff) | Catches obvious issues |
| 3 | Pre-commit hooks | Automates week 1-2 |
| 4 | Commit message validation | Team consistency |
| 5 | Type checking strictness | Catches runtime errors |
| 6 | Security scanning | Catches vulnerabilities |

---

## Working with Separate Repos

When frontend and backend are in separate repos:

### Frontend Repo Setup

```bash
# Clone and analyze
git clone [frontend-repo]
cd frontend

# Run analysis
# Expect: React/Vue/Angular, no backend code

# Add frontend-specific guardrails
# - Husky + lint-staged
# - ESLint + Prettier
# - Component testing (Vitest/Jest)
```

### Backend Repo Setup

```bash
# Clone and analyze
git clone [backend-repo]
cd backend

# Run analysis
# Expect: FastAPI/Express/Django, no frontend code

# Add backend-specific guardrails
# - pre-commit framework
# - Ruff + mypy
# - API testing (pytest/Jest)
```

### Cross-Repo Coordination

| Concern | Solution |
|---------|----------|
| Shared types | Generate from OpenAPI spec |
| API contracts | Contract testing (Pact) |
| Deployments | Coordinate via CI/CD triggers |
| Versioning | Semantic versioning on both |

---

## Anti-Patterns

- **Adding unused guardrails** - Only add what the team will use
- **Strict rules on day 1** - Introduce gradually
- **Blocking on warnings** - Start permissive, tighten over time
- **Ignoring existing patterns** - Work with what exists
- **Over-engineering** - Simple rules > complex systems
- **Skipping the analysis phase** - Always understand before changing

---

## Quick Reference: Detection Commands

```bash
# One-liner repo analysis
echo "=== Repo Type ===" && \
ls -d packages apps frontend backend 2>/dev/null || echo "Standard repo" && \
echo "=== Tech Stack ===" && \
ls *.json *.toml *.yaml 2>/dev/null && \
echo "=== Existing Guardrails ===" && \
ls .husky .pre-commit-config.yaml .eslintrc* 2>/dev/null || echo "None detected" && \
echo "=== Entry Points ===" && \
ls index.* main.* app.* server.* 2>/dev/null
```
