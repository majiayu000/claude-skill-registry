---
name: 311-frameworks-spring-boot-slice-testing
description: Use when you need to write slice tests for Spring Boot applications — including @WebMvcTest, @JdbcTest, @JsonTest, @MockBean, test profiles, and @TestConfiguration for focused layer testing. Part of the skills-for-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.13.0-SNAPSHOT
---
# Spring Boot Slice Testing

Apply Spring Boot slice testing guidelines.

**What is covered in this Skill?**

- @WebMvcTest for web layer
- @JdbcTest for repository layer
- @JsonTest for JSON serialization
- @MockBean for mocking dependencies
- Test profiles
- @TestConfiguration for custom setup

**Scope:** Apply recommendations based on the reference rules and good/bad code examples.

## Constraints

Before applying any test changes, ensure the project compiles. If compilation fails, stop immediately. After applying improvements, run full verification.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any change
- **SAFETY**: If compilation fails, stop immediately
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **BEFORE APPLYING**: Read the reference for detailed rules and good/bad patterns

## Reference

For detailed guidance, examples, and constraints, see [references/311-frameworks-spring-boot-slice-testing.md](references/311-frameworks-spring-boot-slice-testing.md).
