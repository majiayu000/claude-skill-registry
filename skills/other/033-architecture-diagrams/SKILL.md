---
name: 033-architecture-diagrams
description: Use when you need to generate Java project diagrams — including UML sequence diagrams, UML class diagrams, C4 model diagrams, UML state machine diagrams, and ER (Entity Relationship) diagrams — through a modular, step-based interactive process that adapts to your specific visualization needs. This should trigger for requests such as Generate UML diagram; Create sequence diagram; Create class diagram; Create state machine diagram; Create C4 diagram. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.15.0-SNAPSHOT
---
# Java Diagrams Generator with modular step-based configuration

Generate comprehensive Java project diagrams through a modular, step-based interactive process that covers UML sequence diagrams, UML class diagrams, C4 model diagrams, UML state machine diagrams, and ER (Entity Relationship) diagrams using PlantUML syntax. **This is an interactive SKILL**.

**What is covered in this Skill?**

- UML sequence diagram generation for application workflows and API interactions
- UML class diagram generation for package structure and class relationships
- C4 model diagram generation at Context/Container/Component levels only (levels 1–3; Code/Level 4 not generated)
- UML state machine diagram generation for entity lifecycles and business workflows
- ER diagram generation from SQL schema (DDL, migrations) using PlantUML Chen notation
- PlantUML syntax for all diagram types
- File organization strategies: single-file, separate-files, or integrated with existing documentation
- Final diagram validation with PlantUML syntax checking

## Constraints

Before applying any diagram generation, ensure the project validates. If validation fails, stop immediately — do not proceed until all validation errors are resolved.

- **MANDATORY**: Run `./mvnw validate` or `mvn validate` before applying any diagram generation
- **SAFETY**: If validation fails, stop immediately — do not proceed until all validation errors are resolved
- **BEFORE APPLYING**: Read the reference for detailed good/bad examples, constraints, and safeguards for each diagram generation pattern
- **C4 LIMIT**: C4 diagrams restricted to levels 1, 2, 3 only (Context, Container, Component); never generate Level 4 (Code) diagrams

## When to use this skill

- Generate UML diagram
- Create sequence diagram
- Create class diagram
- Create state machine diagram
- Create C4 diagram
- Generate ER diagram

## Workflow

1. **Validate project state**

Run `./mvnw validate` or `mvn validate` before applying any diagram generation.

Step constraints:
- If validation fails, stop and ask to resolve errors first

2. **Read reference and configure diagram scope**

Read `references/033-architecture-diagrams.md`, identify requested diagram types, and confirm output organization strategy (single-file, separate-files, or integrated docs).

3. **Generate PlantUML diagrams**

Create requested diagrams in PlantUML syntax (sequence, class, C4 levels 1-3 only, state machine, ER) using project inputs and context.

Step constraints:
- Never generate C4 Level 4 (Code) diagrams

4. **Validate and finalize outputs**

Check generated diagrams for syntax correctness and consistency with selected scope before final delivery.

## Reference

For detailed guidance, examples, and constraints, see [references/033-architecture-diagrams.md](references/033-architecture-diagrams.md).
