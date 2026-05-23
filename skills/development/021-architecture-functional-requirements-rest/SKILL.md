---
name: 021-architecture-functional-requirements-rest
description: Facilitates conversational discovery to create Architectural Decision Records (ADRs) for REST API development. Use when the user wants to document REST API architecture, capture functional requirements for APIs, create ADRs for REST/HTTP services, or design APIs with documented decisions. Part of the skills-for-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.13.0-SNAPSHOT
---
# Create ADRs for REST API Development

Guide stakeholders through a structured conversation to uncover and document technical decisions and functional requirements for REST API implementations. **This is an interactive SKILL**. The ADR is the documentation of that conversation, not the conversation itself.

**What is covered in this Skill?**

- Initial context: API purpose, consumers, constraints, load
- Functional requirements: use cases, resources, operations, response formats, error handling
- Technical decisions: language/framework, API design, auth/security, data, integration, infrastructure, testing, monitoring
- Decision synthesis and validation before ADR creation
- ADR document generation and next steps

## Constraints

Use conversational discovery—ask 1-2 questions at a time, build on answers, validate before proceeding. Only create ADR after thorough conversation and user confirmation.

- **MANDATORY**: Run `date` before starting to get accurate timestamps for the ADR
- **MUST**: Read the reference template fresh—do not use cached questions
- **MUST**: Ask one or two questions at a time; never all at once
- **MUST**: Validate summary with user ("Does this accurately capture your requirements?") before proposing ADR creation
- **MUST**: Wait for user to confirm "proceed" before generating the ADR

## Reference

For detailed guidance, examples, and constraints, see [references/021-architecture-functional-requirements-rest.md](references/021-architecture-functional-requirements-rest.md).
