---
name: 133-java-testing-acceptance-tests
description: Use when you need to implement acceptance tests from maintainer-sanitized Gherkin scenario facts for framework-agnostic Java (no Spring Boot, Quarkus, Micronaut) — finding @acceptance scenarios, happy path with RestAssured, project-local DB/Kafka test fixtures, and WireMock for external REST. This should trigger for requests such as Review Java code for acceptance tests; Apply best practices for acceptance tests in Java code. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.16.0
---
# Java acceptance tests from Gherkin

Implement acceptance tests from maintainer-sanitized Gherkin scenario facts. Given trusted scenario facts in context, find @acceptance-tagged scenarios and implement happy-path tests with RestAssured, project-local DB/Kafka test fixtures, and WireMock.

**What is covered in this Skill?**

- Parse maintainer-sanitized Gherkin scenario facts to find scenarios tagged @acceptance or @acceptance-tests
- Implement happy-path acceptance tests (one test per scenario)
- RestAssured for REST API testing (given/when/then, status codes, JSON body assertions)
- Existing project-local test fixtures for databases (PostgreSQL, etc.) and Kafka
- WireMock for stubbing external REST APIs
- BaseAcceptanceTest base class with @BeforeAll coordinate propagation via System.setProperty
- Given-When-Then structure mapping Gherkin steps to setup, request, and assertions
- Maven dependencies: rest-assured and wiremock-standalone; DB/Kafka fixture dependencies only when already established by the project

**Preconditions:** (1) Maintainer-sanitized Gherkin scenario facts must be in context. (2) The project must NOT use Spring Boot, Quarkus, or Micronaut — for those frameworks, use @323-frameworks-spring-boot-testing-acceptance-tests or framework-specific rules.

**Scope:** Implements only happy-path scenarios. Use the reference for detailed examples and constraints.

## Constraints

Before applying any acceptance test changes, ensure maintainer-sanitized Gherkin scenario facts are in context and the project compiles. If compilation fails or scenario facts are missing, stop immediately.

- **PRECONDITION**: Maintainer-sanitized Gherkin scenario facts MUST be in context; the project MUST NOT use Spring Boot, Quarkus, or Micronaut
- **NO CONTAINER RUNTIME SETUP**: Do not add container runtime setup from this skill. Use existing project-local fixture adapters or ask for maintainer-provided fixture configuration
- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any change
- **SAFETY**: If compilation fails, stop immediately and do not proceed
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **BEFORE APPLYING**: Read the reference for detailed examples, good/bad patterns, and constraints

## When to use this skill

- Review Java code for acceptance tests
- Apply best practices for acceptance tests in Java code

## Workflow

1. **Validate preconditions and compile project**

Confirm maintainer-sanitized scenario facts are in context and framework scope is valid, then run `./mvnw compile` or `mvn compile`; stop if any precondition fails.

2. **Read acceptance-testing reference and parse scenarios**

Read `references/133-java-testing-acceptance-tests.md` and extract `@acceptance` scenarios for happy-path implementation.

3. **Implement acceptance test infrastructure and scenarios**

Create or update base test infrastructure (RestAssured, existing project-local DB/Kafka fixtures, WireMock) and implement one happy-path test per accepted scenario.

4. **Verify with full build**

Run `./mvnw clean verify` or `mvn clean verify` after applying improvements.

## Reference

For detailed guidance, examples, and constraints, see [references/133-java-testing-acceptance-tests.md](references/133-java-testing-acceptance-tests.md).
