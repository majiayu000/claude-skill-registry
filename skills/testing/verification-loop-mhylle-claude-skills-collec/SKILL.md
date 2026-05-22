---
name: verification-loop
description: Comprehensive 6-check verification framework for validating implementation quality across build, types, lint, tests, security, and diff review. This skill ensures code meets all quality gates before phase completion. Triggers on "verify implementation", "run verification", "/verification-loop", or automatically as part of implement-phase Step 2.
allowed-tools: Read, Glob, Bash
---

# Verification Loop

A systematic 6-check verification framework that validates implementation quality across multiple dimensions. This skill provides a structured approach to catching issues early, ensuring code compiles, type-checks, passes linting, runs tests, has no security issues, and contains no unintended changes.

> **TERMINOLOGY NOTE**: This skill uses "Checks" (Check 1-6) for its internal verification stages. Do not confuse these with "Phases" (plan phases) or "Steps" (implement-phase steps).

---

## Design Philosophy

### Defense in Depth

Each verification check catches different categories of issues:

| Check | Catches | Why It Matters |
|-------|---------|----------------|
| Build | Syntax errors, missing deps, bundling issues | Code must compile to run |
| Types | Type mismatches, null safety, interface violations | Type safety prevents runtime errors |
| Lint | Style violations, code smells, potential bugs | Consistent, maintainable code |
| Tests | Logic errors, regressions, broken contracts | Functional correctness |
| Security | Secrets, debug code, vulnerable patterns | Production safety |
| Diff | Unintended changes, scope creep, leftover code | Change discipline |

### Fail Fast

Checks are ordered by detection speed. Build errors appear in seconds; security scans may take longer. By running fast checks first, we provide rapid feedback on common issues.

### Project-Agnostic

The framework detects project type automatically and applies appropriate tooling. The same verification loop works for Node.js, Python, Go, Rust, and mixed-language projects.

### Idempotent Execution

Running the verification loop multiple times produces the same result. Each check either passes or fails deterministically based on codebase state.

---

## When to Use This Skill

**Automatically invoked by implement-phase:**
- As Step 2 (Exit Condition Verification)
- Before proceeding to integration testing
- After implementation subagents complete their work

**Manually invoked when:**
- Validating changes before committing
- Checking code quality after refactoring
- Running pre-merge verification
- Debugging CI/CD failures locally

**Do NOT use when:**
- Only reading or analyzing code (no changes made)
- Running exploratory tests (use test runner directly)
- Checking a single file (use individual tools)

---

## Project Type Detection

Before running verification checks, detect the project type to determine appropriate commands.

### Detection Matrix

| Project Type | Primary Indicator | Secondary Indicators |
|--------------|-------------------|----------------------|
| **Node.js/TypeScript** | `package.json` exists | `tsconfig.json`, `node_modules/` |
| **Python** | `pyproject.toml` OR `setup.py` | `requirements.txt`, `.venv/`, `__pycache__/` |
| **Go** | `go.mod` exists | `go.sum`, `*.go` files |
| **Rust** | `Cargo.toml` exists | `Cargo.lock`, `target/` |
| **Mixed/Monorepo** | Multiple indicators | Workspace files, multiple `package.json` |

### Detection Process

```bash
# Check for project type indicators
detect_project_type() {
  if [ -f "package.json" ]; then
    if [ -f "tsconfig.json" ]; then
      echo "typescript"
    else
      echo "nodejs"
    fi
  elif [ -f "pyproject.toml" ] || [ -f "setup.py" ]; then
    echo "python"
  elif [ -f "go.mod" ]; then
    echo "go"
  elif [ -f "Cargo.toml" ]; then
    echo "rust"
  else
    echo "unknown"
  fi
}
```

### Package Manager Detection (Node.js)

```bash
# Determine Node.js package manager
detect_package_manager() {
  if [ -f "pnpm-lock.yaml" ]; then
    echo "pnpm"
  elif [ -f "yarn.lock" ]; then
    echo "yarn"
  elif [ -f "bun.lockb" ]; then
    echo "bun"
  else
    echo "npm"
  fi
}
```

### Python Environment Detection

```bash
# Determine Python tooling
detect_python_tooling() {
  if [ -f "pyproject.toml" ] && grep -q "\[tool.poetry\]" pyproject.toml; then
    echo "poetry"
  elif [ -f "pyproject.toml" ] && grep -q "\[tool.pdm\]" pyproject.toml; then
    echo "pdm"
  elif [ -f "Pipfile" ]; then
    echo "pipenv"
  elif [ -f "pyproject.toml" ]; then
    echo "pip"  # PEP 517/518 compatible
  else
    echo "pip"
  fi
}
```

---

## Check 1: Build Verification

**Purpose**: Ensure the codebase compiles, bundles, and produces valid build artifacts.

### PASS Criteria

- Build command exits with code 0
- No compilation errors
- All build artifacts generated successfully
- No missing dependency errors

### FAIL Criteria

- Non-zero exit code from build command
- Compilation/bundling errors
- Missing or incomplete build artifacts
- Unresolved dependency errors

### Commands by Project Type

#### Node.js / TypeScript

```bash
# Standard build
npm run build

# Or if build script not defined, compile TypeScript
npx tsc --noEmit  # Type check only
npx tsc           # Full compilation

# Common build tools
npx vite build          # Vite
npx next build          # Next.js
npx nest build          # NestJS
npx webpack             # Webpack
npx esbuild src/index.ts --bundle --outdir=dist  # esbuild
```

#### Python

```bash
# Poetry
poetry build

# PDM
pdm build

# pip / setuptools
python -m build

# Check syntax without full build
python -m py_compile src/**/*.py

# Compile to bytecode (catches syntax errors)
python -m compileall src/
```

#### Go

```bash
# Standard build
go build ./...

# With all packages
go build -v ./...

# Check only (no output)
go build -n ./...
```

#### Rust

```bash
# Debug build
cargo build

# Release build
cargo build --release

# Check only (faster)
cargo check
```

### Failure Handling

1. **Parse error output** - Extract specific error locations
2. **Identify root cause** - Missing import? Syntax error? Type mismatch?
3. **Spawn fix subagent** - Provide error context for targeted fix
4. **Re-run build** - Verify fix resolved the issue
5. **Max retries: 3** - Escalate to user if build keeps failing

### Example Output

```
CHECK_1_BUILD_VERIFICATION:
  STATUS: PASS | FAIL
  COMMAND: npm run build
  EXIT_CODE: 0 | [non-zero]
  DURATION: 12.3s
  ARTIFACTS: dist/main.js, dist/main.js.map
  ERRORS: [] | [list of errors]
```

---

## Check 2: Type Verification

**Purpose**: Ensure type safety across the codebase with no type errors.

### PASS Criteria

- Type checker exits with code 0
- No type errors reported
- All type assertions valid
- No missing type definitions

### FAIL Criteria

- Type errors in any file
- Missing type definitions for dependencies
- Invalid type assertions
- Unreachable code detected (in strict mode)

### Commands by Project Type

#### TypeScript

```bash
# Standard type check
npx tsc --noEmit

# With specific config
npx tsc --noEmit --project tsconfig.json

# For monorepos with references
npx tsc --noEmit --build

# NestJS (may have separate tsconfig)
npx tsc --noEmit --project tsconfig.build.json
```

#### Python

```bash
# mypy (standard)
mypy src/

# With config
mypy src/ --config-file pyproject.toml

# pyright (faster, VSCode-compatible)
pyright src/

# Using poetry/pdm
poetry run mypy src/
pdm run mypy src/

# Type checking specific files
mypy src/module.py src/other.py
```

#### Go

```bash
# Go has built-in type checking during build
go build ./...

# Additional static analysis
go vet ./...

# With staticcheck (recommended)
staticcheck ./...
```

#### Rust

```bash
# Rust type checks during compilation
cargo check

# With all features
cargo check --all-features

# For all targets
cargo check --all-targets
```

### Failure Handling

1. **Parse type errors** - Extract file, line, and error message
2. **Categorize errors**:
   - Missing types: Add type annotations
   - Type mismatch: Fix incorrect types
   - Missing definitions: Install @types/* packages
3. **Spawn fix subagent** with type error context
4. **Re-run type check** after fix
5. **Max retries: 3**

### Example Output

```
CHECK_2_TYPE_VERIFICATION:
  STATUS: PASS | FAIL
  COMMAND: npx tsc --noEmit
  EXIT_CODE: 0 | [non-zero]
  DURATION: 8.2s
  FILES_CHECKED: 127
  ERRORS: [] | [
    { file: "src/auth.ts", line: 45, error: "Type 'string' not assignable to 'number'" }
  ]
```

---

## Check 3: Lint Verification

**Purpose**: Ensure code follows style guidelines and catches potential bugs.

### PASS Criteria

- Linter exits with code 0
- No errors (warnings may be acceptable based on config)
- All auto-fixable issues resolved
- Formatting matches project standards

### FAIL Criteria

- Lint errors present
- Unfixable formatting issues
- Security-related lint rules violated
- Complexity thresholds exceeded

### Commands by Project Type

#### Node.js / TypeScript

```bash
# ESLint
npx eslint . --ext .ts,.tsx,.js,.jsx

# With fix (run first to auto-resolve issues)
npx eslint . --ext .ts,.tsx,.js,.jsx --fix

# Prettier (formatting)
npx prettier --check .

# With fix
npx prettier --write .

# Combined (if configured)
npm run lint

# Biome (modern alternative)
npx biome check .
npx biome check . --apply  # auto-fix
```

#### Python

```bash
# Ruff (fast, recommended)
ruff check src/
ruff check src/ --fix

# Ruff formatting
ruff format src/ --check
ruff format src/

# Flake8
flake8 src/

# Black (formatting)
black src/ --check
black src/

# isort (import sorting)
isort src/ --check-only
isort src/

# pylint (comprehensive)
pylint src/

# Using poetry/pdm
poetry run ruff check src/
pdm run ruff check src/
```

#### Go

```bash
# gofmt (formatting)
gofmt -l .
gofmt -w .  # fix

# go vet (static analysis)
go vet ./...

# golangci-lint (comprehensive)
golangci-lint run

# With fix
golangci-lint run --fix
```

#### Rust

```bash
# rustfmt (formatting)
cargo fmt -- --check
cargo fmt  # fix

# clippy (linting)
cargo clippy -- -D warnings

# With all features
cargo clippy --all-features -- -D warnings
```

### Failure Handling

1. **Run auto-fix first** - Resolve mechanical issues automatically
2. **Parse remaining errors** - Categorize by severity
3. **Spawn fix subagent** for non-auto-fixable issues
4. **Re-run lint** after fixes
5. **Max retries: 3**

### Example Output

```
CHECK_3_LINT_VERIFICATION:
  STATUS: PASS | FAIL
  COMMANDS: [
    { cmd: "npm run lint:fix", exit_code: 0 },
    { cmd: "npm run lint", exit_code: 0 }
  ]
  AUTO_FIXED: 12 issues
  REMAINING_ERRORS: 0 | [
    { rule: "no-unused-vars", file: "src/utils.ts", line: 23 }
  ]
  WARNINGS: 3
```

---

## Check 4: Test Verification

**Purpose**: Ensure all tests pass and new code has appropriate coverage.

### PASS Criteria

- All tests pass (exit code 0)
- No skipped tests without documented reason
- Coverage thresholds met (if configured)
- No flaky test failures

### FAIL Criteria

- Any test failure
- Coverage below threshold
- Test timeout
- Test infrastructure errors

### Commands by Project Type

#### Node.js / TypeScript

```bash
# Jest
npm test
npx jest
npx jest --coverage

# Vitest
npx vitest run
npx vitest run --coverage

# Mocha
npx mocha

# Specific test files
npx jest src/auth/__tests__/
npx vitest run src/auth/

# With coverage report
npm test -- --coverage --coverageReporters=text
```

#### Python

```bash
# pytest
pytest
pytest -v
pytest --cov=src

# With specific directory
pytest tests/
pytest tests/unit/ tests/integration/

# Using poetry/pdm
poetry run pytest
pdm run pytest

# unittest (built-in)
python -m unittest discover

# With coverage
coverage run -m pytest
coverage report
```

#### Go

```bash
# Standard test
go test ./...

# Verbose
go test -v ./...

# With coverage
go test -cover ./...
go test -coverprofile=coverage.out ./...

# Specific package
go test -v ./pkg/auth/...
```

#### Rust

```bash
# Standard test
cargo test

# With output
cargo test -- --nocapture

# Specific tests
cargo test auth::
cargo test --package my-crate

# With all features
cargo test --all-features
```

### Failure Handling

1. **Identify failing tests** - Parse test output for failures
2. **Categorize failures**:
   - Test bug: Fix the test
   - Implementation bug: Fix the code
   - Environmental: Fix test setup
3. **Spawn fix subagent** with test failure context
4. **Re-run failing tests** first (faster feedback)
5. **Re-run full suite** after fix
6. **Max retries: 3**

### Example Output

```
CHECK_4_TEST_VERIFICATION:
  STATUS: PASS | FAIL
  COMMAND: npm test
  EXIT_CODE: 0 | [non-zero]
  DURATION: 45.2s
  TESTS_RUN: 156
  TESTS_PASSED: 156 | [count]
  TESTS_FAILED: 0 | [count]
  TESTS_SKIPPED: 2
  COVERAGE: 87.3%
  FAILURES: [] | [
    { test: "should authenticate user", file: "auth.test.ts", error: "Expected 200, got 401" }
  ]
```

---

## Check 5: Security Scan

**Purpose**: Detect secrets, debug code, and security vulnerabilities before code reaches production.

### PASS Criteria

- No hardcoded secrets detected
- No console.log/print statements in production code
- No debug flags enabled
- No known vulnerable dependencies (if scanned)

### FAIL Criteria

- Secrets detected (API keys, passwords, tokens)
- Debug code present (console.log in production paths)
- Debug flags left enabled
- Critical security vulnerabilities in dependencies

### Scan Categories

#### 5a. Secrets Detection

```bash
# Using git-secrets
git secrets --scan

# Using gitleaks
gitleaks detect --source .

# Using trufflehog
trufflehog filesystem .

# Manual patterns to search for
grep -r "API_KEY\|SECRET\|PASSWORD\|TOKEN" src/ --include="*.ts" --include="*.js"
grep -r "sk-\|pk_\|api_key\|secret_key" src/
```

**Common Secret Patterns:**
```
# AWS
AKIA[0-9A-Z]{16}
aws_secret_access_key

# API Keys (generic)
[aA][pP][iI]_?[kK][eE][yY].*=.*['"][a-zA-Z0-9]{20,}['"]

# Private Keys
-----BEGIN (RSA|DSA|EC|OPENSSH) PRIVATE KEY-----

# Tokens
(ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{36,}  # GitHub
xox[baprs]-[0-9a-zA-Z-]+                    # Slack
```

#### 5b. Console/Debug Code Detection

```bash
# JavaScript/TypeScript
grep -rn "console\.log\|console\.debug\|console\.warn\|console\.error" src/ --include="*.ts" --include="*.js" --include="*.tsx" --include="*.jsx"

# Exclude test files
grep -rn "console\.log" src/ --include="*.ts" --exclude="*.test.ts" --exclude="*.spec.ts"

# Python
grep -rn "print(\|pdb\|breakpoint()\|debugger" src/ --include="*.py"

# Go
grep -rn "fmt\.Print\|log\.Print" . --include="*.go"

# Rust
grep -rn "println!\|dbg!\|todo!\|unimplemented!" src/ --include="*.rs"
```

**Allowed Exceptions:**
- Logging framework calls (logger.info, logger.debug)
- Error handling in catch blocks (if configured)
- Test files
- Development-only files

#### 5c. Debug Flag Detection

```bash
# Environment checks
grep -rn "NODE_ENV.*development\|DEBUG.*true\|SKIP_AUTH" src/

# Disabled security
grep -rn "verify.*false\|secure.*false\|https.*false" src/

# TODO/FIXME with security implications
grep -rn "TODO.*security\|FIXME.*auth\|HACK.*bypass" src/
```

#### 5d. Dependency Vulnerability Scan

```bash
# Node.js
npm audit
npm audit --production

# Python
pip-audit
safety check

# Go
govulncheck ./...

# Rust
cargo audit
```

### Failure Handling

1. **Secrets detected**: CRITICAL - Must remove before proceeding
2. **Console logs**: WARNING - Auto-remove or justify with logger
3. **Debug flags**: WARNING - Must disable for production
4. **Vulnerabilities**: Varies by severity (CRITICAL blocks, others warn)

### Example Output

```
CHECK_5_SECURITY_SCAN:
  STATUS: PASS | FAIL
  SCANS_RUN: [
    { scan: "secrets", status: "PASS", findings: 0 },
    { scan: "console_logs", status: "WARN", findings: 3 },
    { scan: "debug_flags", status: "PASS", findings: 0 },
    { scan: "dependencies", status: "PASS", findings: 0 }
  ]
  CRITICAL_FINDINGS: 0 | [count]
  WARNINGS: 3
  DETAILS: [] | [
    { type: "console.log", file: "src/api.ts", line: 45 }
  ]
```

---

## Check 6: Diff Review

**Purpose**: Verify only intended changes are present and no unintended modifications occurred.

### PASS Criteria

- All changes relate to the current phase/task
- No unrelated file modifications
- File count within expected range
- No accidental deletions or additions
- No formatting-only changes to unrelated files

### FAIL Criteria

- Changes outside scope of current work
- Unexpected file additions/deletions
- Modifications to protected files
- Large diffs in files that should have minimal changes

### Review Process

#### 6a. Changed File Inventory

```bash
# List all changed files
git diff --name-only HEAD~1

# With status (added, modified, deleted)
git diff --name-status HEAD~1

# Compared to base branch
git diff --name-only main...HEAD

# With line counts
git diff --stat HEAD~1
```

#### 6b. Scope Verification

```bash
# Expected files based on phase
# (Provided as input to verification)
EXPECTED_PATTERNS=(
  "src/auth/*"
  "tests/auth/*"
  "src/types/auth.ts"
)

# Actual changed files
CHANGED_FILES=$(git diff --name-only HEAD~1)

# Check for unexpected changes
for file in $CHANGED_FILES; do
  matches_expected=false
  for pattern in "${EXPECTED_PATTERNS[@]}"; do
    if [[ $file == $pattern ]]; then
      matches_expected=true
      break
    fi
  done
  if ! $matches_expected; then
    echo "UNEXPECTED: $file"
  fi
done
```

#### 6c. File Count Verification

```bash
# Count changed files
git diff --name-only HEAD~1 | wc -l

# Expected range (provided as input)
MIN_FILES=3
MAX_FILES=15

# Verify within range
COUNT=$(git diff --name-only HEAD~1 | wc -l)
if [ $COUNT -lt $MIN_FILES ] || [ $COUNT -gt $MAX_FILES ]; then
  echo "WARNING: Changed $COUNT files, expected $MIN_FILES-$MAX_FILES"
fi
```

#### 6d. Protected Files Check

```bash
# Files that should not be modified without explicit approval
PROTECTED_FILES=(
  "package-lock.json"
  ".env*"
  "*.lock"
  "docker-compose.yml"
  "Dockerfile"
  ".github/workflows/*"
)

# Check for protected file changes
for file in $CHANGED_FILES; do
  for protected in "${PROTECTED_FILES[@]}"; do
    if [[ $file == $protected ]]; then
      echo "PROTECTED FILE CHANGED: $file"
    fi
  done
done
```

#### 6e. Diff Size Analysis

```bash
# Get diff stats
git diff --stat HEAD~1

# Flag large diffs
git diff --numstat HEAD~1 | while read added deleted file; do
  total=$((added + deleted))
  if [ $total -gt 500 ]; then
    echo "LARGE DIFF: $file (+$added -$deleted)"
  fi
done
```

### Failure Handling

1. **Unexpected files**: Review if changes are valid
   - Valid: Update expected scope
   - Invalid: Revert unintended changes
2. **Protected files**: Require explicit approval
3. **Large diffs**: Review for scope creep
4. **Missing expected files**: Investigate incomplete implementation

### Example Output

```
CHECK_6_DIFF_REVIEW:
  STATUS: PASS | FAIL
  FILES_CHANGED: 8
  EXPECTED_RANGE: 5-12
  SCOPE_VIOLATIONS: 0 | [list]
  PROTECTED_FILES_CHANGED: 0 | [list]
  LARGE_DIFFS: 0 | [list]
  SUMMARY: [
    { type: "added", count: 3 },
    { type: "modified", count: 4 },
    { type: "deleted", count: 1 }
  ]
  DETAILS: [
    { file: "src/auth/auth.service.ts", status: "M", lines: "+45 -12" },
    { file: "src/auth/auth.guard.ts", status: "A", lines: "+78 -0" }
  ]
```

---

## Integration with implement-phase

When invoked as Step 2 of implement-phase, this skill runs all 6 verification checks and returns a structured result.

### Input Context

```
VERIFICATION_INPUT:
  phase_number: 2
  phase_name: "Authentication Service"
  plan_path: docs/plans/auth-implementation.md
  expected_file_patterns: ["src/auth/*", "tests/auth/*"]
  expected_file_range: [5, 15]
  protected_files: ["package-lock.json", ".env"]
  skip_checks: []  # Optional: skip specific checks
```

### Output Format

```
VERIFICATION_LOOP_STATUS: PASS | FAIL
CHECKS_RUN: 6
CHECKS_PASSED: 6 | [count]
CHECKS_FAILED: 0 | [count]
FAILED_CHECKS: [] | [
  {
    check: 1,
    name: "build",
    error: "TypeScript compilation failed",
    details: "src/auth.ts(45): error TS2322: Type 'string' not assignable..."
  }
]
REPORT:
  check_1_build:
    status: PASS
    duration: 12.3s
  check_2_types:
    status: PASS
    duration: 8.2s
  check_3_lint:
    status: PASS
    auto_fixed: 12
    duration: 5.1s
  check_4_tests:
    status: PASS
    tests_run: 156
    tests_passed: 156
    coverage: 87.3%
    duration: 45.2s
  check_5_security:
    status: PASS
    secrets_found: 0
    console_logs: 0
    duration: 3.4s
  check_6_diff:
    status: PASS
    files_changed: 8
    scope_violations: 0
    duration: 1.2s
TOTAL_DURATION: 75.4s

═══════════════════════════════════════════════════════════════
⚡ ACTION REQUIRED: IMMEDIATELY EXECUTE STEP 3 (Integration Testing)
   DO NOT wait for user input. DO NOT ask for confirmation.
   YOU MUST proceed to Step 3 NOW as your next action.
═══════════════════════════════════════════════════════════════
```

> **CRITICAL INSTRUCTION TO AI**: When VERIFICATION_LOOP_STATUS is PASS, you MUST:
> 1. Output the above ACTION REQUIRED block exactly as shown
> 2. **IMMEDIATELY** proceed to Step 3 (Automated Integration Testing) as your very next action
> 3. **DO NOT** wait for user input or confirmation
> 4. **DO NOT** ask "shall I proceed?" or similar questions
>
> This is a direct instruction to execute, not information to display. Treat this like a function call that must happen automatically.

### Implement-Phase Integration Point

```
implement-phase pipeline:

Step 1: Implementation (subagents)
        ↓
Step 2: VERIFICATION-LOOP (this skill) ←
        ├── Check 1: Build
        ├── Check 2: Types
        ├── Check 3: Lint
        ├── Check 4: Tests
        ├── Check 5: Security
        └── Check 6: Diff Review
        ↓
Step 3: Automated Integration Testing
        ↓
Step 4: Code Review
        ↓
...
```

### Retry Logic

implement-phase handles retry logic:

```
1. INVOKE verification-loop
2. IF any check FAILS:
   a. IDENTIFY failure type
   b. SPAWN fix subagent with failure context
   c. Re-run verification-loop (or just failed checks)
   d. REPEAT until PASS (max 3 retries per check)
3. IF all checks PASS:
   a. PROCEED to Step 3 (Integration Testing)
```

---

## Standalone Invocation

### Command Line

```
/verification-loop

# With specific checks
/verification-loop checks:build,types,tests

# Skip checks
/verification-loop skip:security,diff

# Specific project path
/verification-loop path:./packages/auth
```

### Interactive

```
/verification-loop

> Running verification loop...
>
> Check 1: Build Verification
>   Command: npm run build
>   Status: PASS (12.3s)
>
> Check 2: Type Verification
>   Command: npx tsc --noEmit
>   Status: PASS (8.2s)
>
> Check 3: Lint Verification
>   Command: npm run lint
>   Auto-fixed: 12 issues
>   Status: PASS (5.1s)
>
> Check 4: Test Verification
>   Command: npm test
>   Tests: 156 passed, 0 failed
>   Coverage: 87.3%
>   Status: PASS (45.2s)
>
> Check 5: Security Scan
>   Secrets: 0 found
>   Console logs: 0 found
>   Status: PASS (3.4s)
>
> Check 6: Diff Review
>   Files changed: 8
>   Scope violations: 0
>   Status: PASS (1.2s)
>
> ═══════════════════════════════════════
> VERIFICATION COMPLETE: ALL CHECKS PASSED
> Duration: 75.4s
> ═══════════════════════════════════════
>
> ═══════════════════════════════════════════════════════════════
> ⚡ ACTION REQUIRED: IMMEDIATELY EXECUTE STEP 3 (Integration Testing)
>    DO NOT wait for user input. DO NOT ask for confirmation.
>    YOU MUST proceed to Step 3 NOW as your next action.
> ═══════════════════════════════════════════════════════════════
```

---

## Configuration

### Project-Level Configuration

The verification loop auto-detects project type and uses appropriate defaults. Override specific checks via project config if needed:

```json
// package.json or .verification.json
{
  "verification": {
    "checks": {
      "build": { "command": "<command>", "timeout": "<ms>" },
      "types": { "command": "<command>", "timeout": "<ms>" },
      "lint": { "command": "<command>", "autoFix": "<bool>" },
      "tests": { "command": "<command>", "coverage": { "threshold": "<percent>" } },
      "security": {
        "scanSecrets": "<bool>",
        "scanConsoleLogs": "<bool>",
        "excludePatterns": ["<glob-patterns>"]
      },
      "diff": {
        "protectedFiles": ["<glob-patterns>"],
        "maxFileCount": "<number>"
      }
    }
  }
}
```

```toml
# pyproject.toml or .verification.toml
[tool.verification]
checks.build.command = "<command>"
checks.types.command = "<command>"
checks.lint.command = "<command>"
checks.lint.auto_fix = <bool>
checks.tests.command = "<command>"
checks.tests.coverage_threshold = <percent>
checks.security.scan_secrets = <bool>
checks.security.exclude_patterns = ["<glob-patterns>"]
```

### Environment Variables

```bash
# Skip specific checks
VERIFICATION_SKIP_CHECKS=<comma-separated-check-names>

# Set timeouts
VERIFICATION_BUILD_TIMEOUT=<ms>
VERIFICATION_TEST_TIMEOUT=<ms>

# Security scan configuration
VERIFICATION_SECRETS_SCAN=<bool>
VERIFICATION_CONSOLE_LOG_SCAN=<bool>
```

---

## Best Practices

### For Check Authors

1. **Order checks by speed** - Fast checks first for rapid feedback
2. **Make checks independent** - Each check should run in isolation
3. **Provide clear error messages** - Include file, line, and fix suggestions
4. **Support auto-fix** - Automate mechanical fixes where possible
5. **Cache when possible** - Avoid redundant work across runs

### For Verification Consumers

1. **Run locally before commit** - Catch issues before CI
2. **Trust the verification** - If it passes, proceed confidently
3. **Fix root causes** - Don't skip checks; fix the underlying issues
4. **Review security warnings** - Even non-blocking findings need attention
5. **Keep scope tight** - Large diffs often indicate scope creep

### For CI/CD Integration

1. **Run full verification** - Don't skip checks in CI
2. **Cache dependencies** - Speed up build/install checks
3. **Parallelize when possible** - Some checks can run concurrently
4. **Fail fast** - Stop on first failure to save CI time
5. **Report clearly** - Surface which check failed and why

---

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Build fails with missing deps | node_modules out of sync | Run `npm install` first |
| Type errors in node_modules | Wrong @types versions | Update or remove conflicting @types |
| Lint auto-fix causes more errors | Conflicting rules | Review ESLint/Prettier config |
| Tests timeout | Slow tests or hanging processes | Increase timeout or fix test |
| Security scan false positive | Valid use of flagged pattern | Add to exclude list with comment |
| Diff scope violation | Unrelated file touched | Review and revert or expand scope |

### Debug Mode

Run verification with verbose output:

```
/verification-loop --verbose

# Or set environment
VERIFICATION_DEBUG=true /verification-loop
```

---

## References

- [implement-phase SKILL.md](../implement-phase/SKILL.md) - Parent skill that invokes verification-loop
- [code-review SKILL.md](../code-review/SKILL.md) - Follows verification-loop in the pipeline
- [security-review SKILL.md](../security-review/SKILL.md) - Deep security analysis (beyond Check 5)

---

## Appendix: Quick Reference

### Check Summary

| Check | Purpose | Commands | Blocks On |
|-------|---------|----------|-----------|
| 1. Build | Compilation | `npm run build`, `cargo build` | Any error |
| 2. Types | Type safety | `tsc --noEmit`, `mypy` | Any error |
| 3. Lint | Code quality | `eslint`, `ruff` | Errors (not warnings) |
| 4. Tests | Correctness | `npm test`, `pytest` | Any failure |
| 5. Security | Production safety | Custom scans | Secrets, critical vulns |
| 6. Diff | Change discipline | `git diff` analysis | Scope violations |

### Minimum Viable Verification

For quick verification (e.g., pre-commit hook):

```bash
# Fast path: build + types + lint
npm run build && npx tsc --noEmit && npm run lint
```

### Full Verification

For complete verification (e.g., pre-merge):

```bash
# All 6 checks
npm run build && \
npx tsc --noEmit && \
npm run lint && \
npm test && \
npm run security:scan && \
./scripts/verify-diff.sh
```
