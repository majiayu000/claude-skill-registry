---
name: create-failing-test
description: Use to create failing tests before implementing features (TDD approach). Ensures test-first development workflow.
version: 1.0.0
---
<!-- Powered by PRISMâ„¢ Core -->

# Create Failing Test Task

## When to Use

- Before implementing a new feature (TDD approach)
- When documenting a customer-reported bug
- When QA needs exact reproduction steps
- When validating issue before assigning to Dev
- When creating acceptance criteria for fixes

## Quick Start

1. Gather evidence from validation (screenshots, errors, steps)
2. Define test preconditions (data, environment, config)
3. Write exact reproduction steps
4. Define assertions (expected vs actual behavior)
5. Package test specification for Dev/QA handoff

## Purpose

Document a reproducible failing test case that demonstrates the customer issue, providing Dev and QA teams with exact steps and assertions to verify the bug and confirm the fix.

## Context

Support agents validate issues but CANNOT write test code. This task creates a detailed test specification with exact reproduction steps that:
- Dev can use to confirm they see the issue
- QA can implement as automated test
- Serves as acceptance criteria for the fix

## SEQUENTIAL Task Execution

### 1. Gather Evidence from Validation

```yaml
validation_data:
  issue_id: "{ticket_number}"
  
  reproduction_evidence:
    - Playwright validation results
    - Screenshots showing issue
    - Console errors captured
    - Network failures logged
    - Exact user steps taken
    
  environment:
    - Browser and version
    - User role/permissions
    - Data state required
    - Configuration settings
```

### 2. Define Test Preconditions

```yaml
test_setup:
  data_requirements:
    - User account type needed
    - Specific data records required
    - System configuration state
    - External service dependencies
    
  initial_state:
    - URL to start from
    - Login credentials needed
    - Features enabled/disabled
    - Database seed data
```

### 3. Document Exact Steps to Reproduce

```yaml
reproduction_steps:
  - step: 1
    action: "Navigate to {specific URL}"
    expected: "Page loads successfully"
    actual: "Page loads successfully"
    
  - step: 2
    action: "Click on {specific element}"
    element_selector: "#button-id or .class-name"
    expected: "Modal opens"
    actual: "Modal opens"
    
  - step: 3
    action: "Enter '{value}' in {field}"
    element_selector: "input[name='fieldname']"
    expected: "Field accepts input"
    actual: "Field accepts input"
    
  - step: 4
    action: "Submit form"
    element_selector: "button[type='submit']"
    expected: "Success message appears"
    actual: "ERROR: {exact error message}"
    
  failure_point:
    step_number: 4
    expected_behavior: "Form submits and shows success"
    actual_behavior: "Form fails with error: {message}"
    error_details:
      - Console error text
      - Network response code
      - Stack trace if available
```

### 4. Define Assertions for Test

```yaml
test_assertions:
  should_pass_but_fails:
    - description: "Form submission should succeed"
      assertion: "expect(successMessage).toBeVisible()"
      current_result: "FAILS - Error message appears instead"
      
    - description: "API should return 200"
      assertion: "expect(response.status).toBe(200)"
      current_result: "FAILS - Returns 500"
      
    - description: "Data should be saved"
      assertion: "expect(database.record).toExist()"
      current_result: "FAILS - No record created"
      
  regression_prevention:
    - "Test should fail before fix applied"
    - "Test should pass after fix applied"
    - "Test should remain in suite permanently"
```

### 5. Create Test Specification Document

Generate failing-test-{issue_id}.md:

```markdown
# Failing Test: {Issue Title}

## Issue ID: {ISSUE-XXX}
## Priority: {P0|P1|P2|P3}
## Status: Reproduces Consistently

## Test Objective
Verify that {specific functionality} works correctly when {conditions}.
Currently FAILS due to {brief description of bug}.

## Preconditions
- Environment: {staging|production}
- User: {role/permissions}
- Data: {required records}
- Configuration: {settings}

## Steps to Reproduce
1. {Detailed step with selectors}
2. {Detailed step with selectors}
3. {Detailed step with selectors}
4. **FAILURE POINT:** {Where it breaks}

## Expected vs Actual
- **Expected:** {What should happen}
- **Actual:** {What actually happens}
- **Error:** {Exact error message/behavior}

## Test Assertions
```javascript
// Pseudocode for QA implementation
test('Customer Issue {ID}: {Title}', () => {
  // Setup
  {setup_steps}
  
  // Action
  {action_steps}
  
  // This assertion currently FAILS
  expect({element}).{assertion}
  
  // After fix, this should PASS
});
```

## Evidence
- Screenshot: {link_to_screenshot}
- Console Error: {error_text}
- Network Log: {request/response}

## Definition of Done
- [ ] Test fails consistently before fix
- [ ] Test passes after fix applied
- [ ] Test added to regression suite
- [ ] No similar issues in related areas
```

### 6. Handoff Package

```yaml
deliverables:
  for_dev_team:
    - Exact reproduction steps
    - Failing assertions to verify
    - Environment requirements
    - Expected behavior after fix
    
  for_qa_team:
    - Test specification document
    - Selectors and assertions
    - Test data requirements
    - Regression suite placement
    
  tracking:
    - Link test to issue ticket
    - Add to test coverage matrix
    - Update test documentation
```

## Success Criteria

- [ ] Test case reproduces the issue 100% of the time
- [ ] Steps are detailed enough for automation
- [ ] Assertions clearly define pass/fail
- [ ] Dev can use to verify they see the issue
- [ ] QA can implement without clarification
- [ ] Test prevents regression after fix

## Output

- failing-test-{issue_id}.md specification
- Links to validation evidence
- Clear handoff to Dev and QA teams
- Acceptance criteria for fix verification
