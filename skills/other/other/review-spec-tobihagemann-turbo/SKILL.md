---
name: review-spec
description: "Review a specification document: launches an internal spec review and `/peer-review-spec` in parallel and returns combined findings. Use when the user asks to \"review my spec\", \"review this spec\", \"check my spec\", \"critique my spec\", or wants spec feedback before planning."
---

# Review Spec

Run two AI spec reviews in parallel and return combined findings.

## Step 1: Identify the Spec

Determine the spec to review:

- If **spec text** is in conversation context, use it
- If a **spec file path** was provided, read the file
- If **neither** was provided, check for a spec at `.turbo/spec.md`

## Step 2: Run Two Reviews in Parallel

Launch two agents in a single message so they run concurrently (`model: "opus"`, do not set `run_in_background`):

### Internal Spec Review

Spawn a subagent with the full spec text and instruct it to:

1. Read project context (CLAUDE.md and any existing codebase) to understand constraints
2. Apply the spec determination criteria below
3. Return findings in the output format below

### Run `/peer-review-spec` Skill

Spawn a subagent to run the `/peer-review-spec` skill with the spec text.

## Step 3: Return Combined Findings

Wait for both agents to complete. Aggregate their findings with attribution (reviewer: "internal" or "peer") and return them to the caller.

The caller determines what to do with the findings (evaluate, apply, or present to the user).

## Spec Determination Criteria

Flag an issue only when ALL of these hold:

1. It would cause problems during implementation planning or lead to building the wrong thing
2. The issue is discrete and actionable (not a vague concern or general suggestion)
3. The author would likely fix the issue if made aware of it
4. The issue is clearly not an intentional design choice

### What to Review

- **Completeness** — Missing requirements, undefined behavior, TODOs, placeholder text, or "TBD" markers that would block planning
- **Consistency** — Internal contradictions between sections (e.g., data model conflicts with API design, feature list conflicts with MVP scope)
- **Clarity** — Ambiguous requirements that could lead to misinterpretation during implementation
- **Scope** — Spec focuses on a coherent system. No unconnected components or features that serve no specified consumer
- **YAGNI** — Unrequested features, over-engineering, or premature abstractions that add complexity without clear value

### What to Ignore

- Wording, stylistic, or cosmetic preferences that don't affect clarity
- Alternative architectural approaches that aren't clearly better
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
