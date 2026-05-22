---
name: agile-workflow
description: "Orchestrate agile development workflows by invoking commands in sequence with checkpoint-based flow control. This skill should be used when the user asks to 'run the workflow', 'continue working', 'what's next', 'complete the task cycle', 'start my day', 'end the sprint', 'implement the next task', or wants guided step-by-step development assistance. Keywords: workflow, orchestrate, agile, task cycle, sprint, daily, implement, review, PR, standup, retrospective."
license: MIT
compatibility: Requires git, GitHub CLI (gh), and a context network with backlog structure.
metadata:
  author: agent-skills
  version: "1.0"
---

# Agile Workflow Orchestrator

A skill that guides agents through structured agile development workflows by intelligently invoking commands in sequence. Uses checkpoint-based flow control to auto-progress between steps while pausing at key decision points.

## When to Use This Skill

Use this skill when:
- Starting work for the day ("run morning standup", "start my day")
- Working on a task ("implement next task", "continue working")
- Completing a development cycle ("finish this task", "prepare PR")
- Running sprint ceremonies ("start sprint", "end sprint", "retrospective")
- Resuming interrupted work ("what's next", "where was I")

Do NOT use this skill when:
- Running a single specific command (use that command directly)
- Just checking status (use `/status` directly)
- Only doing code review without full cycle (use `/review-code` directly)
- Researching or planning without implementation

## Prerequisites

Before using this skill:
- **Git repository** initialized with worktree support
- **GitHub CLI** installed and authenticated (`gh auth status`)
- **Context network** with backlog structure at `context-network/backlog/`
- Task status files at `context-network/backlog/by-status/*.md`

## Workflow Types Overview

```
WORKFLOW TYPES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TASK CYCLE (Primary)     DAILY                SPRINT
──────────────────────   ──────────────────   ──────────────────
sync                     Morning:             Start:
  ↓                        sync --last 1d       sync --all
next → [CHECKPOINT]        status --brief       groom --all
  ↓                        groom --ready        plan sprint-goals
implement                                       status
  ↓                      Evening:
[CHECKPOINT]               checklist          End:
  ↓                        discovery            sync --sprint
review-code                sync --last 1d       retrospective
review-tests                                    audit --sprint
  ↓                                             maintenance --deep
[CHECKPOINT]
  ↓
apply-recommendations (if issues)
  ↓
pr-prep → [CHECKPOINT]
  ↓
pr-complete
  ↓
END
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## State Detection

The skill determines current workflow state automatically. No manual tracking needed.

### Detection Signals

| Signal | How to Check | Indicates |
|--------|--------------|-----------|
| Worktree exists | `git worktree list` | Task in progress |
| Task branch active | `git branch --show-current` matches `task/*` | Active implementation |
| Uncommitted changes | `git status --porcelain` | Active coding |
| PR exists | `gh pr list --head [branch]` | In review |
| PR merged | `gh pr view --json state` | Ready for cleanup |

### State Matrix

```
STATE DETECTION LOGIC
─────────────────────────────────────────────────────────────
Check                           → State           → Next Step
─────────────────────────────────────────────────────────────
No worktree, no in-progress     → IDLE            → sync, next
Worktree exists, uncommitted    → IMPLEMENTING    → continue implement
Worktree exists, all committed  → READY_REVIEW    → review-code
PR open, checks pending         → AWAITING_CI     → wait or address
PR open, checks pass            → READY_MERGE     → pr-complete
PR merged, worktree exists      → CLEANUP         → pr-complete
─────────────────────────────────────────────────────────────
```

For detailed detection algorithms, see [references/state-detection.md](references/state-detection.md).

## Invocation Patterns

```bash
# Auto-detect state and continue from where you are
/agile-workflow

# Start specific workflow phase
/agile-workflow --phase task-cycle
/agile-workflow --phase daily-morning
/agile-workflow --phase daily-evening
/agile-workflow --phase sprint-start
/agile-workflow --phase sprint-end

# Resume work on specific task
/agile-workflow --task TASK-123

# Preview what would happen without executing
/agile-workflow --dry-run
```

## Task Cycle Phase

The primary workflow for completing a single task from selection to merge.

### Step 1: Sync Reality

Ensure context network matches actual project state.

```
Run: sync --last 1d --dry-run
Purpose: Detect drift between documented and actual state
Output: Sync report showing completions, partial work, divergences
```

### Step 2: Select Task

Identify the next task to work on.

```
Run: next
Purpose: Find highest priority ready task
Output: Task ID, title, branch name suggestion
```

**CHECKPOINT: TASK_SELECTED**
- Pause to confirm task selection
- User can accept or choose different task
- On accept: continue to implementation

### Step 3: Implement

Test-driven development in isolated worktree.

```
Run: implement [TASK-ID]
Purpose: Create worktree, write tests first, implement, verify
Output: Working implementation with passing tests
```

**CHECKPOINT: IMPL_COMPLETE**
- Pause after implementation completes
- Show test results and coverage
- On success: continue to review

### Step 4: Review

Quality validation of implementation.

```
Run: review-code --uncommitted
Run: review-tests --uncommitted
Purpose: Identify quality issues, security concerns, test gaps
Output: Review reports with issues and recommendations
```

**CHECKPOINT: REVIEWS_DONE**
- Display combined review results
- If critical issues: must address before continuing
- If no issues: auto-continue to PR prep
- User decides: apply recommendations now or defer

### Step 5: Apply Recommendations (Conditional)

Address review findings intelligently.

```
Run: apply-recommendations [review-output]
Purpose: Apply quick fixes now, defer complex changes to tasks
Output: Applied fixes + created follow-up tasks
```

### Step 6: Prepare PR

Create pull request with full documentation.

```
Run: pr-prep
Purpose: Validate, document, and create PR
Output: PR created with description, tests verified
```

**CHECKPOINT: PR_CREATED**
- Display PR URL and CI status
- Wait for CI checks to complete
- On CI pass + approval: continue to merge
- On CI fail: stop, address issues

### Step 7: Complete PR

Merge and cleanup.

```
Run: pr-complete [PR-NUMBER]
Purpose: Merge PR, delete branch, remove worktree, update status
Output: Task marked complete, cleanup done
```

For detailed task-cycle instructions, see [references/phases/task-cycle.md](references/phases/task-cycle.md).

## Daily Phase

Quick sequences for start and end of workday.

### Morning Standup (~5 min)

```
Run sequence:
1. sync --last 1d --dry-run   # What actually happened yesterday
2. status --brief --sprint    # Current sprint health
3. groom --ready-only         # What's ready to work on

Output: Clear picture of today's priorities
```

### Evening Wrap-up (~10 min)

```
Run sequence:
1. checklist                  # Ensure nothing lost
2. discovery                  # Capture learnings
3. sync --last 1d            # Update task statuses

Output: Knowledge preserved, state synchronized
```

For detailed daily instructions, see [references/phases/daily.md](references/phases/daily.md).

## Sprint Phase

Ceremonies for sprint boundaries.

### Sprint Start (~60 min)

```
Run sequence:
1. sync --all                 # Full reality alignment
2. groom --all               # Comprehensive grooming
3. plan sprint-goals         # Architecture and goals
4. status --detailed         # Baseline metrics

Output: Sprint plan with groomed, ready backlog
```

### Sprint End (~90 min)

```
Run sequence:
1. sync --sprint             # Final sprint sync
2. retrospective             # Capture learnings
3. audit --scope sprint      # Quality review
4. status --metrics          # Sprint metrics
5. maintenance --deep        # Context network cleanup

Output: Sprint closed, learnings captured, ready for next
```

For detailed sprint instructions, see [references/phases/sprint.md](references/phases/sprint.md).

## Checkpoint Handling

Checkpoints are pauses for human decision-making.

### Checkpoint Behavior

At each checkpoint:
1. **Summarize** what just completed
2. **Show** key results and any issues
3. **Present** next steps
4. **Wait** for user input

### Checkpoint Responses

| Response | Action |
|----------|--------|
| "continue" / "proceed" / "yes" | Move to next step |
| "stop" / "pause" | Save state, exit workflow |
| "back" | Re-run previous step |
| "skip" | Skip current step (use cautiously) |
| Custom input | May adjust next step parameters |

### Auto-Continue Conditions

Some checkpoints can auto-continue when conditions are met:

| Checkpoint | Auto-Continue If |
|------------|------------------|
| IMPL_COMPLETE | All tests pass, build succeeds |
| REVIEWS_DONE | No critical or high severity issues |
| PR_CREATED | CI passes, required approvals obtained |

For detailed checkpoint handling, see [references/checkpoint-handling.md](references/checkpoint-handling.md).

## Command Reference

Each workflow step uses embedded command instructions:

| Command | Reference | Purpose |
|---------|-----------|---------|
| sync | [references/commands/sync.md](references/commands/sync.md) | Reality synchronization |
| groom | [references/commands/groom.md](references/commands/groom.md) | Task refinement |
| next | [references/commands/next.md](references/commands/next.md) | Task selection |
| implement | [references/commands/implement.md](references/commands/implement.md) | TDD implementation |
| review-code | [references/commands/review-code.md](references/commands/review-code.md) | Code quality review |
| review-tests | [references/commands/review-tests.md](references/commands/review-tests.md) | Test quality review |
| apply-recommendations | [references/commands/apply-recommendations.md](references/commands/apply-recommendations.md) | Triage and apply fixes |
| pr-prep | [references/commands/pr-prep.md](references/commands/pr-prep.md) | PR creation |
| pr-complete | [references/commands/pr-complete.md](references/commands/pr-complete.md) | PR merge and cleanup |
| discovery | [references/commands/discovery.md](references/commands/discovery.md) | Learning capture |
| retrospective | [references/commands/retrospective.md](references/commands/retrospective.md) | Post-work analysis |
| maintenance | [references/commands/maintenance.md](references/commands/maintenance.md) | Context network cleanup |

## Example: Complete Task Cycle

**Scenario:** Start of day, implement next available task

**Invocation:**
```
/agile-workflow --phase task-cycle
```

**Flow:**
```
Agent: Detecting current state...
       No worktree found, checking ready tasks...

Agent: Running sync --last 1d --dry-run
       [Sync output: 0 tasks completed but undocumented]

Agent: Running next
       Found: TASK-042 - Add user preferences endpoint
       Priority: High | Size: Small | Branch: task/TASK-042-preferences

       ╔═══════════════════════════════════════════╗
       ║  CHECKPOINT: Task Selection               ║
       ╠═══════════════════════════════════════════╣
       ║  Selected: TASK-042                       ║
       ║  Proceed with implementation?             ║
       ║                                           ║
       ║  [continue] [stop] [other task]           ║
       ╚═══════════════════════════════════════════╝

User: continue

Agent: Creating worktree at .worktrees/TASK-042/
       Running implement TASK-042
       [Implementation proceeds with TDD...]

       Tests: 12 passing
       Coverage: 87%
       Build: Success

       ╔═══════════════════════════════════════════╗
       ║  CHECKPOINT: Implementation Complete      ║
       ╠═══════════════════════════════════════════╣
       ║  All tests passing, ready for review      ║
       ║  Proceed to code review?                  ║
       ║                                           ║
       ║  [continue] [stop]                        ║
       ╚═══════════════════════════════════════════╝

[Flow continues through review, PR, merge...]
```

## Limitations

- Requires context network with specific backlog structure
- GitHub-centric (uses `gh` CLI for PR operations)
- Single-task focus (parallel task work not orchestrated)
- Manual intervention needed when CI fails or conflicts occur

## Related Skills

- **skill-maker** - Create new skills following agentskills.io spec
- **research-workflow** - For research tasks before implementation
