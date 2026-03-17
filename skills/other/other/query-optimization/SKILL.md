---
name: query-optimization
description: Select only the columns you need—avoid SELECT * Use when optimizing code performance. Performance category skill.
metadata:
  category: Performance
  priority: medium
  is-built-in: true
  session-guardian-id: builtin_query_optimization
---

# Query Optimization

Select only the columns you need—avoid SELECT *. Use appropriate indexes for your query patterns. Batch related queries or use JOINs instead of N+1 queries. Use EXPLAIN to understand query execution plans. Consider pagination for large result sets. Avoid complex calculations in WHERE clauses that prevent index usage. Use query parameterization for both security and performance.