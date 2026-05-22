---
name: test-driven-development
description: Core TDD philosophy and testing principles. Use when writing tests interactively or need testing guidance. Emphasizes tests as contracts, mock boundaries not internals, and implementation fixes over test changes.
---

# Test-Driven Development

**For system-level design principles and architectural boundaries, see the `software-engineer` skill.**

## Core Philosophy

<core_philosophy>
**Foundation**: TDD is an application of contract-based design. Tests define the contract an implementation must fulfill—they are specifications, not afterthoughts. This connects directly to the abstraction principles in the `software-engineer` skill.

**Tests = Contracts**: Tests represent business requirements and expected behavior. They are contracts the implementation must fulfill. Never compromise test integrity to achieve green tests.

**Tests are source of truth**: When tests fail, fix the implementation. Only change tests when requirements change or test has a verified bug.
</core_philosophy>

## Testing Approach

### Architectural Boundaries and Mocking Strategy

<architectural_boundaries>
**Identify architectural boundaries** in your system:
- Layer boundaries (e.g., data layer, service layer, presentation layer)
- Module boundaries (e.g., namespaces, packages, crates)
- Process boundaries (e.g., Erlang processes, Elixir GenServers)
- External system boundaries (e.g., APIs, databases, third-party services)
</architectural_boundaries>

<unit_definition>
**What constitutes a "unit":**

A "unit" is a cohesive component at an architectural boundary:
- Classes (e.g., Java, Python, Swift)
- Namespaces with related functions (e.g., Clojure, Haskell)
- Modules with related predicates (e.g., Prolog)
- Processes/GenServers (e.g., Erlang, Elixir)
- Modules with traits/protocols (e.g., Rust, Swift)
</unit_definition>

<mocking_rules>
**When to mock:**
- Mock dependencies **across** architectural boundaries
- External dependencies injected/passed into system under test get mocked

**When NOT to mock:**
- Don't mock the system under test itself
- Don't mock **within** a cohesive unit (e.g., private methods, internal helpers)
- If tempted to mock internals, that's a design smell — refactor instead
</mocking_rules>

<test_balance>
**Balance unit and integration tests:**
- **Unit tests**: Test each component in isolation with mocked dependencies across boundaries
- **Integration tests**: Test behavior across boundaries with real implementations
- Both are necessary — unit tests verify component logic, integration tests verify system behavior
- Over-mocked tests validate mocks, not real behavior
</test_balance>

<example>
**Layered data store (hexagonal architecture):**

```
┌───────────────────────────────────────────────────────┐
│                   Application Core                    │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐  │
│  │   Domain    │   │   Service   │   │   Use Case  │  │
│  │   Models    │   │   Layer     │   │   Layer     │  │
│  └─────────────┘   └─────────────┘   └─────────────┘  │
│                                                       │
├───────────────────────BOUNDARY────────────────────────┤
│                                                       │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐  │
│  │  Database   │   │   External  │   │   HTTP      │  │
│  │  Adapter    │   │   API       │   │   Client    │  │
│  └─────────────┘   └─────────────┘   └─────────────┘  │
└───────────────────────────────────────────────────────┘
```

- **Unit tests**: Test domain models and service layer with mocked adapters
- **Integration tests**: Test adapters with real external systems (DB, APIs)
- **Contract tests**: Verify adapters fulfill the port interface
- External database gets mocked at adapter boundary, not inside services
</example>

### Test Doubles Taxonomy

<test_doubles>
**Understanding test double types** aids in communicating test intent. This taxonomy was formalized by Gerard Meszaros in *xUnit Test Patterns* (2007):[^1]

| Type | Purpose | When to Use |
|------|---------|-------------|
| **Stub** | Returns predetermined values | When behavior doesn't affect test outcome |
| **Mock** | Verifies interactions occurred | When the interaction IS the behavior being tested |
| **Fake** | Working implementation (simplified) | When real implementation too slow/complex |
| **Spy** | Records calls for later verification | When need to verify after execution |

**Key insight**: Overuse of mocks often indicates testing implementation rather than behavior. Prefer stubs when possible; use mocks when interactions are the contract.

[^1]: Gerard Meszaros. 2007. *xUnit Test Patterns: Refactoring Test Code*. Addison-Wesley.
</test_doubles>

### Test Design Process

<design_steps>
**When designing tests:**
1. Identify architectural boundaries in the system
2. Determine what constitutes a "unit" (component, layer, module)
3. Plan unit tests for each unit with dependencies mocked at boundaries
4. Plan integration tests crossing boundaries with real implementations
5. Ensure tests verify usage/requirements, not implementation details
</design_steps>

<failure_response>
**When test fails:**
1. Read test to understand expected behavior
2. Debug implementation to find why it doesn't meet expectations
3. Fix implementation, never "fix" test to pass
</failure_response>

<quality_criteria>
**Test quality requirements:**
- Descriptive names explaining the requirement being checked
- Readable as documentation of system behavior
- Plan test cases based on usage, not implementation details
- Include comprehensive documentation (e.g., Javadoc for JUnit, Sphinx for Python) explaining what test ensures and special considerations
- Tests can have bugs or enforce wrong behaviors—always assess correctness
</quality_criteria>

## Test-Driven Development Workflow

<tdd_cycle>
1. **Write failing tests FIRST** based on requirements (including desired usage patterns)
   - Thoroughly document planned tests to guide implementation
   - Stub planned tests with exceptions: `throw new IllegalStateException("Not implemented yet!")`
2. **Implementation makes existing tests pass** without test modification
3. **Tests are source of truth** — never change tests to match broken code
4. **When debugging:**
   - Understand why test is failing
   - Fix implementation to match test expectations
   - Only modify tests if requirements changed or test has VERIFIED bug
5. **Treat test failures as implementation bugs**, not test bugs
   - Test bugs exist, but assume only after verifying implementation is correct
</tdd_cycle>

<debugging_tip>
**Debug and trace logging**: Effective way to probe program function during test execution.
</debugging_tip>

## Critical Anti-Patterns

<anti_patterns>
**Never:**
- Mock the system under test itself (the component being tested)
- Mock within a cohesive unit (e.g., private methods, internal helpers of the unit under test)
- Change test assertions to match current behavior
- Write tests that mirror implementation rather than requirements
- Over-mock to the point tests don't validate real behavior
- Write tests that don't exercise code in module being tested (e.g., calculating result in test instead of using module-under-test)
- Mock to make tests pass — fix implementation instead
</anti_patterns>

<design_smell>
**If tempted to mock internals of the unit under test**: That's a design smell — refactor the code instead.
</design_smell>

## Framework-Specific Guidance

**See language-specific skills** for testing framework details:
- **java-programmer**: JUnit, Mockito, assertion patterns
- **python-programmer**: pytest, unittest, mocking strategies
- **clojure-programmer**: clojure.test, test.check
- **racket-programmer**: RackUnit, testing patterns

General principles across frameworks:
- Use framework's assertion methods instead of custom comparison logic
- Include descriptive assertion messages explaining business/technical reasons
- Organize tests into logical categories/suites
- Maintain consistent assertion styles within codebase

## Planning and Scaffolding

<scaffolding_steps>
**Before implementing:**
- Create interfaces, type signatures, abstract classes, and other definitional structures
- Create empty functions with step-by-step comments: "1. Setup data.", "2. Process data.", etc.
- Write tests after defining but NOT implementing code structures to create example API uses
- Examine example code for potential usage problems requiring scaffold refactoring
</scaffolding_steps>

<maintainability_principles>
**Maintainability:**
- Assume code maintained by junior engineers and other LLMs
- Prefer strongly defined structures based on idiomatic patterns for the language
- If uncertain, ask — user is senior engineer with answers or resources
</maintainability_principles>

## Common Mistakes

<common_mistakes>
### Mechanical Mistakes
- Planning tests based on implementation instead of usage/requirements
- Creating tests that over-fit to specific implementation
- Removing existing documentation or comments (rephrase for consistency instead)
- Not documenting tests (every test needs comprehensive documentation)
- Using inconsistent assertion/verification styles across tests
- Not explaining business/technical reasons in assertion messages

### Judgment Mistakes (Staff-Level Insights)
- **Confusing "tests first" with "tests drive design"**: TDD is about using tests to discover design, not just writing tests before code
- **Treating coverage metrics as quality proxies**: 100% coverage with bad tests is worse than 70% coverage with good tests
- **Not recognizing test difficulty as design feedback**: If a unit is hard to test, the design is likely wrong—don't fight to mock, refactor instead
- **Writing tests that specify implementation sequence**: Tests should specify WHAT behavior occurs, not HOW or in what order
- **Testing internal state rather than observable behavior**: Tests should verify outputs and side effects, not implementation details
- **Over-mocking to achieve isolation**: If everything is mocked, the test validates mocks, not system behavior
</common_mistakes>

## Resources

<resources>
**Primary References:**
- Martin Fowler's testing articles: https://martinfowler.com/testing/
- Kent Beck's "Test-Driven Development: By Example" concepts
- Gerard Meszaros' test doubles taxonomy (xUnit Test Patterns)

**Key Principles:**
- Test Pyramid concept (Mike Cohn, 2009): more unit tests, fewer integration tests, even fewer E2E
- Arrange-Act-Assert pattern (Bill Wake, 2001) for test structure
- Given-When-Then (Dan North and Chris Matts, ~2006) for behavior specification

**See also:** Language-specific skills for framework-specific testing patterns (JUnit, pytest, clojure.test, RackUnit, PlUnit).
</resources>
