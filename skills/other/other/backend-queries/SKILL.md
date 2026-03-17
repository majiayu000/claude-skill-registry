---
name: backend-queries
description: Write secure, performant, and optimized database queries using parameterized queries, eager loading, proper indexing, and transaction management. Use this skill when writing database queries in controllers, repositories, services, or model methods, when using query builders or ORM methods, when implementing filtering/sorting/pagination logic, when optimizing N+1 query problems with eager loading, when working with joins and complex queries, when implementing query caching, or when wrapping related operations in database transactions.
---

# Backend Queries

This Skill provides Claude Code with specific guidance on how to adhere to coding standards as they relate to how it should handle backend queries.

## When to use this skill

- When writing database queries in controllers, service classes, repositories, or model methods
- When using query builder methods (where, select, join, orderBy, etc.)
- When implementing eager loading to prevent N+1 query problems (with, load, etc.)
- When optimizing queries by selecting only needed columns instead of using SELECT *
- When implementing filtering, sorting, or pagination logic in queries
- When writing complex queries with joins, subqueries, or aggregations
- When wrapping multiple related database operations in transactions
- When implementing query timeouts or performance optimization
- When adding database indexes to improve query performance
- When implementing query result caching strategies
- When using raw queries or complex SQL (ensuring parameterization for security)
- When debugging slow queries or performance issues

## Instructions

For details, refer to the information provided in this file:
[backend queries](../../../agent-os/standards/backend/queries.md)
