---
name: 111-java-maven-dependencies
description: Use when you need to add or evaluate Maven dependencies that improve code quality — including nullness annotations (JSpecify), static analysis (Error Prone + NullAway), functional programming (VAVR), or architecture testing (ArchUnit) — and want a consultative, question-driven approach that adds only what you actually need. This should trigger for requests such as Add Maven dependencies; Add JSpecify nullness dependencies; Add Error Prone NullAway dependencies; Add VAVR functional dependencies; Add ArchUnit architecture testing dependencies. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.16.0
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
- **BEFORE READING DEPENDENCY REFERENCES**: Run the question flow embedded in this SKILL.md first. Ask one consolidated dependency-selection question, then ask only conditional follow-up questions required by the selected options. Read only the dependency references selected by the user's answers. Use consultative language, present trade-offs, and wait for user responses before implementing

## When to use this skill

- Add Maven dependencies
- Add JSpecify nullness dependencies
- Add Error Prone NullAway dependencies
- Add VAVR functional dependencies
- Add ArchUnit architecture testing dependencies

## Workflow

1. **Validate project before changes**

Run `./mvnw validate` or `mvn validate` and stop if validation fails.

2. **Ask dependency assessment questions before reading references**


Run this XML-included question flow before reading any dependency implementation reference. Ask the consolidated dependency-selection question first, wait for the user's answer, and record selected dependency families before continuing. Ask conditional follow-up questions only when required by the selected dependencies.


**Question 1**: Which code-quality dependencies do you want to add?

Options:
- JSpecify (modern nullness annotations, `provided` scope; recommended for new projects)
- Error Prone + NullAway (enhanced compiler analysis and compile-time nullness checking; requires JSpecify)
- VAVR (functional programming support with Try/Either and immutable collections)
- ArchUnit (architecture testing with JUnit 5, `test` scope)
- None
- Other (specify)

**Recommendation**: Select JSpecify for better null-safety annotations. Add Error Prone + NullAway when you want stronger compile-time analysis. Add VAVR only when functional programming patterns are useful for the project. Add ArchUnit when you want automated architecture governance.

**Selection notes**:
- If Error Prone + NullAway is selected, also select JSpecify unless the project already has equivalent nullness annotations configured.
- If None is selected, do not add dependency-family references.

---

**Question 2** (conditional): What is your main project package name?

**Note**: This question is asked only if Error Prone + NullAway was selected.

This is needed to configure NullAway to analyze your code. For example, if your classes are in `com.example.myproject`, enter `com.example.myproject`.

**Format**: Use dot notation (e.g., `com.example.myproject` or `org.mycompany.myapp`)

**Example**: `com.example.myproject`


After all applicable questions are answered, confirm the selections and map them to references:

- If JSpecify is selected, read `references/111-java-maven-dependencies-jspecify.md`.
- If enhanced compiler analysis is selected, use the Error Prone + NullAway section from `references/111-java-maven-dependencies-jspecify.md`.
- If VAVR is selected, read `references/111-java-maven-dependencies-vavr.md`.
- If ArchUnit is selected, read `references/111-java-maven-dependencies-archunit.md`.
- Do not read or apply unselected dependency-family references.


3. **Read selected references and add only selected dependencies**

Read only the selected dependency-family references, then implement only the dependencies, properties, scopes, plugin configuration, and support files chosen by the user while preserving the existing `pom.xml` structure.

4. **Report trade-offs and next checks**

Summarize what was added, why, and any recommended follow-up validations or tooling alignment.

## Reference

For detailed guidance, examples, and constraints, see:

- [references/111-java-maven-dependencies-jspecify.md](references/111-java-maven-dependencies-jspecify.md)
- [references/111-java-maven-dependencies-vavr.md](references/111-java-maven-dependencies-vavr.md)
- [references/111-java-maven-dependencies-archunit.md](references/111-java-maven-dependencies-archunit.md)
