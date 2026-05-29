---
name: 030-architecture-adr-general
description: Use when you need to generate Architecture Decision Records (ADRs) for a Java project through an interactive, conversational process that systematically gathers context, stakeholders, options, and outcomes to produce well-structured ADR documents. This should trigger for requests such as Generate ADR; Create Architecture Decision Record; Document architecture decision; Architecture Decision Record for Java. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.15.0-SNAPSHOT
---
# Java ADR Generator with interactive conversational approach

Generate Architecture Decision Records (ADRs) for Java projects through an interactive, conversational process that systematically gathers all necessary context to produce well-structured ADR documents. **This is an interactive SKILL**.

**What is covered in this Skill?**

- ADR file storage configuration
- Conversational information gathering: context, stakeholders, decision drivers, options with pros/cons, outcome, consequences
- MADR template generation

## Constraints

Handle ambiguity and blockers explicitly to avoid implicit assumptions.

- **EDGE CASE**: If the user goal is ambiguous, stop and ask a clarifying question before editing files or running project-wide commands
- **EDGE CASE**: If required context, files, credentials, or tools are missing, report the blocker explicitly and ask whether to proceed with setup or fallback guidance
- **EDGE CASE**: If requested changes conflict with project constraints or safety boundaries, explain the conflict and ask for user confirmation on the preferred trade-off

## When to use this skill

- Generate ADR
- Create Architecture Decision Record
- Document architecture decision
- Architecture Decision Record for Java
- Write ADR
- Document technical decision
- Architecture documentation
- Record design decision
- Technology choice documentation
- Framework selection ADR
- Database choice ADR
- Architectural trade-offs
- Technical alternatives evaluation
- Why did we choose
- Deployment strategy ADR
- Infrastructure choice
- Vendor selection ADR

## Workflow

1. **Read ADR reference and gather context**

Read `references/030-architecture-adr-general.md`, then collect context, stakeholders, decision drivers, options, and trade-offs through conversation.

2. **Synthesize and confirm decision**

Summarize recommended option, rationale, and consequences, and confirm alignment with the user before creating the ADR artifact.

3. **Generate ADR output**

Create a MADR-style ADR document with the final decision, alternatives, consequences, and follow-up actions.

## Reference

For detailed guidance, examples, and constraints, see [references/030-architecture-adr-general.md](references/030-architecture-adr-general.md).
