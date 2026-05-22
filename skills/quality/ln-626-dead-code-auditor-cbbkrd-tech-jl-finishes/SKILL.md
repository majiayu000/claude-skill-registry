---
name: ln-626-dead-code-auditor
description: Dead code & legacy audit worker (L3). Checks unreachable code, unused imports/variables/functions, commented-out code, backward compatibility shims, deprecated patterns. Returns findings.
allowed-tools: Read, Grep, Glob, Bash
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# Dead Code Auditor (L3 Worker)

Specialized worker auditing unused and unreachable code.

## Purpose & Scope

- **Worker in ln-620 coordinator pipeline**
- Audit **dead code** (Category 9: Low Priority)
- Find unused imports, variables, functions, commented-out code
- Calculate compliance score (X/10)

## Inputs (from Coordinator)

Receives `contextStore` with tech stack, codebase root, output_dir.

## Workflow

1) Parse context + output_dir
2) Run dead code detection (linters, grep)
3) Collect findings
4) Calculate score
5) **Write Report:** Build full markdown report in memory per `shared/templates/audit_worker_report_template.md`, write to `{output_dir}/626-dead-code.md` in single Write call
6) **Return Summary:** Return minimal summary to coordinator

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

**MANDATORY READ:** Load `shared/references/audit_scoring.md` for unified scoring formula.

## Output Format

**MANDATORY READ:** Load `shared/templates/audit_worker_report_template.md` for file format.

Write report to `{output_dir}/626-dead-code.md` with `category: "Dead Code"` and checks: unreachable_code, unused_exports, commented_code, legacy_shims.

Return summary to coordinator:
```
Report written: docs/project/.audit/626-dead-code.md
Score: X.X/10 | Issues: N (C:N H:N M:N L:N)
```

## Reference Files

- **Worker report template:** `shared/templates/audit_worker_report_template.md`
- **Clean code checklist:** `shared/references/clean_code_checklist.md`
- **Audit scoring formula:** `shared/references/audit_scoring.md`
- **Audit output schema:** `shared/references/audit_output_schema.md`

## Critical Rules

- **Do not auto-fix:** Report only, never delete code
- **Age-aware severity:** Legacy shims >6 months = MEDIUM, <3 months = LOW
- **Effort realism:** S = <1h, M = 1-4h, L = >4h
- **Exclusions:** Skip generated code, vendor, migrations, test fixtures
- **Git-aware:** Recommend deletion confidently -- git history preserves old code

## Definition of Done

- contextStore parsed (including output_dir)
- All 4 checks completed (unreachable code, unused imports/vars/functions, commented-out code, legacy shims)
- Clean code checklist loaded from `shared/references/clean_code_checklist.md`
- Findings collected with severity, location, effort, recommendation
- Score calculated per `shared/references/audit_scoring.md`
- Report written to `{output_dir}/626-dead-code.md` (atomic single Write call)
- Summary returned to coordinator

---
**Version:** 3.0.0
**Last Updated:** 2025-12-23
