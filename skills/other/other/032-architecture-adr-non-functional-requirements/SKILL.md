---
name: 032-architecture-adr-non-functional-requirements
description: Facilitates conversational discovery to create Architectural Decision Records (ADRs) for non-functional requirements using the ISO/IEC 25010:2023 quality model. Use when the user wants to document quality attributes, NFR decisions, security/performance/scalability architecture, or design systems with measurable quality criteria. Part of the skills-for-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.13.0-SNAPSHOT
---
# Create ADRs for Non-Functional Requirements

Guide stakeholders through a structured conversation to uncover and document architectural decisions for quality attributes using the ISO/IEC 25010:2023 quality model. **This is an interactive SKILL**. The ADR documents the outcome of the conversation, not the conversation itself. Act as an architecture consultant: challenge-first, consultative, adaptive.

**What is covered in this Skill?**

- Challenge-first opening: ISO 25010:2023 quality characteristics (Functional Suitability, Performance Efficiency, Compatibility, Reliability, Security, Maintainability, Flexibility, Safety)
- Understanding the challenge: drivers, constraints, system context
- Quality-specific deep dive tailored to primary NFR category
- Solution exploration and trade-off preferences
- Decision synthesis and validation before ADR creation
- ADR document generation with Quality Metrics &amp; Success Criteria

## Constraints

Use challenge-first, consultative discovery—ask 1-2 questions at a time, build on answers, tailor to NFR category. Only create ADR after thorough conversation and user confirmation.

- **MANDATORY**: Run `date` before starting to get accurate timestamps for the ADR
- **MUST**: Read the reference template fresh—do not use cached questions
- **MUST**: Start with challenge-first opening (ISO 25010:2023 quality characteristics)
- **MUST**: Ask one or two questions at a time; never all at once
- **MUST**: Validate summary with user ("Does this accurately capture your quality needs?") before proposing ADR creation
- **MUST**: Wait for user to confirm "proceed" before generating the ADR

## When to use this skill

- Document quality attributes
- Create ADR for NFR
- Non-functional requirements ADR
- Security performance scalability architecture

## Reference

For detailed guidance, examples, and constraints, see [references/032-architecture-adr-non-functional-requirements.md](references/032-architecture-adr-non-functional-requirements.md).
