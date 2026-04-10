---
name: 703-technologies-fuzzing-testing
description: Use when you need to add or review fuzz testing for Java APIs with CATS — including contract-driven negative testing, malformed payload validation, boundary input exploration, CI integration, reproducible failures, and local execution guidance. Part of the skills-for-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.14.0
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

## When to use this skill

- Add fuzz testing to a Java project
- Use CATS for API negative testing
- Review CI quality gates for API contract robustness
- Improve boundary and malformed input test coverage

## Reference

For detailed guidance, examples, and constraints, see [references/703-technologies-fuzzing-testing.md](references/703-technologies-fuzzing-testing.md).
