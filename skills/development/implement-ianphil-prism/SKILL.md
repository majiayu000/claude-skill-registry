---
name: implement
description: This skill should be used when the user asks to "implement phase N", "implement task T001", "do TDD for phase", "implement T001-T009", or wants to execute tasks following strict TDD red-green-refactor workflow.
---

# Implement

## User Input

PHASE_OR_TASK = $ARGUMENT

Accept and use user input (ARGUMENT). Valid formats:
- A phase name (e.g., "Phase 1", "US1", "Phase 3")
- A specific task ID (e.g., "T001", "T017-T028")
- A task range (e.g., "T001-T009")

## Context Loading

1. Identify the current feature ID from the git branch (e.g., `feature/001-mcp-integration` → `001-mcp-integration`)
2. Find the feature folder: check `backlog/plans/{feature-id}/` first, then `backlog/plans/_completed/{feature-id}/`
3. Read `{feature-path}/tasks.md` to get task list
4. Read `specs/tests/{feature-id}.md` if it exists

## Phase Execution

If the input is a phase name:

### Phase Entry: Spec Tests (RED)
- Find the phase's entry spec test task (e.g., "T016 [SPEC] Run spec tests for FR-3...")
- Run the spec tests specified in that task
- **Expected**: ALL FAIL (requirements not yet implemented)
- If any pass unexpectedly, report and ask user to verify

### Task Execution Loop
- For each task in the phase:
  1. **[TEST] tasks**: Write failing tests first
     - Run tests: `cargo test {module} --lib` → expect FAIL (RED)
  2. **[IMPL] tasks**: Implement minimal code to pass tests
     - Run tests: `cargo test {module} --lib` → expect PASS (GREEN)
  3. **[SPEC] tasks**: Skip during main loop (handled at phase boundaries)
  4. Mark task as completed in `tasks.md` (check the box)
  5. Run `make lint` to ensure code quality
  6. Commit after each logical group of tasks (2-3 tasks)

### Phase Exit: Spec Tests (GREEN)
- Find the phase's exit spec test task (e.g., "T029 [SPEC] Run spec tests for FR-3...")
- Run the spec tests specified in that task
- **Expected**: ALL PASS (requirements satisfied)
- If any fail, identify which implementation tasks need revision

## Task-Specific Execution

If the input is a task ID or range:

1. Read the task description from `tasks.md`
2. Check dependencies (if task has prerequisites, verify they're completed)
3. Execute based on task type:
   - **[TEST]**: Write tests, run them → expect FAIL
   - **[IMPL]**: Implement code, run tests → expect PASS
   - **[SPEC]**: Run spec tests as specified in task description
4. Mark task as completed in `tasks.md`
5. Run `make check && make lint` to verify

## TDD Rules

For Rust code, strictly follow Red-Green-Refactor:
1. **RED**: Write failing test first → run `cargo test` → see failure
2. **GREEN**: Write minimal code to pass → run `cargo test` → see pass
3. **REFACTOR**: Clean up code → run `cargo test` → keep passing

For bash/scripts, implement directly without TDD.

## Extensive Mocking Detection

**STOP and ask the user** when a [TEST] task would require:

- Mocking an entire external system (MCP server, database, HTTP server)
- Creating complex fake implementations with multiple methods/traits
- Spawning actual processes or network connections in unit tests
- More than 50 lines of mock/stub code to test a single function

**Signs you're over-mocking:**
- The mock is as complex as the real implementation
- Simulating protocol handshakes or connection lifecycle is required
- Tests require async runtime setup for fake services
- Mock state management becomes a testing problem itself

**When detected, ask the user:**

```
⚠️ Task {TASK_ID} requires extensive mocking to unit test.

The test would need to mock: {what needs mocking}

Options:
1. **Defer to integration test** - Implement first, test with real/echo server later
2. **Simplify test scope** - Test only pure functions, defer interaction tests
3. **Proceed with mocking** - Accept complexity, write the mock

Which approach do you prefer?
```

**Typical resolution:**
- Change [TEST] task to [INTEG] and move to integration phase
- Implement the code first, then write integration tests with real servers
- Update tasks.md to reflect the change

## Verification

Before marking phase complete:
- [ ] All unit tests pass: `make test-{module}`
- [ ] All spec tests pass: `python specs/tests/run_tests_claude.py specs/tests/{feature-id}.md`
- [ ] Linting passes: `make lint`
- [ ] Build succeeds: `make build`

## Finally (REQUIRED)

After implementation is complete, follow in this order:

1. **Run `/progress`** to generate session log in `.ai/YYYY-MM-DD/`
2. **Run `/commit`** to commit any remaining changes
3. Close GitHub issue if specified

This step is **mandatory** - do not skip the progress log.

## Example Usage

```bash
/implement "Phase 1"           # Implement entire Phase 1 (Setup)
/implement "US1"               # Implement User Story 1 phase
/implement "T001"              # Implement single task
/implement "T017-T028"         # Implement task range
```
