---
name: optimizing-query-text
description: |
  Optimizes Snowflake SQL query performance from provided query text. Use when optimizing Snowflake SQL for:
  (1) User provides or pastes a SQL query and asks to optimize, tune, or improve it
  (2) Task mentions "slow query", "make faster", "improve performance", "optimize SQL", or "query tuning"
  (3) Reviewing SQL for performance anti-patterns (function on filter column, implicit joins, etc.)
  (4) User asks why a query is slow or how to speed it up
---

# Optimize Query from SQL Text

## OUTPUT FORMAT

Return ONLY the optimized SQL query. No markdown formatting, no explanations, no bullet points - just pure SQL that can be executed directly in Snowflake.

## CRITICAL: Semantic Preservation Rules

**The optimized query MUST return IDENTICAL results to the original.**

Before returning ANY optimization, verify:
- **Same columns**: Exact same columns in exact same order with exact same aliases
- **Same rows**: Filter conditions must be semantically equivalent
- **Same ordering**: Preserve `ORDER BY` exactly as written
- **Same limits**: If original has `LIMIT N`, keep `LIMIT N`. If no LIMIT, do NOT add one.

**If you cannot guarantee identical results, return the original query unchanged.**

---

## Pattern 1: Function on Filter Column

**Problem**: Functions on columns in WHERE clause prevent partition pruning and index usage.

### CAN Fix

| Original | Optimized | Why Safe |
|----------|-----------|----------|
| `WHERE DATE(ts) = '2024-01-01'` | `WHERE ts >= '2024-01-01' AND ts < '2024-01-02'` | Equivalent range |
| `WHERE YEAR(dt) = 2024` | `WHERE dt >= '2024-01-01' AND dt < '2025-01-01'` | Equivalent range |
| `WHERE MONTH(dt) = 3 AND YEAR(dt) = 2024` | `WHERE dt >= '2024-03-01' AND dt < '2024-04-01'` | Equivalent range |
| `WHERE DATE(ts) >= '2024-01-01' AND DATE(ts) < '2024-02-01'` | `WHERE ts >= '2024-01-01' AND ts < '2024-02-01'` | Same boundaries |
| `WHERE YEAR(dt) BETWEEN 1995 AND 1996` | `WHERE dt >= '1995-01-01' AND dt < '1997-01-01'` | Equivalent range |

### CANNOT Fix

| Pattern | Why Not |
|---------|---------|
| `WHERE YEAR(dt) IN (SELECT year FROM ...)` | Dynamic values, cannot precompute range |
| `WHERE DATE(ts) = DATE(other_col)` | Comparing two columns, both need function |
| `WHERE EXTRACT(DOW FROM dt) = 1` | Day-of-week has no contiguous range |
| `WHERE DATE_TRUNC('month', dt) = '2024-01-01'` in GROUP BY | Needed for grouping logic |
| `SELECT YEAR(dt) AS yr ... GROUP BY YEAR(dt)` | Function in SELECT/GROUP BY is fine, only filter matters |

---

## Pattern 2: Function on JOIN Column

**Problem**: Functions on JOIN columns prevent hash joins, forcing slower nested loop joins.

### CAN Fix

| Original | Optimized | Why Safe |
|----------|-----------|----------|
| `ON CAST(a.id AS VARCHAR) = CAST(b.id AS VARCHAR)` | `ON a.id = b.id` | If both are same type (e.g., INTEGER) |
| `ON UPPER(a.code) = UPPER(b.code)` | `ON a.code = b.code` | If data is already consistently cased |
| `ON TRIM(a.name) = TRIM(b.name)` | `ON a.name = b.name` | If data has no leading/trailing spaces |

### CANNOT Fix

| Pattern | Why Not |
|---------|---------|
| `ON CAST(a.id AS VARCHAR) = b.string_id` | Types genuinely differ, CAST required |
| `ON DATE(a.timestamp) = b.date_col` | Different granularity, DATE() required |
| `ON UPPER(a.code) = b.code` | If b.code might have different case |
| `ON a.id = b.id + 1` | Arithmetic transformation, cannot remove |

---

## Pattern 3: NOT IN Subquery

**Problem**: `NOT IN` has poor performance and unexpected NULL behavior.

### CAN Fix

| Original | Optimized | Why Safe |
|----------|-----------|----------|
| `WHERE id NOT IN (SELECT id FROM t WHERE ...)` | `WHERE NOT EXISTS (SELECT 1 FROM t WHERE t.id = main.id AND ...)` | Equivalent when subquery column is NOT NULL |
| `WHERE id NOT IN (SELECT id FROM t)` where id has NOT NULL constraint | `WHERE NOT EXISTS (SELECT 1 FROM t WHERE t.id = main.id)` | NOT NULL guarantees equivalence |

### CANNOT Fix

| Pattern | Why Not |
|---------|---------|
| `WHERE id NOT IN (SELECT nullable_col FROM t)` | If subquery returns NULL, NOT IN returns no rows; NOT EXISTS doesn't |
| `WHERE (a, b) NOT IN (SELECT x, y FROM t)` | Multi-column NOT IN has complex NULL semantics |

**Key Rule**: Only convert NOT IN to NOT EXISTS if you can verify the subquery column cannot be NULL.

---

## Pattern 4: Repeated Subquery

**Problem**: Same subquery executed multiple times causes redundant scans.

### CAN Fix

| Original | Optimized |
|----------|-----------|
| Subquery appears 2+ times identically | Extract to CTE, reference CTE multiple times |
| Same aggregation used in multiple places | Compute once in CTE |

### CANNOT Fix

| Pattern | Why Not |
|---------|---------|
| Correlated subquery (references outer table) | Each execution is different, cannot cache |
| Subqueries with different filters | Not actually the same subquery |
| Subquery in SELECT that depends on current row | Correlation prevents extraction |

---

## Pattern 5: Implicit Comma Joins

**Problem**: Comma-separated tables in FROM clause are harder to read and optimize.

### CAN Fix - Always

Convert `FROM a, b, c WHERE a.id = b.id AND b.id = c.id` to explicit JOIN syntax.

This is always safe - just restructuring, no semantic change.

---

## UNSAFE Optimizations (NEVER apply)

- **UNION to UNION ALL**: UNION deduplicates rows, UNION ALL does not - different results
- **Changing window functions**: Do not modify `SUM(SUM(x)) OVER(...)` or similar nested aggregates
- **Adding redundant filters**: Do not add filters in JOIN ON if same filter exists in WHERE
- **Changing column names**: Copy column names EXACTLY from original - do not "simplify" or rename
- **Changing column aliases**: Keep all aliases exactly as original
- **Adding early filtering in JOINs**: If a filter is in WHERE, do not duplicate it in JOIN ON clause

---

## Principles

1. **Minimal changes**: Make the fewest changes necessary. Simpler optimizations are more reliable.
2. **Preserve structure**: Keep subqueries, CTEs, and overall query structure unless there's a clear benefit.
3. **When in doubt, don't**: If unsure whether a change preserves semantics, skip it.
4. **Copy exactly**: Column names, table aliases, and expressions should be copied character-for-character.

---

## Priority Order

1. **Date/time functions on filter columns** - Highest impact
2. **Implicit joins to explicit JOIN** - Always safe, improves readability
3. **NOT IN to NOT EXISTS** - Only if NULL-safe

---

## Requirements

- **Results must be identical**: Same rows, same columns, same order
- **Valid Snowflake SQL**: Output must execute without errors in Snowflake
