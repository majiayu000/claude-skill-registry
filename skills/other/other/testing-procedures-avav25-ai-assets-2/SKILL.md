---
name: testing-procedures
description: Test strategy design, test writing guide, and coverage targets. Use when writing tests, designing test plans, setting up test infrastructure, or evaluating test quality. Provides patterns for unit, integration, E2E, and API testing.
user-invocable: false
---

# Testing Procedures

Systematic testing skill covering strategy, patterns, and quality gates. Produces consistent, maintainable test suites across tech stacks.

## When to Use

- Writing new tests for features or bug fixes
- Designing test strategy for a new project or module
- Evaluating existing test coverage and quality
- Setting up test infrastructure (fixtures, factories, mocks)
- Creating or updating `TESTING.md` documentation

## When NOT to Use

- Running tests (use `/run-tests` workflow instead)
- Reviewing test code quality (use `code-review` skill)
- Validating CI pipeline configuration (use `Agent(devops-engineer)` role)

## Test Pyramid

Follow the test pyramid for cost-effective coverage:

```
        /  E2E  \           Few — critical user journeys only
       /----------\
      / Integration \       Moderate — API, DB, service boundaries
     /----------------\
    /    Unit Tests     \   Many — fast, isolated, comprehensive
   /--------------------\
```

| Layer | What to Test | Speed | Count |
|---|---|---|---|
| **Unit** | Pure logic, transformations, validators, utils | < 50ms | Many |
| **Integration** | DB queries, API endpoints, service interactions | < 5s | Moderate |
| **E2E** | Critical user journeys, happy paths, key flows | < 30s | Few |

## Test Design Principles

1. **Test behavior, not implementation** — assert outcomes, not internal calls
2. **One assertion per concept** — each test verifies one logical thing
3. **Arrange-Act-Assert** — clear structure in every test
4. **Deterministic** — no flaky tests. Mock time, randomness, external services
5. **Independent** — tests must not depend on execution order
6. **Descriptive names** — test name describes the scenario: `should_return_404_when_user_not_found`
7. **Fast feedback** — unit tests run in seconds, not minutes

## Coverage Targets

| Metric | Target | Hard Minimum |
|---|---|---|
| Line coverage | ≥ 80% | ≥ 60% |
| Branch coverage | ≥ 75% | ≥ 50% |
| Critical path coverage | 100% | 100% |
| New code coverage | ≥ 90% | ≥ 80% |

**Critical paths** = authentication, authorization, payment, data mutations, error handling.

## Key Context File

Projects should have a `TESTING.md` at the root (and per-service in monorepos) documenting test infrastructure, commands, credentials, and organization. Created by `/project-init` using `Agent(qa-engineer)`. Always read `TESTING.md` before writing or running tests.

## Integration

- **Follows rules**: `Agent(qa-engineer)` (test strategy, automation, local test infra), `Agent(software-engineer)` (code quality)
- **Used by workflows**: `/test-local` (full local QA cycle), `/run-tests` (lightweight execution), `/project-init` (TESTING.md generation), `/feature-dev`, `/bugfix`, `/pre-commit`
- **Companion resources**: `test-writing-guide.md`
- **Template**: `templates/testing.template.md` (root + per-service TESTING.md templates)
- **Project context**: `TESTING.md` (root + per-service)
