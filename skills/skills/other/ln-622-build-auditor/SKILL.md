---
name: ln-622-build-auditor
description: Build health audit worker (L3). Checks compiler/linter errors, deprecation warnings, type errors, failed tests, build configuration issues. Returns findings with severity (Critical/High/Medium/Low), location, effort, and recommendations.
allowed-tools: Read, Grep, Glob, Bash
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# Build Health Auditor (L3 Worker)

Specialized worker auditing build health and code quality tooling.

## Purpose & Scope

- **Worker in ln-620 coordinator pipeline** - invoked by ln-620-codebase-auditor
- Audit codebase for **build health issues** (Category 2: Critical Priority)
- Check compiler/linter errors, deprecation warnings, type errors, failed tests, build config
- Return structured findings to coordinator with severity, location, effort, recommendations
- Calculate compliance score (X/10) for Build Health category

## Inputs (from Coordinator)

**MANDATORY READ:** Load `shared/references/task_delegation_pattern.md#audit-coordinator--worker-contract` for contextStore structure.

Receives `contextStore` with: `tech_stack` (including build_tool, test_framework), `best_practices`, `principles`, `codebase_root`, `output_dir`.

## Workflow

1) **Parse Context:** Extract tech stack, build tools, test framework, output_dir from contextStore
2) **Run Build Checks:** Execute compiler, linter, type checker, tests (see Audit Rules below)
3) **Collect Findings:** Record each violation with severity, location, effort, recommendation
4) **Calculate Score:** Count violations by severity, calculate compliance score (X/10)
5) **Write Report:** Build full markdown report in memory per `shared/templates/audit_worker_report_template.md`, write to `{output_dir}/622-build.md` in single Write call
6) **Return Summary:** Return minimal summary to coordinator (see Output Format)

## Audit Rules (Priority: CRITICAL)

### 1. Compiler/Linter Errors
**What:** Syntax errors, compilation failures, linter rule violations

**Detection:** Per `shared/references/ci_tool_detection.md` Command Registry (Build + Linters sections). Check exit code, parse stderr for errors. Use JSON output flags where available.

**Linters:** Per ci_tool_detection.md Linters table. Use `--format json` / `--output-format json` for structured output.

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

**Detection:** Per `shared/references/ci_tool_detection.md` Command Registry (Type Checkers section).

**Severity:**
- **CRITICAL:** Type error prevents compilation (`tsc` fails, `cargo check` fails)
- **HIGH:** Runtime type error likely (implicit `any`, missing type guards)
- **MEDIUM:** Missing type annotations (code works but untyped)
- **LOW:** Overly permissive types (`any`, `unknown` without narrowing)

**Recommendation:** Add type annotations, enable strict mode, use type guards

**Effort:** S-M (add types to single file vs refactor entire module)

### 4. Failed or Skipped Tests
**What:** Test suite failures, skipped tests, missing test coverage

**Detection:** Per `shared/references/ci_tool_detection.md` Command Registry (Test Frameworks section). Use JSON output flags for structured parsing.

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

**MANDATORY READ:** Load `shared/references/audit_scoring.md` for unified scoring formula.

## Output Format

**MANDATORY READ:** Load `shared/templates/audit_worker_report_template.md` for file format.

Write report to `{output_dir}/622-build.md` with `category: "Build Health"` and checks: compilation_errors, linter_warnings, type_errors, test_failures, build_config.

Return summary to coordinator:
```
Report written: docs/project/.audit/ln-620/{YYYY-MM-DD}/622-build.md
Score: X.X/10 | Issues: N (C:N H:N M:N L:N)
```

## Critical Rules

- **Do not auto-fix:** Report violations only; coordinator creates task for user to fix
- **Tech stack aware:** Use contextStore to run appropriate build commands (npm vs cargo vs gradle)
- **Exit code checking:** Always check exit code (0 = success, non-zero = failure)
- **Timeout handling:** Set timeout for build/test commands (default 5 minutes)
- **Environment aware:** Run in CI mode if detected (no interactive prompts)

## Definition of Done

- contextStore parsed successfully (including output_dir)
- All 5 build checks completed (compiler, linter, type checker, tests, config)
- Findings collected with severity, location, effort, recommendation
- Score calculated using penalty algorithm
- Report written to `{output_dir}/622-build.md` (atomic single Write call)
- Summary returned to coordinator

## Reference Files

- **Worker report template:** `shared/templates/audit_worker_report_template.md`
- **Audit scoring formula:** `shared/references/audit_scoring.md`
- **Audit output schema:** `shared/references/audit_output_schema.md`
- Build audit rules: [references/build_rules.md](references/build_rules.md)

---
**Version:** 3.0.0
**Last Updated:** 2025-12-23
