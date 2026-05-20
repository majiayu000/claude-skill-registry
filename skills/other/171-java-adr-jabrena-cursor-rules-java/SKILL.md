---
name: 171-java-adr
description: Use when you need to generate Architecture Decision Records (ADRs) for a Java project through an interactive, conversational process that systematically gathers context, stakeholders, options, and outcomes to produce well-structured ADR documents. Part of the skills-for-java project
metadata:
  author: Juan Antonio Breña Moral
  version: 0.12.0-SNAPSHOT
---
# Java ADR Generator with interactive conversational approach

Generate Architecture Decision Records (ADRs) for Java projects through an interactive, conversational process that systematically gathers all necessary context to produce well-structured ADR documents.

**Core areas:** ADR file storage configuration, conversational information gathering (context, stakeholders, decision drivers, options with pros/cons, outcome, consequences), MADR template generation, and validation with `./mvnw validate` before proceeding.

**Prerequisites:** Run `./mvnw validate` or `mvn validate` before applying any ADR generation. If validation fails, **stop immediately** — do not proceed until all validation errors are resolved.

**Multi-step scope:** Step 1 assesses ADR preferences through targeted questions (storage location, template format) to determine scope. Step 2 generates the ADR through a conversational process: Phase 0 retrieves the current date, Phase 1 gathers information one question at a time (decision topic, context, stakeholders — deciders/consulted/informed, decision drivers, options with pros and cons, chosen option with rationale, implementation consequences), and Phase 2 produces the final ADR document using the MADR template with all collected information.

**Before applying changes:** Read the reference for detailed good/bad examples, constraints, and safeguards for each ADR generation pattern.

## Reference

For detailed guidance, examples, and constraints, see [references/171-java-adr.md](references/171-java-adr.md).
