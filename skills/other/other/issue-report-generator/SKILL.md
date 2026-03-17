---
name: issue-report-generator
description: Automatically generate clear, actionable issue reports from failing tests and repository analysis. Analyze test failures to understand expected vs. actual behavior, identify affected code components, and produce well-structured Markdown reports suitable for GitHub Issues or similar trackers. Use when a test fails, when debugging issues, or when the user asks to create an issue report, generate a bug report, or document a test failure.
---

# Issue Report Generator

## Overview

Generate comprehensive, developer-friendly issue reports from failing tests. Analyze test failures, identify affected code, infer root causes when possible, and produce structured Markdown reports ready for issue tracking systems.

## Report Generation Workflow

### Step 1: Analyze the Failing Test

Understand what the test is checking and why it fails:

1. **Identify the test:**
   - Test file path
   - Test class/function name
   - Test method name

2. **Understand test intent:**
   - What functionality is being tested?
   - What is the expected behavior?
   - What assertions are being made?

3. **Analyze the failure:**
   - Exception type (if any)
   - Assertion failure details
   - Expected vs. actual values
   - Error messages
   - Stack trace

4. **Extract key information:**
   - Failure type (exception, assertion, timeout, etc.)
   - Failure location (file, line number)
   - Failure context (method calls, parameters)

### Step 2: Identify Affected Code Components

Locate the code related to the failure:

1. **From stack trace:**
   - Extract file paths
   - Extract class/method names
   - Extract line numbers
   - Identify the failure point

2. **From test code:**
   - Find the method/class being tested
   - Identify dependencies
   - Locate related components

3. **Code analysis:**
   - Read the failing code section
   - Understand the logic
   - Identify potential issues

4. **Record locations:**
   - Primary affected file(s)
   - Specific methods/functions
   - Line numbers or ranges

### Step 3: Infer Root Cause

Determine why the failure occurs (when possible):

1. **For exceptions:**
   - Which variable/object caused it?
   - Why is it null/invalid?
   - Where should it be initialized?
   - What condition triggers the exception?

2. **For assertion failures:**
   - Why does actual differ from expected?
   - What code produces the wrong value?
   - What condition causes the mismatch?
   - Is there a logic error?

3. **For timeouts:**
   - What operation is slow?
   - Is there an infinite loop?
   - Is there inefficient algorithm?
   - Are there blocking operations?

4. **For integration failures:**
   - What external system failed?
   - What's the error from that system?
   - Is it configuration?
   - Is it connection?

5. **State uncertainty:**
   - If root cause is unclear, say so
   - Use "suspected," "likely," "appears to be"
   - Suggest areas for investigation

### Step 4: Generate Report Structure

Create the issue report with required sections:

1. **Title:**
   - Format: `[Exception/Issue] in [Component].[Method]`
   - Or: `[Feature] returns incorrect [result]`
   - Keep it concise (50-80 characters)
   - Make it descriptive

2. **Description:**
   - Brief summary of the issue
   - Context about when it occurs
   - Impact on functionality

3. **Steps to Reproduce:**
   - Test command to run
   - Or code snippet to execute
   - Minimal reproduction steps

4. **Expected Behavior:**
   - What should happen
   - Based on test assertions
   - Based on documentation

5. **Actual Behavior:**
   - What actually happens
   - Include error messages
   - Include stack traces
   - Include assertion failures

6. **Affected Code:**
   - File paths
   - Class/method names
   - Line numbers
   - Code snippets if helpful

7. **Analysis (optional):**
   - Suspected root cause
   - Why it happens
   - Suggested fix (if clear)

8. **Additional Context:**
   - Test details
   - Environment info
   - Related issues
   - Labels/severity

### Step 5: Format and Finalize

Produce the final Markdown report:

1. **Use proper Markdown:**
   - Headers for sections
   - Code blocks for code/errors
   - Lists for steps
   - Bold for emphasis

2. **Be precise:**
   - Use exact error messages
   - Include full stack traces
   - Reference specific locations
   - Use technical terminology

3. **Be clear:**
   - Developer-friendly language
   - Avoid vague descriptions
   - State facts, not opinions
   - Indicate uncertainty

4. **Be actionable:**
   - Provide reproduction steps
   - Identify affected code
   - Suggest investigation areas
   - Make it easy to fix

## Report Templates

For detailed templates and patterns, see [report_patterns.md](references/report_patterns.md).

### Quick Template Selection

| Failure Type | Template | Key Focus |
|--------------|----------|-----------|
| Exception | Exception-Based Bug | Exception type, location, null/invalid variable |
| Assertion failure | Assertion Failure Bug | Expected vs. actual, wrong value source |
| Timeout | Performance/Timeout Bug | Slow operation, bottleneck |
| Integration error | Integration Failure Bug | External system, error message, config |
| Regression | Regression Bug | Breaking commit, what changed |

## Examples

### Example 1: NullPointerException

**Input:**
- Test: `UserServiceTest.testAuthenticateNonExistentUser`
- Error: `NullPointerException at UserService.java:45`
- Stack trace provided

**Generated Report:**
```markdown
# NullPointerException in UserService.authenticate() when user not found

## Description
A `NullPointerException` is thrown in `UserService.authenticate()` when attempting to authenticate a user that doesn't exist in the database. This causes the authentication endpoint to return a 500 error instead of properly handling the missing user case.

## Steps to Reproduce
1. Run test: `mvn test -Dtest=UserServiceTest#testAuthenticateNonExistentUser`
2. Or call: `userService.authenticate("nonexistent@example.com", "password")`

## Expected Behavior
The method should return an authentication failure result (e.g., `AuthResult.FAILED`) or throw a specific `UserNotFoundException`, not a `NullPointerException`.

## Actual Behavior
```
java.lang.NullPointerException
  at com.example.UserService.authenticate(UserService.java:45)
  at com.example.AuthController.login(AuthController.java:23)
  at com.example.UserServiceTest.testAuthenticateNonExistentUser(UserServiceTest.java:67)
```

## Affected Code
- **File:** `src/main/java/com/example/UserService.java`
- **Method:** `UserService.authenticate`
- **Line:** 45

**Code at line 45:**
```java
String hashedPassword = user.getPassword(); // user is null here
```

## Analysis
The exception occurs because the `user` object is null when the user lookup fails (line 42). The code attempts to call `user.getPassword()` without checking if the user exists.

**Suspected cause:** Missing null check after user lookup.

## Test Details
- Test file: `src/test/java/com/example/UserServiceTest.java`
- Test method: `testAuthenticateNonExistentUser`
```

### Example 2: Assertion Failure

**Input:**
- Test: `CalculatorTest.testDivision`
- Error: `AssertionError: expected 2.5 but got 2.0`

**Generated Report:**
```markdown
# Calculator.divide() returns integer instead of decimal result

## Description
The `Calculator.divide()` method returns `2.0` instead of the expected `2.5` when dividing 5 by 2. This indicates the method is performing integer division instead of floating-point division.

## Steps to Reproduce
1. Run test: `pytest tests/test_calculator.py::CalculatorTest::test_division`
2. Or execute:
```python
calc = Calculator()
result = calc.divide(5, 2)
# Returns 2.0, expected 2.5
```

## Expected Behavior
```python
assert calc.divide(5, 2) == 2.5
```

## Actual Behavior
```python
AssertionError: assert 2.0 == 2.5
  Expected: 2.5
  Actual: 2.0
```

## Affected Code
- **File:** `src/calculator.py`
- **Method:** `Calculator.divide`
- **Lines:** 15-16

**Current implementation:**
```python
def divide(self, a, b):
    return a / b  # Using integer division
```

## Analysis
The method performs integer division when both operands are integers. In Python 2 or when using `//` operator, this truncates the decimal part.

**Suspected cause:** Missing float conversion or using wrong division operator.

**Suggested fix:**
```python
def divide(self, a, b):
    return float(a) / float(b)
```

## Test Details
- Test file: `tests/test_calculator.py`
- Test method: `test_division`
```

### Example 3: Timeout

**Input:**
- Test: `DataProcessorTest.testLargeDataset`
- Error: `Test timeout after 30s`

**Generated Report:**
```markdown
# Performance issue: processLargeDataset() exceeds timeout

## Description
The `DataProcessor.processLargeDataset()` method takes longer than 30 seconds when processing 10,000 items, causing the test to timeout.

## Steps to Reproduce
1. Run test: `npm test -- DataProcessorTest.testLargeDataset`
2. Test processes 10,000 items

## Expected Behavior
Processing should complete within 30 seconds.

## Actual Behavior
Test times out after 30 seconds. Processing is incomplete.

## Affected Code
- **File:** `src/data_processor.js`
- **Method:** `DataProcessor.processLargeDataset`
- **Lines:** 45-60

**Suspected bottleneck (lines 50-55):**
```javascript
for (let i = 0; i < items.length; i++) {
  for (let j = 0; j < items.length; j++) {  // O(n²) nested loop
    if (items[i].id === items[j].relatedId) {
      // Process relationship
    }
  }
}
```

## Analysis
The performance issue appears to be caused by a nested loop with O(n²) complexity. With 10,000 items, this results in 100 million iterations.

**Suspected cause:** Inefficient algorithm using nested loops.

**Suggested optimization:** Use a hash map for O(n) lookup:
```javascript
const itemMap = new Map(items.map(item => [item.id, item]));
for (let item of items) {
  const related = itemMap.get(item.relatedId);
  if (related) {
    // Process relationship
  }
}
```

## Test Details
- Test file: `tests/data_processor.test.js`
- Test method: `testLargeDataset`
- Input size: 10,000 items
```

### Example 4: Integration Failure

**Input:**
- Test: `ApiTest.testGetUserEndpoint`
- Error: `Expected status 200, got 500`
- Response: `{"error": "Database connection failed"}`

**Generated Report:**
```markdown
# Database connection failure in GET /api/users endpoint

## Description
The `/api/users` endpoint returns a 500 error with message "Database connection failed" instead of returning user data.

## Steps to Reproduce
1. Run test: `pytest tests/test_api.py::ApiTest::test_get_user_endpoint`
2. Or make request: `GET http://localhost:8000/api/users`

## Expected Behavior
```
Status: 200 OK
Body: [{"id": 1, "name": "John"}, ...]
```

## Actual Behavior
```
Status: 500 Internal Server Error
Body: {"error": "Database connection failed"}

Stack trace:
  at DatabaseConnection.connect (db.js:23)
  at UserRepository.findAll (user_repository.js:15)
  at UserController.getUsers (user_controller.js:42)
```

## Affected Code
- **File:** `src/db.js`
- **Method:** `DatabaseConnection.connect`
- **Line:** 23

## Analysis
The database connection fails, likely due to:
1. Database server not running
2. Incorrect connection configuration
3. Missing environment variables

**Suspected cause:** Missing or incorrect `DATABASE_URL` environment variable.

## Environment
- Database: PostgreSQL
- Required env var: `DATABASE_URL`
- Expected format: `postgresql://user:pass@host:port/dbname`

## Test Details
- Test file: `tests/test_api.py`
- Test method: `test_get_user_endpoint`
```

## Constraints and Requirements

### MUST Requirements

1. **Evidence-based reporting:**
   - Only report what's in the test/code
   - Don't invent behavior
   - Don't claim fixes without evidence

2. **Precise language:**
   - Use exact error messages
   - Include full stack traces
   - Reference specific locations
   - Use technical terminology

3. **Clear uncertainty:**
   - Use "suspected," "likely," "appears to be"
   - State when root cause is unclear
   - Suggest investigation areas

4. **Complete information:**
   - Include all required sections
   - Provide reproduction steps
   - Document affected code
   - Include test details

### MUST NOT Requirements

1. **Don't invent:**
   - Don't create behavior not in test
   - Don't guess at functionality
   - Don't assume fixes

2. **Don't be vague:**
   - Avoid "something is wrong"
   - Avoid "the code doesn't work"
   - Avoid "fix the bug"

3. **Don't be judgmental:**
   - Avoid "badly written"
   - Avoid "obviously wrong"
   - State facts, not opinions

## Best Practices

1. **Be specific:** Reference exact files, methods, line numbers
2. **Be clear:** Use developer-friendly language
3. **Be honest:** Indicate uncertainty when appropriate
4. **Be actionable:** Provide steps to reproduce and investigate
5. **Be complete:** Include all relevant information
6. **Be concise:** Don't include irrelevant details
7. **Be formatted:** Use proper Markdown for readability

## Quality Checklist

Before finalizing a report:

- [ ] Title is concise and descriptive
- [ ] Description explains the issue clearly
- [ ] Steps to reproduce are provided
- [ ] Expected behavior is stated
- [ ] Actual behavior is documented
- [ ] Error messages/stack traces included
- [ ] Affected code locations specified
- [ ] Uncertainty is indicated where appropriate
- [ ] Language is developer-friendly
- [ ] Report is properly formatted in Markdown
- [ ] Report is ready to post to issue tracker

## Resources

- **Report patterns:** See [report_patterns.md](references/report_patterns.md) for comprehensive templates and examples
- **GitHub Issues:** https://docs.github.com/en/issues
- **Writing good bug reports:** Best practices for issue documentation
