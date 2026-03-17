---
name: tdd
description: Test-driven development — write failing test first, then implement (red-green-refactor)
disable-model-invocation: true
---

Implement using TDD: $ARGUMENTS

Follow the red-green-refactor cycle strictly.

## Phase 1 — RED: Write Failing Tests

1. **Understand the requirement**: What should the feature/fix do?
2. **Choose test file**: Use the test file mapping in project config
3. **Write tests BEFORE any implementation code**:
   - Success path test — what should happen with valid input
   - Validation error test — what should happen with invalid input
   - Service/device error test — what should happen when external resource is unavailable
4. **Run tests** — they MUST fail. If tests pass without implementation, they're testing nothing.

### Test Conventions
- Class: `Test<Feature>`
- Method: `test_<action>_<expected_outcome>`
- Fixtures with proper type hints and cleanup
- Test HTTP client configured for proper error testing (no automatic error propagation)
- Audit log tests with log capture mechanism (see stack concepts) on the project's audit logger

## Phase 2 — GREEN: Minimal Implementation

1. **Write the minimum code to make tests pass** — nothing more
2. Follow project standards:
   - Future annotations pattern (see stack concepts)
   - Typed exceptions from the exception hierarchy
   - Thread safety in service layer
   - Typed schemas for API shapes (see stack concepts)
   - Thin route handlers with DI injection (see stack concepts)
3. **Run tests** — they MUST now pass

## Phase 3 — REFACTOR: Clean Up

1. Remove duplication
2. Improve naming
3. Extract helpers if three or more similar patterns exist
4. Ensure layer boundaries are respected
5. **Run full suite** — nothing must break. Run test and type-check commands (see project config).

## Phase 4 — Complete

1. Verify audit logging if state changes were added
2. Update OpenAPI metadata (summary, description, responses)
3. Update project documentation if new endpoints or config were added
4. Run final verification with the test and type-check commands