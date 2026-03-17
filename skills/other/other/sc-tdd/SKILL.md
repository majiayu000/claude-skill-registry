---
name: sc-tdd
description: Strict Test-Driven Development enforcer with Red-Green-Refactor workflow automation. Auto-detects frameworks, validates semantic test failures, and blocks production code until tests fail properly. Use for feature development, bug fixes with test coverage, or refactoring with safety nets.
---

# Test-Driven Development (TDD) Skill

**Strict Red-Green-Refactor workflow enforcement with automated validation.**

This skill acts as a TDD workflow state machine that enforces discipline through validators. It prevents common TDD anti-patterns and ensures proper test-first development.

## Quick Start

```bash
# Start TDD for a new feature
/sc:tdd "add user password validation"

# TDD with specific framework
/sc:tdd payment-module --framework pytest

# Fast mode (skip full suite after green, run at end)
/sc:tdd api-endpoint --fast

# Allow snapshot tests
/sc:tdd ui-component --allow-snapshots
```

## Behavioral Flow

This skill enforces a **7-step Red-Green-Refactor cycle**:

1. **Initialize** - Detect scope, framework, create state
2. **RED: Write Failing Test** - Create test for missing functionality
3. **RED: Validate Failure** - Run validator, confirm SEMANTIC failure (assertion, not compile error)
4. **GREEN: Implement Minimally** - Write smallest code to pass test
5. **GREEN: Validate Passing** - Run validators, confirm test passes + no regressions
6. **REFACTOR: Improve Design** - Clean up with tests as safety net
7. **REFACTOR: Validate Stability** - Re-run suite, confirm still green

## State Machine

```
IDLE → RED_PENDING → RED_CONFIRMED → GREEN_PENDING →
GREEN_CONFIRMED → REFACTOR_PENDING → REFACTOR_COMPLETE → [cycle repeats]
```

**Critical Rules:**
- **Validator output is source of truth** - If validator says blocked, you MUST stop
- **Exit codes matter**: 0 = allowed, 2 = blocked, 3 = error (ask user for help)
- **No bypassing** - Every phase transition requires validator approval

## Phase 1: Initialize (IDLE → RED_PENDING)

**When**: User requests TDD workflow

**Your Actions**:
1. Detect scope root:
```bash
python .claude/skills/sc-tdd/scripts/framework_detector.py \
  --detect-scope $(pwd) \
  --json
```

2. Initialize state:
```bash
python .claude/skills/sc-tdd/scripts/tdd_state_machine.py \
  --scope-root <detected_scope> \
  --init \
  --json
```

3. Transition to RED_PENDING:
```bash
python .claude/skills/sc-tdd/scripts/tdd_state_machine.py \
  --scope-root <scope> \
  --phase RED_PENDING \
  --evidence "User requested: <feature_description>" \
  --json
```

**Output**: Confirm initialization, explain RED phase rules to user

## Phase 2: Write Failing Test (RED_PENDING)

**Rules**:
- User writes test first
- You MAY help write the test
- You MAY add empty stubs/interfaces to make test compile (e.g., `pass`, `raise NotImplementedError`, empty functions)
- You MUST NOT write production implementation yet

**Your Actions**:
1. Help user write test file
2. Explain test must fail with **assertion** (not compile error)
3. When test is written, proceed to validation

## Phase 3: Validate Red (RED_PENDING → RED_CONFIRMED)

**CRITICAL**: You MUST run this validator before proceeding.

**Command**:
```bash
python .claude/skills/sc-tdd/scripts/validate_red.py \
  --scope-root <scope> \
  --json
```

**Interpretation**:
- **Exit code 0** + **`"allowed": true`** → Proceed to RED_CONFIRMED
- **Exit code 2** + **`"allowed": false`** → STOP, show user `reasons`, ask them to fix

**Common Blocking Reasons**:
- `"Test failed but NOT with semantic assertion"` - Compile error, need to fix test
- `"Test PASSED (expected failure)"` - Test not actually testing the feature
- `"No changed test files found"` - Forgot to write test

**If Blocked**: Show user the `reasons` array, `artifacts.test_output`, and ask them to address the issue. **DO NOT** propose production code until validator allows.

**If Allowed**: Store `artifacts.intent_test` information, transition state, proceed to GREEN phase.

## Phase 4: Implement Minimally (RED_CONFIRMED → GREEN_PENDING)

**Rules**:
- Write MINIMAL implementation to pass the test
- Focus on making test pass, not perfection
- NO premature optimization
- NO extra features beyond test requirements

**Your Actions**:
1. Confirm current state is RED_CONFIRMED
2. Implement minimal production code
3. Explain your implementation approach
4. Transition to GREEN_PENDING:
```bash
python .claude/skills/sc-tdd/scripts/tdd_state_machine.py \
  --scope-root <scope> \
  --phase GREEN_PENDING \
  --evidence "Implemented: <description>" \
  --json
```
5. Proceed to validation

## Phase 5: Validate Green (GREEN_PENDING → GREEN_CONFIRMED)

**CRITICAL**: You MUST run this validator before claiming success.

**Command** (standard):
```bash
python .claude/skills/sc-tdd/scripts/validate_green.py \
  --scope-root <scope> \
  --json
```

**Command** (fast mode, skips full suite):
```bash
python .claude/skills/sc-tdd/scripts/validate_green.py \
  --scope-root <scope> \
  --skip-full-suite \
  --json
```

**Interpretation**:
- **Exit code 0** + **`"allowed": true`** → GREEN_CONFIRMED, proceed to refactor
- **Exit code 2** + **`"allowed": false`** → STOP, implementation insufficient

**Common Blocking Reasons**:
- `"Intent test still FAILING"` - Implementation didn't make test pass
- `"Full test suite FAILED - REGRESSION DETECTED"` - Broke existing tests

**If Blocked**: Show user the failure details, fix implementation, re-validate.

**If Allowed**: Celebrate! Test passes, no regressions. Ask user if they want to refactor or complete cycle.

## Phase 6: Refactor (Optional, GREEN_CONFIRMED → REFACTOR_PENDING)

**Rules**:
- Improve code quality WITHOUT changing behavior
- Tests must continue passing
- Allowed changes: extract methods, rename variables, improve clarity, remove duplication
- NOT allowed: add features, change test expectations, weaken tests

**Your Actions**:
1. Ask user if they want to refactor
2. If yes, transition to REFACTOR_PENDING
3. Propose refactorings
4. Apply changes
5. Re-run tests to confirm stability

## Phase 7: Validate Refactor (REFACTOR_PENDING → REFACTOR_COMPLETE)

**Command**:
```bash
python .claude/skills/sc-tdd/scripts/validate_green.py \
  --scope-root <scope> \
  --json
```

(Same validator, ensures tests still pass)

**If Allowed**: Cycle complete! Ask user:
- Continue with next test? (start new RED cycle)
- Feature complete?

## Flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--framework` | string | auto | Test framework: auto, pytest, jest, vitest, go, cargo |
| `--fast` | bool | false | Skip full suite in GREEN, run only at feature completion |
| `--allow-snapshots` | bool | false | Allow snapshot tests as semantic failures |
| `--strict` | bool | false | No stubs allowed in RED (must be pure test-first) |

## Personas Activated

- **agent-test-automator** - Test design expertise
- **agent-quality-engineer** - Test quality validation
- **agent-python-pro** / **agent-typescript-expert** - Language-specific implementation
- **agent-backend-architect** / **agent-frontend-architect** - Architecture guidance

## MCP Integration

- **PAL MCP**
  - `mcp__pal__codereview` - Review test quality and implementation
  - `mcp__pal__debug` - Investigate unexpected test failures

## Anti-Patterns Detected & Blocked

**Blocked by validators:**
- Production code before failing test
- Compile errors counted as "red" (must be runtime assertion)
- Test passing when it should fail
- Weakened assertions during GREEN phase
- Regressions in full suite

**Warned by validators:**
- Snapshot tests (blocked unless --allow-snapshots)
- Flaky patterns: sleep, network, random without mocking
- Assertionless tests
- Tests that always pass

## Tool Coordination

- **Read** - Read existing test files, implementation code, framework configs
- **Write** - Create new test files, state files
- **Edit** - Modify tests and implementation incrementally
- **Bash** - Execute validator scripts (NON-NEGOTIABLE, always run validators)
- **Glob** - Find test files, manifest files, CI configs
- **Grep** - Search for test patterns, framework usage

## Quality Dimensions

Evaluated on:
- **Correctness** (30%) - Tests pass, implementation works as specified
- **Completeness** (20%) - All test scenarios covered, edge cases handled
- **Testability** (20%) - Tests are clear, maintainable, fast, deterministic
- **Maintainability** (15%) - Code is clean, well-structured, no duplication
- **Discipline** (15%) - Followed TDD process, no shortcuts, proper Red-Green-Refactor

**Threshold**: 70+ score required to mark feature complete

## Examples

### Example 1: Feature Development

```bash
/sc:tdd "add password validation: minimum 8 characters"

# Workflow enforced:
# 1. Initialize state for current directory scope
# 2. User/Claude writes test_password_validation.py:
#    def test_password_min_length():
#        assert validate_password("short") == False
#        assert validate_password("longenough") == True
# 3. Run validate_red.py → confirms test FAILS with AssertionError (no validate_password function)
# 4. Claude implements:
#    def validate_password(password: str) -> bool:
#        return len(password) >= 8
# 5. Run validate_green.py → confirms test PASSES, full suite GREEN
# 6. Ask user about refactoring
# 7. Feature complete or next cycle
```

### Example 2: Bug Fix with TDD

```bash
/sc:tdd "fix: user deletion doesn't cascade to posts" --framework pytest

# Workflow:
# 1. Write test exposing bug (test fails showing cascade doesn't work)
# 2. Validate RED (confirms bug exists)
# 3. Fix cascade behavior
# 4. Validate GREEN (confirms bug fixed, no regressions)
```

### Example 3: Monorepo Package

```bash
cd backend/user-service
/sc:tdd "add email validation"

# Auto-detects:
# - scope_root: backend/user-service (nearest package.json)
# - framework: jest (from package.json devDependencies)
# - Runs tests only in this package scope
```

## Troubleshooting

### "No testing framework detected"
**Solution**:
1. Check if test framework is installed
2. Specify manually: `--framework pytest`
3. Ensure framework config exists (pytest.ini, jest.config.js, etc.)

### "Test failed but NOT with semantic assertion"
**Cause**: Compile error, import error, syntax error

**Solution**:
1. Fix test to compile and run
2. Add empty stub if needed: `def my_function(): raise NotImplementedError`
3. Re-run validate_red.py

### "Full test suite timed out"
**Solution**:
1. Use `--fast` mode for faster cycles
2. Run full suite only at feature completion
3. Investigate slow tests

### "Multiple test files changed"
**Cause**: More than one test file modified (TDD requires focus)

**Solution**:
1. Commit/stash other changes
2. Work on one test at a time
3. Use multiple micro-cycles

## State Recovery

If state file is lost or corrupted:
1. Validator will attempt recovery from git diff + current test results
2. You can manually re-initialize: `python tdd_state_machine.py --init --scope-root <path>`
3. State is per-scope, so multiple packages can have independent TDD states

## Important Reminders

1. **ALWAYS run validators before phase transitions** - This is non-negotiable
2. **Trust validator output over assumptions** - If validator says blocked, stop
3. **Exit codes matter**: Check both exit code AND `"allowed"` field in JSON
4. **One test at a time** - TDD is about smallest increments
5. **Semantic failures only** - Compile errors don't count as proper "red"
6. **Full suite matters** - Don't skip unless using --fast mode explicitly

---

**Version**: 1.0.0
**Last Updated**: 2025-01-09
**Maintainer**: SuperClaude Framework
