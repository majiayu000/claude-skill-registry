---
name: start-implementation
description: "Start an implementation session from an existing plan. Discovers available plans, checks environment setup, and invokes the technical-implementation skill."
disable-model-invocation: true
allowed-tools: Bash(.claude/scripts/discovery-for-implementation-and-review.sh)
---

Invoke the **technical-implementation** skill for this conversation.

## Workflow Context

This is **Phase 5** of the six-phase workflow:

| Phase | Focus | You |
|-------|-------|-----|
| 1. Research | EXPLORE - ideas, feasibility, market, business | |
| 2. Discussion | WHAT and WHY - decisions, architecture, edge cases | |
| 3. Specification | REFINE - validate into standalone spec | |
| 4. Planning | HOW - phases, tasks, acceptance criteria | |
| **5. Implementation** | DOING - tests first, then code | ◀ HERE |
| 6. Review | VALIDATING - check work against artifacts | |

**Stay in your lane**: Execute the plan via strict TDD - tests first, then code. Don't re-debate decisions from the specification or expand scope beyond the plan. The plan is your authority.

---

## Instructions

Follow these steps EXACTLY as written. Do not skip steps or combine them. Present output using the EXACT format shown in examples - do not simplify or alter the formatting.

**CRITICAL**: This guidance is mandatory.

- After each user interaction, STOP and wait for their response before proceeding
- Never assume or anticipate user choices
- Even if the user's initial prompt seems to answer a question, still confirm with them at the appropriate step
- Complete each step fully before moving to the next
- Do not act on gathered information until the skill is loaded - it contains the instructions for how to proceed

---

## Step 0: Run Migrations

**This step is mandatory. You must complete it before proceeding.**

Invoke the `/migrate` skill and assess its output.

**If files were updated**: STOP and wait for the user to review the changes (e.g., via `git diff`) and confirm before proceeding to Step 1. Do not continue automatically.

**If no updates needed**: Proceed to Step 1.

---

## Step 1: Run Discovery Script

Run the discovery script to gather current state:

```bash
.claude/scripts/discovery-for-implementation-and-review.sh
```

This outputs structured YAML. Parse it to understand:

**From `plans` section:**
- `exists` - whether any plans exist
- `files` - list of plans with: name, topic, status, date, format, specification, specification_exists, plan_id (if present)
- Per plan `external_deps` - array of dependencies with topic, state, task_id
- Per plan `has_unresolved_deps` - whether plan has unresolved dependencies
- Per plan `unresolved_dep_count` - count of unresolved dependencies
- `count` - total number of plans

**From `implementation` section:**
- `exists` - whether any implementation tracking files exist
- `files` - list of tracking files with: topic, status, current_phase, completed_phases, completed_tasks

**From `dependency_resolution` section:**
- Per plan `deps_satisfied` - whether all resolved deps have their tasks completed
- Per plan `deps_blocking` - list of deps not yet satisfied with reason

**From `environment` section:**
- `setup_file_exists` - whether environment-setup.md exists
- `requires_setup` - true, false, or unknown

**From `state` section:**
- `scenario` - one of: `"no_plans"`, `"single_plan"`, `"multiple_plans"`
- `plans_concluded_count` - plans with status concluded
- `plans_with_unresolved_deps` - plans with unresolved external deps
- `plans_ready_count` - concluded plans with all deps satisfied
- `plans_in_progress_count` - implementations in progress
- `plans_completed_count` - implementations completed

**IMPORTANT**: Use ONLY this script for discovery. Do NOT run additional bash commands (ls, head, cat, etc.) to gather state - the script provides everything needed.

→ Proceed to **Step 2**.

---

## Step 2: Route Based on Scenario

Use `state.scenario` from the discovery output to determine the path:

#### If scenario is "no_plans"

No plans exist yet.

```
No plans found in docs/workflow/planning/

The implementation phase requires a plan. Please run /start-planning first to create a plan from a specification.
```

**STOP.** Wait for user to acknowledge before ending.

#### If scenario is "single_plan" or "multiple_plans"

Plans exist.

→ Proceed to **Step 3** to present options.

---

## Step 3: Present Plans and Select

Present all discovered plans using the icon system below. Classify each plan into one of three sections based on its state.

**Classification logic:**

A plan is **Implementable** if:
- It has `status: concluded` AND all deps are satisfied (`deps_satisfied: true` or no deps) AND no tracking file or tracking `status: not-started`, OR
- It has an implementation tracking file with `status: in-progress`

A plan is **Implemented** if:
- It has an implementation tracking file with `status: completed`

A plan is **Not implementable** if:
- It has `status: concluded` but deps are NOT satisfied (blocking deps exist)
- It has `status: planning` or other non-concluded status
- It has unresolved deps (`has_unresolved_deps: true`)

**Present the full state:**

```
Implementation Phase

Implementable:
  1. ▶ billing - continue [Phase 2, Task 3]
  2. + core-features - start

Implemented:
  3. > user-auth

Not implementable:
  · advanced-features [blocked: core-features task core-2-3 not completed]
  · reporting [planning]
```

**Formatting rules:**

Implementable (numbered, selectable):
- **`▶`** — implementation `status: in-progress`, show current position `[Phase N, Task M]`
- **`+`** — concluded plan, deps met, no tracking file or tracking `status: not-started`

Implemented (numbered, selectable):
- **`>`** — implementation `status: completed`

Not implementable (not numbered, not selectable):
- **`·`** — blocked or plan not concluded
- `[blocked: {topic} task {id} not completed]` — resolved dep, task not done
- `[blocked: unresolved dep on {topic}]` — no task linked
- `[planning]` — plan status is not `concluded`

**Ordering:**
1. Implementable first: `▶` in-progress, then `+` new (foundational before dependent)
2. Implemented next: `>` completed
3. Not implementable last

Numbering is sequential across Implementable and Implemented. Omit any section entirely if it has no entries.

**If Not implementable section is shown**, append after the presentation:

```
If a blocked dependency has been resolved outside this workflow, name the plan and the dependency to unblock it.
```

**Then prompt based on what's actionable:**

**If single implementable plan and no implemented plans (auto-select):**
```
Auto-selecting: {topic} (only implementable plan)
```
→ Proceed directly to **Step 4**.

**If nothing selectable (no implementable or implemented):**
Show Not implementable section only (with unblock hint above).

```
No implementable plans.

Before you can start implementation:
- Complete blocking dependencies first, or
- Finish plans still in progress with /start-planning

Then re-run /start-implementation.
```

**STOP.** This workflow cannot continue — do not proceed.

**Otherwise (multiple selectable plans, or implemented plans exist):**
```
· · ·

Select a plan (enter number):
```

**STOP.** Wait for user response.

#### If the user requests an unblock

1. Identify the plan and the specific dependency
2. Confirm with the user which dependency to mark as satisfied
3. Update the plan's `external_dependencies` frontmatter: set `state` to `satisfied_externally`
4. Commit the change
5. Re-run classification and re-present Step 3

→ Based on user choice, proceed to **Step 4**.

---

## Step 4: Check External Dependencies

**This step is a confirmation gate.** Dependencies have been pre-analyzed by the discovery script.

After the plan is selected:

1. **Check the plan's `external_deps` and `dependency_resolution`** from the discovery output

#### If all deps satisfied (or no deps)

```
External dependencies satisfied.
```

→ Proceed to **Step 5**.

#### If any deps are blocking

This should not normally happen for plans classified as "Implementable" in Step 3. However, as an escape hatch:

```
Missing dependencies:

UNRESOLVED (not yet planned):
- {topic}: {description}
  -> No plan exists for this topic. Create with /start-planning or mark as satisfied externally.

INCOMPLETE (planned but not implemented):
- {topic}: task {task_id} not yet completed
  -> This task must be completed first.

· · ·

OPTIONS:
1. Implement the blocking dependencies first
2. Mark a dependency as "satisfied externally" if it was implemented outside this workflow
3. Run /link-dependencies to wire up any recently completed plans
```

**STOP.** Wait for user response.

#### Escape Hatch

If the user says a dependency has been implemented outside the workflow:

1. Ask which dependency to mark as satisfied
2. Update the plan frontmatter: Change the dependency's `state` to `satisfied_externally`
3. Commit the change
4. Re-check dependencies

→ Proceed to **Step 5**.

---

## Step 5: Check Environment Setup

> **IMPORTANT**: This step is for **information gathering only**. Do NOT execute any setup commands at this stage. The skill contains instructions for handling environment setup.

Use the `environment` section from the discovery output:

**If `setup_file_exists: true` and `requires_setup: false`:**
```
Environment: No special setup required.
```
→ Proceed to **Step 6**.

**If `setup_file_exists: true` and `requires_setup: true`:**
```
Environment setup file found: docs/workflow/environment-setup.md
```
→ Proceed to **Step 6**.

**If `setup_file_exists: false` or `requires_setup: unknown`:**

Ask:
```
Are there any environment setup instructions I should follow before implementation?
(Or "none" if no special setup is needed)
```

**STOP.** Wait for user response.

- If the user provides instructions, save them to `docs/workflow/environment-setup.md`, commit and push
- If the user says no/none, create `docs/workflow/environment-setup.md` with "No special setup required." and commit

→ Proceed to **Step 6**.

---

## Step 6: Invoke the Skill

After completing the steps above, this skill's purpose is fulfilled.

Invoke the [technical-implementation](../technical-implementation/SKILL.md) skill for your next instructions. Do not act on the gathered information until the skill is loaded - it contains the instructions for how to proceed.

**Example handoff:**
```
Implementation session for: {topic}
Plan: docs/workflow/planning/{topic}.md
Format: {format}
Plan ID: {plan_id} (if applicable)
Specification: {specification} (exists: {true|false})
Implementation tracking: {exists | new} (status: {in-progress | not-started | completed})

Dependencies: {All satisfied | List any notes}
Environment: {Setup required | No special setup required}

Invoke the technical-implementation skill.
```
