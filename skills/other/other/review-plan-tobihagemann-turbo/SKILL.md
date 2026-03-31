---
name: review-plan
description: "Review an implementation plan: launches an internal plan review and `/peer-review-plan` in parallel and returns combined findings. Use when the user asks to \"review my plan\", \"review this plan\", \"check my plan\", \"critique my plan\", or wants plan feedback before implementation."
---

# Review Plan

Run two AI plan reviews in parallel and return combined findings.

## Step 1: Identify the Plan

Determine the plan to review:

- If **plan text** is in conversation context, use it
- If a **plan file path** was provided, read the file

## Step 2: Run Two Reviews in Parallel

Launch two agents in a single message so they run concurrently (`model: "opus"`, do not set `run_in_background`):

### Internal Plan Review

Spawn a subagent with the full plan text and instruct it to:

1. Read project context (CLAUDE.md and files mentioned in the plan) to understand the codebase
2. Apply the plan determination criteria below
3. Return findings in the output format below

### Run `/peer-review-plan` Skill

Spawn a subagent to run the `/peer-review-plan` skill with the plan text.

## Step 3: Return Combined Findings

Wait for both agents to complete. Aggregate their findings with attribution (reviewer: "internal" or "peer") and return them to the caller.

The caller determines what to do with the findings (evaluate, apply, or present to the user).

## Plan Determination Criteria

Flag an issue only when ALL of these hold:

1. It would cause an implementer to build the wrong thing or get stuck
2. The issue is discrete and actionable (not a vague concern or general suggestion)
3. The author would likely fix the issue if made aware of it
4. The issue is clearly not an intentional design choice

### What to Review

- **Completeness** — Missing steps, undefined behavior, unaddressed requirements or edge cases
- **Feasibility** — Technically unsound approaches, ignored constraints, missing dependencies
- **Scope** — Requirements addressed without creep. No missing requirements from the original ask
- **Ordering** — Step dependency issues, missing prerequisites, circular dependencies
- **Buildability** — Steps specific enough to execute without getting stuck. No logical gaps between steps
- **Pattern Alignment** — Proposed approach follows existing codebase patterns where applicable. Deviations from established patterns are justified

### What to Ignore

- Wording, stylistic, or cosmetic preferences that don't affect buildability
- Alternative approaches that aren't clearly better
- Suggestions that add complexity without clear implementation value

## Priority Levels

- **P0** — Plan is fundamentally flawed. Wrong approach or missing core requirement
- **P1** — Significant gap that will likely cause implementation problems
- **P2** — Moderate issue that should be addressed before implementation
- **P3** — Minor improvement

## Output Format

Return findings as a numbered list. For each finding:

```
### [P<N>] <title (imperative, ≤80 chars)>

**Section:** <plan section or step where the issue occurs>
**Reviewer:** <internal | peer>

<one paragraph explaining why this is a problem, what implementation impact it has, and a suggested fix>
```

After all findings, add:

```
## Overall Verdict

**Readiness:** <ready | needs revision>

<1-3 sentence assessment>
```

If there are no qualifying findings, state that the plan looks ready for implementation and explain briefly.

## Rules

- If any reviewer is unavailable or returns malformed output, proceed with findings from the remaining reviewer.
- Present findings grouped by priority, then by reviewer.
