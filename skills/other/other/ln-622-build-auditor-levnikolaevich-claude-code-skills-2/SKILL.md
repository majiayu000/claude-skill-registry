---
name: ln-622-build-auditor
description: "Checks compiler/linter errors, deprecation warnings, type errors, failed tests, build config issues. Use when auditing build health."
allowed-tools: Read, Grep, Glob, Bash
license: MIT
model: claude-sonnet-4-6
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

# Build Health Auditor (L3 Worker)

**Type:** L3 Worker

Specialized worker auditing build health and code quality tooling.

## Purpose & Scope

- **Worker in codebase audit pipeline**
- Audit codebase for **build health issues** (Category 2: Critical Priority)
- Check compiler/linter errors, deprecation warnings, type errors, failed tests, build config
- Return structured findings to coordinator with severity, location, effort, recommendations
- Calculate compliance score (X/10) for Build Health category

## Inputs

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md`.

Receives `contextStore` with: `tech_stack` (including build_tool, test_framework), `best_practices`, `principles`, `codebase_root`, `output_dir`.

## Workflow

**MANDATORY READ:** Load `shared/references/two_layer_detection.md` for detection methodology.

1) **Parse Context:** Extract tech stack, build tools, test framework, output_dir from contextStore
2) **Run Build Checks (Layer 1):** Execute compiler, linter, type checker, tests (see Audit Rules below)
3) **Analyze Output Context (Layer 2):** For deprecation warnings -- read notice to determine if removal is imminent or distant. For config issues -- check if dev-only or production config.
4) **Collect Findings:** Record each violation with severity, location, effort, recommendation
5) **Calculate Score:** Count violations by severity, calculate compliance score (X/10)
6) **Write Report:** Build full markdown report in memory per `shared/templates/audit_worker_report_template.md`, write to `{output_dir}/ln-622--global.md` in single Write call
7) **Trend Tracking:** Append build_health metric to results_log per `shared/references/results_log_pattern.md`. Metric: `build_health | 0-10 | penalty formula`. Calculate delta and status (improving/stable/declining) vs previous run.
8) **Return Summary:** Return minimal summary to coordinator (see Output Format)

## Audit Rules (Priority: CRITICAL)

**MANDATORY READ:** Load `shared/references/ci_tool_detection.md` for build commands, linter commands, type checker commands, and test framework commands per ecosystem.

### 1. Compiler/Linter Errors
**What:** Syntax errors, compilation failures, linter rule violations

**Detection:** Use ci_tool_detection.md Command Registry (Build + Linters sections). Check exit code, parse stderr for errors. Use JSON output flags where available.

**Linters:** Use ci_tool_detection.md Linters table. Use `--format json` / `--output-format json` for structured output.

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

**Detection:** Use ci_tool_detection.md Command Registry (Type Checkers section).

**Severity:**
- **CRITICAL:** Type error prevents compilation (`tsc` fails, `cargo check` fails)
- **HIGH:** Runtime type error likely (implicit `any`, missing type guards)
- **MEDIUM:** Missing type annotations (code works but untyped)
- **LOW:** Overly permissive types (`any`, `unknown` without narrowing)

**Recommendation:** Add type annotations, enable strict mode, use type guards

**Effort:** S-M (add types to single file vs refactor entire module)

### 4. Failed or Skipped Tests
**What:** Test suite failures, skipped tests, missing test coverage

**Detection:** Use ci_tool_detection.md Command Registry (Test Frameworks section). Use JSON output flags for structured parsing.

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

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md` and `shared/references/audit_scoring.md`.

## Output Format

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md` and `shared/templates/audit_worker_report_template.md`.

Write JSON summary per `shared/references/audit_summary_contract.md`. In managed mode the caller passes both `runId` and `summaryArtifactPath`; in standalone mode the worker generates its own run-scoped artifact path per shared contract.

Write report to `{output_dir}/ln-622--global.md` with `category: "Build Health"` and checks: compilation_errors, linter_warnings, type_errors, test_failures, build_config.

Return summary per `shared/references/audit_summary_contract.md`.

When `summaryArtifactPath` is absent, write the standalone runtime summary under `.hex-skills/runtime-artifacts/runs/{run_id}/audit-worker/{worker}--{identifier}.json` and optionally echo the same summary in structured output.
```
Report written: .hex-skills/runtime-artifacts/runs/{run_id}/audit-report/ln-622--global.md
Score: X.X/10 | Issues: N (C:N H:N M:N L:N)
```

## Critical Rules

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md`.

- **Do not auto-fix:** Report violations only; coordinator creates task for user to fix
- **Tech stack aware:** Use contextStore to run appropriate build commands (npm vs cargo vs gradle)
- **Exit code checking:** Always check exit code (0 = success, non-zero = failure)
- **Timeout handling:** Set timeout for build/test commands (default 5 minutes)
- **Environment aware:** Run in CI mode if detected (no interactive prompts)

## Definition of Done

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md`.

- [ ] contextStore parsed successfully (including output_dir)
- [ ] All 5 build checks completed (compiler, linter, type checker, tests, config)
- [ ] Findings collected with severity, location, effort, recommendation
- [ ] Score calculated using penalty algorithm
- [ ] Report written to `{output_dir}/ln-622--global.md` (atomic single Write call)
- [ ] build_health metric appended to results_log with trend status
- [ ] Summary written per contract

## Reference Files

- **Audit output schema:** `shared/references/audit_output_schema.md`
- **CI tool detection:** `shared/references/ci_tool_detection.md`
- **Results log pattern:** `shared/references/results_log_pattern.md`
- Build audit rules: [references/build_rules.md](references/build_rules.md)

---
**Version:** 3.0.0
**Last Updated:** 2025-12-23
