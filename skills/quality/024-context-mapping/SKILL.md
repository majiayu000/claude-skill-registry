---
name: 024-context-mapping
description: Use when a problem under exploration needs its surrounding system context identified before design begins — Existing systems, Integrations, Ownership, and External dependencies. This should trigger when an issue's Context Mapping point of view needs evaluation, or when a maintainer directly asks to map the systems, integrations, owners, and external dependencies relevant to a problem. Part of Plinth Toolkit
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.18.0
---
# Context Mapping

Guide identification of Existing systems, Integrations, Ownership, and External dependencies relevant to a problem under exploration. **This is an interactive SKILL**.

**What is covered in this Skill?**

- Identifying existing systems that already touch the problem area
- Mapping integrations and data flows between those systems
- Naming ownership: who operates, maintains, or is accountable for each system or integration
- Identifying external dependencies (third-party services, other teams, contracts) outside the team's direct control
- Feeding context-mapping findings into `025-quality-attribute-discovery` and the remaining Functional Specification lenses

## Constraints

Map the surrounding context before any design decision assumes a system boundary. When this technique is orchestrated by another workflow, the orchestrator owns clarifying-question sequencing; when applied standalone, ask directly.

- **MUST** read `references/024-context-mapping.md` before applying Context Mapping guidance
- **MUST** identify existing systems that already touch the problem area, not only the system expected to change
- **MUST** identify integrations and data flows between the identified systems
- **MUST** name an owner (team or role) for each identified system or integration when known
- **MUST** identify external dependencies outside the team's direct control, such as third-party services, other teams, or contracts
- **MUST NOT** invent a system, integration, owner, or external dependency when the available content is vague or ambiguous; flag the gap for a clarifying question instead

## When to use this skill

- Map the systems and integrations around this problem
- Identify ownership for these systems
- List the external dependencies for this issue
- Apply context mapping before design begins
- Draft the Context Mapping section of a Functional Specification

## Workflow

1. **Read the Reference**

Read `references/024-context-mapping.md`, then review the problem frame for systems already implicated by the problem.

2. **Identify Existing Systems**

List existing systems that already touch the problem area, including systems that are affected but not expected to change.

3. **Map Integrations**

Identify integrations and data flows between the identified systems.

4. **Name Ownership**

Name an owning team or role for each identified system or integration when known.

5. **Identify External Dependencies**

Identify third-party services, other teams, or contracts outside the team's direct control that the problem or its resolution depends on.

6. **Report the Context Map**

Report Existing systems, Integrations, Ownership, and External dependencies, and flag any item left open pending a clarifying answer.

## Reference

For detailed guidance, examples, and constraints, see [references/024-context-mapping.md](references/024-context-mapping.md).
