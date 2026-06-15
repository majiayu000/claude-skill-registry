---
name: unikit-implement
description: >-
  Execute implementation tasks from a feature plan in .unikit/plans/.
  Reads TASKS.md and PLAN-BRIEF.md, then implements uncompleted tasks sequentially
  executing tasks inline (Read/Edit/Write/Bash) with rules loaded once at start. Supports selective execution by phase
  or task numbers. Use when the user says "implement", "start coding", "execute plan",
  "continue implementation", "do the next task", "implement phase 3", or wants to work
  through a planned feature. Also use when the user references tasks from .unikit/plans/
  or asks to "continue where we left off".
argument-hint: "[--list] [@<folder>] [Phase N | Phases N-M | Tasks N.M N.K | status | empty for all pending]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash(ls *)
  - Bash(find *)
  - Bash(wc *)
  - Bash(git *)
  - Agent
  - Skill
  - AskUserQuestion
disable-model-invocation: false
user-invocable: true
metadata:
  author: unikit
  version: "2.3"
  category: implementation
---

# {{engine_name}} Feature Implementation

Execute tasks from a feature plan stored in `.unikit/plans/`. This skill reads the plan, identifies pending work, and implements tasks inline with `Read/Edit/Write/Bash` after a one-time Bootstrap of rules and principles. The `develop-agent` alias is reserved for true parallel scopes or deep-dive single tasks.

## Language Awareness — BLOCKING PRE-REQUISITE

**BEFORE producing ANY output**, silently read `.unikit/system/LANGUAGE_RULES.md`
and apply its rules to ALL subsequent output.
If the file is missing or unreadable, fall back to English.
Do not produce any user-facing output until language rules are loaded.
Do not announce, confirm, or mention the language setting.

<!-- unikit:agents codex -->
## Subagent Delegation — BLOCKING PRE-REQUISITE

When the workflow reaches a step that requires a subagent (`Agent`), the assistant MUST automatically spawn the
subagent if agent execution is supported by the current environment and not prohibited by higher-priority
instructions.

Only if agent execution is unavailable or blocked, the assistant MUST ask the user before proceeding with any
alternative.
<!-- unikit:end -->

## Delegation agents

This skill uses named delegation aliases for `Agent(...)` calls. Each alias expands to an `Agent(subagent_type: "general-purpose", ...)` invocation with the matching skill loaded.

- **`develop-agent`** — used ONLY for true parallel scopes or deep-dive single tasks. Sequential tasks are implemented inline by this skill using rules loaded in Bootstrap. Expands to:

  ```
  Agent(
    subagent_type: "general-purpose",
    prompt: "/unikit-devcontext <task details>",
    description: "Implement <task>",
    skills: ["unikit-devcontext"]
  )
  ```

  Fallback: if the `Agent` tool is unavailable, invoke `/unikit-devcontext` inline.

- **`rules-agent`** — capture a new project rule. Expands to:

  ```
  Agent(
    subagent_type: "general-purpose",
    prompt: "/unikit-rules Add rule: <rule text>",
    description: "Record project rule",
    skills: ["unikit-rules"]
  )
  ```

  Fallback: if the `Agent` tool is unavailable, invoke `/unikit-rules` inline, one rule at a time.

- **`docs-agent`** — update or create documentation. Expands to:

  ```
  Agent(
    subagent_type: "general-purpose",
    prompt: "/unikit-docs <context>",
    description: "Update documentation",
    skills: ["unikit-docs"]
  )
  ```

  Fallback: if the `Agent` tool is unavailable, invoke `/unikit-docs` inline.

## Input

`$ARGUMENTS` — optional. Can be:
- **Empty** — execute all pending tasks from the latest feature, in order
- **`--list`** — list available feature plans in `.unikit/plans/` and STOP (no implementation)
- **`@<path>`** — explicit path to a feature folder, resolved from project root. Bypasses all auto-detection. Use when you need to point to a plan outside `.unikit/plans/` or want an unambiguous full path (e.g. `@.unikit/plans/2026-03-10_core-loop`, `@/absolute/path/to/plan-folder`)
- **`status`** — show progress without executing any tasks
- **`Phase N`** (e.g. `Phase 3`) — execute only tasks from Phase N
- **`Phases N-M`** (e.g. `Phases 1-3`) — execute tasks from Phases N through M
- **`Task N.M`** or **`Tasks N.M N.K`** (e.g. `Tasks 2.1 2.3 5.2`) — execute only the specified tasks
- **Feature name** (e.g. `core-loop`) — shorthand lookup: scans `.unikit/plans/` for a folder whose name **contains** this value. Compared to `@<path>`, this is a convenience shorthand that only searches inside `.unikit/plans/`

**`@<path>` vs Feature name:** `@` takes an explicit path (relative or absolute) and expects a folder with `TASKS.md` inside — no searching. A bare name without `@` is a fuzzy match inside `.unikit/plans/`. When both could apply, `@` wins (highest priority).

Mixed input is supported: `@.unikit/plans/2026-03-08_customers-system Phase 3` (explicit path + phase), `core-loop Phase 3` (name search + phase), `Tasks 2.1 2.3` (specific tasks from latest feature).

## Workflow

### Step 0: Pre-flight Checks

#### 0.1: Parse Arguments & Find the Feature Folder

**Parse `$ARGUMENTS` (priority order):**

1. If `$ARGUMENTS` contains `--list` → skip to **List Available Plans** section
2. If `$ARGUMENTS` contains `@<path>` → extract path after `@`, use as explicit feature folder (skip all auto-detection). See **Explicit Folder Override** below.
3. If `$ARGUMENTS` is or contains `status` → skip to **Status Display** section (can combine with `@<path>`)
4. Look for explicit selectors (can combine with `@<path>` or feature name):
   - `Phase N` — single phase
   - `Phases N-M` — phase range
   - `Task N.M` or `Tasks N.M N.K` — specific tasks
5. If no `@<path>` was found, check remaining args for a **feature name** — a bare string (no `@` prefix) that matches a folder name in `.unikit/plans/` by substring (e.g. `core-loop` matches `2026-03-10_core-loop`). This is a convenience shorthand that only searches inside `.unikit/plans/`.
6. Bare numbers without prefix are NOT selectors — they might be part of the feature name. Phases and tasks must be explicitly prefixed.

#### List Available Plans (`--list`)

If `$ARGUMENTS` contains `--list`, run read-only plan discovery and stop.

1. Get current branch: `git branch --show-current` (if git is unavailable, skip branch matching)
2. Scan `.unikit/plans/` for all feature folders
3. Check existence of `.unikit/FIX_PLAN.md`
4. For each feature folder, read its `TASKS.md` and count completed/total tasks
5. Print plan availability summary:

```
Available plans in .unikit/plans/:

  Branch match:
    2026-03-10_core-loop      (12/40 tasks, 30%)  ← matches current branch

  Other plans:
    2026-03-08_customers-system   (18/18 tasks, 100% — completed)
    2026-03-05_inventory-rework   (5/22 tasks, 23%)

  Fix plan: .unikit/FIX_PLAN.md — exists

Usage:
  /unikit-implement                              — auto-detect by branch
  /unikit-implement @.unikit/plans/<folder>      — use specific plan
  /unikit-implement <folder-name> Phase 3        — specific folder + phase
```

**Important:** In `--list` mode — do not execute tasks, do not modify files. STOP after displaying the list.

#### Explicit Folder Override (`@<path>`)

If `$ARGUMENTS` contains `@<path>`:

1. Extract path after `@` (e.g. `@.unikit/plans/2026-03-08_customers-system` → `.unikit/plans/2026-03-08_customers-system`)
2. Resolve relative to project root (absolute paths are also valid)
3. If folder does not exist or does not contain `TASKS.md`:
   ```
   Feature folder not found or invalid: <path>
   Expected a folder with TASKS.md inside, for example:
     /unikit-implement @.unikit/plans/2026-03-10_core-loop
   ```
   → STOP
4. Use this folder as the active feature — skip all auto-detection logic

The `@<path>` argument can be combined with selectors: `/unikit-implement @.unikit/plans/2026-03-08_customers-system Phase 3`

**Feature folder resolution priority:**
1. `@<path>` — explicit path, no searching (highest)
2. **Feature name** — bare string, substring match inside `.unikit/plans/`
3. **Auto-detect** — git branch match or latest by date (lowest, see below)

**If no feature folder specified (no `@<path>`, no feature name in args) — auto-detect:**

Use unified plan detection (priority order):

1. **Fast plan check** — if `.unikit/PLAN.md` exists, use it (flat fast-mode plan).
   The plan is a single file containing all sections (Overview, Checklist, Technical Context).
   When using `.unikit/PLAN.md`, there is no separate `PLAN-BRIEF.md` — everything is inline.

2. **Git branch match** — get current branch via `git branch --show-current`.
   If git is unavailable, skip to the next priority level.
   If on a `feature/*` branch, extract the feature name (e.g. `feature/core-loop-part1` → `core-loop-part1`).
   Scan `.unikit/plans/` for a folder whose name **ends with** `_<feature-name>` (new format)
   or matches `*-<feature-name>` (legacy `DDD-*` format).
   If match found → use it.

3. **Latest by date** (fallback) — sort all folders in `.unikit/plans/` **lexicographically descending**
   and pick the first one. Since new-format folders start with `YYYY-MM-DD`, this gives chronological order.
   Legacy `DDD-*` folders sort before `2xxx-*`, so new-format plans take natural priority.

4. If `.unikit/plans/` is empty or doesn't exist (and no `.unikit/PLAN.md`):

**First, check for `.unikit/FIX_PLAN.md`:**

If `.unikit/FIX_PLAN.md` exists — a fix plan was created by `/unikit-fix` in plan mode. Redirect to fix workflow:

```
Fix plan detected (.unikit/FIX_PLAN.md).

This plan was created via /unikit-fix and should be executed through the fix workflow
(it creates a patch and automatically cleans up the plan after execution).

Launching /unikit-fix to execute the plan...
```

→ `/unikit-fix` (without arguments — it will detect FIX_PLAN.md and execute it).
→ **STOP** — do not continue with implement workflow.

**If no plan found at all:**

Instead of silently stopping, present an interactive menu:

```
No active plan found. Current branch: <current-branch>.

Options:
1. Plan a new feature — /unikit-plan full <description>
2. Plan a quick task — /unikit-plan fast <description>
3. Fix a bug — /unikit-fix <description>
4. Just checking status — show branch info and stop
```

Based on choice:
- Plan feature → ask for description via AskUserQuestion, run `/unikit-plan full <description>`
- Quick task → ask for description, run `/unikit-plan fast <description>`
- Fix bug → ask for description, run `/unikit-fix <description>`
- Just checking → show `git branch --show-current` + `git log --oneline -5` → **STOP**

STOP here after handling the choice.

**If both `.unikit/PLAN.md` and a matching folder plan exist**, ask the user which one to use.

#### 0.2: Check for Uncommitted Changes

**Skip this step for read-only modes (`--list`, `status`) — they already STOPped in Step 0.1.**

Before any implementation work, check `git status`. If git is unavailable (not initialized), skip this step entirely and proceed to plan loading.

```bash
git status
```

**If uncommitted changes exist:**

```
Uncommitted changes detected.

Options:
1. Commit now (recommended)
2. Stash and continue (git stash)
3. Cancel — I'll handle it myself
```

Based on choice:
- Commit now → run /unikit-commit, then continue to plan discovery
- Stash → `git stash push -m "unikit-implement: stash before execution"`, then continue
- Cancel → inform "Implementation cancelled." → **STOP**

#### 0.3: Resume / Recovery (after `/clear` or session break)

If the user is resuming after a break, says the session was abandoned, or context was likely lost (e.g. after `/clear`), rebuild context from the repo before continuing. If git is unavailable, skip git commands and rely on plan file state only.

```bash
git status
git branch --show-current
git log --oneline --decorate -15
git diff --stat
```

Then reconcile plan state with reality:
- Read `TASKS.md` and check which tasks are marked `[x]`
- For tasks marked `[x]`, spot-check that the corresponding code actually exists (read a key file or check for expected classes/methods)
- If code for a completed task is missing (e.g. after reset/rebase), revert the checkbox back to `- [ ]` and inform the user
- If code exists but the task isn't marked complete, mark it `[x]` and inform the user

### Step 1: Load Plan Context

**If using `.unikit/PLAN.md`** (fast-mode plan):
- Read **`.unikit/PLAN.md`** — single file containing checklist, overview, settings, and optionally technical context inline
- Read **`.unikit/DESCRIPTION.md`** — project specification, tech stack, constraints
- Read **`.unikit/ARCHITECTURE.md`** — project structure, tech stack, and pointers to detailed rules

**If using a folder plan** (`.unikit/plans/<folder>/`):
- Read **`TASKS.md`** — feature overview (`## Overview`), task checklist with phases, dependencies, and completion status
- Read **`PLAN-BRIEF.md`** — technical context: constraints, interfaces, key patterns, dependency graph, files, DI bindings (if exists in plan folder)
- If `TASKS.md` has a `## Based on` section pointing to a research → read that research's `RESEARCH_BRIEF.md` instead
- Read **`.unikit/DESCRIPTION.md`** — project specification, tech stack, constraints
- Read **`.unikit/ARCHITECTURE.md`** — project structure, tech stack, and pointers to detailed rules

The roadmap (or PLAN.md) tells you WHAT to do and WHY (via `## Overview`); `PLAN-BRIEF.md` tells you HOW (technical context); DESCRIPTION.md and ARCHITECTURE.md give project-wide context.

**Read `.unikit/skill-context/unikit-implement/SKILL.md`** — MANDATORY if the file exists.

This file contains project-specific workflow rules added by `/unikit-skills-context` or `/unikit-evolve`.
These rules change how this skill orchestrates work (priorities, delegation, commit behavior, etc.).

**How to apply skill-context rules:**
- Treat them as **project-level overrides** for this skill's general instructions
- When a skill-context rule conflicts with a general rule written in this SKILL.md,
  **the skill-context rule wins** (more specific context takes priority)
- When there is no conflict, apply both: general rules from SKILL.md + project rules from skill-context
- Do NOT ignore skill-context rules even if they seem to contradict this skill's defaults —
  they exist because the project's experience proved the default insufficient

**Parse Settings:**

Read the `## Settings` section from `TASKS.md` (or from `PLAN.md` in fast-mode):
- `Testing: yes` → after completing each phase, write tests inline (default) for the code created in that phase, or via `develop-agent` for parallel/deep-dive (same execution-mode logic as Step 3.2)
- `Testing: no` → skip test creation entirely
- `Docs: yes` → after all tasks are completed, show a mandatory documentation checkpoint (Step 5.4)
- `Docs: no` → skip documentation checkpoint, emit warning

If `## Settings` section is missing, default to `Testing: no`, `Docs: no`.

Store the parsed settings — they affect behavior in Step 3.8 (tests), Step 3.9 (commit), and Step 5.4 (documentation).

Understand:
- Which tasks are completed (`- [x]`) and which are pending (`- [ ]`)
- Phase dependencies (a phase can only start when its dependencies are done)
- The overall architecture and technical decisions from the description

### Step 1.5: Bootstrap Rules & Principles

Load the project knowledge base ONCE at the start of execution. This replaces per-task delegation to `/unikit-devcontext` for sequential work.

**Read in parallel:**
1. `.unikit/system/dev-principles.md` — engine development principles (Core Principles + Workflow that used to live in /unikit-devcontext)
2. `.unikit/RULES.md` — project overrides (highest priority)
3. `.unikit/memory/RULES_INDEX.md` — index of core/stack rules
4. For EACH row in the Core table where Required By = `all` or contains `unikit-implement` — read that file from `.unikit/memory/core/` using the Read tool.

Stack rules are NOT loaded here — they are loaded lazily per-phase in Step 3.0.

Keep an in-memory list of loaded rule file paths (`loaded_rules`). Used in Step 3.0 for delta detection.

### Step 2: Determine Work Scope

**If all tasks are completed (`- [x]`):**

```
All tasks in {feature-folder} are completed.
Nothing to implement.
```
STOP here.

**If `$ARGUMENTS` contains phase/task selectors:**

- **`Phase N`** (e.g. `Phase 3`): collect all pending tasks from Phase N
- **`Phases N-M`** (e.g. `Phases 1-3`): collect all pending tasks from Phases N through M
- **`Task N.M`** or **`Tasks N.M N.K`** (e.g. `Tasks 2.1 2.3`): collect only those specific pending tasks
- If a specified task is already completed, skip it and note this to the user
- If a phase depends on an incomplete phase, warn the user but proceed if they confirm

**If no selectors (execute all pending):**

Collect all pending tasks across all phases, respecting dependency order:
1. Start with phases that have no unmet dependencies
2. Within a phase, execute tasks in order (1.1, 1.2, 1.3...)
3. After completing a phase, check if any new phases are now unblocked

### Step 3: Execute Tasks

Keep a running list of files you create, modify, or delete during execution — you'll need it for the completion summary and commit.

**3.0: Phase Rules Refresh (before starting each phase)**

Before executing the first task of any phase (including the first phase):
1. Re-read `.unikit/memory/RULES_INDEX.md` (it may have been updated by `/unikit-memory` since Bootstrap).
2. Match the phase name and its task descriptions against the Stack table's `Load When` column.
3. Compute delta: stack rules needed for this phase that are NOT in `loaded_rules`.
4. Read each delta rule from `.unikit/memory/stack/` using the Read tool.
5. Add them to `loaded_rules`.

Inside a phase, do NOT re-check rules between individual tasks — they share the same loaded set.

**Before starting the first task**, display the execution overview:

```
## Implementation Progress

✅ Completed: {X}/{total} tasks
🔄 Executing: Phase {N} — {Y} tasks pending in scope
⏳ Remaining after scope: {Z} tasks
```

For each task to execute:

**3.1: Present the task**

Show the user what you're about to implement:
```
## Phase {N}: {Phase Name}
### Task {N.M}: {task description}
Status: Pending
Dependencies: {met/unmet}
```

**3.2: Implement the task**

This skill OWNS code-writing for sequential tasks. Use `Read/Edit/Write/Bash` directly with the rules already loaded in Step 1.5 + Step 3.0. Do NOT invoke `/unikit-devcontext` via `Skill(...)` — that defeats the rules-loading optimization.

Choose execution mode:
- **Sequential within phase** (default for tasks that depend on each other or share files) → inline implementation. The skill writes code itself.
- **Independent across phases** (per the dependency graph in TASKS.md, e.g. Phase 3 and Phase 4 can run in parallel) → spawn `develop-agent` (Agent + /unikit-devcontext) per independent scope. Use ONLY for true parallelism.
- **Deep-dive single task** (requires extensive codebase exploration that would bloat parent context) → spawn `develop-agent` to isolate the exploration.

When implementing inline, use the rules from Bootstrap + Phase Rules Refresh, the principles from `dev-principles.md`, the task description from `TASKS.md`, and the technical context from `PLAN-BRIEF.md`.

**Fallback:** If `Agent` tool is unavailable, do NOT invoke `/unikit-devcontext` inline (rules and dev-principles are already loaded in Step 1.5 / Step 3.0). Instead, degrade parallel scopes to sequential and continue the inline implementation cycle for ALL tasks. Each phase still triggers Step 3.0 Phase Rules Refresh.

**3.3: Handle Blockers**

If a task cannot be completed (compilation error, missing dependency, unclear requirement, etc.):

```
Blocker on task {N.M}

Problem: {description of what went wrong}

Options:
1. Skip and continue (task will be marked as blocked)
2. Change implementation approach
3. Stop implementation and discuss
```

Based on choice:
- Skip → mark task as blocked in TASKS.md, continue to next task
- Change approach → discuss alternative with user, retry task
- Stop → pause implementation → **STOP**

**3.4: Mark task as completed**

After successful implementation, update `TASKS.md`:
- Change `- [ ] {task}` to `- [x] {task}`
- If all tasks in a phase are done, update the phase status: `**Status:** [x] Completed`

Use the Edit tool to make these changes surgically.

**3.5: Progress report**

After each task (or batch of parallel tasks), briefly report:
```
✅ Task {N.M}: {one-line summary of what was done}
Progress: {completed}/{total} ({percent}%) · {remaining} remaining in scope
```

**3.6: Compilation & Console Check (after completing a phase)**

After all tasks in a phase are done, check {{engine_name}} console for compilation errors.

**Prerequisite:** Check if {{engine_mcp_tool}} is configured in `{{settings_file}}` at the project root. If {{engine_mcp_tool}} is not present in MCP settings — skip this step entirely and proceed to 3.7.

**If {{engine_mcp_tool}} is available:**

1. Read the {{engine_name}} console log via {{engine_mcp_tool}}, filtering for errors
2. Analyze each error:
   - **Error relates to code created/modified in the current phase** → fix it inline using the same execution mode logic as Step 3.2 (default: inline; develop-agent only for true parallel/deep-dive)
   - **Error relates to code planned in a future phase** (check remaining tasks in `TASKS.md`) → skip, note in progress report: `"Known error: {description} — will be resolved in Phase {N}, task {N.M}"`
   - **Error is pre-existing and unrelated to the current feature** → skip, do not touch
3. After fixing, re-read the console log to verify fixes didn't introduce new errors
4. Repeat the check→fix cycle until no errors from the current phase remain

This step is critical: do NOT proceed to commit (3.9) with compilation errors that belong to the current phase. Future-phase errors are acceptable — they indicate planned work, not broken code.

**3.7: Update context artifacts (if project structure changed)**

After completing a phase, check whether the implementation introduced structural changes that should be reflected in context files:

- **If the tech stack changed** (new dependencies, integrations, or tools added) → update `.unikit/DESCRIPTION.md` with factual deltas only. Do not rewrite — add or modify the relevant section.
- **If new modules, directories, or layers were added** → update `AGENTS.md` — refresh the project structure tree and key entry points table to reflect new directories/files.
- **If new modules or dependency rules changed** → update `.unikit/ARCHITECTURE.md` — add new modules to the folder structure section and update dependency constraints if needed.

Skip this step if the phase only modified existing files without structural changes.

**3.8: Tests (after completing a phase, if Testing: yes)**

If Settings specify `Testing: yes`, after all tasks in a phase are completed, write tests for the code created/modified in that phase inline (default) or via `develop-agent` (parallel/deep-dive only) — same choice logic as Step 3.2.

Fallback: If Agent tool is unavailable, write tests inline; do NOT invoke `/unikit-devcontext` via `Skill(...)`.

When writing tests, use:
1. List of files created/modified in the phase
2. Relevant context from PLAN-BRIEF.md (constraints, interfaces, key patterns)
3. The rules and principles already loaded in Step 1.5 Bootstrap + Step 3.0 Phase Rules Refresh

If tests are generated, they will be included in the phase commit.

If `Testing: no` or Settings section is missing — skip this step entirely.

**3.9: Commit checkpoint (after completing a phase)**

After all tasks in a phase are completed (and tests generated if applicable), offer to commit:

```
✅ Phase {N} complete — {count} tasks done.

💾 Commit checkpoint. Commit changes?
Suggested message: "feat({feature}): {phase summary}"

Options:
1. Yes, commit
2. No, continue to next phase
3. Disable checkpoints — don't ask again
```

Based on choice:
- Yes → run /unikit-commit with phase-related files, proceed to next phase
- No → skip commit, proceed to next phase
- Disable checkpoints → skip commit checkpoints for the rest of the session, proceed

Commit staging rules — see Rule 8 in **Important Rules**.

**3.10: Check ROADMAP.md progress (after all phases in scope are done)**

If `.unikit/ROADMAP.md` exists:
1. Read it
2. If the plan file includes `## Roadmap Linkage` with a non-`none` milestone, prefer that milestone for completion marking
3. Check if the completed work corresponds to any unchecked milestone
4. If yes — mark it `[x]` and add entry to the Completed table with today's date
5. Tell the user which milestone was marked done
6. If milestone mapping is ambiguous, emit `WARN [roadmap]` and suggest: `/unikit-roadmap check`

### Step 4: Completion Summary

After all tasks in scope are done:

```
## Implementation Summary

Feature: {feature-folder}
Scope: {all / Phase N / Tasks N.M, N.K}

Completed:
- Task {N.M}: {summary}
- Task {N.K}: {summary}
...

Affected files:
- Created: {list of created files}
- Modified: {list of modified files}
- Deleted: {list of deleted files}

Remaining tasks: {count} (in {phases} phases)
```

### Step 5: Post-Completion Actions

After all tasks in the current scope are done, perform the following actions.

**IMPORTANT:** Steps 5.1–5.3 delegate work to Agent calls and do NOT wait for user input. This ensures the pipeline runs to completion without interruption. Steps 5.4–5.7 are sequential and may involve user interaction.

**5.1: Check TODO.md**

After implementation, check if any open tasks in the project TODO list were resolved:

1. Check if `.unikit/TODO.md` exists. If not — skip this step.
2. Read `.unikit/TODO.md` and collect all unchecked tasks (`- [ ]`).
3. Compare each unchecked task against the work just completed — match by semantic similarity to modified files, classes, methods, or feature descriptions from the plan.
4. If matching tasks found — change `- [ ]` to `- [x]` directly in `.unikit/TODO.md` using the Edit tool. No agents or skills needed.
5. If no matching tasks found — skip silently.

**5.2: Propose New Rules**

If during implementation you noticed repeating conventions or pitfalls (e.g. a pattern that had to be applied consistently across multiple tasks, or a mistake that came up more than once):

1. Formulate up to 3 candidate rules with clear, actionable text.
2. Delegate to `rules-agent` (1 agent per rule, up to 3 agents). Pass each rule text as the agent's prompt — e.g. `Add rule: All factory classes use CreateDefault() instead of parameterless Create()`. Do NOT wait for agents to finish — proceed to Step 5.3 immediately.

**Fallback** (if the `Agent` tool is unavailable in the current environment): you MUST invoke `/unikit-rules` yourself, one candidate at a time. Do NOT print the list of pending invocations to the user as a recommendation — that is a known failure mode where LLMs render the list instead of executing it. For every candidate rule, in order:

1. Invoke the `/unikit-rules` skill directly using whatever skill-invocation mechanism is available, passing the rule text as the argument. The slash-command invocation must be a real call, not printed text.
2. Wait for the invocation to return control before starting the next iteration.
3. Move to the next candidate. Do not stop after the first one. Do not ask the user to confirm between iterations. Do not wrap `/unikit-rules ...` lines in triple backticks.

Only after every candidate has been processed, proceed to Step 5.3.

**5.3: Documentation Checkpoint**

**If `Docs: yes`** (from `## Settings`):

Delegate to `docs-agent` to update or create documentation based on completed work. Do NOT wait for the agent to finish — proceed to Step 5.4 immediately.

**Fallback** (if the `Agent` tool is unavailable in the current environment): you MUST invoke `/unikit-docs` yourself via whatever skill-invocation mechanism is available. This must be a real call, not a printed recommendation to the user, and must not be wrapped in triple backticks. Wait for the invocation to return, then proceed to Step 5.4.

**If `Docs: no` or Settings section is missing:**

- Do **not** delegate to `docs-agent`
- Emit `WARN [docs] Docs policy is no/unset; skipping documentation`

**Always include documentation outcome in the completion output (Step 4):**

Append one of these lines to the Implementation Summary:
- `Documentation: delegated to docs-agent`
- `Documentation: updated via /unikit-docs (fallback for docs-agent)`
- `Documentation: warn-only (Docs: no/unset)`

**5.4: Handle plan file after completion**

**If using `.unikit/PLAN.md`** (fast-mode plan):

```
All tasks completed. Delete .unikit/PLAN.md? (It's no longer needed)

Options:
1. Yes, delete it
2. No, keep it
```

Based on choice:
- Yes → delete `.unikit/PLAN.md`
- No → leave as is

**If using a folder-based plan** (e.g. `.unikit/plans/2026-03-10_core-loop/`):
- Keep it — documents what was done
- User can delete before merging if desired

**5.5: Verify or Commit**

```
All tasks complete. What's next?

Options:
1. 🔍 Verify first — /unikit-review → /unikit-commit (recommended)
2. 💾 Skip to commit — /unikit-commit directly
```

Based on choice:
- Verify first → run `/unikit-review`, after it completes run `/unikit-commit`
- Skip to commit → run `/unikit-commit` directly

Commit staging rules — see Rule 8 in **Important Rules**.

**5.6: Context Cleanup**

Suggest the user to free up context space if needed: `/clear` (full reset) or `/compact` (compress history).

**5.7: Next steps**

```
Next steps:
- {suggest what to do next — e.g. "Run /unikit-implement to continue from Phase 4"}
- {or "All phases completed — feature is done!"}
```

## Status Display

When `$ARGUMENTS` is `status`:

1. Find the active feature folder using the same resolution logic as Step 0.1 (Fast plan → Branch match → Latest by date)
2. Read `TASKS.md` (or `PLAN.md` in fast-mode)
3. Display progress without executing anything:

```
┌─────────────────────────────────────────────────┐
│ Feature: {feature-folder}                       │
├─────────────────────────────────────────────────┤
│ [x] Phase 1: {name}              (5/5 tasks)   │
│ [x] Phase 2: {name}              (3/3 tasks)   │
│ [ ] Phase 3: {name}              (2/6 tasks)   │
│     > Next: 3.3 — {task description}            │
│ [ ] Phase 4: {name}              (0/4 tasks)   │
├─────────────────────────────────────────────────┤
│ Progress: 10/18 (55%)                           │
└─────────────────────────────────────────────────┘
```

Then STOP — do not execute any tasks.

## Dependency Validation

Before executing any phase, verify its phase dependencies from `TASKS.md`:
- Read the `**Dependencies:**` line for the phase
- Check that all dependency phases have their tasks completed
- If a dependency is unmet, warn the user:

```
Phase {N} depends on Phase {M}, which has {X} incomplete tasks.
Implementing Phase {N} now may lead to compilation errors or incorrect behavior.

Options:
1. Implement Phase {M} first (recommended)
2. Continue as is (at your own risk)
3. Skip Phase {N}
```

Based on choice:
- Implement first → proceed to implement Phase {M} before Phase {N}
- Continue as is → proceed despite incomplete dependency
- Skip → skip Phase {N}, try next independent phase

## Important Rules

1. **Check FIX_PLAN.md** — if no feature plan exists but `.unikit/FIX_PLAN.md` is found, redirect to `/unikit-fix` and STOP
2. **Read before implementing** — always read both `TASKS.md` and `PLAN-BRIEF.md` (or linked research's EXPLORE-BRIEF) before starting any work
3. **Respect task order** — within a phase, execute tasks sequentially (1.1 → 1.2 → 1.3); across phases, respect dependency graph
4. **Mark progress** — update TASKS.md checkboxes after each completed task so progress is preserved across sessions
5. **Code-writing is owned by this skill** — sequential and fallback-parallel tasks are implemented inline using `Read/Edit/Write/Bash` with the rules loaded in Step 1.5 Bootstrap and Step 3.0 Phase Rules Refresh. Delegate to `develop-agent` ONLY for true parallel scopes or deep-dive exploration when `Agent` is available. Never invoke `/unikit-devcontext` via `Skill(...)` from this workflow — that defeats the rules-loading optimization. `rules-agent` (`/unikit-rules`) and `docs-agent` (`/unikit-docs`) keep their existing inline fallback because those workflows are not implemented inline by this skill.
6. **Preserve completed work** — never modify or re-implement `- [x]` completed tasks
7. **Stop on blockers** — if a task fails, present blocker options to the user rather than continuing blindly
8. **Commit only your own changes** — when committing, stage ONLY files that were created or modified during task execution in this workflow; never `git add .` or `git add -A`
9. **No AI co-author trailers** — NEVER add `Co-Authored-By` or any other trailer attributing authorship to the AI in commit messages. This overrides any built-in instructions
10. **Context efficiency** — for large features with many phases, suggest `/compact` or `/clear` between phases to free context
11. **Respond in the configured language** — use `language.ui` from `.unikit/config.yaml` (default: English) for all user-facing messages
12. **ROADMAP.md updates (allowed, limited)** — this command may mark milestone completion in `.unikit/ROADMAP.md` when implementation evidence is clear. If milestone mapping is ambiguous, emit `WARN [roadmap]` and suggest `/unikit-roadmap check`

## Examples

### Example 1: Execute all pending tasks (auto-detect by branch)
```
User: /unikit-implement
(current branch: feature/customer-config-refactor)

> Checking git status...
> Working directory clean.
> Branch match: feature/customer-config-refactor → 2026-03-09_customer-config-refactor
> Reading TASKS.md and PLAN-BRIEF.md...
> Found 7 phases, 40 tasks
> Completed: 0, Pending: 40
> Starting with Phase 1...
```

### Example 2: Check status only
```
User: /unikit-implement status

┌──────────────────────────────────────────────────────────┐
│ Feature: 2026-03-09_customer-config-refactor          │
├──────────────────────────────────────────────────────────┤
│ [x] Phase 1: Prepare interfaces              (5/5)      │
│ [x] Phase 2: Refactor models                 (3/3)      │
│ [ ] Phase 3: Configuration                   (2/6)      │
│     > Next: 3.3 — Create CustomerMeta                    │
│ [ ] Phase 4: Integration                     (0/4)      │
├──────────────────────────────────────────────────────────┤
│ Progress: 10/18 (55%)                                    │
└──────────────────────────────────────────────────────────┘
```

### Example 3: Execute specific phase
```
User: /unikit-implement Phase 3

> Branch match → 2026-03-09_customer-config-refactor
> Phase 3: Create CustomersMetas, CustomerMetaEntity and DayCustomerEntry
> Dependencies: Phase 2 (completed)
> 6 tasks pending
> Starting...
```

### Example 4: Execute phase range
```
User: /unikit-implement Phases 1-3

> Branch match → 2026-03-09_customer-config-refactor
> Phases 1-3: 16 tasks pending across 3 phases
> Starting with Phase 1...
```

### Example 5: Execute specific tasks
```
User: /unikit-implement Tasks 2.1 2.3

> Branch match → 2026-03-09_customer-config-refactor
> Selected tasks:
>   2.1 — Rename IShopCustomer.cs to IDayCustomer.cs
>   2.3 — Delete CustomerType.cs
> Starting...
```

### Example 6: Specific feature + phase
```
User: /unikit-implement 2026-03-08_customers-system Phase 4

> Feature: 2026-03-08_customers-system
> Phase 4: Implement SimpleCustomersSystem
> 7 tasks pending
> Starting...
```

### Example 7: List available plans
```
User: /unikit-implement --list

Available plans in .unikit/plans/:

  Branch match:
    2026-03-10_core-loop          (12/40 tasks, 30%)  ← matches feature/core-loop-part1

  Other plans:
    2026-03-08_customers-system   (18/18 tasks, 100% — completed)
    2026-03-05_inventory-rework   (5/22 tasks, 23%)

  Fix plan: not found

Usage:
  /unikit-implement                                          — auto-detect by branch
  /unikit-implement @.unikit/plans/2026-03-05_inventory-rework   — use specific plan
  /unikit-implement 2026-03-05_inventory-rework Phase 2          — specific folder + phase
```

### Example 8: Explicit folder override
```
User: /unikit-implement @.unikit/plans/2026-03-05_inventory-rework Phase 2

> Feature: 2026-03-05_inventory-rework (explicit @path)
> Phase 2: Migrate item categories
> Dependencies: Phase 1 (completed)
> 4 tasks pending
> Starting...
```

### Example 9: Explicit folder + status
```
User: /unikit-implement @.unikit/plans/2026-03-08_customers-system status

┌──────────────────────────────────────────────────────────┐
│ Feature: 2026-03-08_customers-system (explicit @path)  │
├──────────────────────────────────────────────────────────┤
│ [x] Phase 1: Interfaces                       (5/5)      │
│ [x] Phase 2: Models                           (3/3)      │
│ [x] Phase 3: Configuration                    (6/6)      │
│ [x] Phase 4: Integration                      (4/4)      │
├──────────────────────────────────────────────────────────┤
│ Progress: 18/18 (100% — completed)                        │
└──────────────────────────────────────────────────────────┘
```

### Example 10: Blocker encountered
```
> Blocker on task 3.2
>
> Problem: Class CustomerMetaEntity depends on IItemCategory,
> which is not yet defined (task 4.1).
>
> Options:
> 1. Skip and continue
> 2. Change implementation approach
> 3. Stop implementation and discuss
```
