---
name: postgres-code-review
description: Reviews PostgreSQL code for indexing strategies, JSONB operations, connection pooling, and transaction safety. Use when reviewing SQL queries, database schemas, JSONB usage, or connection management.
---

# PostgreSQL Code Review

## Quick Reference

| Issue Type | Reference |
|------------|-----------|
| Missing indexes, wrong index type, query performance | [references/indexes.md](references/indexes.md) |
| JSONB queries, operators, GIN indexes | [references/jsonb.md](references/jsonb.md) |
| Connection leaks, pool configuration, timeouts | [references/connections.md](references/connections.md) |
| Isolation levels, deadlocks, advisory locks | [references/transactions.md](references/transactions.md) |

## Review Checklist

- [ ] WHERE/JOIN columns have appropriate indexes
- [ ] Composite indexes match query patterns (column order matters)
- [ ] JSONB columns use GIN indexes when queried
- [ ] Using proper JSONB operators (`->`, `->>`, `@>`, `?`)
- [ ] Connection pool configured with appropriate limits
- [ ] Connections properly released (context managers, try/finally)
- [ ] Appropriate transaction isolation level for use case
- [ ] No long-running transactions holding locks
- [ ] Advisory locks used for application-level coordination
- [ ] Queries use parameterized statements (no SQL injection)

## Gates (before reporting findings)

Use this sequence so conclusions stay evidence-bound (not “I checked mentally”):

1. **Scope** — Record the concrete paths (and line ranges or symbols if helpful) for the SQL, DDL/migrations, and connection code under review. **Pass:** every subsystem you critique (queries, JSONB, pool, transactions) has at least one cited path.
2. **SQL/DDL citation for performance claims** — Index, sequential-scan, JSONB-operator, and plan-related findings must point to the exact statement or schema (quoted excerpt or `file:line`). **Pass:** each such finding includes that citation.
3. **Binding check before injection flags** — Only assert SQL-injection risk after locating how SQL and values are combined (bound parameters vs string concat/format/f-strings). **Pass:** you name the mechanism you saw in code for each flagged callsite.

Then load the relevant reference doc from [Quick Reference](#quick-reference) and walk the [Review Checklist](#review-checklist).

## When to Load References

- Reviewing SELECT queries with WHERE/JOIN → indexes.md
- Reviewing JSONB columns or JSON operations → jsonb.md
- Reviewing database connection code → connections.md
- Reviewing BEGIN/COMMIT or concurrent updates → transactions.md

## Review Questions

1. Will this query use an index or perform a sequential scan?
2. Are JSONB operations using appropriate operators and indexes?
3. Are database connections properly managed and released?
4. Is the transaction isolation level appropriate for this operation?
5. Could this cause deadlocks or long-running locks?
