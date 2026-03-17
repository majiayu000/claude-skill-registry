---
name: performance-check
description: Analyze code for performance anti-patterns and run performance tests. Checks for N+1 queries, unbounded queries, missing indexes, and response time regressions.
---

# Performance Check Skill

Comprehensive performance verification combining static code analysis and runtime testing to detect performance issues before shipping.

## When to Use

- Adding or modifying API routes with database queries
- Before shipping features that touch data-heavy paths
- Investigating slow endpoints
- Manual check with `/performance-check`

## Instructions

### Phase 1: Analyze Changed Files

**Goal**: Identify files that need performance analysis

```bash
# Get changed file list
git status --short

# Get file paths only
git diff --name-only HEAD

# Categorize by type
git diff --name-only HEAD | grep -E "^app/api/|^src/api/" | head -20
git diff --name-only HEAD | grep -E "^src/components/" | head -20
git diff --name-only HEAD | grep -E "^hooks/|^lib/" | head -20
```

**Categorize files**:
- API routes: `app/api/**/*.ts` or `src/api/**/*.ts` - Primary focus
- Components: `src/components/**/*.tsx` - Check data fetching patterns
- Hooks: `hooks/**/*.ts` - Check caching configurations
- Utilities: `lib/**/*.ts` - Check query helpers

---

### Phase 2: Static Code Analysis [BLOCKING/WARNING]

#### 2.1 N+1 Query Patterns [BLOCKING]

The most common and severe database performance issue.

```bash
# Check for queries inside loops
git diff HEAD -- '*.ts' '*.tsx' | grep -nE "for\s*\(|while\s*\(|\.forEach\(|\.map\(" -A 10 | grep -E "await.*query|await.*find|await.*fetch"

# Check for async operations in array methods
git diff HEAD -- '*.ts' '*.tsx' | grep -nE "\.map\(async|\.forEach\(async" -A 5 | grep -E "query|find|fetch|prisma|db\."

# Check for Promise.all with individual queries (potential N+1)
git diff HEAD -- '*.ts' '*.tsx' | grep -nE "Promise\.all\(" -A 10 | grep -E "\.map.*query|\.map.*find"
```

**Flag if found**:
- **BLOCKING**: Queries inside `for`, `while`, `forEach`, or `map` loops
- **BLOCKING**: Async array methods with database calls

**Fix guidance**:
```
Found: items.forEach(async (item) => {
         await db.query('SELECT * FROM details WHERE item_id = ?', [item.id])
       })

Fix: Batch query with IN/ANY:
     const ids = items.map(i => i.id);
     const details = await db.query(
       'SELECT * FROM details WHERE item_id IN (?)',
       [ids]
     );
     // Then map results back to items
```

#### 2.2 Unbounded Queries [BLOCKING]

Queries that can return unlimited rows.

```bash
# SELECT without LIMIT or ID filter
git diff HEAD -- '*.ts' '*.tsx' | grep -nE "SELECT.*FROM" | grep -v "LIMIT|WHERE.*id\s*=|RETURNING|COUNT\(|EXISTS\(|MAX\(|MIN\(|SUM\("

# ORM queries without limits
git diff HEAD -- '*.ts' '*.tsx' | grep -nE "\.findMany\(|\.find\(\{" | grep -v "take:|limit:"
```

**Flag if found**:
- **BLOCKING**: SELECT without LIMIT and without ID equality filter
- **BLOCKING**: findMany/find without take/limit on user data tables

**Safe patterns**:
- `SELECT * FROM items WHERE id = ?` - Single row by ID
- `SELECT * FROM items WHERE user_id = ? LIMIT 100` - Paginated
- `SELECT COUNT(*) FROM items` - Aggregation
- `db.items.findMany({ take: 100 })` - ORM with limit

#### 2.3 Missing Index Patterns [WARNING]

Query patterns that may not use indexes efficiently.

```bash
# Leading wildcard LIKE (full table scan)
git diff HEAD -- '*.ts' '*.tsx' | grep -nE "LIKE\s*['\"]%|LIKE\s*\\\$"

# Multiple OR conditions
git diff HEAD -- '*.ts' '*.tsx' | grep -nE "WHERE.*OR.*OR.*OR"

# Functions on indexed columns
git diff HEAD -- '*.ts' '*.tsx' | grep -nE "WHERE\s*(LOWER|UPPER|TRIM|DATE)\("
```

**Flag if found**:
- **WARNING**: `LIKE '%term%'` - Cannot use B-tree index
- **WARNING**: Excessive OR chains - Consider using IN or ANY
- **WARNING**: Functions on columns in WHERE - Prevents index use

#### 2.4 Missing Transaction Boundaries [WARNING]

Multiple related writes that should be atomic.

```bash
# Multiple INSERT/UPDATE/DELETE in same function without transaction
git diff HEAD -- '*.ts' '*.tsx' | grep -E "INSERT|UPDATE|DELETE" | grep -v "BEGIN|COMMIT|ROLLBACK|transaction|\$transaction"
```

**Flag if found**:
- **WARNING**: Multiple writes without transaction wrapper

#### 2.5 Data Fetching Issues [WARNING]

Client-side data fetching anti-patterns.

```bash
# Fetching in loops (client-side N+1)
git diff HEAD -- '*.tsx' | grep -nE "\.map\(.*useSWR|\.map\(.*useQuery|\.map\(.*fetch"

# Missing deduplication/caching config
git diff HEAD -- '*.tsx' '*.ts' | grep -n "useSWR\|useQuery" -A 8 | grep -v "dedupe\|staleTime\|cacheTime"
```

**Flag if found**:
- **BLOCKING**: Data fetching hooks inside loops/maps
- **WARNING**: Missing caching/deduplication configuration

#### 2.6 Sequential Awaits [OPTIMIZATION]

Independent async operations that could run in parallel.

```bash
# Back-to-back awaits
git diff HEAD -- '*.ts' '*.tsx' | grep -nE "const.*=\s*await" -A 1 | grep -E "const.*=\s*await"
```

**Flag if found**:
- **OPTIMIZATION**: Sequential awaits that could use Promise.all

**Fix guidance**:
```
Found:
  const user = await db.users.findOne({ id: userId });
  const project = await db.projects.findOne({ id: projectId });

Fix (if independent):
  const [user, project] = await Promise.all([
    db.users.findOne({ id: userId }),
    db.projects.findOne({ id: projectId }),
  ]);
```

---

### Phase 3: Runtime Performance Tests (Optional)

If performance tests exist, run them to detect regressions.

#### 3.1 Check for Performance Tests

```bash
# Look for performance test files
ls tests/performance/ 2>/dev/null || ls __tests__/performance/ 2>/dev/null || echo "No performance tests found"

# Check package.json for perf script
grep -E "\"perf|\"performance" package.json 2>/dev/null || echo "No performance script"
```

#### 3.2 Run Performance Tests (if available)

```bash
# Run performance test suite
npm run test:perf 2>/dev/null || npm test -- --testPathPattern=performance 2>/dev/null
```

#### 3.3 Compare Against Baselines

If baselines exist, compare current performance:

```markdown
### Response Time Tests

✅ GET /api/users - 85ms (target: <100ms)
✅ GET /api/projects - 145ms (target: <200ms)
❌ GET /api/data - 892ms (target: <400ms) - REGRESSION!
   Baseline: 250ms | Current: 892ms | +256% slower
```

**If tests fail:**
- Fix the regression before shipping
- Or update baseline with documented justification

---

### Phase 4: Present Results

Present all findings in scannable format:

```markdown
## Performance Check Results

### Static Analysis

#### Critical Issues [BLOCKING] - X found
- [ ] **N+1 Query** in app/api/items/route.ts:45
  Found: `items.map(async (item) => { await db.query(...) })`
  Fix: Use batch query with `WHERE id IN (?)`

- [ ] **Unbounded Query** in app/api/reports/route.ts:23
  Found: `SELECT * FROM audit_logs WHERE user_id = ?`
  Fix: Add `LIMIT 100 OFFSET ?` for pagination

#### Warnings - Y found
- [ ] **Leading Wildcard LIKE** in app/api/search/route.ts:56
  Found: `WHERE title LIKE '%' || ? || '%'`
  Fix: Consider full-text search for large tables

- [ ] **Missing Transaction** in app/api/orders/route.ts:78
  Found: Multiple INSERT statements without transaction
  Fix: Wrap in transaction block

#### Optimizations - Z found
- [ ] **Sequential Awaits** in app/api/projects/route.ts:67
  Found: 3 independent queries awaited sequentially
  Fix: Use Promise.all for parallel execution

---

### Runtime Tests (if available)

✅ 3 endpoints within baseline
❌ 1 endpoint with regression

---

**Summary:**
- Critical (blocking): X issues
- Warnings: Y issues
- Optimizations: Z suggestions

**Actions:**
- Fix all BLOCKING issues before commit
- Review warnings for potential improvements
- Optimizations are optional but recommended
```

---

## Quick Reference

| Check | Pattern | Severity | What to Look For |
|-------|---------|----------|------------------|
| N+1 Queries | Loop + await query | BLOCKING | `forEach/map` with async DB calls |
| Unbounded SELECT | No LIMIT/ID filter | BLOCKING | `SELECT` without `LIMIT` or `WHERE id=` |
| Leading Wildcard | LIKE '%...' | WARNING | `LIKE '%term%'` patterns |
| Missing Transaction | Multiple writes | WARNING | Multiple INSERT/UPDATE without tx |
| Data Fetch Loops | Hook in map | BLOCKING | `useSWR`/`useQuery` inside loops |
| Sequential Awaits | Back-to-back await | OPTIMIZATION | Independent awaits in sequence |

---

## Severity Levels

| Marker | Meaning | Blocking? | Action |
|--------|---------|-----------|--------|
| **BLOCKING** | Critical performance issue | Yes | Must fix before commit |
| **WARNING** | Significant concern | No | Should fix, review carefully |
| **OPTIMIZATION** | Improvement opportunity | No | Nice to have |

---

## Example Output

```
User: /performance-check

Claude: I'll analyze your changes for performance patterns.

[Phase 1: Identify changed files]
Found 4 changed files:
- 2 API routes (app/api/projects/*, app/api/items/*)
- 1 component (src/components/Dashboard.tsx)
- 1 hook (hooks/useItems.ts)

[Phase 2: Static code analysis]

## Performance Check Results

### Critical Issues [BLOCKING] - 1 found
- [ ] **N+1 Query** in app/api/items/route.ts:67
  Found: `projects.map(async p => await db.findOne(...))`
  Fix: Use single batch query

### Warnings - 1 found
- [ ] **Missing caching config** in hooks/useItems.ts:12

---
**Summary:** 1 blocking, 1 warning

You must fix the N+1 query before committing.
```

---

## Notes

- **Static analysis only** runs instantly (no runtime tests required)
- **Runtime tests** are optional and depend on project setup
- **BLOCKING issues** must be fixed before committing
- All checks are framework-agnostic where possible
- Adapt grep patterns to your ORM/framework if needed
