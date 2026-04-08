---
name: ln-626-dead-code-auditor
description: "Checks unreachable code, unused imports/variables/functions, commented-out code, deprecated patterns. Use when auditing dead code."
allowed-tools: Read, Grep, Glob, Bash, mcp__hex-graph__index_project, mcp__hex-graph__audit_workspace
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

# Dead Code Auditor (L3 Worker)

**Type:** L3 Worker

Specialized worker auditing unused and unreachable code.

## Purpose & Scope

- Audit **dead code** (Category 9: Low Priority)
- Find unused imports, variables, functions, commented-out code
- Calculate compliance score (X/10)

## Inputs

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md`.

Receives `contextStore` with tech stack, codebase root, output_dir.

## Workflow

**MANDATORY READ:** Load `shared/references/two_layer_detection.md` for detection methodology.

1) Parse context + output_dir
2) Run dead code detection (Layer 1: linters, grep)
   - **Graph-capable projects:** For JavaScript, TypeScript/TSX, Python, C#, and PHP, use `index_project` then `audit_workspace(verbosity="full")` as primary detection for unused exports when graph indexing is available.
   - Keep grep/linter fallback for unsupported languages, graph-unavailable runs, and checks outside export liveness.
3) Analyze context per candidate (Layer 2):
   - Unused functions: used via dynamic import/reflection? Exported in public API? Used in other packages (monorepo)?
   - Commented code: TODO with context or algorithm explanation -> FP. Truly dead code block -> confirmed
   - Legacy shims: read git blame -- age? Is there an issue/PR tracking removal?
4) Collect confirmed findings
5) Calculate score
6) **Write Report:** Build full markdown report in memory per `shared/templates/audit_worker_report_template.md`, write to `{output_dir}/ln-626--global.md` in single Write call
7) **Return Summary:** Return minimal summary to coordinator

## Audit Rules

**MANDATORY READ:** Load `shared/references/clean_code_checklist.md` for universal dead code patterns and severity definitions.

### 1. Unreachable Code
**Detection:**
- Linter rules: `no-unreachable` (ESLint)
- Check code after `return`, `throw`, `break`

**Severity:** MEDIUM

### 2. Unused Imports/Variables/Functions
**Detection:**
- ESLint: `no-unused-vars`
- TypeScript: `noUnusedLocals`, `noUnusedParameters`
- Python: `flake8` with `F401`, `F841`

**Severity:**
- **MEDIUM:** Unused functions (dead weight)
- **LOW:** Unused imports (cleanup needed)

### 3. Commented-Out Code
**Detection:**
- Grep for `//.*{` or `/*.*function` patterns
- Large comment blocks (>10 lines) with code syntax

**Severity:** LOW

**Recommendation:** Delete (git preserves history)

### 4. Legacy Code & Backward Compatibility
**What:** Backward compatibility shims, deprecated patterns, old code that should be removed

**Detection:**
- Renamed variables/functions with old aliases:
  - Pattern: `const oldName = newName` or `export { newModule as oldModule }`
  - Pattern: `function oldFunc() { return newFunc(); }` (wrapper for backward compatibility)
- Deprecated exports/re-exports:
  - Grep for `// DEPRECATED`, `@deprecated` JSDoc tags
  - Pattern: `export.*as.*old.*` or `export.*legacy.*`
- Conditional code for old versions:
  - Pattern: `if.*legacy.*` or `if.*old.*version.*` or `isOldVersion ? oldFunc() : newFunc()`
- Migration shims and adapters:
  - Pattern: `migrate.*`, `Legacy.*Adapter`, `.*Shim`, `.*Compat`
- Comment markers:
  - Grep for `// backward compatibility`, `// legacy support`, `// TODO: remove in v`
  - Grep for `// old implementation`, `// deprecated`, `// kept for backward`

**Severity:**
- **HIGH:** Backward compatibility shims in critical paths (auth, payment, core features)
- **MEDIUM:** Deprecated exports still in use, migration code from >6 months ago
- **LOW:** Recent migration code (<3 months), planned deprecation with clear removal timeline

**Recommendation:**
- Remove backward compatibility shims - breaking changes are acceptable when properly versioned
- Delete old implementations - keep only the correct/new version
- Remove deprecated exports - update consumers to use new API
- Delete migration code after grace period (3-6 months)
- Clean legacy support comments - git history preserves old implementations

**Effort:**
- **S:** Remove simple aliases, delete deprecated exports
- **M:** Refactor code using old APIs to new APIs
- **L:** Remove complex backward compatibility layer affecting multiple modules

## Scoring Algorithm

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md` and `shared/references/audit_scoring.md`.

## Output Format

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md` and `shared/templates/audit_worker_report_template.md`.

Write JSON summary per `shared/references/audit_summary_contract.md`. In managed mode the caller passes both `runId` and `summaryArtifactPath`; in standalone mode the worker generates its own run-scoped artifact path per shared contract.

Write report to `{output_dir}/ln-626--global.md` with `category: "Dead Code"` and checks: unreachable_code, unused_exports, commented_code, legacy_shims.

Return summary per `shared/references/audit_summary_contract.md`.

When `summaryArtifactPath` is absent, write the standalone runtime summary under `.hex-skills/runtime-artifacts/runs/{run_id}/audit-worker/{worker}--{identifier}.json` and optionally echo the same summary in structured output.
```
Report written: .hex-skills/runtime-artifacts/runs/{run_id}/audit-report/ln-626--global.md
Score: X.X/10 | Issues: N (C:N H:N M:N L:N)
```

## Reference Files

- **Clean code checklist:** `shared/references/clean_code_checklist.md`
- **Audit output schema:** `shared/references/audit_output_schema.md`

## Critical Rules

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md`.

- **Do not auto-fix:** Report only, never delete code
- **Age-aware severity:** Legacy shims >6 months = MEDIUM, <3 months = LOW
- **Effort realism:** S = <1h, M = 1-4h, L = >4h
- **Exclusions:** Skip generated code, vendor, migrations, test fixtures
- **Git-aware:** Recommend deletion confidently -- git history preserves old code

## Definition of Done

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md`.

- [ ] contextStore parsed (including output_dir)
- [ ] All 4 checks completed (unreachable code, unused imports/vars/functions, commented-out code, legacy shims)
- [ ] Clean code checklist loaded from `shared/references/clean_code_checklist.md`
- [ ] Findings collected with severity, location, effort, recommendation
- [ ] Score calculated per `shared/references/audit_scoring.md`
- [ ] Report written to `{output_dir}/ln-626--global.md` (atomic single Write call)
- [ ] Summary written per contract

---
**Version:** 3.0.0
**Last Updated:** 2025-12-23
