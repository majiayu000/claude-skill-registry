---
name: task-module_testing
description: Domain-agnostic module testing task execution with two-tier skill loading
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Task Module Testing Skill

**Role**: Domain-agnostic task executor skill for executing module testing tasks (profile=module_testing). Loaded by `pm-workflow:task-execute-agent` when `task.profile` is `module_testing`.

**Key Pattern**: Agent loads this skill via `resolve-task-executor --profile module_testing`. Skill executes a test-focused workflow: understand context → plan tests → implement tests → verify. Domain-specific testing knowledge comes from `task.skills` (loaded by agent).

## Contract Compliance

**MANDATORY**: Follow the execution contract defined in:

| Contract | Location | Purpose |
|----------|----------|---------|
| Task Execution Contract | `pm-workflow:manage-tasks/standards/task-execution-contract.md` | Skill responsibilities |
| Task Contract | `pm-workflow:manage-tasks/standards/task-contract.md` | Task structure |

## Two-Tier Skill Loading

See [workflow-architecture:skill-loading](../workflow-architecture/standards/skill-loading.md) for the complete two-tier skill loading pattern with visual diagrams.

**Summary**: Agent loads Tier 1 (system skills) automatically, then Tier 2 (domain skills from `task.skills`). This workflow skill defines HOW the agent executes tests.

## Input

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `plan_id` | string | Yes | Plan identifier |
| `task_number` | number | Yes | Task number to execute |

## Output

```toon
status: success | error
plan_id: {echo}
task_number: {echo}
execution_summary:
  steps_completed: N
  steps_total: M
  files_modified: [paths]
  tests_written: N
  coverage_impact: {if available}
verification:
  passed: true | false
  command: "{cmd}"
  tests_passed: N
  tests_failed: N
next_action: task_complete | requires_attention
message: {error message if status=error}
```

## Workflow

### Step 1: Load Task Context

Read the task file to understand what tests need to be written:

```bash
python3 .plan/execute-script.py pm-workflow:manage-tasks:manage-tasks get \
  --plan-id {plan_id} \
  --task-number {task_number}
```

Extract key fields:
- `domain`: Domain for this task
- `profile`: Should be `module_testing`
- `skills`: Domain testing skills to apply (already loaded by agent)
- `description`: What tests to create
- `steps`: File paths (test files) to work on
- `verification`: How to verify tests pass
- `depends_on`: Dependencies (implementation tasks should be complete)

### Step 2: Understand Implementation Context

Before writing tests, understand what is being tested:

**Read implementation files**:
```bash
# Find the implementation being tested
# Test file: src/test/java/com/example/UserServiceTest.java
# Implementation: src/main/java/com/example/UserService.java

# Java pattern
Grep "class UserService" --type java
Read {implementation_file}

# JavaScript pattern
Glob src/**/*.{js,ts}
Read {implementation_file}
```

**Identify testable elements**:
- Public methods/functions
- Edge cases and error conditions
- Input validation
- Integration points
- Configuration behaviors

### Step 3: Plan Test Implementation

For each step (test file path), determine:
- What test scenarios to cover
- Test structure (unit vs integration)
- Mocking requirements
- Assertions needed
- Setup/teardown requirements

**Mark step as in-progress**:
```bash
python3 .plan/execute-script.py pm-workflow:manage-tasks:manage-tasks update-step \
  --plan-id {plan_id} \
  --task-number {task_number} \
  --step-number {N} \
  --status in_progress
```

### Step 4: Implement Tests

For each step (test file path):

**Create new test file**:
```bash
Write {test_file_path}
# Apply testing patterns from domain skills
# Follow AAA pattern (Arrange-Act-Assert)
# Include setup/teardown if needed
```

**Modify existing test file**:
```bash
Edit {test_file_path}
# Add new test methods
# Maintain existing test structure
# Follow project test conventions
```

**Apply testing patterns**:
- Use AAA structure (Arrange, Act, Assert)
- Follow domain testing skill patterns (JUnit 5, Jest, etc.)
- Include positive and negative test cases
- Add descriptive test names
- Include documentation for complex tests

### Step 5: Test Structure Patterns

**Unit Test Pattern**:
```
1. Setup test class/describe block
2. Create setup method (@BeforeEach, beforeEach)
3. Write test methods for each scenario:
   - Happy path tests
   - Edge case tests
   - Error/exception tests
   - Boundary tests
4. Add teardown if needed
5. Include clear assertions
```

**Integration Test Pattern**:
```
1. Setup test class with integration annotations
2. Configure test dependencies (database, services)
3. Write tests that verify component interactions
4. Include proper cleanup
5. Mark as integration test (@IT suffix, separate folder)
```

### Step 6: Mark Step Complete

After each step:
```bash
python3 .plan/execute-script.py pm-workflow:manage-tasks:manage-tasks update-step \
  --plan-id {plan_id} \
  --task-number {task_number} \
  --step-number {N} \
  --status completed
```

### Step 7: Run Verification

After all test files are written, run verification:

```bash
# Execute verification commands from task
{verification.commands[0]}
```

**Verification patterns by domain**:
- Java: `mvn test -Dtest={TestClass}` or `./gradlew test --tests {TestClass}`
- JavaScript: `npm test -- --testPathPattern={pattern}` or `npm run test:unit`
- General: Domain-specific test commands from task

### Step 8: Handle Test Results

**If all tests pass**:
```bash
python3 .plan/execute-script.py pm-workflow:manage-tasks:manage-tasks update \
  --plan-id {plan_id} \
  --task-number {task_number} \
  --status completed
```

**If tests fail**:
1. Analyze test failures
2. Determine if test logic is wrong or implementation has bug
3. If test logic issue → fix test
4. If implementation bug discovered → note in task, don't fix implementation
5. Re-run tests
6. Iterate until pass (max 3 iterations)

If still failing after 3 iterations:
```bash
python3 .plan/execute-script.py pm-workflow:manage-tasks:manage-tasks update \
  --plan-id {plan_id} \
  --task-number {task_number} \
  --status blocked \
  --notes "Tests failing after 3 attempts: {failure summary}"
```

### Step 9: Record Lessons

On issues or unexpected patterns:
```bash
python3 .plan/execute-script.py plan-marshall:manage-lessons:manage-lesson add \
  --component "pm-workflow:task-module_testing" \
  --category improvement \
  --title "{issue summary}" \
  --detail "{context and resolution}"
```

**Valid categories**: `bug`, `improvement`, `anti-pattern`

### Step 10: Return Results

```toon
status: success
plan_id: {plan_id}
task_number: {task_number}
execution_summary:
  steps_completed: {N}
  steps_total: {M}
  files_modified:
    - {test_path1}
    - {test_path2}
  tests_written: {count}
verification:
  passed: true
  command: "{test command}"
  tests_passed: {N}
  tests_failed: 0
next_action: task_complete
```

## Testing Patterns by Domain

### Java Testing (JUnit 5)

```java
@DisplayName("UserService Tests")
class UserServiceTest {

    @BeforeEach
    void setUp() {
        // Arrange - setup
    }

    @Test
    @DisplayName("should return user when valid ID provided")
    void shouldReturnUserWhenValidIdProvided() {
        // Arrange
        // Act
        // Assert
    }

    @Test
    @DisplayName("should throw exception when user not found")
    void shouldThrowExceptionWhenUserNotFound() {
        // Arrange
        // Act & Assert
        assertThrows(UserNotFoundException.class, () -> ...);
    }
}
```

### JavaScript Testing (Jest)

```javascript
describe('UserService', () => {
    beforeEach(() => {
        // Arrange - setup
    });

    it('should return user when valid ID provided', () => {
        // Arrange
        // Act
        // Assert
        expect(result).toEqual(expectedUser);
    });

    it('should throw error when user not found', () => {
        // Arrange
        // Act & Assert
        expect(() => service.getUser('invalid')).toThrow();
    });
});
```

## Test Coverage Considerations

When writing tests, consider:

| Coverage Type | Priority | When to Include |
|---------------|----------|-----------------|
| Happy path | High | Always |
| Error handling | High | Always |
| Edge cases | Medium | When logic has boundaries |
| Null/undefined | Medium | When inputs can be null |
| Integration | Low | When testing component interaction |

## Error Handling

### Implementation Not Found

If implementation to test doesn't exist:
- Check if implementation task is in dependencies
- If yes, mark task as blocked
- If no, note in lessons learned

### Flaky Tests

If tests pass/fail inconsistently:
- Add retry logic in test
- Investigate timing issues
- Consider mocking external dependencies

### Missing Dependencies

If test requires unavailable dependencies:
- Use mocks/stubs
- Document mocking approach
- Note any limitations

## Integration

**Invoked by**: `pm-workflow:task-execute-agent` (when task.profile = module_testing)

**Skill Loading**: Agent resolves this skill via `resolve-task-executor --profile module_testing`

**Script Notations** (use EXACTLY as shown):
- `pm-workflow:manage-tasks:manage-tasks` - Task operations (get, update, update-step)
- `plan-marshall:manage-lessons:manage-lesson` - Record lessons (add)

**Domain Testing Skills Applied** (loaded by agent from task.skills):
- Java: `pm-dev-java:java-core`, `pm-dev-java:junit-core`, `pm-dev-java:junit-integration`
- JavaScript: `pm-dev-frontend:cui-javascript`, `pm-dev-frontend:cui-javascript-unit-testing`, `pm-dev-frontend:cui-cypress`
- Apply patterns from whatever domain testing skills are listed in task.skills
