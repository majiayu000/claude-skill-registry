---
name: failure-recovery
description: "Recovery protocols for stuck agents, context exhaustion, build failures, and confusion. Use when agent is looping, responses degrading, builds failing repeatedly, or user says 'you're stuck' or 'start over'."
allowed-tools: Read, Bash, Glob, Grep
---

# Failure Recovery

Recovery protocols when things go wrong. Don't panic - follow these systematic approaches.

## When To Use

- Agent is looping or repeating the same action
- Responses are getting shorter or missing context
- Build/tests failing repeatedly (3+ times)
- User says "you're stuck", "start over", "lost", "confused"
- Project state feels inconsistent

---

## Build Failure Recovery

**Trigger**: Tests fail, build errors, runtime crashes

```yaml
recovery_build_failure:
  step_1_isolate:
    - "pytest tests/ -x --tb=short"  # Stop at first failure
    - "git diff HEAD~1"              # What changed?

  step_2_rollback_test:
    - "git stash"
    - "git checkout HEAD~1"
    - "pytest tests/"                # Verify it works

  step_3_bisect_if_needed:
    - "git bisect start"
    - "git bisect bad HEAD"
    - "git bisect good [last-good-commit]"

  step_4_fix:
    rule: "Fix the bug, don't refactor"
    avoid: "No cleanup, no improvements, just fix"

  step_5_verify:
    - "pytest tests/"
    - "git stash pop"  # If we stashed changes
```

**Key principle**: Smallest change that fixes the issue. Do NOT refactor while debugging.

---

## Agent Confusion Recovery

**Trigger**: Looping, contradicting self, asking already-answered questions

```yaml
recovery_agent_confusion:
  symptoms:
    - "Repeating same action without progress"
    - "Contradicting previous statements"
    - "Asking questions already answered"
    - "Making changes that break previously working code"

  step_1_restate:
    action: |
      STOP. Let's reset.
      Current phase: [Phase X]
      Current task: [Task Y]
      Last successful action: [What worked]

  step_2_narrow_focus:
    action: |
      Focus only on: [single file]
      Specific change: [exact change needed]
      Do not touch other files.

  step_3_verify_understanding:
    action: |
      Before proceeding, confirm:
      1. What file are we changing?
      2. What exact change?
      3. Why this change?

  step_4_checkpoint:
    action: "Update TODO.md before continuing"
```

---

## Context Window Exhaustion

**Trigger**: Responses getting shorter, missing earlier context, forgetting decisions

```yaml
recovery_context_exhaustion:
  symptoms:
    - "Responses noticeably shorter"
    - "Forgetting earlier decisions"
    - "Re-asking questions already answered"
    - "Missing important context from earlier"

  prevention:
    - "Use TODO.md for task state"
    - "Keep LLM-OVERVIEW.md updated"
    - "Don't paste entire files unnecessarily"
    - "Reference file:line instead of copying code"

  recovery:
    step_1_handoff:
      action: "Generate handoff state document"
      template: |
        ## HANDOFF STATE
        **Project**: [name]
        **Timestamp**: [now]

        ### Completed
        - [list from TODO.md Done section]

        ### In Progress
        - [current task + status]

        ### Next Action (BE SPECIFIC)
        1. Open file: [exact path]
        2. Find: [function/line]
        3. Do: [exact change]

        ### Critical Context
        - [decisions made]
        - [blockers encountered]

    step_2_new_session:
      action: |
        Start new session. Read in order:
        1. LLM-OVERVIEW.md
        2. TODO.md
        3. Handoff document
        Confirm understanding before proceeding.
```

---

## Predictive Context Management (PROACTIVE)

**NEW in v7.4**: Don't wait for exhaustion - predict and prevent.

### Token Usage Estimation

Track rolling average of tokens per operation:

| Operation | Avg Tokens |
|-----------|------------|
| File read | ~500 |
| Grep result (per match) | ~200 |
| Tool output | ~1000 |
| Subagent summary | ~300 |
| User message | ~100 |

### Pre-emptive Action Thresholds

| Context Level | Prediction | Action |
|---------------|------------|--------|
| **<30%** | Safe zone | Continue normally |
| **30-40%** | Approaching limit | Start delegating exploration to subagents |
| **40-50%** | Warning zone | Delegate ALL remaining discovery work |
| **50-60%** | Critical zone | Create handoff checkpoint, delegate implementation |
| **>60%** | Danger zone | Stop, create handoff, instruct /compact |

### Pre-emptive Delegation Pattern

At 30% context, start offloading to subagents:

```
Context at 35%. Complex exploration ahead.

Action: Delegate to Explore agent
Prompt: "Find all files matching X, return summary only"
Result: Agent explores in isolated context
Main context: receives 300-token summary, not 5000-token search results
```

### Pre-emptive Checkpoint Pattern

At 40% context, create checkpoint before continuing:

```
Context at 42%.

Action:
1. bd sync (save beads state)
2. Update TODO.md with current position
3. Continue with caution flag

If next operation would push >50%:
  → Create handoff immediately
  → Delegate remaining work to background agent
  → Report: "Checkpointed at [position]. Background agent continuing."
```

### Background Handoff Pattern

At 50% context, continue work via delegation instead of stopping:

```
Context at 52%. Would normally stop here.

Instead:
1. Create handoff document
2. Spawn background agent with remaining tasks:

   Task:
     subagent_type: general-purpose
     description: "Continue implementation"
     prompt: |
       Continuing from handoff: [path]
       Remaining tasks from beads:
       - [task 1]
       - [task 2]
       - [task 3]

       Implement each, commit, close in beads.
     run_in_background: true

3. Report to user:
   "Context high. Handed off to background agent.
    Agent ID: [id]
    Use 'bd poll-all' to check progress.
    Or start new session and 'resume handoff'."

4. User can:
   - Wait for background agent to finish
   - Start new session with /compact
   - Poll agent results via TaskOutput
```

### Context Prediction Indicators

Watch for these signals to predict exhaustion:

| Signal | Meaning |
|--------|---------|
| Large file reads queued | Will consume significant context |
| Many grep matches expected | High token consumption ahead |
| User requesting "find all" | Exploration will be heavy |
| Complex implementation ahead | Multiple file reads/writes |
| Already at 25% with more to go | Pre-emptively delegate now |

### Proactive vs Reactive

| Reactive (OLD) | Proactive (NEW) |
|----------------|-----------------|
| Wait until 50% to warn | Start delegating at 30% |
| Stop work at high context | Continue via background agents |
| User must /compact manually | Background agent keeps working |
| Context lost on compact | Handoff preserves everything |
| Resume requires reading files again | Background agent has full context |

---

## "I'm Lost" Recovery

**Trigger**: Request doesn't match any category, project state unclear, contradictory context

```yaml
recovery_lost:
  symptoms:
    - "User request doesn't fit normal patterns"
    - "Project state is inconsistent"
    - "Previous context missing or contradictory"
    - "Agent unsure what to do next"

  recovery_protocol:
    step_1: "STOP. Don't guess or hallucinate."

    step_2_ask_user:
      action: |
        I want to make sure I help you correctly. Can you tell me:
        1. What's the end goal you're trying to achieve?
        2. Is this a new project, existing project, or continuation?
        3. What's the most important thing to get right?

    step_3: "Based on answers, re-run triage"

  anti_patterns:
    - "DO NOT pretend to understand when confused"
    - "DO NOT make up context that wasn't provided"
    - "DO NOT assume - ask"
```

---

## Dependency Hell Recovery

**Trigger**: Package conflicts, version mismatches, environment issues

```yaml
recovery_dependency_hell:
  step_1_isolate:
    - "python -m venv .venv-clean"
    - "source .venv-clean/bin/activate"

  step_2_minimal_install:
    - "pip install [core-deps-only]"
    - "Test if basic functionality works"

  step_3_add_incrementally:
    - "Add deps one at a time"
    - "Test after each addition"
    - "Stop when you find the conflict"

  step_4_pin_versions:
    - "pip freeze > requirements.lock"
    - "Document what versions work"
```

---

## Loop Detection (Autonomous Mode)

**Trigger**: Agent running autonomously, possibly stuck in infinite loop

```yaml
recovery_loop_detection:
  detection_methods:
    iteration_count:
      threshold: 100
      action: "Stop after MAX_ITERATIONS"

    stuck_detection:
      check: "Compare beads state hash between iterations"
      threshold: 5  # Same state for 5 iterations
      action: "Stop, write to .agent/LAST_ERROR.md"

    error_threshold:
      consecutive_errors: 3
      action: "Stop and report"

  indicators:
    - "Same bd ready output for multiple iterations"
    - "Repeating same commit messages"
    - "No progress on any beads task"
    - "Iteration count > 50 with few tasks completed"

  recovery:
    step_1: "Write state to .agent/STATUS.md"
    step_2: "bd sync (save beads state)"
    step_3: "Exit gracefully (exit 1)"
    step_4: "User reviews .agent/ and decides next action"

  manual_check:
    commands:
      - "cat .agent/ITERATIONS.md"    # How many iterations?
      - "cat .agent/LAST_ERROR.md"    # What went wrong?
      - "bd list --json"              # What's the task state?
      - "git log --oneline -10"       # What was committed?
```

**Key principle**: Better to stop early and let user review than to burn compute looping.

---

## Recovery Decision Tree

```
Problem detected
    ├─ Build/test failure?     → Build Failure Recovery
    ├─ Agent acting weird?     → Agent Confusion Recovery
    ├─ Responses degrading?    → Context Window Exhaustion
    ├─ Package conflicts?      → Dependency Hell Recovery
    ├─ Infinite loop?          → Loop Detection Recovery
    ├─ Completely lost?        → "I'm Lost" Recovery
    └─ Unknown?                → Generate handoff, start fresh session
```

---

## Anti-Patterns

**During recovery, AVOID:**
- Refactoring while debugging
- Making multiple changes at once
- Guessing at solutions without verification
- Continuing when confused
- Skipping verification steps

**ALWAYS:**
- Make one change at a time
- Verify after each change
- Update TODO.md with current state
- Ask user when genuinely stuck

## Keywords

stuck, looping, confused, lost, broken, failing, recovery, reset, start over, context exhaustion, dependency hell, build failure
