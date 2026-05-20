---
name: todo-management
description: Systematic progress tracking for skill development. Manages task states (pending/in_progress/completed), updates in real-time, reports progress, identifies blockers, and maintains momentum. Use when tracking skill development, coordinating work, or reporting progress.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch
---

# Todo Management

## Overview

todo-management provides systematic task tracking throughout skill development. It manages task states, provides real-time progress updates, identifies blockers, and ensures momentum is maintained from start to finish.

**Purpose**: Track progress systematically, maintain visibility into work status, identify issues early, and ensure completion.

**Value**: Prevents work from being forgotten, provides clear progress visibility, enables course correction, and maintains momentum through completion.

**When to Use**:
- After breaking down work with task-development
- Throughout skill implementation (continuous tracking)
- When coordinating multiple parallel tasks
- When reporting progress to stakeholders
- When ensuring all work gets completed

## Prerequisites

Before using todo-management:

1. **Task List**: Complete task breakdown from task-development
2. **Clear Objectives**: Understanding of what "done" means for each task
3. **Regular Updates**: Commitment to updating task status as you work

## Task-Based Operations

### Operation 1: Initialize Todo List

**When to Use**: At start of skill development, after task breakdown complete

**Process**:

1. **Import Task List** from task-development
2. **Set Initial State**: All tasks to "pending"
3. **Add Metadata**: Skill name, start date, estimates
4. **Verify Completeness**: All tasks included

**Output**: Initial todo list ready for tracking

**Example**:
```markdown
# Todo List: my-skill
Started: 2025-11-06
Estimate: 12-15 hours

⬜ 1. Create directory (15 min)
⬜ 2. SKILL.md frontmatter (30 min)
⬜ 3. Write Overview (1h)
...
```

---

### Operation 2: Start Task

**When to Use**: When beginning work on specific task

**Process**:

1. **Check Dependencies**: Prerequisites complete?
2. **Update State**: pending → in_progress
3. **Add Timestamp**: Note start time
4. **Focus**: Only ONE task in_progress at a time

**Output**: Task marked as in_progress

**Example**:
```markdown
Before: ⬜ 3. Write Overview (1h)
After:  🔄 3. Write Overview (1h) - Started 10:00 AM
```

**Critical Rule**: Maximum 1 task in_progress (prevents context switching)

---

### Operation 3: Complete Task

**When to Use**: Immediately after finishing task

**Process**:

1. **Verify Completion**: Output exists, quality checked
2. **Update State**: in_progress → completed
3. **Record Actual Time**: Compare to estimate
4. **Check Next**: What's ready now?

**Output**: Task marked as completed

**Example**:
```markdown
Before: 🔄 3. Write Overview (1h) - Started 10:00 AM
After:  ✅ 3. Write Overview (1h) - Done 10:45 AM (45min actual)
```

**Best Practice**: Complete IMMEDIATELY, don't batch updates

---

### Operation 4: Report Progress

**When to Use**: Daily, at milestones, or when requested

**Process**:

1. **Calculate Metrics**: Completed, in-progress, remaining
2. **Format Report**: Status, current work, blockers
3. **Present**: Share with team or document

**Output**: Progress report with metrics

**Example**:
```markdown
Progress Report: my-skill (2025-11-06 14:00)

Overall: 8/20 tasks (40%), 6h spent, ~9h remaining

Completed Today:
- ✅ Directory structure
- ✅ SKILL.md frontmatter
- ✅ Overview
- ✅ Prerequisites

Currently: 🔄 Step 1 (1.5h est, 30min elapsed)

Next Up:
- Step 2
- Step 3

Blockers: None
Status: On track (ahead 30min)
```

---

### Operation 5: Identify Blockers

**When to Use**: When task cannot proceed or takes >>20% longer

**Process**:

1. **Recognize Blocker**: Cannot start/complete task
2. **Document**: What's blocked, what's the blocker, who can unblock
3. **Take Action**: Request help, switch tasks, escalate

**Output**: Blocker documented and addressed

**Example**:
```markdown
BLOCKER: Task 7 - API integration guide
Issue: API documentation not available
Impact: 1 task blocked, 2 downstream affected (~5h work)
Action: Requested from API team, ETA Friday
Workaround: Working on independent tasks meanwhile
```

**Blocker Types**:
- Hard: Cannot proceed at all
- Soft: Can proceed but inefficiently
- Waiting: External dependency

---

### Operation 6: Update Estimates

**When to Use**: When actual time differs significantly from estimated (>20%)

**Process**:

1. **Compare Actual vs Estimated**: Calculate variance
2. **Identify Pattern**: All tasks or specific type?
3. **Adjust Remaining**: Apply calibration factor
4. **Communicate**: Update completion timeline

**Output**: Revised estimates reflecting reality

**Example**:
```markdown
Original: 12-15h total
Actual (5 tasks): 7h vs 5.5h est (27% over)
Analysis: Writing tasks taking longer
Adjustment: 1.3x multiplier for remaining writing
Updated: 15-18h total (vs 12-15h)
New completion: Friday vs Thursday
```

---

### Operation 7: Handle Task Changes

**When to Use**: Scope changes, new tasks discovered, tasks obsolete

**Process**:

1. **Document Change**: What, why, impact
2. **Update List**: Add/remove/modify tasks
3. **Recalculate**: New estimate, critical path

**Output**: Updated todo list

**Example - Add Task**:
```markdown
Added: 8a. Create advanced-patterns.md (3h)
Reason: Users need advanced examples
Impact: +3h (now 15-18h total)
```

**Example - Remove Task**:
```markdown
Removed: 12. Create script (4h) - OBSOLETE
Reason: Manual process sufficient
Impact: -4h (now 8-11h total)
```

---

### Operation 8: Maintain Momentum

**When to Use**: Continuously, especially when feeling stuck

**Process**:

1. **Check Progress**: Regular daily review
2. **Identify Killers**: Long tasks, blockers, switching, perfectionism
3. **Apply Strategies**: Quick wins, timeboxing, skip and return
4. **Celebrate**: Mark completions, acknowledge milestones

**Momentum Checklist**:
- [ ] ≥1 task completed per session?
- [ ] Making progress daily?
- [ ] No tasks stuck >2 days?
- [ ] Blockers addressed <1 day?
- [ ] Focus maintained (1 in-progress)?

**When Stuck**:
1. Review completed tasks (see progress!)
2. Pick smallest pending task (quick win)
3. Take 15-min break
4. Ask for help
5. Switch to different task

**When Overwhelmed**:
1. Focus on current task only
2. Break task down further
3. Set smaller milestone (next hour)
4. Remind yourself of MVP

---

## Task State Model

### The Three Core States

**pending** (⬜)
- Not yet started
- Ready to work on (or waiting for dependencies)
- Initial state for all tasks

**in_progress** (🔄)
- Currently being worked on
- **CRITICAL**: Only ONE at a time
- Active work happening now

**completed** (✅)
- Finished and verified
- Output exists, quality checked
- Terminal state (no further changes)

### State Transitions

```
pending → in_progress (start work)
in_progress → completed (finish and verify)
in_progress → pending (blocker discovered)
```

### Special States (Optional)

**blocked** (🚫): Cannot proceed due to obstacle
**obsolete** (⊗): Task no longer needed
**deferred** (⏸): Postponed to later version

---

## Progress Tracking Formats

### Format 1: Simple Checklist

```markdown
# My Skill Todos

- [ ] Task 1 (30 min)
- [x] Task 2 (1h)
- [ ] Task 3 (2h)

Progress: 1/3 (33%)
```

**Pros**: Simple, portable
**Cons**: No in-progress state

---

### Format 2: Enhanced with Emoji

```markdown
# My Skill Todos

⬜ 1. Create directory (15 min)
✅ 2. SKILL.md frontmatter (30 min) - Done 10:30
🔄 3. Write Overview (1h) - Started 10:45
⬜ 4. Write Step 1 (1.5h)

Progress: 1/4 complete (25%), 1 in progress
```

**Pros**: Clear states, visual
**Cons**: Need emoji support

---

### Format 3: Table Format

```markdown
| # | Task | Est | Status | Actual | Notes |
|---|------|-----|--------|--------|-------|
| 1 | Create dir | 15m | ✅ | 15m | Done |
| 2 | Frontmatter | 30m | ✅ | 25m | Done |
| 3 | Overview | 1h | 🔄 | - | Working |
| 4 | Step 1 | 1.5h | ⬜ | - | Ready |

Progress: 2/4 (50%), Time: 40min / 3.25h
```

**Pros**: Structured, tracks actuals
**Cons**: Verbose

---

### Format 4: Grouped by Phase

```markdown
# My Skill Todos

## Phase 1: Initialization ✅
- ✅ 1. Create directory (15 min)
- ✅ 2. SKILL.md frontmatter (30 min)

## Phase 2: Core Content 🔄
- ✅ 3. Write Overview (1h)
- 🔄 4. Write Step 1 (1.5h) - Working
- ⬜ 5. Write Step 2 (1h)
- ⬜ 6. Write Step 3 (1h)

## Phase 3: References ⬜
- ⬜ 7. Create ref-1.md (3h)
- ⬜ 8. Create ref-2.md (2h)

Progress: 3/8 (37.5%), Phase 1 complete
```

**Pros**: Logical grouping, milestones
**Cons**: More structure

---

## Best Practices

### Todo Management Best Practices

1. **Update Immediately**
   - Mark complete right after finishing
   - Don't batch updates
   - Update as you work, not end of day

2. **One Task In-Progress**
   - Focus on single task
   - Prevents context switching
   - Finish before starting next

3. **Complete Before Moving**
   - Finish current task first
   - "Done" = verified, not "mostly done"
   - Avoid 90% complete tasks

4. **Track Actuals**
   - Record actual time
   - Compare to estimates
   - Learn for better estimation

5. **Address Blockers Fast**
   - Don't let blockers sit >1 day
   - Document clearly
   - Take action immediately

6. **Celebrate Progress**
   - Acknowledge completed tasks
   - Mark milestones visibly
   - Maintain momentum with wins

### Common Mistakes

**Mistake 1: Batching Updates**
- Problem: Update once per day
- Fix: Update immediately as you work

**Mistake 2: Multiple In-Progress**
- Problem: 3-4 tasks marked in-progress
- Fix: ONE task in-progress maximum

**Mistake 3: Not Completing**
- Problem: Move to next when "mostly done"
- Fix: Complete current before next

**Mistake 4: Ignoring Blockers**
- Problem: Blocked tasks sit for days
- Fix: Address within 1 day

**Mistake 5: No Actual Tracking**
- Problem: Can't improve estimates
- Fix: Track actuals, compare to estimates

---

## Integration with Other Skills

### With task-development

**Flow**: task-development → todo-management

task-development creates task list → todo-management tracks progress

---

### With planning-architect

**Flow**: planning-architect → task-development → todo-management

Plan estimate → Tasks with estimates → Track to completion

---

### With momentum-keeper

**Flow**: todo-management ← monitors ← momentum-keeper

momentum-keeper checks for stuck tasks, declining velocity

---

## Quick Start

### 5-Minute Setup

**Step 1**: Get task list (from task-development)

**Step 2**: Create initial todos
```markdown
# Todo: my-skill
⬜ 1. Task one (30 min)
⬜ 2. Task two (1h)
⬜ 3. Task three (2h)
```

**Step 3**: Start first task
```markdown
🔄 1. Task one (30 min) - Started
⬜ 2. Task two (1h)
⬜ 3. Task three (2h)
```

**Step 4**: Complete and continue
```markdown
✅ 1. Task one (30 min) - Done!
🔄 2. Task two (1h) - Started
⬜ 3. Task three (2h)
```

---

## Examples

### Example 1: Simple Skill (5 tasks)

```markdown
# Todo: calculator-skill

Started: 2025-11-06 09:00
Estimate: 3 hours

✅ 1. Create directory (15 min) - Done 09:15
✅ 2. SKILL.md frontmatter (20 min) - Done 09:35
🔄 3. Write operations (1.5h) - Started 09:35
⬜ 4. Write examples (45 min)
⬜ 5. Validate (15 min)

Progress: 2/5 (40%), 35min / 3h, On track
```

---

### Example 2: With Blocker

```markdown
# Todo: medical-integration

✅ 1-6: Completed (6h)
🚫 7. FHIR integration guide (3h) - BLOCKED
⬜ 8-15: Pending

Blocker: FHIR API docs not available
Impact: 3 tasks affected (~5h work)
Action: Requested docs, ETA Friday
Workaround: Working on tasks 8-11 (independent)
```

---

## References

Detailed guides for specific aspects:

- **[State Management Guide](references/state-management-guide.md)** - Comprehensive guide to task states, transitions, special states, validation rules

- **[Progress Reporting Guide](references/progress-reporting-guide.md)** - Reporting formats, metrics calculation, visualization techniques, communication strategies

---

## Automation

Use the todo management script:

```bash
# Initialize from task list
python scripts/update-todos.py --init task-list.md

# Start task
python scripts/update-todos.py --start 5

# Complete task
python scripts/update-todos.py --complete 5

# Progress report
python scripts/update-todos.py --report

# Mark blocker
python scripts/update-todos.py --blocker 7 "Waiting for docs"
```

---

## Success Criteria

Effective todo management:

✅ **Regular Updates** - Tasks updated immediately
✅ **Clear Visibility** - Progress at a glance
✅ **Momentum Maintained** - ≥1 task completed per session
✅ **Realistic Tracking** - Estimates updated based on actuals
✅ **Completion Achieved** - All tasks eventually completed

---

## Quick Reference

### The 8 Todo Operations

| Operation | Purpose | When to Use | Time |
|-----------|---------|-------------|------|
| **Initialize** | Create todo list from tasks | Start of project | 10-20m |
| **Start Task** | Mark task in progress | Beginning work on task | 1-2m |
| **Complete Task** | Mark task done | Finishing task | 1-2m |
| **Report Progress** | Generate progress report | Status updates, check-ins | 5-10m |
| **Identify Blockers** | Mark blocked tasks | When task stuck | 2-5m |
| **Update Estimates** | Adjust time estimates | Learning from actuals | 10-15m |
| **Handle Changes** | Add/remove/modify tasks | Requirements change | 5-15m |
| **Maintain Momentum** | Ensure continuous progress | Keeping work moving | Ongoing |

**All operations are independent** - use as needed throughout development

### Task States

| State | Symbol | Meaning | Transition To |
|-------|--------|---------|---------------|
| **pending** | ⬜ | Not yet started | in_progress |
| **in_progress** | 🔄 | Currently working on | completed |
| **completed** | ✅ | Finished successfully | - |
| **blocked** | 🚫 | Stuck, waiting | in_progress (when unblocked) |
| **deferred** | ⏸ | Postponed | pending or in_progress |
| **obsolete** | ⊗ | No longer needed | - |

**Critical Rule**: Only **ONE** task in_progress at a time (prevents context switching)

### Common Commands (Script)

```bash
# Initialize from task list
python scripts/update-todos.py --init task-list.md

# Start task #5
python scripts/update-todos.py --start 5

# Complete task #5
python scripts/update-todos.py --complete 5

# Mark task #7 as blocked
python scripts/update-todos.py --blocker 7 "Waiting for API docs"

# Generate progress report
python scripts/update-todos.py --report

# Update estimate for task #3
python scripts/update-todos.py --update-estimate 3 "2h"

# Add new task
python scripts/update-todos.py --add "Validate new feature" "1h" "Phase 4"
```

### Progress Metrics

**Completion Rate**: `Completed / Total × 100%`

**Velocity**: `Completed tasks / Time elapsed`

**Estimated Remaining**: `Sum of remaining task estimates`

**Burn Rate**: `Time spent / Total estimated time × 100%`

**On Track?**: Burn rate ≈ Completion rate (±10%)

### Best Practices Quick List

1. ✅ **Update immediately** (not in batches)
2. ✅ **One in_progress** (no context switching)
3. ✅ **Mark blockers** (visibility of issues)
4. ✅ **Complete before new** (finish current task first)
5. ✅ **Update estimates** (learn and improve)
6. ✅ **Report regularly** (track progress)
7. ✅ **Handle changes** (adapt to new requirements)
8. ✅ **Maintain momentum** (≥1 completed per session)

### State Transition Diagram

```
pending ──start──> in_progress ──complete──> completed
   ↑                    ↓
   └────────────────blocked
                        ↓
                    deferred
```

### Troubleshooting Quick Fixes

| Problem | Quick Fix |
|---------|-----------|
| Multiple in_progress | Complete or defer all but one |
| Stalled progress | Identify blockers, seek help |
| Estimates way off | Update remaining estimates |
| Too many tasks | Defer low-priority tasks |
| Losing momentum | Complete quick wins |

### For More Information

- **State management**: references/state-management-guide.md
- **Progress reporting**: references/progress-reporting-guide.md
- **Automation**: scripts/update-todos.py --help

---

**todo-management** is essential for maintaining progress from task list to completed skill. Use it consistently throughout development for successful outcomes.