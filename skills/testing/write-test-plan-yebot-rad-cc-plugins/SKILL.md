---
description: Create comprehensive test plans for features and changes
disable-model-invocation: false
---

# Write Test Plan

Create structured test plans that ensure quality and prevent regressions.

## When to Use

- Before implementing a new feature
- When planning a release
- After discovering a bug (to prevent regression)
- When onboarding someone to test a feature

## Used By

- QA Engineer (primary owner)
- Full-Stack Engineer (test implementation)
- Frontend Engineer (component testing)
- Backend Engineer (API testing)

---

## Test Plan Template

```markdown
# Test Plan: [Feature/Change Name]

**Author**: [Name]
**Date**: [Date]
**Status**: Draft | Ready | Executing | Complete
**Feature/PR**: [Link]

---

## Overview

### Feature Summary
[Brief description of what's being tested]

### Testing Scope
- **In Scope**: [What will be tested]
- **Out of Scope**: [What won't be tested, and why]

### Test Environment
- **Environment**: [Staging / Production / Local]
- **Test Data**: [Source of test data]
- **Dependencies**: [External services, mock requirements]

---

## Test Scenarios

### Happy Path Tests

| ID | Scenario | Steps | Expected Result | Priority |
|----|----------|-------|-----------------|----------|
| HP-1 | [Scenario name] | [Brief steps] | [Expected outcome] | P1 |
| HP-2 | [Scenario name] | [Brief steps] | [Expected outcome] | P1 |

### Edge Cases

| ID | Scenario | Steps | Expected Result | Priority |
|----|----------|-------|-----------------|----------|
| EC-1 | [Edge case] | [Steps] | [Expected outcome] | P2 |
| EC-2 | [Edge case] | [Steps] | [Expected outcome] | P2 |

### Error Cases

| ID | Scenario | Steps | Expected Result | Priority |
|----|----------|-------|-----------------|----------|
| ER-1 | [Error scenario] | [Steps] | [Expected error handling] | P1 |
| ER-2 | [Error scenario] | [Steps] | [Expected error handling] | P2 |

### Boundary Conditions

| ID | Scenario | Steps | Expected Result | Priority |
|----|----------|-------|-----------------|----------|
| BC-1 | [Boundary test] | [Steps] | [Expected outcome] | P2 |
| BC-2 | [Boundary test] | [Steps] | [Expected outcome] | P3 |

---

## Detailed Test Cases

### [HP-1] [Test Case Name]

**Preconditions:**
- [Required state/setup]

**Test Data:**
- [Specific data needed]

**Steps:**
1. [Detailed step 1]
2. [Detailed step 2]
3. [Detailed step 3]

**Expected Results:**
- [ ] [Verification point 1]
- [ ] [Verification point 2]
- [ ] [Verification point 3]

**Actual Results:**
[To be filled during execution]

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

## Test Data Requirements

### Required Test Accounts
| Account Type | Username | Purpose |
|-------------|----------|---------|
| Admin | test-admin | Admin functionality |
| Regular User | test-user | Standard flows |
| New User | (create) | First-time experience |

### Test Data Sets
| Data Set | Description | Location |
|----------|-------------|----------|
| [Set 1] | [Description] | [Location/script] |
| [Set 2] | [Description] | [Location/script] |

---

## Automation Coverage

### Automated Tests
| Test Area | Framework | Coverage | Location |
|-----------|-----------|----------|----------|
| Unit | [Jest/Vitest] | [X%] | [path] |
| Integration | [Testing Library] | [X%] | [path] |
| E2E | [Playwright] | [X scenarios] | [path] |
| API | [Supertest] | [X endpoints] | [path] |

### New Tests Needed
- [ ] [Test 1] - Type: [Unit/Integration/E2E]
- [ ] [Test 2] - Type: [Unit/Integration/E2E]
- [ ] [Test 3] - Type: [Unit/Integration/E2E]

---

## Performance Testing

### Performance Criteria
| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Page Load | < 2s | Lighthouse |
| API Response | < 200ms | Load testing |
| Time to Interactive | < 3s | Lighthouse |

### Load Testing (if applicable)
- **Concurrent Users**: [Target]
- **Duration**: [Minutes]
- **Scenarios**: [Key flows to test]

---

## Accessibility Testing

### WCAG Compliance
- [ ] Color contrast (AA standard)
- [ ] Keyboard navigation
- [ ] Screen reader testing
- [ ] Focus management
- [ ] Alt text for images

### Testing Tools
- [ ] axe DevTools
- [ ] VoiceOver / NVDA
- [ ] Keyboard-only navigation

---

## Cross-Browser / Cross-Device

### Browsers to Test
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)
- [ ] Mobile Safari
- [ ] Mobile Chrome

### Devices to Test
- [ ] Desktop (1920x1080)
- [ ] Laptop (1440x900)
- [ ] Tablet (768x1024)
- [ ] Mobile (375x667)

---

## Regression Testing

### Areas to Regression Test
- [ ] [Related feature 1]
- [ ] [Related feature 2]
- [ ] [Authentication flow]

### Smoke Test Checklist
- [ ] User can log in
- [ ] Main navigation works
- [ ] Core feature X works
- [ ] No console errors

---

## Test Execution

### Schedule
| Phase | Date | Owner |
|-------|------|-------|
| Test Plan Review | [Date] | QA |
| Test Environment Setup | [Date] | DevOps |
| Test Execution | [Date] | QA |
| Bug Triage | [Date] | Team |
| Retest | [Date] | QA |
| Sign-off | [Date] | QA Lead |

### Test Results Summary
| Category | Total | Passed | Failed | Blocked |
|----------|-------|--------|--------|---------|
| Happy Path | | | | |
| Edge Cases | | | | |
| Error Cases | | | | |
| Regression | | | | |

---

## Sign-Off

### Entry Criteria
- [ ] Feature development complete
- [ ] Code reviewed and merged
- [ ] Test environment ready
- [ ] Test data available

### Exit Criteria
- [ ] All P1 tests passed
- [ ] No P1/P2 bugs open
- [ ] Test coverage meets target
- [ ] Performance criteria met
- [ ] Accessibility verified

### Approval
| Role | Name | Date | Approved |
|------|------|------|----------|
| QA Lead | | | [ ] |
| Dev Lead | | | [ ] |
| PM | | | [ ] |
```

---

## Test Scenario Categories

### Think About These Areas

1. **Happy Path**: Normal, expected user flows
2. **Edge Cases**: Boundary conditions, unusual but valid inputs
3. **Error Cases**: Invalid inputs, failure scenarios
4. **Security**: Authentication, authorization, injection
5. **Performance**: Load, stress, response times
6. **Accessibility**: Keyboard, screen reader, contrast
7. **Compatibility**: Browsers, devices, screen sizes
8. **Integration**: Third-party services, APIs
9. **State**: Different user states, data conditions
10. **Concurrency**: Multiple users, race conditions

### Prioritization

- **P1 (Must Test)**: Core functionality, security-critical, high-usage paths
- **P2 (Should Test)**: Important edge cases, error handling
- **P3 (Nice to Test)**: Rare scenarios, minor functionality

---

## Testing Techniques

### Equivalence Partitioning
Divide inputs into groups that should be treated the same:
- Valid emails: test one representative
- Invalid emails: test one representative

### Boundary Value Analysis
Test at the edges:
- Minimum value
- Maximum value
- Just below minimum
- Just above maximum

### Decision Table Testing
For complex business logic with multiple conditions:
| Condition 1 | Condition 2 | Expected Action |
|-------------|-------------|-----------------|
| True | True | Action A |
| True | False | Action B |
| False | True | Action C |
| False | False | Action D |

### State Transition Testing
For features with state machines:
- Identify all states
- Identify all transitions
- Test each transition
- Test invalid transitions

---

## Automation Guidelines

### What to Automate

**Automate**:
- Regression tests (run frequently)
- Happy path flows
- Data-driven tests (many similar cases)
- API tests

**Don't Automate**:
- Exploratory testing
- One-time tests
- Rapidly changing features
- Visual design validation

### Test Pyramid

```
        /\
       /E2E\      Few, critical flows
      /------\
     /  INT   \   More, key integrations
    /----------\
   /    UNIT    \ Many, fast, isolated
  ----------------
```

---

## Quick Test Checklist

Before shipping, verify:

### Functionality
- [ ] All acceptance criteria met
- [ ] Happy path works
- [ ] Error handling works
- [ ] Edge cases handled

### Quality
- [ ] No console errors
- [ ] No broken links
- [ ] Loading states work
- [ ] Empty states work

### Performance
- [ ] Page loads in < 3s
- [ ] No memory leaks
- [ ] Images optimized

### Accessibility
- [ ] Keyboard navigable
- [ ] Screen reader friendly
- [ ] Color contrast OK

### Security
- [ ] Auth required where needed
- [ ] Permissions enforced
- [ ] No sensitive data exposed
