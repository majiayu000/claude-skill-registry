---
name: create-spec
description: "Guide a collaborative discussion that produces a comprehensive specification document at .turbo/spec.md. Use when the user asks to \"create a spec\", \"write a spec\", \"discuss a project plan\", \"spec out a project\", \"design a system\", \"let's plan this project\", \"help me scope this\", \"architect a solution\", or \"let's discuss before building\"."
---

# Create Spec

Guide a collaborative discussion to explore a project idea, then synthesize the conversation into a comprehensive specification at `.turbo/spec.md`.

## Step 1: Capture the Vision

Absorb whatever the user has provided — a sentence, a paragraph, a brain dump. Do not interrupt or ask questions yet. Restate the vision back in two or three sentences to confirm understanding.

Then use `AskUserQuestion` to ask 1-4 focused opening questions targeting the biggest unknowns. Skip anything the user already answered. Prioritize from:

- What problem does this solve, and for whom?
- Is this greenfield or does existing code/infrastructure exist?
- Are there strong technology preferences or constraints?
- What does the MVP look like versus the full vision?
- Are there hard deadlines, budget limits, or team size constraints?

## Step 2: Deep-Dive Discussion

Explore the project through multi-turn conversation. Cover these categories over the course of the discussion — track coverage internally but do not present them as a rigid checklist. Follow the user's energy and weave topics in naturally.

| Category | What to explore |
|---|---|
| **Users and personas** | Who uses this? Goals, pain points, technical sophistication |
| **Core features** | Primary capabilities and user-facing workflows |
| **Architecture** | Client/server split, monolith vs services, real-time needs, offline support |
| **Tech stack** | Languages, frameworks, databases, hosting — preferences and constraints |
| **Data model** | Key entities, relationships, storage strategy |
| **Integrations** | Third-party APIs, auth providers, external data sources |
| **Non-functional requirements** | Performance, security, accessibility, i18n, compliance |
| **MVP scope** | What ships first? What is explicitly deferred? |
| **Open questions** | Unknowns needing research, prototyping, or external input |

### Discussion Guidelines

- Use `AskUserQuestion` to ask one or two questions at a time, not a wall of questions. Use options with descriptions to frame trade-offs and offer concrete suggestions. Use `multiSelect` when choices are not mutually exclusive.
- When the user gives a short answer, probe deeper before moving on
- Offer concrete suggestions and trade-off analysis — be a collaborator, not an interviewer
- If the user says "you decide" or "what do you recommend", make a clear recommendation with reasoning
- When all categories have sufficient depth or the user signals readiness, confirm before moving to drafting

## Step 3: Draft the Spec

Synthesize the entire discussion into `.turbo/spec.md`. Structure the document organically based on what emerged in conversation:

- Include only sections with real substance — no placeholder filler
- Use concrete details from the discussion, not vague generalizations
- Where the user deferred a decision, capture it in an Open Questions section
- Where recommendations were accepted, state them as decisions with brief rationale
- Adapt the structure to the project — a CLI tool spec looks different from a SaaS platform spec
- Trace every specified component (data model, API, utility, service) to at least one consumer in the spec. If a component exists only to "support future work," either spec the future work concretely or defer the component. Unconnected components become dead code during implementation.

Create the `.turbo/` directory if it does not exist. Accept a different output path if the user provides one.

## Step 4: Run `/review-spec` Skill

After drafting the spec and before presenting it to the user:

1. Run the `/review-spec` skill with the full spec text
2. Run the `/evaluate-findings` skill on the combined review findings
3. Run the `/apply-findings` skill on the evaluated findings to incorporate accepted changes into the spec
4. For medium-confidence findings that require user judgment, use `AskUserQuestion` to present the trade-offs and let the user decide

## Step 5: Review and Finalize

Present the draft to the user. Use `AskUserQuestion` to offer three paths:

- **Approve** — spec is final
- **Revise** — user specifies sections to change; apply edits and re-present
- **Discuss more** — return to Step 2 for additional exploration, then re-draft

After approval:

> The spec is ready at `.turbo/spec.md`. To break it into implementation prompts, run `/create-prompt-plan`.

## Rules

- Never skip Step 2 — even with extensive initial context, confirm understanding and probe gaps
- The spec is the only output — do not create code, scaffolding, or other project files
- If the project is trivially small (single-file script, simple config), say so and suggest skipping the spec process
