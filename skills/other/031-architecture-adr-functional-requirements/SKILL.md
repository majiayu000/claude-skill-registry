---
name: 031-architecture-adr-functional-requirements
description: Facilitates conversational discovery to create Architectural Decision Records (ADRs) for functional requirements covering CLI, REST/HTTP APIs, or both. Use when the user wants to document command-line or HTTP service architecture, capture functional requirements, create ADRs for CLI or API projects, or design interfaces with documented decisions. This should trigger for requests such as Create ADR for functional requirements; Document functional requirements; Capture functional requirements; Generate functional requirements in an ADR. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.16.0
---
# Create ADRs for Functional Requirements (CLI and/or REST API)

Guide stakeholders through a structured conversation to uncover and document technical decisions and functional requirements for command-line tools, REST/HTTP APIs, or combined surfaces. **This is an interactive SKILL**. The ADR is the documentation of that conversation, not the conversation itself. Infer CLI vs API from the current workspace when possible; ask a short clarifying question when unclear. Use only the current conversation and repository files explicitly available in the current session.

**What is covered in this Skill?**

- Surface discovery: CLI, REST/HTTP API, or both (inference + confirmation)
- Initial context: purpose, users/consumers, constraints, timeline, load (API when relevant)
- Functional requirements: surface-specific workflows, I/O, resources, errors
- Technical decisions: language/framework; REST blocks (API design, auth, data, infra, testing/monitoring) and/or CLI blocks (architecture, data/integration, testing/distribution)
- Decision synthesis and validation before ADR creation
- ADR document generation and next steps

## Constraints

Use conversational discovery in small batches, build on answers, validate before proceeding. Only create ADR after thorough conversation and user confirmation.

- **MANDATORY**: Use the local shell `date` command before starting to get accurate timestamps for the ADR
- **MUST**: Load the bundled reference template during the current session; ignore prior-session content unless the user provides it again
- **MUST**: Pose one or two discovery questions at a time; never all at once
- **MUST**: Validate summary with user (Does this accurately capture your requirements?) before proposing ADR creation
- **MUST**: Wait for user to confirm proceed before generating the ADR

## When to use this skill

- Create ADR for functional requirements
- Document functional requirements
- Capture functional requirements
- Generate functional requirements in an ADR

## Workflow

0. **Get current date**

Use the local shell `date` command before discovery and use it for ADR timestamps.

1. **Load reference and discover surface scope**

Load `references/031-architecture-adr-functional-requirements.md` from this skill, infer CLI/API scope from the current workspace, and ask a short clarifying question if unclear.

2. **Conduct conversational discovery**

Guide discovery in small batches to elicit functional requirements and technical decisions for CLI, REST API, or both.

Step constraints:
- Never ask all discovery questions at once
- Validate summary with user before proposing ADR generation

3. **Generate ADR after explicit confirmation**

Only after user confirms proceed, generate the ADR document and provide concise next steps.

## Reference

For detailed guidance, examples, and constraints, see [references/031-architecture-adr-functional-requirements.md](references/031-architecture-adr-functional-requirements.md).
