---
name: ln-743-test-infrastructure
description: Creates test infrastructure with Vitest, xUnit, and pytest
---

# ln-743-test-infrastructure

**Type:** L3 Worker
**Category:** 7XX Project Bootstrap
**Parent:** ln-740-quality-setup

Sets up testing frameworks, coverage tools, and sample tests for projects.

---

## Purpose & Scope

**Does:**
- Detects project stack to choose appropriate test framework
- Creates test configuration files
- Sets up coverage reporting with thresholds
- Creates sample tests demonstrating patterns
- Verifies test suite runs successfully

**Does NOT:**
- Configure linters (ln-741 does this)
- Set up pre-commit hooks (ln-742 does this)
- Write actual application tests (developers do this)

---

## Supported Stacks

| Technology | Test Framework | Coverage Tool | Config File |
|------------|---------------|---------------|-------------|
| TypeScript/React | Vitest | v8/Istanbul | `vitest.config.ts` |
| .NET | xUnit | Coverlet | `*.Tests.csproj` |
| Python | pytest | pytest-cov | `pytest.ini` or `pyproject.toml` |

---

## Phase 1: Check Existing Tests

Before creating test infrastructure, check what exists.

**Files to Check:**

| Stack | Test Indicators |
|-------|-----------------|
| TypeScript | `vitest.config.*`, `jest.config.*`, `*.test.ts`, `*.spec.ts` |
| .NET | `*.Tests.csproj`, `*.IntegrationTests.csproj` |
| Python | `pytest.ini`, `conftest.py`, `tests/`, `test_*.py` |

**Decision Logic:**
1. If complete test setup exists: **SKIP** (inform user)
2. If partial setup: **ASK** to extend or replace
3. If no tests: **CREATE** from templates

---

## Phase 2: Create Test Configuration

### TypeScript/React (Vitest)

Create `vitest.config.ts`:
- Use v8 coverage provider (faster than Istanbul)
- Configure jsdom environment for React
- Set coverage thresholds (80% minimum)
- Create setup file for testing-library

**Dependencies:**
```
npm install -D vitest @vitest/coverage-v8 @testing-library/react @testing-library/jest-dom jsdom
```

### .NET (xUnit)

Create test project:
```bash
dotnet new xunit -n {Project}.Tests
dotnet sln add tests/{Project}.Tests
```

**Dependencies (in .csproj):**
- Microsoft.NET.Test.Sdk
- xunit
- xunit.runner.visualstudio
- Moq
- FluentAssertions
- coverlet.collector

### Python (pytest)

Add to `pyproject.toml` or create `pytest.ini`:
- Configure test discovery paths
- Set coverage thresholds (80% minimum)
- Configure coverage reporting

**Dependencies:**
```
pip install pytest pytest-cov pytest-asyncio
# OR with uv:
uv add --dev pytest pytest-cov pytest-asyncio
```

---

## Phase 3: Create Test Directory Structure

### TypeScript

```
src/
├── components/
│   ├── Button.tsx
│   └── Button.test.tsx  # Co-located tests
├── test/
│   └── setup.ts         # Test setup file
```

### .NET

```
tests/
├── {Project}.Tests/
│   ├── Controllers/
│   │   └── SampleControllerTests.cs
│   ├── Services/
│   └── {Project}.Tests.csproj
└── {Project}.IntegrationTests/  # Optional
```

### Python

```
tests/
├── __init__.py
├── conftest.py          # Fixtures
├── unit/
│   └── test_sample.py
└── integration/         # Optional
```

---

## Phase 4: Create Sample Tests

Create one sample test per stack demonstrating:
- AAA pattern (Arrange-Act-Assert)
- Test naming conventions
- Basic assertions
- Framework-specific patterns

### TypeScript Sample Test

Shows:
- render() from testing-library
- screen queries
- Jest-dom matchers

### .NET Sample Test

Shows:
- [Fact] attribute
- Moq for mocking
- FluentAssertions syntax

### Python Sample Test

Shows:
- pytest fixtures
- assert statements
- parametrized tests (optional)

---

## Phase 5: Verify Test Run

After setup, verify tests work.

**TypeScript:**
```bash
npm test
npm run test:coverage
```
Expected: Sample test passes, coverage report generated

**.NET:**
```bash
dotnet test
dotnet test --collect:"XPlat Code Coverage"
```
Expected: Sample test passes, coverage collected

**Python:**
```bash
pytest
pytest --cov=src --cov-report=term-missing
```
Expected: Sample test passes, coverage report shown

**On Failure:** Check test configuration, dependencies, verify sample test syntax.

---

## Coverage Requirements

| Metric | Minimum | Target |
|--------|---------|--------|
| Lines | 70% | 80% |
| Branches | 70% | 80% |
| Functions | 70% | 80% |
| Statements | 70% | 80% |

Configure CI to fail if coverage drops below thresholds.

---

## Critical Rules

> **RULE 1:** Coverage thresholds MUST be configured. No exceptions.

> **RULE 2:** Sample tests MUST pass. Don't create broken examples.

> **RULE 3:** Use AAA pattern (Arrange-Act-Assert) in all sample tests.

> **RULE 4:** Co-locate unit tests with source (TypeScript) or use tests/ directory (.NET, Python).

---

## Definition of Done

- [ ] Test framework installed and configured
- [ ] Coverage tool configured with 80% threshold
- [ ] Test directory structure created
- [ ] Sample test created and passing
- [ ] `npm test` / `dotnet test` / `pytest` runs successfully
- [ ] Coverage report generates
- [ ] User informed of:
  - How to run tests
  - Where to add new tests
  - Coverage requirements

---

## Reference Files

| File | Purpose |
|------|---------|
| [vitest_template.ts](references/vitest_template.ts) | Vitest config template |
| [vitest_setup_template.ts](references/vitest_setup_template.ts) | Test setup file |
| [react_test_template.tsx](references/react_test_template.tsx) | React component test |
| [xunit_csproj_template.xml](references/xunit_csproj_template.xml) | .NET test project |
| [xunit_test_template.cs](references/xunit_test_template.cs) | xUnit test example |
| [pytest_config_template.toml](references/pytest_config_template.toml) | pytest config |
| [pytest_test_template.py](references/pytest_test_template.py) | pytest test example |
| [testing_guide.md](references/testing_guide.md) | Testing best practices |

---

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Vitest not found | Not installed | `npm install -D vitest` |
| jsdom errors | Missing dependency | `npm install -D jsdom` |
| xUnit discovery fails | SDK version mismatch | Update Microsoft.NET.Test.Sdk |
| pytest not found | Not in PATH | `pip install pytest` |
| Coverage 0% | Wrong source path | Check coverage.include config |

---

**Version:** 2.0.0
**Last Updated:** 2026-01-10
