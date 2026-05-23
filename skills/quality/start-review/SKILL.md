---
name: start-review
description: "Start a review session from an existing plan and implementation. Discovers available plans, validates implementation exists, and invokes the technical-review skill."
disable-model-invocation: true
allowed-tools: Bash(.claude/scripts/discovery-for-implementation-and-review.sh)
---

Invoke the **technical-review** skill for this conversation.

## Workflow Context

This is **Phase 6** of the six-phase workflow:

| Phase | Focus | You |
|-------|-------|-----|
| 1. Research | EXPLORE - ideas, feasibility, market, business | |
| 2. Discussion | WHAT and WHY - decisions, architecture, edge cases | |
| 3. Specification | REFINE - validate into standalone spec | |
| 4. Planning | HOW - phases, tasks, acceptance criteria | |
| 5. Implementation | DOING - tests first, then code | |
| **6. Review** | VALIDATING - check work against artifacts | ◀ HERE |

**Stay in your lane**: Verify that every plan task was implemented, tested adequately, and meets quality standards. Don't fix code - identify problems. You're reviewing, not building.

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
- `count` - total number of plans

**From `state` section:**
- `scenario` - one of: `"no_plans"`, `"single_plan"`, `"multiple_plans"`

**IMPORTANT**: Use ONLY this script for discovery. Do NOT run additional bash commands (ls, head, cat, etc.) to gather state - the script provides everything needed.

→ Proceed to **Step 2**.

---

## Step 2: Route Based on Scenario

Use `state.scenario` from the discovery output to determine the path:

#### If scenario is "no_plans"

No plans exist yet.

```
No plans found in docs/workflow/planning/

The review phase requires a completed implementation based on a plan. Please run /start-planning first to create a plan, then /start-implementation to build it.
```

**STOP.** Wait for user to acknowledge before ending.

#### If scenario is "single_plan" or "multiple_plans"

Plans exist.

→ Proceed to **Step 3** to present options.

---

## Step 3: Present Plans and Select

Present all discovered plans to help the user make an informed choice.

**Present the full state:**

```
Available Plans:

  1. {topic-1} ({status}) - format: {format}, spec: {exists|missing}
  2. {topic-2} ({status}) - format: {format}, spec: {exists|missing}

· · ·

Which plan would you like to review the implementation for? (Enter a number or name)
```

**If single plan exists (auto-select):**
```
Auto-selecting: {topic} (only available plan)
```
→ Proceed directly to **Step 4**.

**If multiple plans exist:**

**STOP.** Wait for user response.

→ Based on user choice, proceed to **Step 4**.

---

## Step 4: Identify Implementation Scope

Ask the user what code to review:

```
· · ·

What code should I review?

1. All changes since the plan was created
2. Specific directories or files
3. Let me identify from git status

Which approach?
```

**STOP.** Wait for user response.

If they choose specific directories/files, ask them to specify.

→ Proceed to **Step 5**.

---

## Step 5: Invoke the Skill

After completing the steps above, this skill's purpose is fulfilled.

Invoke the [technical-review](../technical-review/SKILL.md) skill for your next instructions. Do not act on the gathered information until the skill is loaded - it contains the instructions for how to proceed.

**Example handoff:**
```
Review session for: {topic}
Plan: docs/workflow/planning/{topic}.md
Format: {format}
Plan ID: {plan_id} (if applicable)
Specification: {specification} (exists: {true|false})
Scope: {all changes | specific paths | from git status}

Invoke the technical-review skill.
```
