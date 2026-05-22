---
name: 423-frameworks-quarkus-testing-acceptance-tests
description: Use when you need to implement acceptance tests from a Gherkin .feature file for Quarkus applications — including @acceptance scenarios, @QuarkusTest, BaseAcceptanceTest with QuarkusTestResourceLifecycleManager for Testcontainers and WireMock, REST Assured for full HTTP pipeline testing, WireMock JSON mapping files (classpath:wiremock/mappings/), *AT suffix naming, and Maven Surefire/Failsafe three-tier split. Requires the .feature file in context. This should trigger for requests such as Implement Quarkus acceptance tests from a Gherkin feature file; Set up BaseAcceptanceTest with Testcontainers and WireMock for Quarkus; Create WireMock JSON mapping files for external HTTP stubs in Quarkus acceptance tests; Configure Maven *AT naming convention and Failsafe plugin for Quarkus acceptance tests. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.15.0-SNAPSHOT
---
# Quarkus acceptance tests from Gherkin

Implement happy-path acceptance tests from Gherkin for Quarkus using real HTTP and infrastructure.

**What is covered in this Skill?**

- Preconditions: .feature file in context; Quarkus project confirmed
- Parsing and filtering scenarios tagged @acceptance / @acceptance-tests
- BaseAcceptanceTest with @QuarkusTest, @QuarkusTestResource, and QuarkusTestResourceLifecycleManager for:
  - Testcontainers (PostgreSQL, Kafka) with dynamic config injection on startup
  - WireMock with wireMockServer.resetAll() in @BeforeEach to isolate stubs
- Concrete acceptance test class extending BaseAcceptanceTest:
  - @DisplayName mirroring the Gherkin scenario title
  - Given (stubs + fixtures) / When (REST Assured HTTP call) / Then (response assertions + wireMock.verify)
- WireMock JSON mapping files under classpath:wiremock/mappings/ with body files under __files/
- Naming convention: *AT suffix for Failsafe; never *Test (Surefire) or *AcceptanceTest
- Maven three-tier split: *Test → Surefire, *IT + *AT → Failsafe
- Happy-path scope by default; escalate to negatives only when explicitly requested

**Scope:** Apply recommendations based on the reference rules and step workflow.

## Constraints

Do not generate without a .feature file; compile before and verify after.

- **PRECONDITION**: Gherkin `.feature` file must be in context — stop and ask if not provided
- **PRECONDITION**: The project must use Quarkus — direct the user to @133 or @323 otherwise
- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any change
- **PREREQUISITE**: Project must compile successfully before generating acceptance test scaffolding
- **BLOCKING CONDITION**: Compilation errors must be resolved by the user before proceeding
- **NO EXCEPTIONS**: Do not generate tests if the project fails to compile or the feature file is missing
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **BEFORE APPLYING**: Read the reference for detailed steps and safeguards

## When to use this skill

- Implement Quarkus acceptance tests from a Gherkin feature file
- Set up BaseAcceptanceTest with Testcontainers and WireMock for Quarkus
- Create WireMock JSON mapping files for external HTTP stubs in Quarkus acceptance tests
- Configure Maven *AT naming convention and Failsafe plugin for Quarkus acceptance tests

## Workflow

1. **Read reference and assess project context**

Read `references/423-frameworks-quarkus-testing-acceptance-tests.md` and inspect the current project setup before proposing changes.

2. **Gather scope and decide target improvements**

Identify requested outcomes, constraints, and the minimum safe set of changes to apply.

3. **Apply framework-aligned changes**

Implement or refactor configuration/code following the reference patterns and project conventions.

4. **Run verification and report results**

Execute appropriate build/tests and summarize what changed, what was verified, and any follow-up actions.

## Reference

For detailed guidance, examples, and constraints, see [references/423-frameworks-quarkus-testing-acceptance-tests.md](references/423-frameworks-quarkus-testing-acceptance-tests.md).
