---
name: evolve
description: Population-based evolutionary search for code optimization. Maintains k candidates, evaluates against a fitness function, selects survivors, breeds new candidates via LLM mutation and crossover until fitness converges.
args:
  - name: -k N
    description: Population size (default 4)
  - name: -g N
    description: Maximum generations (default 10)
  - name: -s N
    description: Stale generations before stopping (default 3)
  - name: --files <paths>
    description: Target files to evolve (prompted if omitted)
---

# Evolve

You don't find the best implementation by improving one. You find it by improving many and keeping the winners.

## Why This Works

Hill climbing improves a single candidate and hopes it's in the right basin. Evolutionary search maintains a population — multiple candidates exploring different regions of the solution space simultaneously. Selection keeps the best, mutation explores nearby, crossover combines good ideas, and fresh random prevents the population from collapsing to a local optimum.

LLMs make vastly better mutation operators than random perturbation. They understand code semantics, so mutations are meaningful — not "flip a bit" but "swap the sorting algorithm" or "add a caching layer." This turns evolutionary search from brute force into intelligent exploration.

## Relationship to Existing Skills

| Aspect         | `loop-codex-review`       | `spike`              | `evolve`                       |
| -------------- | ------------------------- | -------------------- | ------------------------------ |
| **Candidates** | 1 (hill climbing)         | N (one-shot)         | k per generation (iterated)    |
| **Fitness**    | Binary (clean/issues)     | Human judgment       | Quantitative (scalar score)    |
| **Iteration**  | Review-fix loop           | None                 | Generational selection         |
| **Selection**  | Single candidate improves | Human picks winner   | Automated: keep top ceil(k/2)  |
| **Mutation**   | Fix reviewer issues       | N/A                  | LLM rewrite toward objective   |
| **Good for**   | Correctness, clarity      | Comparing approaches | Performance, optimization      |
| **Stops when** | No reviewer issues        | All branches built   | Fitness plateaus (convergence) |

## Core Concept

```
          ┌──────────┐
          │ Evaluate  │◄──────────────────────┐
          └────┬─────┘                        │
               │                              │
          ┌────▼─────┐                        │
          │  Select   │  keep top ceil(k/2)   │
          └────┬─────┘                        │
               │                              │
          ┌────▼─────┐                        │
          │  Report   │  HIL checkpoint       │
          └────┬─────┘                        │
               │                              │
          ┌────▼─────┐                        │
          │  Breed    │  mutation + crossover  │
          └────┬─────┘                        │
               │                              │
               └──────────────────────────────┘
```

- **Evaluate**: Run user's fitness command on each candidate (sequential checkout-and-run)
- **Select**: Rank by fitness, keep the best, delete the rest
- **Report**: Present leaderboard to human, get approval to continue
- **Breed**: LLM agents produce new candidates via mutation, crossover, or fresh generation

## On Activation

1. **Initialize** — Parse args, validate fitness command, identify target files, evaluate baseline
2. **Seed** — Spawn k agents to create initial population (generation 1)
3. **Evaluate** — Run fitness on all candidates
4. **Select** — Keep top ceil(k/2), eliminate the rest
5. **Report** — Present leaderboard, get human decision
6. **Breed** — LLM agents produce new candidates to fill population back to k
7. **Loop** — Return to Evaluate (step 3)
8. **Converge** — When fitness plateaus or budget exhausted, present winner

## State Schema

Track in task description for compaction survival.

```yaml
# Parameters
target_files: []
fitness_cmd: ""
base_branch: ""
population_size: 4 # k
max_generations: 10
stale_limit: 3

# Current state
generation: 0
best_fitness: null
best_candidate: null
stale_count: 0
baseline_fitness: null

# Current population
candidates:
  - id: "gen1-1"
    branch: "evolve/gen1-1"
    fitness: 847
    parents: ["gen0-seed"]
    operator: "mutation"
    focus: "caching"
    status: "alive" # alive | eliminated | invalid

# Compact history (one line per generation)
history:
  - { gen: 0, best: 712, avg: 712 }
  - { gen: 1, best: 923, avg: 847 }
```

## Phase: Initialize

### Do:

- Parse args: fitness command (first positional), target files (`--files` or ask), population size (`-k`), max generations (`-g`), stale limit (`-s`)
- Validate fitness command: run it once, confirm it exits 0 and the last line of stdout parses as a number
- Record baseline fitness (the seed's score)
- Create seed branch: `git checkout -b evolve/gen0-seed`
- Create tracking task with full state schema

### Don't:

- ❌ Skip fitness validation — a broken fitness command wastes every subsequent generation
- ❌ Assume target files — always confirm with user if `--files` not provided
- ❌ Start breeding without a baseline — you need a reference point for improvement

### Fitness validation

```bash
output=$($FITNESS_CMD 2>&1)
exit_code=$?

if [ $exit_code -ne 0 ]; then
    echo "Fitness command failed (exit $exit_code)"
    exit 1
fi

score=$(echo "$output" | tail -1)
echo "$score" | grep -qE '^-?[0-9]+\.?[0-9]*$'
```

### Args examples

```bash
/evolve "python benchmark.py"                    # Ask for target files
/evolve "make bench" --files src/solver.rs       # Explicit target
/evolve "./test.sh | tail -1" -k 6 -g 20        # Larger population
```

## Phase: Seed (Generation 1)

**First generation only.** Creates the initial population from the seed.

### Do:

- Spawn k agents in parallel (`run_in_background: true`)
- Each agent gets: target file contents, fitness objective, baseline fitness score
- Each agent writes its variant to a new branch (`evolve/gen1-{id}`)
- Assign each agent a different **focus lens** to force diversity

### Don't:

- ❌ Let all agents optimize the same way — enforce diversity via focus directives
- ❌ Run agents sequentially — they're independent, always parallel
- ❌ Skip the focus lens — without it, agents converge to the same "obvious" optimization

### Focus Lenses

Each seed agent gets one lens — a constraint that forces it to explore a different region of the solution space. **Choose lenses appropriate to the user's objective.** The lenses below are examples, not an exhaustive list.

| Objective domain   | Example lenses                                                    |
| ------------------ | ----------------------------------------------------------------- |
| Performance        | Algorithm, data structure, caching, loop structure, parallelism   |
| Accuracy / quality | Algorithm, error handling, edge cases, validation, representation |
| Size / simplicity  | Elimination, decomposition, alternative libraries, rewrite        |
| Robustness         | Error paths, input validation, retry strategy, fallback design    |
| General (any)      | Algorithm, data structure, simplification, inversion              |

The key requirement: lenses must be **genuinely different axes**, not variations on a theme. With k=4, pick 4 lenses spanning the widest range. With k > 8, lenses may repeat.

### Agent prompt template (seed)

```
You are optimizing code for the following objective:
[user's description / fitness command explanation]

Baseline fitness: [score]. Higher = better.
The fitness function is: [command]

Here are the target files:
[file contents]

Your focus: **[lens]**. Approach the problem primarily through [lens description].

Write the complete modified file(s). Do not stub or TODO — the code
must be functional. You may make multiple changes, but your primary
axis of variation should be [lens].
```

Each agent:

1. Checks out `evolve/gen0-seed`
2. Creates branch `evolve/gen1-{id}`
3. Writes modified files
4. Commits: `"evolve: gen1-{id} (seed, focus: {lens})"`

## Phase: Evaluate

### Do:

- For each candidate branch (sequentially):
  1. `git checkout evolve/gen{N}-{id}`
  2. Run fitness command
  3. Record score (last line of stdout, parsed as number)
  4. Record exit code (non-zero = invalid, fitness = -infinity)
- Return to base branch after all evaluations
- Update state with all fitness scores

### Don't:

- ❌ Evaluate in parallel without worktrees — concurrent checkouts corrupt the working tree
- ❌ Skip invalid candidates silently — report them in the leaderboard as "INVALID"
- ❌ Discard invalid candidates before selection — they're data (the mutation broke something)

### Evaluation loop

```bash
git checkout "$BRANCH"
output=$($FITNESS_CMD 2>&1)
exit_code=$?

if [ $exit_code -eq 0 ]; then
    score=$(echo "$output" | tail -1)
else
    score="-inf"
fi

git checkout "$BASE_BRANCH"
```

## Phase: Select

### Do:

- Sort candidates by fitness (descending)
- Keep top ceil(k/2) as survivors
- Delete eliminated branches immediately (`git branch -D evolve/gen{N}-{id}`)
- Record lineage of survivors in state

### Don't:

- ❌ Keep all branches — branch sprawl makes the repo unnavigable
- ❌ Delete branches before recording their fitness in state — the history is valuable
- ❌ Keep invalid candidates unless they're the only ones left (warn the user)

### Selection example (k=4)

```
Candidates sorted by fitness:
  gen2-3: 923 (mutation)    ← KEEP
  gen2-1: 889 (crossover)   ← KEEP
  gen2-2: 847 (mutation)    ← ELIMINATE
  gen2-4: 801 (fresh)       ← ELIMINATE

Survivors: gen2-3, gen2-1
Eliminated: gen2-2, gen2-4 (branches deleted)
```

## Phase: Report (HIL)

### Do:

- Present leaderboard with fitness, parentage, operator, delta from baseline
- Show fitness trend across generations (compact table)
- Show stale counter (N/stale_limit)
- Use `AskUserQuestion` with clear options

### Don't:

- ❌ Skip this checkpoint — human oversight is mandatory
- ❌ Present raw numbers without context — always show delta from baseline and trend
- ❌ Auto-continue without asking — the human decides

### Leaderboard format

```markdown
## Generation {N} Results

### Leaderboard

| Rank | Candidate | Fitness | Delta Baseline | Parents        | Operator           |
| ---- | --------- | ------- | -------------- | -------------- | ------------------ |
| 1    | gen3-2    | 1,089   | +377           | gen2-3         | mutation (loop)    |
| 2    | gen3-1    | 1,012   | +300           | gen2-3, gen2-1 | crossover          |
| 3    | gen3-3    | 956     | +244           | gen2-1         | mutation (caching) |
| 4    | gen3-4    | 823     | +111           | seed           | fresh              |

### Trend

| Gen | Best  | Avg | Delta Best |
| --- | ----- | --- | ---------- |
| 0   | 712   | 712 | --         |
| 1   | 923   | 847 | +211       |
| 2   | 978   | 901 | +55        |
| 3   | 1,089 | 970 | +111       |

Stale: 0/3. Best ever: 1,089 (gen3-2).
```

### Options

```
AskUserQuestion:
1. "Continue" (Recommended) — Breed next generation
2. "Inspect winner" — Show diff of best candidate vs seed
3. "Adjust parameters" — Change k, stale_limit, or mutation strategy
4. "Stop and keep winner" — Apply best candidate
5. "Stop and discard" — Delete all evolve branches, return to base
```

## Phase: Breed

### Do:

- Determine how many new candidates needed: `k - ceil(k/2)`
- Assign operators: ~50% point mutation, ~25% crossover, ~25% fresh random
- Spawn agents in parallel (`run_in_background: true`), one per new candidate
- Each agent creates a new branch (`evolve/gen{N+1}-{id}`) from its parent
- Wait for all agents to complete before proceeding to Evaluate

### Don't:

- ❌ Run agents sequentially — they're independent
- ❌ Use the same focus lens for all point mutations — diversify
- ❌ Skip fresh random candidates — they prevent population collapse
- ❌ Show agents the full population — each agent sees only its parent(s)

### Operator assignment (k=4, 2 survivors, 2 new slots)

| Slot  | Operator                              | Parents               | Focus             |
| ----- | ------------------------------------- | --------------------- | ----------------- |
| New 1 | Point mutation                        | Best survivor         | Randomly selected |
| New 2 | Crossover OR Fresh random (alternate) | Both survivors / Seed | --                |

### Operator assignment (k=6, 3 survivors, 3 new slots)

| Slot  | Operator       | Parents         | Focus       |
| ----- | -------------- | --------------- | ----------- |
| New 1 | Point mutation | Best survivor   | Random lens |
| New 2 | Crossover      | Top 2 survivors | --          |
| New 3 | Fresh random   | Seed only       | --          |

### Point mutation prompt

```
You are optimizing code for: [objective]

Current implementation (fitness [score]):
[code]

Best known fitness: [best_score].
The fitness function is: [command]. Higher = better.

Make ONE meaningful change to improve fitness.
Focus on: **[randomly selected lens]**.

Do not rewrite from scratch. Make a targeted modification.
Output the complete modified file(s).
```

### Crossover prompt

```
You are combining two implementations that both optimize for: [objective]

Parent A (fitness [score_a]):
[code_a]

Parent B (fitness [score_b]):
[code_b]

The fitness function is: [command]. Higher = better.

Combine the best ideas from both parents into a single implementation.
Do not simply pick one parent. Identify what each does well and synthesize.
Output the complete merged file(s).
```

### Fresh random prompt

```
You are writing code to optimize: [objective]

The fitness function is: [command]. Higher = better.
Current best fitness: [best_score].

Here is the original (unoptimized) starting point for reference:
[seed code]

Write a completely new implementation. Do NOT modify the original —
start from first principles. Use a different algorithm, different
data structures, or a fundamentally different approach.
Output the complete file(s).
```

## Phase: Converge

Triggered when any termination condition is met.

### Termination conditions

| Condition | Trigger                           | Message                                 |
| --------- | --------------------------------- | --------------------------------------- |
| Plateau   | `stale_count >= stale_limit`      | "Fitness plateaued for {N} generations" |
| Budget    | `generation >= max_generations`   | "Maximum generations reached"           |
| User stop | User chose "Stop and keep winner" | "Stopped by user"                       |

### Do:

- Present the winning candidate with full lineage
- Show diff of winner vs seed (`git diff evolve/gen0-seed..evolve/{winner}`)
- Show fitness curve (generation to best fitness)
- Use `AskUserQuestion` for final disposition

### Don't:

- ❌ Auto-merge the winner — always ask
- ❌ Delete branches before user confirms — they may want to inspect losers
- ❌ Skip the diff — the user needs to see what actually changed

### Final report

```markdown
## Evolution Complete

**Winner:** gen5-2 (fitness 1,247)
**Improvement:** +535 from baseline (+75%)
**Generations:** 5 (converged: plateau for 3 generations)
**Total candidates evaluated:** 20

### Lineage

gen0-seed (712)
→ gen1-2 (923, mutation/caching)
→ gen2-3 (978, mutation/loop)
→ gen3-2 (1,089, crossover)
→ gen5-2 (1,247, mutation/branch elimination)

### Fitness Curve

| Gen | Best  | Avg   | Delta Best |
| --- | ----- | ----- | ---------- |
| 0   | 712   | 712   | --         |
| 1   | 923   | 847   | +211       |
| 2   | 978   | 901   | +55        |
| 3   | 1,089 | 970   | +111       |
| 4   | 1,247 | 1,102 | +158       |
| 5   | 1,247 | 1,150 | 0          |
```

### Options

```
AskUserQuestion:
1. "Apply winner" (Recommended) — Merge winning branch to base, clean up
2. "Apply winner on new branch" — Create clean branch with winning code
3. "Keep all branches" — Leave everything for archaeology
4. "Discard all" — Delete all evolve/* branches, return to base
```

### Apply winner

```bash
git checkout $BASE_BRANCH
git merge evolve/$WINNER --no-ff -m "evolve: apply winner ($WINNER, fitness $SCORE)"
git branch -D $(git branch --list 'evolve/*')
```

## Fitness Function Contract

The fitness command must:

1. **Exit 0** on success. Non-zero = candidate is invalid (fitness = -infinity).
2. **Print a number as the last line of stdout.** Parsed as a float. Higher = better.
3. **Be deterministic enough to compare.** If stochastic, average multiple runs within the script.
4. **Run in the repo root.** Working directory is the repo root with the candidate's code checked out.

### Examples

```bash
# Performance: operations per second
./benchmark.sh

# Accuracy: correct predictions out of test set
python eval.py --dataset test.csv

# Test pass rate
make test 2>&1 | grep -oP '\d+ passed' | grep -oP '\d+'

# Lower-is-better metrics: negate so higher = better
echo "-$(./measure_latency.sh)"    # Latency
echo "-$(wc -c < solution.py)"     # Code size

# Multi-metric composite
python evaluate.py  # Script prints composite score as last line
```

## Branch Management

### Naming

`evolve/gen{N}-{id}` where N = generation, id = candidate number within generation.

Special: `evolve/gen0-seed` = the original code, unmodified. Never deleted until final cleanup.

### Lifecycle

```
Created (breed) → Evaluated → Alive or Eliminated
  Alive → survives to next generation (may become parent)
  Eliminated → branch deleted immediately after selection
```

### Branch count

At any moment: at most k (current population) + seed (1) = k+1 branches. Eliminated candidates are deleted eagerly.

## Resumption (Post-Compaction)

1. Run `TaskList` to find the evolve tracking task
2. Read task description for persisted state
3. Verify branches exist: `git branch --list 'evolve/*'`
4. Check for running background agents (breeding phase)
5. Resume from appropriate phase:
   - Breeding agents still running → wait, then Evaluate
   - Population has fitness but no selection → Select
   - Selection done, no breeding yet → Report or Breed
   - Unclear → re-evaluate current population

## Anti-patterns

- **Optimizing without a fitness function** — "Make it faster" is not measurable. Require a command that produces a number.
- **k=1** — That's hill climbing, not evolution. Use `loop-codex-review` instead.
- **Evaluating in parallel without isolation** — Concurrent checkouts corrupt the working tree. Sequential or worktrees only.
- **Keeping all branches** — 40 branches after 10 generations is unnavigable. Eliminate eagerly.
- **Same focus lens for all mutations** — Population converges to a single approach. Diversify.
- **Skipping fresh random** — Without new genetic material, the population collapses to a local optimum.
- **Breeding before evaluating** — Selection requires fitness scores. Always evaluate first.
- **Auto-merging the winner** — The human must approve. Best-by-fitness may have unacceptable trade-offs.

## Quick Reference: Don'ts

| Phase      | Don't                                                                      |
| ---------- | -------------------------------------------------------------------------- |
| Initialize | Skip fitness validation, assume target files, start without baseline       |
| Seed       | Same focus for all agents, run sequentially, skip focus lens               |
| Evaluate   | Parallel without worktrees, skip invalid candidates, discard before select |
| Select     | Keep all branches, delete before recording fitness                         |
| Report     | Skip HIL, present without trend context, auto-continue                     |
| Breed      | Run sequentially, same lens for mutations, skip fresh random               |
| Converge   | Auto-merge, delete before user confirms, skip the diff                     |

---

Begin evolve now. Parse args for fitness command (first positional), target files (`--files` or ask), population size (`-k`, default 4), max generations (`-g`, default 10), and stale limit (`-s`, default 3). Validate the fitness command produces a number. Evaluate baseline fitness on current code. Then create the initial population with k diverse agents, each with a different focus lens. Enter the evolutionary loop: Evaluate → Select → Report → Breed → repeat. Present the leaderboard to the human after each generation.
