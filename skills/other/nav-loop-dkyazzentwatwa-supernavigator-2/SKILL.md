---
name: nav-loop
description: Run tasks until complete with structured completion signals. Auto-invoke when user says "run until done", "keep going until complete", "iterate until finished", "loop mode", "autonomous mode".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion
version: 1.0.0
---

# Navigator Loop Skill

Execute tasks iteratively until completion with structured signals, stagnation detection, and dual-condition exit gates.

## Why This Exists

Traditional AI coding requires manual "keep going" prompts. Navigator Loop provides:
- **Structured completion signals** (NAVIGATOR_STATUS block)
- **Dual-condition exit gate** (heuristics + explicit signal)
- **Stagnation detection** (circuit breaker for stuck loops)
- **Progress visibility** (phases: INIT → RESEARCH → IMPL → VERIFY → COMPLETE)

Based on Ralph's autonomous loop innovations, adapted for Navigator's context-efficient architecture.

## When to Invoke

**Auto-invoke when**:
- User says "run until done", "keep going until complete"
- User says "iterate until finished", "autonomous mode"
- User says "loop mode", "don't stop until done"
- Task document has `loop_mode: true`

**DO NOT invoke if**:
- Single-step task (no iteration needed)
- User says "just do this once"
- Already in loop mode (prevent nested loops)
- User explicitly disabled loop mode

## Configuration

Loop mode settings in `.agent/.nav-config.json`:

```json
{
  "loop_mode": {
    "enabled": false,
    "max_iterations": 5,
    "stagnation_threshold": 3,
    "exit_requires_explicit_signal": true,
    "show_status_block": true
  }
}
```

**Options**:
- `enabled`: Default state for new tasks
- `max_iterations`: Hard cap to prevent infinite loops (1-20)
- `stagnation_threshold`: Same-state count before pause (2-5)
- `exit_requires_explicit_signal`: Require EXIT_SIGNAL alongside heuristics

## Execution Steps

### Step 1: Initialize Loop State

**Load configuration**:
```bash
python3 functions/phase_detector.py --init
```

**Initialize tracking variables**:
```
iteration = 1
max_iterations = config.loop_mode.max_iterations or 5
stagnation_threshold = config.loop_mode.stagnation_threshold or 3
hash_history = []
phase = "INIT"
```

**Display loop start**:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LOOP MODE ACTIVATED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Task: {TASK_DESCRIPTION}
Max iterations: {max_iterations}
Stagnation threshold: {stagnation_threshold}

Starting iteration 1...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Step 2: Execute Iteration

**Perform task work** based on current phase:

| Phase | Actions |
|-------|---------|
| INIT | Load context, understand requirements |
| RESEARCH | Explore codebase, find patterns |
| IMPL | Write code, make changes |
| VERIFY | Run tests, validate functionality |
| COMPLETE | All indicators met, ready to exit |

**Track changes during iteration**:
- Files read (for RESEARCH detection)
- Files changed (for IMPL detection)
- Tests run (for VERIFY detection)
- Commits made (for completion indicator)

### Step 3: Generate Status Block

**After each iteration**, generate NAVIGATOR_STATUS:

```bash
python3 functions/status_generator.py \
  --phase "{phase}" \
  --iteration "{iteration}" \
  --max-iterations "{max_iterations}" \
  --indicators "{indicators_json}" \
  --state-hash "{current_hash}" \
  --prev-hash "{previous_hash}" \
  --stagnation-count "{stagnation_count}"
```

**Display status block**:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NAVIGATOR_STATUS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Phase: {PHASE}
Iteration: {N}/{MAX}
Progress: {PERCENT}%

Completion Indicators:
  [{x or space}] Code changes committed
  [{x or space}] Tests passing
  [{x or space}] Documentation updated
  [{x or space}] Ticket closed
  [{x or space}] Marker created

Exit Conditions:
  Heuristics: {MET}/{TOTAL} (need 2+)
  EXIT_SIGNAL: {true/false}

State Hash: {HASH}
Previous Hash: {PREV_HASH}
Stagnation: {COUNT}/{THRESHOLD}

Next Action: {NEXT_ACTION}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Step 4: Check Stagnation

**Calculate state hash**:
```bash
python3 functions/stagnation_detector.py \
  --phase "{phase}" \
  --indicators "{indicators_json}" \
  --files-changed "{files_json}" \
  --history "{hash_history_json}"
```

**If stagnation detected** (same hash for N iterations):

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STAGNATION DETECTED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Same state detected for {N} consecutive iterations.

Current State:
  Phase: {PHASE}
  Indicators: {MET}/{TOTAL}
  Last Action: {LAST_ACTION}

Possible causes:
1. Blocked by external dependency
2. Unclear requirements
3. Test failures preventing progress
4. Missing context or permissions

Options:
1. [Continue] - Try one more iteration
2. [Clarify] - Explain what's blocking
3. [Abort] - End loop, manual intervention

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Use AskUserQuestion** for choice:
- Continue: Reset stagnation counter, continue loop
- Clarify: User explains blocker, incorporate and continue
- Abort: Exit loop with partial completion marker

### Step 5: Check Exit Conditions

**Evaluate dual-condition gate**:
```bash
python3 functions/exit_gate.py \
  --indicators "{indicators_json}" \
  --exit-signal "{exit_signal}" \
  --require-explicit "{config.exit_requires_explicit_signal}"
```

**Exit conditions**:
1. **Heuristics**: At least 2 completion indicators met
2. **EXIT_SIGNAL**: Explicit signal that task is complete

**Completion indicators** (mapped from autonomous protocol):
- `code_committed`: Changes committed to git
- `tests_passing`: Test suite passes (exit code 0)
- `docs_updated`: Documentation files changed
- `ticket_closed`: PM tool ticket marked done
- `marker_created`: Completion marker exists

**Exit decision logic**:
```
IF heuristics >= 2 AND exit_signal == true:
  → EXIT: Task complete
ELIF heuristics >= 2 AND exit_signal == false:
  → CONTINUE: Awaiting explicit completion signal
ELIF exit_signal == true AND heuristics < 2:
  → BLOCKED: Cannot exit with insufficient indicators
ELSE:
  → CONTINUE: More work needed
```

### Step 6: Handle Max Iterations

**If iteration >= max_iterations**:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MAX ITERATIONS REACHED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Completed {MAX} iterations without full completion.

Current State:
  Phase: {PHASE}
  Indicators: {MET}/{TOTAL}
  EXIT_SIGNAL: {true/false}

Progress made:
- {PROGRESS_ITEM_1}
- {PROGRESS_ITEM_2}

Options:
1. [Extend] - Add 3 more iterations
2. [Complete] - Accept current state as done
3. [Abort] - Exit without completion

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Step 7: Complete Loop

**When exit conditions met**, display completion:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LOOP COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Task: {TASK_DESCRIPTION}
Iterations: {FINAL_COUNT}/{MAX}
Final Phase: COMPLETE

Completion Indicators:
  [x] Code changes committed
  [x] Tests passing
  [x] Documentation updated
  [ ] Ticket closed (skipped - no PM tool)
  [x] Marker created

Exit Conditions:
  Heuristics: 4/5 (passed)
  EXIT_SIGNAL: true (passed)

Summary:
- {KEY_CHANGE_1}
- {KEY_CHANGE_2}
- {KEY_CHANGE_3}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Execute autonomous completion protocol**:
1. Commit changes (if not already)
2. Archive task documentation
3. Close ticket (if PM configured)
4. Create completion marker (with loop state)
5. Suggest compact

---

## Setting EXIT_SIGNAL

The EXIT_SIGNAL is set **explicitly by Claude** when:
- All primary task requirements are met
- Code is functional and tested
- No obvious remaining work

**How to signal completion**:
```
I've completed the implementation. All requirements met.

EXIT_SIGNAL: true
```

This explicit declaration prevents premature exits when heuristics are met but work remains.

---

## Phase Detection

Phases auto-detected based on context:

```python
def detect_phase(context):
    # COMPLETE: Exit conditions met
    if indicators_met >= 4 and exit_signal:
        return "COMPLETE"

    # VERIFY: Tests running or recently run
    if context.tests_running or context.test_exit_code is not None:
        return "VERIFY"

    # IMPL: Files being modified
    if context.files_changed:
        return "IMPL"

    # RESEARCH: Reading files, searching
    if context.files_read and not context.files_changed:
        return "RESEARCH"

    # INIT: Default starting state
    return "INIT"
```

---

## Integration with Navigator

### With Autonomous Completion
Loop mode enhances (not replaces) the autonomous protocol:
- Completion indicators map to autonomous steps
- EXIT_SIGNAL triggers autonomous completion
- Marker includes loop state for restoration

### With nav-diagnose
Stagnation triggers nav-diagnose quality check:
- 3 same-state loops = potential quality issue
- nav-diagnose helps identify root cause
- Re-anchoring can resolve stuck loops

### With nav-marker
Markers capture loop state:
- Current iteration and max
- Phase at time of marker
- State hash for continuity
- Completion indicators status

### With ToM Features
Loop mode respects ToM configuration:
- Verification checkpoints still apply in VERIFY phase
- Profile preferences affect communication style
- Belief anchors can help clarify stuck states

---

## Predefined Functions

### functions/status_generator.py
Generates formatted NAVIGATOR_STATUS block.

### functions/exit_gate.py
Evaluates dual-condition exit (heuristics + explicit signal).

### functions/stagnation_detector.py
Calculates state hash and detects consecutive same-states.

### functions/phase_detector.py
Auto-detects current task phase from context.

---

## Error Handling

**Config not found**:
```
Loop mode config not found in .nav-config.json.
Using defaults: max_iterations=5, stagnation_threshold=3
```

**Function execution fails**:
- Fall back to manual evaluation
- Log error but don't interrupt loop
- Continue with best-effort phase detection

**User aborts mid-loop**:
- Create partial completion marker
- Document progress made
- List remaining work

---

## Success Criteria

Loop mode succeeds when:
- [ ] Task completes within max_iterations
- [ ] No stagnation pauses (or resolved quickly)
- [ ] EXIT_SIGNAL + heuristics both satisfied
- [ ] Completion marker includes loop state
- [ ] User sees clear progress each iteration

---

## Examples

### Example 1: Simple Feature
```
User: "Run until done: add isPrime function with tests"

Iteration 1 (INIT → RESEARCH):
  - Read existing math utils
  - Found test patterns

Iteration 2 (IMPL):
  - Created isPrime function
  - Created test file

Iteration 3 (VERIFY):
  - Ran tests: PASS
  - Committed changes
  EXIT_SIGNAL: true

→ Loop complete in 3 iterations
```

### Example 2: Stagnation Recovery
```
User: "Run until done: fix authentication bug"

Iteration 1-3 (IMPL):
  - Same changes attempted
  - Tests still failing
  - State hash unchanged

→ STAGNATION DETECTED

User: "The test needs a mock for the auth service"

Iteration 4 (IMPL):
  - Added mock
  - Tests pass
  EXIT_SIGNAL: true

→ Loop complete in 4 iterations
```

---

## Limitations

**Cannot handle**:
- External blockers (waiting for API, permissions)
- Subjective completion criteria ("make it look nice")
- Tasks requiring human judgment mid-loop

**Should not use for**:
- Quick fixes (single iteration sufficient)
- Exploratory work (no clear completion state)
- Tasks with security implications (need human review)

---

**This skill provides Ralph-style "run until done" capability while maintaining Navigator's context efficiency and ToM integration.**
