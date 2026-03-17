---
name: harness-tester
version: 1.0.0
description: Testing orchestrator for autonomous harness. Runs comprehensive tests (unit, integration, E2E), coordinates with validation systems, and reports results to Archon. Supports browser automation via Playwright MCP. Use when verifying features, running test suites, or validating code changes.
---

# Harness Testing Skill

Specialized testing skill for the autonomous harness system. Runs comprehensive tests and reports results to Archon for tracking.

## Triggers

Use this skill when:
- Verifying features in harness workflow
- Running comprehensive test suites
- Performing E2E browser testing
- Validating code changes
- Keywords: harness test, verify feature, run tests, test suite, e2e testing, browser testing, validation

## Core Mission

Provide thorough testing and verification of features:
1. **Run test suites** - Unit, integration, and E2E tests
2. **Browser automation** - Test UI features via Playwright MCP
3. **Report results** - Update Archon tasks with test status
4. **Identify issues** - Document any failures clearly

---

## Testing Modes

### Mode 1: Verify Specific Feature
Test a specific feature by task ID.

### Mode 2: Run Full Test Suite
Run all tests in the project.

### Mode 3: Health Check
Quick validation that the project builds and basic tests pass.

### Mode 4: E2E Browser Testing
UI testing with browser automation.

---

## Testing Protocol

### STEP 1: Determine Test Scope

Identify:
- **Target**: Specific feature or full suite?
- **Task ID**: Which Archon task to update?
- **Test Type**: Unit, integration, E2E, or all?

### STEP 2: Read Harness Configuration

```bash
cat .harness/config.json
```

```python
# Get project configuration
config = find_documents(
    project_id=PROJECT_ID,
    document_type="guide",
    query="Harness Configuration"
)

testing_strategy = config["content"]["testing_strategy"]
# Could be: "unit", "unit+integration", "full-e2e", "manual"
```

### STEP 3: Run Appropriate Tests

#### Unit Tests

```bash
# Node.js / TypeScript
npm test -- --coverage

# Python
pytest tests/unit/ -v --cov

# Go
go test ./... -v -cover

# Rust
cargo test --lib

# .NET
dotnet test --filter Category=Unit
```

#### Integration Tests

```bash
# Node.js
npm run test:integration

# Python
pytest tests/integration/ -v

# Or with specific database/services
docker-compose up -d test-db
npm run test:integration
docker-compose down
```

#### E2E Browser Tests

For web applications, use Playwright MCP for browser automation:

```python
# Using Playwright MCP
mcp__playwright__browser_navigate(url="http://localhost:3000")
mcp__playwright__browser_snapshot()

# Test user flow
mcp__playwright__browser_type(
    element="Email input",
    ref="input[name='email']",
    text="test@example.com"
)
mcp__playwright__browser_type(
    element="Password input",
    ref="input[name='password']",
    text="testpassword123"
)
mcp__playwright__browser_click(
    element="Login button",
    ref="button[type='submit']"
)
mcp__playwright__browser_wait_for(text="Dashboard")

# Verify result
snapshot = mcp__playwright__browser_snapshot()
# Check for expected elements
```

### STEP 4: Collect and Analyze Results

Parse test output to determine:
- Total tests run
- Tests passed
- Tests failed
- Test coverage (if available)
- Specific failure messages

### STEP 5: Report Results to Archon

```python
# Update task with test results
manage_task("update",
    task_id="<TASK_ID>",
    description=f"""[ORIGINAL_DESCRIPTION]

---
## Test Results (Verified by harness-tester)
**Timestamp**: {timestamp}
**Status**: {"PASSING" if all_passed else "FAILING"}

### Summary
| Type | Passed | Failed | Total |
|------|--------|--------|-------|
| Unit | {unit_passed} | {unit_failed} | {unit_total} |
| Integration | {int_passed} | {int_failed} | {int_total} |
| E2E | {e2e_passed} | {e2e_failed} | {e2e_total} |

### Coverage
- Statements: {stmt_coverage}%
- Branches: {branch_coverage}%
- Functions: {func_coverage}%

{"### Failures" if failures else ""}
{failure_details if failures else ""}

### Verification
- [x] Unit tests executed
- [x] Integration tests executed
- [x] E2E tests executed
- [x] Results logged to Archon
"""
)
```

### STEP 6: Update Session Notes (if significant)

Only update session notes for failures or important findings:

```python
if failures:
    notes = find_documents(project_id=PROJECT_ID, query="Session Notes")

    # Add test failure note
    manage_document("update",
        project_id=PROJECT_ID,
        document_id=notes["id"],
        content={
            ...notes["content"],
            "blockers": notes["content"]["blockers"] + [
                {
                    "type": "test_failure",
                    "task_id": TASK_ID,
                    "feature": FEATURE_NAME,
                    "details": failure_summary,
                    "timestamp": timestamp
                }
            ]
        }
    )
```

---

## Test Patterns by Project Type

### Web Application (React/Vue/Next.js)

```javascript
// Unit test pattern
describe('Component', () => {
  it('should render correctly', () => {
    render(<Component />);
    expect(screen.getByText('Expected')).toBeInTheDocument();
  });
});

// Integration test pattern
describe('API Integration', () => {
  it('should fetch data', async () => {
    const response = await api.getData();
    expect(response.status).toBe(200);
  });
});
```

```bash
# Run commands
npm test                    # Unit tests
npm run test:integration    # Integration
npx playwright test         # E2E
```

### Python API (FastAPI/Flask)

```python
# Unit test pattern
def test_service_function():
    result = service.process(input_data)
    assert result == expected

# Integration test pattern
def test_api_endpoint(client):
    response = client.post("/api/endpoint", json=data)
    assert response.status_code == 200
```

```bash
# Run commands
pytest tests/unit/ -v
pytest tests/integration/ -v
pytest tests/e2e/ -v
```

### CLI Application

```bash
# Test CLI commands
./mycli --help | grep "Usage"
./mycli process input.txt | diff - expected_output.txt
echo $? # Should be 0
```

---

## Output Format

### Success Output

```markdown
## Tests Passed

**Feature**: [FEATURE_NAME]
**Task**: [TASK_ID]

### Results
| Type | Status | Count |
|------|--------|-------|
| Unit | Pass | 15/15 |
| Integration | Pass | 8/8 |
| E2E | Pass | 3/3 |

### Coverage
- Statements: 87%
- Branches: 72%
- Functions: 91%

**Archon Updated**: Yes
```

### Failure Output

```markdown
## Tests Failed

**Feature**: [FEATURE_NAME]
**Task**: [TASK_ID]

### Results
| Type | Status | Count |
|------|--------|-------|
| Unit | Pass | 14/15 |
| Integration | Fail | 6/8 |
| E2E | Skip | 0/3 |

### Failures

#### Integration Test: `test_user_creation`
```
AssertionError: Expected status 201, got 400
  at tests/integration/user.test.ts:45

Possible causes:
- Validation logic changed
- Database constraint not met
- Missing required field
```

### Recommended Actions
1. Check validation rules in `src/services/user.ts`
2. Verify database schema matches model
3. Review request payload structure

**Archon Updated**: Yes (marked as failing)
```

---

## Browser Testing Guidelines

When running E2E browser tests:

### Do:
- Test as a real user would (clicks, typing)
- Take snapshots at key verification points
- Wait for elements before interacting
- Test error states and edge cases
- Verify both functionality AND appearance

### Don't:
- Use JavaScript evaluation to bypass UI
- Skip visual verification
- Test only happy paths
- Assume elements are immediately available
- Ignore console errors

### Common Browser Test Patterns

```python
# Login flow test
async def test_login():
    await navigate("http://localhost:3000/login")
    await fill("input[name='email']", "user@test.com")
    await fill("input[name='password']", "password123")
    await click("button[type='submit']")
    await wait_for_text("Dashboard")
    snapshot = await take_snapshot()
    assert "Welcome" in snapshot
    return {"passed": True}

# Form validation test
async def test_form_validation():
    await navigate("http://localhost:3000/signup")
    await click("button[type='submit']")  # Submit empty form
    await wait_for_text("Email is required")
    snapshot = await take_snapshot()
    assert "Email is required" in snapshot
    assert "Password is required" in snapshot
    return {"passed": True}
```

---

## Critical Rules

1. **NEVER modify tests to make them pass** - Fix code, not tests
2. **ALWAYS report results to Archon** - Even if tests pass
3. **ALWAYS include failure details** - Specific error messages
4. **RUN ALL relevant test types** - Based on configuration
5. **DOCUMENT flaky tests** - Note if a test is intermittent
6. **BLOCK on failures** - Don't allow completion without passing tests
