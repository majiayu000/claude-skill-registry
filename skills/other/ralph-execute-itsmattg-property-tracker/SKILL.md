---
name: ralph-execute
description: Autonomous execution loop that processes a Beads epic task-by-task with fresh subagents, two-stage review, and circuit breaker safety. Use after plan-to-epic creates the epic.
disable-model-invocation: true
---

# Ralph Execute — Autonomous Epic Runner

Process a Beads epic autonomously, dispatching fresh subagents per task with two-stage review gates.

## Arguments

- First argument: Beads epic ID (required)
- `--dry-run`: Show what would execute without doing it (optional)

## Pre-Flight Checks

Before starting the loop:

1. **Verify epic exists**: `bd show <epic-id>`
2. **Check ready tasks**: `bd ready --parent <epic-id>` — must have at least one
3. **Verify worktree**: Must be in a worktree, not main repo (enforced by block-work-on-develop hook)
4. **Initialize circuit breaker**: `.claude/hooks/circuit-breaker.sh reset`
5. **Create session marker**: `mkdir -p .ralph-session/questions .ralph-session/answers .ralph-session/messages`
6. **Notify start**: Send ntfy notification "Ralph starting epic <id>"
7. **Set phase to IMPLEMENT**: If `.claude/phases/output/current-phase.json` exists and `current_phase` is not `implement`, update it:
   ```bash
   PHASE_FILE=".claude/phases/output/current-phase.json"
   if [[ -f "$PHASE_FILE" ]]; then
     python3 -c "
   import json
   with open('$PHASE_FILE') as f: state = json.load(f)
   if state.get('current_phase') != 'implement':
       completed = state.get('completed_phases', [])
       if state.get('current_phase') and state['current_phase'] not in completed:
           completed.append(state['current_phase'])
       state['current_phase'] = 'implement'
       state['completed_phases'] = completed
       with open('$PHASE_FILE', 'w') as f: json.dump(state, f, indent=2)
   "
   fi
   ```
   If no phase file exists, create one:
   ```bash
   mkdir -p .claude/phases/output
   echo '{"topic":"<epic-name>","current_phase":"implement","completed_phases":["research","plan"],"output_files":{}}' > "$PHASE_FILE"
   ```

## Execution Loop

For each task from `bd ready --parent <epic-id>`:

### Step A: Claim Task
```bash
bd update <task-id> --status in_progress
```

Log activity and update monitor:
```bash
echo "[$(date +%H:%M)] Task <task-id> started: <title>" >> .ralph-session/ralph.log
.claude/hooks/circuit-breaker.sh write-status "<task-id>" "<title>" <total> <completed> <mode>
```

### Step A.5: Plan Pass (First Iteration Only)

For the FIRST iteration of each task, run a gap analysis:

```bash
.claude/hooks/generate-prompt.sh <task-id> .ralph-session/PROMPT.md plan
```

Dispatch a read-only subagent (model: haiku) with the plan-mode PROMPT.md.
The subagent writes findings to `.ralph-session/gap-analysis.md`.

**Validate plan pass output:**
After the plan subagent completes, verify `.ralph-session/gap-analysis.md` exists and has content:
```bash
if [[ ! -f ".ralph-session/gap-analysis.md" ]] || [[ $(wc -w < ".ralph-session/gap-analysis.md") -lt 20 ]]; then
  echo "[Ralph] Plan pass failed — no gap analysis produced" >> .ralph-session/ralph.log
  .claude/hooks/circuit-breaker.sh record-failure
  # Skip to next task
  continue
fi
```

Read the gap analysis before proceeding to build mode. Use it to inform
the implementation subagent's context.

### Step B: Generate PROMPT.md
```bash
.claude/hooks/generate-prompt.sh <task-id> .ralph-session/PROMPT.md build
```

### Step C: Check Circuit Breaker
```bash
.claude/hooks/circuit-breaker.sh check
```
If PAUSED — stop loop, notify human, exit.
If DEGRADED — wait 30 seconds (`sleep 30`) as a backoff, then continue.

### Step D: Dispatch Subagent

Launch a Task subagent with the PROMPT.md content. The subagent:
- Reads the generated PROMPT.md
- Implements the task following the rules
- Runs verification commands (test, lint, typecheck)
- Outputs `RALPH_COMPLETE` when done
- Writes completion signal: `echo "RALPH_COMPLETE" > .ralph-session/completion-signal`

### Step D.5: Handle Escalation

After the subagent returns, check if it escalated:

**If result contains `ESCALATE:`:**
1. Read the question file:
   ```bash
   cat .ralph-session/questions/<task-id>.json
   ```
2. Log the escalation:
   ```bash
   echo "[$(date +%H:%M)] Task <task-id> ESCALATED: <summary>" >> .ralph-session/ralph.log
   ```
3. Ask the user the question directly in your response text. Include the full question, context, and options from the JSON file.
4. Write the user's answer to `.ralph-session/answers/<task-id>.json`:
   ```json
   {"task_id":"<task-id>","answer":"<user's response>","timestamp":"<iso>"}
   ```
5. **Dispatch a new subagent** with a Task call that includes the user's answer in the prompt context, along with the original task description and any partial work from `.ralph-session/`.
6. After the new subagent completes, proceed to Step E as normal.

**If result contains `RALPH_COMPLETE`:**
Proceed to Step E.

**If result contains neither:**
The subagent may have failed silently. Record failure and proceed:
```bash
.claude/hooks/circuit-breaker.sh record-failure
echo "[$(date +%H:%M)] Task <task-id> returned without completion signal" >> .ralph-session/ralph.log
```

### Step E: Two-Stage Review

**Stage 1 — Spec Compliance:**
Launch a review subagent that compares the code changes against the task description.
Check: Does the implementation match what was requested? Any missing requirements?

**Stage 2 — Code Quality:**
Launch the code-reviewer agent (`.claude/agents/code-reviewer.md`).
Check: Anti-patterns, security, test coverage, conventions.

### Step F: Handle Review Results

**If both pass:**
```bash
.claude/hooks/circuit-breaker.sh record-success
bd close <task-id>
curl -s -X POST "https://ntfy.sh/property-tracker-claude" \
  -d "Task <task-id> complete" -H "Title: Ralph Progress"
```
Clean up: `rm -f .ralph-session/completion-signal`

Log completion:
```bash
echo "[$(date +%H:%M)] Task <task-id> completed (pass@1)" >> .ralph-session/ralph.log
```

**If either fails:**
```bash
.claude/hooks/circuit-breaker.sh record-failure
```
Dispatch a fix subagent with the review feedback. Then re-run Step E.
Max 3 fix attempts per task (enforced by circuit breaker).

### Step F.5: Record to eval-tracker

After each task resolution (pass or max-attempts-exceeded), append to `.claude/instincts/eval-tracker.jsonl`:

```bash
echo "{\"task_id\":\"<task-id>\",\"epic_id\":\"<epic-id>\",\"attempts\":1,\"fix_attempts\":<N>,\"passed\":<true|false>,\"date\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"branch\":\"$(git branch --show-current)\",\"duration_sec\":<elapsed>,\"skill_context\":[\"<instinct-id-1>\",\"<instinct-id-2>\"]}" >> .claude/instincts/eval-tracker.jsonl
```

Where:
- `attempts`: always 1 (one dispatch per task)
- `fix_attempts`: 0 if passed on first try, 1-3 for fix iterations
- `passed`: true if eventually passed review, false if max attempts exceeded
- `duration_sec`: wall-clock seconds from dispatch to completion
- `skill_context`: array of instinct IDs that were active (injected via `{{LEARNED_PATTERNS}}`) when this task was dispatched. Enables `/eval-report` Step 4 to measure per-instinct effectiveness.

### Step G: Next Task

Loop back to Step A with the next `bd ready --parent <epic-id>` task.

## Exit Conditions

The loop exits when ANY of these are true:
1. `bd ready --parent <epic-id>` returns no tasks (epic complete)
2. Circuit breaker enters PAUSED state
3. User manually creates `.ralph-session/STOP` file

## Cleanup

On exit (success or circuit breaker), save summary before deleting session evidence:
```bash
# Preserve session summary for post-mortem analysis
mkdir -p .claude/agent-memory/ralph
if [[ -f .ralph-session/circuit-breaker.json ]]; then
  cp .ralph-session/circuit-breaker.json ".claude/agent-memory/ralph/session-$(date +%Y%m%d-%H%M%S).json"
fi
rm -rf .ralph-session
```

**Phase Advance (auto):**
After all tasks complete (not on PAUSED exit):
```bash
PHASE_FILE=".claude/phases/output/current-phase.json"
TOPIC=$(python3 -c "import json; print(json.load(open('$PHASE_FILE')).get('topic','unknown'))" 2>/dev/null)

# Run checkpoint evaluation
CHECKPOINT_RESULT=$(.claude/hooks/checkpoint-eval.sh implement review "$TOPIC" 2>&1)
CHECKPOINT_EXIT=$?

if [[ "$CHECKPOINT_EXIT" -eq 0 ]]; then
  python3 -c "
import json
with open('$PHASE_FILE') as f: state = json.load(f)
state['completed_phases'] = list(set(state.get('completed_phases', []) + ['implement']))
state['current_phase'] = 'review'
with open('$PHASE_FILE', 'w') as f: json.dump(state, f, indent=2)
"
  echo "Phase advanced to REVIEW"
else
  echo "Phase remains IMPLEMENT — checkpoint failed: $CHECKPOINT_RESULT"
fi
```

On PAUSED exit, do NOT advance phase — user intervention needed.

Send final notification:
```bash
curl -s -X POST "https://ntfy.sh/property-tracker-claude" \
  -d "Ralph finished epic <id>. Status: <complete|paused>" \
  -H "Title: Ralph Done" -H "Priority: high"
osascript -e 'display notification "Ralph finished" with title "Claude Code"'
```

## Safety Guarantees

- All 17 existing hooks remain active (lint, anti-patterns, security, auth checks)
- Circuit breaker prevents infinite loops (max 3 failures per task, max 5 iterations without progress)
- Fresh subagent per task prevents context pollution
- Two-stage review catches both spec drift and quality issues
- ntfy notifications on every state change

## Language Patterns (From Ghuntley Research)

When generating PROMPT.md, these language patterns improve subagent performance:
- "Study" not "read" or "look at" — triggers deeper analysis
- "Don't assume not implemented" — prevents hallucinated code
- "Using parallel subagents" — explicit parallelism instruction
- "Only 1 subagent for build/tests" — enforces backpressure
- "Capture the why" — documentation emphasis
