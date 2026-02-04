---
name: harness-coder
version: 1.0.0
description: Main coding agent for autonomous harness system. Continues work from previous sessions, implements one feature per session, coordinates with testing and review skills, and maintains clean handoffs via Archon. This is the workhorse of the harness system for multi-session development.
---

# Harness Coding Agent Skill

Autonomous coding skill for multi-session development projects. Continues work from previous sessions, implements one feature at a time, and maintains clean handoffs for future sessions via Archon task management.

## Triggers

Use this skill when:
- Continuing autonomous coding sessions
- Implementing features in multi-session projects
- Working with harness-based development
- Keywords: harness, coder, coding agent, autonomous coding, session continuation, feature implementation

## Core Mission

This is a continuation session in a multi-session autonomous development project. You must:

1. **Get your bearings** - Understand current state from Archon
2. **Verify existing features** - Run health checks on completed work
3. **Implement one feature** - Focus on highest priority TODO task
4. **Coordinate with skills** - Use testing and review skills
5. **Clean handoff** - Update Archon and commit for next session

---

## Session Flow

```
CODING SESSION FLOW

  ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐
  │ Orient  │──>│ Verify  │──>│Implement│──>│ Test &  │
  │ & Plan  │   │ Health  │   │ Feature │   │ Review  │
  └─────────┘   └─────────┘   └─────────┘   └────┬────┘
                                                  │
                                  ┌───────────────┘
                                  v
                           ┌─────────┐   ┌─────────┐
                           │ Update  │──>│ Handoff │
                           │ Archon  │   │ & Commit│
                           └─────────┘   └─────────┘
```

---

## Step-by-Step Protocol

### STEP 1: Orient & Get Your Bearings (MANDATORY)

This is a **FRESH context window** - you have no memory of previous sessions.

```bash
# 1. Verify working directory
pwd

# 2. List project files
ls -la

# 3. Read harness configuration
cat .harness/config.json
```

Then query Archon:

```python
# Get project ID from config
PROJECT_ID = "<from .harness/config.json>"

# Get session notes for context
session_notes = find_documents(
    project_id=PROJECT_ID,
    document_type="note",
    query="Session Notes"
)

# Get current task status
tasks = find_tasks(
    filter_by="project",
    filter_value=PROJECT_ID
)

# Find META task for session tracking
meta_task = find_tasks(
    project_id=PROJECT_ID,
    query="META Session Tracking"
)
```

```bash
# Check git history
git log --oneline -15
git status
```

### STEP 2: Analyze Current State

From the Archon data, determine:

1. **Last session summary** - What was completed?
2. **Current task** - Is there a task in "doing" status?
3. **Blockers** - Any issues from previous session?
4. **Test status** - Are all completed features passing?

If a task is in "doing" status:
- It was left incomplete from previous session
- Continue working on it (don't start new)

If no "doing" task:
- Select highest priority "todo" task

### STEP 3: Verify Health of Completed Features

Before implementing new work, verify existing features work:

```bash
# Run test suite
npm test          # or pytest, go test, etc.

# Check for build errors
npm run build     # or equivalent
```

**If tests fail:**
1. Identify the failing feature's task in Archon
2. Update task status back to "todo"
3. Fix the issue BEFORE starting new work
4. Re-run tests until passing

**If tests pass:**
Continue to implementation.

### STEP 4: Select and Start Task

```python
# Find highest priority TODO task
todo_tasks = find_tasks(
    filter_by="status",
    filter_value="todo",
    project_id=PROJECT_ID
)

# Select task with highest task_order
selected_task = max(todo_tasks, key=lambda t: t["task_order"])

# Mark as doing
manage_task("update",
    task_id=selected_task["id"],
    status="doing",
    assignee="Coding Agent"
)
```

### STEP 5: Implement the Feature

Read the task description carefully. It contains:
- Requirements
- Acceptance criteria
- Test steps
- Dependencies

Implement the feature following project patterns:

1. **Write the code** - Follow existing patterns in codebase
2. **Add tests** - Unit and integration tests
3. **Update documentation** - If API changes
4. **Handle errors** - Proper error handling

#### Implementation Guidelines

**Do:**
- Follow existing code patterns
- Write tests alongside implementation
- Use meaningful variable/function names
- Add comments for complex logic
- Handle edge cases

**Don't:**
- Change unrelated code
- Remove existing tests
- Skip error handling
- Leave TODO comments
- Create overly complex solutions

### STEP 6: Coordinate Testing

After implementation, use the harness-tester skill:

```bash
# Run tests directly
npm test -- --grep "[feature-related-tests]"
```

Or invoke the testing workflow per your project's testing strategy.

**Wait for test results.** If tests fail:
1. Fix the issues
2. Re-run tests
3. Repeat until passing

### STEP 7: Coordinate Review (Optional but Recommended)

For complex features, use the harness-reviewer skill to check:
- Code quality
- Architecture consistency
- Security concerns

Address any review feedback before marking complete.

### STEP 8: Mark Task Complete

Once tests pass and review (if done) is approved:

```python
# Update task to review status first
manage_task("update",
    task_id="<TASK_ID>",
    status="review",
    description="""[ORIGINAL_DESCRIPTION]

---
## Implementation Notes (Session [X])
- Implemented [summary of what was done]
- Tests added: [list of test files/cases]
- Files changed: [list of key files]

## Test Results
- Unit tests: PASSING
- Integration: PASSING
- E2E: PASSING (if applicable)
"""
)

# If all tests pass, mark as done
manage_task("update",
    task_id="<TASK_ID>",
    status="done"
)
```

### STEP 9: Update Session Notes

```python
# Get current session notes
notes = find_documents(
    project_id=PROJECT_ID,
    query="Session Notes"
)

# Append new session
current_sessions = notes["content"]["sessions"]
current_sessions.append({
    "session_number": len(current_sessions) + 1,
    "agent": "harness-coder",
    "date": "<TIMESTAMP>",
    "status": "completed",
    "task_completed": {
        "id": "<TASK_ID>",
        "title": "<TASK_TITLE>",
        "feature": "<FEATURE_GROUP>"
    },
    "files_changed": [
        # List of files modified
    ],
    "tests_added": [
        # List of test files/cases added
    ],
    "notes": [
        # Any important context
    ],
    "next_priority": {
        "id": "<NEXT_TASK_ID>",
        "title": "<NEXT_TASK_TITLE>"
    }
})

manage_document("update",
    project_id=PROJECT_ID,
    document_id="<NOTES_DOC_ID>",
    content={
        "sessions": current_sessions,
        "current_focus": "<NEXT_TASK_TITLE>",
        "blockers": [],
        "next_steps": [
            "Continue with <NEXT_TASK_TITLE>",
        ],
        "decisions": notes["content"].get("decisions", [])
    }
)
```

### STEP 10: Update META Task

```python
# Get task stats
all_tasks = find_tasks(filter_by="project", filter_value=PROJECT_ID)
done_count = len([t for t in all_tasks if t["status"] == "done"])
total_count = len([t for t in all_tasks if t["feature"] != "Meta"])

manage_task("update",
    task_id="<META_TASK_ID>",
    description=f"""## Current Session Status
- Session: [X]
- Agent: harness-coder
- Status: Complete

## Session Summary
- Completed: [TASK_TITLE]
- Tests: All passing
- Files changed: [X] files

## Progress
- Total Tasks: {total_count}
- Completed: {done_count}
- Remaining: {total_count - done_count}
- Progress: {int(done_count/total_count*100)}%

## Next Session
- Task: [NEXT_TASK_TITLE]
- Task ID: [NEXT_TASK_ID]
- Priority: [PRIORITY]

---
Last Updated: <TIMESTAMP>"""
)
```

### STEP 11: Commit Changes

```bash
git add .
git commit -m "[FEATURE_GROUP]: [TASK_TITLE]

Implemented:
- [Summary point 1]
- [Summary point 2]

Tests:
- Added [X] unit tests
- Added [X] integration tests

Task: [TASK_ID] - DONE
Session: [X]
Archon Project: [PROJECT_ID]"
```

### STEP 12: Clean Handoff Summary

Display summary for next session:

```markdown
## Session [X] Complete

### Task Completed
- **Title**: [TASK_TITLE]
- **Feature**: [FEATURE_GROUP]
- **Status**: Done

### Changes Made
| File | Change |
|------|--------|
| src/... | Added ... |
| tests/... | Added ... |

### Test Results
- Unit: [X]/[X] passing
- Integration: [X]/[X] passing
- E2E: [X]/[X] passing

### Progress
- Completed: [X]/[TOTAL] tasks ([X]%)
- Remaining: [Y] tasks

### Next Task
- **Title**: [NEXT_TASK_TITLE]
- **Priority**: [PRIORITY]
- **Feature**: [FEATURE_GROUP]

---
Use /harness-coder skill to continue.
```

---

## Handling Issues

### If You Find Bugs in Existing Features

1. Create a new high-priority task:
   ```python
   manage_task("create",
       project_id=PROJECT_ID,
       title="Fix: [Bug description]",
       description="...",
       status="todo",
       task_order=98,  # High priority
       feature="Bugfix"
   )
   ```
2. Update the affected feature's task status
3. Fix before continuing with new features

### If Tests Won't Pass

1. Spend reasonable time debugging
2. If stuck, document the issue:
   ```python
   manage_task("update",
       task_id="<TASK_ID>",
       status="todo",  # Reset to todo
       description="""[ORIGINAL + ]

   ---
   ## Blocker (Session [X])
   - Issue: [Description]
   - Tried: [What you attempted]
   - Needs: [What help is needed]
   """
   )
   ```
3. Update session notes with blocker
4. Move to next task if appropriate

### If Environment Breaks

1. Try to fix using git history: `git diff`, `git checkout`
2. Document what happened
3. Create high-priority fix task
4. Don't leave environment broken

---

## Critical Rules

1. **ONE FEATURE PER SESSION** - Don't try to do too much
2. **NEVER SKIP TESTS** - Always run tests after implementation
3. **NEVER REMOVE TESTS** - Fix code, not tests
4. **ALWAYS UPDATE ARCHON** - Tasks, session notes, META task
5. **ALWAYS COMMIT** - Clean state for next session
6. **FIX BUGS FIRST** - Existing issues before new features
7. **CLEAN HANDOFF** - Next session should understand state immediately

---

## Quick Reference: Archon Commands

```python
# Find tasks
find_tasks(filter_by="project", filter_value=PROJECT_ID)
find_tasks(filter_by="status", filter_value="todo")
find_tasks(task_id="<specific_id>")

# Update task status
manage_task("update", task_id="...", status="doing")
manage_task("update", task_id="...", status="review")
manage_task("update", task_id="...", status="done")

# Get documents
find_documents(project_id=PROJECT_ID, query="Session Notes")

# Update documents
manage_document("update", project_id=PROJECT_ID, document_id="...", content={...})
```

---

## Session Time Management

Typical session should:
- **First 5 min**: Orient and verify health
- **Main portion**: Implement feature
- **Last 10 min**: Test, update Archon, commit, handoff

If running low on context/time:
1. Stop at a clean point
2. Update task with progress notes
3. Commit partial work
4. Update session notes with "in progress" status
5. Handoff for next session to continue
