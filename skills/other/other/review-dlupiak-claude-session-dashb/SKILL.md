---
name: review
description: Code review current changes against project standards
user-invocable: true
---

# Code Review

Review all uncommitted changes against project standards.

## Steps

### 1. Gather Changes
```bash
git diff
git diff --cached
git status --short
```

### 2. Review Criteria

For each changed file, check:

**Architecture**
- Follows Vertical Slice Architecture (no cross-slice imports except via `src/lib/`)
- No `/services`, `/utils`, `/controllers` directories created
- Feature code in the correct slice

**TypeScript**
- No `any` types (use `unknown` + type guards)
- Proper error handling with typed errors
- Zod schemas for external data validation

**React**
- Components use named exports
- Server vs client boundary is correct
- No unnecessary `useEffect` for data fetching (use TanStack Query)

**Security**
- No secrets in code
- No path traversal in filesystem reads (all reads scoped to `~/.claude`)
- Server function return values validated with Zod

### 3. Report

Output a structured review:

```
## Review Summary
- Files reviewed: N
- Issues found: N (critical: N, warning: N, info: N)

## Issues
### [CRITICAL/WARNING/INFO] filename:line — description
```

### 4. Suggest Fixes
For each critical or warning issue, provide a specific fix suggestion.
