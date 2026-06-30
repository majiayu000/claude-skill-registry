---
name: 702-technologies-wiremock
description: Use when you need framework-agnostic WireMock guidance — stub design, JSON or programmatic mappings, precise request matching, response bodies and faults, classpath fixtures, isolation and reset between tests, verification of calls, dynamic ports and base URLs, and avoiding flaky stubs — without choosing Spring Boot, Quarkus, or Micronaut. This should trigger for requests such as Design or review WireMock stubs (JSON mappings or Java DSL); Improve request matching, isolation, or reset strategy for HTTP mocks; Add or fix verification of outbound HTTP calls to a WireMock server; Debug flaky tests involving WireMock or unmatched request journals. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.16.0
---
# WireMock best practices

Help teams use **WireMock** effectively for HTTP dependency stubbing with **stable, isolated** tests.

**What is covered in this Skill?**

- Stub **isolation**: per-test registration, `resetAll()`, avoiding leaked global stubs
- **Request matching**: method, path, headers, query, body patterns; when broad patterns are acceptable
- **Responses**: status, headers, JSON/XML bodies, `bodyFileName` / classpath fixtures, fault simulation (delays, errors)
- **Dynamic ports** and propagating base URLs into the system under test
- **Verification** of outbound HTTP calls and debugging unmatched requests
- Clear **delegation** to framework integration-test skills for test class layout and extensions

**Scope:** Portable WireMock behavior only. For **`BaseIntegrationTest`**, `WireMockExtension`, and stack-specific integration tests, use `@132-java-testing-integration-testing`, `@322-frameworks-spring-boot-testing-integration-tests`, `@422-frameworks-quarkus-testing-integration-tests`, or `@522-frameworks-micronaut-testing-integration-tests`. For **OpenAPI** contract quality, use `@701-technologies-openapi`.

## Constraints

Keep recommendations at the WireMock and HTTP-stub layer unless the user explicitly asks for framework integration. After editing this repository's XML sources, regenerate skills and verify the build.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before proposing Java or Maven changes in the same change set
- **FRAMEWORK**: Defer `@SpringBootTest` / `@QuarkusTest` / `@MicronautTest` and extension setup to `@132-java-testing-integration-testing` or the matching `322` / `422` / `522` integration-test skill
- **CONTRACTS**: Defer OpenAPI document structure and linting to `@701-technologies-openapi`
- **MANDATORY**: Regenerate skills with `./mvnw clean install -pl skills-generator` after editing skill or system-prompt XML in this repo
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` before promoting changes
- **EDGE CASE**: If the user goal is ambiguous, stop and ask a clarifying question before editing files or running project-wide commands
- **EDGE CASE**: If required context, files, credentials, or tools are missing, report the blocker explicitly and ask whether to proceed with setup or fallback guidance
- **EDGE CASE**: If requested changes conflict with project constraints or safety boundaries, explain the conflict and ask for user confirmation on the preferred trade-off

## When to use this skill

- Design or review WireMock stubs (JSON mappings or Java DSL)
- Improve request matching, isolation, or reset strategy for HTTP mocks
- Add or fix verification of outbound HTTP calls to a WireMock server
- Debug flaky tests involving WireMock or unmatched request journals
- Stub external HTTP APIs in tests with stable fixtures and dynamic ports

## Workflow

1. **Read reference and assess project context**

Read `references/702-technologies-wiremock.md` and inspect current API/context artifacts before proposing changes.

2. **Gather scope and decide target improvements**

Identify requested outcomes, constraints, and the minimum safe set of changes to apply.

3. **Apply technology-aligned changes**

Implement or refactor artifacts following the reference patterns and project conventions.

4. **Run verification and report results**

Execute appropriate checks and summarize what changed, what was verified, and any follow-up actions.

## Reference

For detailed guidance, examples, and constraints, see [references/702-technologies-wiremock.md](references/702-technologies-wiremock.md).
