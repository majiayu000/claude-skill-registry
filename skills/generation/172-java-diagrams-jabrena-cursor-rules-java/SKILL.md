---
name: 172-java-diagrams
description: Use when you need to generate Java project diagrams — including UML sequence diagrams, UML class diagrams, C4 model diagrams, and UML state machine diagrams — through a modular, step-based interactive process that adapts to your specific visualization needs. Part of the skills-for-java project
metadata:
  author: Juan Antonio Breña Moral
  version: 0.12.0-SNAPSHOT
---
# Java Diagrams Generator with modular step-based configuration

Generate comprehensive Java project diagrams through a modular, step-based interactive process that covers UML sequence diagrams, UML class diagrams, C4 model diagrams, and UML state machine diagrams using PlantUML syntax.

**Core areas:** UML sequence diagram generation for application workflows and API interactions, UML class diagram generation for package structure and class relationships, C4 model diagram generation at Context/Container/Component/Code abstraction levels, UML state machine diagram generation for entity lifecycles and business workflows, PlantUML syntax for all diagram types, file organization strategies (single-file, separate-files, or integrated with existing documentation), and final diagram validation with PlantUML syntax checking.

**Prerequisites:** Run `./mvnw validate` or `mvn validate` before applying any diagram generation. If validation fails, **stop immediately** — do not proceed until all validation errors are resolved.

**Multi-step scope:** Step 1 assesses diagram preferences through targeted questions to determine which subsequent steps to execute. Step 2 generates UML sequence diagrams for main application flows, API interactions, and complex business logic — conditionally executed if selected. Step 3 generates UML class diagrams for all packages, core business logic packages, or specific packages, showing inheritance, composition, and dependency relationships — conditionally executed if selected. Step 4 generates C4 model diagrams covering System Context, Container, Component, and Code levels — conditionally executed if selected. Step 5 generates UML state machine diagrams for entity lifecycles, business workflows, system behaviors, and user interactions — conditionally executed if selected. Step 6 validates all generated diagrams and produces a comprehensive summary of files created, directory structure, content coverage, and usage instructions for rendering with PlantUML.

**Before applying changes:** Read the reference for detailed good/bad examples, constraints, and safeguards for each diagram generation pattern.

## Reference

For detailed guidance, examples, and constraints, see [references/172-java-diagrams.md](references/172-java-diagrams.md).
