---
name: evolve
description: 'Goal-driven fitness-scored improvement loop. Measures goals, picks worst gap, runs $rpi, compounds via knowledge flywheel. Also pulls from open beads when goals all pass. Accepts ordered roadmap via --queue for sequential execution with auto-unblocking. Use when you want to "improve", "iterate", "fix issues", "work through tasks", "evolve", "check goal fitness", "run improvement loop", "pick up next work", or "run roadmap".'
---


# $evolve — Goal-Driven Compounding Loop

> Measure what's wrong. Fix the worst thing. Measure again. Compound.

Always-on autonomous loop over `$rpi`. Work selection order:
0. **Pinned work queue** (`--queue=<file>` or inline roadmap — see `references/pinned-queue.md`)
1. **Harvested `.agents/rpi/next-work.jsonl` work** (freshest concrete follow-up)
2. **Open ready beads work** (`bd ready`)
3. **Failing goals and directive gaps** (`ao goals measure`)
4. **Testing improvements** (missing/thin coverage, missing regression tests)
5. **Validation tightening and bug-hunt passes** (gates, audits, bug sweeps)
6. **Complexity / TODO / FIXME / drift / dead code / stale docs / stale research mining**
7. **Concrete feature suggestions** derived from repo purpose when no sharper work exists

**Dormancy is last resort.** Empty current queues mean "run the generator layers", not "stop". Only go dormant after the queue layers and generator layers come up empty across multiple consecutive passes.

```bash
$evolve                      # Run until kill switch, max-cycles, or real dormancy
$evolve --max-cycles=5       # Cap at 5 cycles
$evolve --dry-run            # Show what would be worked on, don't execute
$evolve --beads-only         # Skip goals measurement, work beads backlog only
$evolve --quality            # Quality-first mode: prioritize post-mortem findings
$evolve --quality --max-cycles=10  # Quality mode with cycle cap
$evolve --compile             # Mine → Defrag warmup before first cycle
$evolve --compile --max-cycles=5  # Warm knowledge base then run 5 cycles
$evolve --test-first         # Default strict-quality $rpi execution path
$evolve --no-test-first      # Explicit opt-out from test-first mode
$evolve --queue=.agents/evolve/roadmap.md           # Process ordered roadmap
$evolve --queue=.agents/evolve/roadmap.md --test-first  # Roadmap with strict quality
```

## Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--max-cycles=N` | unlimited | Stop after `N` completed cycles |
| `--dry-run` | off | Show planned cycle actions without executing |
| `--beads-only` | off | Skip goal measurement and run backlog-only selection |
| `--skip-baseline` | off | Skip first-run baseline snapshot |
| `--quality` | off | Prioritize harvested post-mortem findings |
| `--compile` | off | Run `ao mine` + `ao defrag` warmup before cycle 1 |
| `--test-first` | on | Pass strict-quality defaults through to `$rpi` |
| `--no-test-first` | off | Explicitly disable test-first passthrough to `$rpi` |
| `--queue=<file>` | none | Process items from ordered markdown queue file sequentially before fitness-driven selection |

## Execution Steps

**YOU MUST EXECUTE THIS WORKFLOW. Do not just describe it.**

**FULLY AUTONOMOUS.** Evolve runs without human intervention from start to teardown. Every `$rpi` invocation uses `--auto`. Do NOT ask the user for confirmation, clarification, or approval at any point. Do NOT pause between cycles. Do NOT summarize and wait. The user's only touchpoint is the teardown report at the very end.

**Each cycle is a COMPLETE $rpi run** — all 3 phases (discovery → implementation → validation). Never invoke a partial RPI. If a task is too large for one cycle, break it into smaller sub-tasks during discovery and let `$crank` handle the waves. Evolve's job is to keep the loop turning, not to micro-manage individual tasks.

**Break large work into sub-RPI cycles.** When work selection identifies a massive task (7+ issues, multi-subsystem scope), decompose it during `$rpi`'s discovery phase into an epic with waves. One evolve cycle = one `$rpi` run = one complete lifecycle. If the epic is too large for a single session, `$rpi`'s built-in retry and `--from=` resume handle continuation.

### Anti-Patterns (DO NOT)

| Anti-Pattern | Why It's Wrong | Correct Behavior |
|--------------|----------------|------------------|
| Ask the user anything during execution | Evolve is fully autonomous — questions break the loop | Make best judgment, report in teardown |
| Stop after one `$rpi` cycle and summarize | Evolve loops until kill switch, max-cycles, or dormancy | Increment cycle and re-enter Step 1 |
| Run `$rpi` without `--auto` | Non-auto `$rpi` has human gates that halt the loop | Always pass `--auto` to `$rpi` |
| Run partial `$rpi` (skip validation) | Each cycle must be a complete 3-phase lifecycle | Let `$rpi` run all 3 phases autonomously |
| Pause between cycles to explain progress | The user wants results, not narration | Log cycle results, immediately start next cycle |
| Treat "no queued work" as "stop" | Generator layers (testing, validation, drift, features) produce work | Run all generator layers before considering dormancy |

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

Recover cycle number, queue/generator streaks, and the last claimed work item from disk (survives context compaction):
```bash
if [ -f .agents/evolve/cycle-history.jsonl ]; then
  CYCLE=$(( $(tail -1 .agents/evolve/cycle-history.jsonl | jq -r '.cycle // 0') + 1 ))
else
  CYCLE=1
fi
SESSION_START_SHA=$(git rev-parse HEAD)

# Recover idle streak from disk (not in-memory — survives compaction)
# Portable: forward-scanning awk counts trailing idle run without tac (unavailable on stock macOS)
IDLE_STREAK=$(awk '/"result"\s*:\s*"(idle|unchanged)"/{streak++; next} {streak=0} END{print streak+0}' \
  .agents/evolve/cycle-history.jsonl 2>/dev/null)

PRODUCTIVE_THIS_SESSION=0

# Recover generator state and queue claim state
if [ -f .agents/evolve/session-state.json ]; then
  GENERATOR_EMPTY_STREAK=$(jq -r '.generator_empty_streak // 0' .agents/evolve/session-state.json 2>/dev/null || echo 0)
  LAST_SELECTED_SOURCE=$(jq -r '.last_selected_source // empty' .agents/evolve/session-state.json 2>/dev/null || true)
  CLAIMED_WORK_REF=$(jq -r '.claimed_work.ref // empty' .agents/evolve/session-state.json 2>/dev/null || true)
else
  GENERATOR_EMPTY_STREAK=0
  LAST_SELECTED_SOURCE=""
  CLAIMED_WORK_REF=""
fi

# Circuit breaker: stop if last productive cycle was >60 minutes ago
LAST_PRODUCTIVE_TS=$(grep -v '"idle"\|"unchanged"' .agents/evolve/cycle-history.jsonl 2>/dev/null \
  | tail -1 | jq -r '.timestamp // empty')
# Consecutive failure breaker (pinned queue mode)
if [ -n "$QUEUE_FILE" ]; then
  CONSEC_FAILURES=$(awk '/"result"\s*:\s*"(regressed|unchanged)"/{streak++; next} {streak=0} END{print streak+0}' \
    .agents/evolve/cycle-history.jsonl 2>/dev/null)
  if [ "$CONSEC_FAILURES" -ge 5 ]; then
    echo "CIRCUIT BREAKER: 5 consecutive failures in pinned queue mode. Stopping."
    # go to Teardown
  fi
fi

# Time-based circuit breaker: skip when pinned queue has items remaining
if [ -z "$QUEUE_FILE" ] || [ "$QUEUE_INDEX" -ge "$QUEUE_TOTAL" ]; then
  if [ -n "$LAST_PRODUCTIVE_TS" ]; then
    NOW_EPOCH=$(date +%s)
    LAST_EPOCH=$(date -j -f "%Y-%m-%dT%H:%M:%S%z" "$LAST_PRODUCTIVE_TS" +%s 2>/dev/null \
      || date -d "$LAST_PRODUCTIVE_TS" +%s 2>/dev/null || echo 0)
    if [ "$LAST_EPOCH" -gt 1000000000 ] && [ $((NOW_EPOCH - LAST_EPOCH)) -ge 3600 ]; then
      echo "CIRCUIT BREAKER: No productive work in 60+ minutes. Stopping."
      # go to Teardown
    fi
  fi
fi

# Track oscillating goals (improved→fail→improved→fail) to avoid burning cycles
declare -A QUARANTINED_GOALS  # goal_id → true if oscillation count >= 3

# Pre-populate quarantine list from cycle history (lightweight local scan)
if [ -f .agents/evolve/cycle-history.jsonl ]; then
  while IFS= read -r goal; do
    QUARANTINED_GOALS[$goal]=true
    echo "Quarantined oscillating goal: $goal"
  done < <(
    jq -r '.target' .agents/evolve/cycle-history.jsonl 2>/dev/null \
    | awk '{
        if (prev != "" && prev != $0) transitions[$0]++
        prev = $0
      }
      END {
        for (g in transitions) if (transitions[g] >= 3) print g
      }'
  )
fi
```

Parse flags: `--max-cycles=N` (default unlimited), `--dry-run`, `--beads-only`, `--skip-baseline`, `--quality`, `--compile`, `--queue=<file>`.

### Step 0.1: Parse Pinned Queue (--queue only)

Skip if `--queue` was not passed.

If the `--queue` value is not a file path (file does not exist), auto-write the value to `.agents/evolve/roadmap.md` and use that file. This enables inline/prompt-based roadmaps.

Parse the queue file as an ordered markdown checklist:

```bash
if [ -n "$QUEUE_FILE" ] && [ -f "$QUEUE_FILE" ]; then
  QUEUE_ITEMS=()
  declare -A QUEUE_BLOCKERS
  declare -A QUEUE_LINES  # preserve full line per item ID for freeform prompts
  while IFS= read -r line; do
    ITEM_ID=$(echo "$line" | sed -n 's/.*`\([^`]*\)`.*/\1/p' | head -1)
    BLOCKER=$(echo "$line" | sed -n 's/.*blocker:[[:space:]]*`\([^`]*\)`.*/\1/p')
    if [ -n "$ITEM_ID" ]; then
      QUEUE_ITEMS+=("$ITEM_ID")
      QUEUE_LINES["$ITEM_ID"]="$line"
    fi
    [ -n "$BLOCKER" ] && QUEUE_BLOCKERS["$ITEM_ID"]="$BLOCKER"
  done < <(grep -E '^\s*[0-9]+\.' "$QUEUE_FILE")
  QUEUE_TOTAL=${#QUEUE_ITEMS[@]}
fi

# Initialize tracking arrays
PINNED_COMPLETED=()
PINNED_ESCALATED='[]'

# Resume from persisted state
if [ -f .agents/evolve/pinned-queue-state.json ]; then
  QUEUE_INDEX=$(jq -r '.current_index // 0' .agents/evolve/pinned-queue-state.json)
  # Restore completed items array
  mapfile -t PINNED_COMPLETED < <(jq -r '.completed[]? // empty' .agents/evolve/pinned-queue-state.json 2>/dev/null)
  # Load escalated items (both IDs for skip-check and full JSON for state persistence)
  ESCALATED_IDS=$(jq -r '.escalated[]?.id // empty' .agents/evolve/pinned-queue-state.json 2>/dev/null)
  PINNED_ESCALATED=$(jq -c '.escalated // []' .agents/evolve/pinned-queue-state.json 2>/dev/null)
else
  QUEUE_INDEX=0
fi
```

See `references/pinned-queue.md` for format specification, blocker syntax, and state schema.

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
  queue_refresh_count: <incremented after every $rpi cycle>,
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

Skip if `--compile` was not passed or if `--dry-run`.

Run the mechanical half of the Compile cycle to surface fresh signal before the first evolve cycle:

```bash
mkdir -p .agents/mine .agents/defrag
echo "Compile warmup: mining signal..."
ao mine --since 26h --quiet 2>/dev/null || echo "(ao mine unavailable — skipping)"

echo "Compile warmup: defrag sweep..."
ao defrag --prune --dedup --quiet 2>/dev/null || echo "(ao defrag unavailable — skipping)"
```

Then read `.agents/mine/latest.json` and `.agents/defrag/latest.json` and note (in 1-2 sentences each):
- Any **orphaned research** files that look relevant to current goals
- Any **code hotspots** (high-CC functions with recent edits) that may be the root cause of failing goals
- Any **duplicate learnings** merged by defrag — context on what's been cleaned up

These notes inform work selection throughout the evolve session. Store them in a session variable (in-memory), not a file.

### Step 0.5: Baseline (first run only)

Skip if `--skip-baseline` or `--beads-only` or baseline already exists.

```bash
if [ ! -f .agents/evolve/fitness-0-baseline.json ]; then
  bash scripts/evolve-capture-baseline.sh \
    --label "era-$(date -u +%Y%m%dT%H%M%SZ)" \
    --timeout 60
fi
```

### Step 1: Kill Switch Check

Run at the TOP of every cycle:

```bash
CYCLE_START_SHA=$(git rev-parse HEAD)
[ -f ~/.config/evolve/KILL ] && echo "KILL: $(cat ~/.config/evolve/KILL)" && exit 0
[ -f .agents/evolve/STOP ] && echo "STOP: $(cat .agents/evolve/STOP 2>/dev/null)" && exit 0
```

### Step 2: Measure Fitness

Skip if `--beads-only`.

```bash
bash scripts/evolve-measure-fitness.sh \
  --output .agents/evolve/fitness-latest.json \
  --timeout 60 \
  --total-timeout 75
```

**Do NOT write per-cycle `fitness-{N}-pre.json` files.** The rolling file is sufficient for work selection and regression detection.

This writes a fitness snapshot to `.agents/evolve/` atomically via a temp file plus JSON validation. The AgentOps CLI is required for fitness measurement because the wrapper shells out to `ao goals measure`. If measurement exceeds the whole-command bound or returns invalid JSON, the wrapper fails without clobbering the previous rolling snapshot.

### Step 3: Select Work

Selection is a ladder, not a one-shot check. After every productive cycle, return to the TOP of this step and re-read the queue before considering dormancy.

When a repo-local program contract exists, apply a scope filter before Step 4:
- candidate work that clearly requires immutable-scope edits is not eligible for direct execution
- prefer harvested, beads, goals, and generated work that can plausibly land within mutable scope
- if the selected item is inherently out of scope, escalate it or convert it into durable follow-up work instead of invoking `$rpi` and hoping discovery widens scope

**Step 3.0: Pinned work queue** (only when `--queue` is set)

If a pinned queue exists and `QUEUE_INDEX < QUEUE_TOTAL`:

1. Read the current item and set tracking variables:
   ```bash
   CURRENT_ITEM=${QUEUE_ITEMS[$QUEUE_INDEX]}
   CURRENT_LINE=${QUEUE_LINES[$CURRENT_ITEM]}
   ```
2. Skip if this item ID is in the escalated list (log skip reason, advance index, re-enter Step 3.0)
3. Check for declared blocker: `QUEUE_BLOCKERS[$CURRENT_ITEM]`
4. If blocker exists AND blocker is not yet resolved (not in `pinned_queue_completed`):
   - Set `UNBLOCK_TARGET` to the blocker
   - Set `UNBLOCK_DEPTH=0` (increments before each deeper nesting)
   - Proceed to Step 4 with the blocker as the work item
5. If no blocker (or blocker already resolved):
   - Proceed to Step 4 with the queue item as the work item

**Item-to-prompt mapping:**
- If item ID matches a bead (`bd show $CURRENT_ITEM` succeeds), use: `$rpi "Land $CURRENT_ITEM: $(bd show $CURRENT_ITEM --json | jq -r .title)" --auto --max-cycles=1`
- Otherwise, use the preserved full queue line: `$rpi "${QUEUE_LINES[$CURRENT_ITEM]}" --auto --max-cycles=1`

**Escalation cascade guard:** When an item is escalated (skipped), check if subsequent items declare the escalated item as a `blocker:`. If so, those dependent items are also marked escalated. This prevents attempting work that depends on a skipped item.

When pinned queue is active, skip Steps 3.1-3.7 (and 3.0q-3.6q in quality mode) entirely. The queue IS the work source. `--quality` in pinned queue mode affects `$rpi` invocations (via `--quality` passthrough) but does not change the work selection ladder — the queue always takes priority.

When pinned queue is exhausted (`QUEUE_INDEX >= QUEUE_TOTAL`):
- Fall through to normal selection (Steps 3.1-3.7)
- This enables fitness-driven work after roadmap completion

**Step 3.1: Harvested work first**

Read `.agents/rpi/next-work.jsonl` and pick the highest-value unconsumed item for this repo. Prefer:
- exact repo match before `*`, then legacy unscoped entries
- already-harvested concrete implementation work before process work
- higher severity before lower severity

When evolve picks a queue item, **claim it first**:
- set `claim_status: "in_progress"`
- set `claimed_by: "evolve:cycle-N"`
- set `claimed_at: "<timestamp>"`
- keep `consumed: false` until the `$rpi` cycle and regression gate both succeed

If the cycle fails, regresses, or is interrupted before success, release the claim and leave the item available for the next cycle.

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

**Oscillation check:** Before working a failing goal, check if it has oscillated (improved→fail transitions ≥ 3 times in cycle-history.jsonl). If so, quarantine it and try the next failing goal. See `references/oscillation.md`.
```bash
# Count improved→fail transitions for this goal
OSC_COUNT=$(jq -r "select(.target==\"$FAILING\") | .result" .agents/evolve/cycle-history.jsonl \
  | awk 'prev=="improved" && $0=="fail" {count++} {prev=$0} END {print count+0}')
if [ "$OSC_COUNT" -ge 3 ]; then
  QUARANTINED_GOALS[$FAILING]=true
  echo "{\"cycle\":${CYCLE},\"target\":\"${FAILING}\",\"result\":\"quarantined\",\"oscillations\":${OSC_COUNT},\"timestamp\":\"$(date -Iseconds)\"}" >> .agents/evolve/cycle-history.jsonl
fi
```

**Step 3.4: Testing improvements**

Work generators for concrete improvement signals:
- `$test --coverage` — find test gaps and generate candidates
- `$refactor --sweep` — find complexity debt and refactor targets
- `$deps audit` — check dependency health, vulnerabilities, and license compliance
- `$perf profile` — identify performance debt and optimization opportunities

When queues and goals are empty, generate concrete testing work instead of idling:
- find packages/files with thin or missing tests
- look for missing regression tests around recent bug-fix paths
- identify flaky or absent headless/runtime smokes

Convert any real finding into durable work:
- add a bead when the work needs tracked backlog ownership, or
- append a queue item under the shared next-work contract when it should flow directly back into `$rpi`

**Step 3.5: Validation tightening and bug-hunt passes**

If testing improvement generation returns nothing, run bug-hunt and validation sweeps:
- missing validation gates
- weak lint/contract coverage
- bug-hunt style audits for risky areas
- stale assumptions between docs, contracts, and runtime truth

Again: convert findings into beads or queue items, then immediately select the highest-priority result and continue.

**Step 3.6: Drift / hotspot / dead-code mining**

If the prior generators are empty, mine for:
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
- or append a queue item with `source: "feature-suggestion"` when it is ready for the next `$rpi` cycle

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
- Set `consumed: true` only after the $rpi cycle and regression gate succeed
- If the $rpi cycle fails (regression), clear the claim and leave `consumed: false`

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

If `UNBLOCK_TARGET` is set (from Step 3.0), enter the blocker resolution sub-loop:

```text
unblock_loop:
  if UNBLOCK_DEPTH > 2:
    ESCALATE: "Blocker chain too deep (>2 levels). Item: $ITEM_ID, chain: $UNBLOCK_CHAIN"
    Write escalation to .agents/evolve/escalated.md (item, reason, cycle, chain)
    Mark item as escalated in pinned-queue-state.json
    Run escalation cascade: check if subsequent queue items declare this item as blocker
    Advance QUEUE_INDEX to next non-escalated item
    Return to Step 3

  Run: $rpi "Unblock: land $UNBLOCK_TARGET as minimum unblocker" --auto --max-cycles=1

  if unblock succeeded:
    Close/update blocker bead if applicable (bd close $UNBLOCK_TARGET)
    Add UNBLOCK_TARGET to pinned_queue_completed
    Clear UNBLOCK_TARGET, reset UNBLOCK_DEPTH to 0
    UNBLOCK_FAILURES=0
    Persist queue state (atomic write)
    Return to Step 3.0 to re-check the original item (blocker now resolved)

  if unblock failed:
    UNBLOCK_FAILURES++
    if UNBLOCK_FAILURES >= 3:
      ESCALATE: "3 consecutive unblock failures on $UNBLOCK_TARGET"
      Write escalation to .agents/evolve/escalated.md
      Mark item as escalated in pinned-queue-state.json
      Run escalation cascade for dependent items
      Advance QUEUE_INDEX to next non-escalated item
      Return to Step 3

    Dynamic blocker detection — scan $rpi failure output for:
      - bead IDs mentioned in error context (bd show $ID succeeds)
      - dependency keywords ("blocked by", "requires", "depends on")
      - import/build failures pointing to missing prerequisites
    if deeper_blocker found AND UNBLOCK_DEPTH < 2:
      UNBLOCK_DEPTH++
      Push current UNBLOCK_TARGET to UNBLOCK_CHAIN
      Set UNBLOCK_TARGET = deeper_blocker
      goto unblock_loop
    else:
      Retry with narrowed scope: $rpi "Unblock $UNBLOCK_TARGET" --auto --max-cycles=1 --quality
      (--quality forces pre-mortem on the unblock attempt for better diagnosis)
      goto unblock_loop
```

Kill switch is checked at the top of EVERY sub-`$rpi` invocation (inherited from `$rpi`'s own kill switch check). See `references/pinned-queue.md` for full protocol details.

**4.2: Normal Execution**

Primary engine: use `$rpi` for any implementation-quality work. Every `$rpi` call MUST run all 3 phases (discovery → implementation → validation). `$implement` and `$crank` are allowed only when a bead already contains execution-ready scope and skipping discovery is clearly the better path.

If a repo-local `PROGRAM.md` contract is active, `$rpi` will load it automatically. `$evolve` must compose with that behavior, not bypass it:
- Do not select work that is obviously outside mutable scope.
- If a queue item, bead, or goal would require edits under immutable scope, escalate it or convert it into durable follow-up work instead of launching `$rpi`.
- When work is plausibly in scope but still uncertain, let `$rpi` discovery validate the fit and surface a scope escape explicitly.

For a **harvested item, failing goal, directive gap, testing improvement, validation tightening task, bug-hunt result, drift finding, or feature suggestion**:
```
Invoke $rpi "{normalized work title}" --auto --max-cycles=1
```

For a **beads issue**:
```
Prefer: $rpi "Land {issue_id}: {title}" --auto --max-cycles=1
Fallback: $implement {issue_id}
```
Or for an epic with children: `Invoke $crank {epic_id}`.

**CRITICAL:** `$rpi --auto` runs hands-free through all 3 phases. Do NOT intervene, ask questions, or pause between phases. Wait for `$rpi` to return its completion marker, then proceed to Step 5.

If Step 3 created durable work instead of executing it immediately, re-enter Step 3 and let the newly-created queue/bead item win through the normal selection order.

### Step 5: Regression Gate

After execution, run the project build+test bundle. If the repo execution profile declared `validation_commands`, run them. If a repo-local program contract exists, run its `validation_commands` too, de-duplicated and in declared order after the repo bootstrap checks.

```bash
# Detect and run project build+test
if [ -f Makefile ]; then make test
elif [ -f package.json ]; then npm test
elif [ -f go.mod ]; then go build ./... && go vet ./... && go test ./... -count=1 -timeout 120s
elif [ -f Cargo.toml ]; then cargo build && cargo test
elif [ -f pyproject.toml ] || [ -f setup.py ]; then python -m pytest
else echo "No recognized build system found"; fi

# Cross-cutting constraint check (catches wiring regressions)
if [ -f scripts/check-wiring-closure.sh ]; then
  bash scripts/check-wiring-closure.sh
else
  echo "WARNING: scripts/check-wiring-closure.sh not found — skipping wiring check"
fi
```

Use the program contract's `decision_policy` as the first keep/revert rule set for the cycle:
- if the cycle breached immutable scope, treat it as regressed
- if program validation commands fail, treat it as regressed
- if the decision policy declares a revert rule that fired, revert before consuming claimed work or advancing the queue

Treat program `stop_conditions` as per-cycle done criteria. Do not mark claimed work consumed, completed, or productive until both the stop conditions and the regression gate pass.

If not `--beads-only`, also re-measure to produce a post-cycle snapshot:
```bash
bash scripts/evolve-measure-fitness.sh \
  --output .agents/evolve/fitness-latest-post.json \
  --timeout 60 \
  --total-timeout 75 \
  --goal "$GOAL_ID"

# Extract goal counts for cycle history entry
PASSING=$(jq '[.goals[] | select(.result=="pass")] | length' .agents/evolve/fitness-latest-post.json 2>/dev/null || echo 0)
TOTAL=$(jq '.goals | length' .agents/evolve/fitness-latest-post.json 2>/dev/null || echo 0)
```

**If regression detected** (previously-passing goal now fails):
```bash
git revert HEAD --no-edit  # single commit
# or for multiple commits:
git revert --no-commit ${CYCLE_START_SHA}..HEAD && git commit -m "revert: evolve cycle ${CYCLE} regression"
```
Set outcome to "regressed".

Queue finalization after the regression gate:
- **success:** finalize any claimed queue item with `consumed: true`, `consumed_by`, and `consumed_at`; clear transient claim fields
- **failure/regression:** clear `claim_status`, `claimed_by`, and `claimed_at`; keep `consumed: false`; record the release in `session-state.json`

After the cycle's `$post-mortem` finishes, immediately re-read `.agents/rpi/next-work.jsonl` before selecting the next item. Never assume the queue state from before the cycle.

### Step 6: Log Cycle + Commit

Two paths: productive cycles get committed, idle cycles are local-only.

**PRODUCTIVE cycles** (result is improved, regressed, or harvested):

```bash
# Quality mode: compute quality_score BEFORE writing the JSONL entry
QUALITY_SCORE_ARGS=()
if [ "$QUALITY_MODE" = "true" ]; then
  REMAINING_HIGH=$(jq -r 'select(.consumed==false) | .items[] | select(.severity=="high")' \
    .agents/rpi/next-work.jsonl 2>/dev/null | wc -l | tr -d ' ')
  REMAINING_MEDIUM=$(jq -r 'select(.consumed==false) | .items[] | select(.severity=="medium")' \
    .agents/rpi/next-work.jsonl 2>/dev/null | wc -l | tr -d ' ')
  QUALITY_SCORE=$((100 - (REMAINING_HIGH * 10) - (REMAINING_MEDIUM * 3)))
  [ "$QUALITY_SCORE" -lt 0 ] && QUALITY_SCORE=0
  QUALITY_SCORE_ARGS=(--quality-score "$QUALITY_SCORE")
fi

# Pinned queue fields (appended to cycle entry when active)
QUEUE_ARGS=()
if [ -n "$QUEUE_FILE" ]; then
  QUEUE_ARGS=(--queue-item "${CURRENT_ITEM:-}" --queue-index "$QUEUE_INDEX" --queue-total "$QUEUE_TOTAL")
  [ -n "$UNBLOCK_TARGET" ] && QUEUE_ARGS+=(--unblock-target "$UNBLOCK_TARGET" --unblock-depth "$UNBLOCK_DEPTH")
fi

ENTRY_JSON="$(
  bash scripts/evolve-log-cycle.sh \
    --cycle "$CYCLE" \
    --target "$TARGET" \
    --result "$OUTCOME" \
    --canonical-sha "$(git rev-parse --short HEAD)" \
    --cycle-start-sha "$CYCLE_START_SHA" \
    --goals-passing "$PASSING" \
    --goals-total "$TOTAL" \
    "${QUALITY_SCORE_ARGS[@]}" \
    "${QUEUE_ARGS[@]}"
)"
OUTCOME="$(printf '%s\n' "$ENTRY_JSON" | jq -r '.result')"
REAL_CHANGES=$(git diff --name-only "${CYCLE_START_SHA}..HEAD" -- ':!.agents/**' ':!GOALS.yaml' ':!GOALS.md' \
  2>/dev/null | wc -l | tr -d ' ')

# Telemetry
bash scripts/log-telemetry.sh evolve cycle-complete cycle=${CYCLE} goal=${TARGET} outcome=${OUTCOME} 2>/dev/null || true

if [ "$OUTCOME" = "unchanged" ]; then
  # No-delta cycle: leave local-only so history stays honest and stagnation logic can see it.
  :
elif [ "$REAL_CHANGES" -gt 0 ]; then
  # Full commit: real code was changed
  git add .agents/evolve/cycle-history.jsonl
  git commit -m "evolve: cycle ${CYCLE} -- ${TARGET} ${OUTCOME}"
else
  # Productive cycle with non-agent repo delta already committed by a sub-skill:
  # stage the ledger but do not create a standalone follow-up commit.
  git add .agents/evolve/cycle-history.jsonl
fi

PRODUCTIVE_THIS_SESSION=$((PRODUCTIVE_THIS_SESSION + 1))

# Advance pinned queue after successful cycle (not unblock sub-cycles)
if [ -n "$QUEUE_FILE" ] && [ -z "$UNBLOCK_TARGET" ] && [ "$OUTCOME" != "regressed" ] && [ "$OUTCOME" != "failed" ]; then
  PINNED_COMPLETED+=("$CURRENT_ITEM")
  QUEUE_INDEX=$((QUEUE_INDEX + 1))
  # Persist queue state (atomic write via temp file)
  TMP=$(mktemp .agents/evolve/pinned-queue-state.XXXXXX.json)
  jq -n --arg file "$QUEUE_FILE" --argjson idx "$QUEUE_INDEX" \
    --argjson completed "$(printf '%s\n' "${PINNED_COMPLETED[@]}" | jq -R . | jq -s .)" \
    --argjson escalated "$PINNED_ESCALATED" \
    '{queue_file: $file, current_index: $idx, completed: $completed, in_progress: null, escalated: $escalated, unblock_chain: []}' \
    > "$TMP" && jq . "$TMP" >/dev/null 2>&1 && mv "$TMP" .agents/evolve/pinned-queue-state.json
fi
```

**IDLE cycles** (nothing found even after generator layers):

```bash
bash scripts/evolve-log-cycle.sh \
  --cycle "$CYCLE" \
  --target "idle" \
  --result "unchanged" >/dev/null
# No git add, no git commit, no fitness snapshot write
```

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

1. Commit any staged but uncommitted cycle-history.jsonl (from artifact-only cycles):
```bash
if git diff --cached --name-only | grep -q cycle-history.jsonl; then
  git commit -m "evolve: session teardown -- artifact-only cycles logged"
fi
```
2. Run `$post-mortem "evolve session: ${CYCLE} cycles"` to harvest learnings.
3. Push only if unpushed commits exist:
```bash
UNPUSHED=$(git log origin/main..HEAD --oneline 2>/dev/null | wc -l)
[ "$UNPUSHED" -gt 0 ] && git push
```
4. Report summary:

```
## $evolve Complete
Cycles: N | Productive: X | Regressed: Y (reverted) | Idle: Z
Stop reason: stagnation | circuit-breaker | max-cycles | kill-switch
```

In quality mode, the report includes additional fields:
```
## $evolve Complete (quality mode)
Cycles: N | Findings resolved: X | Goals fixed: Y | Idle: Z
Quality score: start → end (delta)
Remaining unconsumed: H high, M medium
Stop reason: stagnation | circuit-breaker | max-cycles | kill-switch
```

In pinned queue mode, the report includes:
```
## $evolve Complete (pinned queue mode)
Queue: X/Y items completed | Unblocked: U items | Escalated: E items
Cycles: N | Productive: P | Regressed: R (reverted)
Stop reason: queue-complete | escalated | circuit-breaker | kill-switch
Remaining items: [list of uncompleted item IDs]
```

## Examples

**User says:** `$evolve --max-cycles=5`
**What happens:** Evolve re-enters the full selection ladder after every `$rpi` cycle and runs producer layers instead of idling on empty queues.

**User says:** `$evolve --beads-only`
**What happens:** Evolve skips goals measurement and works through `bd ready` backlog.

**User says:** `$evolve --dry-run`
**What happens:** Evolve shows what would be worked on without executing.

**User says:** `$evolve --compile`
**What happens:** Evolve runs `ao mine` + `ao defrag` at session start to surface fresh signal (orphaned research, code hotspots, oscillating goals) before the first evolve cycle. Use before a long autonomous run or after a burst of development activity.

**User says:** `$evolve`
**What happens:** See `references/examples.md` for a worked overnight flow that moves through beads -> harvested work -> goals -> testing -> bug hunt -> feature suggestion before dormancy is considered.

**User says:** `$evolve --queue=.agents/evolve/roadmap.md --test-first`
**What happens:** Evolve processes each item in the roadmap sequentially. When an item is blocked (e.g., `rig-difc` blocked by `rig-8z29`), evolve auto-lands `rig-8z29` via sub-`$rpi` first, then resumes `rig-difc`. After all queue items complete, evolve falls through to fitness-driven selection. If a blocker chain exceeds 2 levels or fails 3 times, the item is escalated and evolve moves to the next one.

**User says:** `$evolve --queue=.agents/evolve/roadmap.md --max-cycles=20`
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
- `references/parallel-execution.md` — Parallel $swarm architecture
- `references/teardown.md` — Trajectory computation and session summary
- `references/examples.md` — Detailed usage examples
- `references/artifacts.md` — Generated files registry
- `references/oscillation.md` — Oscillation detection and quarantine
- `references/quality-mode.md` — Quality-first mode: scoring, priority cascade, artifacts
- `references/pinned-queue.md` — Pinned queue format, blocker resolution, state persistence

## See Also

- `skills/rpi/SKILL.md` — Full lifecycle orchestrator (called per cycle)
- `skills/crank/SKILL.md` — Epic execution (called for beads epics)
- `docs/contracts/autodev-program.md` — Repo-local operational contract for bounded autonomous development
- `GOALS.yaml` — Fitness goals for this repo
- [test](../test/SKILL.md) — Test generation and coverage analysis
- [refactor](../refactor/SKILL.md) — Safe, verified refactoring for complexity targets
- [deps](../deps/SKILL.md) — Dependency audit, vulnerability scanning, and license compliance
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
- [references/pinned-queue.md](references/pinned-queue.md)
- [references/teardown.md](references/teardown.md)

## Local Resources

### references/

- [references/artifacts.md](references/artifacts.md)
- [references/compounding.md](references/compounding.md)
- [references/cycle-history.md](references/cycle-history.md)
- [references/examples.md](references/examples.md)
- [references/goals-schema.md](references/goals-schema.md)
- [references/oscillation.md](references/oscillation.md)
- [references/parallel-execution.md](references/parallel-execution.md)
- [references/pinned-queue.md](references/pinned-queue.md)
- [references/quality-mode.md](references/quality-mode.md)
- [references/teardown.md](references/teardown.md)

### scripts/

- `scripts/validate.sh`


<!-- Lifecycle integration wired: 2026-03-28. See skills/evolve/SKILL.md for canonical -->
