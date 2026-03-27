---
name: 522-frameworks-micronaut-testing-integration-tests
description: Use when you need to write or improve integration tests for Micronaut — @MicronautTest, HttpClient, TestPropertyProvider with Testcontainers, transactional test mode where appropriate, and *IT naming with Failsafe. Part of the skills-for-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.13.0-SNAPSHOT
---
# Micronaut Integration Testing

Prove real wiring in Micronaut with containers and HTTP.

**What is covered in this Skill?**

- Scope: contracts and boundaries, not duplicated unit-test logic
- TestPropertyProvider + static @Container for JDBC/Kafka properties
- HttpClient full-stack HTTP assertions
- @MicronautTest(transactional = true) for rollback where supported
- Shared containers per class; pinned image tags
- *IT suffix and maven-failsafe-plugin alignment

**Scope:** Apply recommendations based on the reference rules and good/bad code examples.

## Constraints

Compile before changes; run verify including integration phase.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any change
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **BEFORE APPLYING**: Read the reference for detailed rules and examples

## When to use this skill

- Add Micronaut integration tests with Testcontainers
- Wire dynamic datasource or broker URLs for @MicronautTest

## Reference

For detailed guidance, examples, and constraints, see [references/522-frameworks-micronaut-testing-integration-tests.md](references/522-frameworks-micronaut-testing-integration-tests.md).
