---
name: faion-testing-developer
description: "Testing: unit, integration, E2E, TDD, mocking, security testing."
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion, TodoWrite, Skill
---
> **Entry point:** `/faion-net` — invoke this skill for automatic routing to the appropriate domain.

# Testing Developer Skill

Testing strategies and implementation covering unit tests, integration tests, E2E tests, TDD workflow, and testing best practices.

## Purpose

Handles all aspects of software testing including test design, implementation, mocking, fixtures, and testing frameworks.

---

## Context Discovery

### Auto-Investigation

Detect testing setup from project:

| Signal | How to Check | What It Tells Us |
|--------|--------------|------------------|
| `pytest.ini` or `pyproject.toml [tool.pytest]` | `Glob("**/pytest.ini")` | pytest used |
| `conftest.py` | `Glob("**/conftest.py")` | pytest fixtures exist |
| `jest.config.*` | `Glob("**/jest.config.*")` | Jest used |
| `vitest.config.*` | `Glob("**/vitest.config.*")` | Vitest used |
| `*_test.go` | `Glob("**/*_test.go")` | Go tests exist |
| `playwright.config.*` | `Glob("**/playwright.config.*")` | E2E with Playwright |
| `cypress/` | `Glob("**/cypress/**")` | E2E with Cypress |
| Coverage config | `Grep("coverage", "**/package.json")` | Coverage enabled |

**Read existing patterns:**
- Check existing tests for patterns (AAA, fixtures)
- Read conftest.py for shared fixtures
- Check CI for test commands

### Discovery Questions

#### Q1: Testing Goal

```yaml
question: "What testing help do you need?"
header: "Goal"
multiSelect: false
options:
  - label: "Write tests for existing code"
    description: "Add test coverage"
  - label: "Set up testing framework"
    description: "Configure from scratch"
  - label: "TDD for new feature"
    description: "Write tests first"
  - label: "Fix flaky tests"
    description: "Stabilize test suite"
  - label: "Improve coverage"
    description: "Find and fill gaps"
```

#### Q2: Test Level

```yaml
question: "What level of testing?"
header: "Level"
multiSelect: true
options:
  - label: "Unit tests"
    description: "Test individual functions/classes"
  - label: "Integration tests"
    description: "Test components together"
  - label: "E2E tests"
    description: "Test full user flows"
  - label: "API tests"
    description: "Test HTTP endpoints"
```

**Routing:**
- "Unit" → unit-testing, mocking-strategies
- "Integration" → integration-testing, test containers
- "E2E" → e2e-testing, Playwright/Cypress
- "API" → api-testing, contract testing

#### Q3: Test Framework (if not detected)

```yaml
question: "Which test framework?"
header: "Framework"
multiSelect: false
options:
  - label: "pytest (Python)"
    description: "Python testing framework"
  - label: "Jest (JavaScript)"
    description: "JavaScript testing"
  - label: "Vitest (JavaScript)"
    description: "Fast Vite-native testing"
  - label: "Go testing"
    description: "Built-in Go testing"
  - label: "Playwright (E2E)"
    description: "Cross-browser E2E"
```

#### Q4: Mocking Needs

```yaml
question: "What do you need to mock?"
header: "Mocking"
multiSelect: true
options:
  - label: "External APIs"
    description: "HTTP calls to third parties"
  - label: "Database"
    description: "DB queries and transactions"
  - label: "Time/dates"
    description: "Freeze time for tests"
  - label: "File system"
    description: "File operations"
  - label: "Nothing / minimal mocking"
    description: "Prefer real dependencies"
```

---

## When to Use

- Unit testing strategies
- Integration testing
- End-to-end (E2E) testing
- Test-driven development (TDD)
- Mocking and stubbing
- Test fixtures and factories
- Security testing
- Code coverage analysis
- Language-specific testing (pytest, Jest, Go testing, etc.)

## Methodologies

| Category | Methodology | File |
|----------|-------------|------|
| **Testing Levels** |
| Unit testing | Unit test patterns, isolation, assertions | unit-testing.md |
| Integration testing | Integration test patterns, test containers | integration-testing.md |
| E2E testing basics | End-to-end test patterns | e2e-testing.md |
| E2E testing alt | E2E strategies | testing-e2e.md |
| **Testing Practices** |
| TDD workflow | Red-green-refactor, TDD cycle | tdd-workflow.md |
| Mocking strategies | Mocks, stubs, spies, fakes | mocking-strategies.md |
| Test fixtures | Fixture patterns, factory pattern | test-fixtures.md |
| Testing patterns | General testing patterns | testing-patterns.md |
| **Security** |
| Security testing | SAST, DAST, penetration testing | security-testing.md |
| **Language-Specific** |
| pytest testing | pytest fixtures, parametrize, markers | testing-pytest.md |
| JavaScript testing | Jest, Vitest, React Testing Library | testing-javascript.md |
| Go testing | Go testing stdlib, table tests | testing-go.md |

## Tools by Language

**Python:** pytest, unittest, hypothesis, factory-boy, faker
**JavaScript:** Jest, Vitest, Mocha, Chai, React Testing Library, Cypress, Playwright
**Go:** testing stdlib, testify, gomock
**Java:** JUnit 5, Mockito, AssertJ
**C#:** xUnit, NUnit, Moq, FluentAssertions

**E2E:** Playwright, Cypress, Selenium, Puppeteer
**Security:** OWASP ZAP, Burp Suite, Snyk, SonarQube

## Related Sub-Skills

| Sub-skill | Relationship |
|-----------|--------------|
| faion-python-developer | pytest, Django testing |
| faion-javascript-developer | Jest, Vitest testing |
| faion-backend-developer | Language-specific testing |
| faion-api-developer | API testing, contract testing |
| faion-devtools-developer | Code coverage, test automation |

## Integration

Invoked by parent skill `faion-software-developer` for testing-related work.

---

*faion-testing-developer v1.0 | 12 methodologies*
