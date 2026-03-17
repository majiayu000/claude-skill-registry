---
name: "testing-strategies"
description: "Systematic testing for confidence without over-testing — the right test at the right level"
applyTo: "**/*test*,**/*spec*,**/*.test.*,**/*.spec.*"
---

# Testing Strategies Skill

> Test the behavior, not the implementation. Test the boundaries, not the happy path.

## Testing Pyramid

| Level | Volume | Speed | Cost to Maintain | What It Catches |
| ----- | ------ | ----- | ---------------- | --------------- |
| Unit | Many (70%) | < 10ms each | Low | Logic errors, edge cases, regressions |
| Integration | Some (20%) | < 1s each | Medium | Wiring bugs, API contracts, data flow |
| E2E | Few (10%) | 5-30s each | High | User journey failures, deployment issues |

**Anti-pattern**: Inverted pyramid (too many E2E, few unit) → slow CI, flaky tests, hard to debug.
**Anti-pattern**: Ice cream cone (manual testing on top of everything) → doesn't scale.

## Unit Test Pattern (AAA)

```typescript
test('should calculate discount when order exceeds $100', () => {
    // Arrange
    const order = createOrder({ subtotal: 150, customerTier: 'gold' });
    
    // Act
    const discount = calculateDiscount(order);
    
    // Assert
    expect(discount).toBe(15); // 10% for gold tier
});
```

**Naming convention**: `should [expected behavior] when [condition]` — reads as a specification.

## Test Types Beyond the Pyramid

| Type | Purpose | When to Use | Example |
| ---- | ------- | ----------- | ------- |
| **Snapshot** | Detect unexpected output changes | UI components, serialized data | `expect(render(<Button/>)).toMatchSnapshot()` |
| **Contract** | Verify API shape between services | Microservices, public APIs | Pact, OpenAPI validation |
| **Property-based** | Find edge cases humans miss | Pure functions, parsers, serializers | `fc.assert(fc.property(fc.string(), s => decode(encode(s)) === s))` |
| **Mutation** | Verify tests actually catch bugs | Critical business logic | Stryker, pitest |
| **Performance** | Catch regressions in speed/memory | Hot paths, API endpoints | Benchmark before/after |
| **Smoke** | Verify deployment didn't break basics | Post-deploy, staging | Hit health endpoint + key pages |

## What to Mock (and What Not To)

| Mock This | Why | Don't Mock This | Why |
| --------- | --- | --------------- | --- |
| External HTTP APIs | Unreliable, slow, costly | Your own business logic | You'd be testing your mocks |
| Database in unit tests | Slow, stateful | Database in integration tests | That's the whole point |
| Time (`Date.now`) | Non-deterministic | Pure functions | Already deterministic |
| File system | Side effects | In-memory equivalents | Faster than mocking |
| Random/UUID | Non-deterministic | Framework internals | Not your responsibility |

## Coverage Philosophy

| Range | Interpretation | Action |
| ----- | -------------- | ------ |
| < 50% | Probably missing critical paths | Increase |
| 50-70% | Reasonable for most projects | Focus on changed code |
| 70-85% | Good, diminishing returns starting | Maintain, don't chase |
| 85-100% | Often wasteful unless safety-critical | Review if the effort is worth it |

**The real metric**: Coverage of *changed code* in each PR, not overall percentage.

**What coverage doesn't tell you**: That your tests assert the right things. 100% coverage with no assertions is useless.

## What NOT to Test

| Don't Test | Why | Instead |
| ---------- | --- | ------- |
| Third-party library internals | Not your code | Trust it (or pick a different library) |
| Framework behavior | Already tested upstream | Test your code that uses the framework |
| Private implementation details | Breaks on refactor | Test the public interface |
| Trivial getters/setters | No logic to break | Only if they have side effects |
| Generated code | Changes on regeneration | Test the generator, not the output |

## Test Quality Signals

| Good Test | Bad Test |
| --------- | -------- |
| Fails when behavior breaks | Fails when implementation changes |
| One clear reason to fail | Multiple assertions testing different things |
| Self-contained | Depends on other test order |
| Fast (< 100ms unit) | Slow due to unnecessary setup |
| Readable as documentation | Requires reading source to understand |
| Deterministic | Flaky (passes sometimes) |

## TDD Cycle

| Step | Action | Common Mistake |
| ---- | ------ | -------------- |
| **Red** | Write a failing test | Writing too much test (test the next small behavior) |
| **Green** | Make it pass with minimal code | Over-engineering the solution |
| **Refactor** | Clean up while green | Skipping this step (accumulates debt) |

**TDD is not always the right choice**: It works best for well-understood requirements. For exploratory code, write tests after the design stabilizes.

## Flaky Test Triage

| Pattern | Likely Cause | Fix |
| ------- | ------------ | --- |
| Fails 1 in 10 runs | Timing/race condition | Add proper waits, remove shared state |
| Fails only in CI | Environment difference | Pin versions, use containers |
| Fails after another test | Test pollution | Isolate setup/teardown |
| Fails on slow machines | Hardcoded timeouts | Use retry with backoff or event-based waits |

## Synapses

See [synapses.json](synapses.json) for connections.
