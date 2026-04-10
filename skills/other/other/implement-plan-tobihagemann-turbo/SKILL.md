---
name: implement-plan
description: "Execute an implementation plan file produced by /draft-plan or /turboplan. Runs pre-implementation prep, loads task-specific skills by matching plan content against available skill triggers, executes the plan steps, and runs /finalize. Use when the user asks to \"implement plan\", \"implement the plan\", \"execute the plan\", \"run the plan\", \"implement plans/<slug>.md\", \"start implementing the plan\", or starts a fresh session to implement a previously drafted plan."
---

# Implement Plan

Execute an implementation plan file.

## Task Tracking

At the start, use `TaskCreate` to create a task for each step:

1. Resolve and read the plan file
2. Run `/code-style` skill
3. Read relevant files and load task-specific skills
4. Execute implementation steps
5. Run `/finalize` skill

## Step 1: Resolve and Read the Plan File

Determine which plan file to implement using these rules in order:

1. **Explicit path** — If an absolute or relative path was passed, use it
2. **Explicit slug** — If a slug was passed (e.g., `add-image-cache`), resolve to `.turbo/plans/<slug>.md`
3. **Single file** — Glob `.turbo/plans/*.md`, excluding shell files (see shell detection below). If exactly one non-shell file exists, use it
4. **Most recent** — If multiple non-shell files exist, use the most recently modified
5. **Legacy fallback** — If `.turbo/plans/` does not exist but `.turbo/plan.md` exists, use it
6. **Nothing found** — If no plan file exists, tell the user to run `/turboplan` (for a new task) or `/pick-next-prompt` (for an existing prompt plan) and stop

If multiple files exist and the most-recent choice is non-obvious (e.g., several plans were modified within the same minute), use `AskUserQuestion` to let the user pick from the candidates.

### Shell Detection

A file is a **shell** when it contains `## Produces`, `## Consumes`, and `## Covers Spec Requirements` AND does NOT contain `## Pattern Survey`.

If the resolved file is a shell, halt with:

> `<path>` is a shell plan from `/create-prompt-plan`. Shells need to be filled in before implementation. Run `/pick-next-prompt` to advance the prompt plan.

State the resolved plan path before continuing, then read the file.

Parse the plan's sections:

- **Context** — the why
- **Pattern Survey** — existing patterns and utilities to reuse
- **Implementation Steps** — the ordered work
- **Verification** — how to confirm the change works after implementation
- **Context Files** — files to read in full before editing

## Step 2: Run `/code-style` Skill

Run the `/code-style` skill to load code style principles.

## Step 3: Read Relevant Files and Load Task-Specific Skills

### Read Relevant Files

Read in full:

- Every file listed in the plan's **Context Files** section
- Files the user referenced in their original request (if any)
- Every file path the plan references in the Context, Pattern Survey, and Implementation Steps sections
- One or two similar files in the project to mirror their style when creating new files or extending existing patterns

### Identify and Load Task-Specific Skills

Scan the plan's **Implementation Steps** for work types that match available skills. For each unambiguous match, run the skill via the Skill tool before editing.

To identify matches:

1. Scan the available skill list
2. For each skill, compare its trigger description against the plan's Implementation Steps
3. Load skills whose triggers clearly match the work. For example, if the plan includes "add a Drizzle migration" and a skill exists whose triggers reference Drizzle migrations, load it. If the plan mentions "run the test suite" but no testing-specific skill trigger matches, do not load a generic testing skill.

If unsure, do not load. Do not load `/code-style` here — it was loaded in Step 2.

## Step 4: Execute Implementation Steps

Work through the plan's Implementation Steps in order. Use `TaskCreate` to add one task per plan step. Mark each task `in_progress` when starting and `completed` when done.

Follow the plan's `file_path:line_number` references. Reuse patterns and utilities listed in the Pattern Survey instead of reimplementing them.

After the last Implementation Step, run the plan's Verification section: execute the test commands, smoke checks, or MCP tool invocations it lists. If any verification step fails, stop and investigate before moving to `/finalize`.

If a step cannot be completed (blocked by a dependency, unclear requirement, or environmental issue), stop and report. Do not silently skip steps.

## Step 5: Run `/finalize` Skill

After all Implementation Steps and the Verification section are complete, run the `/finalize` skill. `/finalize` runs polish, changelog, self-improvement, commit, and PR.

## Rules

- The plan file is read-only during execution. If revisions are needed, run `/refine-plan` or `/draft-plan` separately.
- Never skip Step 3. Pre-implementation prep catches style-mirroring gaps and skill loading that the plan content cannot enforce on its own.
- Never skip Step 5. `/finalize` is mandatory even for small plans. Context window, perceived task simplicity, and diff size are not reasons to skip it.
- Do not edit the plan as part of execution.
