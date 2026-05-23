---
name: start-planning
description: "Start a planning session from an existing specification. Discovers available specifications, gathers context, and invokes the technical-planning skill."
disable-model-invocation: true
allowed-tools: Bash(.claude/scripts/discovery-for-planning.sh)
---

Invoke the **technical-planning** skill for this conversation.

## Workflow Context

This is **Phase 4** of the six-phase workflow:

| Phase | Focus | You |
|-------|-------|-----|
| 1. Research | EXPLORE - ideas, feasibility, market, business | |
| 2. Discussion | WHAT and WHY - decisions, architecture, edge cases | |
| 3. Specification | REFINE - validate into standalone spec | |
| **4. Planning** | HOW - phases, tasks, acceptance criteria | ◀ HERE |
| 5. Implementation | DOING - tests first, then code | |
| 6. Review | VALIDATING - check work against artifacts | |

**Stay in your lane**: Create the plan - phases, tasks, and acceptance criteria. Don't jump to implementation or write code. The specification is your sole input; transform it into actionable work items.

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
.claude/scripts/discovery-for-planning.sh
```

This outputs structured YAML. Parse it to understand:

**From `specifications` section:**
- `exists` - whether any specifications exist
- `feature` - list of feature specs (name, status, has_plan, plan_status)
- `crosscutting` - list of cross-cutting specs (name, status)
- `counts.feature` - total feature specifications
- `counts.feature_ready` - feature specs ready for planning (concluded + no plan)
- `counts.feature_with_plan` - feature specs that already have plans
- `counts.crosscutting` - total cross-cutting specifications

**From `plans` section:**
- `exists` - whether any plans exist
- `files` - each plan's name, format, status, and plan_id (if present)
- `common_format` - the output format if all existing plans share the same one; empty string otherwise

**From `state` section:**
- `scenario` - one of: `"no_specs"`, `"nothing_actionable"`, `"has_options"`

**IMPORTANT**: Use ONLY this script for discovery. Do NOT run additional bash commands (ls, head, cat, etc.) to gather state - the script provides everything needed.

→ Proceed to **Step 2**.

---

## Step 2: Route Based on Scenario

Use `state.scenario` from the discovery output to determine the path:

#### If scenario is "no_specs"

No specifications exist yet.

```
No specifications found in docs/workflow/specification/

The planning phase requires a concluded specification. Please run /start-specification first.
```

**STOP.** Wait for user to acknowledge before ending.

#### If scenario is "nothing_actionable"

Specifications exist but none are actionable — all are still in-progress and no plans exist to continue.

→ Proceed to **Step 3** to show the state.

#### If scenario is "has_options"

At least one specification is ready for planning, or an existing plan can be continued or reviewed.

→ Proceed to **Step 3** to present options.

---

## Step 3: Present Workflow State and Options

Present everything discovered to help the user make an informed choice.

**Present the full state:**

```
Planning Phase

Available:
  1. + {topic-2} - create new plan
  2. ▶ {topic-3} - continue in-progress plan
  3. > {topic-4} - review concluded plan

Not plannable specifications:
  · {topic-1} [feature, in-progress]
  · {caching-strategy} [cross-cutting, concluded]
  · {rate-limiting} [cross-cutting, in-progress]
```

**Formatting rules:**

Available (numbered, selectable):
- **`+`** — concluded spec with no plan yet
- **`▶`** — has a plan with `plan_status: planning`
- **`>`** — has a plan with `plan_status: concluded`

Not plannable specifications (no number, not selectable — `[type, status]` format):
- **`·`** — feature specs still in-progress, or cross-cutting specifications
- Feature specs: `[feature, in-progress]`
- Cross-cutting specs: `[cross-cutting, {status}]`

Omit either section entirely if it has no entries.

**Then prompt based on what's actionable:**

**If multiple actionable items:**
```
· · ·

Select a specification (enter number):
```

**STOP.** Wait for user response.

**If single actionable item (auto-select):**
```
Auto-selecting: {topic} (only actionable specification)
```

→ Proceed directly to **Step 4**.

**If nothing actionable:**
```
No plannable specifications.

Before you can start planning:
- Complete any in-progress specifications with /start-specification, or
- Create a new specification first

Then re-run /start-planning.
```

**STOP.** This workflow cannot continue — do not proceed.

→ Based on user choice, proceed to **Step 4**.

---

## Step 4: Route by Plan State

Check whether the selected specification already has a plan (from `has_plan` in discovery output).

#### If no existing plan (fresh start)

→ Proceed to **Step 5** to gather context before invoking the skill.

#### If existing plan (continue or review)

The plan already has its context from when it was created. Skip context gathering.

→ Go directly to **Step 7** to invoke the skill.

---

## Step 5: Gather Additional Context

Ask:
- Any additional context or priorities to consider?
- Any constraints since the specification was concluded?

**STOP.** Wait for user response.

→ Proceed to **Step 6**.

---

## Step 6: Surface Cross-Cutting Context

**If no cross-cutting specifications exist**: Skip this step. → Proceed to **Step 7**.

Read each cross-cutting specification from `specifications.crosscutting` in the discovery output.

### 6a: Warn about in-progress cross-cutting specs

If any **in-progress** cross-cutting specifications exist, check whether they could be relevant to the feature being planned (by topic overlap — e.g., a caching strategy is relevant if the feature involves data retrieval or API calls).

If any are relevant:

```
Note: The following cross-cutting specifications are still in-progress:
  · {rate-limiting} - in-progress

These may contain architectural decisions relevant to this plan. You can:
- Continue planning without them
- Stop and complete them first (/start-specification)
```

**STOP.** Wait for user response.

If the user chooses to stop, end here. If they choose to continue, proceed.

### 6b: Summarize concluded cross-cutting specs

If any **concluded** cross-cutting specifications exist, identify which are relevant to the feature being planned and summarize for handoff:

```
Cross-cutting specifications to reference:
- caching-strategy.md: [brief summary of key decisions]
```

These specifications contain validated architectural decisions that should inform the plan. The planning skill will incorporate these as a "Cross-Cutting References" section in the plan.

→ Proceed to **Step 7**.

---

## Step 7: Invoke the Skill

After completing the steps above, this skill's purpose is fulfilled.

Invoke the [technical-planning](../technical-planning/SKILL.md) skill for your next instructions. Do not act on the gathered information until the skill is loaded - it contains the instructions for how to proceed.

**Example handoff (fresh plan):**
```
Planning session for: {topic}
Specification: docs/workflow/specification/{topic}.md
Additional context: {summary of user's answers from Step 5}
Cross-cutting references: {list of applicable cross-cutting specs with brief summaries, or "none"}
Recommended output format: {common_format from discovery if non-empty, otherwise "none"}

Invoke the technical-planning skill.
```

**Example handoff (continue/review existing plan):**
```
Planning session for: {topic}
Specification: docs/workflow/specification/{topic}.md
Existing plan: docs/workflow/planning/{topic}.md

Invoke the technical-planning skill.
```

## Notes

- Ask questions clearly and wait for responses before proceeding
- The feature specification is the primary source of truth for planning
- Cross-cutting specifications provide supplementary context for architectural decisions
- Do not reference discussions - only specifications
