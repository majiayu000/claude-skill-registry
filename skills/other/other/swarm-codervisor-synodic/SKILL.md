---
name: swarm
description: "Speculative swarm — forks N agents to explore divergent strategies for the same task, cross-pollinates insights at checkpoints, prunes convergent branches, and fuses the best fragments into a composite result. Use when a problem has multiple viable approaches and you want to explore them simultaneously, or when the user invokes /swarm run <spec-path>."
---

# Speculative Swarm Skill

> **Governance:** This skill implements the Harness governance protocol.
> See [HARNESS.md](../../HARNESS.md) for the evaluation model, checkpoint protocol,
> and feedback taxonomy. Swarm's checkpoint map:
> - Step 3 CHECKPOINT (cross-pollination) → Layer 1 (convergence detection)
> - Step 4 PRUNE → Layer 1 (algorithmic similarity)
> - Step 5 MERGE GATE → Layer 2 (fragment quality scoring)
> - Step 7 Escalate → Layer 3

Fork N agents from a single task to explore divergent strategies simultaneously. At configurable checkpoints, branches cross-pollinate insights. Convergence detection prunes redundant branches. Fragment fusion merges the best pieces from surviving branches into a result no single branch could produce.

**This is not a committee or ensemble.** Committees discuss and vote on one solution. Ensembles average independent predictions. Speculative swarm *executes divergently and fuses selectively*.

**Agent property exploited:** Zero fork cost + speculative parallelism — agents can execute N mutually exclusive strategies simultaneously, which humans cannot.

## Usage

```
/swarm run <spec-path> [--strategies N] [--merge fragment-fusion|winner-take-all|weighted-blend]
```

Examples:
```
/swarm run specs/050-algorithm-design/README.md
/swarm run specs/050-algorithm-design/README.md --strategies 4 --merge winner-take-all
```

## Configuration

Defaults can be overridden by placing a `.swarm.yaml` in the repo root:

```yaml
swarm:
  max_forks: 4                        # Maximum parallel branches (default: 4)
  checkpoint_interval_steps: 1        # Cross-pollinate every N solve steps (default: 1)
  convergence_threshold: 0.85         # 0.0–1.0 similarity for pruning (default: 0.85)
  merge: fragment-fusion              # fragment-fusion | winner-take-all | weighted-blend
  budget:
    max_attempts_per_branch: 3        # Max solve attempts per branch (default: 3)
```

## Orchestration Protocol

When invoked, execute the following steps **exactly**:

### Step 1 — Initialize

1. Read the spec at `<spec-path>`.
2. Generate a work ID: `swarm-{unix-timestamp}` (e.g., `swarm-1710600000`).
3. Create `.swarm/{work-id}/` directory.
4. Initialize `manifest.json`:
   ```json
   {
     "id": "{work-id}",
     "spec": "{spec-path}",
     "status": "forking",
     "branches": [],
     "checkpoints": [],
     "pruned": [],
     "merge_result": null,
     "metrics": {}
   }
   ```
5. Read `.swarm.yaml` from the repo root if it exists and override defaults.
6. Record the start time for cycle-time measurement.

### Step 2 — Fork (generate divergent strategies)

Spawn a **general-purpose subagent** to generate divergent strategy prompts:

```
Agent(
  subagent_type: "general-purpose",
  prompt: <STRATEGIZE_PROMPT below>
)
```

**STRATEGIZE_PROMPT:**

> You are the STRATEGIZE station of a speculative swarm pipeline.
>
> ## Task
> {full spec content}
>
> ## Instructions
>
> Analyze this task and generate {max_forks} fundamentally different strategies
> for solving it. Each strategy must be a genuinely different approach, not a
> minor variation.
>
> Good strategies diverge on:
> - Algorithm choice (recursion vs iteration vs reduction)
> - Architecture (monolith vs microservice vs event-driven)
> - Data structure (tree vs graph vs hash map)
> - Paradigm (imperative vs functional vs declarative)
>
> Bad strategies diverge only on:
> - Naming conventions
> - Code style
> - Comment placement
>
> ## Output format
>
> ```
> === STRATEGY SET ===
> STRATEGIES:
> - id: strategy-1
>   name: {short descriptive name}
>   approach: {2-3 sentence description of the approach}
>   prompt_suffix: {instruction to append to the solve prompt for this strategy}
> - id: strategy-2
>   ...
> === END STRATEGY SET ===
> ```

After the strategize subagent returns:
- Parse the STRATEGY SET.
- Record strategies in the manifest.
- For each strategy, spawn a SOLVE subagent (Step 2b).

### Step 2b — Solve branches (parallel)

Spawn **general-purpose subagents** for ALL branches concurrently, each with `isolation: worktree`:

```
Agent(
  subagent_type: "general-purpose",
  isolation: "worktree",
  prompt: <BRANCH_SOLVE_PROMPT below>
)
```

**BRANCH_SOLVE_PROMPT:**

> You are BRANCH {branch-id} of a speculative swarm. You are one of {N} agents
> exploring different strategies for the same task.
>
> ## Task
> {full spec content}
>
> ## Your strategy
> {strategy name}: {strategy approach}
> {prompt_suffix}
>
> ## Cross-pollination context (if any)
> {insights from other branches at previous checkpoints, or "None — first attempt."}
>
> ## Rework feedback (if any)
> {rework items from previous checkpoint, or "None — first attempt."}
>
> ## Instructions
>
> 1. Implement the task using YOUR assigned strategy.
> 2. Do not deviate to another strategy — divergence is the point.
> 3. Run any tests mentioned in the spec (if applicable).
> 4. Commit all changes with prefix `swarm({branch-id}):`.
> 5. After committing, run `git diff main...HEAD --stat`.
>
> ## Output format
>
> ```
> === BRANCH REPORT ===
> BRANCH: {branch-id}
> STRATEGY: {strategy name}
> STATUS: COMPLETE | PARTIAL | FAILED
> FILES: {comma-separated list of files changed}
> TESTS: PASS | FAIL | SKIPPED
> COMMIT: {short SHA}
> WORKTREE_BRANCH: {branch name from the worktree}
> KEY_INSIGHT: {one sentence — the most important thing learned}
> FRAGMENT_SUMMARY: {paragraph — what this branch produced that could be reused}
> === END BRANCH REPORT ===
> ```

After all branch subagents return:
- Parse each BRANCH REPORT.
- Record results in the manifest.
- Proceed to Step 3 (Checkpoint).

### Step 3 — Checkpoint (cross-pollination + convergence detection)

After each solve round, evaluate all branches:

1. **Collect insights.** Extract `KEY_INSIGHT` and `FRAGMENT_SUMMARY` from each branch report.

2. **Convergence detection (algorithmic).** Compare branch outputs pairwise:
   - Collect the file lists from each branch report.
   - Compute Jaccard similarity on changed file sets.
   - If two branches modified >85% the same files with similar diffs (convergence_threshold), flag for pruning.

3. **Cross-pollination.** Aggregate all `KEY_INSIGHT` values into a shared context block that will be passed to surviving branches in the next solve round.

4. Record the checkpoint in the manifest:
   ```json
   {
     "checkpoint": 1,
     "convergence_pairs": [["strategy-1", "strategy-3"]],
     "insights": ["insight from branch 1", "..."],
     "pruned_this_round": ["strategy-3"]
   }
   ```

### Step 4 — Prune

For each convergence pair flagged in Step 3:

1. Compare the two branches' test results and status.
2. Prune the lower-quality branch (prefer PASS over FAIL, COMPLETE over PARTIAL).
3. If equal quality, prune the one with fewer unique files changed (less novel).
4. Record the pruned branch and reason in the manifest.

**Minimum survivors:** Never prune below 2 branches. If pruning would leave fewer than 2, skip pruning.

### Step 5 — Merge (fragment fusion)

After checkpoints and pruning are complete, merge surviving branches.

Spawn a **general-purpose subagent** with `isolation: worktree`:

```
Agent(
  subagent_type: "general-purpose",
  isolation: "worktree",
  prompt: <MERGE_PROMPT below>
)
```

**MERGE_PROMPT (fragment-fusion):**

> You are the MERGE station of a speculative swarm. Multiple agents explored
> different strategies for the same task. Your job is to produce a result
> that combines the best fragments from each surviving branch.
>
> ## Original task
> {full spec content}
>
> ## Surviving branches
> {for each surviving branch: id, strategy, branch report, key files changed}
>
> ## Branch diffs
> {for each surviving branch: `git diff main...{worktree-branch}`}
>
> ## Merge strategy: {merge}
>
> ### fragment-fusion (default)
> Decompose each branch's output into scored fragments (functions, modules,
> design decisions). Select the highest-quality fragment for each sub-problem.
> The result should be BETTER than any single branch — a novel composite.
>
> ### winner-take-all
> Select the single best branch. Only use when outputs are atomic and cannot
> be meaningfully decomposed into fragments.
>
> ### weighted-blend
> Weighted combination of approaches. Only use when outputs are numeric
> or probabilistic.
>
> ## Instructions
>
> 1. Read each branch's diff carefully.
> 2. Identify the strongest fragments from each branch.
> 3. Construct the merged implementation, resolving any conflicts.
> 4. Run tests to verify the merged result.
> 5. Commit with prefix `swarm(merge):`.
>
> ## Output format
>
> ```
> === MERGE REPORT ===
> MERGE_STRATEGY: {fragment-fusion|winner-take-all|weighted-blend}
> STATUS: MERGED | CONFLICT | FAILED
> FRAGMENTS_USED:
> - from: {branch-id}
>   what: {description of fragment taken}
>   why: {why this fragment was best}
> - from: {branch-id}
>   ...
> FILES: {comma-separated list of files in merged result}
> TESTS: PASS | FAIL | SKIPPED
> COMMIT: {short SHA}
> WORKTREE_BRANCH: {branch name}
> SUMMARY: {one-paragraph summary of the fused result}
> === END MERGE REPORT ===
> ```

After the merge subagent returns:
- Parse the MERGE REPORT.
- Record in the manifest.

### Step 5.5 — MERGE GATE (static checks)

After MERGE completes, run project-level checks (same as Factory's STATIC GATE):

1. **Detect languages changed** from the MERGE REPORT files list:
   - **Rust** (`.rs`): `cargo check` and `cargo clippy -- -D warnings`
   - **TypeScript/JavaScript** (`.ts`, `.tsx`, `.js`, `.jsx`): `tsc --noEmit` and `eslint`
   - **Python** (`.py`): `pyright` and `ruff check`

2. **Custom rules**: Run `.harness/rules/` scripts against the merge diff.

3. **If failures:** Route back to Step 5 with failures as rework feedback. Cap at 1 static rework.

4. **If pass:** Proceed to Step 6.

### Step 6 — Create PR

1. Push the merge branch: `git push -u origin swarm/{work-id}`
2. Create a PR using `gh pr create`:
   ```
   gh pr create \
     --title "swarm: {spec title}" \
     --body "## Speculative Swarm Report

   **Spec:** {spec-path}
   **Work ID:** {work-id}
   **Strategies explored:** {N}
   **Surviving branches:** {M}
   **Merge strategy:** {merge strategy used}

   ## Strategy Summary
   {table of strategies: id, name, status, pruned?}

   ## Fragment Attribution
   {which fragments came from which branch}

   ---
   *Produced by the Synodic swarm skill.*"
   ```
3. Update the manifest with final status and metrics.
4. Report success to the user with the PR URL.

### Step 7 — Escalate

If the merge fails after rework:

1. Update the manifest: `"status": "escalated"`.
2. Report to the user:
   - The swarm could not produce a merged result.
   - Show surviving branch reports for manual selection.
   - Individual branch worktrees are available for inspection.
3. Do NOT create a PR.

### Step 8 — Finalize Manifest

After Step 6 or Step 7, update `.swarm/{work-id}/manifest.json` with:

```json
{
  "metrics": {
    "cycle_time_seconds": 0,
    "total_branches": 0,
    "surviving_branches": 0,
    "pruned_branches": 0,
    "checkpoints": 0,
    "merge_strategy": "fragment-fusion",
    "fragments_used": [{"from": "strategy-1", "what": "..."}]
  }
}
```

### Step 8b — Persist to GovernanceLog

Append a summary record to `.harness/swarm.governance.jsonl`:

```json
{
  "work_id": "swarm-...",
  "source": "swarm",
  "spec": "specs/...",
  "timestamp": "<ISO 8601>",
  "status": "merged|escalated",
  "total_branches": 0,
  "surviving_branches": 0,
  "pruned_branches": 0,
  "pruned_reasons": [{"branch": "strategy-3", "reason": "converged with strategy-1"}],
  "merge_strategy": "fragment-fusion",
  "merge_status": "MERGED|CONFLICT|FAILED",
  "static_failures": [],
  "fragments_used": [{"from": "strategy-1", "what": "..."}],
  "cycle_time_seconds": 0
}
```

After appending, commit the updated `governance.jsonl` as part of the swarm run.

## Parsing Rules

- STRATEGY SET is between `=== STRATEGY SET ===` and `=== END STRATEGY SET ===`.
- BRANCH REPORT is between `=== BRANCH REPORT ===` and `=== END BRANCH REPORT ===`.
- MERGE REPORT is between `=== MERGE REPORT ===` and `=== END MERGE REPORT ===`.
- If a subagent response doesn't contain the expected block, log the raw response in the manifest and treat it as FAILED.

## Important Notes

- **Divergence is the point.** Each branch must follow its assigned strategy. Cross-pollination shares insights, not implementations — branches that converge get pruned.
- **Never swarm within a swarm.** N outer x M inner = N*M agents. Multiplicative cost with no convergence guarantee. This is the one invalid composition.
- `.swarm/` directory is gitignored (per-run manifests are local artifacts). Governance logs go to `.harness/swarm.governance.jsonl`.
- All branch subagents run in `isolation: worktree` so branches have independent git state.
- **Fragment fusion** produces novel composite outputs — the merged result should be strictly better than any individual branch.
- **Winner-take-all** is the fallback when outputs are atomic (cannot be decomposed into fragments).
- **Minimum 2 survivors** — never prune to fewer than 2 branches, as the merge needs at least 2 inputs to justify the swarm overhead.
- Budget is bounded: `max_forks` caps branch count, `max_attempts_per_branch` caps rework per branch.

## Composability

| Composition | Valid | Rationale |
|-------------|-------|-----------|
| Pipeline → Swarm | Yes | Each pipeline stage is independent; swarming within a stage doesn't affect others |
| Swarm → Adversarial | Yes | Each branch gets adversarial hardening before the merge selects among them |
| Fractal → Swarm | Yes | A fractal leaf uses swarm to explore multiple solution strategies |
| Factory → Swarm | Yes | Factory BUILD invokes swarm when the spec has multiple viable approaches |
| **Swarm → Swarm** | **No** | N outer x M inner = N*M agents. Multiplicative cost, no convergence guarantee |

## Comparison with Other Skills

| Aspect | Factory | Fractal | Swarm |
|--------|---------|---------|-------|
| Shape | Linear pipeline | Recursive tree | Parallel fan-out + merge |
| Strategy | Single attempt + review | Divide and conquer | Explore N strategies |
| Parallelism | Sequential stations | Parallel leaves | Parallel branches |
| Output | Reviewed implementation | Unified sub-solutions | Best-of-N composite |
| When to use | Single spec, needs review | Complex, needs decomposition | Multiple viable approaches |
