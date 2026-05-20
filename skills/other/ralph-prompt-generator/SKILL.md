---
name: ralph-prompt-generator
description: Use when a user has a rough prompt that needs a staged prompt-improvement workflow for `$ralph-wiggum-codex`, with saved draft/final files and explicit review checkpoints.
---

# Ralph Prompt Generator

Companion skill for `$ralph-wiggum-codex`.

This skill does not exist to synthesize flags first. Its primary job is to improve the prompt itself through a staged prompt-improvement workflow, then finish with a small Ralph-specific handoff.

## Core Rule

Clarify, do not prescribe.

The receiving agent is equally capable. Improve the briefing, preserve the user's boundaries, and avoid doing the downstream agent's job.

## When To Use

Use this skill when:
- The source prompt is ambiguous, bloated, or structurally weak.
- The user wants a reusable prompt for `$ralph-wiggum-codex`.
- The task needs critique and revision, not just runner flag suggestions.
- The user wants saved planning, draft, and final prompt files in the repo.

Do not use this skill when:
- The user already has a production-ready Ralph prompt.
- The user wants `$ralph-wiggum-codex` executed immediately with no prompt rewrite.
- The only missing detail is a minor flag choice that can be handled inline.

## Inputs

Primary input:
- `<user_prompt>`

Optional supporting context:
- `<examples>`
- `<feedback>`

Treat `<examples>` as demonstrations, not new requirements. Treat `<feedback>` as revision guidance, not permission to weaken the original constraints.

## Repo-Backed Workspace

Use this workspace for all saved outputs:
- `docs/prompt-improver-spec/artifacts/implementation_plan.md`
- `docs/prompt-improver-spec/artifacts/task.md`
- `docs/prompt-improver-spec/artifacts/walkthrough.md`
- `docs/prompt-improver-spec/final-prompts/<prompt-name>-draft.md`
- `docs/prompt-improver-spec/final-prompts/<prompt-name>.md`

Determine `<prompt-name>` during planning using a descriptive kebab-case filename. Reuse the saved files on resume instead of redoing earlier analysis from scratch.

Delete the draft file after creating the final prompt.

## Required Workflow

Follow the staged workflow defined in `references/prompt-improver-workflow-codex.md`.

### Phase A

Planning only. Complete Steps 1-2.

Required work:
- Read `<user_prompt>` and any optional `<examples>` / `<feedback>`.
- Extract and normalize examples.
- Quote unclear or problematic phrases from the source prompt.
- Preserve all explicit MUST, MUST NOT, and DO NOT constraints.
- Create `docs/prompt-improver-spec/artifacts/implementation_plan.md`.
- Create `docs/prompt-improver-spec/artifacts/task.md`.
- Choose `<prompt-name>`.

`implementation_plan.md` must include:
- Step 1 example identification
- Step 2 planning analysis
- intent summary
- deployment summary
- task flowchart
- lessons from examples
- chain-of-thought approach assessment
- output format analysis
- variable plan
- structural notes
- ambiguities and questions
- prompt filename
- constraint-preservation checklist

End Phase A at a native Codex review checkpoint after Steps 1-2. Pause and ask the user to review the saved planning artifacts before continuing.

### Phase B

Initial draft only. Complete Step 3.

Required work:
- Read the saved planning artifacts instead of redoing them.
- Write the first improved prompt draft to `docs/prompt-improver-spec/final-prompts/<prompt-name>-draft.md`.
- Update `docs/prompt-improver-spec/artifacts/task.md` to mark Steps 1-3 complete.
- Include clarifying questions only if ambiguities remain.

The draft must:
- define the assistant role clearly
- introduce descriptive XML variables when useful
- preserve all constraints
- clarify the objective
- specify output expectations without pre-solving the task
- add anti-patterns or verification checklists only when they help

End Phase B with the saved draft path and any remaining clarifying questions. Do not emit the Ralph-ready invocation snippet yet.

### Phase C

Critique and revision planning only. Complete Step 4.

Required work:
- Read `docs/prompt-improver-spec/final-prompts/<prompt-name>-draft.md`.
- Append the critique and revision plan to `docs/prompt-improver-spec/artifacts/implementation_plan.md`.
- Update `docs/prompt-improver-spec/artifacts/task.md` for Step 4.

The critique must quote specific problem text and describe:
- issues identified
- areas needing expansion
- structural improvements
- constraint-preservation check

End Phase C at a second native Codex review checkpoint after Step 4. Pause and ask the user to review the critique before continuing.

### Phase D

Revision, final polish, and delivery. Complete Steps 5-6.

Required work:
- Read and reuse all existing prompt-improver artifacts.
- Apply the revision plan to strengthen weak sections.
- Save the final prompt to `docs/prompt-improver-spec/final-prompts/<prompt-name>.md`.
- Delete the draft file at `docs/prompt-improver-spec/final-prompts/<prompt-name>-draft.md`.
- Create `docs/prompt-improver-spec/artifacts/walkthrough.md`.
- Update `docs/prompt-improver-spec/artifacts/task.md` to mark all steps complete.

The final polish must verify:
- all original constraints are preserved
- XML tag usage is consistent when tags are used
- instructions are logically ordered
- the prompt is complete without doing the receiving agent's work

Final delivery must include:
- the completion message ending with `All 6 Steps Complete.`
- the saved final prompt path
- confirmation that the draft file was removed
- a short Ralph-ready invocation snippet that points to the saved final prompt file
- a final prompt structure that clearly covers `Objective`, `Acceptance Criteria`, `Source of Truth`, `Optional Verification`, and `Blocker Policy`

## Ralph-Specific Tailoring Is Secondary

After the prompt itself is finished, add only a small Ralph-specific wrapper:
- how to use the saved prompt with `$ralph-wiggum-codex`
- optional validation or progress-scope guidance if it materially helps
- optional flags only when they materially improve the run

The final deliverable is a production-ready prompt file plus a Ralph-ready invocation snippet, not a flags-first handoff block.

When the improved prompt is intended for `$ralph-wiggum-codex`, the prompt itself should normally include these sections:
- `Objective`
- `Acceptance Criteria`
- `Source of Truth`
- `Optional Verification`
- `Blocker Policy`

## Non-Negotiable Constraints

You must not:
- execute or answer the source prompt's underlying task
- remove or weaken original constraints
- invent missing facts without labeling them
- redo earlier phases from scratch when saved artifacts already exist
- leave the draft file behind after finalizing
- fill the prompt with example outputs that amount to doing the agent's work
- prescribe low-level execution steps unless the user explicitly asked for them

## Prompt Quality Checks

When drafting or revising, explicitly check:
- Clarity: quote confusing phrases and rewrite them
- Structure: fix ordering, grouping, and entry point issues
- Completeness: add missing briefing context, not extra deliverables
- Variables: keep placeholders and XML tags consistent
- Constraints: preserve MUST / MUST NOT / DO NOT rules
- Output format: show structure, not pre-filled answers
- Anti-over-engineering: remove content that does the downstream agent's job

## Optional Ralph Guidance

Model and flag guidance are secondary.

Only consult these references when the final Ralph wrapper actually needs them:
- `references/prompt-improver-principles.md`
- `references/openai-codex-prompting-2026.md`
- `references/ralph-flag-selection-matrix.md`

If a model name or OpenAI capability is uncertain, consult the `openaiDeveloperDocs` MCP dependency declared in `agents/openai.yaml`.
