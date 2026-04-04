---
name: review-spec
description: "Review a specification document: launches an internal spec review and `/peer-review` in parallel and returns combined findings. Use when the user asks to \"review my spec\", \"review this spec\", \"check my spec\", \"critique my spec\", or wants spec feedback before planning."
---

# Review Spec

Run two AI spec reviews in parallel and return combined findings.

## Step 1: Identify the Spec

Determine the spec to review:

- If **spec text** is in conversation context, use it
- If a **spec file path** was provided, read the file
- If **neither** was provided, check for a spec at `.turbo/spec.md`

## Step 2: Run Two Reviews in Parallel

Launch two Agent tool calls in a single message so they run concurrently (`model: "opus"`, do not set `run_in_background`):

### Internal Spec Review

Spawn a subagent with the full spec text and instruct it to:

1. Read project context (CLAUDE.md and any existing codebase) to understand constraints
2. Apply the spec determination criteria below
3. Return findings in the output format below

### Run `/peer-review` Skill

Spawn a subagent whose prompt includes the full spec text and the following review prompt, and instructs it to invoke `/peer-review` via the Skill tool:

```
<task>
Review the following specification document for issues that would cause problems during implementation planning. Challenge the design direction: question whether the proposed system design is the simplest safe option and identify assumptions about users, environment, or dependencies that could break.
</task>

<dig_deeper_nudge>
After surface-level issues, check for failure scenarios the spec does not account for: partial failure, race conditions, rollback safety, stale state, and data loss.
</dig_deeper_nudge>

<structured_output_contract>
For each issue, state: (1) the problem, (2) where in the spec it occurs, (3) impact on planning or implementation, (4) a suggested fix, and (5) priority: P0 (fundamentally flawed), P1 (significant gap), P2 (moderate issue), P3 (minor improvement).
Ignore stylistic preferences and minor wording. If no issues are found, state that the spec looks sound.
</structured_output_contract>
```

## Step 3: Return Combined Findings

Wait for both agents to complete. Aggregate their findings with attribution (reviewer: "internal" or "peer") and return them to the caller.

The caller determines what to do with the findings (evaluate, apply, or present to the user).

## Spec Determination Criteria

Flag an issue only when ALL of these hold:

1. It would cause problems during implementation planning or lead to building the wrong thing
2. The issue is discrete and actionable (not a vague concern or general suggestion)
3. The author would likely fix the issue if made aware of it
4. The issue is clearly not an intentional design choice, OR it challenges a design choice with evidence of concrete failure modes or a simpler alternative

### What to Review

- **Completeness** — Missing requirements, undefined behavior, TODOs, placeholder text, or "TBD" markers that would block planning
- **Consistency** — Internal contradictions between sections (e.g., data model conflicts with API design, feature list conflicts with MVP scope)
- **Clarity** — Ambiguous requirements that could lead to misinterpretation during implementation
- **Scope** — Spec focuses on a coherent system. No unconnected components or features that serve no specified consumer
- **YAGNI** — Unrequested features, over-engineering, or premature abstractions that add complexity without clear value
- **Design Direction** — Whether the proposed system design is the simplest safe option. Challenge assumptions about users, environment, or dependencies and flag when a different approach would be safer or simpler
- **Failure Modes** — Scenarios the spec does not account for: partial failure, race conditions, stale state, rollback, data loss, and degraded dependencies

### What to Ignore

- Wording, stylistic, or cosmetic preferences that don't affect clarity
- Alternative architectural approaches without evidence of concrete advantages over the chosen one
- Suggestions that add complexity without clear planning value

## Priority Levels

- **P0** — Spec is fundamentally flawed. Missing core requirement or internal contradiction that blocks planning
- **P1** — Significant gap that will likely cause planning or implementation problems
- **P2** — Moderate issue that should be addressed before planning
- **P3** — Minor improvement

## Output Format

Return findings as a numbered list. For each finding:

```
### [P<N>] <title (imperative, ≤80 chars)>

**Section:** <spec section where the issue occurs>
**Reviewer:** <internal | peer>

<one paragraph explaining why this is a problem, what impact it has on planning or implementation, and a suggested fix>
```

After all findings, add:

```
## Overall Verdict

**Readiness:** <ready | needs revision>

<1-3 sentence assessment>
```

If there are no qualifying findings, state that the spec looks ready for planning and explain briefly.

## Rules

- If any reviewer is unavailable or returns malformed output, proceed with findings from the remaining reviewer.
- Present findings grouped by priority, then by reviewer.
