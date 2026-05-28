---
name: ln-626-dead-code-pruning-auditor
description: "Finds code that can be safely deleted: unreachable, unused, obsolete compatibility, and commented-out code. Use when pruning dead code."
allowed-tools: Read, Grep, Glob, Bash, mcp__hex-graph__index_project, mcp__hex-graph__audit_workspace, mcp__hex-line__read_file, mcp__hex-line__grep_search, mcp__hex-line__outline
license: MIT
---

> **Paths:** File paths (`references/`, `../ln-*`) are relative to this skill directory.

# Dead Code Pruning Auditor (L3 Worker)

**Type:** L3 Worker

Specialized worker identifying safe deletion candidates.

## Purpose & Scope

- Audit **dead code pruning** (Category 9: Low Priority)
- Find unused imports, variables, functions, commented-out code
- Emit `DELETE_DEAD_CODE`, `REMOVE_OBSOLETE_COMPAT`, or `DELETE_COMMENTED_CODE`
- Calculate compliance score (X/10)

## Inputs

**MANDATORY READ:** Load `references/audit_worker_core_contract.md`.
Tool policy: follow host AGENTS.md MCP preferences; load `references/mcp_tool_preferences.md` and `references/mcp_integration_patterns.md` only when host policy is absent or MCP behavior is unclear.

Receives `contextStore` with tech stack, codebase root, output_dir.

Use `hex-graph` first when export liveness or workspace hotspots materially improve the audit. Use `hex-line` first for local code reads when available. If MCP is unavailable, unsupported, or not indexed, continue with built-in `Read/Grep/Glob/Bash` and state the fallback in the report.

## Workflow

Detection policy: use two-layer detection (candidate scan, then context verification); load `references/two_layer_detection.md` only when the verification method is ambiguous.

1) Parse context + output_dir
2) Run dead code detection (Layer 1: linters, grep)
   - **Graph-capable projects:** For JavaScript, TypeScript/TSX, Python, C#, and PHP, use `index_project` then bounded `audit_workspace(verbosity="minimal", limit=5)` as primary detection for unused exports when graph indexing is available. Raise `limit` only for deliberate drill-down.
   - Keep grep/linter fallback for unsupported languages, graph-unavailable runs, and checks outside export liveness.
3) Analyze context per candidate (Layer 2):
   - Unused functions: used via dynamic import/reflection? Exported in public API? Used in other packages (monorepo)?
   - Commented code: TODO with context or algorithm explanation -> FP. Truly dead code block -> confirmed
   - Legacy shims: read git blame -- age? Is there an issue/PR tracking removal?
4) Collect confirmed findings
5) Calculate score
6) **Write Report:** Build full markdown report in memory per `references/templates/audit_worker_report_template.md`, write to `{output_dir}/ln-626--global.md` in single Write call
7) **Return Summary:** Return minimal summary

## Audit Rules

**MANDATORY READ:** Load `references/clean_code_checklist.md` for universal dead code patterns and severity definitions.

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
**What:** Backward compatibility shims, unsupported patterns, old code that should be removed

**Detection:**
- Renamed variables/functions with old aliases:
  - Pattern: `const oldName = newName` or `export { newModule as oldModule }`
  - Pattern: `function oldFunc() { return newFunc(); }` (wrapper for backward compatibility)
- Unsupported exports/re-exports:
  - Grep for `// DEPRECATED`, `@obsolete` JSDoc tags
  - Pattern: `export.*as.*old.*` or `export.*legacy.*`
- Conditional code for old versions:
  - Pattern: `if.*legacy.*` or `if.*old.*version.*` or `isOldVersion ? oldFunc() : newFunc()`
- Migration shims and adapters:
  - Pattern: `migrate.*`, `Legacy.*Adapter`, `.*Shim`, `.*Compat`
- Comment markers:
  - Grep for `// backward compatibility`, `// legacy support`, `// TODO: remove in v`
  - Grep for `// old implementation`, `// unsupported`, `// kept for backward`

**Severity:**
- **HIGH:** Backward compatibility shims in critical paths (auth, payment, core features)
- **MEDIUM:** Unsupported exports still in use, migration code from >6 months ago
- **LOW:** Recent migration code (<3 months), planned deprecation with clear removal timeline

**Recommendation:**
- Remove backward compatibility shims - breaking changes are acceptable when properly versioned
- Delete old implementations - keep only the correct/new version
- Remove unsupported exports - update consumers to use new API
- Delete migration code after grace period (3-6 months)
- Clean legacy support comments - git history preserves old implementations

**Effort:**
- **S:** Remove simple aliases, delete unsupported exports
- **M:** Refactor code using old APIs to new APIs
- **L:** Remove complex backward compatibility layer affecting multiple modules

## Scoring Algorithm

**MANDATORY READ:** Load `references/audit_scoring.md`.

## Output Format

**MANDATORY READ:** Load `references/templates/audit_worker_report_template.md`.

Write JSON summary per `references/audit_summary_contract.md`. In managed mode the caller passes both `runId` and `summaryArtifactPath`; in standalone mode the worker generates its own run-scoped artifact path per shared contract.

Write report to `{output_dir}/ln-626--global.md` with `category: "Dead Code Pruning"` and checks: unreachable_code, unused_exports, commented_code, legacy_shims.

Return summary per `references/audit_summary_contract.md`.

When `summaryArtifactPath` is absent, write the standalone runtime summary under `.hex-skills/runtime-artifacts/runs/{run_id}/evaluation-worker/{worker}--{identifier}.json` and optionally echo the same summary in structured output.
```
Report written: .hex-skills/runtime-artifacts/runs/{run_id}/audit-report/ln-626--global.md
Score: X.X/10 | Issues: N (C:N H:N M:N L:N)
```

## Reference Files

- **Clean code checklist:** `references/clean_code_checklist.md`
- **Audit output schema:** `references/audit_output_schema.md`

## Critical Rules

Apply the already-loaded `references/audit_worker_core_contract.md`.

- **Do not auto-fix:** Report only, never delete code
- **Age-aware severity:** Legacy shims >6 months = MEDIUM, <3 months = LOW
- **Effort realism:** S = <1h, M = 1-4h, L = >4h
- **Exclusions:** Skip generated code, vendor, migrations, test fixtures
- **Git-aware:** Recommend deletion confidently -- git history preserves old code
- **Unique angle:** Audit safe deletion candidates only. Do not refactor live code, restructure modules, or assess dependency/package health.
- **Action required:** Every finding uses `DELETE_DEAD_CODE`, `REMOVE_OBSOLETE_COMPAT`, or `DELETE_COMMENTED_CODE`.

## Definition of Done

Apply the already-loaded `references/audit_worker_core_contract.md`.

- [ ] contextStore parsed (including output_dir)
- [ ] All 4 checks completed (unreachable code, unused imports/vars/functions, commented-out code, legacy shims)
- [ ] Clean code checklist loaded from `references/clean_code_checklist.md`
- [ ] Findings collected with severity, location, effort, action, recommendation
- [ ] Score calculated per `references/audit_scoring.md`
- [ ] Report written to `{output_dir}/ln-626--global.md` (atomic single Write call)
- [ ] Summary written per contract

---
**Version:** 3.0.0
**Last Updated:** 2025-12-23
