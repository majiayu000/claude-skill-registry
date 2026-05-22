---
name: ln-626-dead-code-auditor
description: Dead code & legacy audit worker (L3). Checks unreachable code, unused imports/variables/functions, commented-out code, backward compatibility shims, deprecated patterns. Returns findings.
allowed-tools: Read, Grep, Glob, Bash
---

# Dead Code Auditor (L3 Worker)

Specialized worker auditing unused and unreachable code.

## Purpose & Scope

- **Worker in ln-620 coordinator pipeline**
- Audit **dead code** (Category 9: Low Priority)
- Find unused imports, variables, functions, commented-out code
- Calculate compliance score (X/10)

## Inputs (from Coordinator)

Receives `contextStore` with tech stack, codebase root.

## Workflow

1) Parse context
2) Run dead code detection (linters, grep)
3) Collect findings
4) Calculate score
5) Return JSON

## Audit Rules

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

```
penalty = (high * 1.0) + (medium * 0.5) + (low * 0.2)
score = max(0, 10 - penalty)
```

## Output Format

```json
{
  "category": "Dead Code",
  "score": 6,
  "total_issues": 12,
  "high": 2,
  "medium": 3,
  "low": 7,
  "findings": [
    {
      "severity": "MEDIUM",
      "location": "src/utils/helpers.ts:45",
      "issue": "Function 'formatDate' is never used",
      "principle": "Code Maintainability / Clean Code",
      "recommendation": "Remove unused function or export if needed elsewhere",
      "effort": "S"
    },
    {
      "severity": "HIGH",
      "location": "src/api/v1/auth.ts:12-15",
      "issue": "Backward compatibility shim for old password validation (6+ months old)",
      "principle": "No Legacy Code / Clean Architecture",
      "recommendation": "Remove old password validation, keep only new implementation. Update API version if breaking.",
      "effort": "M"
    }
  ]
}
```

---
**Version:** 3.0.0
**Last Updated:** 2025-12-23
