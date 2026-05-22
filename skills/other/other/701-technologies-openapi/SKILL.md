---
name: 701-technologies-openapi
description: Use when you need framework-agnostic OpenAPI 3.x guidance — spec structure, metadata and versioning, paths and operations, reusable schemas, security schemes, examples, documentation quality, contract validation (e.g. Spectral), breaking-change awareness, and handoffs to codegen — without choosing Spring Boot, Quarkus, or Micronaut. This should trigger for requests such as Review an OpenAPI; Improve an OpenAPI; Improve API contract; Improve API schema design. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.15.0-SNAPSHOT
---
# OpenAPI 3.x best practices

Help teams produce maintainable **OpenAPI 3.x** contracts that stay aligned with HTTP semantics and consumer needs.

**What is covered in this Skill?**

- Document structure: `openapi`, `info`, `servers`, `tags`, and consistent resource grouping
- Path and operation design: parameters, request bodies, response matrices, `operationId`, status codes
- Reusable `components` (schemas, parameters, responses, security schemes) and examples
- Validation and CI: spec linting, breaking-change checks, pre-codegen gates
- Security modeling in the contract (schemes, scopes, global vs operation security)
- Clear boundaries between contract-first design and runtime implementation concerns

**Scope:** Contract-first quality only. Focus this skill on OpenAPI design, quality, and governance guidance.

## Constraints

Keep recommendations at the OpenAPI layer unless the user explicitly asks for Java framework integration. After editing this repository's XML sources, regenerate skills and verify the build.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before proposing Java or Maven changes in the same change set
- **FRAMEWORK**: Keep guidance contract-centric; do not prescribe framework-specific controller wiring or runtime exposure details
- **FUZZING**: Keep fuzzing guidance high-level and contract-focused without linking to external skill identifiers
- **MANDATORY**: Regenerate skills with `./mvnw clean install -pl skills-generator` after editing skill or system-prompt XML in this repo
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` before promoting changes
- **EDGE CASE**: If the user goal is ambiguous, stop and ask a clarifying question before editing files or running project-wide commands
- **EDGE CASE**: If required context, files, credentials, or tools are missing, report the blocker explicitly and ask whether to proceed with setup or fallback guidance
- **EDGE CASE**: If requested changes conflict with project constraints or safety boundaries, explain the conflict and ask for user confirmation on the preferred trade-off

## When to use this skill

- Review an OpenAPI
- Improve an OpenAPI
- Improve API contract
- Improve API schema design
- Validate an OpenAPI spec

## Workflow

1. **Read reference and assess project context**

Read `references/701-technologies-openapi.md` and inspect current API/context artifacts before proposing changes.

2. **Gather scope and decide target improvements**

Identify requested outcomes, constraints, and the minimum safe set of changes to apply.

3. **Apply technology-aligned changes**

Implement or refactor artifacts following the reference patterns and project conventions.

4. **Run verification and report results**

Execute appropriate checks and summarize what changed, what was verified, and any follow-up actions.

## Reference

For detailed guidance, examples, and constraints, see [references/701-technologies-openapi.md](references/701-technologies-openapi.md).
