---
name: 704-technologies-sql
description: Use when you need framework-agnostic SQL guidance — schema naming, relational table design, query readability, indexes, transactions, database security, migrations, testing, and monitoring — without choosing Spring Boot, Quarkus, or Micronaut. This should trigger for requests such as Review SQL schema or migrations; Improve SQL query performance and readability; Design relational tables and indexes; Review database transaction, security, or monitoring practices. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.16.0
---
# SQL best practices

Help teams create maintainable, secure, and performant **SQL** for Java applications across relational database engines.

**What is covered in this Skill?**

- Naming conventions for tables, columns, indexes, constraints, views, triggers, and routines
- Relational table design: keys, constraints, timestamps, soft deletes, normalization, and dialect-aware data types
- Query writing: readable formatting, explicit column lists, joins, CTEs, bind parameters, and execution-plan review
- Index strategy: foreign keys, filter/sort paths, composite indexes, over-indexing risks, and index lifecycle
- Security, transactions, migrations, testing, and monitoring practices for production database work

**Scope:** Framework-agnostic SQL quality. For Java data-access APIs, defer to the matching JDBC, Spring Data JDBC, Panache, or Micronaut Data skill.

## Constraints

Keep recommendations at the SQL and database-design layer unless the user explicitly asks for Java framework integration. After editing this repository's XML sources, regenerate skills and verify the build.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before proposing Java or Maven changes in the same change set
- **SQL INJECTION**: Never concatenate untrusted input into SQL strings; use bind parameters through the application's data-access API
- **DIALECTS**: Call out database-specific syntax and portability trade-offs when using PostgreSQL, MySQL, Oracle, SQL Server, H2, or another engine
- **FRAMEWORK**: Defer Spring JDBC to `@311-frameworks-spring-jdbc`, Quarkus JDBC to `@411-frameworks-quarkus-jdbc`, Micronaut JDBC to `@511-frameworks-micronaut-jdbc`, and framework-specific migrations to the matching Flyway skill
- **MANDATORY**: Regenerate skills with `./mvnw clean install -pl skills-generator` after editing skill or system-prompt XML in this repo
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` before promoting changes
- **EDGE CASE**: If the target database dialect, migration tool, or production constraint is missing and affects the recommendation, ask a clarifying question before editing SQL
- **EDGE CASE**: If requested changes conflict with data safety, backwards compatibility, or zero-downtime deployment constraints, explain the trade-off and ask for confirmation

## When to use this skill

- Review SQL schema or migrations
- Improve SQL query performance and readability
- Design relational tables and indexes
- Review database transaction, security, or monitoring practices
- Apply SQL best practices to database DDL or DML

## Workflow

1. **Read reference and assess database context**

Read `references/704-technologies-sql.md` and inspect current schema, migrations, SQL queries, tests, and database configuration before proposing changes.

2. **Identify dialect and operational constraints**

Confirm the target database engine, migration tool, data volume expectations, availability requirements, and compatibility constraints that shape the SQL design.

3. **Apply SQL-aligned changes**

Implement or refactor SQL artifacts following the reference patterns and project conventions, keeping Java framework integration out of scope unless explicitly requested.

4. **Run verification and report results**

Execute appropriate build, migration, SQL validation, and test checks; summarize what changed, what was verified, and any remaining database risks.

## Reference

For detailed guidance, examples, and constraints, see [references/704-technologies-sql.md](references/704-technologies-sql.md).
