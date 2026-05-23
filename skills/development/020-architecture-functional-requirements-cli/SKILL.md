---
name: 020-architecture-functional-requirements-cli
description: Facilitates conversational discovery to create Architectural Decision Records (ADRs) for CLI development. Use when the user wants to document CLI architecture, capture functional requirements for a command-line tool, create ADRs for CLI projects, or design CLI applications with documented decisions. Part of the skills-for-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.13.0-SNAPSHOT
---
# Create ADRs for CLI Development

Guide stakeholders through a structured conversation to uncover and document technical decisions and functional requirements for CLI applications. **This is an interactive SKILL**. The ADR is the documentation of that conversation, not the conversation itself.

**What is covered in this Skill?**

- Initial context: CLI purpose, users, constraints, timeline
- Functional requirements: workflows, commands, input/output, UX
- Technical decisions: language/framework, architecture, data, integration, testing, distribution
- Decision synthesis and validation before ADR creation
- ADR document generation and next steps

## Constraints

Use conversational discovery—ask 1-2 questions at a time, build on answers, validate before proceeding. Only create ADR after thorough conversation and user confirmation.

- **MANDATORY**: Run `date` before starting to get accurate timestamps for the ADR
- **MUST**: Read the reference template fresh—do not use cached questions
- **MUST**: Ask one or two questions at a time; never all at once
- **MUST**: Validate summary with user ("Does this sound accurate?") before proposing ADR creation
- **MUST**: Wait for user to confirm "proceed" before generating the ADR

## Reference

For detailed guidance, examples, and constraints, see [references/020-architecture-functional-requirements-cli.md](references/020-architecture-functional-requirements-cli.md).
