---
name: to-spec
description: 'Use when settled conversation decisions need synthesis into an agent-ready implementation spec, stopping before publication. Not for turning plans into tickets: use to-tickets.'
---

# To spec

## Contract

| Field | Bound contract |
|---|---|
| Trigger | Settled decisions need synthesis into an implementation spec. |
| Authority | Reversible local: writes only a named local spec file; rollback is deleting that file. No remote mutation. |
| Side effect | Writes an agent-ready specification file locally and stops before publishing or distributing it; a human performs any publication. |
| Done | Problem, solution, stories, decisions, tests, and exclusions are agent-ready in a verified local specification file; publication remains an unexecuted human handoff. |

## Inputs

- **Conversation context.** The current conversation must contain settled decisions: what is being built, why, and how completion will be judged. If the conversation lacks settled decisions, stop and state what is missing.
- **Codebase state.** Explore the repository to understand the current state. Use the project's domain glossary vocabulary throughout the spec and respect any ADRs in the area being touched.
- **Optional: CONTEXT.md or domain docs.** If present, read them for vocabulary and constraints. Do not require them.

## Refusals

- Will not interview the user or open a new round of questioning: synthesize what has already been decided.
- Will not fabricate decisions or fill gaps with assumptions.
- Will not publish, distribute, or assign labels: publication is a human handoff.
- Will not proceed to spec writing until the user confirms the identified seams.

## Procedure

1. Explore the repository to understand the current state of the codebase if not already done. Identify the project's domain vocabulary and any ADRs in the relevant area. **Done when:** the codebase state and domain vocabulary are understood.
2. Identify the seams at which the feature will be tested. Prefer existing seams to new ones, and use the highest existing seam possible. If a new seam is needed, propose it at the highest practical point. Fewer seams across the codebase are better; the ideal number is one. **Done when:** the testing seams are identified.
3. Present the identified seams to the user and confirm they match expectations. Do not proceed until the user confirms. **Done when:** the user confirms the seams.
4. Synthesize the spec from the conversation context, codebase understanding, and confirmed seams. Do not interview the user or open a new round of questioning. Capture what has already been decided. **Done when:** the spec content is synthesized from settled decisions.
5. Write the spec to `docs/specs/<feature-slug>-spec.md` using the template below. **Done when:** the spec file is written to disk.
6. Verify the written file contains all seven sections populated with substantive content. If any section is empty or stubbed, fill it before declaring done. **Done when:** all seven sections are substantive.
7. Stop. Do not publish, distribute, or assign labels. Report the file path and that publication is a human handoff. **Done when:** the file path is reported and no publication action is taken.

### Spec template

Write the spec using this structure:

```markdown
# <Feature name> - spec

### Problem statement

The problem from the user's perspective.

### Solution

The solution from the user's perspective.

### User stories

A numbered list of user stories. Each in the format:

1. As an <actor>, I want a <feature>, so that <benefit>

Cover all aspects of the feature exhaustively.

### Implementation decisions

A list of implementation decisions:
- Modules to build or modify
- Interfaces to modify
- Technical clarifications
- Architectural decisions
- Schema changes
- API contracts
- Specific interactions

Do NOT include specific file paths or code snippets unless a prototype produced a snippet that encodes a decision more precisely than prose (state machine, reducer, schema, type shape). Trim to the decision-rich part.

### Testing decisions

- What makes a good test (external behavior only, not implementation details)
- Which modules will be tested
- Prior art for similar tests in the codebase

### Out of scope

What is deliberately excluded from this spec.

### Further notes

Any additional notes about the feature.
```

## Failure and recovery

| Failure class | Behavior |
|---|---|
| Missing settled decisions | Stop. Report exactly which decisions are missing. Do not fabricate decisions or fill gaps with assumptions. |
| No seams identifiable | Propose seams at the highest reasonable points and present them as proposals, not facts. |
| User rejects seams | Ask what they would prefer and iterate. Do not proceed to spec writing until seams are confirmed. |
| Write failure | Report the error. No partial artifact is acceptable; delete any incomplete file. |
| Non-convergent synthesis | Name the contradiction and stop rather than choosing a side silently. |

## Output

A local specification file at `docs/specs/<feature-slug>-spec.md` with all seven sections (Problem Statement, Solution, User Stories, Implementation Decisions, Testing Decisions, Out of Scope, Further Notes) populated and agent-ready, publication is a separate human step.
