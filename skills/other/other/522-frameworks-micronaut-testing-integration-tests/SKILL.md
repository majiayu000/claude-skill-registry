---
name: 522-frameworks-micronaut-testing-integration-tests
description: Use when you need to write or improve integration tests for Micronaut — @MicronautTest, HttpClient, TestPropertyProvider with Testcontainers, transactional test mode where appropriate, and Maven Surefire/Failsafe splits for *Test, *Tests, *IT, and *AT. This should trigger for requests such as Add Micronaut integration tests with Testcontainers; Wire dynamic datasource or broker URLs for @MicronautTest. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.15.0-SNAPSHOT
---
# Micronaut Integration Testing

Prove real wiring in Micronaut with containers and HTTP.

**What is covered in this Skill?**

- Scope: contracts and boundaries, not duplicated unit-test logic
- TestPropertyProvider + static @Container for JDBC/Kafka properties
- HttpClient full-stack HTTP assertions
- @MicronautTest(transactional = true) for rollback where supported
- Shared containers per class; pinned image tags
- Maven Surefire/Failsafe: *Test / *Tests vs *IT / *AT; explicit plugin includes and excludes

**Scope:** Apply recommendations based on the reference rules and good/bad code examples.

## Constraints

Before applying any integration test changes, ensure the project compiles. If compilation fails, stop immediately. After applying improvements, run full verification.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any change
- **PREREQUISITE**: Project must compile successfully and pass basic validation checks before any test refactoring
- **CRITICAL SAFETY**: If compilation fails, IMMEDIATELY STOP and DO NOT CONTINUE with any recommendations
- **BLOCKING CONDITION**: Compilation errors must be resolved by the user before proceeding with integration test changes
- **NO EXCEPTIONS**: Under no circumstances should testing recommendations be applied to a project that fails to compile
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **BEFORE APPLYING**: Read the reference for detailed rules and examples

## When to use this skill

- Add Micronaut integration tests with Testcontainers
- Wire dynamic datasource or broker URLs for @MicronautTest

## Workflow

1. **Read reference and assess project context**

Read `references/522-frameworks-micronaut-testing-integration-tests.md` and inspect the current project setup before proposing changes.

2. **Gather scope and decide target improvements**

Identify requested outcomes, constraints, and the minimum safe set of changes to apply.

3. **Apply framework-aligned changes**

Implement or refactor configuration/code following the reference patterns and project conventions.

4. **Run verification and report results**

Execute appropriate build/tests and summarize what changed, what was verified, and any follow-up actions.

## Reference

For detailed guidance, examples, and constraints, see [references/522-frameworks-micronaut-testing-integration-tests.md](references/522-frameworks-micronaut-testing-integration-tests.md).
