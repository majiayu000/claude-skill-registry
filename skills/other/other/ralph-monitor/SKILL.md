---
name: ralph-monitor
version: 1.0.0
description: Monitor and report on Ralph Wiggum loop progress. Provides real-time status, iteration summaries, and progress tracking via Archon state. Use to check on running or completed loops, view iteration history, and diagnose issues.
---

# Ralph Monitor Skill

Monitor and report on Ralph Wiggum loop status and progress. Provides visibility into active and completed loops via Archon state.

## Triggers

Use this skill when:
- Checking Ralph loop status
- Viewing iteration progress
- Monitoring running loops
- Reviewing loop history
- Diagnosing stuck loops
- Keywords: ralph status, loop status, ralph monitor, check loop, iteration progress, loop history

## Core Mission

Query Archon and local state to provide comprehensive status reports on Ralph loops.

---

## Status Report Formats

### Active Loop Status

```markdown
## Ralph Loop Status

### Loop Information
| Property | Value |
|----------|-------|
| Loop ID | [LOOP_ID] |
| Status | Running / Paused / Stopped |
| Started | [TIMESTAMP] |
| Duration | [HH:MM:SS] |

### Progress
| Metric | Current | Target |
|--------|---------|--------|
| Iteration | [N] | [MAX] |
| Tasks | [DONE] | [TOTAL] |
| Tests Passing | [PASS] | [TOTAL] |

[====================----------] 67% complete

### Current Iteration
| Property | Value |
|----------|-------|
| Iteration | [N] |
| Started | [TIME] |
| Focus | [Current work summary] |

### Recent Activity
| Iter | Time | Summary | Files | Tests |
|------|------|---------|-------|-------|
| N | 5m ago | [Summary] | 3 | 15/15 |
| N-1 | 12m ago | [Summary] | 5 | 14/15 |
| N-2 | 20m ago | [Summary] | 2 | 10/15 |

### Validation Status
- Build: Passing
- Tests: 15/15 passing
- Lint: 2 warnings

### Archon Integration
- Project: [PROJECT_NAME] ([PROJECT_ID])
- Task: [TASK_TITLE] ([TASK_ID])
- Task Status: doing
- State Doc: [DOC_ID]

### Commands
- View full log: `cat .ralph/loop.log`
- Cancel loop: Use ralph-loop skill with cancel mode
- View prompt: `cat .ralph/prompts/current.md`
```

---

## Data Collection

### From Archon

```python
# Get state document
state_docs = find_documents(
    project_id=PROJECT_ID,
    query="Ralph Loop State"
)

# Get active loops
active_loops = [
    doc for doc in state_docs
    if doc["content"]["status"] == "running"
]

# Get associated tasks
for loop in active_loops:
    task = find_tasks(task_id=loop["content"]["task_id"])
    loop["task"] = task
```

### From Local State

```bash
# Read config
cat .ralph/config.json

# Read recent log
tail -100 .ralph/loop.log

# Git status
git --no-pager log --oneline -5
git status --short
```

---

## Report Types

### Quick Status

Returns brief one-liner:

```
Ralph: Iteration 12/50 | 67% | Tests 15/15 | Duration 25m
```

### Full Status

Returns complete report as shown above.

### History Report

```markdown
## Ralph Loop History

### Completed Loops
| Loop ID | Task | Iterations | Duration | Status |
|---------|------|------------|----------|--------|
| ralph-20260122-150000 | Auth API | 12 | 45m | Complete |
| ralph-20260121-100000 | DB Schema | 8 | 30m | Complete |
| ralph-20260120-140000 | User Model | 25 | 1h 20m | Max reached |

### Statistics
| Metric | Value |
|--------|-------|
| Total Loops | 15 |
| Completed | 12 (80%) |
| Blocked | 2 (13%) |
| Max Reached | 1 (7%) |
| Avg Iterations | 14 |
| Avg Duration | 35m |
```

### Comparison Report

```markdown
## Loop Comparison

| Metric | loop1 | loop2 |
|--------|-------|-------|
| Task | Auth API | User API |
| Iterations | 12 | 18 |
| Duration | 45m | 1h 10m |
| Files Changed | 24 | 31 |
| Tests Added | 15 | 22 |
| Status | Complete | Complete |
```

---

## Progress Visualization

### Iteration Timeline

```
Iteration Progress
==================

1  #### Setup
2  ######## Basic impl
3  ############ Tests added
4  ###### Bug fix
5  ################ Feature complete
6  #### Refactor
7  ########## Edge cases
8  #################### Validation
9  ###### Polish
10 ######################## Complete

Legend: #### = Work done, length = files changed
```

### Test Progress

```
Test Progress Across Iterations
===============================

Iter  1: [          ] 0/0
Iter  2: [###       ] 5/15
Iter  3: [#####     ] 8/15
Iter  4: [######    ] 10/15
Iter  5: [########  ] 12/15
Iter  6: [########  ] 12/15  <- regression
Iter  7: [##########] 15/15 PASS
```

---

## Alerts and Warnings

### Stuck Detection

```markdown
## Potential Issue Detected

### Stuck Pattern
The loop appears to be stuck:
- Last 3 iterations made no test progress
- Same files being modified repeatedly
- Similar error messages in output

### Recommendation
Consider:
1. Reviewing the prompt for clarity
2. Breaking the task into smaller pieces
3. Adding more specific validation criteria
4. Canceling and debugging manually

### Action
- Continue monitoring
- Cancel loop if needed
- Review logs: `cat .ralph/loop.log | tail -500`
```

### Resource Warning

```markdown
## Resource Warning

### Issue
- Token usage high in recent iterations
- Approaching context limit

### Recommendation
- Consider checkpointing
- May need to restart with fresh context
- Current work is saved in Archon
```

---

## Troubleshooting Commands

### Check Configuration

```markdown
## Configuration Check

### Files
- [x] .ralph/config.json exists
- [x] .ralph/prompts/current.md exists
- [x] .ralph/loop-state.json exists

### Archon Connection
- [x] Project found: [PROJECT_NAME]
- [x] Task found: [TASK_TITLE]
- [x] State document found

### Validation Commands
- [x] Build: `npm run build` (verified)
- [x] Test: `npm test` (verified)
- [ ] Lint: `npm run lint` (not configured)

### All checks passed
```

---

## Usage Examples

### Check Current Status

```python
# Quick check
"What's the Ralph loop status?"

# Full details
"Show me detailed Ralph loop status"
```

### View History

```python
# All loops
"Show Ralph loop history"

# Specific loop
"Show details for ralph-20260122-150000"
```

### Diagnose Issues

```python
# Check for problems
"Is the Ralph loop stuck?"

# View recent iterations
"Show last 5 Ralph iterations"
```

---

## Integration with Other Skills

### With ralph-loop Skill

```python
# If monitoring shows issues, suggest:
"Use ralph-loop skill to cancel or resume"
```

### With archon-workflow Skill

```python
# For task management integration:
"Use archon-workflow to update task status"
```

---

## Best Practices

1. **Regular Monitoring**: Check status periodically for long loops
2. **Watch for Patterns**: Same files modified repeatedly = potential issue
3. **Test Progress**: Should generally increase each iteration
4. **Duration Tracking**: Unusually long iterations may indicate problems
5. **Archon Sync**: Ensure state is properly saved to Archon
6. **Log Review**: Check loop.log for detailed error messages
