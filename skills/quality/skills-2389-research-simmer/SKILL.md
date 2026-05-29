---
name: simmer
description: >
  Use when user says "simmer this", "refine this", "hone this", "iterate on this",
  or asks to improve a specific artifact over multiple rounds. Runs an iterative
  refinement loop with investigation-first judges that read the code, understand
  the problem, and propose evidence-based improvements. Auto-selects single judge
  or multi-judge board based on complexity. Works on any artifact type: documents,
  prompts, specs, emails, creative writing, API designs, pipelines, codebases.
  Supports multi-file workspace targets, runnable evaluators, and open-ended
  optimization (model selection, pipeline topology, prompt tuning).
---

# Simmer

Iterative refinement loop — take an artifact (single file or workspace) and hone it repeatedly against user-defined criteria until it's as good as it can get.

**Related skills (test-kitchen family):**
- `test-kitchen:omakase-off` — don't know what you want → parallel designs → react → pick
- `test-kitchen:cookoff` — know what you want, it's code → parallel implementations → fixed criteria → steal the best
- `simmer` — know what you want, it's anything → user-defined criteria → iterate until good

## Flow

```
"Simmer this" / "Refine this" / "Optimize this pipeline"
    ↓
┌─────────────────────────────────────┐
│  SETUP (identify + criteria)        │
│  Load simmer-setup subskill         │
│                                     │
│  Output: artifact, rubric, N iters, │
│  evaluator (optional),              │
│  background (optional)              │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  LOOP (default 3 iterations)        │
│                                     │
│  Each iteration:                    │
│  1. Dispatch generator subagent     │
│  2. Run evaluator (if present)      │
│  3. Dispatch judge subagent         │
│  4. Load reflect subskill           │
│                                     │
│  Generator gets: candidate + ASI    │
│           + background              │
│  Judge gets: candidate + rubric     │
│       + evaluator output (if any)   │
│  Reflect gets: full score history   │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  OUTPUT                             │
│  Best candidate → result file       │
│  Score trajectory displayed         │
└─────────────────────────────────────┘
```

## When to Use

Trigger when user wants iterative refinement of any kind:
- "Simmer this", "refine this", "hone this", "iterate on this"
- "Make this better", "improve this over a few rounds"
- "Polish this", "tighten this up"
- "Optimize this pipeline", "find the best model for this task"
- "Tune this configuration", "improve these prompts against this test suite"
- Any request to iteratively improve an artifact or workspace


**Judge mode is auto-selected by setup** based on problem complexity:

| Condition | JUDGE_MODE |
|-----------|-----------|
| text/creative, ≤2 criteria, short artifact (email, tweet, tagline) | `single` |
| text/creative, 3 criteria or long/complex artifact | `board` |
| code/testable (any) | `board` |
| pipeline/engineering (any) | `board` |
| User says "with a single judge" | `single` (override) |
| User says "with a judge board" or "with a panel" | `board` (override) |

**Plateau upgrade:** If the loop started with a single judge and detects a plateau (3 iterations without improvement), offer: "Scores have plateaued. Switch to judge board for deeper diagnosis?" If the user accepts, switch to `JUDGE_MODE: board` for remaining iterations.

**Not simmer:** If the artifact is code and the user wants parallel implementations, use cookoff instead.

## Orchestration

**Announce:** "I'm using the simmer skill to set up iterative refinement."

**Track progress** (TodoWrite if available, otherwise inline):
1. Setup — identify artifact, elicit criteria, determine evaluation method
2. Refinement loop (N iterations)
3. Output best version with score trajectory

### Phase 1: Setup

**Invoke `simmer:simmer-setup`.**

Do not attempt to identify the artifact or ask about criteria yourself — that is the setup subskill's job.

**Shortcut:** If the user (or calling system) has already provided artifact, criteria (each with at least one sentence describing what a high score looks like), iteration count, mode, and optionally evaluator/background, skip the setup subskill entirely. Construct the setup brief directly and proceed to Phase 2.

Setup returns a brief:
```
ARTIFACT: [content, file path, or directory path]
ARTIFACT_TYPE: [single-file | workspace]
CRITERIA:
  - [criterion 1]: [what better looks like]
  - [criterion 2]: [what better looks like]
  - [criterion 3]: [what better looks like]
PRIMARY: [criterion name — omit if equally weighted]
EVALUATOR: [command to run — omit for judge-only mode]
BACKGROUND: [constraints, available resources, domain knowledge — omit if not needed]
OUTPUT_CONTRACT: [valid output format description — omit for text/creative]
VALIDATION_COMMAND: [quick check command — omit if no cheap validation exists]
SEARCH_SPACE: [what's in scope to explore — omit if unconstrained]
JUDGE_MODE: [single | board — auto-selected by setup based on complexity. User can override]
JUDGE_PANEL: [optional custom judge definitions — omit to use defaults for problem class]
ITERATIONS: [N]
MODE: [seedless | from-file | from-paste | from-workspace]
OUTPUT_DIR: [path, default: docs/simmer]
```

### Phase 2: Refinement Loop

**For single-file mode:**
```bash
mkdir -p {OUTPUT_DIR}
```

**For workspace mode:**
```bash
# Create initial commit to snapshot the seed state
cd {ARTIFACT}
git add -A && git commit -m "simmer: iteration 0 — seed state"
```

**Iteration counting:**

"N iterations" means N generate-judge-reflect cycles AFTER the initial seed judgment. The seed judgment is iteration 0 (not counted toward N). So `ITERATIONS: 3` means:
- Iteration 0: Judge the seed (no generator)
- Iteration 1: Generate → Judge → Reflect
- Iteration 2: Generate → Judge → Reflect
- Iteration 3: Generate → Judge → Reflect
- Total: 3 generation passes + 1 seed judgment = 4 judge rounds

For seedless mode: iteration 1 generates the initial candidate AND judges it. `ITERATIONS: 3` means 3 generation passes total.

**Iteration 0 (seed):**

*Single-file mode:*
- Write the seed artifact to `{OUTPUT_DIR}/iteration-0-candidate.md`
- If seedless: dispatch generator subagent to produce initial candidate from description + criteria, then judge it
- If from-file or from-paste: the seed IS the starting artifact — judge it directly (no generator)

*Workspace mode:*
- The seed is the current state of the workspace directory
- If from-workspace: judge the current state directly (no generator)
- If seedless: dispatch generator to scaffold the initial workspace, then judge it

**Each iteration:**

**Step 1: Generator (subagent)**

Invoke `simmer:simmer-generator` as a subagent.

*Single-file subagent prompt:*
```
You are the generator in a simmer refinement loop.

Invoke the skill: simmer:simmer-generator

ITERATION: [N]
ARTIFACT_TYPE: single-file
CRITERIA:
[rubric from setup]

CURRENT CANDIDATE:
[full text of current best candidate]

JUDGE FEEDBACK (ASI from previous round):
[ASI text, or "First iteration — generate initial candidate" if seedless iteration 1]

Write your improved candidate to: {OUTPUT_DIR}/iteration-[N]-candidate.md
(or appropriate extension matching artifact type)

Report: what specifically changed and why (2-3 sentences).
```

*Workspace subagent prompt:*
```
You are the generator in a simmer refinement loop.

Invoke the skill: simmer:simmer-generator

ITERATION: [N]
ARTIFACT_TYPE: workspace
WORKSPACE: [directory path]
CRITERIA:
[rubric from setup]

BACKGROUND:
[constraints, available resources, domain knowledge from setup]

OUTPUT_CONTRACT:
[valid output format — omit if not specified in setup]

VALIDATION_COMMAND:
[quick check command — omit if not specified in setup]

SEARCH_SPACE:
[what's in scope to explore — omit if not specified in setup]

JUDGE FEEDBACK (ASI from previous round):
[ASI text — may describe coordinated changes across multiple files]

EXPLORATION STATUS:
[from reflect: what's been tried vs untried — omit on iteration 1 or if no search space]

Make your changes directly in the workspace directory.
You may edit multiple files in a single iteration when the ASI calls for coordinated changes.
If making infrastructure changes, run VALIDATION_COMMAND (if available) before reporting success.

Report: what specifically changed and why (2-3 sentences).
```

**Step 2: Run Evaluator (if present)**

If the setup brief includes an `EVALUATOR` command:
```bash
cd {ARTIFACT}  # for workspace mode
{EVALUATOR}
```

Capture stdout and stderr. This output will be passed to the judge.

**Timeouts:** Set generous timeouts for evaluator commands. If the evaluator involves LLM inference, network calls, or large data processing, allow 10-60 minutes per run. The orchestrator should not timeout before the evaluator completes.

If no evaluator, skip this step.

**Step 3: Judge (subagent or judge board)**

**If `JUDGE_MODE: board`:** Invoke `simmer:simmer-judge-board` instead of the single judge. Pass it all the same context below, plus `JUDGE_PANEL` if specified in the setup brief. The board dispatches multiple judges, runs deliberation, and returns output in the exact same format as a single judge. The rest of the loop (reflect, generator) is unchanged.

**Include file paths so judges can investigate.** In addition to pasted content, pass:
- Path to the candidate file (or workspace directory)
- Path to the evaluator script (if evaluator mode)
- Path to ground truth / test data (if known from setup inspection)
- Paths to prior iteration candidate files
- Paths to config files (from setup inspection)

Judges need to read these files themselves — not just the pre-digested summaries in the prompt. A judge who reads the evaluator script discovers exact-match scoring on iteration 0 instead of learning it through 3 iterations of trial and error.

**Otherwise:** Invoke `simmer:simmer-judge` as a subagent.

*Without evaluator:*
```
You are the judge in a simmer refinement loop.

Invoke the skill: simmer:simmer-judge

ITERATION: [N]
ARTIFACT_TYPE: [single-file | workspace]
CRITERIA:
[rubric from setup]

CANDIDATE:
[full text of candidate, or key files from workspace]

SEED CALIBRATION:
[full text of original seed artifact, or key seed files]
SEED SCORES:
[iteration 0 scores — omit this block on iteration 0]

Score this candidate against the criteria using the seed as a calibration reference.
Do NOT look at or consider any intermediate iteration scores.
```

*With evaluator:*
```
You are the judge in a simmer refinement loop.

Invoke the skill: simmer:simmer-judge

ITERATION: [N]
ARTIFACT_TYPE: [single-file | workspace]
CRITERIA:
[rubric from setup]

CANDIDATE:
[full text of candidate, or key files from workspace]

EVALUATOR OUTPUT:
[stdout and stderr from the evaluator command]

SEED CALIBRATION:
[full text of original seed artifact, or key seed files]
SEED SCORES:
[iteration 0 scores — omit this block on iteration 0]

OUTPUT_CONTRACT:
[valid output format — omit if not specified in setup]

SEARCH_SPACE:
[what's in scope to explore — omit if not specified in setup]

PREVIOUS ASI:
[the ASI from the previous judge round — omit on iteration 0]

ITERATION HISTORY:
[condensed trajectory: iteration number, scores, config, key change for each
 prior iteration — omit on iteration 0]

EXPLORATION STATUS:
[from reflect: what's been tried vs untried in the search space — omit on
 iteration 0 or if no search space specified]

Interpret the evaluator output alongside the criteria.
Check evaluator output against the output contract if specified.
Score this candidate using the seed as a calibration reference.
Use the iteration history, previous ASI, and exploration status to inform
your ASI — analyze what's been tried, what worked, what didn't, and propose
an evidence-based direction. You may research approaches if the current
path is stuck.
```

**Step 4: Reflect (inline, load subskill)**

Invoke `simmer:simmer-reflect`.

Provide: full score history across all iterations so far, current iteration number, max iterations, judge output from this round.

**After reflect completes, display the updated trajectory table to the user.** Show the full table so far — the user should see scores accumulate row by row as the loop runs. This is especially important during long evaluator runs where the user otherwise sees nothing for 10-15 minutes per iteration.

```
Iteration 2 complete.

| Iter | Value Prop | Tone | CTA | Composite | Key Change |
|------|-----------|------|-----|-----------|------------|
| 0    | 4         | 5    | 3   | 4.0       | seed       |
| 1    | 7         | 5    | 4   | 5.3       | specific problem statement |
| 2    | 7         | 6    | 6   | 6.3       | low-friction CTA |

Best so far: iteration 2 (6.3/10). 1 iteration remaining.
```

**Handling regression:** If reflect reports that this iteration scored lower than best-so-far:
- *Single-file:* the NEXT generator receives the best candidate file (not the latest regressed one)
- *Workspace:* selectively restore workspace files from the best iteration's commit: `git checkout <best-commit> -- <workspace-files>`. Do NOT revert trajectory.md or other tracking files in `{OUTPUT_DIR}`.
- The generator prompt should note: "Starting from the best version (iteration N), not the latest (which regressed)."

**Plateau detection:** If the best-so-far score (primary criterion if set, otherwise composite) has not improved for 3 consecutive iterations — including regressions that were rolled back:

- **If currently using single judge (`JUDGE_MODE: single`):** Offer upgrade: "Best score has not improved for 3 iterations (best: N.N/10 at iteration M). Switch to judge board for deeper diagnosis, or stop?" If the user accepts the upgrade, switch to `JUDGE_MODE: board` and add 2 iterations to the remaining count (the board typically needs 2-3 iterations to surface and act on new insights). The board's multi-perspective deliberation often surfaces blind spots the single judge missed.

- **If already using board:** Offer early termination: "Best score has not improved for 3 iterations with the judge board (best: N.N/10 at iteration M). Continue or stop?"

This catches both flat plateaus and oscillation around a ceiling. Especially important when evaluator runs are expensive (minutes to hours per iteration).

### Phase 3: Output

After all iterations complete:

*Single-file mode:*
1. Write best-scoring candidate to `{OUTPUT_DIR}/result.md`
2. Display full trajectory table
3. Summarize what changed from start to finish (2-3 sentences)
4. Offer: "N iterations complete. Run 3 more?"

*Workspace mode:*
1. Ensure workspace is on the best iteration's state
2. Display full trajectory table
3. Summarize what changed from start to finish (2-3 sentences)
4. Offer: "N iterations complete. Run 3 more?"

If user continues: carry forward best candidate as new seed, continue iteration numbering (e.g., iterations 4, 5, 6), run 3 more.

## Directory Structure

**Single-file mode:**
```
{OUTPUT_DIR}/
  iteration-0-candidate.md     # Seed (or seedless first generation)
  iteration-1-candidate.md     # Each improved candidate
  iteration-2-candidate.md
  iteration-3-candidate.md
  trajectory.md                # Running score table
  result.md                    # Final best output
```

**Workspace mode:**
```
{WORKSPACE}/                    # The target directory
  [project files]               # Modified in place by generator

{OUTPUT_DIR}/                   # Tracking files (can be inside or outside workspace)
  trajectory.md                 # Running score table
```

Iterations are tracked via git commits in workspace mode rather than separate candidate files.

`{OUTPUT_DIR}` defaults to `docs/simmer`. Override via setup brief's `OUTPUT_DIR` field.

## Single-Agent Mode

If you cannot dispatch separate subagents (e.g., nested Claude sessions are blocked, or you're running in a constrained environment), execute all roles sequentially.

**Context discipline is aspirational in single-agent mode.** You will see prior scores and evaluator output. Mitigate bias by:
- (a) Writing your judge scores BEFORE reading your previous trajectory
- (b) Scoring against the criterion descriptions and seed reference, not against your memory of prior scores
- (c) In the generator step, work from the ASI text only — do not reference raw evaluator metrics or output. If the ASI is well-written (specific, citing concrete failures), it already contains the signal you need.

**Per-iteration checklist (single-agent):**
1. **GENERATOR**: Review the simmer-generator constraints (especially what context you receive and do NOT receive). Read ASI + current best candidate + background. Write improved version.
2. **RUN EVALUATOR**: If evaluator command exists, run it and capture output.
3. **JUDGE**: Review the simmer-judge constraints (especially scoring rules, seed calibration, and ASI format). Score against criteria + seed reference + evaluator output (if any). Write scores in required format.
4. **REFLECT**: Update `{OUTPUT_DIR}/trajectory.md`. Note best-so-far. If regression, flag it and roll back to best candidate. Skip the formal "output to orchestrator" block — just update the file and continue.

## Context Discipline

**This is critical for consistent results:**

| Subskill | Receives | Does NOT receive |
|----------|----------|------------------|
| Generator | Current candidate, criteria, ASI from last judge, background, exploration status | Score history, previous candidates, evaluator output |
| Judge (text/creative) | Current candidate, criteria, iteration number, seed + seed scores | Intermediate scores, intermediate candidates, previous ASI, trajectory |
| Judge (code/pipeline) | Current candidate, criteria, iteration number, seed + seed scores, evaluator output, previous ASI, iteration history, search space, exploration status | Full candidate history |
| Judge Board | Same as single judge per problem class, plus: other panelists' scores during deliberation | Other panelists' ASI candidates (withheld until synthesis) |
| Reflect | Full score history, all iteration summaries, search space | Candidate content (just scores + summaries) |

The generator improves based on specific feedback (ASI) and available resources (background), not scores.
The judge scores against criteria definitions, evaluator output, and the seed as a fixed calibration reference — no intermediate scores.
The judge board preserves these same rules per panelist — deliberation adds within-iteration cross-judge visibility only, no new cross-iteration information.
The reflect subskill is the only one that sees the full trajectory.

## Skill Dependencies

| Dependency | Usage |
|------------|-------|
| `parallel-agents` | `superpowers:dispatching-parallel-agents` — fallback: dispatch sequentially |

## Common Mistakes

**Giving the generator score history**
- Problem: Generator optimizes for scores instead of addressing the specific ASI
- Fix: Generator only sees current candidate + ASI + criteria + background

**Giving the judge previous scores**
- Problem: Anchoring — judge calibrates relative to prior scores instead of fresh
- Fix: Judge only sees current candidate + criteria + evaluator output

**Trying to fix everything at once (single-file mode)**
- Problem: Generator makes scattered edits, regression on some criteria
- Fix: ASI is a single focused fix — focused improvement compounds

**Treating ASI as always single-edit (workspace mode)**
- Problem: Generator makes one tiny change when the ASI calls for a coordinated move
- Fix: In workspace mode, ASI describes a single *direction* which may involve coordinated changes across files

**Sharing candidate history with the judge**
- Problem: Judge compares to previous versions instead of scoring against criteria
- Fix: Judge sees only the current candidate

**Not tracking best candidate separately**
- Problem: Last iteration may not be the best
- Fix: Reflect tracks best-scoring candidate across all iterations

**Not rolling back on regression (workspace mode)**
- Problem: Generator builds on a regressed state instead of the best state
- Fix: Selectively restore workspace files: `git checkout <best-commit> -- <files>`. Do NOT revert trajectory.md.

**Dual-writing embedded artifacts**
- Problem: Artifact is embedded in a larger system (prompt inside a script, config inside YAML) requiring updates in two places
- Fix: Design evaluators to read from the canonical candidate file rather than requiring dual writes. Pass the artifact path as input to the evaluator script.

**Reverting trajectory on git rollback (workspace mode)**
- Problem: `git checkout <commit>` reverts ALL files including trajectory.md tracking
- Fix: Always use selective checkout: `git checkout <commit> -- file1 file2`. Keep trajectory.md and other tracking files outside the rollback scope.

## Example Flow: Single-File (v1 behavior)

```
User: "Simmer this" [pastes a pitch email]

Claude: I'm using the simmer skill to set up iterative refinement.

[Invokes simmer-setup]

Setup identifies: pitch email, suggests criteria
User accepts: value prop clarity, tone match, call to action strength
Iterations: 3

[Iteration 0: Judge scores seed — 4.0/10]
[Iteration 1: Generator fixes value prop → 5.3/10]
[Iteration 2: Generator fixes CTA → 6.3/10]
[Iteration 3: Generator fixes tone → 7.3/10]

Trajectory:
| Iter | Value Prop | Tone | CTA | Composite | Key Change |
|------|-----------|------|-----|-----------|------------|
| 0    | 4         | 5    | 3   | 4.0       | seed       |
| 1    | 7         | 5    | 4   | 5.3       | specific problem statement |
| 2    | 7         | 6    | 6   | 6.3       | lower-friction CTA |
| 3    | 7         | 7    | 8   | 7.3       | specific asset in CTA |

Best candidate: iteration 3 (7.3/10)
3 iterations complete. Run 3 more?
```

## Example Flow: Workspace with Evaluator

```
User: "Simmer this pipeline — find the best model and prompt setup"

Claude: I'm using the simmer skill to set up iterative refinement.

[Invokes simmer-setup]

Setup identifies: workspace at ./pipeline/
Evaluator: python evaluate.py --input output.json
Background: "Available models: claude-sonnet, gpt-4o-mini, llama-8b, llama-70b.
            Topologies: single-call, multi-step chain, parallel fan-out.
            Budget: <$0.01/call, <2s latency."
Criteria: accuracy, cost efficiency, latency
Iterations: 5

[Iteration 0: Run evaluator on seed, judge scores — 3.7/10]
  accuracy: 6/10, cost: 2/10, latency: 3/10
  ASI: "Using claude-sonnet for a simple extraction task. The model is
       overkill — accuracy is fine but cost is 5x over budget. Switch to
       gpt-4o-mini which handles extraction well at 1/10th the cost."

[Iteration 1: Generator swaps model + adjusts prompt → 5.3/10]
  accuracy: 5/10, cost: 8/10, latency: 7/10
  ASI: "Cost and latency are great now but accuracy dropped on multi-step
       reasoning tasks (cases 7, 12). Split into two calls — extraction
       on mini, reasoning on sonnet — to get accuracy back without
       blowing the budget."

[Iteration 2: Generator restructures to 2-step chain → 7.0/10]
  accuracy: 7/10, cost: 7/10, latency: 7/10
  ASI: "Architecture is solid. The extraction prompt is too generic —
       add 3 few-shot examples from the test cases to anchor the format."

[Iteration 3: Generator adds few-shot examples → 7.7/10]
  ...

Best candidate: iteration 3 (7.7/10)
5 iterations complete. Run 3 more?
```
