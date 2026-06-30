---
name: 511-frameworks-micronaut-jdbc
description: Use when you need programmatic JDBC in Micronaut — pooled DataSource, parameterized SQL, io.micronaut.transaction.annotation.Transactional, batching, and domain exception translation. This should trigger for requests such as Review JDBC or SQL data access in a Micronaut project; Improve transactions and parameter binding for Micronaut JDBC; Translate SQLException to domain exceptions or stream large result sets; Fix self-invocation bypassing @Transactional in Micronaut. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.16.0
---
# Micronaut JDBC — programmatic SQL

Apply programmatic JDBC patterns in Micronaut with safe SQL and clear transactions.

**What is covered in this Skill?**

- Injected javax.sql.DataSource (Hikari-backed with micronaut-jdbc-hikari) and try-with-resources for Connection / PreparedStatement
- PreparedStatement with bind parameters — never string concatenation
- Mapping ResultSet rows to Java records (dedicated mapRow method)
- Safe single-row queries with Optional<T>; never assume rs.next() succeeds
- SQLException translation to domain exceptions (catch-translate-rethrow)
- Streaming large result sets with setFetchSize to avoid OOM
- Batch updates with addBatch / executeBatch for bulk inserts
- @Transactional service boundaries and TransactionDefinition.Propagation (e.g. REQUIRES_NEW for independent commits)
- Self-invocation pitfall: call transactional collaborators through injected beans, not this.method()
- SQL text blocks for multi-line SQL (upserts, dialect-specific clauses)
- When to prefer Micronaut Data (`@512`) vs raw JDBC

**Scope:** Apply recommendations based on the reference rules and good/bad code examples.

## Constraints

Compile before JDBC refactors; verify after changes.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any change
- **PREREQUISITE**: Project must compile before applying JDBC improvements
- **SAFETY**: If compilation fails, stop immediately
- **BLOCKING CONDITION**: Compilation errors must be resolved by the user before proceeding
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **BEFORE APPLYING**: Read the reference for detailed rules and examples

## When to use this skill

- Review JDBC or SQL data access in a Micronaut project
- Improve transactions and parameter binding for Micronaut JDBC
- Translate SQLException to domain exceptions or stream large result sets
- Fix self-invocation bypassing @Transactional in Micronaut

## Workflow

1. **Read reference and assess project context**

Read `references/511-frameworks-micronaut-jdbc.md` and inspect the current project setup before proposing changes.

2. **Gather scope and decide target improvements**

Identify requested outcomes, constraints, and the minimum safe set of changes to apply.

3. **Apply framework-aligned changes**

Implement or refactor configuration/code following the reference patterns and project conventions.

4. **Run verification and report results**

Execute appropriate build/tests and summarize what changed, what was verified, and any follow-up actions.

## Reference

For detailed guidance, examples, and constraints, see [references/511-frameworks-micronaut-jdbc.md](references/511-frameworks-micronaut-jdbc.md).
