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
5. Present and finalize

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

## Step 4: Draft the Spec

Synthesize the consulted skill and doc context plus the entire discussion into `.turbo/specs/<slug>.md` using the slug picked in Step 1. Structure the document organically based on what emerged in conversation:

- Include only sections with real substance — no placeholder filler
- Use concrete details from the discussion, not vague generalizations
- Where the user deferred a decision, capture it in an Open Questions section
- Where recommendations were accepted, state them as decisions with brief rationale
- Adapt the structure to the project — a CLI tool spec looks different from a SaaS platform spec
- Trace every specified component (data model, API, utility, service) to at least one consumer in the spec. If a component exists only to "support future work," either spec the future work concretely or defer the component.

Create the `.turbo/specs/` directory if it does not exist. Accept a different output path if the user provides one.

## Step 5: Present and Finalize

Present the draft to the user. Use `AskUserQuestion` to offer three paths:

- **Approve** — spec is final
- **Revise** — user specifies sections to change; apply edits and re-present
- **Discuss more** — return to Step 3 for additional exploration, then re-draft

After approval:

> The spec is ready at the resolved spec path. To break it into implementation prompts, run `/draft-prompt-plan`.

## Rules

- Never skip Step 3 — even with extensive initial context, confirm understanding and probe gaps
- The spec is the only output — do not create code, scaffolding, or other project files
- If the project is trivially small (single-file script, simple config), say so and suggest skipping the spec process
