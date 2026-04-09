---
name: 701-technologies-openapi
description: Use when you need framework-agnostic OpenAPI 3.x guidance — spec structure, metadata and versioning, paths and operations, reusable schemas, security schemes, examples, documentation quality, contract validation (e.g. Spectral), breaking-change awareness, and handoffs to codegen — without choosing Spring Boot, Quarkus, or Micronaut. Part of the skills-for-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.14.0-SNAPSHOT
---
# OpenAPI 3.x best practices

Help teams produce maintainable **OpenAPI 3.x** contracts that stay aligned with HTTP semantics and consumer needs.

**What is covered in this Skill?**

- Document structure: `openapi`, `info`, `servers`, `tags`, and consistent resource grouping
- Path and operation design: parameters, request bodies, response matrices, `operationId`, status codes
- Reusable `components` (schemas, parameters, responses, security schemes) and examples
- Validation and CI: spec linting, breaking-change checks, pre-codegen gates
- Security modeling in the contract (schemes, scopes, global vs operation security)
- Clear **delegation** to framework REST skills for runtime and generator-specific work

**Scope:** Contract-first quality only. For **Spring Boot**, **Quarkus**, or **Micronaut** REST implementation details, use the matching `302`, `402`, or `502` skill. For **CATS fuzz testing** against a contract, use `134-java-testing-fuzzing-testing`.

## Constraints

Keep recommendations at the OpenAPI layer unless the user explicitly asks for Java framework integration. After editing this repository's XML sources, regenerate skills and verify the build.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before proposing Java or Maven changes in the same change set
- **FRAMEWORK**: Defer OpenAPI Generator goals, controller bindings, and runtime `/openapi` exposure to `@302-frameworks-spring-boot-rest`, `@402-frameworks-quarkus-rest`, or `@502-frameworks-micronaut-rest`
- **FUZZING**: Defer CATS execution and CI fuzz pipelines to `@134-java-testing-fuzzing-testing`
- **MANDATORY**: Regenerate skills with `./mvnw clean install -pl skills-generator` after editing skill or system-prompt XML in this repo
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` before promoting changes

## When to use this skill

- Review an OpenAPI
- Improve an OpenAPI
- Improve API contract
- Improve API schema design
- Validate an OpenAPI spec

## Reference

For detailed guidance, examples, and constraints, see [references/701-technologies-openapi.md](references/701-technologies-openapi.md).
