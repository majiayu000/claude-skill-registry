---
name: linting-complete
description: Complete linting workflow from setup to fix. Use when setting up linting in a project, running lint checks, fixing linting issues, or as part of quality gates. Covers setup, detection, auto-fix, manual fix, and scope management. Triggers on "lint", "fix linting", "setup linter", "code quality", "formatting".
---

# Linting Complete

## Purpose

Complete linting workflow: from initial setup to fixing issues. Ensures code quality and consistency across the project.

**Workflow:** Setup → Detect → Check → Fix → Verify

## When to Use

- Setting up linting in a new project
- Running lint checks before commit
- Fixing linting issues
- Configuring code formatting
- Part of quality gates

**When NOT to use:**
- Quick format on save (IDE handles this)
- After quality gates passed (use skill-quality-gates)
- CI/CD setup (different configuration)

## Quick Start

```bash
# Complete workflow
1. Detect environment and existing setup
2. Install missing tools
3. Run lint check
4. Auto-fix what possible
5. Manual fix remaining
6. Verify clean state
```

## Phase 1: Setup & Detection

### Detect Project Type

```bash
# Detect language and framework
if [ -f "package.json" ]; then
    PROJECT_TYPE="nodejs"
    # Check for TypeScript
    if [ -f "tsconfig.json" ]; then
        LANGUAGE="typescript"
    else
        LANGUAGE="javascript"
    fi
elif [ -f "requirements.txt" ] || [ -f "pyproject.toml" ]; then
    PROJECT_TYPE="python"
elif [ -f "Cargo.toml" ]; then
    PROJECT_TYPE="rust"
elif [ -f "build.gradle.kts" ]; then
    PROJECT_TYPE="kotlin"
fi
```

### Detect Existing Linting Setup

| File | Tool | Status |
|------|------|--------|
| `.eslintrc.js` | ESLint | ✅ Configured |
| `biome.json` | Biome | ✅ Configured |
| `ruff.toml` | Ruff | ✅ Configured |
| `.pylintrc` | Pylint | ✅ Configured |
| `.prettierrc` | Prettier | ✅ Configured |
| `.editorconfig` | EditorConfig | ✅ Configured |

### Check Installed Tools

```bash
# Node.js projects
if [ -f "package.json" ]; then
    # Check for linting tools in devDependencies
    if grep -q "eslint" package.json; then
        echo "✓ ESLint found"
    fi
    if grep -q "prettier" package.json; then
        echo "✓ Prettier found"
    fi
    if grep -q "@biomejs/biome" package.json; then
        echo "✓ Biome found"
    fi
    if grep -q "oxlint" package.json; then
        echo "✓ oxlint found"
    fi
fi
```

## Phase 2: Install Missing Tools

### Node.js / TypeScript

**Option A: Biome (Recommended - Fast, All-in-One)**

```bash
npm install --save-dev @biomejs/biome
```

Create `biome.json`:
```json
{
  "$schema": "https://biomejs.dev/schemas/1.5.3/schema.json",
  "organizeImports": {
    "enabled": true
  },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true
    }
  },
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 100
  }
}
```

Add to `package.json`:
```json
{
  "scripts": {
    "lint": "biome check .",
    "lint:fix": "biome check --write .",
    "format": "biome format --write ."
  }
}
```

**Option B: ESLint + Prettier (Traditional)**

```bash
npm install --save-dev eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin prettier eslint-config-prettier
```

Create `.eslintrc.js`:
```javascript
module.exports = {
  parser: '@typescript-eslint/parser',
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'prettier',
  ],
  parserOptions: {
    ecmaVersion: 2020,
    sourceType: 'module',
  },
  rules: {
    '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
    '@typescript-eslint/explicit-function-return-type': 'off',
  },
};
```

Create `.prettierrc`:
```json
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2
}
```

**Option C: Advanced Stack (Biome + oxlint + secretlint)**

```bash
npm install --save-dev @biomejs/biome oxlint secretlint @secretlint/secretlint-rule-preset-recommend
```

Create `.secretlintrc.json`:
```json
{
  "rules": [
    {
      "id": "@secretlint/secretlint-rule-preset-recommend"
    }
  ]
}
```

Update `package.json`:
```json
{
  "scripts": {
    "lint": "biome check . && oxlint . && secretlint .",
    "lint:fix": "biome check --write . && oxlint --fix .",
    "format": "biome format --write ."
  }
}
```

### Python

**Ruff (Modern, Fast - Recommended)**

```bash
pip install ruff
```

Create `ruff.toml`:
```toml
line-length = 88
indent-width = 4
target-version = "py311"

[lint]
select = ["E", "F", "W", "I", "N", "UP", "B", "A", "C4", "T20"]
fixable = ["ALL"]

[format]
quote-style = "double"
indent-style = "space"
```

Or add to `pyproject.toml`:
```toml
[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "W", "I", "N", "UP", "B", "A", "C4", "T20"]

[tool.ruff.format]
quote-style = "double"
```

### Kotlin

**ktlint + Detekt**

Add to `build.gradle.kts`:
```kotlin
plugins {
    id("org.jlleitschuh.gradle.ktlint") version "11.6.1"
    id("io.gitlab.arturbosch.detekt") version "1.23.3"
}

ktlint {
    version.set("1.0.1")
    android.set(false)
    outputToConsole.set(true)
}

detekt {
    buildUponDefaultConfig = true
    allRules = false
    config.setFrom(files("$projectDir/config/detekt/detekt.yml"))
}
```

## Phase 3: Scope Management

### CRITICAL: Modified Files vs Unchanged Files

**Files You Modify:**
- ✅ MUST fix ALL errors
- ✅ MUST fix warnings OR justify with inline comment
- ✅ Style issues: auto-fix with formatter

**Files You Don't Touch:**
- Not your responsibility
- Don't auto-fix (would change too many files)
- Create tracking issue if critical

### Identify Changed Files

```bash
# Get files changed in current branch
CHANGED_FILES=$(git diff --name-only --diff-filter=ACMRTUXB main | grep -E '\.(ts|tsx|js|jsx|py|kt)$')

# Lint only changed files
npm run lint -- $CHANGED_FILES
# or
ruff check $CHANGED_FILES
```

## Phase 4: Run Lint Check

### Execute Linter

```bash
# Full project
npm run lint
# or
ruff check .
# or
./gradlew ktlintCheck detekt
```

### Review Output

**Example ESLint Output:**
```
src/auth.ts
  12:5   error    'token' is assigned a value but never used    @typescript-eslint/no-unused-vars
  23:10  warning  Unexpected console statement                   no-console
  45:1   error    Missing return type on function                @typescript-eslint/explicit-function-return-type

✖ 3 problems (2 errors, 1 warning)
  1 error and 0 warnings potentially fixable with the `--fix` option
```

**Example Ruff Output:**
```
src/parser.py:12:5: F841 Local variable `data` is assigned to but never used
src/parser.py:23:10: E501 Line too long (105 > 88 characters)
src/parser.py:45:1: D103 Missing docstring in public function
Found 3 errors.
```

## Phase 5: Auto-Fix

### Run Auto-Fix

```bash
# TypeScript/JavaScript
npm run lint:fix
# or
npx eslint . --ext .ts,.tsx --fix
# or
npx @biomejs/biome check --write .

# Python
ruff check --fix .
ruff format .

# Kotlin
./gradlew ktlintFormat
```

### What Gets Auto-Fixed

✅ **Safe to auto-fix:**
- Formatting (spacing, indentation, line breaks)
- Import sorting
- Missing semicolons
- Quote style consistency
- Trailing whitespace
- Unused imports (sometimes)

❌ **Requires manual fix:**
- Unused variables (logic issue)
- Missing return types (design issue)
- Complex logic issues
- API misuse

## Phase 6: Manual Fix

### Common Issues & Solutions

**Unused Variables:**
```typescript
// Before (error)
function processData(input: string, token: string) {
  return input.toUpperCase();
}

// Fix 1: Use the variable
function processData(input: string, token: string) {
  validateToken(token);
  return input.toUpperCase();
}

// Fix 2: Remove if not needed
function processData(input: string) {
  return input.toUpperCase();
}

// Fix 3: Prefix with _ if intentionally unused
function processData(input: string, _token: string) {
  return input.toUpperCase();
}
```

**Missing Return Types:**
```typescript
// Before (error)
function calculateTotal(items) {
  return items.reduce((sum, item) => sum + item.price, 0);
}

// Fix: Add types
function calculateTotal(items: Item[]): number {
  return items.reduce((sum, item) => sum + item.price, 0);
}
```

**Line Too Long:**
```python
# Before (error - 120 chars)
user_data = fetch_user_from_database(user_id, include_profile=True, include_preferences=True, include_history=True)

# Fix: Break into multiple lines
user_data = fetch_user_from_database(
    user_id,
    include_profile=True,
    include_preferences=True,
    include_history=True
)
```

### Handle Exceptions (Inline Disables)

**TypeScript:**
```typescript
// eslint-disable-next-line @typescript-eslint/no-explicit-any -- Legacy API requires any type
function handleLegacyResponse(data: any): void {
  // ...
}
```

**Python:**
```python
# ruff: noqa: E501 -- URL is long and cannot be broken
LEGACY_API_URL = "https://api.example.com/v1/very/long/path/that/cannot/be/shortened"
```

**Kotlin:**
```kotlin
@Suppress("MagicNumber") // Port numbers are inherently magic
const val DEFAULT_PORT = 8080
```

**Rules for Exceptions:**
- ✅ Always include comment explaining WHY
- ✅ Be specific (one rule, not all)
- ✅ Use inline disables, not file-level
- ✅ Consider better fix first
- ❌ Never disable just to avoid fixing

## Phase 7: Verify Clean State

### Re-Run Linter

```bash
npm run lint        # TypeScript
ruff check .        # Python
./gradlew ktlintCheck  # Kotlin
```

Expected output:
```
✓ No linting errors found
```

### Check Formatting

```bash
npm run format:check    # TypeScript
ruff format --check .   # Python
```

## Integration with Quality Gates

After linting passes, proceed to:

| Next Step | Skill |
|-----------|-------|
| Unit/Integration Tests | skill-testing-workflow |
| E2E Testing | skill-testsprite-pre-pr |
| Complete Quality Gates | skill-quality-gates |

## Best Practices

### IDE Integration

**VSCode settings.json:**
```json
{
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff"
  }
}
```

### Pre-Commit Hooks

```bash
npm install --save-dev husky lint-staged
npx husky install
```

`.husky/pre-commit`:
```bash
#!/bin/sh
npm run lint
npm run test
```

### Legacy Code Strategy

**Option 1: Fix All (Small Projects)**
```bash
npm run lint:fix
ruff check --fix .
```

**Option 2: Baseline (Large Projects)**
```bash
# Generate baseline
ruff check --output-format=json > .ruff-baseline.json
```

Document in README:
```markdown
## Linting
We use [tool] for code quality. Legacy code has a baseline -
new code must pass all checks.
```

## Output Confirmation

```
✓ Linter configured: [biome/eslint/ruff]
✓ Lint command works: [npm run lint/ruff check]
✓ No errors in modified files (MANDATORY)
✓ Warnings fixed or justified
✓ Formatting consistent
```

## Version

v1.0.0 (2025-01-28) - Complete linting workflow