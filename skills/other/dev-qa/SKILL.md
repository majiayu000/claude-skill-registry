---
name: dev-qa
description: Run QA checks on current work. Tests, linting, type checking, build verification. Use during or after development to catch issues early.
---

# Dev QA - Quality Assurance Checks

Run all quality checks: Tests → Lint → Types → Build

## Philosophy

"Find bugs before they find users. Run QA early, run it often."

## Flow

### 1. Detect Project Type

```bash
# Check what we're working with
[ -f "package.json" ] && echo "node"
[ -f "Cargo.toml" ] && echo "rust"
[ -f "pyproject.toml" ] || [ -f "requirements.txt" ] && echo "python"
[ -f "go.mod" ] && echo "go"
```

### 2. Run Checks (by project type)

#### Node/TypeScript
```bash
# Tests
npm test 2>&1 || yarn test 2>&1 || pnpm test 2>&1

# Lint
npm run lint 2>&1 || npx eslint . 2>&1

# Type check
npx tsc --noEmit 2>&1

# Build
npm run build 2>&1
```

#### Rust
```bash
# Tests
cargo test 2>&1

# Lint
cargo clippy -- -D warnings 2>&1

# Format check
cargo fmt --check 2>&1

# Build
cargo build 2>&1
```

#### Python
```bash
# Tests
pytest 2>&1 || python -m pytest 2>&1

# Lint
ruff check . 2>&1 || flake8 . 2>&1

# Type check
mypy . 2>&1 || pyright . 2>&1

# Format check
black --check . 2>&1 || ruff format --check . 2>&1
```

#### Go
```bash
# Tests
go test ./... 2>&1

# Lint
golangci-lint run 2>&1

# Build
go build ./... 2>&1
```

### 3. Report Results

Format output as:

```
## QA Report

### Tests
✓ Passed: 42
✗ Failed: 2
⊘ Skipped: 1

Failed tests:
- test_user_auth: AssertionError at line 45
- test_token_refresh: Timeout

### Lint
✓ No issues

### Type Check
⚠ 3 warnings:
- src/auth.ts:12 - Type 'any' used
- src/utils.ts:34 - Implicit return type

### Build
✓ Build successful

### Summary
Status: FAILING
Must fix: 2 test failures
Should fix: 3 type warnings
```

### 4. Next Steps

Based on results:

**If all pass:**
```
QA passed! Ready for:
- /dev-security - Security audit
- /dev-rc - Release candidate prep
- /dev-finish - Close the cycle
```

**If failures:**
```
QA found issues.

Options:
1. Fix now (I'll help)
2. Fix manually, run /dev-qa again
3. Continue anyway (not recommended)
```

If "Fix now":
- Delegate to Bob: "Fix these QA issues: {list}"
- Re-run QA after fixes
- Loop until clean

## Quick Mode

For a fast check (CI-style):
```
/dev-qa quick
```

Runs only:
- Tests
- Lint
- Build

Skips:
- Verbose output
- Interactive fixing
- Type checking (if slow)

## Integration with Dev Cycle

If active dev-cycle session exists:
- Log QA results to session file
- Update session phase if QA passes

```markdown
## QA History
- 2024-01-15 14:30: FAILED (2 test failures)
- 2024-01-15 14:45: PASSED
```

## What We Check

| Check | Why |
|-------|-----|
| Tests | Does it work? |
| Lint | Is it clean? |
| Types | Is it safe? |
| Build | Does it compile? |

## Agent Involvement

- **Bob**: Fixes code issues found by QA
- **Arlo**: Reviews if test failures involve data/calculations
