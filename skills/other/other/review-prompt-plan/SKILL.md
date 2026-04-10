---
name: review-prompt-plan
description: "Review a prompt plan against its source spec: launches an internal prompt plan review and `/peer-review` in parallel and returns combined findings. Use when the user asks to \"review my prompt plan\", \"review my prompts\", \"check my prompt plan\", \"critique my prompts\", or wants prompt plan feedback before implementation."
---

# Review Prompt Plan

Run two AI prompt plan reviews in parallel and return combined findings.

## Step 1: Identify the Prompt Plan

Determine the prompt plan index to review using these rules in order:

1. **Prompt plan text in conversation** — If full prompt plan text is already in context, use it
2. **Explicit path** — If a file path was provided, read it
3. **Explicit slug** — If a slug was provided, resolve to `.turbo/prompt-plans/<slug>.md`
4. **Single file** — Glob `.turbo/prompt-plans/*.md`. If exactly one file exists, read it
5. **Most recent** — If multiple files exist, read the most recently modified
6. **Legacy fallback** — If `.turbo/prompt-plans/` does not exist but `.turbo/prompts.md` exists, use it
7. **Nothing found** — If no prompt plan exists, say so and stop

Read the index file. For each shell listed in the index, read the corresponding shell file from the `Shell:` path. Also read the source spec (path listed in the index's `Source:` field).

## Step 2: Run Two Reviews in Parallel

Launch two Agent tool calls in a single message so they run concurrently (`model: "opus"`, do not set `run_in_background`):

### Internal Prompt Plan Review

Spawn a subagent with the full index text, every shell's full text, and the source spec. Instruct it to:

1. Apply the prompt plan review dimensions below
2. Return findings in the output format below

### Run `/peer-review` Skill

Spawn a subagent whose prompt includes the full index text, every shell's full text, the source spec, and the following review prompt, and instructs it to invoke `/peer-review` via the Skill tool:

```
<task>
Review the following prompt plan against its source spec. The prompt plan consists of an index file listing shells, plus one shell file per entry containing Context, Produces, Consumes, Covers Spec Requirements, high-level Implementation Steps, and Open Questions. Check for: spec requirements not appearing in any shell's Covers Spec Requirements field (gaps), dead ends where a shell's Produces is never consumed by a later shell or required by the final system, missing prerequisites where a shell's Consumes does not trace to a prior shell's Produces or to "from existing codebase", implicit dependencies where a shell's Consumes traces to a prior shell that is not listed in its Depends on field, duplicated requirements across shells' Covers Spec Requirements fields, and incorrect dependency ordering.
</task>

<structured_output_contract>
For each issue, state: the problem, which shell(s) are affected, the impact, a suggested fix, and priority: P0 (spec requirement missing or system broken), P1 (significant gap), P2 (moderate issue), P3 (minor improvement).
Ignore stylistic preferences. If no issues are found, state that the prompt plan looks sound.
</structured_output_contract>
```

## Step 3: Aggregate Combined Findings

Wait for both agents to complete. Aggregate their findings with attribution (reviewer: "internal" or "peer").

## Prompt Plan Review Dimensions

### 1. Spec Coverage (No Gaps)

The union of every shell's `Covers Spec Requirements` field must equal the set of requirements in the source spec. For each spec requirement, verify it appears in at least one shell's `Covers Spec Requirements` list. Flag any requirement not covered.

### 2. Wiring (Consumes Trace to Produces)

Every entry in a shell's `Consumes` field must trace to either:

- A prior shell's `Produces` entry (check dependency ordering via the index's `Depends on` field), OR
- An explicit "from existing codebase" annotation

Flag:

- **Missing prerequisites** — Consumes entries with no matching source
- **Dead ends** — Produces entries that no later shell Consumes and that are not part of the final system's entry points (e.g., top-level APIs, main functions, UI routes)
- **Implicit dependencies** — Shells whose Consumes trace to a prior shell that is not listed in their `Depends on` field

### 3. Completeness (Chain Implements the Spec)

Walk through the shells in dependency order and accumulate their Produces into a running set. After the final shell, verify that every spec requirement (not just every Covers entry) is satisfied by a reachable component in the running set. No component should be orphaned.

### 4. No Duplication

The `Covers Spec Requirements` fields across shells must be disjoint. Flag any spec requirement that appears in more than one shell's `Covers Spec Requirements`. If two shells intentionally touch the same area (one creates, the other extends), the requirement should still map to exactly one of them.

### 5. Cross-Reference Accuracy

If shells reference external resources (other codebases, documentation, APIs, search terms) in their Context, Implementation Steps, or Open Questions, spot-check that referenced projects or docs actually exist and are relevant.

## Priority Levels

- **P0** — Spec requirement missing from all shells, or shell chain produces a broken system
- **P1** — Dead end, missing prerequisite, or implicit dependency that will cause implementation problems
- **P2** — Moderate issue: duplicated requirement, unclear shell boundary, or ordering improvement
- **P3** — Minor improvement

## Output Format

Return findings as a numbered list. For each finding:

```
### [P<N>] <title (imperative, ≤80 chars)>

**Shell(s):** <shell number(s) affected>
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
