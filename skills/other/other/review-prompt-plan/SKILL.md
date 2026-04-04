---
name: review-prompt-plan
description: "Review a prompt plan against its source spec: launches an internal prompt plan review and `/peer-review` in parallel and returns combined findings. Use when the user asks to \"review my prompt plan\", \"review my prompts\", \"check my prompt plan\", \"critique my prompts\", or wants prompt plan feedback before implementation."
---

# Review Prompt Plan

Run two AI prompt plan reviews in parallel and return combined findings. The core principle: a prompt plan is a "broken down spec." Following the full prompt chain should implement the entire spec with nothing missing and nothing disconnected.

## Step 1: Identify the Prompt Plan

Determine the prompt plan to review:

- If **prompt plan text** is in conversation context, use it
- If a **file path** was provided, read the file
- If **neither** was provided, check for a prompt plan at `.turbo/prompts.md`

Also read the source spec (path listed in the prompt plan's `Source:` field).

## Step 2: Run Two Reviews in Parallel

Launch two Agent tool calls in a single message so they run concurrently (`model: "opus"`, do not set `run_in_background`):

### Internal Prompt Plan Review

Spawn a subagent with the full prompt plan text and the source spec. Instruct it to:

1. Apply the prompt plan review dimensions below
2. Return findings in the output format below

### Run `/peer-review` Skill

Spawn a subagent whose prompt includes the full prompt plan text, the source spec, and the following review prompt, and instructs it to invoke `/peer-review` via the Skill tool:

```
<task>
Review the following prompt plan against its source spec. Check for: spec requirements not covered by any prompt, dead ends where a prompt creates something no later prompt consumes, missing prerequisites where a prompt assumes something no prior prompt creates, duplicated requirements across prompts, and incorrect dependency ordering.
</task>

<structured_output_contract>
For each issue, state: the problem, which prompt(s) are affected, the impact, a suggested fix, and priority: P0 (spec requirement missing or system broken), P1 (significant gap), P2 (moderate issue), P3 (minor improvement).
Ignore stylistic preferences. If no issues are found, state that the prompt plan looks sound.
</structured_output_contract>
```

## Step 3: Return Combined Findings

Wait for both agents to complete. Aggregate their findings with attribution (reviewer: "internal" or "peer") and return them to the caller.

The caller determines what to do with the findings (evaluate, apply, or present to the user).

## Prompt Plan Review Dimensions

### 1. Spec Coverage (No Gaps)

For every requirement, feature, acceptance criterion, and constraint in the spec, verify it appears in at least one prompt. Flag any requirement not assigned to a prompt.

### 2. Wiring (Outputs Feed Inputs)

Each prompt produces artifacts (files, modules, endpoints, types) that later prompts may depend on. Verify the chain is connected. Check for:

- **Dead ends** — A prompt creates a module, API, or capability that no subsequent prompt consumes or integrates
- **Missing prerequisites** — A prompt assumes an artifact exists that no prior prompt creates
- **Implicit dependencies** — A prompt's `Depends on` field omits a prompt it actually relies on

### 3. Completeness (Chain Implements the Spec)

Walk through the prompts in order and simulate what exists after each one completes. After the final prompt, verify that every spec feature is reachable from the project's entry points and no component is orphaned.

### 4. No Duplication

Verify each spec requirement is assigned to exactly one prompt. Duplication causes conflicting implementations. If two prompts intentionally touch the same area (one creates, the other extends), confirm they have clear boundaries.

### 5. Cross-Reference Accuracy

If prompts reference external resources (other codebases, documentation, APIs, search terms), spot-check that referenced projects or docs actually exist and are relevant.

## Priority Levels

- **P0** — Spec requirement missing from all prompts, or prompt chain produces a broken system
- **P1** — Dead end, missing prerequisite, or implicit dependency that will cause implementation problems
- **P2** — Moderate issue: duplicated requirement, unclear prompt boundary, or ordering improvement
- **P3** — Minor improvement

## Output Format

Return findings as a numbered list. For each finding:

```
### [P<N>] <title (imperative, ≤80 chars)>

**Prompt(s):** <prompt number(s) affected>
**Reviewer:** <internal | peer>

<one paragraph explaining the problem, what impact it has on implementation, and a suggested fix>
```

After all findings, add:

```
## Overall Verdict

**Readiness:** <ready | needs revision>

<1-3 sentence assessment>
```

If there are no qualifying findings, state that the prompt plan looks ready for implementation and explain briefly.

## Rules

- If any reviewer is unavailable or returns malformed output, proceed with findings from the remaining reviewer.
- Present findings grouped by priority, then by reviewer.
