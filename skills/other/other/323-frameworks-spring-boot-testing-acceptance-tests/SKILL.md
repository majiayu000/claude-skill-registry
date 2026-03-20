---
name: 323-frameworks-spring-boot-testing-acceptance-tests
description: Use when you need to implement acceptance tests from a Gherkin .feature file for Spring Boot apps — finding @acceptance scenarios, happy path with RestAssured, @SpringBootTest, Testcontainers for DB/Kafka, WireMock for external REST. Requires .feature file in context. Part of the skills-for-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.13.0-SNAPSHOT
---
# Spring Boot acceptance tests from Gherkin

Implement acceptance tests from Gherkin feature files in Spring Boot projects. Given a .feature file in context, find @acceptance-tagged scenarios and implement happy-path tests with @SpringBootTest, RestAssured, Testcontainers, and WireMock.

**What is covered in this Skill?**

- Parse Gherkin .feature files to find scenarios tagged @acceptance or @acceptance-tests
- Implement happy-path acceptance tests (one test per scenario)
- @SpringBootTest(webEnvironment = RANDOM_PORT), @LocalServerPort
- @DynamicPropertySource for Testcontainers and WireMock coordinates
- RestAssured for REST API testing (given/when/then, status codes, JSON body assertions)
- Testcontainers for databases (PostgreSQL, etc.) and Kafka
- WireMock for stubbing external REST APIs
- BaseAcceptanceTest base class with Spring Boot test utilities
- Given-When-Then structure mapping Gherkin steps to setup, request, and assertions

**Preconditions:** (1) The Gherkin .feature file must be in context. (2) The project must use Spring Boot. For framework-agnostic Java, use @133-java-testing-acceptance-tests.

**Scope:** Implements only happy-path scenarios. Use the reference for detailed examples and constraints.

## Constraints

Before applying any acceptance test changes, ensure the Gherkin .feature file is in context and the project compiles. If compilation fails or the feature file is missing, stop immediately.

- **PRECONDITION**: The Gherkin .feature file MUST be in context; the project MUST use Spring Boot
- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any change
- **SAFETY**: If compilation fails, stop immediately and do not proceed
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **BEFORE APPLYING**: Read the reference for detailed examples, good/bad patterns, and constraints

## When to use this skill

- Review Java code for Spring Boot acceptance tests
- Apply best practices for Spring Boot acceptance tests in Java code

## Reference

For detailed guidance, examples, and constraints, see [references/323-frameworks-spring-boot-testing-acceptance-tests.md](references/323-frameworks-spring-boot-testing-acceptance-tests.md).
