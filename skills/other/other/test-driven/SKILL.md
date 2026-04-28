---
name: test-driven
description: Test-Driven Development (TDD) - design tests from requirements, then execute RED -> GREEN -> REFACTOR cycle. Use when implementing features or fixes with TDD methodology, writing tests before code, or following XP-style development across any supported language.
---

# Test-driven development (XP-style)

Tests define the specification. Design them from requirements before any implementation. The RED-GREEN-REFACTOR cycle is the heartbeat: write a failing test, make it pass with minimal code, then clean up while green.

**Modern insight (2025)**: TDD + property-based testing pairing is the standard -- example tests prevent regressions, property tests discover edge cases. TDD also serves AI-assisted development: structural integrity keeps code understandable for both human and AI collaborators (Kent Beck, "Augmented Coding"). Mutation testing validates test quality beyond coverage metrics (TDD+Mutation: 63.3% vs TDD-alone: 39.4% mutation coverage).

See [frameworks](references/frameworks.md) for language-specific test runners, property testing, coverage, and mutation tools.
See [examples](references/examples.md) for brief TDD cycle patterns per language.

---

## When to Apply

- New features with clear requirements (both inside-out and outside-in approaches valid)
- Bug fixes -- write a failing test that proves the bug before fixing
- Refactoring -- ensure coverage exists before restructuring
- API contract enforcement -- test the interface, not internals
- Property-based invariants -- complement example tests with PBT
- Legacy code -- add characterization tests before modifying (Michael Feathers pattern)

## When NOT to Apply

- Exploratory prototyping or spike research
- One-off scripts, data migrations, generated code
- Purely visual UI layout work (prefer visual regression testing)
- Highly experimental algorithmic research (but PBT still helps)
- Throwaway code with <1 week lifespan

---

## Anti-patterns

- **Test-last**: Writing tests after implementation defeats the design benefit
- **Testing implementation details**: Tests should verify behavior, not internal structure -- breaks refactoring confidence
- **Over-mocking**: Testing the mocks instead of the code; mock external I/O, not core logic
- **Skipping RED**: Tests that never fail aren't tests -- they verify nothing
- **100% coverage obsession**: Coverage does not equal quality. Mutation testing exposes gaps coverage cannot
- **Refactoring on RED**: Never restructure with failing tests
- **Test-induced architectural damage**: Letting mock boundaries dictate design
- **Snapshot bloat**: Approval-style tests without curation become maintenance burden

---

## Two Schools (decision guidance, not prescription)

- **Inside-Out (Classic/Detroit)**: Start with unit tests for smallest pieces, build upward. Minimizes mocks. Best for well-understood domains, algorithms, utility functions.
- **Outside-In (London/Mockist)**: Start with acceptance test for user-facing behavior, use mocks to discover interfaces. Best for layered systems, APIs, microservices.
- **Pragmatic teams use both depending on context.** Neither is superior.

## Test Doubles Hierarchy

- **Stubs**: Return predefined data; verify outcomes (state-based)
- **Mocks**: Verify interactions/calls were made (behavior-based)
- **Fakes**: Working implementations (e.g., in-memory database)
- **Spies**: Record calls while using real behavior
- **Rule**: Mock external dependencies. Never mock core domain logic.

---

## Workflow (language-neutral)

1. **CREATE** -- Write failing tests: error cases -> edge cases -> happy paths -> property tests
2. **RED** -- Run tests, verify all fail. If any pass, the test is wrong or behavior already exists.
3. **GREEN** -- Minimal code to pass. No extras, no optimization, no cleanup.
4. **REFACTOR** -- Clean up while green. Separate structural changes from behavioral (Tidy First). Re-run tests after every change.

---

## Constitutional Rules (Non-Negotiable)

1. **Design Tests First**: Plan all test cases from requirements before implementation; write each test iteratively in the RED-GREEN-REFACTOR loop
2. **RED Before GREEN**: Each new test MUST fail before you write implementation for it
3. **Error Cases First**: Implement error handling before success paths
4. **One Test at a Time**: Write one failing test, make it pass, refactor, then add the next test
5. **Refactor Only on GREEN**: Never refactor with failing tests

## Validation Gates

| Gate | Pass Criteria | Blocking |
|------|---------------|----------|
| Tests Created | Test files exist for target module | Yes |
| RED State | All new tests fail before implementation | Yes |
| GREEN State | All tests pass after implementation | Yes |
| Coverage | >= 80% line coverage | No |
| Mutation | Mutation score reviewed (no threshold enforced) | No |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | TDD cycle complete, all tests pass |
| 11 | No test framework detected |
| 12 | Test compilation failed |
| 13 | Tests not failing (RED state invalid) |
| 14 | Tests fail after implementation (GREEN not achieved) |
| 15 | Tests fail after refactor (regression) |

---

## Reference materials (mattpocock/skills tdd fold-in)

- `references/mocking.md` — when to mock vs use real implementations; trade-offs.
- `references/interface-design.md` — interface shape and depth in TDD context.
- `references/refactoring.md` — refactor step discipline post-green.
- `references/deep-modules.md` — Ousterhout's deep-module heuristic applied to TDD.
- `references/tests.md` — what counts as a real-bug test vs ceremony.

These reference docs are MIT-licensed (see `/home/alpha/.claude/claude/skills/LICENSES.md` for full attribution).
