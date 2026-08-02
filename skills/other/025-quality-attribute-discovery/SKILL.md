---
name: 025-quality-attribute-discovery
description: Use when a problem under exploration needs its quality attributes (non-functional requirements) identified and prioritized before architecture and design begin. This should trigger when an issue's Quality Attribute Discovery point of view needs evaluation, or when a maintainer directly asks to discover and prioritize candidate quality attributes for a problem, before any ADR or design work starts. Part of Plinth Toolkit
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.18.0
---
# Quality Attribute Discovery

Guide identification and prioritization of the quality attributes a future solution must satisfy, before architecture and design decisions begin. **This is an interactive SKILL**.

**What is covered in this Skill?**

- Identifying candidate quality attributes (for example performance, security, availability, maintainability, scalability, usability, observability) relevant to the problem
- Grounding each candidate in evidence from the problem frame, root causes, assumptions, and context map, not a generic checklist
- Prioritizing candidate quality attributes by stakeholder impact and risk
- Stopping at a prioritized discovery list rather than selecting or recording an architectural decision
- Explicitly not producing ADRs or an architecture direction itself

## Constraints

Discover and prioritize candidate quality attributes as input to later architecture work; do not make or record the architecture decision here. When this technique is orchestrated by another workflow, the orchestrator owns clarifying-question sequencing; when applied standalone, ask directly.

- **MUST** read `references/025-quality-attribute-discovery.md` before applying Quality Attribute Discovery guidance
- **MUST** ground each candidate quality attribute in evidence from the problem frame, root causes, assumptions, or context map
- **MUST** prioritize candidate quality attributes by stakeholder impact and risk, not list them unordered
- **MUST** stop at a prioritized discovery list without selecting or recording an architecture decision
- **MUST NOT** record an architectural decision, ADR, or design direction as part of this skill's output
- **MUST NOT** invent a quality attribute or priority when the available content is vague or ambiguous; flag the gap for a clarifying question instead

## When to use this skill

- Discover the quality attributes for this problem
- Identify non-functional requirements before design begins
- Prioritize candidate quality attributes for this issue
- Apply quality attribute discovery before architecture decisions
- Draft the Quality Attribute Discovery section of a Functional Specification

## Workflow

1. **Read the Reference**

Read `references/025-quality-attribute-discovery.md`, then review the problem frame, root-cause findings, assumptions, and context map for evidence of quality pressure.

2. **Identify Candidate Quality Attributes**

Identify candidate quality attributes grounded in that evidence, avoiding a generic unfiltered checklist.

3. **Prioritize by Impact and Risk**

Prioritize the candidate quality attributes by stakeholder impact and risk if unmet.

4. **Stop Before Architecture Decisions**

Stop at the prioritized discovery list; do not select an architecture approach or record an ADR here.

5. **Report the Discovery List**

Report the prioritized quality attributes, stating explicitly that the output stops at this discovery list and does not select or record an architecture decision; flag any item left open pending a clarifying answer.

## Reference

For detailed guidance, examples, and constraints, see [references/025-quality-attribute-discovery.md](references/025-quality-attribute-discovery.md).
