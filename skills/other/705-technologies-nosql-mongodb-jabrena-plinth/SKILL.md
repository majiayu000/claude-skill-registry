---
name: 705-technologies-nosql-mongodb
description: Use when you need framework-agnostic MongoDB and non-relational database query guidance — document schema design, collection modeling, JSON Schema validation, indexes, aggregation pipelines, query performance, consistency trade-offs, transactions, and operational safety — without choosing Spring Boot, Quarkus, or Micronaut. This should trigger for requests such as Design MongoDB document schemas; Review MongoDB queries and indexes; Improve aggregation pipeline performance; Model non-relational data access patterns; Review NoSQL consistency and transaction trade-offs. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.16.0
---
# Non-relational database query best practices

Help teams design maintainable, secure, and performant **MongoDB and non-relational database queries** for Java applications.

**What is covered in this Skill?**

- Document modeling for aggregates, embedded documents, references, arrays, and bounded growth
- MongoDB JSON Schema validation and compatibility-aware schema evolution
- Query design: explicit predicates, projections, sort stability, pagination, collation, and read concerns
- Index strategy: compound indexes, covering queries, partial indexes, TTL indexes, unique constraints, and lifecycle review
- Aggregation pipelines: stage ordering, `$match` pushdown, `$project`, `$lookup`, `$unwind`, `$group`, and memory controls
- Consistency, transactions, idempotency, migration safety, testing, observability, and production diagnostics

**Scope:** Framework-agnostic MongoDB and non-relational data modeling. For Java framework integrations, defer to the matching Spring Boot, Quarkus, or Micronaut MongoDB skill.

## Constraints

Keep recommendations at the database-modeling and query layer unless the user explicitly asks for Java framework integration. After editing this repository's XML sources, regenerate skills and verify the build.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before proposing Java or Maven changes in the same change set
- **INJECTION**: Never concatenate untrusted input into query documents, aggregation stages, JSON strings, JavaScript expressions, or `$where`; use driver/framework query builders and validated parameters
- **SCHEMA**: Prefer explicit document contracts, bounded arrays, stable identifiers, and validation rules over unconstrained document growth
- **PERFORMANCE**: Review `explain()` plans, scanned/returned ratios, sort coverage, and index selectivity before claiming a query is optimized
- **FRAMEWORK**: Defer Spring MongoDB to `@315-frameworks-spring-mongodb`, Quarkus MongoDB to `@415-frameworks-quarkus-mongodb`, Micronaut MongoDB to `@515-frameworks-micronaut-mongodb`, and Mongock migrations to the matching framework migration skill
- **MANDATORY**: Regenerate skills with `./mvnw clean install -pl skills-generator` after editing skill or system-prompt XML in this repo
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` before promoting changes
- **EDGE CASE**: If the target database, version, shard topology, read/write concern, data volume, or latency requirement is missing and affects the recommendation, ask a clarifying question before editing queries or schemas
- **EDGE CASE**: If requested changes conflict with data safety, backwards compatibility, zero-downtime deployment, or retention requirements, explain the trade-off and ask for confirmation

## When to use this skill

- Design MongoDB document schemas
- Review MongoDB queries and indexes
- Improve aggregation pipeline performance
- Model non-relational data access patterns
- Review NoSQL consistency and transaction trade-offs

## Workflow

1. **Read reference and assess data context**

Read `references/705-technologies-nosql-mongodb.md` and inspect current collections, schemas, indexes, queries, aggregation pipelines, tests, and database configuration before proposing changes.

2. **Identify workload and operational constraints**

Confirm query patterns, cardinality, data volume, document growth, consistency requirements, shard topology, and migration constraints that shape the non-relational design.

3. **Apply database-aligned changes**

Implement or refactor database artifacts following the reference patterns and project conventions, keeping Java framework integration out of scope unless explicitly requested.

4. **Run verification and report results**

Execute appropriate build, schema validation, query-plan, migration, and test checks; summarize what changed, what was verified, and any remaining database risks.

## Reference

For detailed guidance, examples, and constraints, see [references/705-technologies-nosql-mongodb.md](references/705-technologies-nosql-mongodb.md).
