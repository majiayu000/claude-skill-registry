---
name: testing-philosophy
description: "Apply testing philosophy: test behavior not implementation, minimize mocks, AAA structure, coverage for confidence not percentage. Use when writing tests, reviewing test quality, discussing TDD, or evaluating test strategies."
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Testing Philosophy

Universal principles for writing effective tests. Language-agnostic—applies across testing frameworks and languages.

## Test Thinking

Before writing tests, commit to a clear approach:

- **What is the ONE behavior this test suite must verify?** If you can't answer clearly, the production code needs refactoring.
- **Behavior or implementation?** Tests should survive refactoring. If you're testing how, not what, you're coupling to implementation.
- **What failure would make you distrust this code?** Test that scenario first.

**CRITICAL**: You are capable of identifying subtle behavioral contracts that most tests miss. Don't write generic happy-path tests—find the edge cases that matter, the error handling that fails silently, the state transitions that corrupt data.

## Core Principle

**Test behavior, not implementation.**

Tests should verify what code does, not how it does it. Implementation can change; behavior should remain stable.

## Test-First Workflow (Canon TDD)

**When to TDD**:
- ✅ Core domain logic, algorithms, business rules
- ✅ Well-defined requirements
- ✅ Production code (not prototypes)
- ✅ AI-assisted development (tests guard against hallucinations)
- ❌ UI prototyping, exploration, fuzzy requirements

**Canon TDD Pattern** (Kent Beck 2024):
1. **Write test list** - enumerate all scenarios (happy, edge, error)
2. **Turn one into failing test** - focus on interface design
3. **Make it pass** - minimal implementation
4. **Refactor** - improve design while green
5. **Repeat** until list empty

**AI-Assisted TDD**:
- AI generates test list from requirements
- AI implements code to pass tests (human reviews)
- Tests are specifications in executable form
- Commit tests separately before implementation

**NEVER test**:
- Private method internals (test through public API)
- Mock call counts unless the count IS the behavior
- Internal state unless state IS the contract
- Framework code (trust the framework)

---

## What and When to Test

### Testing Boundaries

**Test at module boundaries (public API):**

**Unit Tests:**
- Pure functions (deterministic input → output)
- Isolated modules (single unit of behavior)
- Business logic (calculations, validations, transformations)

**Integration Tests:**
- Module interactions (how components work together)
- API contracts (request/response shapes)
- Workflows (multi-step processes)

**E2E Tests:**
- Critical user journeys (end-to-end flows)
- Happy path + critical errors only
- Not every feature needs E2E

### What to Test

✅ **Always test:**
- Public API (what callers depend on)
- Business logic (critical rules, calculations)
- Error handling (failure modes)
- Edge cases (boundaries, null, empty)

❌ **Don't test:**
- Private implementation details
- Third-party libraries (already tested)
- Simple getters/setters (unless they have logic)
- Framework code (trust the framework)

### TDD: Sometimes, When It Adds Value

**Use TDD for:**
- Complex logic (algorithms, business rules)
- Well-defined requirements (you know what to build)
- Critical functionality (high-risk code)

**Skip TDD for:**
- UI prototyping (exploring design)
- Exploratory work (discovering requirements)
- Simple CRUD (straightforward logic)

**When in doubt:** Write test after if TDD feels like overhead.

### Coverage Philosophy: Meaningful > Percentage

**Don't chase coverage percentages.**

✅ **Good coverage:**
- Critical paths tested (happy + error cases)
- Edge cases covered (boundary values, null, empty)
- Confidence in refactoring

❌ **Bad coverage:**
- High % but testing wrong things
- Testing implementation details
- Brittle tests that break on refactor

**Remember:** Untested code is legacy code. But 100% coverage doesn't guarantee quality.

---

## Mocking and Test Structure

### Mocking Philosophy: Minimize Mocks

**Prefer real objects when fast and deterministic.**

**When to Mock:**

**ALWAYS mock:**
- External APIs, third-party services
- Network calls
- Non-deterministic behavior (time, randomness)

**USUALLY mock:**
- Databases (or use in-memory/test DB for integration)
- File system (depends on speed needs)

**SOMETIMES mock:**
- Slow operations (if they slow tests significantly)

**NEVER mock:**
- Your own domain logic (test it directly)
- Simple data structures
- Internal collaborators (modules in your own codebase)

**Red flag:** >3 mocks in a test suggests coupling to implementation.

### Internal vs External: The Mock Boundary

**NEVER mock internal collaborators:**
- Functions/modules in your own codebase (`@/lib/*`, `./utils/*`, `../../convex/lib/*`)
- Custom hooks (`@/hooks/*`)
- Domain logic helpers

**WHY:** Mocking internal code:
- Hides integration bugs between modules
- Couples tests to implementation details
- Creates false confidence ("tests pass but prod breaks")
- Requires test updates when internals change

**INSTEAD:** Mock only at system boundaries:
- Third-party libraries (framework, SDK)
- External APIs (network calls)
- Browser/runtime APIs
- Non-deterministic sources

**Pattern:** If the mock path starts with `@/` or `../`, stop and reconsider.

### Test Structure: AAA (Arrange, Act, Assert)

**Clear three-phase structure:**

```
// Arrange: Set up test data, mocks, preconditions
setup test data
configure mocks
establish preconditions

// Act: Execute the behavior being tested
result = performAction()

// Assert: Verify expected outcome
verify result matches expectation
```

**Guidelines:**
- Visual separation between phases (blank lines)
- One logical assertion per test (can have multiple assert statements for same behavior)
- Keep Arrange simple (complex setup = simplify production code)

### Test Naming: Descriptive Sentences

**Pattern:** "should [expected behavior] when [condition]"

**Examples:**
- "should return total when all items valid"
- "should throw error when user not found"
- "calculateTotal with empty cart returns zero"
- "should retry on network failure"

**Guidelines:**
- Be specific about what's being tested
- State expected behavior clearly
- Don't use "test" prefix (redundant in test files)
- Read like documentation

---

## Test Quality and Smells

### Test Smells (Anti-Patterns)

❌ **Too many mocks** (>3 mocks)
- Indicates coupling to implementation
- Test becomes brittle, changes with internals

❌ **Brittle assertions**
- Asserting exact strings when substring would work
- Asserting exact ordering when order doesn't matter
- Over-specifying expected values

❌ **Unclear test intent**
- Can't tell what's being tested from reading test
- Vague test names
- Hidden test logic in helpers

❌ **Testing implementation details**
- Testing private methods directly
- Asserting internal state
- Mocking your own classes

❌ **Flaky tests**
- Pass/fail randomly
- Timing dependencies
- Shared mutable state between tests

❌ **Slow tests**
- Unit tests >100ms
- Integration tests >1s
- Slows development feedback loop

❌ **One giant test**
- Testing multiple behaviors in single test
- Hard to understand failures
- Breaks single responsibility for tests

❌ **Magic values**
- Unexplained constants
- Unclear test data
- No context for why values matter

### Test Quality Priorities

**Readable > DRY**

Tests are documentation. Clarity trumps reuse.

✅ **Good test practices:**
- Each test understandable in isolation
- Explicit setup visible in test
- Some duplication okay for clarity
- Descriptive variable names (even if verbose)

❌ **Over-DRY tests:**
- Extract helpers that hide test logic
- Shared setup that obscures what's being tested
- Reuse at expense of clarity

**Test length:**
- No hard limit
- Unit tests: Usually <50 lines
- Integration tests: Can be longer (setup needed)
- Long test? Ask: Testing too much? Simplify production code?

### Edge Cases: Required for Critical Paths

**Always test critical functionality:**
- Boundary values (0, 1, -1, max, min)
- Empty inputs (empty array, empty string, null)
- Error conditions (invalid input, missing data, failures)

**Ask:** "What could break? What do users depend on?"

**Opportunistic edge cases:**
- Nice-to-have features
- Non-critical paths
- When you find bugs (add regression test)

---

## Quick Reference

### Testing Decision Tree

**Should I write a test?**
1. Is this public API? → Yes, test it
2. Is this critical business logic? → Yes, test it
3. Is this error handling? → Yes, test it
4. Is this private implementation? → No, test through public API
5. Is this a framework feature? → No, trust framework
6. Will this test give confidence? → Yes, write it

**Should I use TDD?**
1. Requirements clear? → Consider TDD
2. Complex logic? → Consider TDD
3. Exploring solution? → Skip TDD, test after
4. Simple CRUD? → Skip TDD, test after

**Should I mock this?**
1. External system? → Mock it
2. Non-deterministic? → Mock it
3. My domain logic? → Don't mock, test it
4. >3 mocks already? → Refactor, too coupled

### Test Checklist

**Before writing test:**
- [ ] What behavior am I testing?
- [ ] What's the happy path?
- [ ] What edge cases matter?
- [ ] Can I test this without mocks?

**After writing test:**
- [ ] Is test name descriptive?
- [ ] Is AAA structure clear?
- [ ] Does test test behavior (not implementation)?
- [ ] Will test break only if behavior changes?
- [ ] Is test fast (<100ms for unit)?

---

## Philosophy

**"Tests are a safety net, not a security blanket."**

Good tests give confidence to refactor. Bad tests give false confidence and slow development.

**Test the contract, not the implementation:**
- Contract: What code promises to do
- Implementation: How code does it

**Tests should:**
- Verify behavior works
- Document how to use code
- Enable refactoring with confidence
- Fail only when behavior breaks

**Tests should NOT:**
- Duplicate production code
- Test framework features
- Prevent all refactoring
- Replace thinking about design

**Remember:** The goal is confidence, not coverage. Write tests that make you confident the code works, not tests that make metrics happy.
