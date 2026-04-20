---
name: expand-shell
description: "Expand a shell into a full implementation plan. Verifies Consumes against the current codebase, runs a fresh pattern survey, escalates open questions, and fills in concrete file references and verification. Use when the user asks to \"expand a shell\", \"expand shell\", \"fill in the shell\", \"expand the shell\", or \"concretize the shell\"."
---

# Expand Shell

Expand a shell into a full implementation plan. The shell's Context, Produces, Consumes, Covers, and high-level Implementation Steps are authoritative. Expansion adds a pattern survey, concrete references, and verification, writes the plan to `.turbo/plans/<shell-slug>.md`, and deletes the source shell once the plan is in place.

## Task Tracking

Use `TaskCreate` to create a task for each step:

1. Load the shell and verify consumes
2. Run `/survey-patterns` skill (shell-focused)
3. Escalate the shell's open questions
4. Write the plan
5. Verify the plan against the shell
6. Delete the shell

## Step 1: Load the Shell and Verify Consumes

Determine which shell to expand:

1. **Explicit path** — If a file path was passed, use it
2. **Single candidate** — Glob `.turbo/shells/*.md` and filter to shells whose `depends_on` are all satisfied (see satisfaction check below). If exactly one match, use it
3. **Multiple candidates** — If multiple matches, use `AskUserQuestion` to let the user choose
4. **Nothing found** — If no shells exist in `.turbo/shells/`, say so and stop

A `depends_on` entry is satisfied when `.turbo/plans/<dep-slug>.md` exists with `status: done` in its frontmatter.

Read the shell file. Parse the YAML frontmatter:

- **spec** (source spec path)
- **depends_on** (list of shell slugs that must already be implemented)

Parse these body fields:

- **Title** (from the `# Plan:` heading)
- **Context** (the why)
- **Produces** (artifacts this shell creates)
- **Consumes** (dependencies this shell requires)
- **Covers Spec Requirements** (the spec sections this shell implements)
- **Implementation Steps (High-Level)** (named tasks without file paths)
- **Open Questions** (decisions deferred to now)

Compute the shell slug from the filename (basename without `.md`). The expanded plan will be written to `.turbo/plans/<shell-slug>.md`.

**Verify Consumes are present in the current codebase.** For each Consumes entry:

- If marked "from existing codebase," grep or read relevant files to confirm the artifact still exists at the expected conceptual location
- If the entry references a prior shell's Produces, verify that the corresponding plan at `.turbo/plans/<prior-slug>.md` has `status: done` AND that the artifact is actually present in the current codebase (the prior implementation may have diverged)

If any Consumes entry fails verification, escalate via `AskUserQuestion`:

- **Adapt the shell** — open the shell for editing, adjust the shell's Consumes/Implementation Steps to match what actually exists, then re-verify
- **Skip this shell** — leave the shell in place and stop. Tell the user to run `/pick-next-shell` again or resolve the prior work.
- **Stop and investigate** — halt without edits so the user can debug

Do not proceed to Step 2 until all Consumes verify cleanly.

## Step 2: Run `/survey-patterns` Skill (Shell-Focused)

Run the `/survey-patterns` skill with a task description built from the shell's structural content:

```
<shell title>

Context: <shell Context>
Produces: <shell Produces, as a bulleted list>
Implementation steps: <shell Implementation Steps, numbered>
```

This scopes the survey to the shell's concern area instead of a generic sweep. Keep the returned findings in conversation context for use in Step 4.

## Step 3: Escalate the Shell's Open Questions

For each entry in the shell's `Open Questions` field, present it via `AskUserQuestion` and collect the answer. Frame each question with enough context from the shell for the user to decide.

Do **not** escalate other questions. If you identify a new question while reading the codebase, note it as a risk in the drafted plan's Verification or Context Files sections.

If the shell's Open Questions field is empty or contains "None," skip this step entirely and proceed to Step 4.

## Step 4: Write the Plan

Expand the shell into a full plan using:

1. The shell's Context as the plan's Context (preserve verbatim or lightly edit)
2. The shell's high-level Implementation Steps as the skeleton, concretizing each with `file_path:line_number` references, named functions, and specific symbols from the pattern survey
3. A Pattern Survey section with the Step 2 findings
4. A Verification section with specific test commands and expected observable results for this shell's work
5. A Context Files section listing the files an implementer needs to read in full

Create `.turbo/plans/` if it does not exist. Write the plan to `.turbo/plans/<shell-slug>.md` using this structure:

````markdown
---
status: draft
spec: <spec path from original shell frontmatter>
---

# Plan: <Task Title>

## Context

<Shell Context, preserved verbatim or lightly edited.>

## Pattern Survey

<Insert the structured findings from `/survey-patterns`: Analogous Features, Reusable Utilities, Convention Anchors, Proposed Alignment. Use the same format the survey returned.>

## Implementation Steps

1. **<Step 1 title>**
   - <Concrete action with `file_path:line_number` references>
2. **<Step 2 title>**
   - ...
3. ...

## Verification

- <Specific test command, manual smoke check, or MCP tool invocation>
- <Expected observable result>
- <Edge cases to spot-check>

## Context Files

- `<path/to/file1>` — <why it matters>
- `<path/to/file2>` — <why it matters>
````

The plan carries `spec` forward as provenance. `depends_on` and the structural contract (Produces, Consumes, Covers) are locked in at expansion and do not need to persist on the plan.

State the plan path before proceeding.

### Content Rules for the Plan

- **Implementation Steps**: Use concrete `file_path:line_number` references. Reference existing functions and utilities from the Pattern Survey instead of reinventing them. Each step describes a discrete unit of work that can be tracked independently during execution.
- **Verification**: Describe how to know the change actually works. Prefer specific test commands, named test files, or named smoke checks over vague phrases like "run the tests." If the change has no observable behavior, say so explicitly.
- **Context Files**: Curate the minimum set needed to become productive. Do not dump every file touched — only the ones that anchor understanding.
- **Scope**: Plan content describes what to build. Do not include task tracking, skill loading, test commands, or commit instructions — those are execution-wrapper concerns.

## Step 5: Verify the Plan Against the Shell

Re-read the shell at `.turbo/shells/<shell-slug>.md` and the drafted plan at `.turbo/plans/<shell-slug>.md`. Confirm the plan honors the shell's structural contract by checking each item below:

- **Produces** — Every artifact listed in the shell's Produces is created by at least one Implementation Step in the plan.
- **Consumes** — Every dependency listed in the shell's Consumes is referenced in the Implementation Steps, Context Files, or Pattern Survey.
- **Covers** — Every spec requirement listed in the shell's Covers is addressed by the Implementation Steps.
- **Context fidelity** — The plan's Context preserves the intent of the shell's Context (verbatim or lightly edited, not reinterpreted).
- **Scope** — The plan does not add artifacts or responsibilities beyond the shell's Produces. Scope creep belongs in a new shell, not this plan.

If every item passes, proceed to Step 6. If any item fails, revise the plan to close the gap and re-verify before proceeding. Do not delete the shell while any check is failing.

## Step 6: Delete the Shell

Delete the source shell at `.turbo/shells/<shell-slug>.md`. The plan is now the authoritative artifact for this work.

Then use the TaskList tool and proceed to any remaining task.

## Rules

- Never proceed past Step 1 if Consumes verification fails.
- The shell's structural contract (Produces, Consumes, Covers) is authoritative. If the pattern survey reveals conflicts, note them in the plan's Context or Verification sections rather than altering the contract.
- The plan file is the only output. Do not write code, scaffolding, or other project files.
- Delete the source shell only after the plan file has been written successfully and Step 5 verification has passed. Never delete before.
- Do not run `/review-plan` or any review skills here.
- Do not embed task tracking, skill loading, or `/finalize` invocation in the plan file.
