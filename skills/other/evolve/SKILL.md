---
name: evolve
description: Run autonomous improvement loops.
practices:
- lean-startup
- dora-metrics
- agile-manifesto
hexagonal_role: supporting
consumes:
- rpi
- goals
- post-mortem
- compile
produces:
- git-changes
- goals-fitness-delta
context_rel:
- kind: customer-of
  with: rpi
skill_api_version: 1
user-invocable: true
context:
  window: fork
  intent:
    mode: task
  sections:
    exclude:
    - HISTORY
  intel_scope: full
metadata:
  tier: execution
  dependencies:
  - rpi
  - post-mortem
  - compile
  triggers:
  - evolve
  - improve everything
  - autonomous improvement
  - run until done
  - postmortem and continue
  - analyze repo and keep going
output_contract: code changes, GOALS.md fitness deltas
---
# /evolve — Goal-Driven Compounding Loop

> **Cross-vendor analog:** Anthropic Managed Agents Outcomes (May 2026). Both close the loop "agent runs → grader scores against a rubric → agent retries"; AgentOps does it locally against any model.

> Measure what's wrong. Fix the worst thing. Measure again. Compound.

**V2 command surface:** keep the name `evolve`. Use `ao evolve` for the
terminal-native loop. It is the top-level operator entrypoint for
`ao rpi loop --supervisor`, preserving the old `/evolve` concept while reusing
the v2 RPI loop engine.

**Operator cadence:** post-mortem finished work, analyze the current repo state,
select or create the next highest-value work item, let `/rpi` handle research,
planning, pre-mortem, implementation, and validation, then harvest follow-ups
and repeat until a kill switch, max-cycle cap, regression breaker, or real
dormancy stops the run.

Always-on autonomous loop over `/rpi`. Work selection order:
1. **Harvested `.agents/rpi/next-work.jsonl` work** (freshest concrete follow-up)
2. **Open ready beads work** (`bd ready`)
3. **Failing goals and directive gaps** (`ao goals measure`)
4. **Testing improvements** (missing/thin coverage, missing regression tests)
5. **Validation tightening and bug-hunt passes** (gates, audits, bug sweeps)
6. **Complexity / TODO / FIXME / drift / dead code / stale docs / stale research mining**
7. **Concrete feature suggestions** derived from repo purpose when no sharper work exists

**Work generators** that feed the selection ladder (auto-invoked, skip with `--no-lifecycle`):
- `Skill(skill="test", args="coverage")` → files with <40% coverage become queue items (Step 3.4)
- `Skill(skill="refactor", args="--sweep all --dry-run")` → functions with CC > 20 become queue items (Step 3.6)
- `Skill(skill="deps", args="audit")` → deps with CVSS >= 7.0 or 2+ major versions behind become queue items (Step 3.5)
- `Skill(skill="perf", args="profile --quick")` → perf findings become queue items when hot paths detected (Step 3.5)

**Dormancy is last resort.** Empty current queues mean "run the generator layers", not "stop". Only go dormant after the queue layers and generator layers come up empty across multiple consecutive passes.

```bash
/evolve                      # Run until kill switch, max-cycles, or real dormancy
/evolve --max-cycles=5       # Cap at 5 cycles
/evolve --dry-run            # Show what would be worked on, don't execute
/evolve --beads-only         # Skip goals measurement, work beads backlog only
/evolve --quality            # Quality-first mode: prioritize post-mortem findings
/evolve --quality --max-cycles=10  # Quality mode with cycle cap
/evolve --compile            # Mine → Defrag warmup before first cycle
/evolve --compile --max-cycles=5 # Warm knowledge base then run 5 cycles
/evolve --test-first         # Default strict-quality /rpi execution path
/evolve --no-test-first      # Explicit opt-out from test-first mode
```

## Delineation vs /dream

| Lane | Runs | Mutates code? | Mutates corpus? | Outer loop? | Budget |
|------|------|---------------|-----------------|-------------|--------|
| `/dream` | nightly, private local | **No** | **Yes (heavy)** | **Yes (convergence)** | wall-clock + plateau |
| `/evolve` | daytime, operator-driven | Yes (via `/rpi`) | Yes (light) | Yes | cycle cap |

Dream owns the knowledge compounding layer; `/evolve` owns the code compounding layer. Both share fitness-measurement substrate via `corpus.Compute` / `ao goals measure`. Run Dream overnight, then start each day with `/evolve` against the freshly-compounded corpus with a clean fitness baseline.

## Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--max-cycles=N` | unlimited | Stop after `N` completed cycles |
| `--dry-run` | off | Show planned cycle actions without executing |
| `--beads-only` | off | Skip goal measurement and run backlog-only selection |
| `--skip-baseline` | off | Skip first-run baseline snapshot |
| `--quality` | off | Prioritize harvested post-mortem findings |
| `--compile` | off | Run `ao mine` + `ao defrag` warmup before cycle 1 |
| `--test-first` | on | Pass strict-quality defaults through to `/rpi` |
| `--no-test-first` | off | Explicitly disable test-first passthrough to `/rpi` |
| `--no-lifecycle` | off | Skip lifecycle work generators in Steps 3.4-3.6 (/test, /deps, /perf, /refactor). Falls back to manual scanning. |
| `--mode=burst\|loop` | burst | Operator-loop; STOP refused. [loop-mode.md](references/loop-mode.md). |

## Execution Steps

**YOU MUST EXECUTE THIS WORKFLOW. Do not just describe it.**

**FULLY AUTONOMOUS.** Read `references/autonomous-execution.md`. Every `/rpi` uses `--auto`. Do NOT ask the user anything. Each cycle = complete 3-phase `/rpi` run.

For broad AgentOps 3.0 domain evolution across skills, CLI, hooks, docs, tests,
beads, and knowledge, first read
[references/domain-evolution-bootstrap.md](references/domain-evolution-bootstrap.md).
It supplies the BDD/DDD/Hexagonal/TDD/XP control surface and the clean-room
skill-factory guardrails.

### Step 0: Setup

```bash
mkdir -p .agents/evolve
ao corpus inject --query "autonomous improvement cycle" --limit 5 2>/dev/null || true
bash scripts/evolve-update-session-state.sh 2>/dev/null || true  # refresh derived idle_streak + mode_repeat_streak
```

`ao corpus inject` routes through the typed BC1 `CorpusReaderPort`
(`cli/cmd/ao/corpus_reader_adapter.go`, cycle 112 productionCorpusReader),
emitting one ranked `ports.CorpusItem` JSON record per line from
`.agents/learnings/` by default. This closes soc-y5vh.1 — Step 0 prior-knowledge
retrieval is now load-bearing on the typed port, not an untyped `ao lookup`
shell-out.

**Apply retrieved knowledge:** If learnings are returned, check each for applicability to the current improvement cycle. For applicable learnings, cite by filename and record: `ao metrics cite "<path>" --type applied 2>/dev/null || true`

**Prior-failure injection (mandatory):** read the last 3 entries of `.agents/evolve/cycle-history.jsonl`. For any with `gate` containing `FAIL|FAILED|BLOCKED`, extract failure-surface keywords (`registry|bats|markdown|supergate|canary|coverage|toolchain`) and search `.agents/learnings/` for matching learnings. Print the top matches before work selection. Without this read path, the loop accumulates write-only ledgers and re-derives lessons each cycle. See `references/convergence-mechanics.md` for the full recipe.

Before cycle recovery, load the repo execution profile contract when it exists. The repo execution profile is the source for repo policy; the user prompt should mostly supply mission/objective, not restate startup reads, validation bundle, tracker wrapper rules, or `definition_of_done`.

- Locate `docs/contracts/repo-execution-profile.md` and `docs/contracts/repo-execution-profile.schema.json`.
- Read the ordered `startup_reads` and bootstrap from those repo paths before selecting work.
- Cache repo `validation_commands`, `tracker_commands`, and `definition_of_done` into session state.
- If the repo execution profile is present but missing required fields, stop or downgrade with an explicit warning before cycle 1. Do not silently invent repo policy.
- Read operating-doctrine ADRs (`docs/adr/` or `docs/decisions/`) when present — intent the loop re-reads each cycle: only operator markers stop the loop; the bead queue is a hypothesis re-confirmed against the goal, not spec; file-a-bead when a candidate is architecture disguised as bounded work.

Then load the repo-local autodev program contract when it exists. The execution profile remains the repo bootstrap and landing-policy layer; `PROGRAM.md` or `AUTODEV.md` is the repo-local execution layer for the current improvement loop.

- Locate `PROGRAM.md` and `AUTODEV.md`. `PROGRAM.md` takes precedence.
- Read the resolved program before cycle recovery and cache `program_path`, `mutable_scope`, `immutable_scope`, `validation_commands`, `decision_policy`, and `stop_conditions` into session state.
- If the program file exists but is structurally invalid, stop or downgrade with an explicit warning before cycle 1. Do not silently ignore a broken operator contract.
- When a program contract exists, prefer work that can land wholly inside mutable scope. Do not silently widen scope around immutable files.

Recover cycle number, generator streaks, and the last claimed work item from disk (survives context compaction). Initialize `CYCLE` from `cycle-history.jsonl`, recover `IDLE_STREAK`, `GENERATOR_EMPTY_STREAK`, `LAST_SELECTED_SOURCE`, and `CLAIMED_WORK_REF` from `session-state.json`.

**Circuit breakers:** Time-based (60 min no productive work).

**Oscillation quarantine:** Pre-populate quarantine list from cycle history (scan for goals with 3+ improved-to-fail transitions). See `references/oscillation.md`.

Parse flags: `--max-cycles=N` (default unlimited), `--dry-run`, `--beads-only`, `--skip-baseline`, `--quality`, `--compile`.

Track cycle-level execution state:

```text
evolve_state = {
  cycle: <current cycle number>,
  mode: <standard|quality|beads-only>,
  test_first: <true by default; false only when --no-test-first>,
  repo_profile_path: <docs/contracts/repo-execution-profile.md or null>,
  startup_reads: <ordered repo bootstrap paths>,
  validation_commands: <ordered repo validation bundle>,
  tracker_commands: <repo tracker shell wrappers>,
  definition_of_done: <repo stop predicates>,
  program_path: <PROGRAM.md|AUTODEV.md or null>,
  program_mutable_scope: <declared mutable paths/globs>,
  program_immutable_scope: <declared immutable paths/globs>,
  program_validation_commands: <ordered program validation bundle>,
  program_decision_policy: <ordered keep/revert rules>,
  program_stop_conditions: <ordered cycle done criteria>,
  generator_empty_streak: <consecutive passes where all generator layers returned nothing>,
  last_selected_source: <harvested|beads|goal|directive|testing|validation|bug-hunt|drift|feature>,
  claimed_work: <null or work reference being worked>,
  queue_refresh_count: <incremented after every /rpi cycle>
}
```

Persist `evolve_state` to `.agents/evolve/session-state.json` at each cycle boundary, after work claims, after release/finalize, and during teardown. `cycle-history.jsonl` remains the canonical cycle ledger; `session-state.json` carries resume-only state that has not yet earned a committed cycle entry. Both files are **local-only** (the nested `.agents/.gitignore` denies all paths) — record durable milestones in commit messages too. See `references/cycle-history.md` for full local-only semantics.

### Step 0.2: Compile Warmup (--compile only)

Skip if `--compile` was not passed or if `--dry-run`. Read `references/knowledge-loop-integration.md` for the full warmup procedure (mine + defrag + signal notes).

### Step 0.5: Baseline (first run only)

Skip if `--skip-baseline` or `--beads-only` or baseline already exists. Read `references/fitness-scoring.md` for the baseline capture procedure.

### Step 1: Kill Switch Check

Run at the TOP of every cycle:

```bash
CYCLE_START_SHA=$(git rev-parse HEAD)
# Mechanical pre-cycle gate (soc-sfjx): markers (KILL/STOP/DORMANT/HANDOFF with
# TTL + soc-5qit non-sticky semantics), goal-regression, and prior-cycle-FAIL.
# This is a SCRIPT the loop MUST run, not prose it can skip — externalized from
# the old inline block so the kill-switch + revert-on-red are enforced, not
# advisory. Adapted from the mt-olympus unbounded-evolve substrate.
if [ -x scripts/evolve/halt-check.sh ]; then
  if ! HALT_OUT=$(bash scripts/evolve/halt-check.sh --json); then
    REASON=$(printf '%s' "$HALT_OUT" | jq -r '.halt_reason // "unknown"')
    if [ "$REASON" = "prior_cycle_fail" ]; then
      export EVOLVE_RESTORATIVE=1   # not terminal: Step 1.5 restricts scope to CI-red reduction
    else
      echo "halt: $REASON"; exit 0  # kill/user_halt/dormant/goal_regression -> stop this cycle
    fi
  fi
else
  # Fallback for repos without the substrate: minimal inline marker check.
  for m in "$HOME/.config/evolve/KILL" .agents/evolve/STOP; do [ -f "$m" ] && { echo "halt: $m"; exit 0; }; done
  [ -f .agents/evolve/DORMANT ] && { [ "$(bd ready --json 2>/dev/null | jq -r 'length // 0')" -gt 0 ] && rm -f .agents/evolve/DORMANT || { echo dormant; exit 0; }; }
  [ -f .agents/evolve/HANDOFF ] && rm -f .agents/evolve/HANDOFF
fi
```

**Agile-first dormancy (soc-5qit):** `DORMANT` is NEVER sticky while ready beads exist — `halt-check.sh` auto-clears it when `bd ready`/harvested work exists. KILL/STOP honor `EVOLVE_KILL_TTL_DAYS` (default 7); stale markers are surfaced and bypassed. `goal_regression` (latest cycle report `goals_passing_after < before`) halts the loop for operator attention. Heavy-context sessions write non-sticky HANDOFF; the next fire clears it and resumes. The gate is mechanical: see `scripts/evolve/halt-check.sh`.

### Step 1.5: Healing-first classifier

Before fitness or work selection, classify the cycle: `ao ci recent --limit 1 2>/dev/null | jq -r '.Conclusion // empty'` (typed BC2 `CIStatusPort`, soc-y5vh.2). If the last push CI was `failure`, this cycle is **restorative-only** — Step 3 takes only CI-red-reducing work (bug-type harvested items, gate-failure-fix beads, generator bug output); no promotions, features, or new-shape work until green. A `gate=FAIL` in cycle-history.jsonl auto-triggers this for cycle N+1 (and `halt-check.sh` surfaces it as `prior_cycle_fail`). See `references/convergence-mechanics.md`.

**Convergence check:** evaluate the STOP predicate via the typed BC3 `ConvergenceCheckPort` — `ao loop converged --green-streak <n> --unconsumed-high-medium <n> [--fitness-baseline]` (soc-y5vh.8). Branch on `.converged` (default: CI green streak ≥ 3, HIGH+MEDIUM next-work ≤ 1, fitness baseline captured); if true, emit teardown and do NOT re-arm wakeup.

### Step 2: Measure Fitness

Skip if `--beads-only`. Run `scripts/evolve-measure-fitness.sh` to produce a rolling fitness snapshot at `.agents/evolve/fitness-latest.json`. Read `references/fitness-scoring.md` for the full measurement procedure, baseline capture, and post-cycle regression detection.

### Step 3: Select Work

Selection is a ladder, not a one-shot check — after every productive cycle, return to the TOP and re-read the queue before considering dormancy. **Read [references/work-selection-ladder.md](references/work-selection-ladder.md) for the full per-rung procedure** (programmatic `ao evolve next-work` recommendation, scope filter, metronome gate, the generator rungs with their code blocks, the `--quality` inverted cascade, and the dormancy hard-gate).

Ladder order (standard mode):
- **3.0 Scope filter** (soc-5qit) — split-or-defer oversized candidates via scout-mode; never bail.
- **3.1 Harvested** — `.agents/rpi/next-work.jsonl`, highest-value unconsumed.
- **3.2 Open ready beads** — `bd ready`, highest priority.
- **3.3 Failing goals + directive gaps** — skip if `--beads-only`; skip quarantined oscillators.
- **3.4–3.6 Generators** — `/test` coverage, `/deps`+`/perf`, `/refactor`; findings → beads/queue items.
- **3.7 Feature suggestions** grounded in repo purpose.

`--quality` inverts the top (findings before goals/directives). The metronome gate blocks a rung that would repeat the trailing run's `mode` (streak ≥3).

**Agile invariant (soc-5qit):** `bd ready ≥ 1` ⇒ the loop NEVER writes DORMANT and NEVER exits. The only path to DORMANT is a fully empty backlog + dry generators (3 passes). Context exhaustion → HANDOFF, not DORMANT. Under loop mode, `write-stop-marker` refuses → log blocked + operator-wait (ADR-0007).

If `--dry-run`: report what would be worked on and go to Teardown.

### Step 4: Execute

Primary engine: `/rpi` for implementation-quality work (all 3 phases mandatory). `/implement` or `/crank` only when a bead has execution-ready scope.

If a repo-local `PROGRAM.md` contract is active, `/rpi` will load it automatically. `/evolve` must compose with that behavior, not bypass it:
- Do not select work that is obviously outside mutable scope.
- If a bead or goal would require edits under immutable scope, escalate it or convert it into durable follow-up work instead of launching `/rpi`.
- When work is plausibly in scope but still uncertain, let `/rpi` discovery validate the fit and surface a scope escape explicitly.

For a **harvested item, failing goal, directive gap, testing improvement, validation tightening task, bug-hunt result, drift finding, or feature suggestion**:
```
Invoke /rpi "{normalized work title}" --auto --max-cycles=1
```

For a **beads issue**:
```
Prefer: /rpi "Land {issue_id}: {title}" --auto --max-cycles=1
Fallback: /implement {issue_id}
```
Or for an epic with children: `Invoke /crank {epic_id}`.

If Step 3 created durable work instead of executing it immediately, re-enter Step 3 and let the newly-created bead item win through the normal selection order.

**Mechanical-batch hint:** when the implementation phase identifies > 20 uniform per-file edits, prefer a script (`awk`/`sed`/`for f in $candidates`) over N tool-level Edit calls. See `references/mechanical-batches.md` for the decision rule and the script-first pattern.

**Pre-flight schema check (architectural migrations):** if the selected work is a port/adapter migration that rewires an existing consumer, BEFORE invoking `/rpi`, sample two representative consumer call sites and compare field-use against the target port surface. If the consumer reads > 20% more fields than the port projects, abort the migration cycle and convert the work into a port-widening cycle instead. The phase-2 narrowness post-mortem (`docs/learnings/2026-05-13-bc-ports-narrowness-postmortem.md`) is the encoded lesson; see `references/pre-flight-schema-check.md` for the procedure.

**Operator-shape carve-out:** `AskUserQuestion` is permitted ONLY for shape decisions affecting > 50 files OR a schema/contract surface (carrier choice, struct-field shape, frontmatter-key shape). See `references/autonomous-execution.md` for the bound on this exception.

### Step 4.5: Source-surface detection (pre-gate sync)

Before invoking the regression gate, sync downstream artifacts when the staged diff touches binary or embedded surfaces:

- `cli/**/*.go` changed → `cd cli && make build && go install ./cmd/ao`
- `skills/**` or `hooks/**` changed → `cd cli && make sync-hooks`
- `skills-codex/**` changed → `bash scripts/regen-codex-hashes.sh`

Without these, the gate fails on stale-binary or embedded-drift errors that look like real regressions. See `references/gate-hygiene.md` for the detection recipe.

### Step 5: Regression Gate

After execution, run the project build+test bundle. If the repo execution profile declared `validation_commands`, run them. If a repo-local program contract exists, run its `validation_commands` too, de-duplicated and in declared order after the repo bootstrap checks. Also check `if [ -f scripts/check-wiring-closure.sh ]; then bash scripts/check-wiring-closure.sh; fi`.

Use the program contract's `decision_policy` as the first keep/revert rule set for the cycle:
- if the cycle breached immutable scope, treat it as regressed
- if program validation commands fail, treat it as regressed
- if the decision policy declares a revert rule that fired, revert before consuming claimed work or advancing the queue

Treat program `stop_conditions` as per-cycle done criteria. Do not mark claimed work consumed, completed, or productive until both the stop conditions and the regression gate pass.

If not `--beads-only`, re-measure fitness to `fitness-latest-post.json` and detect regressions. The AgentOps CLI is required for fitness measurement. Read `references/fitness-scoring.md` for the full measurement, regression detection, and revert procedure.

**Gate output parsing:** trust the structural marker `^.*Pass [0-9]+: (FAILED|BLOCKED)` over the trailing status line — the trailing line conflates blocking and advisory results. See `references/gate-hygiene.md`.

Work finalization after the regression gate: claim it first, then keep `consumed: false` until the /rpi cycle succeeds. After the cycle's `/post-mortem` finishes, immediately re-read `.agents/rpi/next-work.jsonl` before selecting the next item. Read `references/knowledge-loop-integration.md` for full claim/release semantics.

### Step 6: Log Cycle + Commit

Two paths: productive cycles get committed, idle cycles are local-only.

**PRODUCTIVE cycles** (result is improved, regressed, or harvested): compute quality score (if `--quality`), log via `scripts/evolve-log-cycle.sh`, commit if real changes exist. See `references/quality-mode.md` for scoring.

**IDLE cycles** (nothing found even after generator layers): log via `evolve-log-cycle.sh` with `--result "unchanged"`. No git add, no commit.

**Record the XP/BDD/TDD trace.** When a cycle worked a product or goal-backed gap, pass `--trace-json` to `evolve-log-cycle.sh` (or `ao loop append`) so the cycle records the continuous-evolution kernel — goal hypothesis → selected gap → Gherkin scenario → first failing proof → red/green evidence → refactor note → validation evidence → ratchet action → goal reshape — and a reviewer can reconstruct the cycle without the transcript. A trivial one-shot cycle records a `trace.exemption_reason` instead of carrying false BDD/TDD ceremony. Trace completeness is advisory, never a gate. See `references/cycle-history.md` ("XP/BDD/TDD Evidence Trace").

### Step 7: Loop or Stop

```bash
while true; do
  # Step 1 .. Step 6
  # Stop ONLY if: operator override (KILL/STOP), max-cycles, regression-breaker,
  # or genuine stagnation (bd ready=0 AND harvested=0 AND failing-goals=0 AND
  # generators dry across 3 passes). Context exhaustion is NOT a stop — it's a
  # session-handoff signal (HANDOFF marker) that the next cron-fire clears.
  CYCLE=$((CYCLE + 1))
done
```

**Stop reasons (soc-5qit, ALL require genuine reason — never just context size):**

1. **KILL/STOP file present** — operator override.
2. **`--max-cycles=N` cap reached**.
3. **Genuine stagnation** — `bd ready=0 AND harvested-unconsumed=0 AND failing-goals=0 AND GENERATOR_EMPTY_STREAK>=2 AND IDLE_STREAK>=2`. Writes DORMANT, which auto-clears in Step 1 the moment `bd create` adds a new ready bead.
4. **Regression breaker after a revert**.

**Context exhaustion is NOT a stop (soc-5qit).** Heavy-context sessions write `.agents/evolve/HANDOFF` (non-sticky), log `result: "context-handoff"` to cycle-history, and exit the turn cleanly. The next cron-fire (compacted/fresh context) clears HANDOFF in Step 1 and resumes. The loop is continuous across compactions; never write DORMANT for context size. See `references/context-budget.md`.

**Mandatory checkpoint #6 — session-PR threshold (NOT terminal, gates next cycle):** at `session_pr_count >= 5` (soc-waxr default), invoke `/post-mortem --deep`, wait for verdict file. PASS → continue. WARN → continue with caveat in next cycle's `notes`. FAIL or non-convergence → write STOP. Agent MUST NOT self-grade or self-write STOP. Full procedure in `references/postmortem-checkpoint.md` (soc-n75z).

**Self-perpetuation modes:** the terminal-native `ao evolve` loop and the Claude-Code-harness `ScheduleWakeup` end-of-turn pattern are duals — both drive Step 1..Step 7 repeatedly against the same persisted state. See `references/autonomous-execution.md` for the ScheduleWakeup cadence and the rule that hard stops must NOT re-arm.

Push only when productive work has accumulated:
```bash
if [ $((PRODUCTIVE_THIS_SESSION % 5)) -eq 0 ] && [ "$PRODUCTIVE_THIS_SESSION" -gt 0 ]; then
  git push
fi
```

**Drive to completion (orchestrator-merge model, soc-2drk).** Where the repo requires PRs (branch protection rejects direct `main` pushes), a productive cycle does not stop at "PR opened" — the loop is the orchestrator that drives each bead to *merged*. Ship the bead from its per-bead worktree as a PR (trailers `Closes-scenario` / `Bounded-context` / `Evidence`), wait for CI, and **squash-merge to main yourself once CI is green** (`gh pr merge <N> --squash --admin`), then `bd close` the bead and remove the worktree. **Green CI is the only merge gate** — on a quality/test red, fix-and-repush or revert; never merge red. The loop may dispatch sub-agents to implement and drives their PRs to merge too. The operator stays *on* the loop (intent + STOP marker), not *in* it (per-PR approval). This **supersedes "operator is the merge gate"** for the autonomous loop — see [ADR-0008](../../docs/adr/ADR-0008-evolve-intelligent-agile-operating-model.md).

### Teardown

Read `references/knowledge-loop-integration.md` for the full teardown learning extraction procedure (commit staged artifacts, run `/post-mortem`, push, report summary).

A teardown `/post-mortem` is a light-touch retrospective on session-end. It does NOT substitute for the mandatory threshold checkpoint (`references/postmortem-checkpoint.md`); that one is council-gated and edge-triggered at `session_pr_count >= 5`. Never write `.agents/evolve/STOP` as a substitute for the checkpoint's verdict file — STOP without a verdict is the 2026-05-20 anti-pattern (soc-n75z).

**Release-context teardown (MANDATORY when the loop ran on a release-shaped branch):**

When the current branch matches `release/*`, `v*-prep`, `v*-evolve-run`, or `v\d+\.\d+*`, the teardown report MUST NOT recommend `/release` as the next step. Instead, emit the explicit pre-release checklist below — the operator must run these AND confirm green before tagging:

```
## Pre-release checklist — REQUIRED before /release

The autonomous loop has stopped, but release-readiness gates have NOT been run
during cycles. The operator MUST run the following sequence and confirm green
before invoking /release. Do NOT skip any of these on the basis of "cycles
were green" — fast pre-push gate ≠ full pre-push gate; goals-measure ≠
release readiness.

  [ ] 1. Regenerate CLI reference docs if any cobra command/flag changed:
         bash scripts/generate-cli-reference.sh
         git diff cli/docs/COMMANDS.md   # commit if non-empty

  [ ] 2. Run the FULL pre-push gate (NOT --fast):
         bash scripts/pre-push-gate.sh

  [ ] 3. Run the release-readiness gate:
         bash scripts/ci-local-release.sh

  [ ] 4. (Recommended) Smoke /evolve with the new typed read paths if BC port
         wire-ups changed:
         /evolve --quick --max-cycles=1 --dry-run

Only after [1]–[3] pass: /release <version>

If any check fails, fix the issue, re-run all four, then ship.
```

The handoff artifact (e.g., `.agents/runs/<release>/READY-TO-TAG.md`) MUST contain this checklist verbatim, unchecked, when written by the loop. The operator checks the boxes as they complete each gate; "ready to tag" means the boxes are checked, not that the loop ran cleanly.

**Rationale:** cycles 170-183 of the v2.41-evolve-run shipped clean code, all unit/integration tests green, `ao goals measure` 0/30 failing for three consecutive cycles — but the loop never ran the full pre-push gate, `ci-local-release.sh`, or `generate-cli-reference.sh`. The latter was load-bearing (the branch removed a CLI flag). Per-cycle `--fast` is a smoke test, not release readiness. Operator caught the gap; this checklist makes it mechanical.

## Examples

**User says:** `/evolve --max-cycles=5`
**What happens:** Evolve re-enters the full selection ladder after every `/rpi` cycle and runs producer layers instead of idling on empty queues.

**User says:** `/evolve --beads-only`
**What happens:** Evolve skips goals measurement and works through `bd ready` backlog.

**User says:** `/evolve --dry-run`
**What happens:** Evolve shows what would be worked on without executing.

**User says:** `/evolve --compile`
**What happens:** Evolve runs `ao mine` + `ao defrag` at session start to surface fresh signal (orphaned research, code hotspots, oscillating goals) before the first evolve cycle. Use before a long autonomous run or after a burst of development activity.

**User says:** `/evolve`
**What happens:** See `references/examples.md` for a worked overnight flow that moves through beads -> harvested work -> goals -> testing -> bug hunt -> feature suggestion before dormancy is considered.

See `references/examples.md` for detailed walkthroughs.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Loop exits immediately | Remove `~/.config/evolve/KILL` or `.agents/evolve/STOP` |
| Stagnation after repeated empty passes | Queue layers and producer layers were empty across multiple passes — dormancy is the fallback outcome |
| `ao goals measure` hangs | Use `--timeout 30 --total-timeout 75` or `--beads-only` to skip |
| Regression gate reverts | Review reverted changes, narrow scope, re-run; claimed work items must be released back to available state |

See `references/cycle-history.md` for advanced troubleshooting.

## References

- [references/evolve.feature](references/evolve.feature) — Executable spec: gated cycles, ladder, bounded slice, never-self-halt
- [references/long-loop-discipline.md](references/long-loop-discipline.md) — Disk-is-truth axiom
- [references/artifacts.md](references/artifacts.md) — Generated files registry
- [references/autonomous-execution.md](references/autonomous-execution.md) — Autonomous-loop rules + operator-shape carve-out
- [references/snapshot-pattern-for-long-cycle-gates.md](references/snapshot-pattern-for-long-cycle-gates.md) — Snapshot pattern for long-cycle gates
- [references/compounding.md](references/compounding.md) — Knowledge flywheel and work harvesting
- [references/context-budget.md](references/context-budget.md) — `CONTEXT_BUDGET_EXHAUSTED` as a third stop reason and handoff protocol
- [references/convergence-mechanics.md](references/convergence-mechanics.md) — Read-path mechanisms for compounding
- [references/domain-evolution-bootstrap.md](references/domain-evolution-bootstrap.md) — BDD/DDD/Hexagonal/TDD/XP control surface for skill/domain evolution
- [references/cycle-history.md](references/cycle-history.md) — JSONL format, recovery protocol, kill switch
- [references/examples.md](references/examples.md) — Detailed usage examples
- [references/fitness-scoring.md](references/fitness-scoring.md) — Baseline capture, regression detection, revert procedure
- [references/gate-hygiene.md](references/gate-hygiene.md) — Pre-gate source-surface detection and structural gate-output parsing
- [references/goals-schema.md](references/goals-schema.md) — GOALS.yaml format and continuous metrics
- [references/knowledge-loop-integration.md](references/knowledge-loop-integration.md) — Claim/release semantics and harvest re-read
- [references/mechanical-batches.md](references/mechanical-batches.md) — Script-first vs per-file Edit for > 20-file uniform batches
- [references/metronome-gate.md](references/metronome-gate.md) — Cross-cycle same-mode-repeat blocker
- [references/oscillation.md](references/oscillation.md) — Oscillation detection and quarantine
- [references/pre-flight-schema-check.md](references/pre-flight-schema-check.md) — Cheap field-fit check before architectural migration cycles
- [references/postmortem-checkpoint.md](references/postmortem-checkpoint.md) — Stop reason #6: session-PR post-mortem checkpoint (soc-n75z)
- [references/parallel-execution.md](references/parallel-execution.md) — Parallel /swarm architecture
- [references/quality-mode.md](references/quality-mode.md) — Quality-first mode: scoring, priority cascade, artifacts
- [references/scout-mode.md](references/scout-mode.md) — Scout-mode as a first-class cycle result; scope filter procedure
- [references/teardown.md](references/teardown.md) — Trajectory computation and session summary

## See Also

- `skills/dream/SKILL.md` — the nightly knowledge compounder; absorbs /harvest and runs the compounding loop overnight
- `skills/rpi/SKILL.md` — Full lifecycle orchestrator (called per cycle)
- `skills/crank/SKILL.md` — Epic execution (called for beads epics)
- `docs/contracts/autodev-program.md` — Repo-local operational contract for bounded autonomous development
- `GOALS.yaml` — Fitness goals for this repo
- [test](../test/SKILL.md) — Test generation and coverage analysis
- [refactor](../refactor/SKILL.md) — Safe, verified refactoring
- [deps](../deps/SKILL.md) — Dependency audit and vulnerability scanning
- [perf](../perf/SKILL.md) — Performance profiling and benchmarking
