---
name: 111-java-maven-dependencies
description: Use when you need to add or evaluate Maven dependencies that improve code quality — including nullness annotations (JSpecify), static analysis (Error Prone + NullAway), functional programming (VAVR), or architecture testing (ArchUnit) — and want a consultative, question-driven approach that adds only what you actually need. This should trigger for requests such as Add Maven dependencies; Add JSpecify nullness dependencies; Add Error Prone NullAway dependencies; Add VAVR functional dependencies; Add ArchUnit architecture testing dependencies. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.15.0-SNAPSHOT
---
# Add Maven dependencies for improved code quality

Add essential Maven dependencies that enhance code quality and safety through a consultative, question-driven approach. **This is an interactive SKILL**.

**What is covered in this Skill?**

- JSpecify: (nullness annotations, `provided` scope)
- Error Prone + NullAway: (enhanced static analysis with compile-time null checking)
- VAVR: (functional programming with Try/Either and immutable collections)
- ArchUnit: (architecture rule enforcement, `test` scope)

## Constraints

Before adding Maven dependencies, ensure the project is in a valid state. Use a consultative, question-driven flow that adds only what the user selects.

- **MANDATORY**: Run `./mvnw validate` or `mvn validate` before any changes
- **SAFETY**: If validation fails, stop and ask the user to fix issues—do not proceed until resolved
- **BEFORE ASKING QUESTIONS**: Read the reference to use the exact wording and options from the template. Ask questions one-by-one in strict order (JSpecify → Enhanced Compiler Analysis (conditional) → VAVR → ArchUnit) and add only what the user selects. Use consultative language, present trade-offs, and wait for user responses before implementing

## When to use this skill

- Add Maven dependencies
- Add JSpecify nullness dependencies
- Add Error Prone NullAway dependencies
- Add VAVR functional dependencies
- Add ArchUnit architecture testing dependencies

## Workflow

1. **Validate project before changes**

Run `./mvnw validate` or `mvn validate` and stop if validation fails.

2. **Read dependency reference and ask guided questions**

Read `references/111-java-maven-dependencies.md` and ask one-by-one in strict order: JSpecify, conditional Enhanced Compiler Analysis, VAVR, and ArchUnit.

3. **Add only selected dependencies**

Implement only the dependencies and scopes chosen by the user, preserving existing pom.xml structure.

4. **Report trade-offs and next checks**

Summarize what was added, why, and any recommended follow-up validations or tooling alignment.

## Reference

For detailed guidance, examples, and constraints, see [references/111-java-maven-dependencies.md](references/111-java-maven-dependencies.md).
