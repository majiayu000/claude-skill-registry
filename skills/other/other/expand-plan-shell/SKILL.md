---
name: expand-plan-shell
description: "Expand a shell plan into a full implementation plan. Verifies Consumes against the current codebase, runs a fresh pattern survey, escalates open questions, and fills in concrete file references and verification. Use when the user asks to \"expand a shell\", \"expand plan shell\", \"fill in the shell\", \"expand the shell\", or \"concretize the shell\"."
---

# Expand Plan Shell

Expand a shell plan into a full implementation plan. The shell's Context, Produces, Consumes, Covers, and high-level Implementation Steps are authoritative. Expansion adds a pattern survey, concrete references, and verification.

## Task Tracking

Use `TaskCreate` to create a task for each step:

1. Load the shell and verify consumes
2. Run `/survey-patterns` skill (shell-focused)
3. Escalate the shell's open questions
4. Fill in and write back to the shell path

## Step 1: Load the Shell and Verify Consumes

Determine which shell to expand:

1. **Explicit path** — If a file path was passed, use it
2. **Single candidate** — Glob `.turbo/plans/*.md`, filter to files with `type: shell` and `status: draft` whose `depends_on` are all `done`. If exactly one match, use it
3. **Multiple candidates** — If multiple matches, use `AskUserQuestion` to let the user choose
4. **Nothing found** — If no draft shells exist, say so and stop

Read the shell file. Parse the YAML frontmatter:

- **type** (must be `shell`)
- **status** (must be `draft` or `in-progress`)
- **spec** (source spec path)
- **depends_on** (list of shell slugs that must be `done`)

Parse these body fields:

- **Title** (from the `# Plan:` heading)
- **Context** (the why)
- **Produces** (artifacts this shell creates)
- **Consumes** (dependencies this shell requires)
- **Covers Spec Requirements** (the spec sections this shell implements)
- **Implementation Steps (High-Level)** (named tasks without file paths)
- **Open Questions** (decisions deferred to now)

**Verify Consumes are present in the current codebase.** For each Consumes entry:

- If marked "from existing codebase," grep or read relevant files to confirm the artifact still exists at the expected conceptual location
- If the entry references a prior shell's Produces, verify that the prior shell has `status: done` in its frontmatter AND that the artifact is actually present in the current codebase (the prior implementation may have diverged)

If any Consumes entry fails verification, escalate via `AskUserQuestion`:

- **Adapt the shell** — open the shell for editing, adjust the shell's Consumes/Implementation Steps to match what actually exists, then re-verify
- **Skip this shell** — leave the shell's frontmatter status as `draft` and stop. Tell the user to run `/pick-next-plan-shell` again or resolve the prior work.
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

## Step 4: Fill In and Write Back

Expand the shell into a full plan using:

1. The shell's Context as the plan's Context (preserve verbatim or lightly edit)
2. The shell's high-level Implementation Steps as the skeleton, concretizing each with `file_path:line_number` references, named functions, and specific symbols from the pattern survey
3. A Pattern Survey section with the Step 2 findings
4. A Verification section with specific test commands and expected observable results for this shell's work
5. A Context Files section listing the files an implementer needs to read in full

Update the shell's YAML frontmatter to set `status: ready`, then write the full plan to the shell file path (overwriting the shell content) using this structure:

````markdown
---
type: shell
status: ready
spec: <spec path from original frontmatter>
depends_on: <depends_on from original frontmatter>
---

# Plan: <Task Title>

<!-- Expanded from: <spec path> -->

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

### Content Rules for the Plan

- **Implementation Steps**: Use concrete `file_path:line_number` references. Reference existing functions and utilities from the Pattern Survey instead of reinventing them. Each step describes a discrete unit of work that can be tracked independently during execution.
- **Verification**: Describe how to know the change actually works. Prefer specific test commands, named test files, or named smoke checks over vague phrases like "run the tests." If the change has no observable behavior, say so explicitly.
- **Context Files**: Curate the minimum set needed to become productive. Do not dump every file touched — only the ones that anchor understanding.
- **Scope**: Plan content describes what to build. Do not include task tracking, skill loading, test commands, or commit instructions — those are execution-wrapper concerns.

Check your task list for remaining tasks and proceed.

## Rules

- The `type` field stays `shell` after expansion for traceability. Plans originating from shell decomposition are distinguishable from standalone `/draft-plan` output even after expansion.
- Never proceed past Step 1 if Consumes verification fails.
- The shell's structural contract (Produces, Consumes, Covers) is authoritative. If the pattern survey reveals conflicts, note them in the plan's Context or Verification sections rather than altering the contract.
- The plan file is the only output. Do not write code, scaffolding, or other project files.
- Do not run `/review-plan` or any review skills here.
- Do not embed task tracking, skill loading, or `/finalize` invocation in the plan file.
