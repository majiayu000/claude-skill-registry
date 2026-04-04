---
name: plan-style
description: "Planning conventions for pattern surveys, decision escalation, task tracking, skill loading, and finalization. Use when writing implementation plans, or when the user asks to \"load plan style\", \"plan conventions\", or \"how should I structure a plan\"."
---

# Plan Style

Use `EnterPlanMode` to enter plan mode if not already in it. When writing an implementation plan:

1. **Survey patterns** — Search the codebase for analogous features
2. **Escalate decisions** — Surface product/design decisions via `AskUserQuestion` before drafting
3. **Draft the plan** with these elements:
   - **Task tracking** — A section at the top so the implementation session can track progress via `TaskCreate`
   - **Existing patterns** — A note listing analogous features found in the codebase and whether the approach follows or deviates from them
   - **Skills line** — An instruction to load relevant skills before making edits
   - **Finalize step** — A final step instructing to run the `/finalize` skill after implementation
4. **Review the plan** — Run the review pipeline before presenting to the user

## Task Tracking

At the start, use `TaskCreate` to create a task for each step:

1. Survey patterns
2. Escalate decisions
3. Draft the plan
4. Run `/review-plan` skill
5. Run `/evaluate-findings` skill
6. Run `/apply-findings` skill
7. Present revised plan

## Pattern Survey

Before drafting the plan, spawn a subagent (`model: "opus"`, do not set `run_in_background`) to search the codebase for analogous features. Provide:

1. A summary of what the plan will add or change
2. Instructions to find all existing instances of similar behavior (e.g., if adding a new validation, find all existing validations; if adding a new endpoint, find all existing endpoints)

The subagent should return:

- **Patterns found** — List of analogous features with file paths and a brief description of how each works
- **Proposed alignment** — Whether the new work should follow or deviate from these patterns, and why
- **No patterns** — If no analogous features exist, state that explicitly

Include the subagent's findings as an "Existing patterns" note in the plan.

## Decision Escalation

Before drafting plan steps, identify product or design decisions that the user's request does not resolve. Escalate these via `AskUserQuestion` before embedding them in the plan.

**Escalate when:**

- A plan step requires choosing between user-facing behaviors and the request doesn't specify a preference (e.g., opt-in vs opt-out, strict vs lenient, sync vs async)
- The plan assumes product requirements that weren't stated
- Design trade-offs affect UX or product direction rather than technical implementation
- Multiple valid approaches exist and the choice is a matter of product preference, not technical merit

**Do not escalate** technical decisions the agent can make autonomously: which data structure, which existing pattern to follow, internal implementation approach. The boundary is product intent.

Present each decision as a concise trade-off with options via `AskUserQuestion`. Draft plan steps that depend on these decisions only after the user responds.

## Plan Task Tracking

Add a "Task Tracking" section near the top of the plan (after the title, before the first step).

If the plan has few steps or each step is small (e.g., one edit per file), use a single implementation task:

```markdown
## Task Tracking

At the start, use `TaskCreate` to create a task for each item:

1. Implement the plan
2. Run `/finalize` skill
```

If the plan has substantial, distinct steps, create a task per step:

```markdown
## Task Tracking

At the start, use `TaskCreate` to create a task for each step:

1. [Step 1 label]
2. [Step 2 label]
3. ...
N. Run `/finalize` skill
```

Always include "Run `/finalize` skill" as the last task.

## Skills Line

Identify currently available skills from the skill list in the system prompt. Determine which skills are relevant for this plan's work by comparing the work type against each skill's trigger description.

Add an instruction to the plan: "After plan approval and before making edits, run `/skill-a`, `/skill-b`."

## Finalize Step

Add a final step to the plan:

```markdown
## Step N: Run `/finalize` Skill

Run the `/finalize` skill to run tests, simplify code, review, and commit.
```

## Plan Review

After drafting the plan and before presenting it to the user:

1. Run the `/review-plan` skill with the full plan text
2. Run the `/evaluate-findings` skill on the combined review findings
3. Run the `/apply-findings` skill on the evaluated findings to incorporate accepted changes into the plan
4. Present the revised plan to the user for approval
