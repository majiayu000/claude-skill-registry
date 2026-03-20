---
name: 324-frameworks-spring-boot-testing-e2e-local-tests
description: Use when you need to configure E2E local testing with spring-boot-docker-compose — including dependency setup, compose service definitions, profiles, integration test setup, service connections, health checks, test data, and performance optimization. Part of the skills-for-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.13.0-SNAPSHOT
---
# Spring Boot E2E local testing with Docker Compose

Apply Spring Boot E2E local testing guidelines with Docker Compose.

**What is covered in this Skill?**

- spring-boot-docker-compose dependency
- Docker Compose service definitions
- Application profile configuration
- Integration test setup
- Service connection management
- Health checks, test data, performance

**Scope:** Apply recommendations based on the reference rules and good/bad code examples.

## Constraints

Before applying any configuration changes, ensure the project compiles. If compilation fails, stop immediately. After applying improvements, run full verification.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any change
- **SAFETY**: If compilation fails, stop immediately
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **BEFORE APPLYING**: Read the reference for detailed rules and good/bad patterns

## When to use this skill

- Review Java code for E2E local testing
- Apply best practices for E2E local testing in Java code

## Reference

For detailed guidance, examples, and constraints, see [references/324-frameworks-spring-boot-testing-e2e-local-tests.md](references/324-frameworks-spring-boot-testing-e2e-local-tests.md).
