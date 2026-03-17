---
name: execute-tasks
description: This skill should be used when executing tasks from ai-state/active/tasks.yaml sequentially. It loads tasks, gathers context, implements features with phase-appropriate testing, updates task status in tasks.yaml, organizes tests into ai-state/regressions/ folders, and logs all operations to operations.log. Use after write-plan creates tasks.yaml or when resuming development work.
---

# Execute-Tasks Skill

## Purpose

Sequentially execute tasks from `ai-state/active/tasks.yaml` with proper context gathering, phase-appropriate testing, automatic test organization, status tracking, and comprehensive logging.

## When to Use

Use this skill when:
- After `/write-plan` creates tasks.yaml
- Starting development work
- Resuming work after breaks
- Processing task backlog
- Executing sprint work

## CRITICAL: Logging Requirements

**BEFORE YOU DO ANYTHING ELSE, LOG IT!**

Use the unified logging system via `.claude\scripts\log_task.bat` (Windows) or `log_operation.py`:

```bash
# Simple format (Windows):
.claude\scripts\log_task.bat TYPE TASK_ID "message"

# Full format (cross-platform):
python .claude/scripts/log_operation.py --type TYPE --task TASK_ID "message"
```

**Required logging for EVERY task:**
1. Log "Step X: [Step Name]" BEFORE starting each major step (1-8)
2. Log narrative BEFORE executing each substep that modifies state
3. Log all mandatory operation events (task.started, context.gathered, etc.)

**Example logging sequence for Step 2:**
```bash
# Log step header
.claude\scripts\log_task.bat narrative task-001-fastapi-setup "Step 2: Gather Context"

# Log substep 2.1
.claude\scripts\log_task.bat narrative task-001-fastapi-setup "Step 2.1: Load relevant files"

# Log substep 2.2
.claude\scripts\log_task.bat narrative task-001-fastapi-setup "Step 2.2: Save context snapshot"

# Log narrative before action (substep 2.3)
.claude\scripts\log_task.bat narrative task-001-fastapi-setup "Gathering context from backend standards and checking existing project files"

# Log completion (substep 2.4)
.claude\scripts\log_task.bat context task-001-fastapi-setup
```

**DO NOT skip these logs!** They provide visibility into your execution process.

**See `.claude/scripts/LOGGING_GUIDE.md` for complete reference.**

## Step-by-Step Execution Process

For each task with `status: pending` in tasks.yaml, follow these steps in exact order:

### Step 1: Load and Prepare Task

**FIRST: Log this step header**
```bash
.claude\scripts\log_task.bat narrative {task_id} "Step 1: Load and Prepare Task"
```

**1.1 Read the task and sprint context**:
- Read `ai-state/active/tasks.yaml`
- Extract top-level: phase
- Navigate into `sprints` array, find current sprint
- Extract sprint context: sprint, milestone, complexity_range
- Find first task with `status: pending` within the sprint's tasks
- Extract task fields: id, status, complexity, context, who, where, what, how, goal, check, close

**1.2 Update status to in_progress**:
- Use Edit tool to change task status from `pending` to `in_progress` in tasks.yaml
- Save the file

**1.3 Log task start**:
```bash
.claude\scripts\log_task.bat started {task_id} "{what}"
```

**1.4 Create progress tracking**:
- Use TodoWrite to create entry for this task with status `in_progress`

### Step 2: Gather Context

**FIRST: Log this step header**
```bash
.claude\scripts\log_task.bat narrative {task_id} "Step 2: Gather Context"
```

**2.1 Load relevant files**:
```bash
.claude\scripts\log_task.bat narrative {task_id} "Step 2.1: Load relevant files"
```
- Read files mentioned in task's `where` field
- Read standards from `ai-state/standards/{standard}.md` if referenced in `how`
- Search for related code in codebase

**2.2 Save context snapshot**:
```bash
.claude\scripts\log_task.bat narrative {task_id} "Step 2.2: Save context snapshot"
```
- Create `ai-state/contexts/{sprint}/{task_id}.md` with:
  - Full task specification
  - Relevant code snippets
  - Standards being followed
  - Dependencies noted
- **NOTE**: Contexts are organized by sprint folder for better organization

**2.3 Log narrative action**:
```bash
.claude\scripts\log_task.bat narrative {task_id} "Gathering context from backend standards and checking existing project files"
```

**2.4 Log context gathering**:
```bash
.claude\scripts\log_task.bat context {task_id}
```

### Step 3: Execute Implementation

**FIRST: Log this step header**
```bash
.claude\scripts\log_task.bat narrative {task_id} "Step 3: Execute Implementation"
```

**3.1 Implement the feature**:
- Follow the `what` description exactly
- Achieve the `goal` criteria
- Reference standards from `how` field
- Write files to locations in `where` field

**3.2 Use appropriate tools**:
- Write tool for new files
- Edit tool for existing files
- Follow coding standards from the `how` field

**3.3 Log narrative action**:
```bash
.claude\scripts\log_task.bat narrative {task_id} "Creating requirements.txt and main.py with FastAPI initialization"
```

**3.4 Log implementation**:
```bash
.claude\scripts\log_task.bat implemented {task_id}
```

### Step 4: Write Phase-Appropriate Tests

**FIRST: Log this step header**
```bash
.claude\scripts\log_task.bat narrative {task_id} "Step 4: Write Phase-Appropriate Tests"
```

**4.1 Determine required test count**:
Read `.khujta/phase.json` and write tests based on phase:
- **Prototype**: 2 tests (smoke + happy path)
- **MVP**: 4 tests (smoke, happy, error, auth)
- **Growth**: 5 tests (+ edge cases)
- **Scale**: 6-8 tests as needed

**4.2 Create test file**:
- Name: `test_{component}.py` (or appropriate for stack)
- Location: Project root directory (will move later)
- Use Write tool to create file

**4.3 Write test cases**:
- Test 1 (smoke): Basic functionality from `check.valid`
- Test 2 (happy path): Main use case from goal
- Additional tests per phase requirements
- Cover `check.error` scenarios

**4.4 Log narrative action**:
```bash
.claude\scripts\log_task.bat narrative {task_id} "Writing 2 tests (smoke + happy path) for FastAPI server startup validation"
```

**4.5 Log test creation**:
```bash
.claude\scripts\log_task.bat tests-written {task_id} "2 tests"
```

### Step 5: Run Tests and Verify

**FIRST: Log this step header**
```bash
.claude\scripts\log_task.bat narrative {task_id} "Step 5: Run Tests and Verify"
```

**5.1 Execute tests**:
- Use Bash tool: `pytest test_{component}.py -v`
- Capture output

**5.2 If tests FAIL**:
1. Debug the issue
2. Fix implementation or test
3. Re-run tests
4. Repeat until ALL tests pass
5. **DO NOT proceed** until tests pass

**5.3 Log test results**:
```bash
.claude\scripts\log_task.bat tests-passed {task_id} "2/2 passing"
```

### Step 6: Organize Tests into Regressions

**FIRST: Log this step header**
```bash
.claude\scripts\log_task.bat narrative {task_id} "Step 6: Organize Tests into Regressions"
```

**6.1 Determine destination**:
- Use task's `context` field (backend/frontend/database/devops)
- Destination: `ai-state/regressions/{context}/`

**6.2 Create directory if needed**:
- Use Bash: `mkdir -p ai-state/regressions/{context}`

**6.3 Log narrative action**:
```bash
.claude\scripts\log_task.bat narrative {task_id} "Moving tests to ai-state/regressions/backend/ directory for organization"
```

**6.4 Move test file**:
- Use Bash: `mv test_{component}.py ai-state/regressions/{context}/`

**6.5 Verify tests still work**:
- Run: `pytest ai-state/regressions/{context}/test_{component}.py -v`
- Update imports if paths changed

**6.6 Log organization**:
```bash
.claude\scripts\log_task.bat tests-organized {task_id} "ai-state/regressions/{context}/"
```

### Step 7: Complete Task

**7.1 Verify completion criteria**:
- Check task meets the `close` criteria
- Verify all `check` requirements passed

**7.2 Update status to completed**:
- Use Edit tool to change status from `in_progress` to `completed` in tasks.yaml
- Save tasks.yaml

**7.3 Log completion**:
```bash
.claude\scripts\log_task.bat completed {task_id} "{close}"
```

**7.4 Update progress tracking**:
- Use TodoWrite to mark task as completed

### Step 8: Proceed to Next Task

**8.1 Check sprint boundary**:
- Read tasks.yaml and identify current sprint (sprint with in_progress or just-completed tasks)
- Check if current sprint has any remaining `status: pending` tasks
- If current sprint is complete BUT next sprint has pending tasks:
  - **STOP EXECUTION** - Do not proceed to next sprint automatically
  - Show message: "Sprint {N} complete. Run `/core:execute-tasks` again to start Sprint {N+1}"
  - This allows human review of sprint completion before starting next sprint

**8.2 Find next task in CURRENT sprint**:
- Look for next task with `status: pending` **in the current sprint only**
- Check task's `when` field for dependencies
- If dependencies not met, skip to next available task **in current sprint**

**8.3 Repeat process**:
- If pending task found in current sprint: Return to Step 1 with the new task
- If no pending tasks in current sprint: Proceed to Step 9

**8.4 When current sprint complete**:
- If no more pending tasks **in current sprint**, proceed to Step 9: Sprint Completion
- Do NOT automatically continue to next sprint

### Step 9: Sprint Completion (When Current Sprint Done)

**TRIGGER**: When no more `pending` tasks remain **in the current sprint**

**9.1 Verify sprint completion**:
- Count tasks with `status: completed` **in current sprint**
- Count tasks with `status: blocked` or failed **in current sprint**
- Confirm all tasks in current sprint have a final status (no pending remain)

**9.2 Run sprint completion script**:
```bash
python .claude/scripts/complete_sprint.py
```

This automatically generates:
1. **Test runner scripts**: `ai-state/regressions/{context}/run.bat` and `run.sh`
2. **Sprint report**: `ai-state/reports/{sprint}-report.md`
3. **Test results**: `ai-state/reports/{sprint}-test-results.json`
4. **Human docs**: `ai-state/human-docs/{sprint}-summary.md`
5. **Operations log entry**: Sprint completion logged

**9.3 Verify outputs**:
- Check that all regression tests passed
- Review sprint report for completeness
- Confirm human docs are stakeholder-ready

**9.4 Check for next sprint**:
- If more sprints exist in tasks.yaml with pending tasks:
  - **Display message**: "✅ Sprint {N} complete! Review reports in ai-state/reports/ and ai-state/human-docs/"
  - **Display message**: "📋 Sprint {N+1} is ready. Run `/core:execute-tasks` when ready to start."
  - **STOP** - Do not continue automatically
- If no more sprints:
  - Display message: "🎉 All sprints complete! Project ready for next phase."

**NOTE**: Sprint completion runs in ALL phases including prototype. It's no longer just for Growth/Scale phases.

## Required Log Entries Per Task

Every task execution MUST create these log entries in `ai-state/operations.log`:

### Mandatory Operation Logs (7 minimum)
1. `[timestamp] [phase] [sprint] task.started: {task_id} - {what}`
2. `[timestamp] [phase] [sprint] context.gathered: {task_id}`
3. `[timestamp] [phase] [sprint] implementation.complete: {task_id}`
4. `[timestamp] [phase] [sprint] tests.written: {task_id} - {count} tests`
5. `[timestamp] [phase] [sprint] tests.passed: {task_id} - {count}/{count} passing`
6. `[timestamp] [phase] [sprint] tests.organized: {task_id} → ai-state/regressions/{context}/`
7. `[timestamp] [phase] [sprint] task.completed: {task_id} - {close}`

### Narrative Logs (4 minimum - logged BEFORE executing each major step)
Before Step 2: `[timestamp] [phase] [sprint] narrative: {task_id} - {description of what you're about to do}`
Before Step 3: `[timestamp] [phase] [sprint] narrative: {task_id} - {description of implementation about to execute}`
Before Step 4: `[timestamp] [phase] [sprint] narrative: {task_id} - {description of tests about to write}`
Before Step 6: `[timestamp] [phase] [sprint] narrative: {task_id} - {description of test organization}`

**Examples of narrative logs:**
- "narrative: task-001 - Gathering context from backend standards and checking existing files"
- "narrative: task-001 - Creating requirements.txt and main.py with FastAPI initialization"
- "narrative: task-001 - Writing 2 tests (smoke + happy path) for server startup validation"
- "narrative: task-001 - Moving tests to ai-state/regressions/backend/ directory"

**Total minimum log entries per task: 11** (7 mandatory operations + 4 narratives)

**Log Format**:
- `[timestamp]`: ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)
- `[phase]`: Phase from top-level tasks.yaml (e.g., prototype, mvp)
- `[sprint]`: Sprint name from sprints array (e.g., sprint-1)
- `{task_id}`: Task identifier (e.g., task-001-fastapi-setup)
- Additional context as specified per entry

## Phase Requirements Reference

**Prototype** (0-100 users, 30 min to ship):
- Tests: 2 (smoke + happy path)
- Coverage: 40%
- Quality: 6.0/10

**MVP** (100-1K users, 1-2 hours):
- Tests: 4 (+ errors + auth)
- Coverage: 60%
- Quality: 7.0/10

**Growth** (1K-10K users, 2-4 hours):
- Tests: 5 (+ edge cases)
- Coverage: 70%
- Quality: 7.5/10

**Scale** (10K+ users, 4-8 hours):
- Tests: 6-8 as needed
- Coverage: 80%
- Quality: 8.0/10

## Error Handling

**If implementation fails**:
1. Log error to operations.log: `[timestamp] [epic] [sprint] task.failed: {task_id} - {error}`
2. Update status to `blocked` in tasks.yaml
3. Create note in `ai-state/debt/{task_id}-failure.md`
4. Skip to next task

**If tests fail after 3 attempts**:
1. Log: `[timestamp] [epic] [sprint] tests.failed: {task_id} - {failure_details}`
2. Mark task as `blocked`
3. Save test output to `ai-state/debt/{task_id}-test-failures.txt`
4. Skip to next task

**If dependencies missing**:
1. Log: `[timestamp] [epic] [sprint] task.blocked: {task_id} - waiting for {dependency}`
2. Update status to `blocked`
3. Skip to next available task

## Files Modified

**Reads from**:
- `ai-state/active/tasks.yaml`
- `.khujta/phase.json`
- `ai-state/standards/{standard}.md`
- Files mentioned in task's `where`

**Writes to**:
- `ai-state/operations.log` (append all operations)
- `ai-state/active/tasks.yaml` (update status fields)
- `ai-state/contexts/{sprint}/{task_id}.md` (save context)
- `ai-state/regressions/{context}/` (move test files)
- Implementation files per task's `where` field
- `ai-state/reports/{sprint}-*.md` (on sprint completion)
- `ai-state/human-docs/{sprint}-*.md` (on sprint completion)

## Tools Required

- **Read**: Load tasks, context, standards
- **Write**: Create new implementation files, tests, context docs
- **Edit**: Modify existing files, update tasks.yaml status
- **Bash**: Run tests, create directories, move files
- **TodoWrite**: Track real-time progress

## Success Criteria

A successful execution produces:

✅ All pending tasks now `completed` or `blocked` with documented reason
✅ All tests passing and organized in `ai-state/regressions/{context}/`
✅ Complete `operations.log` with minimum 11 entries per task (7 operations + 4 narratives)
✅ Updated `tasks.yaml` with all status changes
✅ Context preserved in `ai-state/contexts/{sprint}/{task_id}.md` for each task
✅ TodoWrite list reflects final state
✅ Sprint completion reports generated (when all tasks done)

## Critical Rules

- **Sequential only**: Execute one task at a time, never skip ahead
- **Status updates required**: Always update tasks.yaml before and after each task
- **Tests must pass**: Never mark task completed if tests are failing
- **Tests must be organized**: Always move tests to ai-state/regressions/
- **Logging is mandatory**: Every operation AND narrative must be logged to operations.log (min 11 per task)
- **Narrative before action**: Always log narrative description BEFORE executing each major step
- **TodoWrite for visibility**: Use TodoWrite for real-time progress tracking
- **Phase/Sprint context**: Always extract and include phase/sprint in ALL log entries

## Example Log Entries

For task-001-fastapi-setup in prototype phase, sprint-1:

```
[2025-11-07T01:35:00Z] [prototype] [sprint-1] task.started: task-001-fastapi-setup - Setup FastAPI project structure
[2025-11-07T01:35:10Z] [prototype] [sprint-1] narrative: task-001-fastapi-setup - Gathering context from backend standards and checking existing project files
[2025-11-07T01:35:15Z] [prototype] [sprint-1] context.gathered: task-001-fastapi-setup
[2025-11-07T01:36:00Z] [prototype] [sprint-1] narrative: task-001-fastapi-setup - Creating requirements.txt and main.py with FastAPI initialization
[2025-11-07T01:36:30Z] [prototype] [sprint-1] implementation.complete: task-001-fastapi-setup
[2025-11-07T01:36:45Z] [prototype] [sprint-1] narrative: task-001-fastapi-setup - Writing 2 tests (smoke + happy path) for server startup validation
[2025-11-07T01:37:00Z] [prototype] [sprint-1] tests.written: task-001-fastapi-setup - 2 tests
[2025-11-07T01:37:10Z] [prototype] [sprint-1] tests.passed: task-001-fastapi-setup - 2/2 passing
[2025-11-07T01:37:15Z] [prototype] [sprint-1] narrative: task-001-fastapi-setup - Moving tests to ai-state/regressions/backend/ directory
[2025-11-07T01:37:20Z] [prototype] [sprint-1] tests.organized: task-001-fastapi-setup → ai-state/regressions/backend/
[2025-11-07T01:37:25Z] [prototype] [sprint-1] task.completed: task-001-fastapi-setup - Server running on localhost:8000
```

This format enables easy filtering:
- `grep "prototype" operations.log` - All operations for this phase
- `grep "sprint-1" operations.log` - All operations for this sprint
- `grep "task-001" operations.log` - All operations for specific task
- `grep "task.completed" operations.log` - All completed tasks
- `grep "narrative:" operations.log` - All narrative descriptions showing what was done
