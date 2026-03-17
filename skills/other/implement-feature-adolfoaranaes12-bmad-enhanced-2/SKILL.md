---
name: implement-feature
description: Implement features from task specifications using Test-Driven Development (TDD) with bmad-commands for file operations and testing. This skill should be used when implementing new functionality from approved task specs.
acceptance:
  - tests_passing: "All tests must pass"
  - coverage_threshold: "Test coverage >= 80%"
  - no_syntax_errors: "Code must have no syntax errors"
  - task_spec_loaded: "Task specification successfully loaded"
  - requirements_met: "All acceptance criteria from task spec addressed"
inputs:
  task_id:
    type: string
    required: true
    description: "Task identifier (e.g., task-auth-002-login)"
    validation: "Must match pattern: task-{component}-{number}-{slug}"
  subtask_id:
    type: string
    required: false
    description: "Optional subtask identifier to implement only a specific subtask (e.g., subtask-1, subtask-2)"
    validation: "Must match pattern: subtask-{number} if provided"
outputs:
  implementation_complete:
    type: boolean
    description: "Whether implementation is complete and meets all criteria"
  test_coverage_percent:
    type: number
    description: "Test coverage percentage achieved"
  files_modified:
    type: array
    description: "List of files created or modified"
  tests_passed:
    type: boolean
    description: "Whether all tests passed"
telemetry:
  emit: "skill.implement-feature.completed"
  track:
    - task_id
    - test_coverage_percent
    - duration_ms
    - files_modified_count
    - tests_total
    - tests_passed
    - tests_failed
---

# Implement Feature Skill

## Purpose

Implement features from task specifications or user stories using Test-Driven Development (TDD). This skill writes tests first, implements code to make tests pass, and validates the implementation meets all acceptance criteria.

**Core Principles:**
- Test-Driven Development (Red → Green → Refactor)
- Deterministic operations via bmad-commands
- Automated acceptance criteria verification
- Continuous validation

## Prerequisites

- Task specification exists at workspace/tasks/{task_id}.md
- bmad-commands skill available at `.claude/skills/bmad-commands/`
- Development environment configured
- Test framework installed (Jest or Pytest)

---

## Workflow

### Step 0: Load Task Specification

**Action:** Use bmad-commands to load task spec.

Execute:
```bash
python .claude/skills/bmad-commands/scripts/read_file.py \
  --path workspace/tasks/{task_id}.md \
  --output json
```

**Parse Response:**
- Verify `success == true`
- Extract `outputs.content` for task specification
- Parse sections: Objective, Acceptance Criteria, Context, Tasks

**If task spec not found:**
- Error: `file_not_found` in `errors` array
- Action: Create task spec first using `create-task-spec` skill
- Halt implementation

**If subtask_id is provided:**
- Parse the task specification to locate the specific subtask section
- Filter acceptance criteria to only those related to the subtask
- Scope implementation to only the subtask requirements
- Note: All workflow steps below apply only to the selected subtask

**See:** `references/templates.md` for required task spec format

---

### Step 1: Analyze Requirements

**Action:** Break down acceptance criteria into test cases.

For each acceptance criterion:
1. Identify what needs to be tested (behavior/outcome)
2. Determine test type (unit/integration/e2e)
3. Plan test structure and data
4. Identify edge cases

**Example Analysis:**
```
AC-1: User can log in with valid credentials

Test Cases:
- [Unit] Should return user object when credentials valid
- [Unit] Should return null when email not found
- [Unit] Should return null when password incorrect
- [Integration] Should create session when login successful
- [Integration] Should return 401 when login fails
```

**Identify Files:**
- Files to create (new implementation + tests)
- Files to modify (existing routes, config)
- Files to reference (existing models, utilities)

**See:** `references/requirement-analysis-guide.md` for detailed analysis patterns

---

### Step 2: Write Tests (TDD Red Phase)

**Action:** Write failing tests that cover all acceptance criteria.

**Run Tests:**
```bash
python .claude/skills/bmad-commands/scripts/run_tests.py \
  --path . \
  --framework auto \
  --output json
```

**Verify RED Phase:**
- Parse response: `outputs.passed == false`
- Tests fail because implementation doesn't exist (not syntax errors)

**If tests pass in RED phase:**
- Tests are invalid (code already exists)
- Refine tests to be more specific

**See:** `references/test-examples.md` for comprehensive test patterns and structure

---

### Step 3: Implement Code (TDD Green Phase)

**Action:** Write minimum code to make tests pass.

**Implementation Strategy:**
1. Start with simplest test first
2. Implement just enough to pass that test
3. Run tests after each small change
4. Keep refactoring for later (Green phase)

**Run Tests:**
```bash
python .claude/skills/bmad-commands/scripts/run_tests.py \
  --path . \
  --framework auto \
  --output json
```

**Verify GREEN Phase:**
- Parse response: `outputs.passed == true`
- Check `outputs.coverage_percent >= 80`
- Verify `outputs.failed_tests == 0`

**If tests still failing:**
- Review failure messages in `outputs.failures`
- Fix implementation
- Re-run tests
- Repeat until GREEN

**See:** `references/implementation-examples.md` for implementation patterns

---

### Step 4: Refactor (TDD Refactor Phase)

**Action:** Improve code quality while keeping tests green.

**Refactoring Targets:**
- Remove duplication (DRY principle)
- Improve naming (clarity)
- Extract functions/methods (single responsibility)
- Simplify conditionals (readability)
- Add type safety
- Enhance error handling

**After Each Refactor:**
```bash
python .claude/skills/bmad-commands/scripts/run_tests.py \
  --path . \
  --framework auto \
  --output json
```

**Verify tests stay green:**
- `outputs.passed == true` after each refactor
- If tests break, revert refactor
- Only commit refactors that keep tests green

**See:** `references/refactoring-patterns.md` for common refactoring techniques

---

### Step 5: Verify Acceptance Criteria

**Action:** Check that all acceptance criteria from task spec are met.

For each acceptance criterion:
1. Identify corresponding tests
2. Verify tests pass
3. Verify behavior matches requirement
4. Check edge cases covered

**Automated Verification:**
```bash
# Run full test suite
python .claude/skills/bmad-commands/scripts/run_tests.py \
  --path . \
  --framework auto \
  --output json
```

**Check:**
- `outputs.passed == true`
- `outputs.coverage_percent >= 80`
- `outputs.total_tests >= expected_count`
- All acceptance criteria have corresponding passing tests

**Manual Verification:**
- Review code against technical specifications
- Verify API contracts match spec
- Check data models are correct
- Ensure error handling is complete

---

### Step 6: Run Validation Suite

**Action:** Run comprehensive checks before completion.

**Validation Checks:**
1. All tests passing
2. Coverage >= 80%
3. No syntax errors
4. No linting errors
5. All files created as specified
6. Code follows project standards

**Run Final Tests:**
```bash
python .claude/skills/bmad-commands/scripts/run_tests.py \
  --path . \
  --framework auto \
  --output json
```

**Acceptance Criteria Verification:**
- ✅ `tests_passing`: `outputs.passed == true`
- ✅ `coverage_threshold`: `outputs.coverage_percent >= 80`
- ✅ `no_syntax_errors`: No syntax errors in output
- ✅ `task_spec_loaded`: Task spec was successfully loaded in Step 0
- ✅ `requirements_met`: All acceptance criteria verified in Step 5

**See:** `references/validation-guide.md` for complete validation procedures

---

## Output

Return structured output with implementation status, test results, and telemetry.

**See:** `references/templates.md` for complete output format and examples

---

## Error Handling

If any step fails:

- **Task Spec Not Found:** Create task spec first using `create-task-spec` skill
- **Tests Failing:** Review failures in outputs, fix code, re-run
- **Coverage Below Threshold:** Add more tests to reach 80%
- **Syntax Errors:** Fix syntax errors, re-run tests

**See:** `references/error-scenarios.md` for detailed error handling strategies

---

## Common Scenarios

### Scenario 1: Ambiguous Requirements

If acceptance criteria are unclear or not testable:
- Halt implementation
- Request requirement refinement
- Suggest using `refine-story` skill

### Scenario 2: Missing Dependencies

If implementation requires files that don't exist:
- Check if dependency is from another task
- Suggest implementing dependency task first
- OR expand scope to include dependency (with user approval)

### Scenario 3: Tests Failing After Refactor

If tests break during refactoring:
- Revert the refactor
- Run tests to verify green again
- Try smaller refactoring step
- Ensure tests are correct (not implementation-dependent)

### Scenario 4: Large Task with Multiple Subtasks

If a task has multiple independent subtasks that can be implemented separately:
- Use the `--subtask` flag to implement one subtask at a time
- Example: `/implement-feature workspace/tasks/task-auth-002.md --subtask subtask-1`
- This allows for incremental development and easier code review
- Each subtask should have its own tests and can be committed independently

---

## Best Practices

1. **Follow TDD Cycle** - Red → Green → Refactor, no shortcuts
2. **Keep Tests Focused** - One test per behavior
3. **Mock External Dependencies** - Database, APIs, file system
4. **Commit Frequently** - After each TDD phase

**See:** `references/best-practices.md` for detailed TDD best practices

---

## Routing Guidance

**Use this skill when:**
- Task complexity is simple to medium (≤60 complexity score)
- Changes affect ≤5 files
- No breaking changes or migrations
- Clear, testable acceptance criteria

**Use alternative when:**
- High complexity (>60 complexity score)
- Large scale changes (>5 files)
- Breaking changes requiring discovery phase
- Migrations or schema changes
- → Route to: `implement-with-discovery` skill

**Complexity Assessment:**
- **Low (0-30):** 1-2 files, no database/API changes → Use this skill
- **Medium (31-60):** 3-5 files, minor schema changes → Use this skill with caution
- **High (61-100):** 6+ files, migrations, breaking changes → Use `implement-with-discovery`

---

## Reference Files

- `references/requirement-analysis-guide.md` - Analyze acceptance criteria, plan tests
- `references/test-examples.md` - Complete test patterns (unit, integration, e2e)
- `references/implementation-examples.md` - Code implementation patterns
- `references/refactoring-patterns.md` - Common refactoring techniques
- `references/validation-guide.md` - Complete validation procedures
- `references/error-scenarios.md` - Error handling strategies
- `references/best-practices.md` - TDD and testing best practices
- `references/templates.md` - Task spec format, output format, commit templates

---

## Using This Skill

Invoked by James subagent with routing, or called directly with task_id input.

---

*Part of BMAD Enhanced Development Suite*
