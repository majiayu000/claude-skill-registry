---
name: 121-java-object-oriented-design
description: Use when reviewing, improving, or refactoring Java object-oriented design, including applying SOLID, DRY, or YAGNI; improving classes and interfaces; correcting encapsulation, inheritance, or polymorphism; resolving God Class, Feature Envy, or Data Clumps; and improving object creation, methods, or exception contracts. Triggers include review Java OOD, refactor Java OOD, improve Java OOD, fix OOP misuse, and identify Java code smells. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.16.0
---
# Java Object-Oriented Design Guidelines

Review and improve Java code using focused object-oriented design references selected after assessing the request and affected code.

**What is covered in this Skill?**

- Fundamental design principles (SOLID, DRY, YAGNI)
- Class and interface design: composition over inheritance, immutability, accessibility minimization, accessor methods
- Core OOP concepts: encapsulation, inheritance, polymorphism
- Object creation patterns: static factory methods, Builder, Singleton, dependency injection, avoiding unnecessary objects
- OOD code smells: God Class, Feature Envy, Inappropriate Intimacy, Refused Bequest, Shotgun Surgery, Data Clumps
- Method design: parameter validation, defensive copies, careful signatures, empty collections over nulls, Optional usage
- Exception handling: checked vs. runtime exceptions, standard exceptions, failure-capture messages, no silent ignoring

**Scope:** Classify the applicable OOD concerns first, then load only the focused references needed for those concerns. Load multiple references when a refactoring crosses concern boundaries.

## Constraints

Before applying any OOD changes, ensure the project compiles. If compilation fails, stop immediately — do not proceed until resolved. After applying improvements, run full verification.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any change
- **SAFETY**: If compilation fails, stop immediately and do not proceed — compilation failure is a blocking condition
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **PROGRESSIVE DISCLOSURE**: Classify the applicable OOD concerns before reading references, then read only the references mapped to those concerns
- **MULTI-CONCERN CHANGES**: Read multiple focused references only when the request or diagnosed code problems cross concern boundaries
- **PRESERVE BEHAVIOR**: Apply focused, incremental refactorings without changing observable business behavior
- **INCREMENTAL SAFETY**: Compile after each significant refactoring and keep changes easy to revert if validation reveals a regression
- **DEPENDENCY SAFETY**: Confirm refactoring does not break imports, dependencies, class relationships, or established contracts
- **ADJACENT SKILLS**: Use skill 122 for dedicated type-design work and skill 126 for dedicated exception-handling work; use the overlapping skill 121 references only when those topics are part of a broader OOD review
- **EDGE CASE**: If request scope is ambiguous, stop and ask a clarifying question before applying changes
- **EDGE CASE**: If required inputs, files, or tooling are missing, report what is missing and ask whether to proceed with setup guidance

## When to use this skill

- Review Java code for object-oriented design
- Refactor Java code for object-oriented design
- Improve Java code for object-oriented design
- Fix OOP concept misuse in Java code
- Identify and resolve code smells in Java code
- Improve object creation patterns in Java code
- Improve method design in Java code
- Improve exception handling in Java code

## Workflow

1. **Compile project before OOD changes**

Run `./mvnw compile` or `mvn compile` and stop immediately if compilation fails.

2. **Assess code and classify OOD concerns**


Analyze the request and affected Java code before reading implementation guidance. Classify each relevant problem into one or more concerns:

- Fundamental principles: SOLID, DRY, or YAGNI violations.
- Core OOP concepts: encapsulation, inheritance, or polymorphism misuse.
- Code smells: God Class, Feature Envy, Inappropriate Intimacy, Refused Bequest, Shotgun Surgery, or Data Clumps.
- Object creation: factories, builders, singletons, dependency injection, or unnecessary object creation.
- Classes and interfaces: accessibility, public fields, mutability, composition, or inheritance design.
- Enums and annotations: int constants, ordinals, bit fields, ordinal indexing, or missing `@Override`.
- Methods: parameter validation, defensive copies, signatures, null collections, or `Optional`.
- Exceptions: exception contracts that are part of the broader OOD review.

If the request is dedicated type-design work, use skill 122. If it is dedicated exception-handling work, use skill 126.


3. **Read only applicable OOD references**


Map the classified concerns to focused references:

- For SOLID, DRY, or YAGNI, read `references/121-java-object-oriented-design-principles.md`.
- For encapsulation, inheritance, or polymorphism, read `references/121-java-object-oriented-design-oop-concepts.md`.
- For object-oriented code smells, read `references/121-java-object-oriented-design-code-smells.md`.
- For factories, builders, singletons, dependency injection, or unnecessary objects, read `references/121-java-object-oriented-design-object-creation.md`.
- For class and interface boundaries, accessibility, mutability, composition, or inheritance design, read `references/121-java-object-oriented-design-classes-interfaces.md`.
- For enums, ordinals, bit fields, enum lookup, or `@Override`, read `references/121-java-object-oriented-design-enums-annotations.md`.
- For method contracts, validation, defensive copies, signatures, collection returns, or `Optional`, read `references/121-java-object-oriented-design-methods.md`.
- For exception contracts within a broader OOD review, read `references/121-java-object-oriented-design-exceptions.md`.

Read every reference required by a cross-concern refactoring, but do not read unrelated references.


4. **Apply focused refactorings**


Prioritize findings by impact: CRITICAL, MAINTAINABILITY, FLEXIBILITY, or CODE_QUALITY. Apply the smallest suitable refactoring for each diagnosed concern while preserving observable behavior:

- Extract classes or methods to restore focused responsibilities.
- Introduce or refine abstractions for extension, interface segregation, and dependency inversion.
- Correct inheritance hierarchies to preserve substitutability, or replace inheritance with composition.
- Move behavior to eliminate Feature Envy and improve encapsulation.
- Introduce cohesive value or parameter objects for Data Clumps.
- Hide exposed state and reduce unnecessary coupling.

Apply changes incrementally and compile after each significant refactoring.


5. **Verify with full build**

Run `./mvnw clean verify` or `mvn clean verify` after applying improvements.

6. **Report applied OOD improvements**

Report findings by impact and concern, focused references used, refactorings applied, maintainability/flexibility/testability benefits, behavior-preservation evidence, and the final compilation and test result.

## Reference

For detailed guidance, examples, and constraints, see:

- [references/121-java-object-oriented-design-principles.md](references/121-java-object-oriented-design-principles.md)
- [references/121-java-object-oriented-design-oop-concepts.md](references/121-java-object-oriented-design-oop-concepts.md)
- [references/121-java-object-oriented-design-code-smells.md](references/121-java-object-oriented-design-code-smells.md)
- [references/121-java-object-oriented-design-object-creation.md](references/121-java-object-oriented-design-object-creation.md)
- [references/121-java-object-oriented-design-classes-interfaces.md](references/121-java-object-oriented-design-classes-interfaces.md)
- [references/121-java-object-oriented-design-enums-annotations.md](references/121-java-object-oriented-design-enums-annotations.md)
- [references/121-java-object-oriented-design-methods.md](references/121-java-object-oriented-design-methods.md)
- [references/121-java-object-oriented-design-exceptions.md](references/121-java-object-oriented-design-exceptions.md)
