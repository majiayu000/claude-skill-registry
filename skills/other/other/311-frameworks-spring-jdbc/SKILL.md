---
name: 311-frameworks-spring-jdbc
description: Use when you need to write or review programmatic JDBC with Spring — including JdbcTemplate, NamedParameterJdbcTemplate, JdbcClient (Spring Framework 6.1+), parameterized SQL, RowMapper mapping to records, batch operations, transactions, safe handling of generated keys, DataAccessException handling, read-only transactions, streaming large result sets, and @JdbcTest slice testing. Part of the skills-for-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.13.0-SNAPSHOT
---
# Spring JDBC — JdbcTemplate and JdbcClient

Apply Spring JDBC guidelines using JdbcTemplate, NamedParameterJdbcTemplate, and JdbcClient.

**What is covered in this Skill?**

- Parameterized SQL (never concatenate user input)
- JdbcClient fluent API for new code (Spring Framework 6.1+)
- NamedParameterJdbcTemplate for named placeholders
- RowMapper and DataClassRowMapper (records)
- Batch operations
- Safe handling of generated keys (KeyHolder / JdbcClient returning keys)
- Service-layer @Transactional boundaries
- Read-only transactions (@Transactional(readOnly = true))
- Safe single-row access (optional() / findFirst() vs queryForObject)
- Streaming large result sets (RowCallbackHandler, ResultSetExtractor)
- DataAccessException handling (DuplicateKeyException, EmptyResultDataAccessException)
- @JdbcTest slice testing with @Sql fixtures

**Scope:** Apply recommendations based on the reference rules and good/bad code examples.

## Constraints

Before applying any Spring JDBC changes, ensure the project compiles. If compilation fails, stop immediately. After applying improvements, run full verification.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any change
- **SAFETY**: If compilation fails, stop immediately
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **SQL INJECTION**: Never concatenate untrusted input into SQL strings — always use bind parameters
- **BEFORE APPLYING**: Read the reference for detailed rules and good/bad patterns

## When to use this skill

- Review Java code for Spring JDBC (JdbcTemplate, JdbcClient, NamedParameterJdbcTemplate)
- Apply best practices for Spring JDBC data access in Java code
- Detect and fix SQL injection risks in JDBC code
- Improve transaction boundaries or exception handling for JDBC operations

## Reference

For detailed guidance, examples, and constraints, see [references/311-frameworks-spring-jdbc.md](references/311-frameworks-spring-jdbc.md).
