---
name: 322-frameworks-spring-boot-testing-integration-tests
description: Use when you need to write or improve integration tests — including Testcontainers, TestRestTemplate, data management, test structure, and performance optimization for integration tests. Part of the skills-for-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.13.0-SNAPSHOT
---
# Java Integration Testing Guidelines

Apply Java integration testing guidelines.

**What is covered in this Skill?**

- Integration test scope and purpose
- Testcontainers for dependencies
- TestRestTemplate for API testing
- Data management strategies
- Test structure and assertions
- Performance and cleanup

**Scope:** Apply recommendations based on the reference rules and good/bad code examples.

## Constraints

Before applying any integration test changes, ensure the project compiles. If compilation fails, stop immediately. After applying improvements, run full verification.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any change
- **SAFETY**: If compilation fails, stop immediately
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **BEFORE APPLYING**: Read the reference for detailed rules and good/bad patterns

## When to use this skill

- Review Java code for Spring Boot integration tests
- Apply best practices for Spring Boot integration tests in Java code

## Reference

For detailed guidance, examples, and constraints, see [references/322-frameworks-spring-boot-testing-integration-tests.md](references/322-frameworks-spring-boot-testing-integration-tests.md).
