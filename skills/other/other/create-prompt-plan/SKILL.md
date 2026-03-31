---
name: create-prompt-plan
description: "Decompose a specification file into context-sized implementation prompts. Use when the user asks to \"create a prompt plan\", \"break spec into prompts\", \"decompose spec into sessions\", \"plan prompts for spec\", \"generate prompts from spec\", or \"make prompts from spec\"."
---

# Create Prompt Plan

Read a specification file and decompose it into a series of implementation prompts. Each prompt represents one unit of work for a separate Claude Code session. Save the output to `.turbo/prompts.md`.

General skill assignment happens later by `/pick-next-prompt` when each prompt is planned for implementation. However, if the spec implies domain-specific skills, mention those specific skills in the prompt text as hints.

## Step 1: Read the Spec

Read the spec file. Default location: `.turbo/spec.md`. Accept a different path if provided by the user.

Identify:
- **Scope** — total surface area of work
- **Work categories** — UI, backend, data layer, infrastructure, tests, documentation, tooling
- **Dependencies** — which pieces must exist before others can start
- **Greenfield vs existing** — is there an established codebase to work within

## Step 2: Decompose Into Prompts

Split the spec into prompts where each prompt fits a single Claude Code context session.

### Sizing

- One prompt = one logical unit of work (a feature, a subsystem, a layer)
- Never split tightly-coupled pieces across prompts (if UI + API + tests are inseparable, keep them together)
- Split independent subsystems into separate prompts
- If a prompt would touch more than ~15-20 files or span 3+ unrelated subsystems, split further
- If the entire scope fits one session, produce a single prompt
- Each prompt must leave the codebase fully integrated, with no components unreachable from the project's entry points
- If a prompt creates a module, API, or data layer, the same prompt (or an earlier one) must wire it into something that calls it
- When a prompt builds infrastructure that a later prompt consumes, name the future consumer explicitly in the prompt text so the reviewer can trace the wiring

### Ordering

Order by dependency, foundational work before dependent work:

1. Setup and scaffolding (project init, config, CI)
2. Data and domain layer (models, schemas, types)
3. Core business logic
4. API and service layer
5. UI and frontend
6. Integration and end-to-end concerns

Mitigate dead code risk in bottom-up ordering by bundling tightly-coupled producer/consumer pairs into the same prompt, or having foundation prompts include a minimal integration point (e.g., a single working endpoint or CLI command) that proves the code is reachable.

### Status tracking

Each prompt gets a status: `pending`, `in-progress`, `done`.

## Step 3: Write .turbo/prompts.md

Create the `.turbo/` directory if it does not exist. Write the output using this format:

````markdown
# Prompt Plan: [Project/Feature Name]

Source: `.turbo/spec.md`
Generated: [date]
Total prompts: N

---

## Prompt 1: [Descriptive Title]
**Status:** pending
**Context:** [What state the project is in before this session starts]
**Depends on:** none

### Prompt

```
[What to build — specific files, features, acceptance criteria.
What "done" looks like — tests passing, endpoints working, etc.
Reference to spec sections if helpful.]
```

---

## Prompt 2: [Descriptive Title]
**Status:** pending
**Context:** [What prior prompts built that this one depends on]
**Depends on:** Prompt 1

### Prompt

```
[What to build...]
```
````

## Step 4: Run `/review-prompt-plan` Skill

After writing the prompt plan and before presenting it to the user:

1. Run the `/review-prompt-plan` skill with the prompt plan text
2. Run the `/evaluate-findings` skill on the combined review findings
3. Run the `/apply-findings` skill on the evaluated findings to incorporate accepted changes into the prompt plan
4. For medium-confidence findings that require user judgment, use `AskUserQuestion` to present the trade-offs and let the user decide

## Step 5: Present Summary

After writing and verification, present a brief summary: number of prompts, one-line description of each prompt's scope, and any assumptions made about ambiguities.

## Rules

- Never merge setup and finalization into the same prompt
- If the spec is ambiguous about what belongs together, split conservatively (smaller prompts are safer than oversized ones)
- Each prompt must be self-contained with enough context to understand the work without reading the full spec
- The `.turbo/prompts.md` file is the only output — do not modify the spec or project files
