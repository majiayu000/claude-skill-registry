---
name: unikit-improve
description: >-
  Refine and enhance an existing feature plan for the current {{engine_name}} project.
  Re-analyzes TASKS.md and PLAN-BRIEF.md, checks for gaps, missing tasks,
  wrong dependencies, architectural issues, and improves plan quality.
  Also detects updated or new researches from /unikit-explore and incorporates
  their findings into the plan. Use this skill whenever the user wants to review,
  polish, or improve a feature plan from .unikit/plans/, even if they say
  "check the plan", "review the feature", "improve the roadmap",
  "what's wrong with the plan", or "update plan from research".
argument-hint: "[--list] [@plan-folder] [feature-name or improvement prompt]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash(git *)
  - Bash(ls *)
  - Bash(find *)
  - Bash(wc *)
  - Agent
  - AskUserQuestion
  - Skill
metadata:
  author: unikit
  version: "2.1"
  category: planning
---

# {{engine_name}} Improve - Feature Plan Refinement

Refine an existing feature plan by re-analyzing it against the codebase. Finds gaps, missing tasks, wrong assumptions, architectural issues, and enhances plan quality.

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

## Core Idea

```
existing feature plan (TASKS.md + PLAN-BRIEF.md)
    + project rules (Bootstrap: RULES_INDEX → core/stack rules)
    + deeper codebase analysis via Explore tasks (with doc references)
    + user feedback (optional)
        ↓
find gaps, missing edge cases, wrong assumptions, architectural issues
        ↓
enhanced plan with better tasks, correct dependencies, more detail
```

## Code Analysis Rules

This skill is a **plan refinement orchestrator**, not a code writer. It loads project rules itself (Step 0.5 Bootstrap) and delegates codebase exploration to Explore tasks.

**For deep code analysis, use Explore tasks** (`Agent(subagent_type: Explore, model: sonnet, ...)`):
- Launch 2-3 tasks in parallel for different aspects of the codebase
- Each task MUST receive references to project doc files in its prompt — paths to `.unikit/ARCHITECTURE.md` and relevant core/stack rule files loaded in Bootstrap

**Do NOT use `/unikit-devcontext` or `develop-agent`** — these are for code-writing skills (`/unikit-implement`, `/unikit-fix`). Plan refinement needs code reading and analysis, not code writing.

**What you CAN do directly** (without Explore tasks):
- Read any `.md` documentation files (`TASKS.md`, `PLAN-BRIEF.md`, `.unikit/*.md`)
- **Lightweight structural queries** via Glob/Grep — checking if a file/folder exists, listing `.asmdef` names, counting files matching a pattern, verifying a namespace or class name is present

**What you MUST delegate to Explore tasks:**
- Reading `.cs` file contents for understanding logic or implementation details
- Finding code patterns, existing implementations, integration points
- Checking architectural consistency against actual code
- Verifying assumptions about class relationships, DI bindings, inheritance hierarchies

The distinction: use Glob/Grep when you need a **yes/no structural fact** (does this file exist? does this class name appear anywhere?). Delegate to Explore tasks when you need to **understand how code works** or **evaluate architectural correctness**.

## Workflow

### Step 0: Find the Feature

Parse `$ARGUMENTS` for special tokens first:

```
- --list    → list available plans only (read-only, then STOP)
- @<path>   → explicit plan folder override (highest priority)
- remaining text → feature name or improvement prompt
```

When both `--list` and `@<path>` are present, `--list` wins and no refinement is executed.

#### Priority 1: `@<path>` — explicit path override

If `$ARGUMENTS` contains `@<path>`:

1. Resolve the path (relative to project root; absolute paths allowed)
2. If the path is a directory containing `TASKS.md` and `PLAN-BRIEF.md` → use it
3. If missing → show "Plan folder not found: `<path>`" and **STOP**

Remaining argument text (after removing `@<path>`) is the improvement prompt.

```
/unikit-improve @.unikit/plans/2026-03-08_customers-system добавь обработку ошибок
→ folder: .unikit/plans/2026-03-08_customers-system, prompt: "добавь обработку ошибок"
```

#### Priority 2: `--list` — show available plans

If `$ARGUMENTS` contains `--list`, run read-only discovery and **STOP**:

```
1. Check if .unikit/PLAN.md exists (fast-mode plan)
2. Check if .unikit/FIX_PLAN.md exists (bugfix plan from /unikit-fix)
3. Get current branch:
   git branch --show-current
4. Scan .unikit/plans/ for all feature folders (both YYYY-MM-DD_name and legacy DDD-name formats)
5. For each, check if TASKS.md has uncompleted tasks (- [ ])
6. Mark which folder matches the current git branch (if any):
   - Extract feature name from branch (e.g. feature/customers-system → customers-system)
   - Match folder ending with _<feature-name> (new format) or *-<feature-name> (legacy)
7. Print availability summary (sorted lexicographically descending — newest first):

## Available Feature Plans

Current branch: feature/customers-system

💾 Fast plan: .unikit/PLAN.md (3 tasks remaining)
🔧 Fix plan:  .unikit/FIX_PLAN.md (2 tasks remaining)

  * 🔄 2026-03-08_customers-system        ← matches branch (4 tasks remaining)
    ✅ 2026-03-10_customers-service-pool   (completed)
    🔄 2026-03-09_customer-config-refactor (2 tasks remaining)

Use:
  /unikit-improve                                              # auto-detect (PLAN.md → branch → latest)
  /unikit-improve customers-system                             # by name
  /unikit-improve @.unikit/plans/2026-03-08_customers-system  # by path

8. STOP.
```

**Important:** In `--list` mode — do not execute refinement, do not modify files.

#### Priority 3: `$ARGUMENTS` contains a feature name

If `$ARGUMENTS` contains a feature name (e.g., `2026-03-08_customers-system`, `customers-system`, or legacy `001-customers-system`):

1. Look for `.unikit/plans/$ARGUMENTS/` directory (exact match)
2. If not found by exact match → try partial match: scan `.unikit/plans/` for folders
   whose name **ends with** `_$ARGUMENTS` (new format) or `*-$ARGUMENTS` (legacy `DDD-*` format)
3. If found → use it
4. If NOT found → tell the user:

```
Feature "$ARGUMENTS" not found in .unikit/plans/.

Available features:
- [list existing feature folders]

What would you like to do?
1. Choose one of the existing features
2. Create a new feature plan
```

→ **STOP here.** Wait for user response.

#### Priority 4: No arguments — auto-detect by fast plan, fix plan, git branch, then latest

If `$ARGUMENTS` is empty (no parameters):

1. **Collect candidates:**
   - Check if `.unikit/PLAN.md` exists (flat fast-mode plan)
   - Check if `.unikit/FIX_PLAN.md` exists (bugfix plan from `/unikit-fix`)
   - Get current git branch: `git branch --show-current`
   - If on a `feature/*` branch → extract the feature name part (e.g., `feature/customers-system` → `customers-system`)
   - Scan `.unikit/plans/` for folders whose name **ends with** `_<feature-name>` (new format)
     or matches `*-<feature-name>` (legacy `DDD-*` format)
     - Example: branch `feature/customers-system` matches folder `2026-03-08_customers-system` or `001-customers-system`
   - If no branch match → sort all folders **lexicographically descending** and note the first one as "latest folder plan"

2. **Resolve ambiguity:**
   - If **no candidates** found (no flat plans, no folder plans) → show "No plans found" message and **STOP**:
     ```
     ⚠️ No plans found in .unikit/plans/, .unikit/PLAN.md, or .unikit/FIX_PLAN.md.

     Create a plan first:
     - /unikit-plan <description>  — for a feature plan
     - /unikit-fix <bug description> — for a bugfix plan
     ```
   - If **exactly one candidate** → use it
   - If **multiple candidates** (e.g., PLAN.md + FIX_PLAN.md, or a flat plan + folder plans, or multiple flat plans + branch-matching folder) → **ask the user** which plan to improve via `AskUserQuestion`, listing all candidates

3. **Use the resolved plan.**

### Step 0.5: Bootstrap Context (MANDATORY)

Before any analysis — silently load the project knowledge base. Do NOT narrate the loading process to the user.

#### Required reads (always, every time, in parallel)

1. **`.unikit/DESCRIPTION.md`** — project description, tech stack, constraints
2. **`.unikit/ARCHITECTURE.md`** — architecture decisions, folder structure, module rules, dependency directions
3. **Read `.unikit/memory/RULES_INDEX.md`**. Load rules:
   - **RULES.md**: ALWAYS read `.unikit/RULES.md` first (highest priority)
   - **Core**: read the Core table. For EACH row where Required By = `all` or contains `{{self_name}}` — read that file from `.unikit/memory/core/` using the Read tool. Do NOT skip any matching row. Always re-read at skill start, never rely on prior conversation cache
   - **Stack**: load dynamically when the current task or context matches "Load When" column, or when a need arises during work
4. **`.unikit/skill-context/{{self_name}}/SKILL.md`** — project-specific skill overrides (if exists)
5. `.unikit/system/dev-principles.md` — engine development principles (used in Step 2.3/2.4 architectural consistency checks)

Remember loaded rule file paths — pass them to Explore tasks in Step 2.

### Step 1: Load Feature Plan

**If using `.unikit/PLAN.md`** (fast-mode plan):
- Read **`.unikit/PLAN.md`** — single file containing overview, checklist, settings, and optionally technical context inline

**If using a folder plan** (`.unikit/plans/<folder>/`):
- Read `TASKS.md` — feature overview (`## Overview`), task checklist with phases, settings, and dependencies
- Read `PLAN-BRIEF.md` — technical context: constraints, interfaces, key patterns, dependency graph, files, DI bindings (if exists in plan folder)
- If `TASKS.md` has a `## Based on` section → parse all linked research entries (folder name + `Attached` timestamp for each). Store as `linked_researches` list for Step 1.5. Also read each linked research's `RESEARCH_BRIEF.md` **alongside** `PLAN-BRIEF.md` (not instead of it) — both are needed for cross-referencing in Step 3.8.

Understand:
- Feature scope and goals
- Current phases and tasks
- Dependencies between tasks
- Which tasks are already completed (checkboxes `- [x]`)
- Architecture decisions made
- Which researches are linked and when they were attached

### Step 1.5: Research Check

Check whether research context has changed since the plan was created or if new relevant researches exist. This step is **optional enrichment** — if no research updates are found, proceed silently to Step 2.

#### Case A: Plan has linked researches (`## Based on` exists with entries)

1. For each entry in `linked_researches`:
   - Read `.unikit/RESEARCHES_INDEX.md` and find the matching entry by `Path`
   - Compare its `Updated` timestamp against the `Attached` timestamp from the plan
   - If `Updated > Attached` → the research was revised after being linked to the plan. Mark it as `research_updated = true`

2. If any `research_updated = true`:
   - Re-read the updated research's `RESEARCH_BRIEF.md`
   - Compare new constraints, interfaces, and decisions against current `PLAN-BRIEF.md` and `TASKS.md`
   - Collect differences as `research_improvements` (these will appear in the report under a dedicated section)

3. After processing linked researches → check for **new** researches:
   - Read `.unikit/RESEARCHES_INDEX.md`
   - Find the latest `Attached` timestamp among all `linked_researches` entries
   - Filter index for researches with `Date` **newer** than this latest `Attached` timestamp
   - Take up to 5 entries, check relevance against the plan's feature scope (compare Summary against plan Overview)
   - If relevant entries found → ask user:
     ```
     AskUserQuestion: Found new researches since the plan was created:

     1. <Title> (<Date>) — <Summary>
     2. <Title> (<Date>) — <Summary>

     Use them to improve the plan?

     Options:
     1. Yes — use all
     2. Let me pick (specify numbers)
     3. Skip — improve without new researches
     ```
   - If user selects researches → read their `RESEARCH_BRIEF.md`, add findings to `research_improvements`, and prepare to attach them to `## Based on` in Step 5

4. If no updates and no new relevant researches → proceed to Step 2 silently.

#### Case B: Plan has NO linked researches (no `## Based on` or empty)

1. **Check current session** — look in the conversation history for results of `/unikit-explore`. If found and relevant to the plan → use as research context, add to `research_improvements`.

2. **Check index** — if no session context:
   - Read `.unikit/RESEARCHES_INDEX.md`
   - Take the **last 5 entries** (index is sorted newest-first)
   - Check relevance against the plan's feature scope
   - If relevant entries found → ask user (same question format as Case A step 3)
   - If user selects → read their `RESEARCH_BRIEF.md`, add to `research_improvements`, prepare to attach in Step 5

3. If nothing found or user skips → proceed to Step 2 silently.

#### After Step 1.5

Regardless of the outcome, **always continue to Step 2** (Deep Codebase Analysis). Research improvements are collected separately and will be merged into the final report in Step 4, appearing in a dedicated section before the standard codebase analysis findings.

### Step 2: Deep Codebase Analysis

Follow the delegation rules from **Code Analysis Rules** section above.

Formulate analysis questions based on the feature plan, then launch Explore tasks in parallel. Each task MUST receive references to project doc files in its prompt.

**Doc references to include in every Explore task prompt:**
- `.unikit/ARCHITECTURE.md` — always (module boundaries, dependency rules)
- Core rule files loaded in Bootstrap — pass the **paths from RULES_INDEX.md** relevant to the task's focus
- Stack rule files loaded in Bootstrap — pass if the task's focus involves that framework

**Example: launching parallel tasks for a customer system feature:**

```
Task 1 — Existing code & bindings:
Agent(subagent_type: Explore, model: sonnet, prompt:
  "Before analysis, read these project docs:
   - .unikit/ARCHITECTURE.md
   - [core rule paths from RULES_INDEX.md Core table]

   Find all existing customer-related classes, interfaces,
   and installers. Show their relationships and Zenject bindings.
   Check for ICustomer, SimpleCustomer, CustomerInstaller, etc.
   Thoroughness: medium.")

Task 2 — Integration points:
Agent(subagent_type: Explore, model: sonnet, prompt:
  "Before analysis, read these project docs:
   - .unikit/ARCHITECTURE.md
   - [core rule paths from RULES_INDEX.md Core table]

   Find all SignalBus events (ISignal structs) related to
   gameplay flow. Check how Bootstrap loading operations work
   and what integration points exist for new systems.
   Thoroughness: medium.")

Task 3 — Save & controller patterns:
Agent(subagent_type: Explore, model: sonnet, prompt:
  "Before analysis, read these project docs:
   - .unikit/ARCHITECTURE.md
   - [core rule paths from RULES_INDEX.md Core table]

   Check existing SaveSerializer implementations.
   Find the pattern for adding new save data to the system.
   Look at existing GRASP controllers for reference patterns.
   Thoroughness: medium.")
```

**Fallback:** If Agent tool is unavailable, investigate directly using Glob/Grep for structural checks and Read for code understanding.

After tasks return, **synthesize** their findings with the project rules loaded in Bootstrap.

**What to analyze (delegate these questions):**

**2.1: Trace existing code paths**
- Existing patterns the plan should follow
- Code that already partially implements what a task describes
- Hidden dependencies the plan missed
- Shared utilities or services the plan should reuse

**2.2: Check integration points**
- Zenject installer registrations needed
- SignalBus events that need declaring
- Addressable asset references
- SaveSystem serializers needed
- Bootstrap loading operations
- Module boundary violations (Modules → Game is FORBIDDEN)

**2.3: Check architectural consistency**
- Non-MonoBehaviour first principle adherence
- Model-View separation, GRASP controller patterns
- R3 reactive subscription cleanup (`.AddTo()`)
- UniTask with CancellationToken on every async method
- Proper DI registration patterns (`.NonLazy()` for controllers/presenters)

**2.4: Check edge cases**
- Missing `CancellationToken` propagation
- Missing R3 subscription disposal
- Missing Odin `[Required]` attributes
- ZLinq usage instead of System.Linq in hot paths

### Step 3: Identify Improvements

Compare the plan against what you found. Categorize issues:

**3.1: Missing tasks**
- Tasks that should exist but don't (e.g., installer registration, save serializer, signal declarations)
- Tasks for edge cases not covered
- Missing test tasks for new systems

**3.2: Task quality issues**
- Descriptions too vague (no file paths, no specific implementation details)
- Missing specific class names or namespaces
- Incorrect assumptions about existing code
- Missing reference to existing patterns that should be followed

**3.3: Dependency issues**
- Wrong task/phase order
- Missing dependencies between phases
- Tasks that could run in parallel but are sequential

**3.4: Redundant or duplicate tasks**
- Two tasks doing the same thing
- Task unnecessary because code already exists
- Task that duplicates existing module functionality

**3.5: Scope issues**
- Tasks too large (should be split into smaller steps)
- Tasks too small (should be merged)
- Tasks outside feature scope (gold-plating)

**3.6: Architectural issues**
- Module boundary violations in the plan
- Wrong namespace assignments
- Missing SOLID/GRASP principle adherence
- Plan suggests patterns that contradict project conventions

**3.7: User-prompted improvements (if specific feedback in `$ARGUMENTS`)**

If the user provided improvement instructions beyond just a feature name:
- Apply the user's feedback to the plan
- Look for tasks that need modification
- Add new tasks if required

**3.8: Research consistency (only when `research_improvements` is non-empty)**

If Step 1.5 produced `research_improvements` (from updated or newly linked researches):
- Compare research `RESEARCH_BRIEF.md` constraints against `PLAN-BRIEF.md` constraints — find mismatches
- Find interfaces defined in research but missing from plan tasks
- Find decisions in research that contradict plan tasks
- Flag research open questions that the plan resolved without justification
- Each finding goes into `research_improvements` list with source attribution (which research it came from)

### Step 4: Present Improvements

Show the user what you found. When `research_improvements` is non-empty, the report has two sections: research-based findings first, then codebase analysis findings. When empty, only the standard section appears.

```
## Plan Improvement Report

Feature: [feature folder name]
Files: TASKS.md, PLAN-BRIEF.md
Phases analyzed: N
Tasks analyzed: N
Researches checked: N (list names if any)

### Research-Based Findings (only if research_improvements is non-empty)

Source: [research folder name(s)]

#### Updated Constraints (N)
1. **[Constraint from research]**
   Change: [what changed in the research vs what the plan has]
   Action: [update PLAN-BRIEF.md constraint / update task description]

#### New/Changed Interfaces (N)
1. **[Interface name]**
   Change: [new method / changed signature / removed]
   Action: [add task / update existing task]

#### Research-Plan Contradictions (N)
1. **[Issue]**
   Research says: [X]
   Plan says: [Y]
   Recommendation: [which to follow and why]

#### New Researches to Attach (N) (only if new researches were selected in Step 1.5)
1. **[Research title]** (<date>)
   Relevant findings: [brief summary of what this research adds]

### Codebase Analysis Findings

#### ⚠️ Missing Tasks (N)
1. **[Task description]**
   Reason: [why this task is necessary]
   After: [dependency on phase/task]

#### 🔍 Task Improvements (N)
1. **Phase X, Task Y: [name]**
   Issue: [what's wrong]
   Fix: [what needs to change]

#### 🔄 Dependency Fixes (N)
1. Phase X should depend on Phase Y
   Reason: [why]

#### 🏗️ Architectural Notes (N)
1. **[Issue description]**
   Recommendation: [how to fix]

#### 🗑️ Removals (N)
1. **Task: [name]**
   Reason: [why it's redundant]

### Summary
- Research-based changes: N
- Missing tasks: N
- Tasks to improve: N
- Dependencies to fix: N
- Architectural notes: N
- Tasks to remove: N

Apply improvements?
1. Yes, apply all
2. Choose which to apply
3. No, keep the plan as is
```

Based on choice:
- **Apply all** → apply all improvements to TASKS.md and PLAN-BRIEF.md, proceed to Step 5
- **Choose which** → use `AskUserQuestion` with `multiSelect: true` to let the user pick items. Group options by category (Missing Tasks, Task Improvements, Dependency Fixes, Architectural Notes, Removals). Each option label = `"#N: short description"`. After the user selects → proceed to Step 5, applying **only the selected items**. Unselected items are skipped without comment.
- **No** → keep plan as is → **STOP**

**If no improvements found:**

```
## Plan Review Complete

✅ The plan looks good! No significant issues found.

Feature: [feature folder name]
Phases: N, Tasks: N

Ready to proceed with implementation.
```

### Step 5: Apply Approved Improvements

Based on user's choice, apply changes sequentially. Use `Edit` for surgical changes; `Write` only if changes are too extensive for Edit.

**5.1: Add missing tasks to TASKS.md**

For each new task from the report:
1. Determine the correct phase (create a new phase if needed)
2. Insert the task with `- [ ]` checkbox at the correct position within its phase
3. Include file paths, class names, and a brief WHY context in the description
4. If the task has dependencies, note them inline (e.g., `(after Phase 1)`)

**5.2: Improve existing task descriptions in TASKS.md**

For each task flagged for improvement:
1. Locate the exact task line in TASKS.md
2. Replace the vague description with the improved one from the report
3. Add specific file paths, class names, namespace references
4. Do NOT change `- [x]` to `- [ ]` — preserve completion status

**5.3: Fix dependency ordering in TASKS.md**

1. Move tasks/phases to correct positions if ordering was wrong
2. Update inline dependency references if task numbers shifted
3. Verify that no task references a dependency that comes after it

**5.4: Remove redundant tasks from TASKS.md**

1. Delete the task line (and its sub-items if any)
2. Check if the parent phase is now empty — remove the phase header too if so
3. Update any other tasks that referenced the removed task

**5.5: Update research references in TASKS.md (`## Based on`)**

Only when `research_improvements` is non-empty (Step 1.5 found updates):

1. **Updated linked researches** — for each research where `Updated > Attached`: update the `Attached` timestamp to the current time (`YYYY-MM-DD HH:MM`). This marks that the plan now reflects the latest research state.

2. **Newly attached researches** — for each new research the user selected in Step 1.5: add a new entry to `## Based on` using the Research Reference Format from `/unikit-plan` (folder name, `Attached` timestamp, file links). If `## Based on` section doesn't exist yet, create it after `## Overview`.

**5.6: Update PLAN-BRIEF.md (if exists)**

Only if PLAN-BRIEF.md exists in the plan folder:
1. **INTERFACES** — add new interfaces that appeared in new tasks or from research; remove interfaces for deleted tasks
2. **CONSTRAINTS** — update if architectural assumptions changed during analysis or from updated research constraints
3. **FILES** — add new file paths from new tasks; remove paths for deleted tasks
4. **DI BINDINGS** — update if new bindings are needed for new tasks

If PLAN-BRIEF.md doesn't exist, do NOT create it unless changes add 3+ new interfaces or significantly alter the plan's technical scope.

**5.7: Update Overview section**

If the total number of tasks or phases changed significantly (added a phase, removed multiple tasks):
1. Update `## Overview` task/phase counts
2. Update scope description if new tasks expanded or narrowed the feature

**5.8: Confirm completion**

```
## Plan Improved

Research updates: (only if research_improvements was non-empty)
- Researches re-synced: N (list names, updated Attached timestamps)
- New researches attached: N (list names)
- Constraints/interfaces updated from research: N

💾 Changes applied to TASKS.md:
- Tasks added: N (list brief names)
- Descriptions improved: N
- Dependencies reordered: N
- Tasks removed: N

💾 Changes applied to PLAN-BRIEF.md: (if updated)
- Interfaces added/removed: N
- Constraints updated: N
- Files updated: N

Updated files:
- .unikit/plans/[feature]/TASKS.md
- .unikit/plans/[feature]/PLAN-BRIEF.md (if updated)
```

### Step 6: Next Steps

```
Plan improved. What's next?

Options:
1. 🚀 Implement now — start /unikit-implement
2. 🔄 Review plan again — re-run /unikit-improve
3. ✅ Done for now
```

Based on choice:
- **Implement now** → invoke `/unikit-implement @<resolved-plan-path>`, passing the same plan path used in this session (e.g., `@.unikit/plans/2026-03-08_customers-system` or `@.unikit/PLAN.md`)
- **Review again** → invoke `/unikit-improve @<resolved-plan-path>` to reload the skill from scratch with full re-analysis
- **Done for now** → suggest `/clear` or `/compact` → **STOP**

### Context Cleanup

Suggest the user to free up context space if needed: `/clear` (full reset) or `/compact` (compress history).

## Important Rules

1. **Don't rewrite from scratch** — improve the existing plan, don't replace it
2. **Preserve completed work** — never modify or remove `- [x]` completed tasks
3. **Traceable improvements** — every change must be justified by codebase analysis
4. **No gold-plating** — don't add tasks outside the feature scope unless critical
5. **User approves first** — never apply changes without user confirmation
6. **Keep files in sync** — if PLAN-BRIEF.md exists, its INTERFACES and FILES sections must match the tasks in TASKS.md after improvements
7. **Agent-based delegation** — follow the rules in the **Code Analysis Rules** section; single source of truth for what to delegate vs. do inline
8. **Respond in the configured language** — use `language.ui` from `.unikit/config.yaml` (default: English)

## Examples

### Example 1: Auto-detect by git branch

```
User: /unikit-improve
(current branch: feature/customers-system)

→ Branch: feature/customers-system → looking for *_customers-system
→ Found: .unikit/plans/2026-03-08_customers-system/
→ Reading TASKS.md and PLAN-BRIEF.md...
→ Bootstrap: loading rules from RULES_INDEX...
→ Deep codebase analysis via Explore tasks...
→ Report with findings → User approves → Changes applied
```

### Example 2: Auto-detect fallback to latest

```
User: /unikit-improve
(current branch: main — no matching feature)

→ No branch match for "main"
→ Latest feature by date: 2026-03-10_customers-service-pool
→ Reading feature files...
→ Analysis...
```

### Example 3: Specific feature by name

```
User: /unikit-improve 2026-03-08_customers-system

→ Found: .unikit/plans/2026-03-08_customers-system/
→ Reading feature files...
→ Analysis...
→ Report...
```

### Example 4: Partial name match

```
User: /unikit-improve customers-system

→ No exact match for "customers-system"
→ Partial match: .unikit/plans/2026-03-08_customers-system/
→ Using it...
```

### Example 5: Explicit path override

```
User: /unikit-improve @.unikit/plans/2026-03-08_customers-system добавь обработку ошибок

→ Explicit path: .unikit/plans/2026-03-08_customers-system/
→ Improvement prompt: "добавь обработку ошибок"
→ Reading feature files...
→ Analysis focused on error handling...
```

### Example 6: List mode

```
User: /unikit-improve --list

## Available Feature Plans

Current branch: feature/customers-system

  Fix plan:  .unikit/FIX_PLAN.md (2 tasks remaining)

  * 2026-03-08_customers-system        ← matches branch (3 tasks remaining)
    2026-03-09_customer-config-refactor (completed)
    2026-03-10_customers-service-pool   (5 tasks remaining)

Use:
  /unikit-improve                                              # auto-detect
  /unikit-improve customers-system                             # by name
  /unikit-improve @.unikit/plans/2026-03-08_customers-system  # by path
```

### Example 7: Fix plan auto-detected

```
User: /unikit-improve
(no .unikit/PLAN.md, .unikit/FIX_PLAN.md exists)

→ Found fix plan: .unikit/FIX_PLAN.md
→ Reading plan...
→ Bootstrap: loading rules from RULES_INDEX...
→ Deep codebase analysis via Explore tasks...
→ Report with findings → User approves → Changes applied
```

### Example 8: Feature not found

```
User: /unikit-improve nonexistent-feature

→ Feature "nonexistent-feature" not found in .unikit/plans/.

Available features:
- 2026-03-08_customers-system
- 2026-03-09_customer-config-refactor
- 2026-03-10_customers-service-pool

What would you like to do?
```
