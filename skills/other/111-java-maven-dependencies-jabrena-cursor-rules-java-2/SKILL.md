---
name: 111-java-maven-dependencies
description: Use when you need to add or evaluate Maven dependencies that improve code quality — including nullness annotations (JSpecify), static analysis (Error Prone + NullAway), functional programming (VAVR), or architecture testing (ArchUnit) — and want a consultative, question-driven approach that adds only what you actually need. Part of the skills-for-java project
metadata:
  author: Juan Antonio Breña Moral
  version: 0.12.0-SNAPSHOT
---
# Add Maven dependencies for improved code quality

Add essential Maven dependencies that enhance code quality and safety through a consultative, question-driven approach.

**Components:** **JSpecify** (nullness annotations, `provided` scope), **Error Prone + NullAway** (enhanced static analysis with compile-time null checking), **VAVR** (functional programming with Try/Either and immutable collections), and **ArchUnit** (architecture rule enforcement, `test` scope).

**Prerequisites:** Run `mvn validate` before any changes. Ensure Maven Wrapper exists; if not, **stop** and prompt the user to install it—do not proceed until resolved.

**Before asking questions:** Read the reference to use the exact wording and options from the template. Ask questions one-by-one in strict order (JSpecify → Enhanced Compiler Analysis (conditional) → VAVR → ArchUnit) and add only what the user selects. Use consultative language, present trade-offs, and wait for user responses before implementing.

## Reference

For detailed guidance, examples, and constraints, see [references/111-java-maven-dependencies.md](references/111-java-maven-dependencies.md).
