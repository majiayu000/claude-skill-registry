---
name: execute-task
description: Execute approved task specifications sequentially with TDD, comprehensive testing, and validation. This skill should be used for implementing tasks from approved specs with full audit trail.
acceptance:
  - task_loaded: "Task specification successfully loaded and validated"
  - status_updated: "Task status progressed from Approved → InProgress → Review"
  - all_complete: "All tasks and subtasks marked complete"
  - tests_passing: "All tests written and passing"
  - criteria_verified: "All acceptance criteria verified and documented"
  - record_complete: "Implementation Record fully populated"
inputs:
  task_file:
    type: string
    required: true
    description: "Path to task specification file (e.g., .claude/tasks/task-006.md)"
    validation: "Must be existing file with status 'Approved'"
  auto_confirm:
    type: boolean
    required: false
    description: "Skip execution plan confirmation"
    default: false
outputs:
  implementation_complete:
    type: boolean
    description: "Whether all tasks completed successfully"
  tasks_completed:
    type: number
    description: "Number of tasks completed"
  subtasks_completed:
    type: number
    description: "Number of subtasks completed"
  tests_passed:
    type: boolean
    description: "Whether all tests passed"
  total_tests:
    type: number
    description: "Total number of tests executed"
  files_modified:
    type: array
    description: "List of files created or modified"
  status:
    type: string
    description: "Final task status (should be 'Review')"
telemetry:
  emit: "skill.execute-task.completed"
  track:
    - task_file
    - tasks_completed
    - subtasks_completed
    - tests_passed
    - total_tests
    - files_modified_count
    - duration_ms
    - halt_count
---

# Execute Task Skill

## Purpose

Execute approved task specifications sequentially using Test-Driven Development (TDD), with comprehensive validation at each step and full implementation audit trail.

**Core Capabilities:**
- Sequential task/subtask execution with validation gates
- Permission-controlled file modifications
- Comprehensive testing and documentation
- Implementation Record maintenance
- Halt-on-error safeguards

**BMAD Pattern (Key Innovation):**
- ALL context embedded in task spec by planning skill
- Dev reads ONLY task spec + always-load files (coding standards)
- No architecture lookup during implementation
- Result: Focused execution, no context searching, no drift

## Prerequisites

- Task specification file with status "Approved"
- Configuration file (`.claude/config.yaml`) with development settings
- Always-load files (coding standards) available
- Test framework configured (Jest, Pytest, etc.)

---

## Workflow

### Step 0: Load Configuration and Task Specification

**Action:** Load all required context and verify task readiness.

Execute:
```bash
python .claude/skills/bmad-commands/scripts/read_file.py \
  --path .claude/config.yaml \
  --output json

python .claude/skills/bmad-commands/scripts/read_file.py \
  --path {task_file} \
  --output json
```

**Parse Response:**
- Extract `development.alwaysLoadFiles` from config
- Extract task status, objective, acceptance criteria, tasks
- Verify status is "Approved"

**Validation:**
- Configuration file exists and loadable
- Task file exists and loadable
- Task status is "Approved" (halt if Draft/Review/Done)
- Always-load files exist

**Update Status:**
- Change task status from "Approved" to "InProgress"
- Record start time in Implementation Record

**See:** `references/configuration-guide.md` for detailed configuration loading

---

### Step 1: Review Task Context and Plan Execution

**Action:** Review embedded context and present execution plan to user.

**Context Review:**
- Previous task insights
- Data models and schemas
- API specifications
- Component specifications
- File locations
- Testing requirements
- Technical constraints

**Task Breakdown:**
- Count total tasks and subtasks
- Identify current task (first unchecked)
- Understand task dependencies

**Present Plan:** Display execution plan with task name, file, context loaded (task spec + coding standards), execution sequence (numbered tasks with subtask counts), total counts, confirmation prompt

**See:** `references/templates.md#execution-plan-template` for complete format

**Wait for confirmation** unless `auto_confirm=true`

**Halt Conditions:**
- Context appears insufficient
- Task breakdown unclear
- User does not confirm

**See:** `references/task-execution-guide.md` for execution details

---

### Step 2: Execute Current Task

**Action:** Execute each task and subtask sequentially with validation.

**For each task in sequence:**

1. **Announce task:** Display task name with acceptance criteria and subtask list
2. **For each subtask:** Implement (read context, create/modify files per coding standards) | If "Write tests": create and run tests (must pass) | If "Validate": run tests, linter, verify AC | Update checkbox to [x] only when complete | Record notes in Implementation Record (deviations, decisions, learnings)
3. **After all subtasks:** Run task validation (all tests, lint, AC coverage) | Update task checkbox [x] only when validated | Update Implementation Record (files, notes)
4. **Move to next task**

**Halt Conditions:**
- 3 consecutive implementation failures on same subtask
- Ambiguous requirements discovered
- Missing dependencies not documented
- Regression test failures
- User requests halt

**See:** `references/task-execution-guide.md` for detailed execution examples

---

### Step 3: Final Validation and Documentation

**Action:** Run complete validation and finalize documentation.

**Validation:**

1. **Run complete test suite:**
   ```bash
   python .claude/skills/bmad-commands/scripts/run_tests.py \
     --path . \
     --framework auto \
     --output json
   ```

2. **Verify acceptance criteria:**
   - Review each AC from task spec
   - Map AC to implementation and tests
   - Confirm all ACs covered

3. **Verify all checkboxes marked:**
   - Scan task spec for unchecked [ ] boxes
   - Ensure all tasks and subtasks complete

**Documentation:** Update Implementation Record with agent model, completion notes (details, decisions, learnings), files modified (created/modified lists), testing results (unit/integration/regression test counts, coverage %, execution time)

**See:** `references/templates.md#implementation-record-complete-template` for complete format

**Status Update:**
- Change status from "InProgress" to "Review"
- DO NOT mark as "Done" (quality skill does that)

**Present Summary:** Display completion summary with task name, status (Review), what was implemented, all ACs met (with checkmarks), test results (counts, coverage, regression), files created/modified counts, quality review prompt

**See:** `references/templates.md#completion-summary-template` for complete format

**See:** `references/validation-guide.md` for validation details

---

### Step 4: Handle Quality Review (Optional)

**Action:** Provide next steps based on user decision.

**If user requests quality review:** Confirm task marked "Review", provide next step (use quality review skill with task file)

**If user approves without review:** Confirm approval, provide next steps (commit changes, mark "Done", move to next task)

**See:** `references/templates.md#step-4-handle-quality-review` for complete messages

---

## File Modification Permissions

**CRITICAL PERMISSION BOUNDARIES:**

**YOU ARE AUTHORIZED TO:**
- ✅ Update "Implementation Record" section of task file
- ✅ Update task/subtask checkboxes ([ ] to [x])
- ✅ Update task status line (Approved → InProgress → Review)
- ✅ Create, modify, delete implementation files (src/, tests/, etc.)
- ✅ Run commands (tests, linters, builds)

**YOU ARE NOT AUTHORIZED TO:**
- ❌ Modify "Objective" section of task file
- ❌ Modify "Acceptance Criteria" section of task file
- ❌ Modify "Context" section of task file
- ❌ Modify task/subtask descriptions (only checkboxes)
- ❌ Modify "Quality Review" section of task file
- ❌ Change task status to "Done" (only to "Review")

**Enforcement:** Only edit Implementation Record section and checkboxes/status

**See:** `references/permissions-halts.md` for detailed permission boundaries

---

## Halt Conditions

**Must halt execution and ask user when:**

1. **Consecutive Failures (default: 3)**
   - Same subtask fails 3 times in a row
   - Present error and ask for guidance

2. **Ambiguous Requirements**
   - Context insufficient to implement subtask
   - Multiple valid interpretations
   - Critical technical decision needed

3. **Missing Dependencies**
   - Required library/service not documented
   - External API credentials needed
   - Database not accessible

4. **Regression Failures**
   - Existing tests start failing
   - Breaking change introduced

5. **User Interruption**
   - User requests halt
   - User asks question mid-execution

**Halt Message Format:** Display halt warning with reason (category), context (what was attempted), issue (specific problem), need from user (required info/decision), current progress (tasks/subtasks complete vs remaining), ready to resume condition

**See:** `references/templates.md#halt-message-templates` for all halt types

**See:** `references/permissions-halts.md` for halt handling details

---

## Output

Return structured JSON output with implementation_complete (boolean), tasks_completed, subtasks_completed, tests_passed, total_tests, files_modified (array), status, telemetry (skill, task_file, metrics, duration_ms, halt_count)

**See:** `references/templates.md#complete-json-output-format` for full structure and examples (success, with halts, failed)

---

## Error Handling

If any step fails:

**1. Task File Not Found:**
- Error: "Task file not found"
- Action: Verify file path

**2. Task Status Not Approved:**
- Error: "Task must be Approved before execution"
- Action: Check task status, update if needed

**3. Test Failures:**
- Error: "X tests failing"
- Action: Review failures, fix issues, re-run

**4. Missing Dependencies:**
- Error: "Dependency X not found"
- Action: Verify task spec includes dependency info

---

## Best Practices

Trust the task spec (context embedded, don't search) | Sequential execution (complete current before next) | Test before checking (run tests before marking [x]) | Document as you go (update notes after each task) | Respect permissions (only Implementation Record + checkboxes) | Halt when appropriate (don't guess unclear requirements)

**See:** `references/best-practices.md` and `references/templates.md#best-practices-with-examples` for detailed guidance and examples

---

## Routing Guidance

**Use this skill when:**
- Executing an approved task specification
- Need sequential, validated task execution
- Want comprehensive testing and documentation
- Need implementation audit trail

**Always use after:**
- Task spec created and approved
- Planning complete

**Before:**
- Quality review
- Pull request creation

---

## Reference Files

Detailed documentation in `references/`:

- **templates.md**: All output formats, examples, file templates, integration workflows, JSON structures, error templates, command-line usage, best practices with examples
- **configuration-guide.md**: Loading config, always-load files, status management
- **task-execution-guide.md**: Executing tasks/subtasks, validation gates, examples
- **validation-guide.md**: Final validation, documentation, completion summary
- **implementation-record.md**: Templates for Implementation Record section
- **permissions-halts.md**: Permission boundaries, halt conditions, error handling
- **best-practices.md**: Best practices, pitfalls to avoid, integration patterns

---

*Part of BMAD Enhanced Implementation Suite*
