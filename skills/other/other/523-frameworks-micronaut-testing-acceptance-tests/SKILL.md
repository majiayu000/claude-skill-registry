---
name: 523-frameworks-micronaut-testing-acceptance-tests
description: Use when you need to implement acceptance tests from a Gherkin .feature file for Micronaut applications — @acceptance scenarios, @MicronautTest, HttpClient, BaseAcceptanceTest with TestPropertyProvider for Testcontainers and WireMock, *AT suffix, Failsafe. Requires the .feature file in context. Part of the skills-for-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.14.0
---
# Micronaut acceptance tests from Gherkin

Implement happy-path acceptance tests from Gherkin for Micronaut using real HTTP and infrastructure.

**What is covered in this Skill?**

- Preconditions: .feature file in context; Micronaut project confirmed
- Parsing scenarios tagged @acceptance / @acceptance-tests
- BaseAcceptanceTest: @MicronautTest, random port, @Client("/") HttpClient, TestPropertyProvider merging DB + WireMock URLs
- wireMock.resetAll() in @BeforeEach when sharing context
- Concrete *AT classes: Given/When/Then → setup, HttpClient exchange, AssertJ assertions
- Maven three-tier split: *Test → Surefire, *IT + *AT → Failsafe
- Happy-path scope by default

**Scope:** Apply recommendations based on the reference rules and step workflow.

## Constraints

Do not generate without a .feature file; compile before and verify after.

- **PRECONDITION**: Gherkin `.feature` file must be in context — stop and ask if not provided
- **PRECONDITION**: The project must use Micronaut — direct the user to @133, @323, or @423 otherwise
- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any change
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **BEFORE APPLYING**: Read the reference for detailed steps and safeguards

## When to use this skill

- Implement Micronaut acceptance tests from a Gherkin feature file
- Set up BaseAcceptanceTest with Testcontainers and WireMock for Micronaut

## Reference

For detailed guidance, examples, and constraints, see [references/523-frameworks-micronaut-testing-acceptance-tests.md](references/523-frameworks-micronaut-testing-acceptance-tests.md).
