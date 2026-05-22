---
name: cui-javascript-unit-testing
description: Jest unit testing standards covering configuration, test structure, testing patterns, and coverage requirements
allowed-tools:
  - Read
  - Grep
  - Glob
---

# JavaScript Unit Testing Standards

**EXECUTION MODE**: You are now executing this skill. DO NOT explain or summarize these instructions to the user. IMMEDIATELY begin the workflow below based on the task context.

## Overview

This skill provides comprehensive Jest unit testing standards for CUI JavaScript projects, covering Jest configuration, test organization, component testing patterns, mocking strategies, and coverage requirements.

## Prerequisites

To effectively use this skill, you should have:

- JavaScript testing experience with Jest framework
- Understanding of unit testing principles (AAA pattern, test isolation)
- Familiarity with DOM testing and component testing concepts
- Knowledge of mocking and test doubles

## Standards Documents

This skill includes the following standards documents:

- **jest-configuration.md** - Jest setup, package.json config, transform patterns, module mapping
- **test-structure.md** - Test file organization, naming conventions, setup files, directory structure
- **testing-patterns.md** - Component testing, mocking strategies, assertions, AAA pattern
- **coverage-standards.md** - Coverage thresholds (80%), reporting formats, collection strategies

## What This Skill Provides

### Jest Configuration
- **Core Setup**: Jest environment configuration (jsdom), testMatch patterns
- **Module Mapping**: Mock configuration for Lit, DevUI, and other dependencies
- **Transform Configuration**: Babel-jest setup for ES modules, transformIgnorePatterns
- **Setup Files**: Global test setup, DOM polyfills, mock implementations

### Test Structure
- **File Organization**: Standard directory structure (components/, mocks/, setup/, utils/)
- **Naming Conventions**: Component tests (*.test.js), integration tests, utility tests
- **Setup Files**: jest.setup.js, jest.setup-dom.js configuration patterns
- **Test File Structure**: Describe blocks, beforeEach/afterEach patterns

### Testing Patterns
- **Component Testing**: Lit component test structure, rendering tests, property tests
- **Mocking Strategies**: Lit framework mocks, DevUI mocks, external dependency mocking
- **Assertion Patterns**: Jest matchers, @testing-library/jest-dom assertions
- **AAA Pattern**: Arrange-Act-Assert structure, test isolation principles

### Coverage Standards
- **Minimum Thresholds**: 80% for branches, functions, lines, statements
- **Coverage Collection**: Strategies for mocked vs actual source files
- **Reporting Formats**: text, lcov, html, cobertura for different use cases
- **Coverage Directory**: target/coverage integration with build system

## When to Activate

This skill should be activated when:

1. **Writing Tests**: Creating new Jest unit tests for JavaScript code
2. **Configuring Jest**: Setting up Jest for a new project or updating configuration
3. **Test Review**: Reviewing test quality and coverage compliance
4. **Mocking**: Implementing mocks for Lit components or external dependencies
5. **Coverage Analysis**: Understanding or improving test coverage
6. **Test Structure**: Organizing test files and setup
7. **CI/CD Integration**: Configuring test execution in build pipelines

## Workflow

When this skill is activated:

### 1. Understand Context
- Identify the specific testing task or requirement
- Determine which standards documents are most relevant
- Check existing project Jest configuration

### 2. Apply Standards
- Reference appropriate standards documents for guidance
- Follow Jest configuration patterns from jest-configuration.md
- Organize test files according to test-structure.md
- Apply testing patterns from testing-patterns.md
- Ensure coverage meets thresholds from coverage-standards.md

### 3. Quality Assurance
- Run tests to verify they execute correctly
- Check coverage reports meet 80% thresholds
- Verify mocks are properly configured
- Ensure tests are isolated and independent
- Validate test naming and organization

### 4. Documentation
- Document complex mocking strategies with clear comments
- Explain non-obvious test setup or configuration
- Note any project-specific test patterns
- Update README if adding new test utilities

## Tool Access

This skill provides access to Jest testing standards through:
- Read tool for accessing standards documents
- Standards documents use Markdown format for compatibility
- All standards are self-contained within this skill
- Cross-references between standards use relative paths

## Integration Notes

### Related Skills
For comprehensive JavaScript development, this skill works with:
- cui-javascript skill - Core JavaScript patterns and code quality
- cui-css skill - CSS testing patterns (if applicable)
- Other testing skills (E2E testing to be provided in separate skill)

### Build Integration
Jest testing integrates with:
- npm for package management and test execution
- Maven frontend-maven-plugin for build automation
- Jest CLI for test execution and coverage reporting
- Babel for ES module transformation

### Quality Tools
Test quality is enforced through:
- Jest framework for test execution
- @testing-library/jest-dom for enhanced DOM assertions
- Coverage reports for quality gates
- ESLint jest plugin for test code quality

## Best Practices

When writing Jest tests in CUI projects:

1. **Meet coverage thresholds** - 80% minimum for all metrics
2. **Use jsdom environment** for DOM and component testing
3. **Mock external dependencies** - Lit, DevUI, and other frameworks
4. **Follow AAA pattern** - Arrange, Act, Assert for clarity
5. **Keep tests isolated** - Independent, no shared state
6. **Organize logically** - Group related tests with describe blocks
7. **Use descriptive names** - Test names explain expected behavior
8. **Setup properly** - Use jest.setup.js and jest.setup-dom.js for global config

## Workflows

### Workflow: Analyze Coverage

Analyzes existing test coverage reports (Jest/Istanbul JSON or LCOV format) and returns structured coverage data.

**When to use**: After running tests with coverage to identify low-coverage areas and uncovered code.

**Steps**:

1. **Locate coverage report**
   - Look for `coverage/coverage-summary.json` (JSON format - preferred)
   - Or `coverage/lcov.info` (LCOV format - more detailed)

2. **Run coverage analysis script**

   Script: `pm-dev-frontend:cui-javascript-unit-testing` → `js-coverage.py`

   ```bash
   python3 .plan/execute-script.py pm-dev-frontend:cui-javascript-unit-testing:js-coverage analyze --report coverage/coverage-summary.json
   # Or for LCOV format:
   python3 .plan/execute-script.py pm-dev-frontend:cui-javascript-unit-testing:js-coverage analyze --report coverage/lcov.info --format lcov
   # With custom threshold:
   python3 .plan/execute-script.py pm-dev-frontend:cui-javascript-unit-testing:js-coverage analyze --report coverage/coverage-summary.json --threshold 80
   ```

3. **Process results**
   - Review `overall_coverage` metrics (lines, statements, functions, branches)
   - Identify files in `low_coverage_files` array (below threshold)
   - Note files with CRITICAL severity (< 50% coverage)
   - Check `uncovered_lines` for specific areas needing tests

**JSON Output Contract**:
```json
{
  "status": "success",
  "data": {
    "report_format": "JSON",
    "overall_coverage": {
      "line_coverage": 85.5,
      "statement_coverage": 84.8,
      "function_coverage": 90.1,
      "branch_coverage": 78.2
    },
    "by_file": [...],
    "low_coverage_files": [
      {"file": "src/utils.js", "coverage": 45.2, "severity": "CRITICAL", "uncovered_lines": [12, 34]}
    ]
  },
  "metrics": {
    "total_files": 45,
    "files_with_good_coverage": 38,
    "files_with_low_coverage": 7,
    "threshold": 80
  }
}
```

**Error handling**:
- Script returns `status: "error"` if report not found
- Supported formats: JSON (coverage-summary.json), LCOV (lcov.info)
