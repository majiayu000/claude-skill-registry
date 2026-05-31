---
name: draft-spec
description: "Guide a collaborative discussion that produces a specification document at .turbo/specs/<slug>.md. Use when the user asks to \"draft a spec\", \"create a spec\", \"write a spec\", \"discuss a project plan\", \"spec out a project\", \"design a system\", \"let's plan this project\", \"help me scope this\", \"architect a solution\", or \"let's discuss before building\"."
---

# Draft Spec

Guide a collaborative discussion to explore a project idea, then synthesize the conversation into a comprehensive specification at `.turbo/specs/<slug>.md`.

## Task Tracking

At the start, use `TaskCreate` to create a task for each step:

1. Capture the vision and pick a slug
2. Consult task-specific skills and docs
3. Deep-dive discussion
4. Draft the spec
5. Resolve open questions
6. Present and finalize

## Step 1: Capture the Vision and Pick a Slug

Absorb whatever the user has provided — a sentence, a paragraph, a brain dump. Do not interrupt or ask questions yet. Restate the vision back in two or three sentences to confirm understanding.

Pick a slug for the spec file derived from the project or feature name:

- Lowercase
- Replace non-alphanumeric characters with hyphens
- Collapse consecutive hyphens
- Trim leading and trailing hyphens
- Truncate to 40 characters at a word boundary

Example: "Photo Sorter v2" → `photo-sorter-v2`. The user may pass an explicit slug; if so, honor it.

If `.turbo/specs/<slug>.md` already exists, use `AskUserQuestion` to ask whether to overwrite, append a numeric suffix (`-2`, `-3`, ...), or pick a different slug.

State the chosen slug and the resulting spec path before continuing.

Then use `AskUserQuestion` to ask 1-4 focused opening questions targeting the biggest unknowns. Skip anything the user already answered. Prioritize from:

- What problem does this solve, and for whom?
- Is this greenfield or does existing code/infrastructure exist?
- Are there strong technology preferences or constraints?
- What does the MVP look like versus the full vision?
- Are there hard deadlines, budget limits, or team size constraints?

## Step 2: Consult Task-Specific Skills and Docs

Ground architecture and tech-stack choices in current reality before the deep-dive discussion.

1. **Scan for matching skills.** Compare the vision and opening-question answers against available skill trigger descriptions. For each unambiguous match, run the skill via the Skill tool. This loads decision-level guidance (idiomatic patterns, known pitfalls, version constraints) before architectural choices are made. If unsure, do not load.
2. **Look up library or framework docs.** For any library, framework, or platform the user mentioned or the project clearly needs, query documentation MCP tools (or WebSearch as a fallback) when the decision hinges on current capabilities, supported versions, or known constraints.

Keep findings at the decision level: what tools can do, which approaches are idiomatic, which versions to target. Do not embed specific API signatures or code snippets into the spec. Those belong in implementation-time skill loads.

## Step 3: Deep-Dive Discussion

Interview the user relentlessly about every aspect of the project until you reach shared understanding. Gather behavioral requirements (the "what") before architectural design (the "how"), so design decisions land against a concrete set of requirements instead of being taken in the abstract. Track coverage internally but do not present the list as a rigid checklist. When the user jumps to architecture early, engage briefly then circle back to confirm the behavioral picture is complete.

### Requirements (gather first)

| Category | What to explore |
|---|---|
| **Users and personas** | Who uses this? Goals, pain points, technical sophistication |
| **Core behaviors** | Primary capabilities and user-facing workflows — the behaviors the system must exhibit |
| **Non-functional requirements** | Performance, security, accessibility, i18n, compliance |

### Design (gather after requirements are clear)

| Category | What to explore |
|---|---|
| **Architecture** | Client/server split, monolith vs services, real-time needs, offline support |
| **Tech stack** | Languages, frameworks, databases, hosting — preferences and constraints |
| **Data model** | Key entities, relationships, storage strategy |
| **Integrations** | Third-party APIs, auth providers, external data sources |

### Cross-cutting

| Category | What to explore |
|---|---|
| **MVP scope** | What ships first? What is explicitly deferred? |
| **Open questions** | Unknowns needing research, prototyping, or external input |

### Discussion Guidelines

- If a question can be answered by exploring the codebase, explore the codebase instead
- Use `AskUserQuestion` to ask one question at a time. Use options with descriptions to frame trade-offs and offer concrete suggestions. Use `multiSelect` when choices are not mutually exclusive.
- When the user gives a short answer, probe deeper before moving on
- Offer concrete suggestions and trade-off analysis — be a collaborator, not an interviewer
- For each question, recommend an answer with reasoning
- Walk down each branch of the design tree, resolving dependencies between decisions one-by-one
- When all categories have sufficient depth or the user signals readiness, confirm before moving to drafting

## Step 4: Draft the Spec

Synthesize the consulted skill and doc context plus the entire discussion into `.turbo/specs/<slug>.md` using the slug picked in Step 1. Use the fixed skeleton below.

````markdown
# <Project or Feature Name>

## Overview

<One or two paragraphs stating the problem being solved and the vision for the solution.>

## Users

<Personas and their goals. Omit this section if the project has no meaningful user role distinction (e.g., a single-integrator internal library).>

## Requirements

Enumerated behavioral requirements with stable IDs. Number requirements `R1`, `R2`, `R3`, ... IDs must stay stable once drafted so downstream artifacts can reference them reliably.

Pick either format per requirement; both can appear in the same spec.

**EARS format** — for unambiguous, testable behaviors:

- **R1.** When <trigger or condition>, the system shall <expected behavior>.

Adapt the slot to the EARS pattern that fits: `When` (event-driven), `While` (state-driven), `Where` (optional feature), `If ... then` (unwanted behavior), or a bare `The system shall ...` (ubiquitous).

**User story format** — for user-facing capabilities with acceptance criteria:

- **R2.** As a <persona>, I want <capability> so that <outcome>.
  - Acceptance: <criterion 1>
  - Acceptance: <criterion 2>

Group related requirements under `### <Subheading>` when the list grows past ~8 items. IDs stay contiguous across subheadings.

## Design

Technical approach that satisfies the requirements above. Cover the elements that apply:

- **Architecture** — component split, deployment shape, communication patterns
- **Tech stack** — languages, frameworks, libraries, hosting
- **Data model** — key entities, relationships, storage strategy
- **Integrations** — third-party APIs, auth providers, external data sources
- **Key flows** — sequence or data flow for any non-trivial interaction

State decisions, not options. Where a decision was deferred, move it to Open Questions.

## MVP Scope

<What ships first versus what is explicitly deferred. Omit this section if scope is not staged.>

## Open Questions

<Unresolved decisions needing further input, research, or prototyping. Omit this section if none remain after Step 5.>
````

### Drafting Rules

- `## Overview`, `## Requirements`, and `## Design` are mandatory. `## Users`, `## MVP Scope`, and `## Open Questions` are omitted when they would be empty.
- Use concrete details from the discussion, not vague generalizations.
- Every Design element must trace to at least one requirement. If a design element has no requirement to justify it, either add the requirement or drop the element.
- Every specified component (data model entity, API endpoint, utility, service) must trace to a consumer in the spec. If a component exists only to "support future work," either spec the future work as a requirement or defer the component.
- Where the user deferred a decision, capture it in Open Questions.
- Where recommendations were accepted, state them in Design with brief rationale.

Create the `.turbo/specs/` directory if it does not exist. Accept a different output path if the user provides one.

## Step 5: Resolve Open Questions

If the spec's Open Questions section is empty, contains "None," or does not exist, skip this step.

For each open question:

1. Analyze the question against the spec, prior discussion, and consulted-docs context from Step 2. State the trade-offs of the leading options in plain text so the user can see the reasoning.
2. Use `AskUserQuestion` to offer 2-3 concrete resolution options with short descriptions, plus a **Defer to implementation** option (leaves the question in Open Questions to be surfaced again when shells are expanded). Mark the strongest option "(Recommended)" and place it first.
3. Fold the chosen answer into the relevant spec section and remove the question from Open Questions.

If the user selects "Other" and provides a freeform answer, accept it and proceed.

Default to resolving. Defer only when the answer genuinely needs codebase or pattern-survey context that is not yet available. If every question resolves, delete the Open Questions section entirely.

## Step 6: Present and Finalize

Present a brief summary of the drafted spec: the problem, the chosen solution, and the shape of the requirements, short enough to read at a glance so the user does not have to read the full spec. Fit the summary to the spec rather than a fixed template.

Then use `AskUserQuestion` to offer two paths:

- **Approve** (Recommended) — the spec is final.
- **Revise** — the user describes what to change, whether specific edits or areas to rethink. Apply the edits, reopening the Step 3 discussion when the change needs exploration, then re-summarize and re-present.

After approval:

> The spec is ready at the resolved spec path. To break it into shells, run `/draft-shells`.

Then use the TaskList tool and proceed to any remaining task.

## Rules

- Never skip Step 3 — even with extensive initial context, confirm understanding and probe gaps
- The spec is the only output — do not create code, scaffolding, or other project files
- If the project is trivially small (single-file script, simple config), say so and suggest skipping the spec process
