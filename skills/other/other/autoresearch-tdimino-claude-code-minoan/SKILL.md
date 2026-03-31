---
name: autoresearch
description: >-
  Scaffold and run Karpathy-style autoresearch loops in any git repo.
  This skill should be used when setting up autonomous code improvement,
  generating adversarial eval harnesses, running hypothesis-implement-eval-keep/discard
  loops, or checking autoresearch progress. Triggers on "autoresearch",
  "autonomous improvement", "eval loop", "hypothesis loop", "self-improvement loop".
argument-hint: [init|eval-gen|run|status|resume]
---

<critical>

## Five Invariants (never violate)

1. **Single mutable surface** — one hypothesis per iteration, one change per experiment
2. **Fixed eval budget** — eval runs in bounded time, no network calls in gates
3. **One scalar metric** — composite score drives keep/discard, not vibes
4. **Binary keep/discard** — improved = keep, else revert `git reset --hard HEAD~1`
5. **Git-as-memory** — every experiment is a commit, discards are reverts, history is the log

## Safety rules

- Never modify `.lab/` contents during hypothesis implementation
- Never skip eval — every commit must be evaluated before keep/discard
- Always revert on crash — `atexit` handler restores git state
- Runner uses **subscription auth** (`claude -p` with ANTHROPIC_API_KEY stripped)

</critical>

# Autoresearch

Scaffold and run autonomous code improvement loops in any git repo. The pattern: generate a hypothesis via `claude -p`, implement it, run programmatic eval gates, keep if the composite score improves, discard if it doesn't. Proven across 50+ iterations on two codebases (shadow-engine: 0.69 to 1.0, perplexity-clone: search quality optimization).

## Category

**Runbooks** — mechanical process with clear steps, not cognitive reasoning.

## Quick Start

```
/autoresearch init          # scaffold .lab/ in your repo
/autoresearch run           # start the loop (default: 50 iterations)
/autoresearch status        # check progress
/autoresearch resume        # recover interrupted run
```

## Command Dispatch

Parse `$ARGUMENTS` and route:

| Argument | Action |
|----------|--------|
| `init` | Run scaffold workflow (see Init below) |
| `eval-gen` | Regenerate eval gates from repo analysis |
| `run [--max-iterations N] [--dry-run]` | Launch the autoresearch loop |
| `status` | Show composite, timeline, convergence signals |
| `resume` | Detect `.lab/`, present state, ask resume or fresh |
| *(empty)* | Show help text with available commands |

---

## Init Workflow (`/autoresearch init`)

1. Verify `.git/` exists in current directory
2. Run stack detection:
   ```bash
   python3 ~/.claude/skills/autoresearch/scripts/detect_stack.py
   ```
3. Review the detected stack info (language, build_cmd, test_cmd, lint_cmd)
4. Run the scaffold script:
   ```bash
   python3 ~/.claude/skills/autoresearch/scripts/scaffold.py --repo-root . --yes
   ```
5. Review `.lab/config.json` — adjust `keep_threshold`, `max_iterations`, `gate_weights` if needed
6. Edit `.lab/program.md` — this is the most important file. Add:
   - Specific areas to improve (not vague goals)
   - Concrete hypothesis list (ranked)
   - Constraints the agent must respect
7. Run baseline eval to verify gates work:
   ```bash
   python3 .lab/eval.py
   ```
8. Report the initial composite to the user

**If `.lab/` already exists**, ask the user: resume existing lab, or archive to `.lab.bak.<timestamp>/` and start fresh?

## Eval-Gen Workflow (`/autoresearch eval-gen`)

Regenerate eval gates without re-scaffolding everything:

```bash
python3 ~/.claude/skills/autoresearch/scripts/eval_gen.py --repo-root . --output .lab/eval.py
```

Review the generated gates. The user may want to:
- Add custom gates for domain-specific behavior
- Adjust tier weights in `.lab/config.json`
- Add behavioral gates that test specific CLI invocations or API endpoints

Gates follow a 4-tier architecture:

| Tier | Weight | What it measures | Anti-cheat |
|------|--------|-----------------|------------|
| T1: Build+Test | 0.20 | Compiles, tests pass, lint clean | Runs real commands, sums pass counts |
| T2: Behavioral | 0.40 | Integration tests, CLI output, API responses | Validates content, not file existence |
| T3: Pipeline | 0.25 | Build artifacts, installs, real I/O | File size >1KB, header validation |
| T4: Documentation | 0.15 | Test count floor, doc coverage | Counts code, never trusts comments |

## Run Workflow (`/autoresearch run`)

```bash
python3 .lab/runner.py --max-iterations 50
```

Or for a dry run (prints hypothesis, creates no files):
```bash
python3 .lab/runner.py --dry-run --max-iterations 1
```

**Monitor progress** in a separate terminal:
```bash
tail -f .lab/results.tsv
```

The runner:
1. Loads config from `.lab/config.json`
2. Reads program.md for constraints and hypothesis direction
3. Creates an `autoresearch/{date}` branch
4. Loops: hypothesis via `claude -p` -> implement via `claude -p` -> git commit -> eval -> keep/discard
5. Logs every experiment to `.lab/results.tsv` with extended statuses:

| Status | Meaning |
|--------|---------|
| `KEEP` | Composite improved >= keep_threshold |
| `KEEP*` | Primary improved but secondary metric regressed |
| `DISCARD` | No improvement, reverted |
| `INTERESTING` | Negative result that reveals structure, logged to dead-ends |
| `CRASH` | Eval infrastructure failure, reverted |
| `TIMEOUT` | Experiment exceeded timeout, logged as crash |

6. Checks 9 convergence signals after each experiment (see `references/convergence-signals.md`)
7. Re-validates baseline every 10 real experiments
8. Auto-generates `.lab/eval-report.md` with cumulative progress

## Status Workflow (`/autoresearch status`)

```bash
python3 ~/.claude/skills/autoresearch/scripts/report.py --repo-root .
```

Shows: composite (live), experiment timeline, keeps/discards/crashes, active convergence signals, branch genealogy, dead-ends.

## Resume Workflow (`/autoresearch resume`)

1. Check if `.lab/` exists
2. If yes: read `config.json`, `results.tsv`, tail of `log.md`
3. Present summary: objective, metrics, experiment count, current best vs baseline, last status
4. Ask: **resume** (continue from last experiment) or **fresh** (archive `.lab.bak.<timestamp>/`)
5. If resume: check for stale lock file, clean up if needed, then run

## .lab/ Directory Layout

```
.lab/                          # gitignored — experiment knowledge store
  config.json                # All parameters (repo_name, build_cmd, keep_threshold, etc.)
  runner.py                  # Customized runner (from runner_template.py)
  eval.py                    # Generated + user-extended eval gates
  eval_base.py               # Base framework (gate registration, composite scoring)
  program.md                 # Human-maintained constraints + priorities
  results.tsv                # Experiment log (experiment_id, branch, parent, commit,
                             #   composite, status, duration_s, description)
  log.md                     # Narrative per-experiment entries
  branches.md                # Branch registry
  dead-ends.md               # Falsified approaches + why they failed
  parking-lot.md             # Deferred ideas for later
  eval-report.md             # Auto-generated cumulative report
  runner-*.log               # Runner stdout/stderr logs
  .runner.lock               # PID lock file (prevents concurrent runs)
```

**Why `.lab/` not `autoresearch/`**: Code state (git) and experiment knowledge (`.lab/`) are fully decoupled. `git reset --hard HEAD~1` (the core discard mechanic) never touches `.lab/`. Results survive branch operations.

## Three-Tier Output Protocol

Eval gates emit structured diagnostics to stderr:

```
GATE build=PASS              # Binary — blocks iteration on FAIL
METRIC test_count=475        # Continuous — tracked in results.tsv
TRACE gate_duration_ms=3200  # Execution data — for debugging only
```

## Scripts Reference

| Script | Purpose | Run from |
|--------|---------|----------|
| `scripts/detect_stack.py` | Detect language, build system, test runner | Skill dir |
| `scripts/scaffold.py` | Create `.lab/` with all files | Skill dir |
| `scripts/eval_gen.py` | Generate adversarial eval gates | Skill dir |
| `scripts/report.py` | Render status report | Skill dir |
| `scripts/runner_template.py` | Template copied to `.lab/runner.py` | Skill dir |
| `assets/eval_base.py` | Base eval framework copied to `.lab/` | Skill dir |
| `assets/config.json.tmpl` | Config template with documented fields | Skill dir |
| `assets/program.md.tmpl` | Program.md template | Skill dir |

All scripts run with `python3` (no special dependencies). Use `uv run` if preferred.

## Gotchas

- **`ANTHROPIC_API_KEY` in environment**: The runner strips it so `claude -p` uses subscription auth (not pay-per-use API). If you want API auth, set `use_api_key: true` in config.json.
- **Gate stochasticity**: If gates produce different scores on the same code, the runner will thrash between keep/discard. All gates must be deterministic.
- **Large dt on resume**: If the machine suspends during a run, the runner handles it gracefully via atexit + lock file cleanup.
- **Eval crashes vs gate crashes**: An eval crash (eval.py itself fails) aborts the iteration. A gate crash (one gate throws) is logged in `crashed_gates` and excluded from composite.

<critical>

## Post-Run Checklist

After every autoresearch run:

1. `tail -f .lab/results.tsv` — review keeps/discards
2. Read `.lab/eval-report.md` for cumulative progress and ceiling detection
3. Merge the autoresearch branch to main if satisfied
4. Update `.lab/program.md` dead ends with falsified approaches
5. Run `python3 .lab/eval.py` to confirm final composite

## Never

- Never modify `.lab/eval_base.py` or `.lab/runner.py` during a run
- Never run two runners concurrently (lock file prevents this, but don't bypass)
- Never commit `.lab/` to git (it's gitignored for a reason)
- Never trust a composite that includes crashed gates

</critical>
