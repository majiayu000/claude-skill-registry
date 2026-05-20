---
name: n1-query-prevention
description: When loading a list of items with related data, use eager loading (JOINs, includes) instead of la... Use when optimizing code performance. Performance category skill.
metadata:
  category: Performance
  priority: high
  is-built-in: true
  session-guardian-id: builtin_prevent_n_plus_one
---

# N+1 Query Prevention

When loading a list of items with related data, use eager loading (JOINs, includes) instead of lazy loading each relation. In ORMs, use features like Prisma's include, TypeORM's relations, or SQLAlchemy's joinedload. Batch related lookups using WHERE IN clauses. Monitor query logs during development to catch N+1 patterns early.