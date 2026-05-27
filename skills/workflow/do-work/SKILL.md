---
name: do-work
description: Execute development work from a scratchpad, tracking progress with TodoWrite and making atomic commits. This skill MUST be invoked as the first action when user says "start work on issue #X", "do work on issue #X", "work on issue #X", "continue work", "resume work", or "keep working". Do not fetch issue details or plan manually.
tools:
  - mcp__serena__*
  - Read
  - Edit
  - Write
  - Bash:git *
  - Glob
  - Grep
  - TodoWrite
  - AskUserQuestion
  - Skill
  - Task
  - LSP
  - EnterPlanMode
---

# Work Session Skill

## Purpose

Execute implementation work from a scratchpad in a structured, trackable way. This skill loads the implementation plan, creates TodoWrite items for visibility, works through tasks systematically, and coordinates commits after task completion.

## Natural Language Triggers

This skill activates when the user says things like:
- "Start work on issue #42" (default trigger)
- "Do work on issue #42"
- "Work on issue #42"
- "Continue work on this issue"
- "Resume work"
- "Keep working"
- "Let's work through the scratchpad"
- "Work on the next task"
- "Pick up where we left off"

## Workflow Execution

### Phase 0: Check Scratchpad Exists (Self-Correction)

**Before proceeding with work, verify scratchpad exists:**

1. **Detect Scratchpad:**
   - Look for `SCRATCHPAD_{issue_number}.md` in project root
   - If issue number provided, look for specific scratchpad

2. **If scratchpad NOT found:**
   ```
   ❌ No scratchpad found for issue #{number}

   Would you like to run setup-work first?
   ```

   Use AskUserQuestion:
   ```
   AskUserQuestion:
     questions:
       - question: "No scratchpad found. Run setup-work to initialize?"
         header: "Setup Required"
         multiSelect: false
         options:
           - label: "Yes, run setup-work"
             description: "Create scratchpad and branch for this issue"
           - label: "No, create manually"
             description: "I'll set up the scratchpad myself"
   ```

   If user chooses "Yes":
   ```
   Skill: setup-work
   args: "{issue_number}"
   ```

   **STOP here** - setup-work will create scratchpad and can chain to do-work after.

3. **If scratchpad exists:**
   - Proceed to Phase 1 (normal work flow)

### Phase 1: Validate Setup

1. **Load Scratchpad:**
   - Scratchpad confirmed to exist from Phase 0
   - Read full scratchpad content
   - Parse implementation checklist
   - Identify completed vs pending tasks

2. **Verify Branch:**
   - Check current branch matches expected feature branch
   - If not, offer to switch:
     ```
     AskUserQuestion:
       question: "Switch to feature branch {branch-name}?"
       options:
         - "Yes, switch branches"
         - "No, stay on current branch"
     ```

4. **Resume Detection:**
   - Check Work Log for previous session
   - Identify last task in progress
   - Offer to resume or start fresh

### Phase 2: Initialize TodoWrite

Create TodoWrite items from scratchpad checklist:

```
TodoWrite:
  todos:
    - content: "{Task 1 description}"
      status: "completed"  # if already done
      activeForm: "{Task 1 active description}"
    - content: "{Task 2 description}"
      status: "in_progress"  # current task
      activeForm: "{Task 2 active description}"
    - content: "{Task 3 description}"
      status: "pending"
      activeForm: "{Task 3 active description}"
    ...
```

**Sync Strategy:**
- TodoWrite = Live UI progress (transient, session-based)
- Scratchpad = Persistent record with notes (survives sessions)
- Keep both in sync: when TodoWrite updates, update scratchpad checkboxes

### Phase 3: Work Loop

For each unchecked item in the Implementation Checklist:

#### 3.1 Start Task

1. **Update TodoWrite:**
   - Mark current task as `in_progress`
   - All others remain `pending` or `completed`

2. **Display Task:**
   ```
   📍 Working on: {task description}
      Files: {affected files}
      Why: {rationale}
   ```

3. **Update Scratchpad Work Log:**
   ```markdown
   ### {Date} - Session Start
   - Starting: {task description}
   ```

#### 3.2 Implement Task

**Before starting implementation, assess complexity:**

**Complex Task Detection → EnterPlanMode:**
If the task involves:
- Changes to more than 3-4 files
- Multiple valid implementation approaches
- New patterns or architectural decisions
- Significant refactoring

Then suggest entering plan mode:
```
AskUserQuestion:
  question: "This task appears complex ({reason}). Enter plan mode first?"
  header: "Approach"
  options:
    - "Yes, plan first"
      description: "Enter plan mode to design approach before implementing"
    - "No, proceed directly"
      description: "Start implementing without formal planning"
```

If user chooses to plan, use `EnterPlanMode` tool.

**Delegate Complex Subtasks → Task Tool:**
For complex analysis or exploration during implementation:
```
Task:
  subagent_type: Explore
  prompt: "Find all usages of {pattern} and how they integrate with {module}"
  description: "Explore {area} for implementation"
```

**Execute the actual work:**
- Use LSP for code navigation (goToDefinition, findReferences, documentSymbol)
- Create/modify files as needed
- Run relevant commands
- Test changes locally

#### 3.3 Complete Task

1. **Update TodoWrite:**
   - Mark task as `completed`
   - Move to next task

2. **Update Scratchpad:**
   - Check off completed item: `- [x] {task}`
   - Add notes to Work Log:
     ```markdown
     - Completed: {task description}
       - Notes: {any decisions or observations}
     ```

3. **Offer Commit:**
   ```
   AskUserQuestion:
     question: "Task complete. Ready to commit?"
     header: "Commit"
     options:
       - "Yes, commit now"
         description: "Invoke commit-changes skill for this task"
       - "Continue to next task"
         description: "Skip commit, keep working"
       - "Review changes first"
         description: "Show me what changed before committing"
   ```

4. **If committing:** Invoke `commit-changes` skill
   ```
   Skill: commit-changes
   ```

5. **Progress Update:**
   ```
   ✓ {X} of {Y} tasks complete
   ```

#### 3.4 Handle Blockers

If blocked during a task:

1. **Update Scratchpad:**
   - Add to Questions/Blockers section
   - Note what's blocking progress

2. **Ask User:**
   ```
   AskUserQuestion:
     question: "Encountered blocker: {description}. How to proceed?"
     options:
       - "Help me resolve it"
       - "Skip to next task"
       - "Pause work session"
       - "Add to blockers and continue"
   ```

### Phase 4: Continuous Sync

Throughout the session:

1. **Push Reminders:**
   - After every 2-3 commits, offer to push:
     ```
     📤 You have {N} unpushed commits. Push to remote?
     ```

2. **Progress Persistence:**
   - Keep scratchpad updated with running notes
   - Work Log captures decisions made
   - Checklist reflects completion state

3. **Interruption Handling:**
   - If work is interrupted, save state:
     - Note current task in Work Log
     - Save any uncommitted progress notes
     - Can resume later with same skill

### Phase 5: Completion Check

When all Implementation Tasks are complete:

1. **Quality Checks:**
   - Run through Quality Checks section of scratchpad
   - Execute linters/tests as applicable
   - Self-review for code quality

2. **Verify Acceptance Criteria:**
   - Review original acceptance criteria
   - Confirm all are met

3. **Update Scratchpad:**
   ```markdown
   ### {Date} - Session Complete
   - All implementation tasks complete
   - Quality checks: {passed/issues}
   - Ready for PR: {yes/no}
   ```

4. **Final TodoWrite:**
   - All tasks marked `completed`
   - Clear visual confirmation of completion

### Phase 6: Next Steps

Present options:

```
✅ All tasks complete!

Options:
1. Create PR → Invoke create-pr skill
2. Archive scratchpad → Invoke archive-work skill
3. Continue in session → Keep working (add more tasks?)
4. End session → Save state and exit

Select option:
```

## State Management

### TodoWrite ↔ Scratchpad Sync

| Action | TodoWrite | Scratchpad |
|--------|-----------|------------|
| Task starts | `in_progress` | Work Log entry |
| Task completes | `completed` | Checkbox checked, Work Log note |
| Task blocked | stays `in_progress` | Blockers section updated |
| Session ends | cleared | Work Log "session end" |
| Session resumes | rebuilt from scratchpad | Work Log "session resume" |

### Progress Recovery

If Claude Code restarts mid-session:
1. Re-read scratchpad
2. Rebuild TodoWrite from checklist state
3. Resume from last incomplete task

## Error Handling

### Scratchpad Not Found
```
❌ No scratchpad found for issue #{number}

   Would you like to:
   1. Run setup-work for this issue
   2. Specify a different issue number
   3. Create a new scratchpad manually
```

### Wrong Branch
```
⚠️ Expected branch: {expected}
   Current branch: {current}

   Would you like to switch branches?
```

### Uncommitted Changes from Previous Session
```
⚠️ Found uncommitted changes from previous work.

   Options:
   1. Commit these changes now
   2. Stash and continue
   3. Review changes first
```

## Integration with Other Skills

**Invokes:**
- `commit-changes` skill - After completing tasks
- `create-pr` skill - When all tasks complete
- `archive-work` skill - After PR created

**Invoked by:**
- User directly via natural language
- After `setup-work` skill completes

**Reads from:**
- Scratchpad - Implementation plan
- Project CLAUDE.md - Conventions

## Best Practices

### ✅ DO:
- Keep TodoWrite in sync with scratchpad
- Add notes to Work Log for decisions
- Commit after each logical task
- Update blockers promptly
- Review progress periodically

### ❌ DON'T:
- Skip TodoWrite updates
- Let scratchpad get stale
- Batch too many changes before committing
- Ignore blockers
- Leave session without saving state

---

**Version:** 1.1.0
**Last Updated:** 2025-12-31
**Maintained By:** Escapement
**Changelog:**
- v1.1.0: Added EnterPlanMode for complex tasks, Task delegation, LSP navigation
- v1.0.0: Initial conversion from commands/start-work.md
