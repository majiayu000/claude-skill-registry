---
name: debt-scan
description: Scan codebase for known anti-patterns and technical debt
user-invocable: true
disable-model-invocation: true
---

# /debt-scan — Technical Debt Scanner

Scan the codebase for all known anti-patterns from `.claude/rules/anti-patterns*.md` files. Produce a report with counts, locations, and trend comparison.

## Scan Checklist

Run these Grep searches across `src/` and report counts:

### General Anti-Patterns
1. **`as any`** — Grep for `as any` in `*.ts,*.tsx` (type safety violation)
2. **`Record<string, unknown>`** — Grep for `Record<string, unknown>` (untyped payloads)
3. **`db: any`** — Grep for `db: any` (untyped database)
4. **`console.log`** — Grep for `console.log` in `src/server/` (use logger)
5. **`console.error`** — Grep for `console.error` in `src/server/` (use logger)
6. **`export *`** — Grep for `export \*` (breaks tree-shaking)
7. **`await import(`** — Grep for `await import\(` in `src/` (dynamic imports)

### React/Next.js Anti-Patterns
8. **`forwardRef`** — Grep for `forwardRef` (React 19 doesn't need it)
9. **`getServerSideProps`** — Grep for `getServerSideProps` (App Router doesn't use it)
10. **`useContext` in tRPC** — Grep for `trpc.useContext()` (deprecated, use useUtils)

### tRPC/Drizzle Anti-Patterns
11. **`queryClient.invalidate`** — Grep for `queryClient.invalidate` (use utils.x.invalidate)
12. **`ctx.db` without comment** — Grep for `ctx.db` outside repositories (should use ctx.uow)
13. **Sequential await** — Grep for patterns like `await.*\n.*await` that could be parallel

### Security Anti-Patterns
14. **Missing ownerId scope** — Grep for queries without `ownerId` filter
15. **`dangerouslySetInnerHTML`** — Grep for `dangerouslySetInnerHTML`

## Output Format

After running all scans, produce a summary table:

```
| # | Anti-Pattern | Count | Files |
|---|-------------|-------|-------|
| 1 | as any | 3 | router.ts, helper.ts, ... |
```

Save results to `.claude/instincts/debt-scan.json`:
```json
{
  "date": "2026-02-26",
  "total_issues": 15,
  "by_pattern": { "as_any": 3, "console_log": 5, ... },
  "trend": "improving"  // compare against previous scan if exists
}
```

## Trend Comparison

If a previous `debt-scan.json` exists, compare counts and report:
- Patterns that improved (count decreased)
- Patterns that regressed (count increased)
- New patterns detected
