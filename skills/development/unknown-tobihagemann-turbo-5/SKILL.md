---
name: draft-plan
description: "Produce an implementation plan at .turbo/plans/<slug>.md. Use when the user asks to \"draft a plan\", \"draft the plan\", \"write an implementation plan\", \"plan this change\", \"create an implementation plan\", or needs a first-draft plan file before refinement."
---

# Draft Plan

Produce an implementation plan at `.turbo/plans/<slug>.md`. Capture the task, survey patterns, escalate decisions, discuss, and draft.

## Task Tracking

Use `update_plan` to track each step:

1. Capture the task and pick a slug
2. Run `$survey-patterns` skill
3. Consult task-specific skills and docs
4. Escalate product decisions
5. Deep-dive discussion
6. Draft and write the plan file

## Step 1: Capture the Task and Pick a Slug

Absorb the user's request without interrupting. Restate the goal in one or two sentences and confirm.

Generate a slug for the plan file from the task title:

- Lowercase
- Replace non-alphanumeric characters with hyphens
- Collapse consecutive hyphens
- Trim leading and trailing hyphens
- Truncate to 40 characters at a word boundary

Example: "Add a caching layer to the image pipeline" → `add-a-caching-layer-to-the-image-pipeline`.

If `.turbo/plans/<slug>.md` already exists, append `-2`, `-3`, etc. until the path is free. Do not overwrite.

The user may pass an explicit slug or path in their request (e.g., "draft plan as `auth-rewrite`"). If so, honor it. If `.turbo/plans/<slug>.md` exists in that case, use `request_user_input` to ask whether to overwrite, append a numeric suffix, or pick a different slug.

State the chosen slug and the resulting plan path before continuing.

### Spec-Derived Input

If the task references an existing spec at `.turbo/specs/<slug>.md` (when a spec path is passed as input), treat the spec as the source of truth for product decisions and discussion areas. Read the spec, then:

- In Step 4, skip escalation for any product decision the spec resolves. Only escalate questions the spec did not answer.
- In Step 5, skip deep-dive areas the spec covers. Only discuss areas the spec did not address.
- Forward the spec's slug as the plan slug so the plan and spec share a slug. If `.turbo/plans/<spec-slug>.md` already exists, do not auto-suffix (that would break the shared-slug invariant). Use `request_user_input` to ask whether to overwrite or pick a different slug, mirroring Step 1's explicit-slug collision handling.

A question is resolved by the spec only when the spec makes a definitive statement that answers it. Mentions without a chosen direction, open questions in the spec, and deferred decisions do not count as resolved; escalate those normally.

Step 2 (pattern survey) and Step 3 (consult skills and docs) still run in full. The spec describes what; `$draft-plan` still surveys how.

## Step 2: Run `$survey-patterns` Skill

Run the `$survey-patterns` skill with the confirmed task description. Keep the returned findings in conversation context for use in Steps 5 and 6.

## Step 3: Consult Task-Specific Skills and Docs

Ground library and framework choices in current reality before escalating decisions.

1. **Scan for matching skills.** Compare the task description against available skill trigger descriptions. For each unambiguous match, run the skill by reading and following the installed skill instructions. This loads decision-level guidance (idiomatic patterns, known pitfalls, version constraints) before product decisions are made. If unsure, do not load.
2. **Look up library docs.** For libraries or frameworks the task clearly depends on, query documentation MCP tools (or WebSearch as a fallback) when the decision hinges on current library state such as whether a feature exists, which versions support it, or whether an API has been deprecated.

Keep findings at the decision level: what a library can do, which approach is idiomatic, which version to target. Do not embed specific API signatures or code snippets into the plan. Those belong in `$implement-plan`, which re-loads the same skills at execution time.

## Step 4: Escalate Product Decisions

Identify product or design decisions the user's request did not resolve. Escalate these via `request_user_input` before drafting steps.

**Escalate when:**

- A plan step requires choosing between user-facing behaviors the request did not specify (opt-in vs opt-out, strict vs lenient, sync vs async)
- The plan assumes product requirements that were not stated
- Design trade-offs affect UX or product direction rather than technical implementation
- Multiple valid approaches exist and the choice is a matter of product preference, not technical merit

**Do not escalate** technical decisions the agent can make autonomously: which data structure, which existing pattern to follow, internal implementation approach. The boundary is product intent.

Present each decision as a concise trade-off with options. Mark the strongest option "(Recommended)" and place it first. Draft plan steps that depend on these decisions only after the user responds.

## Step 5: Deep-Dive Discussion

Interview the user relentlessly about every aspect of the implementation shape until you reach shared understanding. Use `request_user_input`, one question at a time. Use the pattern survey findings to frame choices. Cover whichever of these matter for the task. Do not present a rigid checklist:

| Area | What to explore |
|---|---|
| **Reuse vs new** | Which survey findings should the new work build on? Which should it deliberately not follow, and why? |
| **File placement** | Where do new files live? Which existing files are modified? |
| **Data flow** | How does data move through the change? Any new boundaries or contracts? |
| **Edge cases** | Partial failure, empty states, backward compatibility, concurrency |
| **Tests** | Which existing test patterns apply? Where do new tests live? |
| **Scope cut** | Anything to explicitly defer? |

### Discussion Guidelines

- If a question can be answered by exploring the codebase, explore the codebase instead.
- Make recommendations with reasoning, not just questions. Be a collaborator, not an interviewer.
- Walk down each branch of the design tree, resolving dependencies between decisions one-by-one.
- When the user says "you decide," make the call and explain why.
- Probe short answers before moving on.
- When the shape is clear or the user signals readiness, confirm before drafting.

## Step 6: Draft and Write the Plan File

Synthesize the task description, pattern survey findings, consulted skill and doc context, resolved product decisions, and deep-dive discussion outcomes into a complete plan document.

Create `.turbo/plans/` if it does not exist. Write the plan to `.turbo/plans/<slug>.md` using the slug picked in Step 1 (or the override path from Step 1) using this structure:

````markdown
---
status: draft
---

# Plan: <Task Title>

## Context

<Why this change is being made — the problem or need it addresses, what prompted it, the intended outcome. One or two paragraphs.>

## Pattern Survey

<Insert the structured findings from `$survey-patterns`: Analogous Features, Reusable Utilities, Convention Anchors, Proposed Alignment. Use the same format the survey returned.>

## Implementation Steps

1. **<Step 1 title>**
   - <Concrete action with `file_path` references and named functions or symbols>
   - <Another action>
2. **<Step 2 title>**
   - ...
3. ...

## Verification

How to verify the change works end-to-end after implementation:

- <Specific test command, manual smoke check, or MCP tool invocation>
- <Expected observable result for each verification step>
- <Edge cases to spot-check>

## Context Files

Files to read in full before starting implementation:

- `<path/to/file1>` — <why it matters>
- `<path/to/file2>` — <why it matters>
- ...
````

### Content Rules for the Plan

- **Implementation Steps**: Use concrete `file_path` references and named functions or symbols. Reference existing functions and utilities from the Pattern Survey instead of reinventing them. Each step describes a discrete unit of work that can be tracked independently during execution.
- **Verification**: Describe how to know the change actually works. Prefer specific test commands, named test files, or named smoke checks over vague phrases like "run the tests." If the change has no observable behavior, say so explicitly.
- **Context Files**: Curate the minimum set needed to become productive. Do not dump every file touched — only the ones that anchor understanding.
- **Scope**: Plan content describes what to build. Do not embed task tracking, skill loading, `$finalize` invocation, test commands, or commit instructions in the plan content — those are execution-wrapper concerns.

Then update or check the active plan and proceed to any remaining task.

## Rules

- Never skip the pattern survey.
- Never skip decision escalation for questions left unanswered. When entering from a Spec-Derived Input, questions the spec already resolves are considered answered and may be skipped.
- The plan file is the only output. Do not write code, scaffolding, or other project files.
- Do not run `$review-plan` or any review skills here.
