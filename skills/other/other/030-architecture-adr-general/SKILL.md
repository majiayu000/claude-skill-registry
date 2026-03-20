---
name: 030-architecture-adr-general
description: Use when you need to generate Architecture Decision Records (ADRs) for a Java project through an interactive, conversational process that systematically gathers context, stakeholders, options, and outcomes to produce well-structured ADR documents. Part of the skills-for-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.13.0-SNAPSHOT
---
# Java ADR Generator with interactive conversational approach

Generate Architecture Decision Records (ADRs) for Java projects through an interactive, conversational process that systematically gathers all necessary context to produce well-structured ADR documents. **This is an interactive SKILL**.

**What is covered in this Skill?**

- ADR file storage configuration
- Conversational information gathering: context, stakeholders, decision drivers, options with pros/cons, outcome, consequences
- MADR template generation
- Validation with `./mvnw validate` or `mvn validate` before proceeding

## Constraints

Before applying any ADR generation, ensure the project validates. If validation fails, stop immediately — do not proceed until all validation errors are resolved.

- **MANDATORY**: Run `./mvnw validate` or `mvn validate` before applying any ADR generation
- **SAFETY**: If validation fails, stop immediately — do not proceed until all validation errors are resolved
- **BEFORE APPLYING**: Read the reference for detailed good/bad examples, constraints, and safeguards for each ADR generation pattern

## When to use this skill

- Generate ADR
- Create Architecture Decision Record
- Document architecture decision
- Architecture Decision Record for Java

## Reference

For detailed guidance, examples, and constraints, see [references/030-architecture-adr-general.md](references/030-architecture-adr-general.md).
