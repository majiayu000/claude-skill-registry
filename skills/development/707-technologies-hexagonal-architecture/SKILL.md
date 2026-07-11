---
name: 707-technologies-hexagonal-architecture
description: Use when you need framework-agnostic Hexagonal architecture guidance for Java projects - ports and adapters boundaries, application core independence, driving and driven adapters, dependency direction, infrastructure leakage detection, optional architecture tests, and evidence-backed remediation. This should trigger for requests such as Review Hexagonal architecture; Review ports and adapters boundaries; Enforce dependency direction; Add ArchUnit architecture tests; Detect infrastructure leakage in domain code; Improve ports and adapters boundaries. Part of Plinth Toolkit
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.17.0
---
# Java Hexagonal architecture boundary review

Help teams review and improve **Hexagonal architecture** boundaries in Java applications without coupling the guidance to Spring Boot, Quarkus, or Micronaut runtime wiring.

**What is covered in this Skill?**

- Domain independence: entities, value objects, domain services, and domain policies stay free of framework, persistence, web, messaging, and infrastructure APIs
- Application/use-case orchestration: use cases coordinate domain behavior through inbound or outbound ports without taking dependencies on concrete adapters
- Adapter and infrastructure boundaries: driving adapters call inbound ports, and driven adapters implement outbound ports
- Dependency direction checks: package, module, import, Maven module, and test evidence that adapters depend on the core rather than the core depending on adapters
- Optional architecture verification: ArchUnit-style rules for Hexagonal boundaries when architecture tests fit the project
- Evidence-backed remediation: findings cite concrete classes, imports, dependencies, packages, or tests and propose small boundary-preserving changes

**Scope:** Framework-agnostic architecture boundary review for Java projects. For Spring Boot, Quarkus, or Micronaut runtime wiring, defer to the matching framework skill. For adding ArchUnit or other Maven dependencies, defer to `111-java-maven-dependencies`.

## Constraints

Keep recommendations focused on architecture boundaries and dependency direction unless the user explicitly asks for framework runtime implementation. After editing this repository's XML sources, regenerate skills and verify the build.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before proposing Java or Maven changes in the same change set
- **BOUNDARIES**: Domain packages must not depend on application, adapter, infrastructure, framework, persistence, web, messaging, or dependency-injection APIs
- **USE CASES**: Application/use-case code may orchestrate domain behavior and depend on inbound/outbound ports, but must not depend on concrete adapter implementations
- **ADAPTERS**: Driving adapters call inbound ports and driven adapters implement outbound ports; adapters must not become shared domain logic or depend on each other unnecessarily
- **ARCHUNIT OPTIONAL**: Treat ArchUnit as an optional verification approach selected when it fits the project; do not require adding it before Hexagonal architecture guidance is useful
- **DEPENDENCIES**: Route Maven dependency evaluation, including ArchUnit dependency additions, to `111-java-maven-dependencies`
- **FRAMEWORK ROUTING**: Defer Spring Boot, Quarkus, and Micronaut runtime wiring to the matching framework-specific skill without embedding direct framework skill links in this guidance
- **MANDATORY**: Regenerate skills with `./mvnw clean install -pl skills-generator` after editing skill or system-prompt XML in this repo
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` before promoting changes
- **EDGE CASE**: If package layout, module boundaries, framework ownership, or persistence strategy is ambiguous and affects the review, ask a clarifying question before editing architecture-sensitive code
- **EDGE CASE**: Distinguish confirmed boundary violations from assumptions, conventions inferred from naming, and missing context

## When to use this skill

- Review Hexagonal architecture
- Review ports and adapters boundaries
- Review architecture boundaries
- Enforce dependency direction
- Add ArchUnit architecture tests
- Detect infrastructure leakage in domain code
- Improve ports and adapters boundaries

## Workflow

1. **Read reference and map the codebase**

Read `references/707-technologies-hexagonal-architecture.md` and inspect packages, modules, imports, Maven modules, tests, and framework entry points before making claims about architecture boundaries.

2. **Identify ports, adapters, and dependency direction**

Map domain, application/use-case, inbound ports, outbound ports, driving adapters, driven adapters, and infrastructure responsibilities; record the evidence used and mark unclear areas as assumptions.

3. **Review violations and propose boundary-preserving changes**

Report concrete core-to-adapter dependency violations, framework or infrastructure leakage, adapter coupling, and misplaced behavior with small remediation steps aligned to the existing project structure.

4. **Recommend optional verification and route out-of-scope work**

Suggest ArchUnit-style tests when useful, route dependency additions to `111-java-maven-dependencies`, route framework runtime wiring to the matching framework skill, and summarize verification results.

## Reference

For detailed guidance, examples, and constraints, see [references/707-technologies-hexagonal-architecture.md](references/707-technologies-hexagonal-architecture.md).
