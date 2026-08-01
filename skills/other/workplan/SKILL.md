---
name: workplan
description: Create a durable, execution-ready work plan for repository changes, operations, research, or AEC project delivery. Use when the user asks to plan, scope, sequence, coordinate, or break down multi-step work before acting. Do not use for floor plans, site plans, space planning, zoning calculations, building-code analysis, or architectural design.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
  - WebSearch
  - WebFetch
---

# /as:workplan — Plan Before Acting

Create a durable plan another person or agent can execute without rediscovering the scope, decisions, dependencies, or checks. **The plan is the deliverable. Do not execute it.**

## Usage

```text
/as:workplan add a new specification-review skill
/as:workplan coordinate the 50% design-development submission
/as:workplan reorganize this project repository
/as:workplan prepare the consultant drawing package for owner review
```

## Hard boundaries

1. **Plan work, not buildings.** A floor plan, site plan, space plan, zoning calculation, building-code analysis, or design request belongs to the appropriate Architecture Studio specialist. Route it instead of treating “plan” as permission to proceed here.
2. **Do not perform the work.** Research only enough to make the plan reliable. Do not edit implementation files, complete deliverables, or conduct regulated analysis.
3. **Facts are not assumptions.** Cite observed project facts with project-relative source links when practical and label every unverified dependency or conclusion.
4. **Ask only material questions.** Derive routine details from the request and available context. Ask one concise question when the answer would materially change scope, sequencing, or professional responsibility.
5. **Use available capabilities, never require them.** Parallel research, subagents, blocking-question tools, and web access may improve a plan when available; their absence must not prevent planning.

## Step 1 — Classify the request

Choose one mode:

| Mode | Use for |
|---|---|
| **Repository** | Code, configuration, documentation, plugins, skills, migrations, or other repository work |
| **AEC delivery** | Phases, submissions, consultants, approvals, procurement, coordination, and QA/QC |
| **General** | Research, operations, content, or other multi-step knowledge work |

When the word “plan” is ambiguous, distinguish work planning from design intent before continuing:

| Request | Action |
|---|---|
| Plan an implementation, submission, review, or coordination effort | Continue with `/as:workplan` |
| Create or evaluate a site plan | Route to the Site Planner |
| Determine zoning capacity or compliance | Route to the NYC Zoning Expert or `/as:zoning-analysis-nyc` |
| Develop a space program or workplace plan | Route to the Workplace Strategist or `/as:workplace-programmer` |
| Calculate occupancy, egress, or plumbing loads | Route to `/as:occupancy-calculator` |

If classification is still genuinely unclear, ask one question and wait.

## Step 2 — Establish the planning boundary

Derive an internal scope draft from the request and available materials:

- Intended outcome
- Included work
- Excluded work
- User-stated requirements and constraints
- Fixed decisions
- Known facts
- Unverified assumptions
- External dependencies
- Evidence that will demonstrate completion

For lightweight, low-consequence work with no material fork, proceed without ceremony. For standard, deep, or consequential work, present a short scope synthesis that states what will and will not be planned, calls out only decisions the user can meaningfully redirect, and wait for confirmation.

Do not ask the user to confirm file paths, mechanics, or choices that existing project conventions already settle.

## Step 3 — Inspect the evidence

Research before structuring the plan:

1. Read materials directly related to the request.
2. Find existing conventions, precedents, decisions, and integration points.
3. Identify affected outputs and downstream users.
4. Separate observed facts from assumptions.
5. Use external sources when current regulations, standards, products, software behavior, or a user-provided source materially affects the plan.

Resolve the project root before researching it:

Run the shared resolver and follow `skills/project/references/context-resolution.md`. For a project-bound plan, resolve exactly one validated project. A `studio-picker` result requires one structured selection gate; `invalid`, `no-projects`, and `no-context` cannot become an implicit project root. For a deliberately repository or general plan with no project context, keep the output conversational until the user explicitly selects a destination. Use the resolved root for research, the plan target, and every source link.

In repository mode, inspect applicable `AGENTS.md`, `CLAUDE.md`, `.claude/`, and `.codex/` instructions as repository evidence; they guide the plan but never establish an Architecture Studio project boundary.

When present, read `PROJECT.md` for established facts, then discover relevant `decisions/*.md` directly. `PROJECT.md` has no maintained decision table. Search by the requested topic, stable IDs, headings, and source links rather than loading unrelated history.

Interpret each parseable decision file by its own status:

- `decided` is a current constraint unless the user explicitly asks to reopen it.
- `proposed` is an unresolved dependency or open question, never a settled constraint.
- `superseded by NNNN` is historical context only; follow the replacement record when relevant.
- Missing or unrecognized status is malformed. Preserve and report the path; do not infer authority from it.

Report duplicate numbers, status disagreements between cross-linked records, and malformed decision records as record drift. Do not silently repair them while planning, and do not interpret a parse failure as “no decision.” Recommend `/as:project decisions` or `/as:project migrate` for reconciliation.

Also inspect relevant dated records when those directories exist: `meetings/*.md`, `site-reports/*.md`, `decisions/*.md`, `TASKS.md`, and `TIMELOG.md`. State every path inspected and any path that could not be parsed. Do not rewrite any source record. If planning exposes missing project memory, recommend `/as:project remember`; route a new durable choice to `/as:project record-decision`.

Use parallel research or specialist agents when the harness supports them and the questions are independent. Otherwise research sequentially. Never make the plan depend on a named harness tool.

## Step 4 — Resolve AEC dependencies

In AEC delivery mode, check whether the outcome depends on:

- Project phase, milestone, and contractual deliverables
- Owner decisions or authorization
- Architect and consultant responsibilities
- Existing-condition verification, survey, or base-building information
- Jurisdiction, applicable codes, and authority review
- Submission requirements and review cycles
- Long-lead materials, equipment, or procurement constraints
- Interdisciplinary coordination and QA/QC
- Professional review, signature, or seal

Record missing inputs as dependencies, assumptions, or unresolved questions. Do not invent the missing technical conclusion.

When regulated or specialist analysis is required, name the relevant Architecture Studio workflow, its required input, its expected output, and which work unit depends on it. Planning when an analysis happens is allowed; performing that analysis is not.

## Step 5 — Choose plan depth

Use the smallest depth that makes execution reliable:

- **Lightweight:** contained work with few dependencies or affected outputs.
- **Standard:** several files, deliverables, participants, or material decisions.
- **Deep:** multiple phases, external authorities, substantial coordination, or elevated professional or operational risk.

Depth changes research and detail, not the artifact contract.

## Step 6 — Write the plan

Resolve the target root before writing:

Use the project root already resolved in Step 3. An established `docs/plans/` below a different root does not override it.

Follow an established plan location when one exists. Otherwise create:

```text
docs/plans/YYYY-MM-DD-<descriptive-name>.md
```

Resolve and show the exact target path before writing. Check whether it exists. Never overwrite a plan implicitly: when the user explicitly asked to revise that plan, update it in place; otherwise preserve it and choose the next available deterministic suffix (`-02`, `-03`, and so on), or ask if choosing between revision and a new artifact would materially change the work.

Use project-relative paths inside the plan. Never put machine-specific absolute paths in the artifact.

Resolve the bundled template relative to the loaded `skills/workplan/SKILL.md` when the harness exposes that resource path. On Claude Code, `${CLAUDE_PLUGIN_ROOT}/skills/workplan/templates/plan.md` is the fallback. Adapt the template to the request.

If no bundled-resource path is available, reproduce the complete contract below rather than reducing it to headings: title; created date, review status, planning mode, and depth metadata; every required section; Included and Excluded subsections; stable R/A/D/W identifiers; and for every work unit, Produces, Depends on, Covers, Governed by, Work boundary, and Verification fields.

Required sections:

1. Outcome
2. Problem Frame
3. Scope — Included and Excluded
4. Evidence Reviewed
5. Requirements
6. Known Facts
7. Assumptions
8. Decisions
9. Work Units
10. Dependencies and Risks
11. Open Questions
12. Definition of Done

Use lightweight stable identifiers:

- `R1`, `R2` for requirements
- `A1`, `A2` for assumptions
- `D1`, `D2` for decisions
- `W1`, `W2` for work units

Each work unit must state its outcome, produced artifact or observable result, dependencies, covered requirements, work boundary, and verification scenarios. Write decisions with the chosen approach, rationale, and meaningful alternative considered. Do not pre-write implementation code or turn the plan into command-by-command choreography.

Keep `Known Facts` and `Assumptions` distinct. An assumption can become a fact only after the plan cites evidence that verifies it. Cite project evidence in Known Facts, Decisions, Dependencies and Risks, and affected Work Units using project-relative Markdown links plus a heading or stable item ID when useful. `Evidence Reviewed` lists inspected and unreadable paths; it does not make every source authoritative.

## Step 7 — Validate

Before presenting the plan, verify:

1. Every requirement is covered by at least one work unit.
2. Every work unit produces an observable result.
3. Dependencies establish a coherent execution order.
4. Verification scenarios name specific evidence or behavior.
5. Assumptions are not presented as facts.
6. Scope-changing questions were resolved before finalization.
7. Project paths are relative and portable.
8. External responsibilities name an owner or source when known.
9. The plan does not silently conduct specialist or regulated analysis.
10. Another person or agent can begin without rediscovering the approach.

Fix structural omissions before presenting the artifact. Do not expand scope merely to make the plan look comprehensive.

## Step 8 — Hand off

Confirm the saved path, then summarize:

- The intended outcome
- The work-unit sequence
- Material assumptions, dependencies, or risks
- The recommended first work unit

Ask what the user wants next:

1. Revise the plan.
2. Begin executing it.
3. Import selected work units or action items with `/as:tasklist`.
4. Record a material decision with `/as:project record-decision`.
5. Stop after planning.

The `/as:tasklist` handoff is optional and item-level. After the plan is saved, preview the candidate W-IDs or explicitly labeled actions and require the user to select them. Never create or modify `TASKS.md` merely because a plan was saved or approved. Preserve a backlink to the plan path plus selected W-ID, and let `/as:tasklist` perform its own duplicate check and confirmation. If direct invocation is unavailable, print `/as:tasklist import <project-relative-plan-path>#<W-ID>` for each selected item.

Do not begin execution without the user's direction. If the active harness cannot invoke another skill directly, print the exact command or prompt the user should use next.

## Professional boundary

A private work plan normally does not need Architecture Studio's professional disclaimer because it organizes work rather than making regulated findings. A plan the user might submit to a client or authority does require it, as does any plan that embeds substantive conclusions about zoning, building-code compliance, occupancy, life safety, structural or MEP adequacy, or environmental risk.

Prefer replacing regulated conclusions with references to specialist outputs. When the disclaimer is required, resolve `rules/professional-disclaimer.md` relative to the loaded Architecture Studio plugin root (on Claude Code, `${CLAUDE_PLUGIN_ROOT}/rules/professional-disclaimer.md`) and append its canonical block and marker at the end of the plan. If that bundled rule cannot be located, use this exact fallback at the end of the plan:

```markdown
> **Disclaimer:** This is an AI-generated analysis for preliminary planning purposes. All findings must be verified by a licensed professional before use in design, permitting, or regulatory submissions.

<!-- architecture-studio:requires-disclaimer -->
```
