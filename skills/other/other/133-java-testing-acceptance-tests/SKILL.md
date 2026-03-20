---
name: 133-java-testing-acceptance-tests
description: Use when you need to implement acceptance tests from a Gherkin .feature file for framework-agnostic Java (no Spring Boot, Quarkus, Micronaut) — finding @acceptance scenarios, happy path with RestAssured, Testcontainers for DB/Kafka, WireMock for external REST. Requires .feature file in context. Part of the skills-for-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.13.0-SNAPSHOT
---
# Java acceptance tests from Gherkin

Implement acceptance tests from Gherkin feature files. Given a .feature file in context, find @acceptance-tagged scenarios and implement happy-path tests with RestAssured, Testcontainers, and WireMock.

**What is covered in this Skill?**

- Parse Gherkin .feature files to find scenarios tagged @acceptance or @acceptance-tests
- Implement happy-path acceptance tests (one test per scenario)
- RestAssured for REST API testing (given/when/then, status codes, JSON body assertions)
- Testcontainers for databases (PostgreSQL, etc.) and Kafka
- WireMock for stubbing external REST APIs
- BaseAcceptanceTest base class with @BeforeAll coordinate propagation via System.setProperty
- Given-When-Then structure mapping Gherkin steps to setup, request, and assertions
- Maven dependencies: rest-assured, testcontainers, wiremock-standalone

**Preconditions:** (1) The Gherkin .feature file must be in context. (2) The project must NOT use Spring Boot, Quarkus, or Micronaut — for those frameworks, use @323-frameworks-spring-boot-testing-acceptance-tests or framework-specific rules.

**Scope:** Implements only happy-path scenarios. Use the reference for detailed examples and constraints.

## Constraints

Before applying any acceptance test changes, ensure the Gherkin .feature file is in context and the project compiles. If compilation fails or the feature file is missing, stop immediately.

- **PRECONDITION**: The Gherkin .feature file MUST be in context; the project MUST NOT use Spring Boot, Quarkus, or Micronaut
- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any change
- **SAFETY**: If compilation fails, stop immediately and do not proceed
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **BEFORE APPLYING**: Read the reference for detailed examples, good/bad patterns, and constraints

## When to use this skill

- Review Java code for acceptance tests
- Apply best practices for acceptance tests in Java code

## Reference

For detailed guidance, examples, and constraints, see [references/133-java-testing-acceptance-tests.md](references/133-java-testing-acceptance-tests.md).
