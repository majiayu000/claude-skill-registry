---
description:
  Implement a story with test-driven development. Phase 4 Implementation
user-invocable: true
disable-model-invocation: true
---

# Dev Story Workflow

**Goal:** Implement a story by executing its tasks/subtasks with comprehensive
test coverage.

**Agent:** DEV (Amelia) **Phase:** 4 - Implementation

---

## CRITICAL RULES

**These rules have NO EXCEPTIONS:**

1. Execute ALL steps in exact order - do NOT skip
2. Only modify permitted story file sections: Tasks/Subtasks checkboxes, Dev
   Agent Record, File List, Change Log, Status
3. DO NOT stop for "milestones" or "significant progress" - continue until
   COMPLETE or HALT condition
4. Follow red-green-refactor cycle: failing tests first, minimal code to pass,
   then refactor
5. NEVER mark a task complete unless tests actually exist and pass 100%
6. NEVER implement anything not mapped to a specific task/subtask

---

## WORKFLOW STEPS

### Step 1: Find and Load Story

**If story path provided:** Use directly

**If sprint status exists:**

1. Load `implementation-artifacts/sprint-status.yaml`
2. Find first story with status `ready-for-dev`
3. Load complete story file

**If no ready story:**

- Offer to run `create-story`
- Or accept user-provided story path

### Step 2: Load Project Context

1. Load `project-context.md` if exists
2. Parse story sections: Story, Acceptance Criteria, Tasks/Subtasks, Dev Notes,
   Dev Agent Record, File List, Change Log, Status
3. Extract developer guidance from Dev Notes

### Step 3: Detect Continuation

Check if resuming after code review:

- Look for "Senior Developer Review (AI)" section
- Count pending review follow-up tasks
- Prioritize review items before regular tasks

### Step 4: Mark Story In-Progress

Update sprint status from `ready-for-dev` to `in-progress`

### Step 5: Implement Task (Red-Green-Refactor)

For each task/subtask:

**RED Phase:**

- Write FAILING tests first
- Confirm tests fail (validates correctness)

**GREEN Phase:**

- Implement MINIMAL code to pass tests
- Run tests to confirm pass
- Handle error conditions

**REFACTOR Phase:**

- Improve code structure
- Keep tests green
- Follow architecture patterns

### Step 6: Author Comprehensive Tests

- Unit tests for business logic
- Integration tests for component interactions
- End-to-end tests for critical flows
- Edge cases and error handling

### Step 7: Run Validations

- Run all existing tests (no regressions)
- Run new tests (implementation correctness)
- Run linting/code quality checks
- Validate against acceptance criteria

### Step 8: Mark Task Complete

**Validation Gates (ALL must pass):**

- Tests ACTUALLY exist and pass 100%
- Implementation matches task specification exactly
- All related acceptance criteria satisfied
- No regressions

**Then:**

- Mark task checkbox [x]
- Update File List
- Add completion notes
- Loop to Step 5 for next task

### Step 9: Story Completion

- Verify ALL tasks marked [x]
- Run full regression suite
- Execute definition-of-done checklist
- Update Status to `review`

### Step 10: Communication

- Summarize accomplishments
- Provide story file path
- Offer explanations based on user skill level
- Suggest next steps (code-review, etc.)

---

## HALT CONDITIONS

Stop execution if:

- 3 consecutive implementation failures
- Missing required configuration
- New dependencies need user approval
- Any validation fails and cannot be fixed
- User provides other instruction

---

## OUTPUTS

**Story File Updates:**

- Tasks/Subtasks checkboxes marked [x]
- Dev Agent Record with implementation notes
- File List with all changed files
- Change Log with summary
- Status updated to `review`

**Sprint Status Updates:**

- Story status: `ready-for-dev` → `in-progress` → `review`

---

## INSTRUCTIONS FILE

For detailed step-by-step XML instructions, see:
`${CLAUDE_PLUGIN_ROOT}/skills/dev-story/instructions.xml`
