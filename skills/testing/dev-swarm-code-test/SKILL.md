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
- `07-tech-specs/` - Engineering standards, including source-code-structure.md and testing-standards.md
- `features/` folder with feature design and implementation docs
- `09-sprints/` folder with backlog and test plan
- `src/` folder (organized as defined in source-code-structure.md)
- Access to source code and running environment

## Feature-Driven Testing Workflow

**CRITICAL:** This skill follows a strict feature-driven approach where `feature-name` is the index for the entire project:

**For Each Backlog:**
1. Read backlog.md from `09-sprints/[sprint]/[BACKLOG_TYPE]-[feature-name]-<sub-feature>.md`
2. Extract the `feature-name` from the backlog file name
3. Read `features/features-index.md` to find the feature file
4. Read feature documentation in this order:
   - `features/[feature-name].md` - Feature definition (WHAT/WHY/SCOPE)
   - `features/flows/[feature-name].md` - User flows and process flows (if exists)
   - `features/contracts/[feature-name].md` - API/data contracts (if exists)
   - `features/impl/[feature-name].md` - Implementation notes (if exists)
5. Locate code and test files in `src/` using `features/impl/[feature-name].md`
6. Write/execute tests following `07-tech-specs/testing-standards.md`
7. Update `backlog.md` with test results and findings

This approach ensures AI testers can test large projects without reading all code at once.

## Your Roles in This Skill

- **QA Engineer (Quality Assurance Specialist)**: Lead test planning and execution. Design comprehensive test plans covering all scenarios. Write automated tests (unit, integration, E2E, API). Execute manual tests for complex user flows. Test across different environments and devices. Identify edge cases and boundary conditions. Analyze logs and debugging test failures. Create clear bug reports with reproduction steps. Suggest quality improvements and preventive measures.
- **Security Engineer**: Perform security testing and vulnerability scanning. Test authentication and authorization flows. Verify input validation and sanitization. Test for common vulnerabilities (OWASP Top 10). Review security configurations and access controls. Test encryption and data protection. Conduct penetration testing if applicable.
- **Tech Manager (Architect)**: Verify implementation aligns with architectural principles. Test system integration and component interactions. Validate technical dependencies work as expected. Test scalability and performance against architectural requirements. Identify technical risks and architectural issues during testing.
- **Product Manager**: Verify implementation meets acceptance criteria and user stories. Test user flows match expected behavior. Validate features deliver intended user value. Review test coverage against functional requirements. Ensure quality meets product standards before release.
- **UX Designer**: Conduct usability testing and review user experience. Verify UI matches design specifications and mockups. Test responsive design across devices. Validate accessibility compliance (WCAG). Test user flows for intuitiveness. Identify UX issues or improvements.
- **AI Engineer**: Test AI/ML model performance and accuracy. Validate prompt engineering and LLM integration. Test vector database and embeddings functionality. Verify model monitoring and evaluation pipelines. Test AI fallback strategies and error handling. Validate content generation quality and moderation effectiveness.
- **Legal Advisor**: Verify legal content accuracy and compliance. Review Terms of Service, Privacy Policy, and Cookie Policy for completeness. Ensure compliance with regulations (GDPR, CCPA, etc.). Validate disclaimers and liability statements. Test age restriction enforcement and data handling flows.
- **Customer Support**: Test FAQ pages, help documentation, and support flows. Verify contact forms and troubleshooting guides work correctly. Test self-service support functionality. Validate knowledge base navigation and search. Ensure onboarding guides are clear and effective.
- **Content Moderator**: Test content moderation workflows and reporting mechanisms. Verify moderation queue and review dashboard functionality. Test community guidelines enforcement. Validate user communication flows for moderation actions. Test appeals and dispute resolution processes.

## Role Communication

As an expert in your assigned roles, you must announce your actions before performing them using the following format:

As a {Role} [and {Role}, ...], I will {action description}

This communication pattern ensures transparency and allows for human-in-the-loop oversight at key decision points.
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
   09-sprints/
   └── sprint-name/
       └── [BACKLOG_TYPE]-[feature-name]-<sub-feature>.md
   ```
   - Locate the sprint README at `09-sprints/[sprint-name]/README.md` for required progress log updates

2. **Read the backlog file:**
   - Understand requirements and acceptance criteria
   - Read the test plan defined in backlog
   - **Extract the `feature-name`** from the file name (CRITICAL)
   - Verify `Feature Name` in backlog metadata matches the file name
   - If they do not match, stop and ask the user to confirm the correct feature name
   - Note backlog type (FEATURE/CHANGE/BUG/IMPROVE)
   - Identify success criteria

3. **Read testing standards:**
   - Read `07-tech-specs/testing-standards.md`
   - Understand test coverage requirements
   - Note test frameworks and conventions

4. **Read feature documentation (using feature-name as index):**
   - Read `features/features-index.md` to confirm feature exists
   - Read `features/[feature-name].md` - Feature definition (expected behavior)
   - Read `features/flows/[feature-name].md` - User flows (test these flows)
   - Read `features/contracts/[feature-name].md` - API contracts (test these contracts)
   - Read `features/impl/[feature-name].md` - Implementation notes (what was built)

5. **Locate code and tests:**
   - Use `features/impl/[feature-name].md` to find code locations
   - Navigate to `src/` directory
   - Check existing test files in `src/` (locations from features/impl/[feature-name].md)
   - Identify files to test

6. **Read sprint test plan:**
   - Check `09-sprints/sprint/README.md` for sprint-level test plan
   - Understand end-user test scenarios
   - Note manual vs automated test requirements

7. **Determine test scope:**
   - What test types are needed?
   - Manual or automated or both?
   - Environment requirements?

**DO NOT** read the entire codebase. Use `feature-name` to find only relevant files.

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

Test individual functions/components:

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

2. **Create backlog file in `09-sprints/`:**

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

### Step 9: Update Backlog with Test Results

**CRITICAL:** Update the backlog.md file to track testing progress:

1. **Update backlog status:**
   - Change status from "In Testing" to "Done" (if all tests pass)
   - Or change to "In Development" (if bugs found requiring fixes)
   - Add a "Testing Notes" section if not present

2. **Document testing findings:**
   - **Test Summary:** Total tests executed, passed, failed
   - **Test Types Executed:** Unit, integration, API, UI, manual
   - **Test Coverage:** Percentage of code/features tested
   - **Issues Found:** Count of CHANGE/BUG/IMPROVE backlogs created
   - **Test Decision:** Passed, Passed with minor issues, Failed, or Blocked
   - **Test Evidence:** Screenshots, logs, performance metrics
   - **Related Backlogs:** Link to created CHANGE/BUG/IMPROVE backlogs

3. **Update feature documentation:**
   - Add test notes to `features/impl/[feature-name].md`
   - Document known issues or limitations discovered
   - Note test coverage achieved
   - Update with any testing insights

4. **Notify user:**
   - Summarize test results
   - Report pass/fail status
   - List critical issues found
   - Recommend next steps (fix bugs, deploy, etc.)

5. **Update sprint README (README.md) (CRITICAL):**
   - Update backlog status in the sprint backlog table
   - Append a log entry in the sprint progress log for the Testing step

**These backlog.md and sprint README updates create the audit trail showing testing was completed and results.**
