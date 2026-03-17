---
name: Backend Queries
description: Write secure, performant database queries using parameterized statements, proper indexing, eager loading, and transaction management to prevent SQL injection and N+1 query problems. Use this skill when writing database queries, constructing SQL statements, using ORM query builders, optimizing database performance, or working with repositories, services, or DAO files that interact with databases. Applies to SELECT, INSERT, UPDATE, DELETE operations, joins, aggregations, and any code that retrieves or manipulates data from databases.
---

# Backend Queries

## When to use this skill

- When writing database queries in repository files like `repositories/`, `dao/`, `services/`, or `queries/`
- When constructing SQL statements or using query builders in any backend service or controller
- When using ORM methods to fetch data (SQLAlchemy, TypeORM, Prisma, Django ORM, Sequelize, etc.)
- When implementing SELECT queries with WHERE clauses, JOINs, ORDER BY, or GROUP BY statements
- When writing INSERT, UPDATE, or DELETE operations that modify database records
- When preventing SQL injection by using parameterized queries or prepared statements
- When optimizing queries to avoid N+1 problems through eager loading or `select_related`/`prefetch_related`
- When selecting specific columns instead of using SELECT * for performance optimization
- When wrapping multiple related database operations in transactions for data consistency
- When adding database indexes to columns used in WHERE, JOIN, or ORDER BY clauses
- When implementing query timeouts to prevent runaway queries from impacting performance
- When caching results of expensive or frequently-run queries using Redis or similar

# Backend Queries

This Skill provides Claude Code with specific guidance on how to adhere to coding standards as they relate to how it should handle backend queries.

## Instructions

For details, refer to the information provided in this file:
[backend queries](../../../agent-os/standards/backend/queries.md)
