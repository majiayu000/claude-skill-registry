---
name: testing
description: Comprehensive testing specialization covering test strategy, automation,
  TDD methodology, test writing, and web app testing. Use when setting up test infrastructure,
  writing tests, implementing TDD workflows, analyzing coverage, integrating tests
  into CI/CD, or testing web applications with Playwright. Framework-agnostic approach
  with framework-specific guidance via reference files.
author: Joseph OBrien
status: unpublished
updated: '2025-12-23'
version: 1.0.1
tag: skill
type: skill
---

# Testing

This skill provides comprehensive testing capabilities including test strategy, automation setup, Test-Driven Development (TDD), test writing best practices, coverage analysis, CI/CD integration, and web application testing with Playwright.

## When to Use This Skill

- When setting up test infrastructure for a project
- When creating test strategies and test plans
- When writing unit, integration, or E2E tests
- When implementing TDD/test-first development
- When analyzing test coverage and quality
- When integrating tests into CI/CD pipelines
- When testing web applications with Playwright
- When debugging test failures or improving test reliability
- When writing test fixtures, mock data, or factory functions
- When mocking external dependencies (APIs, databases, file systems)
- When organizing test file structure and test suites
- When testing async code, Promises, or event-driven behavior
- When implementing snapshot tests for UI components
- When configuring test coverage thresholds

## What This Skill Does

1. **Test Strategy**: Designs comprehensive testing strategies (unit, integration, E2E)
2. **Test Automation**: Sets up test frameworks and automation tools
3. **TDD Methodology**: Implements Test-Driven Development workflows (Red-Green-Refactor)
4. **Test Writing**: Writes focused, maintainable tests with proper patterns
5. **Coverage Analysis**: Analyzes and improves test coverage
6. **CI/CD Integration**: Integrates tests into continuous integration pipelines
7. **Web App Testing**: Tests web applications using Playwright
8. **Test Quality**: Improves test reliability and maintainability

## Test Strategy

### Test Pyramid

**Recommended Distribution:**

- **Unit Tests**: 70% - Fast, isolated, test individual functions
- **Integration Tests**: 20% - Test component interactions
- **E2E Tests**: 10% - Test complete user workflows

**Test Types:**

- Functional tests (happy path, edge cases, error handling)
- Non-functional tests (performance, security, accessibility)
- Regression tests (prevent breaking changes)
- Smoke tests (critical path verification)

### Framework Selection

**JavaScript/TypeScript:**

- Jest, Vitest, Mocha for unit/integration
- Playwright, Cypress for E2E
- React Testing Library for component testing

**Python:**

- pytest for unit/integration
- Selenium, Playwright for E2E
- unittest for standard library testing

**Java:**

- JUnit for unit tests
- TestNG for integration
- Selenium for E2E

**Go:**

- Built-in testing package
- Testify for assertions

**Rust:**

- Built-in test framework
- Cargo test for running tests

## Test-Driven Development (TDD)

TDD is a **design technique**, not just a testing technique. It produces better-designed, more maintainable code through small, disciplined steps.

### Core Principle

**Write tests before code. Always.** TDD forces you to think about:

- What behavior do I need?
- How will I know it works?
- What's the simplest implementation?

### The Three Laws (Never Violate)

1. **Write NO production code** without a failing test first
2. **Write only enough test** to demonstrate one failure
3. **Write only enough code** to pass that test

### Red-Green-Refactor Cycle

**Phase 1: RED - Write Failing Test**

1. Write ONE test that defines desired behavior
2. Run test - verify it FAILS
3. Verify it fails for the RIGHT reason (not syntax error)
4. DO NOT write implementation yet

**Phase 2: GREEN - Minimal Implementation**

1. Write MINIMAL code to make test pass
2. Resist urge to add extra features
3. Run test - verify it PASSES
4. If test still fails, fix implementation (not test)

**Phase 3: REFACTOR - Clean Code**

1. Remove code duplication (DRY)
2. Improve naming for clarity
3. Extract complex logic into functions
4. Run ALL tests - must stay green throughout
5. Check test coverage on changed lines

After REFACTOR, start new RED phase for next behavior.

## Test Writing Patterns

### Arrange-Act-Assert (AAA)

**Structure:**

1. **Arrange**: Set up test data and conditions
2. **Act**: Execute the code being tested
3. **Assert**: Verify the expected outcome

**Example:**

```javascript
describe('UserService', () => {
  it('should create user with valid data', async () => {
    // Arrange
    const userData = { email: 'test@example.com', name: 'Test User' };

    // Act
    const result = await userService.createUser(userData);

    // Assert
    expect(result).toHaveProperty('id');
    expect(result.email).toBe(userData.email);
  });
});
```

### Given-When-Then (BDD Style)

**Structure:**

1. **Given**: Initial context/preconditions
2. **When**: Action/event that triggers behavior
3. **Then**: Expected outcome

### Test Organization

**File Structure:**

```
project/
├── src/
│   └── components/
│       └── User.jsx
├── tests/
│   ├── unit/
│   │   └── User.test.jsx
│   ├── integration/
│   │   └── UserAPI.test.js
│   └── e2e/
│       └── user-flow.spec.js
├── jest.config.js
└── playwright.config.js
```

## Coverage Analysis

### Coverage Goals

**Recommended Thresholds:**

- **Lines**: 80%+
- **Functions**: 80%+
- **Branches**: 80%+
- **Statements**: 80%+

**Critical Paths:**

- Always aim for 100% coverage on critical business logic
- Authentication and authorization
- Payment processing
- Data validation

### Coverage Gaps

**Common Gaps:**

- Error handling paths
- Edge cases
- Boundary conditions
- Integration points

**Improvement Strategies:**

- Identify untested code paths
- Add tests for error scenarios
- Test edge cases and boundaries
- Increase integration test coverage

## CI/CD Integration

### Test Pipeline

**Stages:**

1. **Unit Tests**: Fast feedback, run on every commit
2. **Integration Tests**: Run on pull requests
3. **E2E Tests**: Run before merging to main
4. **Performance Tests**: Run on main branch

**Quality Gates:**

- All tests must pass
- Coverage must meet threshold
- No critical security issues
- Performance benchmarks met

## Web Application Testing with Playwright

### Helper Scripts

This skill includes Python helper scripts in `scripts/`:

- **`with_server.py`** - Manages server lifecycle (supports multiple servers). Always run with `--help` first to see usage.

  ```bash
  # Single server
  python scripts/with_server.py --server "npm run dev" --port 5173 -- python your_automation.py

  # Multiple servers (e.g., backend + frontend)
  python scripts/with_server.py \
    --server "cd backend && python server.py" --port 3000 \
    --server "cd frontend && npm run dev" --port 5173 \
    -- python your_automation.py
  ```

### Decision Tree: Choosing Your Approach

```
User task → Is it static HTML?
    ├─ Yes → Read HTML file directly to identify selectors
    │         ├─ Success → Write Playwright script using selectors
    │         └─ Fails/Incomplete → Treat as dynamic (below)
    │
    └─ No (dynamic webapp) → Is the server already running?
        ├─ No → Run: python scripts/with_server.py --help
        │        Then use the helper + write simplified Playwright script
        │
        └─ Yes → Reconnaissance-then-action:
            1. Navigate and wait for networkidle
            2. Take screenshot or inspect DOM
            3. Identify selectors from rendered state
            4. Execute actions with discovered selectors
```

### Playwright Best Practices

- **Use bundled scripts as black boxes** - Use `--help` to see usage, then invoke directly
- Use `sync_playwright()` for synchronous scripts
- Always close the browser when done
- Use descriptive selectors: `text=`, `role=`, CSS selectors, or IDs
- Add appropriate waits: `page.wait_for_selector()` or `page.wait_for_timeout()`
- **CRITICAL**: Wait for `page.wait_for_load_state('networkidle')` before inspection on dynamic apps

### Example: Basic Playwright Script

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('http://localhost:5173')
    page.wait_for_load_state('networkidle')  # CRITICAL: Wait for JS to execute
    # ... your automation logic
    browser.close()
```

### Examples

See `examples/` directory for:

- `element_discovery.py` - Discovering buttons, links, and inputs on a page
- `static_html_automation.py` - Using file:// URLs for local HTML
- `console_logging.py` - Capturing console logs during automation

## Reference Files

For detailed testing patterns and workflows, load reference files as needed:

- **`references/framework_workflows.md`** - Framework-specific TDD workflows and examples for Python (pytest), JavaScript (Jest, Vitest), Java (JUnit), Go, Rust
- **`references/test_patterns.md`** - Common test patterns, test organization, naming conventions, test doubles (mocks, stubs, spies), parametrization, and anti-patterns
- **`references/webapp_testing.md`** - Web application testing patterns, Playwright best practices, and E2E testing strategies
- **`references/TESTING_REPORT.template.md`** - Test quality report template with coverage metrics, audit findings, and recommendations

When working with specific frameworks or need detailed patterns, load the appropriate reference file.

## Best Practices

### Test Quality

1. **Isolation**: Tests should be independent and runnable in any order
2. **Deterministic**: Tests should produce consistent results
3. **Fast**: Unit tests should run quickly (< 100ms each)
4. **Clear**: Test names should describe what they test
5. **Maintainable**: Tests should be easy to update when code changes

### TDD Best Practices

1. **One Behavior Per Test**: Each test verifies ONE behavior
2. **Descriptive Names**: Test names describe the behavior being tested
3. **Independent Tests**: Tests don't depend on each other
4. **Fast Tests**: Mock external dependencies to keep tests fast
5. **Clear Assertions**: Assertions clearly show what's being verified

### Common Mistakes to Avoid

- ❌ Writing multiple tests at once (write one test at a time)
- ❌ Skipping refactor phase (always refactor after green)
- ❌ Implementation before test (delete code and start with test)
- ❌ Over-engineering in GREEN (simplest thing that passes)
- ❌ Writing test that passes immediately (must fail first)

### Test Maintenance

- Review and update tests when requirements change
- Remove obsolete tests
- Refactor tests to reduce duplication
- Keep test data factories up to date
- Monitor test execution time

## Integration with Other Skills

- **debugging**: Use when tests fail unexpectedly
- **code-review**: TDD produces code that's easier to review
- **dead-code-removal**: Tests help identify unused code
- **performance**: Use for performance testing strategies

## Meta-Principle

```
TDD is a DESIGN technique, not a testing technique.

The cycle never changes: RED → GREEN → REFACTOR → Repeat

Writing tests first forces you to think about:
- What behavior do I need?
- How will I know it works?
- What's the simplest implementation?

This produces better-designed, more maintainable code.
```
