---
name: whip-simulate
description: Run multi-agent simulations to measure consistency of non-deterministic behavior. Use when the user wants to A/B test, validate behavioral equivalence, or stress-test outputs at scale.
argument-hint: "<scenario> [--runs N] [--agent]"
user_invocable: true
---

Run multi-agent simulations from a user-provided scenario. Concretize the scenario into test cases, spawn agents, and analyze output patterns for consistency.

## Input

Extract from `$ARGUMENTS`:
- **Scenario**: what to simulate, compare, or verify
- **`--runs N`**: number of simulation runs (default: 5)
- **`--agent`**: use Agent tool directly instead of `whip task create` (lightweight, faster, good for quick sims)

## Dispatch

- **Whip mode (default)**: dispatches through `/whip-start` Team Flow. Each simulation run becomes one task spec handed to `/whip-start`. IRC selection, workspace, and polling follow `/whip-start` conventions.
- **Agent mode (`--agent`)**: bypasses `/whip-start` entirely — uses Agent tool directly for lightweight single-shot runs.

If running inside an active whip workspace, use `whip workspace view <workspace-name>` to get the worktree path for reading code artifacts referenced in the scenario. In whip mode, simulation tasks go in the `global` workspace (ephemeral — do not pollute the active workspace).

## Workflow

### 1. Concretize

Read any files, git refs, or codebase artifacts referenced in the scenario, then transform it into concrete test cases:

| Field | Description |
|-------|-------------|
| Name | Short identifier (e.g., `deprecated-move-1`) |
| Setup | Context the agent receives (file contents, code, instructions) |
| Action | What the agent executes |
| Output contract | Structured format the agent must produce |

The **output contract** is critical — all agents must produce the same structure so results are mechanically comparable:

```
### Result
- pattern: [short label for the approach taken]
- output:
  ```
  [code block, JSON, or other structured output]
  ```
- decisions: [key judgment calls made]
```

For A/B comparisons, choose a strategy:

| Strategy | When to use | Agent count |
|----------|-------------|-------------|
| Sequential | Outputs are structured (code, configs) — one agent runs A then B | N |
| Isolated | Outputs involve judgment or prose — separate agents per version | 2N |

Present the test plan including:
- Test cases with output contracts
- Execution mode (whip or agent)
- A/B strategy if applicable
- Total agent count

**Wait for user approval before executing.**

### 2. Execute

#### Whip mode (default)

Hand off dispatch to `/whip-start`. Prepare one task spec per simulation run and let `/whip-start` handle IRC, creation, assignment, and monitoring.

Each simulation run becomes one task:
- Title: `sim-{test-case}-{run}`
- Workspace: `global`
- Difficulty: `easy`
- Description: self-contained prompt (Role + Context + Task + Output Contract)

After all tasks complete, collect outputs and proceed to analysis.

#### Agent mode (`--agent`)

Spawn one Agent tool call per run, named `sim-{test-case}-{run}`.

Each prompt must be **self-contained** — embed all context inline, not file paths:

1. **Role**: "You are a simulation agent. Execute the task and produce structured output."
2. **Context**: All file contents and reference material inline
3. **Task**: The test case action
4. **Output contract**: The exact format to produce

Batching:
- ≤ 10 runs: spawn all at once with `run_in_background: true`
- \> 10 runs: groups of 10, next batch after previous completes

### 3. Analyze

Classify outputs into patterns:

1. Collect all agent outputs
2. Group by **structural similarity** — ignore cosmetic differences (whitespace, comment style, translation wording)
3. Label each group (A, B, C...)
4. Identify **root cause** of each divergent pattern
5. Flag agents with malformed output as "unclassifiable"

### 4. Report

```
## Simulation Report

### Consistency: X/N (Y%)

### Output Patterns
| Pattern | Count | Runs | Description |
|---------|-------|------|-------------|
| A       | 8     | #1-6,#8,#10 | [dominant behavior] |
| B       | 2     | #7,#9 | [variant behavior] |

### Divergence Analysis
For each non-dominant pattern:
- Runs: [list]
- Root cause: [why]
- Severity: cosmetic | functional | breaking
- Diff from dominant: [key differences]

### Summary
- Total: N runs across M test cases
- Dominant pattern: A (X%)
- Key findings: ...
- Recommendation: [if applicable]
```

Save the full report with raw agent outputs to `/tmp/simulate-{slug}-{timestamp}.md` and tell the user the path.

## Rules

- Never execute before user approves the test plan
- Embed all context inline in prompts — no shared state assumptions
- For A/B comparisons, both versions receive identical inputs
- Use real file contents from the codebase — never fabricate code
- In whip mode, use `global` workspace and delegate dispatch to `/whip-start`
- In whip mode, clean up simulation tasks after collecting results: `whip task clean`
- In agent mode, each run is single-shot — no follow-up messages or shared state
