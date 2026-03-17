---
name: 121-java-object-oriented-design
description: Use when you need to review, improve, or refactor Java code for object-oriented design quality — including applying SOLID, DRY, and YAGNI principles, improving class and interface design, fixing OOP concept misuse (encapsulation, inheritance, polymorphism), identifying and resolving code smells (God Class, Feature Envy, Data Clumps), or improving object creation patterns, method design, and exception handling.
metadata:
  author: Juan Antonio Breña Moral
  version: 0.12.0-SNAPSHOT
---
# Java Object-Oriented Design Guidelines

Review and improve Java code using comprehensive object-oriented design guidelines and refactoring practices.

**Core areas:** Fundamental design principles (SOLID, DRY, YAGNI), class and interface design (composition over inheritance, immutability, accessibility minimization, accessor methods), core OOP concepts (encapsulation, inheritance, polymorphism), object creation patterns (static factory methods, Builder pattern, Singleton, dependency injection, avoiding unnecessary objects), OOD code smells (God Class, Feature Envy, Inappropriate Intimacy, Refused Bequest, Shotgun Surgery, Data Clumps), method design (parameter validation, defensive copies, careful signatures, empty collections over nulls, Optional usage), and exception handling (checked vs. runtime exceptions, standard exceptions, failure-capture messages, no silent ignoring).

**Prerequisites:** Run `./mvnw compile` or `mvn compile` before applying any change. If compilation fails, **stop immediately** and do not proceed — compilation failure is a blocking condition.

**Multi-step scope:** Step 1 validates the project compiles. Step 2 identifies applicable design principles and code smells. Step 3 applies SOLID/DRY/YAGNI improvements. Step 4 addresses class and interface design issues. Step 5 resolves OOP misuse and code smells. Step 6 improves object creation, method design, and exception handling patterns.

**Before applying changes:** Read the reference for detailed examples, good/bad patterns, and constraints.

## Reference

For detailed guidance, examples, and constraints, see [references/121-java-object-oriented-design.md](references/121-java-object-oriented-design.md).
