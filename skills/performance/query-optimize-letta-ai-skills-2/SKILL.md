---
name: query-optimize
description: This skill provides guidance for SQL query optimization tasks, including rewriting slow queries for better performance while preserving semantic equivalence. Use this skill when asked to optimize, improve performance of, or rewrite SQL queries, particularly when dealing with correlated subqueries, complex joins, or queries that need CTEs/window functions.
---

# Query Optimize

## Overview

This skill guides the optimization of SQL queries to improve performance while maintaining semantic equivalence with the original query. It covers common optimization patterns, verification strategies, and pitfalls to avoid.

## Workflow

### Step 1: Fully Read and Understand Input Files

Before starting any optimization work:

1. **Read the complete original query** - If tool responses truncate the query, request the full content explicitly. Never proceed with partial understanding.
2. **Read the complete database schema** - Understand all relevant tables, columns, and relationships. Request continuation if truncated.
3. **Document existing indexes** - Note which indexes exist (if any) as this affects optimization strategy.
4. **Understand the query requirements** - Identify LIMIT clauses, ORDER BY specifications, and HAVING conditions.

**Common Pitfall**: Starting optimization without seeing the full original query leads to semantic differences in the output.

### Step 2: Analyze Performance Bottlenecks

Identify common performance issues:

1. **Correlated subqueries** - Subqueries that reference outer query columns execute once per row
2. **Repeated computations** - Same subquery appearing multiple times
3. **Missing indexes** - Full table scans where indexes could help
4. **Inefficient joins** - Cartesian products or unnecessary joins
5. **Redundant DISTINCT operations** - DISTINCT on already-unique results

Document which specific parts of the query are problematic before rewriting.

### Step 3: Choose Optimization Strategy

Common optimization patterns:

1. **CTE (Common Table Expressions)** - Extract repeated subqueries into WITH clauses
2. **Window functions** - Replace correlated subqueries with ROW_NUMBER(), RANK(), etc.
3. **Materialized subqueries** - Pre-compute expensive operations once
4. **Join optimization** - Reorder joins, use appropriate join types
5. **Index suggestions** - Recommend indexes if schema modifications are permitted

**Document semantic equivalence**: Explicitly map each part of the original query to the optimized version. For example:
- Original: `COUNT(*) DESC, s.synsetid ASC` in subquery
- Optimized: `ROW_NUMBER() OVER (PARTITION BY wordid ORDER BY sense_count DESC, synsetid ASC)`

### Step 4: Implement the Optimized Query

When writing the optimized query:

1. **Preserve all semantic requirements**:
   - Same columns in output
   - Same filtering conditions (WHERE, HAVING)
   - Same ordering (ORDER BY)
   - Same row limits (LIMIT)

2. **Use readable formatting**:
   - Indent CTEs and subqueries consistently
   - Add comments for complex transformations
   - Use meaningful CTE names

3. **Verify the write operation** - After writing the solution file, always read it back to confirm the complete content was written correctly.

**Common Pitfall**: File writes may appear truncated in tool responses. Always verify by reading the file back.

### Step 5: Verification Strategy

Verification must be comprehensive and systematic:

#### Use Database-Native Timing

Prefer database-native timing over shell commands:
- **SQLite**: Use `.timer on` before running queries
- **PostgreSQL**: Use `EXPLAIN ANALYZE`
- **MySQL**: Use `SET profiling = 1`

Shell `time` commands often fail or give unreliable results for query timing.

#### Output Comparison Methods

1. **Full output comparison** (preferred for small results):
   ```sql
   -- Save original output
   .output original_output.txt
   SELECT * FROM (<original_query>);

   -- Save optimized output
   .output optimized_output.txt
   SELECT * FROM (<optimized_query>);

   -- Compare with diff
   ```

2. **Checksum comparison** (for large results):
   ```sql
   SELECT COUNT(*), SUM(hash_column) FROM (<query>);
   ```

3. **Spot-check verification** (supplement, not replacement):
   - Verify rows at beginning, middle, and end
   - Check edge cases (boundary values in HAVING conditions)
   - Test with different LIMIT/OFFSET combinations

**Common Pitfall**: Only checking a few rows is insufficient. Use checksums or full comparison for complete verification.

#### Edge Cases to Verify

- Rows at exact threshold of filtering conditions (e.g., exactly 2 synsets when HAVING requires >= 2)
- Tie-breaking behavior in ORDER BY
- NULL handling in joins and aggregations
- Empty result sets for boundary conditions

### Step 6: Final Validation

Before concluding:

1. **Read and display the final solution file** in full
2. **Confirm performance improvement** with timing measurements
3. **Confirm output equivalence** with comprehensive comparison
4. **Document any assumptions** made during optimization

## Common Optimization Patterns

### Correlated Subquery to Window Function

**Before** (slow - executes subquery per row):
```sql
SELECT w.word,
       (SELECT syn.synsetid
        FROM senses s JOIN synsets syn ON s.synsetid = syn.synsetid
        WHERE s.wordid = w.wordid
        ORDER BY COUNT(*) DESC LIMIT 1) AS top_synset
FROM words w
```

**After** (fast - single pass with window function):
```sql
WITH ranked AS (
  SELECT w.wordid, syn.synsetid,
         ROW_NUMBER() OVER (PARTITION BY w.wordid
                            ORDER BY COUNT(*) DESC, syn.synsetid ASC) AS rn
  FROM words w
  JOIN senses s ON w.wordid = s.wordid
  JOIN synsets syn ON s.synsetid = syn.synsetid
  GROUP BY w.wordid, syn.synsetid
)
SELECT w.word, r.synsetid AS top_synset
FROM words w
JOIN ranked r ON w.wordid = r.wordid AND r.rn = 1
```

### Repeated Subquery to CTE

**Before** (computes same thing twice):
```sql
SELECT (SELECT COUNT(*) FROM orders WHERE user_id = u.id) AS order_count,
       (SELECT COUNT(*) FROM orders WHERE user_id = u.id) * price AS total
FROM users u
```

**After** (computes once):
```sql
WITH user_orders AS (
  SELECT user_id, COUNT(*) AS order_count
  FROM orders
  GROUP BY user_id
)
SELECT uo.order_count, uo.order_count * u.price AS total
FROM users u
JOIN user_orders uo ON u.id = uo.user_id
```

## Efficiency Guidelines

1. **Avoid repetitive SQL file creation** - Create a parameterized test harness early
2. **Define verification approach upfront** - Plan how equivalence will be proven before starting
3. **Use a single comprehensive test script** rather than multiple ad-hoc queries
4. **If a verification attempt times out**, try a smaller sample or use checksum-based comparison

## Checklist Before Completion

- [ ] Original query fully read and understood
- [ ] Schema fully understood with all relevant tables
- [ ] Optimized query preserves semantic equivalence
- [ ] Solution file read back and verified complete
- [ ] Performance improvement confirmed with timing
- [ ] Output equivalence verified comprehensively (not just spot checks)
- [ ] Edge cases tested
