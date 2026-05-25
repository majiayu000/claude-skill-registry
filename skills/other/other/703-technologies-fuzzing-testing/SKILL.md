---
name: 703-technologies-fuzzing-testing
description: Use when you need to add or review fuzz testing for Java APIs with CATS — including contract-driven negative testing, malformed payload validation, boundary input exploration, CI integration, reproducible failures, and local execution guidance. This should trigger for requests such as Add fuzz testing to a Java project; Use CATS for API negative testing; Review CI quality gates for API contract robustness; Improve boundary and malformed input test coverage. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.15.0-SNAPSHOT
---
# Java fuzz testing with CATS

Design and implement contract-driven fuzz testing for Java APIs using CATS to uncover edge cases and input-validation defects early.

**What is covered in this Skill?**

- CATS setup and baseline command usage for OpenAPI-driven fuzzing
- Negative testing strategy for invalid payloads, missing fields, wrong types, and malformed values
- Boundary testing for size, range, format, and enum constraints
- CI integration patterns with actionable logs and reproducible failures
- Local execution workflow for contributors before opening pull requests
- Reporting and triage practices for fuzzing findings

**Scope:** Focus on HTTP API fuzzing and contract validation with CATS. Use this skill to define practical, repeatable checks in both local and CI workflows.

## Constraints

Before applying any fuzz testing changes, ensure the project compiles. If compilation fails, stop immediately. After implementation, regenerate skills and run verification.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any change
- **SAFETY**: If compilation fails, stop immediately and do not proceed
- **MANDATORY**: Regenerate skills with `./mvnw clean install -pl skills-generator` after editing skill XML
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **BEFORE APPLYING**: Read the reference for detailed examples, good/bad patterns, and constraints
- **EDGE CASE**: If request scope is ambiguous, stop and ask a clarifying question before applying changes
- **EDGE CASE**: If required inputs, files, or tooling are missing, report what is missing and ask whether to proceed with setup guidance

## When to use this skill

- Add fuzz testing to a Java project
- Use CATS for API negative testing
- Review CI quality gates for API contract robustness
- Improve boundary and malformed input test coverage

## Workflow

1. **Read reference and assess project context**

Read `references/703-technologies-fuzzing-testing.md` and inspect current API/context artifacts before proposing changes.

2. **Gather scope and decide target improvements**

Identify requested outcomes, constraints, and the minimum safe set of changes to apply.

3. **Apply technology-aligned changes**

Implement or refactor artifacts following the reference patterns and project conventions.

4. **Run verification and report results**

Execute appropriate checks and summarize what changed, what was verified, and any follow-up actions.

## Reference

For detailed guidance, examples, and constraints, see [references/703-technologies-fuzzing-testing.md](references/703-technologies-fuzzing-testing.md).
