---
name: ln-622-build-auditor
description: Build health audit worker (L3). Checks compiler/linter errors, deprecation warnings, type errors, failed tests, build configuration issues. Returns findings with severity (Critical/High/Medium/Low), location, effort, and recommendations.
allowed-tools: Read, Grep, Glob, Bash
---

# Build Health Auditor (L3 Worker)

Specialized worker auditing build health and code quality tooling.

## Purpose & Scope

- **Worker in ln-620 coordinator pipeline** - invoked by ln-620-codebase-auditor
- Audit codebase for **build health issues** (Category 2: Critical Priority)
- Check compiler/linter errors, deprecation warnings, type errors, failed tests, build config
- Return structured findings to coordinator with severity, location, effort, recommendations
- Calculate compliance score (X/10) for Build Health category

## Inputs (from Coordinator)

Receives `contextStore` as JSON string:
```json
{
  "tech_stack": {
    "language": "TypeScript",
    "build_tool": "Webpack",
    "test_framework": "Jest",
    ...
  },
  "best_practices": {...},
  "principles": {...},
  "codebase_root": "/path/to/project"
}
```

## Workflow

1) **Parse Context:** Extract tech stack, build tools, test framework from contextStore
2) **Run Build Checks:** Execute compiler, linter, type checker, tests (see Audit Rules below)
3) **Collect Findings:** Record each violation with severity, location, effort, recommendation
4) **Calculate Score:** Count violations by severity, calculate compliance score (X/10)
5) **Return Results:** Return JSON with category, score, findings to coordinator

## Audit Rules (Priority: CRITICAL)

### 1. Compiler/Linter Errors
**What:** Syntax errors, compilation failures, linter rule violations

**Detection by Stack:**

| Stack | Command | Error Detection |
|-------|---------|-----------------|
| Node.js/TypeScript | `npm run build` or `tsc --noEmit` | Check exit code, parse stderr for errors |
| Python | `python -m py_compile *.py` | Check exit code, parse stderr |
| Go | `go build ./...` | Check exit code, parse stderr |
| Rust | `cargo build` | Check exit code, parse stderr |
| Java | `mvn compile` | Check exit code, parse build log |

**Linters:**
- ESLint (JS/TS): `npx eslint . --format json` → parse JSON for errors
- Pylint (Python): `pylint **/*.py --output-format=json`
- RuboCop (Ruby): `rubocop --format json`
- golangci-lint (Go): `golangci-lint run --out-format json`

**Severity:**
- **CRITICAL:** Compilation fails, cannot build project
- **HIGH:** Linter errors (not warnings)
- **MEDIUM:** Linter warnings
- **LOW:** Stylistic linter warnings (formatting)

**Recommendation:** Fix errors before proceeding, configure linter rules, add pre-commit hooks

**Effort:** S-M (fix syntax error vs refactor code structure)

### 2. Deprecation Warnings
**What:** Usage of deprecated APIs, libraries, or language features

**Detection:**
- Compiler warnings: `DeprecationWarning`, `@deprecated` in stack trace
- Dependency warnings: `npm outdated`, `pip list --outdated`
- Static analysis: Grep for `@deprecated` annotations

**Severity:**
- **CRITICAL:** Deprecated API removed in next major version (imminent breakage)
- **HIGH:** Deprecated with migration path available
- **MEDIUM:** Deprecated but still supported for 1+ year
- **LOW:** Soft deprecation (no removal timeline)

**Recommendation:** Migrate to recommended API, update dependencies, refactor code

**Effort:** M-L (depends on API complexity and usage frequency)

### 3. Type Errors
**What:** Type mismatches, missing type annotations, type checker failures

**Detection by Stack:**

| Stack | Tool | Command |
|-------|------|---------|
| TypeScript | tsc | `tsc --noEmit --strict` |
| Python | mypy | `mypy . --strict` |
| Python | pyright | `pyright --warnings` |
| Go | go vet | `go vet ./...` |
| Rust | cargo | `cargo check` (type checks only) |

**Severity:**
- **CRITICAL:** Type error prevents compilation (`tsc` fails, `cargo check` fails)
- **HIGH:** Runtime type error likely (implicit `any`, missing type guards)
- **MEDIUM:** Missing type annotations (code works but untyped)
- **LOW:** Overly permissive types (`any`, `unknown` without narrowing)

**Recommendation:** Add type annotations, enable strict mode, use type guards

**Effort:** S-M (add types to single file vs refactor entire module)

### 4. Failed or Skipped Tests
**What:** Test suite failures, skipped tests, missing test coverage

**Detection by Stack:**

| Stack | Framework | Command |
|-------|-----------|---------|
| Node.js | Jest | `npm test -- --json --outputFile=test-results.json` |
| Node.js | Mocha | `mocha --reporter json > test-results.json` |
| Python | Pytest | `pytest --json-report --json-report-file=test-results.json` |
| Go | go test | `go test ./... -json` |
| Rust | cargo test | `cargo test --no-fail-fast` |

**Severity:**
- **CRITICAL:** Test failures in CI/production code
- **HIGH:** Skipped tests for critical features (payment, auth)
- **MEDIUM:** Skipped tests for non-critical features
- **LOW:** Skipped tests with "TODO" comment (acknowledged debt)

**Recommendation:** Fix failing tests, remove skip markers, add missing tests

**Effort:** S-M (update test assertion vs redesign test strategy)

### 5. Build Configuration Issues
**What:** Misconfigured build tools, missing scripts, incorrect paths

**Detection:**
- Missing build scripts in `package.json`, `Makefile`, `build.gradle`
- Incorrect paths in `tsconfig.json`, `webpack.config.js`, `Cargo.toml`
- Missing environment-specific configs (dev, staging, prod)
- Unused or conflicting build dependencies

**Severity:**
- **CRITICAL:** Build fails due to misconfiguration
- **HIGH:** Build succeeds but outputs incorrect artifacts (wrong target, missing assets)
- **MEDIUM:** Suboptimal config (no minification, missing source maps)
- **LOW:** Unused config options

**Recommendation:** Fix config paths, add missing build scripts, optimize build settings

**Effort:** S-M (update config file vs redesign build pipeline)

## Scoring Algorithm

```
violations = {critical: N, high: M, medium: K, low: L}

penalty = (critical * 2.0) + (high * 1.0) + (medium * 0.5) + (low * 0.2)

score = max(0, 10 - penalty)
```

**Examples:**
- 0 violations → 10/10
- 1 critical (build fails) → 8/10
- 2 critical, 5 high → 3/10
- 10 high, 20 medium → 0/10

## Output Format

Return JSON to coordinator:
```json
{
  "category": "Build Health",
  "score": 7,
  "total_issues": 5,
  "critical": 1,
  "high": 2,
  "medium": 2,
  "low": 0,
  "findings": [
    {
      "severity": "CRITICAL",
      "location": "src/utils/helper.ts:45",
      "issue": "TypeScript error: Type 'string' is not assignable to type 'number'",
      "principle": "Type Safety",
      "recommendation": "Fix type mismatch: change 'id: string' to 'id: number' or update usage",
      "effort": "S"
    },
    {
      "severity": "HIGH",
      "location": "tests/api.test.ts:112",
      "issue": "Test failed: Expected 200, received 404",
      "principle": "Test Quality",
      "recommendation": "Update API endpoint or fix test assertion",
      "effort": "M"
    }
  ]
}
```

## Critical Rules

- **Do not auto-fix:** Report violations only; coordinator creates task for user to fix
- **Tech stack aware:** Use contextStore to run appropriate build commands (npm vs cargo vs gradle)
- **Exit code checking:** Always check exit code (0 = success, non-zero = failure)
- **Timeout handling:** Set timeout for build/test commands (default 5 minutes)
- **Environment aware:** Run in CI mode if detected (no interactive prompts)

## Definition of Done

- contextStore parsed successfully
- All 5 build checks completed (compiler, linter, type checker, tests, config)
- Findings collected with severity, location, effort, recommendation
- Score calculated using penalty algorithm
- JSON result returned to coordinator

## Reference Files

- Build audit rules: [references/build_rules.md](references/build_rules.md)

---
**Version:** 3.0.0
**Last Updated:** 2025-12-23
