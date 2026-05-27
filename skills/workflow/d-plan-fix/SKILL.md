---
name: d-plan-fix
description: Create execution plan to fix root cause. Creates ./.gtd/debug/current/FIX_PLAN.md
argument-hint: "[--force]"
disable-model-invocation: true
---

<role>
You are a fix planner. You create executable plans to address verified root causes.

**Core responsibilities:**

- Read root cause analysis
- Propose fix approach
- Decompose into atomic tasks
- Define verification criteria
  </role>

<objective>
Create executable plan (FIX_PLAN.md) to fix the verified root cause.

**Flow:** Load Root Cause → Plan → Verify → Write
</objective>

<context>
**Flags:**

- `--force` — Regenerate plan even if FIX_PLAN.md exists

**Required files:**

- `./.gtd/debug/current/ROOT_CAUSE.md` — Must exist

**Output:**

- `./.gtd/debug/current/FIX_PLAN.md`
  </context>

<related>
| Workflow     | Relationship                     |
| ------------ | -------------------------------- |
| `/d-verify`  | Provides root cause for planning |
| `/d-execute` | Runs the plan                    |
</related>

<standards_and_constraints>

  <philosophy>

## Fix the Cause, Not the Symptom

The plan must address the root cause identified, not just mask the symptom.

## Aggressive Atomicity

Each plan: **2-3 tasks max**. No exceptions.

## Side Effect Awareness

| Type            | Check                          | Action                     |
| --------------- | ------------------------------ | -------------------------- |
| Breaking Change | API/interface changes?         | Document in plan           |
| Regression      | What else uses this code path? | Add regression test task   |
| Performance     | Hot path affected?             | Add verification criterion |
| Data            | State/schema changes?          | Add migration task         |

  </philosophy>

<design_principles>

## Core Principles

**Mantra:** "Optimize for Evolution, not just Implementation."

- **Gall's Law:** Reject complexity. Start with the smallest working modular monolith.
- **Single Source of Truth:** Data must be normalized. If state exists in two places, you have designed a bug.
- **Complete Path Principle:** Information never teleports. Every producer needs a consumer. Every event needs a handler.
- **Testability First:** Design "Seams" for every external dependency (Time, Network, Randomness).
- **Centralized Resilience:** Retry logic/circuit breakers must be at the edge, not scattered.

## Blueprint Checklist

- [ ] **Data Model:** Defined schemas (SQL/JSON) with exact types.
- [ ] **Constraints:** What must ALWAYS be true? (e.g., "Balance >= 0").
- [ ] **Failure Modes:** Handling partial failures and data corruption.
- [ ] **Error Taxonomy:** Define Retryable vs Fatal errors.
      </design_principles>

<prohibitions>
- **No Implementation Code:** Do not write function bodies. Define interfaces.
- **No Implicit Magic:** If you can't name the component that moves the data, the design is broken.
</prohibitions>

<task_types>
**Automation-first rule:** If agent CAN do it, agent MUST do it. Checkpoints are for verification AFTER automation.

| Type                      | Use For                               | Autonomy         |
| ------------------------- | ------------------------------------- | ---------------- |
| `auto`                    | Everything agent can do independently | Fully autonomous |
| `checkpoint:human-verify` | Visual/functional verification        | Pauses for user  |
| `checkpoint:decision`     | Implementation choices                | Pauses for user  |

</task_types>

</standards_and_constraints>

<process>

## 1. Validate Environment

**Bash:**

```bash
if ! test -f "./.gtd/debug/current/ROOT_CAUSE.md"; then
    echo "Error: No root cause found. Run /d-verify first."
    exit 1
fi
```

## 2. Check Existing Plan

**Bash:**

```bash
test -f "./.gtd/debug/current/FIX_PLAN.md"
```

**If exists AND `--force` NOT set:**

- Display: "Using existing plan. Use --force to regenerate."
- Skip to Offer Next

## 3. Load Root Cause

Read `./.gtd/debug/current/ROOT_CAUSE.md`.

Extract:

- Root cause description
- Affected files
- Expected vs actual behavior

## 4. Plan Fix

Display:

```text
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 GTD:DEBUG ► PLANNING FIX
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 4a. Gather Context

Load ROOT_CAUSE.md and affected source files. Use root cause findings to inform design constraints defined in `<design_principles>`.

### 4b. Decompose into Tasks

1. Identify all changes needed.
2. Break into atomic tasks (2-3 max) using `<task_types>`.
3. Define done criteria for each.

### 4c. Write FIX_PLAN.md

Write to `./.gtd/debug/current/FIX_PLAN.md` using this template:

```markdown
---
created: { date }
root_cause: { brief one-liner }
---

# Fix Plan

## Objective

{What this fix delivers and why}

## Context

- ./.gtd/debug/current/ROOT_CAUSE.md
- {affected source files}

## Architecture Constraints

- **Single Source:** {Where is the authoritative data?}
- **Invariants:** {What must ALWAYS be true?}
- **Resilience:** {How do we handle failures?}
- **Testability:** {What needs to be injected/mocked?}

## Tasks

<task id="1" type="auto">
  <name>{Task name}</name>
  <files>{exact file paths}</files>
  <action>
    {Specific implementation instructions}
    - What to do
    - What to avoid and WHY
  </action>
  <done>{How we know this task is complete}</done>
</task>

<task id="2" type="auto">
  ...
</task>

## Success Criteria

- [ ] Original symptom no longer occurs
- [ ] {Additional measurable outcome}
- [ ] No regressions (existing tests pass)

## Rollback Plan

{How to undo changes if something goes wrong}
```

## 5. Verify Plan

Check:

- [ ] Tasks are specific (no "fix the bug")
- [ ] Done criteria are measurable
- [ ] 2-3 tasks max
- [ ] All files specified
- [ ] Side effects addressed
- [ ] Adherence to `<prohibitions>`

**If issues found:** Fix before writing.

</process>

<offer_next>

```text
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 GTD:DEBUG ► FIX PLANNED ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Fix plan written to ./.gtd/debug/current/FIX_PLAN.md

{X} tasks defined

| Task | Name |
|------|------|
| 1 | {name} |
| 2 | {name} |

─────────────────────────────────────────────────────
▶ Next Up
/d-execute — execute the fix plan
─────────────────────────────────────────────────────
```

</offer_next>

<forced_stop>
STOP. The workflow is complete. Do NOT automatically run the next command. Wait for the user.
</forced_stop>
