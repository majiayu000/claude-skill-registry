---
name: simmer-reflect
description: >
  Reflect subskill for simmer. Records iteration results in trajectory table,
  tracks best candidate, handles regression rollback, and passes ASI forward
  to the next round. Supports both single-file and workspace modes. Do not
  invoke directly — called by simmer orchestrator after each judge round.
---

# Simmer Reflect

You are the only subskill that sees the full score history. Your job: record the iteration, track the best candidate, and pass the ASI forward.

## Context You Receive

- **Full score history**: all iterations so far (scores, composites, key changes)
- **Current iteration number** and **max iterations**
- **Latest judge output**: scores + ASI for this round
- **Generator report**: what changed this round (2-3 sentences)
- **Artifact type**: single-file or workspace

## What To Do

### 1. Record in Trajectory

Update `{OUTPUT_DIR}/trajectory.md` with the running score table.

**The trajectory table uses the same format regardless of evaluation mode (judge-only, runnable, or hybrid).** Do not dump raw evaluator output, per-test-case breakdowns, or inline analysis into the table. The table is a clean score record.

**Required format (do not add extra columns beyond those listed below):**

*Single-file mode:*
- Columns: Iteration, [criterion names from rubric], Composite, Key Change
- Below table: `Best candidate: iteration [N] (composite: [N.N]/10)`

```markdown
# Simmer Trajectory

| Iteration | [criterion 1] | [criterion 2] | [criterion 3] | Composite | Key Change |
|-----------|---------------|---------------|---------------|-----------|------------|
| 0         | 4             | 5             | 3             | 4.0       | seed       |
| 1         | 7             | 5             | 4             | 5.3       | [summary]  |
| 2         | 7             | 6             | 7             | 6.7       | [summary]  |

Best candidate: iteration 2 (composite: 6.7/10)
```

*Workspace mode:*
- Columns: Iteration, [criterion names from rubric], Composite, Config, Key Change
- The "Config" column captures the key workspace state (model name, topology, etc.) in a few words
- Below table: `Best candidate: iteration [N] (composite: [N.N]/10)`

```markdown
# Simmer Trajectory

| Iteration | Coverage | Efficiency | Noise | Composite | Config | Key Change |
|-----------|----------|------------|-------|-----------|--------|------------|
| 0         | 2        | 6          | 2     | 3.3       | qwen3.5:4b, single-call | seed |
| 1         | 4        | 4          | 4     | 4.0       | qwen3.5:27b, single-call | model swap + rich prompt |
| 2         | 3        | 5          | 3     | 3.3       | qwen3.5:9b, single-call | REGRESSION — 9b too weak |

Best candidate: iteration 1 (composite: 4.0/10)
```

**If evaluator details matter for context**, add them in a separate section BELOW the table:

```markdown
## Evaluator Details

### Iteration 1
- Video ozXhzdjT8tU: 54% coverage (23/43 matched)
- Video DRqUWtnXEXA: 48% coverage (15/31 matched)
- Missed: [list of key misses]
```

The table itself stays clean. Evaluator details are supplementary, not part of the trajectory record.

The "Key Change" column uses the generator's 2-3 sentence report, condensed to a few words (under 60 characters). For iteration 0 (the seed), Key Change is always "seed".

### 2. Track Best Candidate

Compare this iteration's score to the best-so-far. Update the "Best candidate" line at the bottom of the trajectory.

**If a PRIMARY criterion is specified in the setup brief:** best-so-far is determined by the primary criterion score first, composite as tiebreaker. Example: if primary is "coverage" and iteration 2 has coverage 6 (composite 5.3) vs iteration 4 with coverage 5 (composite 6.0), iteration 2 is best.

**If no primary criterion:** best-so-far is determined by composite (default).

**The best candidate may not be the latest one.** If iteration 3 scores lower than iteration 2, the best is still iteration 2.

### 2b. Handle Regression

If this iteration's composite is LOWER than best-so-far:
- Note the regression in the trajectory Key Change column (e.g., "REGRESSION — 9b too weak" or "regressed — prompt compression lost type table")
- Advise the orchestrator: next generator should receive the BEST candidate (not the latest), plus the current ASI
- Include in output: `REGRESSION: true — use iteration [N] as input to next generator`

**Workspace mode regression:** The orchestrator will selectively restore workspace files from the best iteration's commit (`git checkout <commit> -- <files>`). Trajectory.md and other tracking files are NOT reverted. Include the iteration number so the orchestrator knows which snapshot to restore.

### 3. Track Exploration Status (Workspace Mode)

If the setup brief includes a SEARCH_SPACE, review the trajectory to determine what has been explored vs what remains untried. Look at the Config column and Key Change column to identify:
- Which models have been tried
- Which topologies have been tried
- What other search space dimensions have been explored

Produce a concise exploration summary. Example:
```
Models tried: qwen3.5:4b (iter 0), qwen3.5:27b (iter 1-3). Untried: qwen3.5:9b.
Topologies tried: single-call (all iterations). Untried: multi-call.
Prompt changes: 4 variations tried.
```

Skip this for text/creative mode or when no search space is specified.

### 4. Track Stable Wins

Review the trajectory to identify what's been consistently working — elements that were added in a previous iteration and have NOT been associated with a regression since.

Look at the Key Change column across iterations. If an element was introduced at iteration N and scores held or improved through iterations N+1, N+2, etc., it's a stable win. If an iteration that removed or changed that element regressed, that's strong evidence it's load-bearing.

Produce a concise list. Example:
```text
STABLE WINS (do not remove):
- Correction lookup table (added iter 1, held through iters 2-4)
- Worked examples format (added iter 3, improved coverage each iteration since)

NOT WORKING:
- Verbose rule lists (tried iter 2, regressed)
- Multi-step prompt structure (tried iter 1, skipped by executor)
```

This gets passed to the judge board's deliberation summary so judges and the generator know what to preserve and what to avoid.

### 5. Pass ASI Forward

Return to the orchestrator:
- The ASI from this round's judge (passed unchanged to next generator)
- Which iteration contains the current best candidate
- Whether iterations remain
- Whether a regression occurred (and which candidate to use as input)
- Exploration status (workspace mode with search space only)
- Stable wins (what's working, what's not)

## Output to Orchestrator

```
ITERATION [N] RECORDED
BEST SO FAR: iteration [N] (composite: [N.N]/10)
REGRESSION: [true/false] — [if true: use iteration N as input to next generator]
ITERATIONS REMAINING: [N]
ASI FOR NEXT ROUND: [the judge's ASI, unchanged]
EXPLORATION STATUS: [what's been tried vs untried — omit for text/creative or no search space]
STABLE WINS: [what's working — do not remove]
NOT WORKING: [what's been tried and failed — do not retry same approach]
```

## Common Mistakes

**Dumping evaluator output into the trajectory table**
- Problem: Table becomes unreadable, format diverges from standard, can't compare across runs
- Fix: Table uses standard column format. Evaluator details go in a separate section below the table.

**Modifying the ASI**
- Problem: Reflect edits or summarizes the judge's ASI before passing it forward
- Fix: Pass the ASI through unchanged — the judge wrote it for the generator

**Not tracking best-so-far separately**
- Problem: Assumes the last iteration is the best
- Fix: Always compare composite to best-so-far, update if better

**Writing candidate content into trajectory**
- Problem: Trajectory file becomes huge, clutters context
- Fix: Trajectory only contains scores, composites, and short key-change summaries

**Using prose format instead of table**
- Problem: Trajectories written as paragraphs or bullet lists can't be scanned quickly
- Fix: Always use the markdown table format shown above, even in workspace mode with evaluator
