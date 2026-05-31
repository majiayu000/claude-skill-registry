---
name: tester
description: Comprehensive testing skill for GabeDA application - designs test strategies (UAT, integration, smoke, unit), creates tests for frontend (React/Playwright) and backend (Django/pytest), executes tests, analyzes results, and generates detailed reports with findings. Stores reports in ai/testing/ and tests in appropriate project folders.
---

# Tester Skill - GabeDA Testing Framework

This skill provides comprehensive testing capabilities for the GabeDA full-stack application (React frontend + Django backend). Design test strategies, create tests, execute them, analyze results, and generate actionable reports.

## Purpose

Ensure quality and reliability of the GabeDA application through systematic testing across all layers:
- **Frontend Testing**: React components, user flows, E2E scenarios (Playwright)
- **Backend Testing**: Django API endpoints, models, business logic (pytest)
- **Integration Testing**: Full-stack workflows across frontend and backend
- **UAT Testing**: User acceptance scenarios matching real business use cases
- **Smoke Testing**: Critical path validation for rapid deployment verification

## When to Use This Skill

Use this skill when:
- **Creating tests** for new features or existing functionality
- **Executing test suites** and collecting results
- **Analyzing test failures** and generating bug reports
- **Designing test strategies** for sprints or releases
- **Validating deployments** with smoke tests
- **Performing UAT** with business stakeholders
- **Generating test reports** for documentation or review

## Testing Standards & Principles

### Test Design Standard

Follow the **AAA Pattern** (Arrange-Act-Assert):
```python
def test_example():
    # Arrange - Set up test data and preconditions
    user = create_test_user()

    # Act - Perform the action being tested
    result = user.login(email, password)

    # Assert - Verify the expected outcome
    assert result.is_authenticated == True
```

### Test Coverage Goals
- **Critical paths**: 100% coverage (login, company creation, data upload)
- **Core features**: ≥90% coverage (dashboard, analytics, reports)
- **Edge cases**: ≥70% coverage (error handling, validation)
- **UI components**: ≥80% component coverage

### Test Naming Convention
```python
# Backend (pytest)
def test_<feature>_<scenario>_<expected_result>():
    # Example: test_login_with_valid_credentials_returns_tokens()
    pass

# Frontend (Playwright)
test('<feature> - <scenario> - <expected result>', async () => {
    // Example: test('Login - valid credentials - redirects to dashboard')
})
```

## Project Structure

```
GabeDA Project:
├── gabeda_frontend/
│   └── tests/                          # Frontend tests (Playwright)
│       ├── e2e/                        # End-to-end tests
│       ├── integration/                # Integration tests
│       └── smoke/                      # Smoke tests
├── gabeda_backend/
│   └── tests/                          # Backend tests (pytest)
│       ├── unit/                       # Unit tests
│       ├── integration/                # Integration tests
│       └── api/                        # API endpoint tests
└── khujta_ai_business/
    └── ai/testing/                     # Test reports & strategies
        ├── reports/                    # Test execution reports
        │   └── YYYY-MM-DD_HH-MM_<test-type>_report.md
        ├── strategies/                 # Test strategy documents
        └── findings/                   # Bug reports & findings
```

## Test Types & When to Use

### 1. Unit Tests
**Purpose**: Test individual functions/methods in isolation
**When**: After creating any new function, API endpoint, or component
**Location**: Backend `tests/unit/`, Frontend component tests
**Example**:
```python
# Backend: Test RUT validation
def test_validate_rut_with_valid_format_returns_cleaned():
    result = validate_rut_field('12.345.678-9')
    assert result == '123456789'
```

### 2. Integration Tests
**Purpose**: Test interactions between multiple components/services
**When**: After integrating multiple modules or connecting frontend-backend
**Location**: Both `tests/integration/`
**Example**: Test complete login flow (frontend → API → database → response)

### 3. E2E Tests (Playwright)
**Purpose**: Test complete user workflows from browser perspective
**When**: For critical user journeys and multi-step workflows
**Location**: `gabeda_frontend/tests/e2e/`
**Example**: User registers → creates company → uploads CSV → views dashboard

### 4. Smoke Tests
**Purpose**: Quick validation of critical functionality after deployment
**When**: Before/after deployments, CI/CD pipeline
**Location**: Both `tests/smoke/`
**Duration**: Must complete in <5 minutes
**Example**: Can login? Can create company? Can upload file?

### 5. UAT (User Acceptance Tests)
**Purpose**: Validate business requirements with stakeholders
**When**: Before major releases, sprint demos
**Location**: `ai/testing/strategies/uat_<feature>.md`
**Format**: Written scenarios with expected outcomes

## Workflow

### Creating Tests

**Step 1: Analyze the Feature**
- Understand the feature requirements
- Identify critical paths and edge cases
- Determine appropriate test types (unit, integration, E2E)

**Step 2: Design Test Cases**
- List scenarios to test (happy path, edge cases, error cases)
- Define test data requirements
- Plan assertions and expected outcomes

**Step 3: Write Tests**
```bash
# Frontend (Playwright/Vitest)
# Location: gabeda_frontend/tests/<type>/

# Backend (pytest)
# Location: gabeda_backend/tests/<type>/
```

**Step 4: Execute and Verify**
- Run tests locally
- Fix any failures
- Ensure tests are deterministic (no flaky tests)

### Executing Tests

**Frontend Tests:**
```bash
cd gabeda_frontend

# Run all tests
npm run test

# Run E2E tests
npm run test:e2e

# Run specific test file
npm run test tests/e2e/login.spec.ts
```

**Backend Tests:**
```bash
cd gabeda_backend

# Run all tests
./benv/Scripts/python -m pytest

# Run specific test file
./benv/Scripts/python -m pytest tests/unit/test_rut_validation.py

# Run with coverage
./benv/Scripts/python -m pytest --cov=apps --cov-report=html
```

### Generating Reports

After test execution, generate a comprehensive report:

**Report Structure** (stored in `ai/testing/reports/`):
```markdown
# Test Report: <Test Type> - <Date>

## Summary
- Total Tests: X
- Passed: X
- Failed: X
- Skipped: X
- Duration: X minutes
- Coverage: X%

## Test Results by Category
[Breakdown by feature/module]

## Failed Tests
[For each failure:]
- Test Name
- Error Message
- Stack Trace
- Reproduction Steps
- Suggested Fix

## Coverage Analysis
[Areas with low coverage]

## Recommendations
[Next steps, areas needing attention]
```

## Test Execution Commands

### Quick Reference

```bash
# Frontend - All tests
cd gabeda_frontend && npm run test

# Frontend - E2E only
cd gabeda_frontend && npm run test:e2e

# Frontend - Watch mode
cd gabeda_frontend && npm run test:watch

# Backend - All tests
cd gabeda_backend && ./benv/Scripts/python -m pytest

# Backend - With coverage
cd gabeda_backend && ./benv/Scripts/python -m pytest --cov --cov-report=term-missing

# Backend - Specific module
cd gabeda_backend && ./benv/Scripts/python -m pytest tests/unit/accounts/

# Backend - Stop on first failure
cd gabeda_backend && ./benv/Scripts/python -m pytest -x

# Backend - Verbose output
cd gabeda_backend && ./benv/Scripts/python -m pytest -v
```

## Example: Creating a Test for the Dashboard Company Switcher

**Scenario**: Test that users with multiple companies can switch between them

**Step 1: Test Design**
```
Feature: Company Switcher
Test Type: E2E (Playwright)
Location: gabeda_frontend/tests/e2e/company-switcher.spec.ts

Scenarios:
1. User with 1 company - switcher not visible
2. User with 2+ companies - switcher visible
3. Switching companies - dashboard updates
4. Selected company persists - on page reload
```

**Step 2: Implementation** (see `references/test-examples.md` for complete code)

**Step 3: Execution**
```bash
cd gabeda_frontend
npm run test:e2e tests/e2e/company-switcher.spec.ts
```

**Step 4: Report Generation**
Create report in `ai/testing/reports/2025-11-01_18-30_e2e-company-switcher_report.md` with results

## Best Practices

### Test Data Management
- **Use factories/fixtures** for test data creation
- **Clean up after tests** (database transactions, file cleanup)
- **Don't rely on production data** - create isolated test data
- **Use realistic data** - matching production data shapes

### Test Independence
- **Each test must be independent** - can run in any order
- **No shared state** between tests
- **Reset database/state** between test runs

### Assertions
- **Be specific** - assert exact values, not just truthy/falsy
- **One logical assertion per test** - split complex scenarios
- **Clear error messages** - make failures easy to debug

### Performance
- **Keep unit tests fast** (<100ms each)
- **Parallelize when possible** - run independent tests concurrently
- **Mock external services** - don't hit real APIs in tests

## References

- `references/test-examples.md` - Complete test examples for all test types
- `references/playwright-patterns.md` - Playwright best practices and patterns
- `references/pytest-patterns.md` - Pytest fixtures and patterns
- `references/test-data-factories.md` - Test data creation strategies

## Troubleshooting

**Flaky Tests**: Tests that pass/fail inconsistently
- Add explicit waits for async operations
- Use Playwright's built-in wait mechanisms
- Check for race conditions in test setup

**Slow Tests**: Tests taking too long
- Mock external API calls
- Use in-memory database for unit tests
- Parallelize test execution

**Failed Assertions**: Tests failing unexpectedly
- Check test data setup
- Verify environment variables
- Review recent code changes

## Output Locations

**Test Files**:
- Frontend: `C:\Projects\play\gabeda_frontend\tests\`
- Backend: `C:\Projects\play\gabeda_backend\tests\`

**Test Reports**:
- All reports: `C:\Projects\play\khujta_ai_business\ai\testing\reports\`
- Test strategies: `C:\Projects\play\khujta_ai_business\ai\testing\strategies\`
- Bug findings: `C:\Projects\play\khujta_ai_business\ai\testing\findings\`

## Skill Usage Examples

**Example 1: Create E2E test for company dashboard**
```
User: "Create an E2E test that logs in a test user, creates 2 companies,
       and verifies both companies show in the switcher"

Tester Skill:
1. Creates test file at gabeda_frontend/tests/e2e/test-dashboard-multi-company.spec.ts
2. Implements test with Playwright
3. Executes test and collects results
4. Generates report at ai/testing/reports/2025-11-01_19-00_e2e-dashboard_report.md
```

**Example 2: Run smoke tests before deployment**
```
User: "Run smoke tests for the frontend and backend"

Tester Skill:
1. Executes frontend smoke tests
2. Executes backend smoke tests
3. Collects all results
4. Generates combined report with pass/fail status
5. Recommends proceed/block deployment based on results
```

**Example 3: Design UAT strategy for new feature**
```
User: "Design UAT test cases for the file upload feature"

Tester Skill:
1. Reviews feature requirements
2. Creates UAT strategy document at ai/testing/strategies/uat_file_upload.md
3. Lists scenarios: valid CSV, invalid format, large files, etc.
4. Defines acceptance criteria for each scenario
5. Provides test data samples
```
