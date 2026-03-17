---
name: create-qa-task
description: Use to create QA task documents. Generates test specifications and validation requirements for QA team.
version: 1.0.0
---
<!-- Powered by Prism Coreâ„¢ -->

# create-qa-task

Generate a test specification document for the QA agent to implement based on validated customer issue.

## Quick Start

1. Review validation results (Playwright report, screenshots, errors)
2. Create test specification with objective and scope
3. Define test scenarios (happy path, edge cases, error conditions)
4. Specify test data and environment requirements
5. Package for QA agent handoff

## Purpose

Create a comprehensive test specification that describes WHAT to test, not HOW to implement it. The QA agent will use this specification to write actual test code.

## SEQUENTIAL Task Execution

### 1. Review Validation Results
```yaml
inputs:
  - Issue validation report from Playwright
  - Screenshots and error evidence
  - Reproduction steps documented
  - Root cause investigation findings
```

### 2. Create Test Specification Document

```yaml
test_specification:
  ticket_id: "ISSUE-{number}"
  priority: "P0|P1|P2|P3"
  
  test_objective: |
    Ensure that {specific functionality} works correctly
    when {user action} under {conditions}.
    
  test_scope:
    in_scope:
      - {Feature/component to test}
      - {User workflows affected}
      - {Error conditions to verify}
    out_of_scope:
      - {What NOT to test}
      - {Unrelated features}
  
  test_scenarios:
    - scenario_1:
        name: "Happy path - {description}"
        given: "{Initial state}"
        when: "{User action}"
        then: "{Expected result}"
        
    - scenario_2:
        name: "Error case - {description}"
        given: "{Initial state with issue}"
        when: "{Action that triggers issue}"
        then: "{Issue should not occur}"
        
    - scenario_3:
        name: "Edge case - {description}"
        given: "{Boundary condition}"
        when: "{Edge case action}"
        then: "{Graceful handling}"
```

### 3. Define Test Requirements

```yaml
test_requirements:
  test_type: "E2E Integration"
  
  environment:
    - Test database with sample data
    - Authentication enabled
    - External services mocked/containerized
    
  test_data:
    - User accounts with various roles
    - Sample transactions/records
    - Edge case data sets
    
  assertions_needed:
    - Response status codes
    - Data integrity checks
    - UI state validations
    - Performance thresholds
    
  coverage_goals:
    - All reported issue scenarios
    - Related functionality
    - Regression prevention
```

### 4. Handoff Documentation

```markdown
# QA Task: Test Implementation for Issue #{ticket}

## Issue Summary
**Customer Report:** {brief description}
**Validation Status:** Reproduced via Playwright
**Root Cause:** {identified cause from investigation}

## Test Implementation Request

### Priority: {P0|P1|P2|P3}
### Due Date: {sprint deadline}

### Test Scenarios to Implement

1. **Regression Test for Original Issue**
   - Must reproduce the exact customer scenario
   - Should FAIL with current code
   - Should PASS after Dev fix applied

2. **Related Test Coverage**
   - Test variations of the issue
   - Test error boundaries
   - Test data edge cases

### Test Location Recommendation
- Suggested file: `Integration.Tests/CustomerIssues/Issue{number}Tests.cs`
- Test collection: `{appropriate collection}`
- Use existing fixtures where possible

### Evidence to Include in Tests
- Capture screenshots at failure points
- Log console errors
- Record response times
- Validate data state

### Acceptance Criteria
- [ ] Test reproduces customer issue (fails before fix)
- [ ] Test passes after Dev implements fix
- [ ] No flaky test behaviors
- [ ] Clear test documentation
- [ ] Follows project test conventions

## Handoff Notes
- Validation evidence attached: {screenshots/logs}
- Related issues: {linked tickets}
- Contact Support team for clarification if needed
```

### 5. Task Tracking

```yaml
qa_task_metadata:
  assigned_to: "QA Agent"
  created_by: "Support Agent"
  created_date: "{current_date}"
  
  dependencies:
    - "Dev task for fix implementation"
    - "Environment setup if needed"
    
  deliverables:
    - "Failing E2E integration test"
    - "Test documentation"
    - "Coverage report"
    
  success_metrics:
    - "Test catches the reported issue"
    - "Test maintainable and clear"
    - "No false positives"
```

## Success Criteria
- [ ] Complete test specification created
- [ ] All scenarios documented clearly
- [ ] Requirements defined without implementation details
- [ ] Handoff package ready for QA agent
- [ ] Task tracked in system

## Output
- Test specification document
- QA task assignment
- Link to validation evidence
- Clear acceptance criteria for QA team
