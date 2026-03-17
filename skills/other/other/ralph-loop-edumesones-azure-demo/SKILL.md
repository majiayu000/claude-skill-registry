---
name: ralph-loop
description: Autonomous feature development loop. Executes complete 9-phase cycle (Interview -> Think Critically -> Plan -> Branch -> Implement -> Verify -> PR -> Merge -> Wrap-Up) with minimal human intervention. Triggers on "/ralph", "start autonomous loop", "run ralph loop".
globs: ["docs/features/**", "ralph-*.sh", "feature-loop-state.json", "activity.md"]
---

# Ralph Loop - Autonomous Feature Development

Executes the complete Feature Development Cycle (9 phases) autonomously, only pausing for:
- Human input during Interview (if spec.md is incomplete)
- Think Critically: red flags or low confidence level
- Merge approval (PR review)
- 3 consecutive failures

## Triggers

- `/ralph orchestrator [max_parallel]` - Start multi-feature orchestration
- `/ralph feature FEAT-XXX [max_iterations]` - Single feature loop
- `/ralph status` - Check running loops
- `/ralph stop` - Stop all loops
- "Start autonomous loop"
- "Run ralph on FEAT-XXX"

## Architecture

```
RALPH LOOP ARCHITECTURE

ORCHESTRATOR (ralph-orchestrator.sh)
- Reads docs/features/_index.md for Pending features
- Creates git worktrees for isolation
- Launches feature loops in parallel (max N)
- Monitors for merge completion
- Cleans up worktrees after merge

        |
        +--> Worktree: ../project-FEAT-001-loop/
        |    --> ralph-feature.sh FEAT-001
        |
        +--> Worktree: ../project-FEAT-002-loop/
        |    --> ralph-feature.sh FEAT-002
        |
        +--> Worktree: ../project-FEAT-003-loop/
             --> ralph-feature.sh FEAT-003
```

## Feature Loop Phases

```
FEATURE LOOP - 9 PHASES

Iteration 1: INTERVIEW
- Read spec.md
- If Technical Decisions has TBD -> PAUSE for human input
- If complete -> emit INTERVIEW_COMPLETE

Iteration 2: THINK CRITICALLY (11-Step Protocol)
- Determine depth: full/medium/light/skip
- Execute analysis protocol -> analysis.md
- If red flags or low confidence -> PAUSE for review
- If safe -> emit ANALYSIS_COMPLETE

Iteration 3: PLAN
- Read spec.md + analysis.md (BOTH required)
- Generate design.md with architecture
- Generate tasks.md with ordered checklist
- emit PLAN_COMPLETE

Iteration 4: BRANCH
- git checkout -b feature/XXX-name
- emit BRANCH_COMPLETE

Iterations 5-N: IMPLEMENT
- Process 3 tasks per iteration
- Mark [in progress] -> implement -> mark [x] -> commit
- emit IMPLEMENT_PROGRESS until all done
- emit IMPLEMENT_COMPLETE when finished

Iteration N+1: VERIFY (if frontend changes)
- Run browser E2E tests
- emit VERIFY_COMPLETE

Iteration N+2: PR
- git push origin feature/XXX
- gh pr create
- emit PR_COMPLETE

Iteration N+3: MERGE
- Poll gh pr view for merge status
- emit MERGE_WAITING until approved
- emit MERGE_COMPLETE when merged

Iteration N+4: WRAP-UP
- Create context/wrap_up.md
- Document metrics and learnings
- emit WRAPUP_COMPLETE
- emit FEATURE_COMPLETE
```

## Pause Conditions

The loop pauses (doesn't terminate) when:

1. **Human Input Needed** (return code 3)
   - spec.md has TBD values that can't be auto-filled
   - User must complete interview manually

2. **Think Critically Requires Review** (return code 3)
   - Step 2: Assumption with Low confidence + High impact
   - Step 9: Critical red flag identified
   - Step 11: Overall confidence = "Low"
   - User must review analysis.md and decide how to proceed

3. **Waiting for External Action** (return code 2)
   - PR created, waiting for review approval
   - Polls every 60 seconds

4. **Too Many Failures** (3 consecutive)
   - Something is broken
   - User must investigate and fix

## Integration with Feature Cycle

Ralph Loop fully integrates with existing Feature Development Cycle (9 phases):

| Existing Command | Ralph Equivalent |
|-----------------|------------------|
| `/interview FEAT-XXX` | Auto-executed if spec needs completion |
| `/think-critically FEAT-XXX` | Auto-executed with depth based on complexity |
| `/plan FEAT-XXX` | Auto-generated from spec + analysis |
| `/git "msg"` | Auto-commit after each task |
| `/git pr` | Auto-created after implementation |
| `/wrap-up FEAT-XXX` | Auto-generated after merge |

## Usage Examples

```bash
# Start orchestrator for all pending features (max 3 parallel)
./ralph-orchestrator.sh 3

# Run single feature loop
./ralph-feature.sh FEAT-001-auth 15

# Check status
./ralph-orchestrator.sh --status

# Stop all loops
./ralph-orchestrator.sh --stop
```

## Prerequisites

- `git` and `gh` (GitHub CLI) installed and authenticated
- `claude` CLI available
- `python3` for JSON manipulation
- Features defined in `docs/features/_index.md`
