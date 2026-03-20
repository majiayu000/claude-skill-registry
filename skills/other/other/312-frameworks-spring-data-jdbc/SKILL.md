---
name: 312-frameworks-spring-data-jdbc
description: Use when you need to use Spring Data JDBC with Java records — including entity design with records, repository pattern, immutable updates, aggregate relationships, custom queries, transaction management, and avoiding N+1 problems. Part of the skills-for-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.13.0-SNAPSHOT
---
# Spring Data JDBC with Records

Apply Spring Data JDBC guidelines with Java records.

**What is covered in this Skill?**

- Records for entity classes
- Repository pattern
- Immutable updates
- Aggregate relationships
- Custom queries
- Transaction management
- Single query loading (N+1 avoidance)

**Scope:** Apply recommendations based on the reference rules and good/bad code examples.

## Constraints

Before applying any Spring Data JDBC changes, ensure the project compiles. If compilation fails, stop immediately. After applying improvements, run full verification.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any change
- **SAFETY**: If compilation fails, stop immediately
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **BEFORE APPLYING**: Read the reference for detailed rules and good/bad patterns

## When to use this skill

- Review Java code for Spring Data JDBC
- Apply best practices for Spring Data JDBC in Java code

## Reference

For detailed guidance, examples, and constraints, see [references/312-frameworks-spring-data-jdbc.md](references/312-frameworks-spring-data-jdbc.md).
