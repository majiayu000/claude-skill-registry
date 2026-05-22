---
name: testing-automation-expert
description: Production-grade testing strategies for robust, maintainable systems. Covers unit/integration/E2E testing, contract testing, accessibility, mutation testing, and CI/CD patterns. Supports Python (pytest) and TypeScript (Jest/Vitest/Playwright).
author: George Khananaev
---

# Testing Automation Expert

Master production-grade testing strategies for Python and TypeScript applications. QA Architect level - design test ecosystems that scale.

## When to Use

- Designing test strategies for features/projects
- Setting up pytest, Jest, Vitest, or Playwright
- Improving test coverage and quality
- Contract testing, accessibility, mutation testing
- CI/CD test pipeline optimization
- Test architecture review or refactoring

## Triggers

- `/test-plan` - Design test strategy for a feature/project
- `/fixture-refactor` - Optimize test fixture architecture
- `/e2e-setup` - Set up Playwright E2E testing
- `/test-audit` - Review test coverage and quality
- `/contract-test` - Set up Pact contract testing

## Reference Files

Load the appropriate reference based on need:

| Category | Framework | Reference |
|----------|-----------|-----------|
| Python | pytest | `references/python-pytest.md` |
| TypeScript | Jest | `references/typescript-jest.md` |
| TypeScript | Vitest | `references/typescript-vitest.md` |
| E2E | Playwright | `references/e2e-playwright.md` |
| Advanced | Contract/A11y/Mutation | `references/specialized-testing.md` |

## Test Quality Checklists

### Pre-Implementation Checklist

- [ ] **Test strategy defined** - unit, integration, E2E, contract boundaries clear
- [ ] **Fixtures planned** - factory functions, DB setup, cleanup
- [ ] **Mocking strategy** - mock at boundaries only, not internals
- [ ] **Coverage targets** - minimum 80% branches/lines/functions
- [ ] **CI integration** - tests run on every PR with sharding if >10min
- [ ] **Flakiness detection** - pytest-randomly / random test order enabled

### Unit Test Checklist

- [ ] Tests isolated - no shared state between tests
- [ ] One assertion focus - test one behavior per test
- [ ] Descriptive names - `should_return_error_when_user_not_found`
- [ ] AAA pattern - Arrange, Act, Assert clearly separated
- [ ] Edge cases covered - null, empty, boundary values
- [ ] No external dependencies - DB, network, filesystem mocked
- [ ] Property-based tests - Hypothesis/fast-check for edge case discovery

### Integration Test Checklist

- [ ] Real dependencies - use Testcontainers (not SQLite for Postgres!)
- [ ] Transaction rollback - isolate tests with rollback
- [ ] API contract tested - request/response shapes verified
- [ ] Error paths tested - timeout, connection errors
- [ ] Auth flows tested - token generation, validation
- [ ] Declarative assertions - dirty-equals for complex JSON

### E2E Test Checklist

- [ ] Critical paths covered - login, checkout, core flows
- [ ] Page Object Model - locators abstracted into classes
- [ ] Resilient selectors - role/label over CSS/xpath
- [ ] Network mocking - test error states without real API
- [ ] Visual regression - Docker for consistent screenshots
- [ ] Cross-browser - Chrome, Firefox, Safari, mobile
- [ ] Auth state reuse - save/load storage state
- [ ] Trace artifacts - uploaded for CI debugging

### Architecture Checklist (Microservices)

- [ ] Contract tests - Pact CDCT between services
- [ ] API fuzzing - schemathesis against OpenAPI spec
- [ ] Mutation testing - mutmut/Stryker validates test quality
- [ ] Accessibility - axe-core in E2E pipeline
- [ ] Performance baselines - k6/Locust load tests
- [ ] CI sharding - parallel machines for >10min suites

### Test Maintenance Checklist

- [ ] No flaky tests - deterministic, no `sleep()`
- [ ] Fast execution - unit <5s, integration <30s, E2E <2min
- [ ] Readable failures - clear error messages
- [ ] DRY fixtures - reusable factories, not copy-paste
- [ ] Regular cleanup - delete obsolete tests
- [ ] Quarantine flaky - `.flaky.spec.ts` until fixed

## Testing Pyramid

```
         /\
        /E2E\        Few, slow, high confidence
       /-----\
      /Integ. \      Some, moderate speed
     /---------\
    / Contract  \    Service boundaries
   /-------------\
  /    Unit       \  Many, fast, isolated
 /------------------\
```

| Type | Count | Speed | Scope |
|------|-------|-------|-------|
| Unit | 60% | <100ms | Single function |
| Contract | 10% | <1s | Service interface |
| Integration | 20% | <5s | Service + DB |
| E2E | 10% | <30s | Full user flow |

## Test Organization

```
tests/
├── conftest.py / setup.ts   # Root fixtures
├── factories/               # Test data factories
│   └── user.factory.ts
├── fixtures/                # Static test data
│   └── users.json
├── unit/                    # Fast, isolated
│   ├── services/
│   └── utils/
├── integration/             # DB, external services
│   ├── api/
│   └── repositories/
├── contract/                # Pact consumer/provider
│   ├── consumer/
│   └── provider/
├── e2e/                     # Full user flows
│   ├── pages/               # Page objects
│   ├── specs/
│   └── a11y/                # Accessibility tests
└── load/                    # k6/Locust scripts
    └── api-load.js
```

## Anti-Patterns

| Don't | Do |
|-------|-----|
| Test implementation details | Test behavior/contracts |
| Hardcode test data | Use factories/fixtures |
| Share state between tests | Isolate with fixtures |
| Mock everything | Mock at boundaries only |
| Use `time.sleep()` | Use `wait_for` or time mocking |
| Use SQLite for Postgres tests | Use Testcontainers |
| Write flaky time-based tests | Use `time-machine` / `vi.useFakeTimers()` |
| Skip edge cases | Use property-based testing |
| Ignore test failures | Fix or remove immediately |
| One giant conftest.py | Split into modules |
| Integration tests for service contracts | Use Pact contract testing |
| Skip accessibility | Add axe-core to E2E |
| Trust coverage alone | Add mutation testing |

## Specialized Testing

### Contract Testing (Microservices)

```python
# Consumer test (Python)
pact = Consumer("UserService").has_pact_with(Provider("AuthService"))
```

See `references/specialized-testing.md` for full Pact patterns.

### API Fuzzing (FastAPI/OpenAPI)

```bash
schemathesis run http://localhost:8000/openapi.json
```

Auto-generates tests from OpenAPI spec - finds edge cases.

### Mutation Testing

```bash
# Python
mutmut run && mutmut results

# TypeScript
npx stryker run
```

Validates test quality - surviving mutants = gaps.

### Accessibility Testing

```typescript
const results = await new AxeBuilder({ page }).analyze();
expect(results.violations).toEqual([]);
```

## Quick Reference

### Python (pytest)

```bash
pytest                              # Run all
pytest -m "not slow"                # Skip slow
pytest --cov=src --cov-report=html  # Coverage
pytest -n auto                      # Parallel
pytest -x --lf                      # Stop first, re-run failed
pytest -p randomly                  # Randomize order (flakiness detection)
```

### TypeScript (Vitest)

```bash
npx vitest                  # Watch mode
npx vitest run              # Run once
npx vitest --coverage       # Coverage
npx vitest --ui             # Browser UI
```

### Playwright

```bash
npx playwright test                 # Run all
npx playwright test --shard=1/4     # CI sharding
npx playwright test --debug         # Debug mode
npx playwright show-trace trace.zip # View trace
```

## Recommended Packages

### Python

```bash
# Core
pip install pytest pytest-asyncio pytest-cov pytest-xdist
pip install pytest-mock pytest-randomly time-machine

# Advanced
pip install syrupy hypothesis dirty-equals
pip install testcontainers[postgres] httpx
pip install schemathesis pact-python mutmut
pip install playwright pytest-playwright axe-playwright-python
pip install locust  # Load testing
```

### TypeScript

```bash
# Vitest (recommended for new projects)
npm install -D vitest @vitest/coverage-v8 @vitest/ui

# Jest (legacy/React Native)
npm install -D jest ts-jest @types/jest

# Shared
npm install -D supertest @types/supertest @faker-js/faker
npm install -D @testcontainers/postgresql

# Playwright
npm init playwright@latest
npm install -D @axe-core/playwright

# Contract & Mutation
npm install -D @pact-foundation/pact
npm install -D @stryker-mutator/core @stryker-mutator/vitest-runner
```