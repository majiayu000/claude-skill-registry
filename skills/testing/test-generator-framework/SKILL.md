---
name: test-generator-framework
description: Generic test generation framework supporting multiple languages and testing frameworks
license: Apache-2.0
compatibility: opencode
metadata:
  audience: developers
  workflow: testing-framework
---

## What I do

I provide a generic test generation framework that can be adapted for multiple languages and testing frameworks:

1. **Analyze Codebase**: Scan source code to identify functions, classes, modules, and components that need testing
2. **Detect Testing Framework**: Identify and configure the appropriate testing framework (Jest, Vitest, Pytest, etc.)
3. **Detect Package Manager**: Determine package manager (npm, yarn, pnpm, Poetry, pip) and build tools
4. **Generate Test Scenarios**: Create comprehensive test scenarios including:
   - Happy paths (normal operation)
   - Edge cases (boundary conditions)
   - Error handling (exceptions and failures)
   - Input validation
   - State management
   - User interactions (for UI components)
5. **Prompt User Confirmation**: Display all generated scenarios and ask for user approval before proceeding
6. **Create Test Files**: Generate test files with proper structure, imports, and assertions
7. **Verify Executability**: Run tests with appropriate command to ensure they work

## When to use me

Use this framework when:
- You need to create a new test generation skill for a specific language/framework
- You want to standardize test generation across multiple projects
- You're building a language-specific test generator (e.g., for Next.js, Python, React, etc.)
- You need a consistent test scenario generation approach

This is a **framework skill** - it provides the foundational workflow that other skills extend for specific languages/frameworks.

## Core Workflow Steps

### Step 1: Analyze Source Code

**Language-agnostic detection patterns:**
- Use glob patterns to find source files (exclude test files)
- Identify functions, classes, modules, components
- Detect import statements and dependencies
- Analyze export patterns

```bash
# Generic file discovery (adapt patterns per language)
<glob_pattern> --exclude "**/*test*.<ext>" --exclude "**/test/**/*"
```

### Step 2: Detect Testing Framework

**Framework Detection Logic:**

| Language | Framework Detection | Command |
|----------|-------------------|----------|
| JavaScript/TypeScript | Check package.json for jest/vitest | `grep -E "(jest|vitest)" package.json` |
| Python | Check pyproject.toml/requirements.txt for pytest | `grep pytest pyproject.toml` or `grep pytest requirements.txt` |
| Ruby | Check Gemfile for rspec/minitest | `grep -E "(rspec|minitest)" Gemfile` |
| Go | Check go.mod for testing | N/A (built-in testing) |

**Framework Configuration:**
```bash
# Detect test framework
if [ -f "package.json" ]; then
  if grep -q "vitest" package.json; then
    TEST_FRAMEWORK="vitest"
    TEST_CMD="npm run test"
  elif grep -q "jest" package.json; then
    TEST_FRAMEWORK="jest"
    TEST_CMD="npm run test"
  fi
elif [ -f "pyproject.toml" ]; then
  if grep -q "pytest" pyproject.toml; then
    TEST_FRAMEWORK="pytest"
    TEST_CMD="poetry run pytest"
  fi
fi
```

### Step 3: Detect Package Manager

**Package Manager Detection:**

| Language | Manager | Detection | Run Command |
|----------|-----------|------------|-------------|
| JavaScript/TypeScript | npm | `package-lock.json` exists | `npm run <script>` |
| JavaScript/TypeScript | yarn | `yarn.lock` exists | `yarn <script>` |
| JavaScript/TypeScript | pnpm | `pnpm-lock.yaml` exists | `pnpm run <script>` |
| Python | Poetry | `pyproject.toml` exists | `poetry run <script>` |
| Python | pip | `requirements.txt` exists | `python -m <script>` or `<script>` |

**Poetry Detection for Python:**
```bash
if command -v poetry &>/dev/null && [ -f pyproject.toml ]; then
  USE_POETRY=true
  TEST_CMD="poetry run pytest"
else
  USE_POETRY=false
  TEST_CMD="pytest"
fi
```

### Step 4: Generate Test Scenarios

**Universal Scenario Categories:**

#### Happy Path Scenarios
- Normal inputs return expected outputs
- Common use cases work correctly
- Default behavior is as specified

#### Edge Case Scenarios
- Empty inputs (empty string, empty list, None/null)
- Boundary values (0, 1, -1, MAX, MIN)
- Single-item collections
- Maximum allowed values

#### Error Handling Scenarios
- Invalid data types
- Out of range values
- Missing required parameters
- Invalid formats (email, URL, file paths)
- Permission errors
- Network errors (for I/O)

#### State Management Scenarios (for components/classes)
- Initial state is correct
- State updates after actions
- Multiple state transitions
- Reset functionality
- Cleanup on unmount

#### User Interaction Scenarios (for UI components)
- Click events
- Form submissions
- Keyboard navigation
- Input changes
- Hover/focus events

**Scenario Generation Template:**
```
For each [function/class/component]:
  1. Identify input parameters and return values
  2. Determine normal behavior (happy path)
  3. List edge cases based on input types
  4. Identify error conditions
  5. Check for state management or user interactions
```

### Step 5: Display Scenarios for Confirmation

**User Confirmation Template:**
```
📋 Generated Test Scenarios for <file_name>

**Type:** <Component | Function | Class>
**Item:** <Item Name>

**Scenarios:**
1. Happy Path: <description>
   - Expected: <result>
2. Edge Case: <description>
   - Expected: <result>
3. Error Case: <description>
   - Expected: <error>
4. Additional Scenario: <description>

**Total Scenarios:** <number>
**Estimated Test Lines:** <number>

**Framework Detected:** <Jest | Vitest | Pytest | Other>
**Test Command:** <appropriate command>
**Package Manager:** <npm | yarn | pnpm | Poetry | pip>

Are these scenarios acceptable? (y/n/suggest)
```

Wait for user response:
- **y**: Proceed to create test files
- **n**: Ask for modifications or cancel
- **suggest**: Ask user to add/remove scenarios

### Step 6: Create Test Files

**Test File Structure Template:**

```<language>
/**
 * Test suite for <ItemName>
 * Generated by <skill-name> skill
 */

// Framework-specific imports
import { describe, it, expect } from '<framework>'
import { <ItemName> } from './<fileName>'

describe('<ItemName>', () => {
  // Happy path tests
  describe('Happy Path', () => {
    it('works with valid inputs', () => {
      // Test implementation
    })
  })

  // Edge case tests
  describe('Edge Cases', () => {
    it('handles empty input', () => {
      // Test implementation
    })

    it('handles boundary values', () => {
      // Test implementation
    })
  })

  // Error handling tests
  describe('Error Handling', () => {
    it('throws error for invalid input', () => {
      // Test implementation
    })
  })

  // State/interaction tests (if applicable)
  describe('State Management', () => {
    it('updates state correctly', () => {
      // Test implementation
    })
  })
})
```

### Step 7: Verify Executability

**Universal Verification Pattern:**

```bash
# Run tests with appropriate command
<test_command> <test_files>

# Verify output:
# - No import errors
# - Tests are discoverable
# - Tests execute (even if they fail)
# - Test results are reported

# Example outputs:
# Jest: PASS <number> tests
# Vitest: ✓ <number> tests
# Pytest: <number> passed
```

**Verification Checklist:**
- [ ] Test files created in correct location
- [ ] File naming follows framework conventions
- [ ] Imports resolve correctly
- [ ] Tests are discoverable by framework
- [ ] Tests can be executed
- [ ] No syntax errors

### Step 8: Display Summary

**Summary Template:**
```
✅ Test files created successfully!

**Test Files Created:**
- <test_file1> (<number> tests)
- <test_file2> (<number> tests)

**Total Tests Generated:** <number>

**Test Categories:**
- Happy path: <number>
- Edge cases: <number>
- Error handling: <number>
- State/interactions: <number>

**Framework:** <Jest | Vitest | Pytest | Other>
**Test Command:** <command>
**Package Manager:** <npm | yarn | pnpm | Poetry | pip>

**To run tests:**
<test_command>

**Next Steps:**
1. Review generated test files
2. Update test data and expected values
3. Run tests to verify they pass
4. Add any missing scenarios
5. Update snapshots (if applicable)
```

## Scenario Generation Rules

### Happy Path Tests
- Use realistic, valid inputs
- Verify expected outputs
- Test common use cases
- Include multiple valid input combinations

### Edge Case Tests
- Test boundary values (0, 1, -1, max, min)
- Empty strings, empty lists, empty dictionaries
- None/undefined/null values
- Single-character strings, single-item lists
- Maximum/minimum allowed values

### Error Handling Tests
- Invalid data types
- Out of range values
- Missing required parameters
- Invalid file paths or URLs
- Network errors (for I/O operations)
- Permission errors (for file operations)

### State Management Tests
- Initial state is correct
- State updates after actions
- Multiple state transitions
- Reset functionality works
- Cleanup functions execute

### User Interaction Tests
- Click events trigger callbacks
- Form submissions work correctly
- Keyboard navigation functions
- Input changes update state
- Hover/focus events fire

## Test File Naming Conventions

| Framework | Naming Pattern | Example |
|------------|----------------|----------|
| Jest | `<Component>.test.tsx` or `<Component>.spec.tsx` | Button.test.tsx |
| Vitest | `<Component>.test.tsx` or `<Component>.spec.tsx` | Button.test.tsx |
| Pytest | `test_<module>.py` or `<module>_test.py` | test_user.py |
| RSpec | `<module>_spec.rb` | user_spec.rb |
| Go testing | `<module>_test.go` | user_test.go |

## Best Practices

- **Test Organization**: Keep tests in a `tests/` or `__tests__/` directory
- **Naming**: Use framework-specific naming conventions
- **Fixtures**: Use framework-specific fixtures for common setup
- **Parametrization**: Use parametrized tests for similar test cases
- **Clear Messages**: Add descriptive messages to assertions
- **Isolation**: Each test should be independent and can run alone
- **Coverage**: Aim for 80%+ code coverage
- **Fast Tests**: Keep unit tests fast (< 0.1s each for unit tests)
- **Readable**: Test names should describe what is being tested
- **Arrange-Act-Assert**: Structure tests in AAA pattern
- **Framework Detection**: Always detect framework from project files
- **User Confirmation**: Always show scenarios before creating files

## Common Issues

### Framework Not Detected
**Issue**: Unable to determine testing framework

**Solution**: Check for framework-specific configuration files:
- JavaScript/TypeScript: `package.json`, `jest.config.js`, `vitest.config.ts`
- Python: `pyproject.toml`, `pytest.ini`, `setup.cfg`

### Package Manager Not Detected
**Issue**: Unable to determine which command to use

**Solution**: Check for lock files:
- `package-lock.json` → `npm`
- `yarn.lock` → `yarn`
- `pnpm-lock.yaml` → `pnpm`
- `pyproject.toml` → `poetry run` (if Poetry installed) or `pip`

### Import Errors
**Issue**: Cannot import module to test

**Solution**: Ensure correct import paths and that modules are exported:
```bash
# Python: Add source to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# JavaScript/TypeScript: Check exports in package.json
grep '"exports"' package.json
```

### Tests Not Discovered
**Issue**: Framework doesn't find test files

**Solution**: Ensure correct naming and location:
- Check framework's default test patterns
- Verify test files are in correct directory
- Check file naming follows conventions

## Troubleshooting Checklist

Before generating tests:
- [ ] Source files exist and are syntactically correct
- [ ] Framework configuration file exists
- [ ] Package manager is detected
- [ ] Project structure follows conventions

After generating tests:
- [ ] Test files are created in correct location
- [ ] Test files follow naming conventions
- [ ] All imports resolve correctly
- [ ] Tests are discoverable by framework
- [ ] Tests can be executed
- [ ] No syntax errors
- [ ] Test coverage is adequate

## Relevant Skills

Language-specific test generators that use this framework:
- `nextjs-unit-test-creator`: For Next.js/React testing (Jest/Vitest)
- `python-pytest-creator`: For Python testing (Pytest)

Framework-specific utilities:
- `linting-workflow`: For ensuring code quality before testing
