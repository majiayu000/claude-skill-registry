---
name: evolve
description: Goal-driven v2 autonomous improvement loop. Runs the post-mortem, repo analysis, next-work selection, plan/pre-mortem, implementation, validation, and repeat cadence through /rpi and ao evolve. Also pulls from open beads when goals all pass and accepts ordered roadmaps via --queue. Use when you want to "improve", "iterate", "fix issues", "work through tasks", "evolve", "check goal fitness", "run improvement loop", "pick up next work", "postmortem and continue", or "run roadmap".
skill_api_version: 1
user-invocable: true
context:
  window: fork
  intent:
    mode: task
  sections:
    exclude: [HISTORY]
  intel_scope: full
metadata:
  tier: execution
  dependencies:
    - rpi         # required - executes each improvement cycle
    - post-mortem # required - auto-runs at teardown to harvest learnings
    - compile     # optional - knowledge warmup when --compile is passed
  triggers:
    - evolve
    - improve everything
    - autonomous improvement
    - run until done
    - roadmap
    - run queue
    - pinned queue
    - postmortem and continue
    - analyze repo and keep going
output_contract: "code changes, GOALS.md fitness deltas"
---

# /evolve — Goal-Driven Compounding Loop

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
0. **Pinned work queue** (`--queue=<file>` or inline roadmap — see `references/pinned-queue.md`)
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
/evolve --queue=.agents/evolve/roadmap.md           # Process ordered roadmap
/evolve --queue=.agents/evolve/roadmap.md --test-first  # Roadmap with strict quality
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
| `--queue=<file>` | none | Process items from ordered markdown queue file sequentially before fitness-driven selection |
| `--no-lifecycle` | off | Skip lifecycle work generators in Steps 3.4-3.6 (/test, /deps, /perf, /refactor). Falls back to manual scanning. |

## Execution Steps

**YOU MUST EXECUTE THIS WORKFLOW. Do not just describe it.**

**FULLY AUTONOMOUS.** Read `references/autonomous-execution.md`. Every `/rpi` uses `--auto`. Do NOT ask the user anything. Each cycle = complete 3-phase `/rpi` run.

### Step 0: Setup

```bash
mkdir -p .agents/evolve
ao lookup --query "autonomous improvement cycle" --limit 5 2>/dev/null || true
```

**Apply retrieved knowledge:** If learnings are returned, check each for applicability to the current improvement cycle. For applicable learnings, cite by filename and record: `ao metrics cite "<path>" --type applied 2>/dev/null || true`

Before cycle recovery, load the repo execution profile contract when it exists. The repo execution profile is the source for repo policy; the user prompt should mostly supply mission/objective, not restate startup reads, validation bundle, tracker wrapper rules, or `definition_of_done`.

- Locate `docs/contracts/repo-execution-profile.md` and `docs/contracts/repo-execution-profile.schema.json`.
- Read the ordered `startup_reads` and bootstrap from those repo paths before selecting work.
- Cache repo `validation_commands`, `tracker_commands`, and `definition_of_done` into session state.
- If the repo execution profile is present but missing required fields, stop or downgrade with an explicit warning before cycle 1. Do not silently invent repo policy.

Then load the repo-local autodev program contract when it exists. The execution profile remains the repo bootstrap and landing-policy layer; `PROGRAM.md` or `AUTODEV.md` is the repo-local execution layer for the current improvement loop.

- Locate `PROGRAM.md` and `AUTODEV.md`. `PROGRAM.md` takes precedence.
- Read the resolved program before cycle recovery and cache `program_path`, `mutable_scope`, `immutable_scope`, `validation_commands`, `decision_policy`, and `stop_conditions` into session state.
- If the program file exists but is structurally invalid, stop or downgrade with an explicit warning before cycle 1. Do not silently ignore a broken operator contract.
- When a program contract exists, prefer work that can land wholly inside mutable scope. Do not silently widen scope around immutable files.

Recover cycle number, queue/generator streaks, and the last claimed work item from disk (survives context compaction). Initialize `CYCLE` from `cycle-history.jsonl`, recover `IDLE_STREAK`, `GENERATOR_EMPTY_STREAK`, `LAST_SELECTED_SOURCE`, and `CLAIMED_WORK_REF` from `session-state.json`.

**Circuit breakers:** Time-based (60 min no productive work) and consecutive failure (5 in queue mode). See `references/roadmap-queue-patterns.md` for queue-specific circuit breakers.

**Oscillation quarantine:** Pre-populate quarantine list from cycle history (scan for goals with 3+ improved-to-fail transitions). See `references/oscillation.md`.

Parse flags: `--max-cycles=N` (default unlimited), `--dry-run`, `--beads-only`, `--skip-baseline`, `--quality`, `--compile`, `--queue=<file>`.

### Step 0.1: Parse Pinned Queue (--queue only)

Skip if `--queue` was not passed. Read `references/roadmap-queue-patterns.md` for the full queue parsing, state persistence, and resume protocol. See also `references/pinned-queue.md` for format specification and blocker syntax.

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
  claimed_work: <null or queue reference being worked>,
  queue_refresh_count: <incremented after every /rpi cycle>,
  pinned_queue: <parsed items array or null>,
  pinned_queue_file: <path or null>,
  pinned_queue_index: <current 0-based position>,
  pinned_queue_completed: <array of completed item IDs>,
  pinned_queue_escalated: <array of escalated items with reasons>,
  unblock_depth: <current nesting depth, 0 when not unblocking>,
  unblock_failures: <consecutive failures on current item>,
  unblock_chain: <stack of blocker IDs being resolved>
}
```

Persist `evolve_state` to `.agents/evolve/session-state.json` at each cycle boundary, after queue claims, after queue release/finalize, and during teardown. `cycle-history.jsonl` remains the canonical cycle ledger; `session-state.json` carries resume-only state that has not yet earned a committed cycle entry.

### Step 0.2: Compile Warmup (--compile only)

Skip if `--compile` was not passed or if `--dry-run`. Read `references/knowledge-loop-integration.md` for the full warmup procedure (mine + defrag + signal notes).

### Step 0.5: Baseline (first run only)

Skip if `--skip-baseline` or `--beads-only` or baseline already exists. Read `references/fitness-scoring.md` for the baseline capture procedure.

### Step 1: Kill Switch Check

Run at the TOP of every cycle:

```bash
CYCLE_START_SHA=$(git rev-parse HEAD)
[ -f ~/.config/evolve/KILL ] && echo "KILL: $(cat ~/.config/evolve/KILL)" && exit 0
[ -f .agents/evolve/STOP ] && echo "STOP: $(cat .agents/evolve/STOP 2>/dev/null)" && exit 0
```

### Step 2: Measure Fitness

Skip if `--beads-only`. Run `scripts/evolve-measure-fitness.sh` to produce a rolling fitness snapshot at `.agents/evolve/fitness-latest.json`. Read `references/fitness-scoring.md` for the full measurement procedure, baseline capture, and post-cycle regression detection.

### Step 3: Select Work

Selection is a ladder, not a one-shot check. After every productive cycle, return to the TOP of this step and re-read the queue before considering dormancy.

When a repo-local program contract exists, apply a scope filter before Step 4:
- candidate work that clearly requires immutable-scope edits is not eligible for direct execution
- prefer harvested, beads, goals, and generated work that can plausibly land within mutable scope
- if the selected item is inherently out of scope, escalate it or convert it into durable follow-up work instead of invoking `/rpi` and hoping discovery widens scope

**Step 3.0: Pinned work queue** (only when `--queue` is set)

Read `references/roadmap-queue-patterns.md` for the full pinned queue work selection protocol (item-to-prompt mapping, escalation cascade, blocker detection). When pinned queue is active, skip Steps 3.1-3.7 entirely. When exhausted, fall through to normal selection.

**Step 3.1: Harvested work first**

Read `.agents/rpi/next-work.jsonl` and pick the highest-value unconsumed item. Prefer exact repo match, then concrete implementation work, then higher severity. Read `references/knowledge-loop-integration.md` for the claim/release protocol.

**Step 3.2: Open ready beads**

If no harvested item is ready, check `bd ready`. Pick the highest-priority unblocked issue.

**Step 3.3: Failing goals and directive gaps** (skip if `--beads-only`)

First assess directives, then goals:
- top-priority directive gap from `ao goals measure --directives`
- highest-weight failing goals (skip quarantined oscillators)
- lower-weight failing goals

This step exists even when all queued work is empty. Goals are the third source, not the stop condition.

```bash
DIRECTIVES=$(ao goals measure --directives 2>/dev/null)
FAILING=$(jq -r '.goals[] | select(.result=="fail") | .id' .agents/evolve/fitness-latest.json | head -1)
```

**Oscillation check:** Before working a failing goal, check if it has oscillated (improved-to-fail transitions >= 3 times). If so, quarantine it and try the next goal. See `references/oscillation.md` and `references/fitness-scoring.md` for the detection procedure.

**Step 3.4: Testing improvements**

When queues and goals are empty, generate concrete testing work via `/test`:

```
if --no-lifecycle is NOT set:
  Skill(skill="test", args="coverage")
  Only files with < 40% coverage become queue items (severity threshold).
```

If `/test` is unavailable or `--no-lifecycle` is set, fall back to manual scanning:
- find packages/files with thin or missing tests
- look for missing regression tests around recent bug-fix paths
- identify flaky or absent headless/runtime smokes

Convert any real finding into durable work:
- add a bead when the work needs tracked backlog ownership, or
- append a queue item under the shared next-work contract when it should flow directly back into `/rpi`

**Step 3.5: Validation tightening and bug-hunt passes**

If testing improvement generation returns nothing, run lifecycle generators then bug-hunt sweeps:

```
if --no-lifecycle is NOT set:
  a) Skill(skill="deps", args="audit")
     Only deps with CVSS >= 7.0 or 2+ major versions behind become queue items.

  b) if perf-sensitive code detected (benchmarks exist, hot path patterns):
       Skill(skill="perf", args="profile --quick")
       Convert significant perf findings to queue items.
```

If lifecycle generators return nothing or are skipped, fall back to manual sweeps:
- missing validation gates
- weak lint/contract coverage
- bug-hunt style audits for risky areas
- stale assumptions between docs, contracts, and runtime truth

Again: convert findings into beads or queue items, then immediately select the highest-priority result and continue.

**Step 3.6: Drift / hotspot / dead-code mining**

If the prior generators are empty, mine for complexity debt via `/refactor`:

```
if --no-lifecycle is NOT set:
  Skill(skill="refactor", args="--sweep all --dry-run")
  Only functions with CC > 20 become queue items (severity threshold).
```

If `/refactor` is unavailable or `--no-lifecycle` is set, fall back to manual mining:
- complexity hotspots
- stale TODO/FIXME markers
- dead code
- stale docs
- stale research
- drift between generated artifacts and source-of-truth files

Do not stop here. Normalize findings into tracked work and continue.

**Step 3.7: Feature suggestions**

If all concrete remediation layers are empty, propose one or more specific feature ideas grounded in the repo purpose, write them as durable work, and continue:
- create a bead when the feature needs review/backlog treatment
- or append a queue item with `source: "feature-suggestion"` when it is ready for the next `/rpi` cycle

**Quality mode (`--quality`)** — inverted cascade (findings before directives):

Step 3.0q: Unconsumed high-severity post-mortem findings:
```bash
HIGH=$(jq -r 'select(.consumed==false) | .items[] | select(.severity=="high") | .title' \
  .agents/rpi/next-work.jsonl 2>/dev/null | head -1)
```

Step 3.1q: Unconsumed medium-severity findings.

Step 3.2q: Open ready beads.

Step 3.3q: Emergency gates (weight >= 5) and top directive gaps.

Step 3.4q: Testing improvements.

Step 3.5q: Validation tightening / bug-hunt / drift mining.

Step 3.6q: Feature suggestions.

This inverts the standard cascade only at the top of the ladder: findings BEFORE goals and directives. It does NOT skip the generator layers.

When evolve picks a finding, claim it first in next-work.jsonl:
- Set `claim_status: "in_progress"`, `claimed_by: "evolve-quality:cycle-N"`, `claimed_at: "<timestamp>"`
- Set `consumed: true` only after the /rpi cycle and regression gate succeed
- If the /rpi cycle fails (regression), clear the claim and leave `consumed: false`

See `references/quality-mode.md` for scoring and full details.

**Nothing found?** HARD GATE — only consider dormancy after the generator layers also came up empty:

```bash
# Count trailing idle/unchanged entries in cycle-history.jsonl (portable, no tac)
IDLE_STREAK=$(awk '/"result"\s*:\s*"(idle|unchanged)"/{streak++; next} {streak=0} END{print streak+0}' \
  .agents/evolve/cycle-history.jsonl 2>/dev/null)

# Pinned queue mode: never consider stagnation while queue has items
if [ -n "$QUEUE_FILE" ] && [ "$QUEUE_INDEX" -lt "$QUEUE_TOTAL" ]; then
  # Queue not exhausted — skip stagnation check, return to Step 3.0
  :
elif [ "$GENERATOR_EMPTY_STREAK" -ge 2 ] && [ "$IDLE_STREAK" -ge 2 ]; then
  # Queue layers are empty AND producer layers were empty for the 3rd consecutive pass — STOP
  echo "Stagnation reached after repeated empty queue + generator passes. Dormancy is the last-resort outcome."
  # go to Teardown — do NOT log another idle entry
fi
```

If the queue layers were empty but a generator pass has not been exhausted 3 times yet, persist the new generator streak in `session-state.json` and loop back to Step 1. Empty pre-cycle queues are not a stop reason by themselves.

A cycle is idle only if NO work source returned actionable work and every generator layer also came up empty. A cycle that targeted an oscillating goal and skipped it counts as idle only after the remaining ladder was exhausted.

If `--dry-run`: report what would be worked on and go to Teardown.

### Step 4: Execute

**4.1: Blocker Resolution (pinned queue only)**

If `UNBLOCK_TARGET` is set (from Step 3.0), enter the blocker resolution sub-loop. Read `references/roadmap-queue-patterns.md` for the full blocker resolution protocol (depth limits, escalation cascade, retry logic, dynamic blocker detection).

**4.2: Normal Execution**

Primary engine: `/rpi` for implementation-quality work (all 3 phases mandatory). `/implement` or `/crank` only when a bead has execution-ready scope.

If a repo-local `PROGRAM.md` contract is active, `/rpi` will load it automatically. `/evolve` must compose with that behavior, not bypass it:
- Do not select work that is obviously outside mutable scope.
- If a queue item, bead, or goal would require edits under immutable scope, escalate it or convert it into durable follow-up work instead of launching `/rpi`.
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

If Step 3 created durable work instead of executing it immediately, re-enter Step 3 and let the newly-created queue/bead item win through the normal selection order.

### Step 5: Regression Gate

After execution, run the project build+test bundle. If the repo execution profile declared `validation_commands`, run them. If a repo-local program contract exists, run its `validation_commands` too, de-duplicated and in declared order after the repo bootstrap checks. Also check `if [ -f scripts/check-wiring-closure.sh ]; then bash scripts/check-wiring-closure.sh; fi`.

Use the program contract's `decision_policy` as the first keep/revert rule set for the cycle:
- if the cycle breached immutable scope, treat it as regressed
- if program validation commands fail, treat it as regressed
- if the decision policy declares a revert rule that fired, revert before consuming claimed work or advancing the queue

Treat program `stop_conditions` as per-cycle done criteria. Do not mark claimed work consumed, completed, or productive until both the stop conditions and the regression gate pass.

If not `--beads-only`, re-measure fitness to `fitness-latest-post.json` and detect regressions. The AgentOps CLI is required for fitness measurement. Read `references/fitness-scoring.md` for the full measurement, regression detection, and revert procedure.

Queue finalization after the regression gate: claim it first, then keep `consumed: false` until the /rpi cycle succeeds. After the cycle's `/post-mortem` finishes, immediately re-read `.agents/rpi/next-work.jsonl` before selecting the next item. Read `references/knowledge-loop-integration.md` for full claim/release semantics.

### Step 6: Log Cycle + Commit

Two paths: productive cycles get committed, idle cycles are local-only.

**PRODUCTIVE cycles** (result is improved, regressed, or harvested): compute quality score (if `--quality`), build queue args (if `--queue`), log via `scripts/evolve-log-cycle.sh`, commit if real changes exist. See `references/roadmap-queue-patterns.md` for queue advancement logic and `references/quality-mode.md` for scoring.

**IDLE cycles** (nothing found even after generator layers): log via `evolve-log-cycle.sh` with `--result "unchanged"`. No git add, no commit.

### Step 7: Loop or Stop

```bash
while true; do
  # Step 1 .. Step 6
  # Stop if kill switch, max-cycles, or a real safety breaker triggers
  # Otherwise increment cycle and re-enter selection
  CYCLE=$((CYCLE + 1))
done
```

Push only when productive work has accumulated:
```bash
if [ $((PRODUCTIVE_THIS_SESSION % 5)) -eq 0 ] && [ "$PRODUCTIVE_THIS_SESSION" -gt 0 ]; then
  git push
fi
```

### Teardown

Read `references/knowledge-loop-integration.md` for the full teardown learning extraction procedure (commit staged artifacts, run `/post-mortem`, push, report summary).

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

**User says:** `/evolve --queue=.agents/evolve/roadmap.md --test-first`
**What happens:** Evolve processes each item in the roadmap sequentially. When an item is blocked (e.g., `rig-difc` blocked by `rig-8z29`), evolve auto-lands `rig-8z29` via sub-`/rpi` first, then resumes `rig-difc`. After all queue items complete, evolve falls through to fitness-driven selection. If a blocker chain exceeds 2 levels or fails 3 times, the item is escalated and evolve moves to the next one.

**User says:** `/evolve --queue=.agents/evolve/roadmap.md --max-cycles=20`
**What happens:** Evolve processes the roadmap but caps at 20 total cycles (including unblock sub-cycles). If the queue isn't finished, queue state is persisted to `.agents/evolve/pinned-queue-state.json` for resume in the next session.

See `references/examples.md` for detailed walkthroughs.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Loop exits immediately | Remove `~/.config/evolve/KILL` or `.agents/evolve/STOP` |
| Stagnation after repeated empty passes | Queue layers and producer layers were empty across multiple passes — dormancy is the fallback outcome |
| `ao goals measure` hangs | Use `--timeout 30` flag or `--beads-only` to skip |
| Regression gate reverts | Review reverted changes, narrow scope, re-run; claimed queue items must be released back to available state |
| Blocker chain too deep (>2 levels) | Reduce blocker dependencies or manually land the deepest blocker before resuming |
| Queue item escalated after 3 failures | Review the item scope, simplify, or manually unblock; check `.agents/evolve/escalated.md` for details |
| Queue state lost after compaction | Recover from `.agents/evolve/pinned-queue-state.json` — evolve auto-loads this on restart |

See `references/cycle-history.md` for advanced troubleshooting.

## References

- `references/cycle-history.md` — JSONL format, recovery protocol, kill switch
- `references/compounding.md` — Knowledge flywheel and work harvesting
- `references/goals-schema.md` — GOALS.yaml format and continuous metrics
- `references/parallel-execution.md` — Parallel /swarm architecture
- `references/teardown.md` — Trajectory computation and session summary
- `references/examples.md` — Detailed usage examples
- `references/artifacts.md` — Generated files registry
- `references/oscillation.md` — Oscillation detection and quarantine
- `references/quality-mode.md` — Quality-first mode: scoring, priority cascade, artifacts
- `references/pinned-queue.md` — Pinned queue format, blocker resolution, state persistence

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

## Reference Documents

- [references/artifacts.md](references/artifacts.md)
- [references/compounding.md](references/compounding.md)
- [references/cycle-history.md](references/cycle-history.md)
- [references/examples.md](references/examples.md)
- [references/goals-schema.md](references/goals-schema.md)
- [references/oscillation.md](references/oscillation.md)
- [references/parallel-execution.md](references/parallel-execution.md)
- [references/quality-mode.md](references/quality-mode.md)
- [references/autonomous-execution.md](references/autonomous-execution.md)
- [references/pinned-queue.md](references/pinned-queue.md)
- [references/teardown.md](references/teardown.md)
- [references/fitness-scoring.md](references/fitness-scoring.md)
- [references/roadmap-queue-patterns.md](references/roadmap-queue-patterns.md)
- [references/knowledge-loop-integration.md](references/knowledge-loop-integration.md)
