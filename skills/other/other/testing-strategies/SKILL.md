---
name: testing-strategies
description: Strategic guidance for choosing and implementing testing approaches across the test pyramid. Use when building comprehensive test suites that balance unit, integration, E2E, and contract testing for optimal speed and confidence. Covers multi-language patterns (TypeScript, Python, Go, Rust) and modern best practices including property-based testing, test data management, and CI/CD integration.
---

# Testing Strategies

Build comprehensive, effective test suites by strategically selecting and implementing the right testing approaches across unit, integration, E2E, and contract testing levels.

## Purpose

This skill provides strategic frameworks for:
- **Test Type Selection**: Determine when to use unit vs. integration vs. E2E vs. contract testing
- **Test Pyramid Balancing**: Optimize test distribution for fast feedback and reliable coverage
- **Multi-Language Implementation**: Apply consistent testing patterns across TypeScript, Python, Go, and Rust
- **Test Data Management**: Choose appropriate strategies (fixtures, factories, property-based testing)
- **CI/CD Integration**: Integrate tests into automated pipelines with optimal execution patterns

Testing is foundational to reliable software. With microservices architectures and continuous delivery becoming standard in 2025, strategic testing across multiple levels is more critical than ever.

## When to Use This Skill

Invoke this skill when:
- Building a new feature that requires test coverage
- Designing a testing strategy for a new project
- Refactoring existing tests to improve speed or reliability
- Setting up CI/CD pipelines with testing stages
- Choosing between unit, integration, or E2E testing approaches
- Implementing contract testing for microservices
- Managing test data with fixtures, factories, or property-based testing

## The Testing Pyramid Framework

### Core Concept

The testing pyramid guides test distribution for optimal speed and confidence:

```
         /\
        /  \  E2E Tests (10%)
       /----\  - Slow but comprehensive
      /      \  - Full stack validation
     /--------\
    /          \  Integration Tests (20-30%)
   /            \  - Moderate speed
  /--------------\  - Component interactions
 /                \
/------------------\  Unit Tests (60-70%)
                      - Fast feedback
                      - Isolated units
```

**Key Principle**: More unit tests (fast, isolated), fewer E2E tests (slow, comprehensive). Integration tests bridge the gap.

### Modern Adaptations (2025)

**Microservices Adjustment**:
- Add contract testing layer between unit and integration
- Increase integration/contract tests to 30% (validate service boundaries)
- Reduce E2E tests to critical user journeys only

**Cloud-Native Patterns**:
- Use containers for integration tests (ephemeral databases, test services)
- Parallel execution for fast CI/CD feedback
- Risk-based test prioritization (focus on high-impact areas)

For detailed pyramid guidance, see `references/testing-pyramid.md`.

## Universal Testing Decision Tree

### Which Test Type Should I Use?

```
START: Need to test [feature]

Q1: Does this involve multiple systems/services?
  ├─ YES → Q2
  └─ NO  → Q3

Q2: Is this a critical user-facing workflow?
  ├─ YES → E2E Test (complete user journey)
  └─ NO  → Integration or Contract Test

Q3: Does this interact with external dependencies (DB, API, filesystem)?
  ├─ YES → Integration Test (real DB, mocked API)
  └─ NO  → Q4

Q4: Is this pure business logic or a pure function?
  ├─ YES → Unit Test (fast, isolated)
  └─ NO  → Component or Integration Test
```

### Test Type Selection Examples

| Feature | Test Type | Rationale |
|---------|-----------|-----------|
| `calculateTotal(items)` | Unit | Pure function, no dependencies |
| `POST /api/users` endpoint | Integration | Tests API + database interaction |
| User registration flow (form → API → redirect) | E2E | Critical user journey, full stack |
| Microservice A → B communication | Contract | Service interface validation |
| `formatCurrency(amount, locale)` | Unit + Property | Pure logic, many edge cases |
| Form validation logic | Unit | Isolated business rules |
| File upload to S3 | Integration | External service interaction |

For comprehensive decision frameworks, see `references/decision-tree.md`.

## Testing Levels in Detail

### Unit Testing (Foundation - 60-70%)

**Purpose**: Validate small, isolated units of code (functions, methods, components)

**Characteristics**:
- Fast (milliseconds per test)
- Isolated (no external dependencies)
- Deterministic (same input = same output)
- Broad coverage (many tests, small scope each)

**When to Use**:
- Pure functions (input → output)
- Business logic and algorithms
- Utility functions
- Component rendering (without integration)
- Validation logic

**Recommended Tools**:
- **TypeScript/JavaScript**: Vitest (primary, 10x faster than Jest), Jest (legacy)
- **Python**: pytest (industry standard)
- **Go**: testing package (stdlib) + testify (assertions)
- **Rust**: cargo test (stdlib)

For detailed patterns, see `references/unit-testing-patterns.md`.

### Integration Testing (Middle Layer - 20-30%)

**Purpose**: Validate interactions between components, modules, or services

**Characteristics**:
- Moderate speed (seconds per test)
- Partial integration (real database, mocked external APIs)
- Focused scope (test component boundaries)
- API and database validation

**When to Use**:
- API endpoints (request → response)
- Database operations (CRUD, queries)
- Service-to-service communication
- Event handlers and message processing
- File I/O operations

**Recommended Tools**:
- **TypeScript/JavaScript**: Vitest + MSW (API mocking), Supertest (HTTP testing)
- **Python**: pytest + pytest-httpserver, pytest-postgresql
- **Go**: testing + httptest, testcontainers
- **Rust**: cargo test + mockito, testcontainers

For detailed patterns, see `references/integration-testing-patterns.md`.

### End-to-End Testing (Top Layer - 10%)

**Purpose**: Validate complete user workflows across the entire application stack

**Characteristics**:
- Slow (minutes per test suite)
- Full integration (real browser, services, database)
- Wide scope (user journeys from start to finish)
- Prone to flakiness (requires careful design)

**When to Use**:
- Critical user journeys (login, checkout, payment)
- Cross-browser compatibility validation
- Real-world scenarios not covered by integration tests
- Regression prevention for core features

**Best Practices**:
- Limit E2E tests to high-value scenarios (not every edge case)
- Use stable selectors (data-testid, not CSS classes)
- Implement retry logic for network flakiness
- Run tests in parallel for speed

**Recommended Tools**:
- **All Languages**: Playwright (cross-browser, fast, Microsoft-backed)

For detailed patterns, see `references/e2e-testing-patterns.md`.

### Contract Testing (Microservices)

**Purpose**: Validate service interfaces and API contracts without full integration

**When to Use**:
- Microservices architecture
- Service-to-service communication
- API contract validation
- Reducing E2E testing overhead

**Recommended Tool**: Pact (pact.io) - supports TypeScript, Python, Go, Rust

For detailed patterns, see `references/contract-testing.md`.

## Test Data Management Strategies

### When to Use Each Approach

**Fixtures (Static Data)**:
- Pros: Deterministic, easy to debug
- Cons: Can become stale, doesn't test variety
- Use When: Testing known scenarios, regression tests

**Factories (Generated Data)**:
- Pros: Flexible, generates variety
- Cons: Less deterministic, harder to debug
- Use When: Need diverse test data, testing edge cases

**Property-Based Testing (Random Data)**:
- Pros: Finds edge cases not anticipated
- Cons: Can be slow, failures harder to reproduce
- Use When: Complex algorithms, parsers, validators

**Recommended Combination**:
- **Unit Tests**: Fixtures (known inputs) + Property-Based (edge cases)
- **Integration Tests**: Factories (flexible data) + Database seeding
- **E2E Tests**: Fixtures (reproducible scenarios)

**Property-Based Testing Tools**:
- **TypeScript/JavaScript**: fast-check
- **Python**: hypothesis (best-in-class)
- **Go**: gopter
- **Rust**: proptest (primary)

For detailed strategies, see `references/test-data-strategies.md`.

## Mocking Decision Matrix

### When to Mock vs. Use Real Dependencies

| Dependency | Unit Test | Integration Test | E2E Test |
|------------|-----------|------------------|----------|
| **Database** | Mock (in-memory) | Real (test DB, Docker) | Real (staging DB) |
| **External API** | Mock (MSW, nock) | Mock (MSW, VCR) | Real (or staging) |
| **Filesystem** | Mock (in-memory FS) | Real (temp directory) | Real |
| **Time/Date** | Mock (freezeTime) | Mock (if deterministic) | Real (usually) |
| **Environment Variables** | Mock (setEnv) | Mock (test config) | Real (test env) |
| **Internal Services** | Mock (stub) | Real (or container) | Real |

**Guiding Principles**:
1. **Unit Tests**: Mock everything external
2. **Integration Tests**: Use real database (ephemeral), mock external APIs
3. **E2E Tests**: Use real everything (or staging equivalents)
4. **Contract Tests**: Mock nothing (test real interfaces)

For detailed mocking patterns, see `references/mocking-strategies.md`.

## Language-Specific Quick Starts

### TypeScript/JavaScript

**Unit Testing with Vitest**:
```typescript
import { describe, test, expect } from 'vitest'

test('calculates total with tax', () => {
  const items = [{ price: 10, quantity: 2 }]
  expect(calculateTotal(items, 0.1)).toBe(22)
})
```

**Integration Testing with MSW**:
```typescript
import { setupServer } from 'msw/node'
import { http, HttpResponse } from 'msw'

const server = setupServer(
  http.get('/api/user/:id', ({ params }) => {
    return HttpResponse.json({ id: params.id, name: 'Test User' })
  })
)
```

**E2E Testing with Playwright**:
```typescript
import { test, expect } from '@playwright/test'

test('user can checkout', async ({ page }) => {
  await page.goto('https://example.com')
  await page.getByRole('button', { name: 'Add to Cart' }).click()
  await expect(page.getByText('1 item in cart')).toBeVisible()
})
```

See `examples/typescript/` for complete working examples.

### Python

**Unit Testing with pytest**:
```python
def test_calculate_total_with_tax():
    items = [{"price": 10, "quantity": 2}]
    assert calculate_total(items, tax_rate=0.1) == 22
```

**Property-Based Testing with hypothesis**:
```python
from hypothesis import given, strategies as st

@given(st.lists(st.integers()))
def test_reverse_reverse_is_identity(lst):
    assert reverse(reverse(lst)) == lst
```

See `examples/python/` for complete working examples.

### Go and Rust

See `examples/go/` and `examples/rust/` for complete working examples in these languages.

## Coverage and Quality Metrics

### Meaningful Coverage Targets

**Recommended Targets**:
- **Critical Business Logic**: 90%+ coverage
- **API Endpoints**: 80%+ coverage
- **Utility Functions**: 70%+ coverage
- **UI Components**: 60%+ coverage (focus on logic, not markup)
- **Overall Project**: 70-80% coverage

**Anti-Pattern**: Aiming for 100% coverage leads to testing trivial code and false confidence.

**Coverage Tools**:
- **TypeScript/JavaScript**: Vitest coverage (c8/istanbul)
- **Python**: pytest-cov
- **Go**: go test -cover
- **Rust**: cargo-tarpaulin

### Mutation Testing (Validate Test Quality)

Mutation testing introduces bugs and verifies tests catch them.

**Tools**:
- **TypeScript/JavaScript**: Stryker Mutator
- **Python**: mutmut
- **Go**: go-mutesting
- **Rust**: cargo-mutants

For detailed coverage strategies, see `references/coverage-strategies.md`.

## CI/CD Integration Patterns

### Fast Feedback Loop Strategy

**Stage 1: Pre-Commit (< 30 seconds)**
- Lint and format checks
- Unit tests (critical paths only)

**Stage 2: On Commit (< 2 minutes)**
- All unit tests
- Static analysis

**Stage 3: Pull Request (< 5 minutes)**
- Integration tests
- Coverage reporting

**Stage 4: Pre-Merge (< 10 minutes)**
- E2E tests (critical paths)
- Cross-browser testing

### Parallel Execution

**Speed Up Test Runs**:
- **Vitest**: `vitest --threads`
- **Playwright**: `playwright test --workers=4`
- **pytest**: `pytest -n auto` (requires pytest-xdist)
- **Go**: `go test -parallel 4`

## Common Anti-Patterns to Avoid

### The Ice Cream Cone (Inverted Pyramid)

**Problem**: Too many E2E tests, too few unit tests
**Result**: Slow test suites, flaky tests, long feedback loops
**Solution**: Rebalance toward more unit tests, fewer E2E tests

### Testing Implementation Details

**Problem**: Tests coupled to internal structure, not behavior
**Solution**: Test behavior (inputs → outputs), not implementation

### Over-Mocking in Integration Tests

**Problem**: Mocking everything defeats purpose of integration tests
**Solution**: Use real databases (ephemeral), mock only external APIs

### Flaky E2E Tests

**Problem**: Tests fail intermittently due to timing issues
**Solutions**:
- Use auto-wait features (Playwright has built-in auto-wait)
- Avoid hardcoded waits (`sleep(1000)`)
- Use stable selectors (data-testid)
- Implement retry logic for network requests

## Integration with Other Skills

**For form testing**: See `building-forms` skill for form-specific validation and submission testing patterns.

**For API testing**: See `api-patterns` skill for REST/GraphQL endpoint testing and contract validation.

**For CI/CD pipelines**: See `building-ci-pipelines` skill for test automation, parallel execution, and coverage reporting.

**For data visualization testing**: See `visualizing-data` skill for snapshot testing chart configurations and visual regression testing.

## Reference Documentation

For deeper exploration of specific topics:

- **`references/testing-pyramid.md`** - Detailed testing pyramid framework and balancing strategies
- **`references/decision-tree.md`** - Comprehensive decision frameworks for test type selection
- **`references/unit-testing-patterns.md`** - Unit testing patterns across languages
- **`references/integration-testing-patterns.md`** - Integration testing with databases, APIs, and containers
- **`references/e2e-testing-patterns.md`** - E2E testing best practices and Playwright patterns
- **`references/contract-testing.md`** - Consumer-driven contract testing with Pact
- **`references/test-data-strategies.md`** - Fixtures, factories, and property-based testing
- **`references/mocking-strategies.md`** - When and how to mock dependencies
- **`references/coverage-strategies.md`** - Meaningful coverage metrics and mutation testing

## Working Examples

Complete, runnable code examples are available in the `examples/` directory:

- **`examples/typescript/`** - Vitest unit/integration, Playwright E2E, MSW mocking, fast-check property tests
- **`examples/python/`** - pytest unit/integration, fixtures, Playwright E2E, hypothesis property tests
- **`examples/go/`** - stdlib testing, testify assertions, httptest integration
- **`examples/rust/`** - cargo test unit tests, proptest property tests, integration patterns

All examples include dependencies, usage instructions, and error handling.
