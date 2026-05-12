<!-- SOURCE-OF-TRUTH: shared/references/clean_code_checklist.md. Edit ONLY here; run `node tools/marketplace/shared.mjs sync` -->

# Clean Code Checklist

Universal patterns for detecting dead code, backward-compat shims, and legacy remnants.

## 4 Dead Code Categories

### 1. Unreachable Code

Code after `return`/`throw`/`break`; dead branches (always-true/false conditions).

**Severity:** MEDIUM

### 2. Unused Code

| What | Severity |
|------|----------|
| Unused functions, classes, methods | MEDIUM |
| Unused exports (exported but never imported) | MEDIUM |
| Unused imports, variables, parameters | LOW |

### 3. Commented-Out Code

Large code blocks in comments (>5 lines with code syntax). Git preserves history — delete, don't comment.

**Severity:** LOW

### 4. Backward-Compat & Legacy

| Pattern | Example | Severity |
|---------|---------|----------|
| Old aliases | `const oldName = newName` | medium |
| Wrapper functions | `function oldFunc() { return newFunc() }` | medium |
| Unsupported re-exports | `export { newModule as oldModule }` | medium |
| Migration shims/adapters | `LegacyAdapter`, `*Compat`, `*Shim` | high if critical path |
| Version conditionals | `if (isOldVersion) { oldFunc() }` | medium |
| Legacy naming | `_old*`, `_legacy*`, `_compat*`, `_unsupported*` | medium |
| Legacy markers in comments | `// backward compat`, `// unsupported`, `// TODO: remove in v` | low |

## Replacement Rule

When implementation replaces old code:

1. Delete old implementation entirely
2. Update ALL callers to use new API
3. Remove old signatures (don't alias)
4. Remove re-exports of old names
5. Delete adapter/shim files

**Anti-pattern:** keeping old code "just in case" — git history preserves it.

## Exceptions

| Exception | When OK |
|-----------|---------|
| Published packages (npm/NuGet) | Unsupported API cycle required (major version bump) |
| Active migration (<3 months) | Clear removal timeline documented |
| External API contract | Consumers not yet migrated (tracked as tech debt) |

## Quick Checklist

```
[] No unused imports/variables/functions
[] No commented-out code blocks (>5 lines)
[] No backward-compat wrappers or aliases
[] No unsupported re-exports
[] No _old/_legacy/_compat naming
[] All callers updated to new API
[] Old files deleted (not just emptied)
```

---
**Version:** 1.0.0
**Last Updated:** 2026-02-08
