---
name: dev-swarm-code-test
description: Create and execute comprehensive tests including unit tests, integration tests, CLI tests, web/mobile UI tests, API tests, and log analysis. Find bugs, verify requirements, identify improvements, and create change/bug/improve backlogs. Use when testing implementations or ensuring quality.
---

# AI Builder - Code Test

This skill creates and executes comprehensive test suites to verify code quality and functionality. As a QA Engineer expert, you'll design test plans, write automated tests, perform manual testing, analyze results, identify issues, and create backlogs for changes, bugs, or improvements.

## When to Use This Skill

- User asks to test a backlog or feature
- User requests test creation or execution
- Code review is complete and testing is needed
- User wants to verify implementation meets requirements
- User asks to run test suite
- User wants to validate a sprint before completion

## Prerequisites

This skill requires:
- Code implementation completed
- Code review completed (recommended)
- `04-prd/` - Product Requirements Document (business requirements and acceptance criteria)
- `07-tech-specs/` - Engineering standards and constraints
- `features/` folder with feature design and implementation docs
- `10-sprints/` folder with backlog and test plan
- `{SRC}/` folder (organized as defined in source-code-structure.md)
- Access to source code and running environment

## Feature-Driven Testing Workflow

**CRITICAL:** This skill follows a strict feature-driven approach where `feature-name` is the index for the entire project:

**For Each Backlog:**
1. Read backlog.md from `10-sprints/SPRINT-XX-descriptive-name/[BACKLOG_TYPE]-XX-[feature-name]-<sub-feature>.md`
2. Extract the `feature-name` from the backlog file name
3. Read `features/features-index.md` to find the feature file
4. Read feature documentation in this order:
   - `features/[feature-name].md` - Feature definition (WHAT/WHY/SCOPE)
   - `features/flows/[feature-name].md` - User flows and process flows (if exists)
   - `features/contracts/[feature-name].md` - API/data contracts (if exists)
   - `features/impl/[feature-name].md` - Implementation notes (if exists)
5. Locate code and test files in `{SRC}/` using `features/impl/[feature-name].md`
6. Write/execute tests following `07-tech-specs/testing-standards.md`
7. Update `backlog.md` with test results and findings

This approach ensures AI testers can test large projects without reading all code at once.

## Your Roles in This Skill

See `dev-swarm/docs/general-dev-stage-rule.md` for role selection guidance.

## Role Communication

See `dev-swarm/docs/general-dev-stage-rule.md` for the required role announcement format.

## Test Types Overview

This skill handles multiple test types:

1. **Unit Tests**: Test individual functions/components in isolation
2. **Integration Tests**: Test component interactions and data flow
3. **API Tests**: Test REST/GraphQL endpoints, contracts, error handling
4. **CLI Tests**: Test command-line interfaces and scripts
5. **Web UI Tests**: Test web interfaces (Playwright, Selenium, Cypress)
6. **Mobile UI Tests**: Test mobile apps (if applicable)
7. **Log Analysis**: Verify logging, monitoring, error tracking
8. **Performance Tests**: Load testing, stress testing, benchmarks
9. **Security Tests**: Vulnerability scanning, penetration testing

## Instructions

Follow these steps in order:

### Step 0: Verify Prerequisites and Gather Context (Feature-Driven Approach)

**IMPORTANT:** Follow this exact order to efficiently locate all relevant context:

1. **Identify the backlog to test:**
   - User specifies which backlog to test
   - Or test latest reviewed backlog from sprint

   ```
   10-sprints/
   └── SPRINT-XX-descriptive-name/
       └── [BACKLOG_TYPE]-XX-[feature-name]-<sub-feature>.md
   ```
   - Locate the sprint README at `10-sprints/SPRINT-XX-descriptive-name/README.md` for required progress log updates

2. **Read the backlog file:**
   - Understand requirements and acceptance criteria
   - Read the test plan defined in backlog
   - **Extract the `feature-name`** from the file name (CRITICAL)
   - Verify `Feature Name` in backlog metadata matches the file name
   - If they do not match, stop and ask the user to confirm the correct feature name
   - Note backlog type (FEATURE/CHANGE/BUG/IMPROVE)
   - Identify success criteria

3. **Read testing standards:**
   - Understand test coverage requirements
   - Note test frameworks and conventions

4. **Read PRD and tech specs:**
   - Read `04-prd/` (all markdown files) - Product requirements and acceptance criteria for the feature
   - Read `07-tech-specs/` (all markdown files) - Technical specifications and engineering standards
   - Understand the business context and technical constraints

5. **Read feature documentation (using feature-name as index):**
   - Read `features/features-index.md` to confirm feature exists
   - Read `features/[feature-name].md` - Feature definition (expected behavior)
   - Read `features/flows/[feature-name].md` - User flows (test these flows)
   - Read `features/contracts/[feature-name].md` - API contracts (test these contracts)
   - Read `features/impl/[feature-name].md` - Implementation notes (what was built)

6. **Locate code and tests:**
   - Use `features/impl/[feature-name].md` to find code locations
   - Navigate to `{SRC}/` directory
   - Check existing test files in `{SRC}/` (locations from features/impl/[feature-name].md)
   - Identify files to test

7. **Read sprint test plan:**
   - Check `10-sprints/SPRINT-XX-descriptive-name/README.md` for sprint-level test plan
   - Understand end-user test scenarios
   - Note manual vs automated test requirements

8. **Determine test scope:**
   - What test types are needed?
   - Manual or automated or both?
   - Environment requirements?

**DO NOT** read the entire codebase. Use `feature-name` to find only relevant files.

### Checklist and Status Rules (Backlog + Sprint)

Apply these rules whenever you test a backlog or sprint:
- For any checklist, acceptance criteria, or test plan, use task list items and mark results as:
  - `[x]` = pass
  - `[-]` = no test needed
- After testing a backlog, update its status to `Done`.
- After finishing a backlog test, check if any backlogs remain in the sprint README.
  - If none remain, test the sprint-level checklist items in the sprint README, mark each item, and set the sprint status to `Completed`.

### Test Method Priority

Use this priority order when choosing test methods:
1. `curl` commands (highest priority)
2. `playwright-browser-*` skills for web UI (must use browser for any web UI item)
3. Write test code
4. Write unit tests

### Step 1: Design Test Strategy

Before writing tests, plan the approach:

1. **Identify test scenarios:**

   **Happy Path:**
   - Normal, expected user flows
   - Valid inputs and operations
   - Successful outcomes

   **Edge Cases:**
   - Boundary values (min, max, zero, negative)
   - Empty inputs
   - Very large inputs
   - Special characters

   **Error Cases:**
   - Invalid inputs
   - Missing required data
   - Permission denials
   - Network failures
   - System errors

   **Security Cases:**
   - SQL injection attempts
   - XSS attempts
   - Authentication bypass attempts
   - Authorization violations
   - CSRF attacks

2. **Select test types:**
   - Which test types are appropriate?
   - What can be automated?
   - What requires manual testing?
   - What's the priority order?

3. **Define success criteria:**
   - What does passing mean?
   - What coverage is needed?
   - Performance benchmarks?
   - Security requirements?

### Step 2: Write Automated Tests

Create automated test suites based on test type:

#### Unit Tests

Test individual functions/components in isolation:

**Best Practices:**
- Test one thing per test case
- Clear, descriptive test names
- Arrange-Act-Assert pattern
- Mock external dependencies
- Test both success and failure paths

#### Integration Tests

Test component interactions:

#### API Tests

Test endpoints and contracts:



#### CLI Tests

Test command-line interfaces:

#### Web UI Tests (Playwright/Cypress)

Test web interfaces:

### Step 3: Execute Manual Tests

For scenarios that can't be easily automated:

1. **Follow test plan from backlog:**
   - Execute each manual test step
   - Use curl for API testing
   - Use CLI for command testing
   - Use browser for UI testing

2. **Document test execution:**
   - Record what was tested
   - Note any issues encountered
   - Capture screenshots/logs for failures
   - Time performance-critical operations

3. **Test across environments:**
   - Development environment
   - Different browsers (Chrome, Firefox, Safari)
   - Different devices (mobile, tablet, desktop)
   - Different operating systems (if applicable)

### Step 4: Analyze Logs

Review application logs for issues:

1. **Check for errors:**
   - Unhandled exceptions
   - Stack traces
   - Error messages

2. **Verify logging quality:**
   - Appropriate log levels (debug, info, warn, error)
   - No sensitive data in logs (passwords, tokens)
   - Sufficient context in log messages
   - Proper error tracking

3. **Monitor performance:**
   - Slow queries or operations
   - Memory usage patterns
   - Resource leaks

4. **Security audit:**
   - No secrets logged
   - Proper access control logging
   - Suspicious activity detection

### Step 5: Performance Testing (When Needed)

For performance-critical features:

1. **Load testing:**
   - Simulate multiple concurrent users
   - Measure response times
   - Identify bottlenecks

2. **Stress testing:**
   - Push system beyond normal limits
   - Find breaking points
   - Test recovery behavior

3. **Benchmark key operations:**
   - Database query performance
   - API response times
   - Page load times

### Step 6: Analyze Results and Identify Issues

Categorize findings into three types:

#### 1. Changes (Doesn't meet requirements)
Implementation doesn't meet original requirements:
- Missing acceptance criteria
- Incorrect behavior vs specification
- Doesn't follow test plan
- Feature doesn't work as designed

**Action**: Create `change` type backlog

#### 2. Bugs (Defects found)
Code has defects or errors:
- Functional bugs (incorrect results)
- UI bugs (broken layouts, wrong text)
- API bugs (wrong status codes, incorrect responses)
- Performance bugs (timeouts, slowness)
- Security vulnerabilities
- Crashes or exceptions
- Data corruption

**Action**: Create `bug` type backlog

#### 3. Improvements (Enhancement opportunities)
Non-critical enhancements:
- Better error messages
- UX improvements
- Performance optimizations
- Additional validation
- Better logging
- Test coverage gaps
- Accessibility improvements

**Action**: Create `improve` type backlog

### Step 7: Create Backlogs for Issues

For each issue found, create a backlog:

1. **Determine severity:**
   - **Critical**: System unusable, data loss, security breach
   - **High**: Major feature broken, significant user impact
   - **Medium**: Minor feature broken, workaround exists
   - **Low**: Cosmetic issues, minor improvements

2. **Create backlog file in `10-sprints/`:**

   **Test Bug Backlog Template:**
   ```markdown
   # Backlog: [Type] - [Brief Description]

   ## Type
   [change | bug | improve]

   ## Severity
   [critical | high | medium | low]

   ## Original Feature/Backlog
   Reference to original backlog that was tested

   ## Issue Description
   Clear description of the bug or issue

   ## Steps to Reproduce
   1. Step-by-step instructions to reproduce
   2. Include specific inputs/actions
   3. Note environment details

   ## Expected Behavior
   What should happen

   ## Actual Behavior
   What actually happens

   ## Test Evidence
   - Screenshots
   - Log excerpts
   - Error messages
   - Performance metrics

   ## Affected Components
   - Files/functions involved
   - APIs or UI elements broken

   ## Reference Features
   Related features to consult

   ## Test Plan
   How to verify the fix works
   ```

3. **Notify Project Management:**
   - Critical issues need immediate attention
   - High severity bugs should be prioritized
   - Medium/low can be batched

### Step 8: Create Test Report

Document test results:

1. **Test Summary:**
   - Total test cases executed
   - Passed vs Failed
   - Test coverage achieved
   - Time taken

2. **Test Results by Type:**
   - Unit tests: X passed, Y failed
   - Integration tests: X passed, Y failed
   - API tests: X passed, Y failed
   - UI tests: X passed, Y failed
   - Manual tests: X passed, Y failed

3. **Issues Found:**
   - Changes required: count
   - Bugs found: count
   - Improvements suggested: count
   - By severity breakdown

4. **Test Decision:**
   - **Passed**: All tests pass, ready for production
   - **Passed with minor issues**: Non-critical improvements noted
   - **Failed**: Critical issues must be fixed before release
   - **Blocked**: Cannot test due to environment or dependency issues

### Step 9: Finalize and Commit

**CRITICAL:** Follow this process to safely commit changes and update tracking:

1. **Update Tracking Files:**
   - Update `backlog.md`:
     - Change status to `Done` after testing completes
     - Mark all checklist items (acceptance criteria/test plan) as `[x]` pass or `[-]` no test needed
     - Add "Testing Notes" section:
       - **Test Summary:** Passed/Failed counts
       - **Issues Found:** Bug backlogs created
       - **Decision:** Passed/Failed
   - Update feature documentation with test results
   - Update `10-sprints/.../README.md`:
     - Update status in table
     - Add progress log entry
     - If all backlogs are Done, mark sprint-level checklist items as `[x]` pass or `[-]` no test needed
     - If sprint-level checks are complete, set sprint status to `Completed`

2. **Request Human Review:**
   - Present the test results and plan to commit
   - Ask user: "Please review the results. If approved, I will commit and close the backlog."
   - **Wait for approval.**

3. **Commit the Tests/Fixes (Content):**
   - Run `git add .` to stage all changes
   - **Unstage** the backlog file and sprint README (`git reset HEAD <path-to-backlog> <path-to-sprint-readme>`)
   - Check if there are staged changes:
     - **If yes:**
       - Draft conventional commit message (e.g., "test: add tests for [feature-name]")
       - Commit: `git commit -m "test: ..."`
       - Get Commit ID: `git rev-parse --short HEAD`
     - **If no** (only current backlog updated):
       - Skip to next step

4. **Update Backlog with Commit ID:**
   - If a commit was made, append "**Test Commit:** `[commit-id]`" to the "Testing Notes" in `backlog.md`

5. **Commit the Backlog (Metadata):**
   - Stage `backlog.md` and sprint `README.md`
   - Commit: `git commit -m "docs([feature-name]): update backlog status to Done"`

6. **Notify user:**
   - Confirm completion
   - If Done: "Backlog closed successfully"
   - If Failed: "Backlog returned to development"

**This two-step commit process ensures history is preserved before the backlog is updated with the commit reference.**
