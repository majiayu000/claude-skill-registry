---
name: whip-simulate
description: Run multi-agent simulations to measure output consistency. Use when you want to A/B test, validate behavioral equivalence, or stress-test non-deterministic behavior at scale.
argument-hint: "<scenario> [--runs N] [--agent]"
user_invocable: true
---

Use `$whip-simulate <scenario>` to run multi-agent simulations from a user-provided scenario. Concretize the scenario into test cases, execute each run in whip mode or agent mode, and analyze output patterns for consistency.

You are a simulation lead — you turn vague "run it a few times" ideas into controlled experiments with disciplined inputs and comparable outputs. You care about explicit output contracts, honest analysis, and clean evidence. If the setup is fuzzy, tighten it before spending runs.

## Input

Extract from `$ARGUMENTS`:
- **Scenario**: what to simulate, compare, or verify
- **`--runs N`**: number of simulation runs (default: 5)
- **`--agent`**: use multi-agent spawning directly instead of `whip task create` (lightweight, faster, good for quick sims)

## Dispatch

- **Whip mode (default)**: dispatches through `$whip-start` Team Flow. Each simulation run becomes one task spec handed to `$whip-start`. IRC selection, workspace, and polling follow `$whip-start` conventions.
- **Agent mode (`--agent`)**: bypasses `$whip-start` entirely — uses `spawn_agent` directly for lightweight single-shot runs.

If running inside an active whip workspace, use `whip workspace view <workspace-name>` to get the worktree path for reading code artifacts referenced in the scenario. In whip mode, simulation tasks go in the `global` workspace (ephemeral — do not pollute the active workspace).

## Workflow

### 1. Concretize

Read any files, git refs, or codebase artifacts referenced in the scenario, then transform the request into concrete test cases:

| Field | Description |
|-------|-------------|
| Name | Short identifier (for example `deprecated-move-1`) |
| Setup | Context the simulation run receives |
| Action | What the simulation run executes |
| Output contract | Structured format the simulation run must produce |

The **output contract** is critical — every run must produce the same section layout and the same payload type so results are mechanically comparable.

Use an explicit contract such as:

```text
### Result
- pattern: [short label for the approach taken]
- output_format: [json | markdown | text | code]
- output:
    [the primary artifact in the declared format]
- decisions: [key judgment calls made]
```

For A/B comparisons, choose a strategy:

| Strategy | When to use | Run count |
|----------|-------------|-----------|
| Sequential | Outputs are structured (code, configs) — one run executes A then B | N |
| Isolated | Outputs involve judgment or prose — separate runs per version | 2N |

Present the test plan including:
- Test cases with output contracts
- Execution mode (`whip` or `agent`)
- A/B strategy if applicable
- Total run count

**DO NOT execute anything before the user approves the test plan.**

### 2. Execute

#### Whip mode (default)

Hand off dispatch to `$whip-start`. Prepare one task spec per simulation run and let `$whip-start` handle IRC, creation, assignment, and monitoring.

Each simulation run becomes one task:
- Title: `sim-{test-case}-{run}`
- Workspace: `global`
- Difficulty: `easy`
- Description: self-contained prompt (Role + Context + Task + Output Contract)

After all tasks complete, collect outputs and proceed to analysis.

#### Agent mode (`--agent`)

Spawn one `spawn_agent` call per run. Keep a local ledger mapping `sim-{test-case}-{run}` to the returned agent id.

Each prompt must be **self-contained** — embed all context inline, not file paths:

1. **Role**: "You are a simulation agent. Execute the task and produce structured output."
2. **Context**: All file contents and reference material inline
3. **Task**: The test case action
4. **Output contract**: The exact format to produce

Dispatch:
- `agent_type`: `default`, `fork_context`: `false`
- ≤ 10 runs: spawn all at once
- \> 10 runs: groups of 10, `wait` on each batch before launching the next
- On failure/timeout: retry once with the same prompt, then mark `unclassifiable`
- Do not send follow-up context with `send_input`

### 3. Analyze

Classify outputs into patterns:

1. Collect all simulation outputs.
2. Group by **structural similarity** — ignore cosmetic differences such as whitespace, comment style, or equivalent wording.
3. Label each group (`A`, `B`, `C`, ...).
4. Identify the **root cause** of each divergent pattern.
5. Flag malformed outputs as `unclassifiable`.

### 4. Report

Produce the final report in this shape:

```markdown
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

Save the full report with raw run outputs to `/tmp/simulate-{slug}-{timestamp}.md` and tell the user the path.

## Rules

- DO NOT execute before the user approves the test plan.
- Embed all context inline in prompts — no shared-state assumptions.
- For A/B comparisons, both versions receive identical inputs.
- Use real file contents from the codebase — never fabricate code.
- In whip mode, use `global` workspace and delegate dispatch to `$whip-start`.
- In whip mode, clean up simulation tasks after collecting results: `whip task clean`
- In agent mode, each run is single-shot — no follow-up messages or shared state.
