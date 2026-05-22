---
name: test-design
description: Design comprehensive test strategies with risk-informed prioritization (P0/P1/P2), test levels (unit/integration/E2E), mock strategies, and CI/CD integration. Creates Given-When-Then scenarios for all acceptance criteria, develops mock strategies for external dependencies, and plans CI/CD execution stages. Use during task planning before implementation to ensure comprehensive test coverage.
version: 2.0
category: Quality
acceptance:
  all_acs_have_tests: "All acceptance criteria have test scenarios designed with Given-When-Then format, clear pass/fail criteria, and test data specifications"
  priorities_assigned: "All test scenarios assigned priority levels (P0/P1/P2) based on risk scores from risk-profile or AC criticality"
  mock_strategies_developed: "Mock strategies developed for all external dependencies (APIs, databases, services) with implementation guidance"
  cicd_integration_planned: "CI/CD test execution strategy planned with stages (pre-commit, PR, pre-deployment, production), parallelization, and coverage requirements"
inputs:
  task_id:
    type: string
    required: true
    description: "Task identifier for test design (e.g., 'task-007')"
  task_file:
    type: string
    required: true
    description: "Path to task specification file"
  assessment_mode:
    type: enum
    required: false
    description: "Assessment timing (pre-implementation | retrospective)"
    default: "pre-implementation"
  risk_profile_file:
    type: string
    required: false
    description: "Path to risk profile file (for risk-informed prioritization)"
outputs:
  total_tests:
    type: number
    description: "Total number of test scenarios designed"
  p0_tests_count:
    type: number
    description: "Number of P0 (critical) tests"
  p1_tests_count:
    type: number
    description: "Number of P1 (high priority) tests"
  p2_tests_count:
    type: number
    description: "Number of P2 (medium priority) tests"
  unit_tests_count:
    type: number
    description: "Number of unit tests"
  integration_tests_count:
    type: number
    description: "Number of integration tests"
  e2e_tests_count:
    type: number
    description: "Number of end-to-end tests"
  estimated_execution_time_seconds:
    type: number
    description: "Estimated total test execution time in seconds"
  test_design_file:
    type: string
    description: "Path to generated test design document"
telemetry:
  emit: "skill.test-design.completed"
  track:
    - task_id
    - assessment_mode  # pre-implementation | retrospective
    - total_tests
    - p0_tests_count
    - p1_tests_count
    - p2_tests_count
    - unit_tests_count
    - integration_tests_count
    - e2e_tests_count
    - estimated_execution_time_seconds
    - risk_profile_available
---

# Quality Skill: Test Design Strategy

Design comprehensive test strategies **before implementation** using risk-informed prioritization, test level recommendations (unit/integration/E2E), mock strategies for dependencies, and CI/CD integration planning.

## Purpose

Create test design documents that specify:
- **Test scenarios** with Given-When-Then format for all acceptance criteria
- **Test levels** (unit, integration, E2E) based on what's being tested
- **Test priorities** (P0/P1/P2) based on risk scores and criticality
- **Mock strategies** for external dependencies with implementation guidance
- **CI/CD integration** with execution stages and coverage requirements

**Key Innovation (BMAD Pattern):**
- Test design BEFORE implementation guides what tests to write
- Risk-informed prioritization prevents missing critical tests
- Level recommendations optimize test execution speed
- Mock strategies enable effective testing of complex systems

## When to Use This Skill

**Best Used:**
- After task spec creation, before implementation
- After risk profiling (uses risk scores for prioritization)
- For complex features requiring multiple test levels
- When planning test infrastructure for new components

**Can Skip For:**
- Simple bug fixes with obvious test cases (1-2 tests)
- Trivial changes with existing test patterns
- Emergency hotfixes (add test design after stabilization)

**Triggers:**
- User asks to "design tests", "create test strategy", "plan test cases"
- Before implementing complex features (proactively suggest)
- After risk profile completed (natural next step)

## Test Levels

### Unit Tests
**Purpose:** Test individual functions, methods, classes in isolation

**Characteristics:**
- Fast execution (< 50ms each)
- No external dependencies (fully mocked)
- Test business logic, algorithms, validation rules
- High coverage expected (>80%)

**When to use:** Business logic, data transformations, validation rules, utility functions, error handling

### Integration Tests
**Purpose:** Test interactions between components/modules

**Characteristics:**
- Moderate execution time (< 500ms each)
- May use test database, test APIs
- Test component interactions and integration points
- Focus on service boundaries

**When to use:** API endpoints, database operations, service-to-service communication, authentication flows, external API interactions (mocked)

### E2E (End-to-End) Tests
**Purpose:** Test complete user journeys through the system

**Characteristics:**
- Slower execution (seconds per test)
- Use real or near-real environment
- Test critical user workflows end-to-end
- Fewer tests, higher value (focus on critical paths)

**When to use:** Critical user journeys, multi-step workflows, UI + backend integration, business-critical paths, regression prevention

## Test Priority Levels

### P0 (Critical) - Must Have
**Requirements:**
- Tests critical functionality (authentication, payment, data integrity)
- Validates security requirements (injection, XSS, auth bypass)
- Prevents data loss or corruption
- Covers high-risk areas (score ≥6 from risk profile)
- **Must pass before merge** (CI blocks merge if P0 fails)

**Examples:** Authentication/authorization, payment processing, data integrity operations, security vulnerability prevention

### P1 (High) - Should Have
**Requirements:**
- Tests important functionality (core features)
- Covers medium-risk areas (score 3-5)
- Validates key user features
- **Should pass before merge** (exceptions allowed with justification)

**Examples:** Core feature functionality, error handling paths, performance requirements, user experience features

### P2 (Medium) - Nice to Have
**Requirements:**
- Tests edge cases and rare scenarios
- Covers low-risk areas (score 1-2)
- Nice-to-have validations
- **Can defer if time-constrained** (implement after main work)

**Examples:** Rare edge cases, minor UI variations, optional features, future enhancements

## SEQUENTIAL Skill Execution

**CRITICAL:** Do not proceed to next step until current step is complete

### Step 0: Load Configuration and Context

**Purpose:** Load task specification, risk profile, and configuration to understand test requirements

**Actions:**

1. **Load configuration from `.claude/config.yaml`:**
   - Extract test coverage targets (overall, critical paths, new code)
   - Extract test timeout limits
   - Extract quality settings

2. **Get task file path from user:**
   - Example: `.claude/tasks/task-006-user-signup.md`
   - Verify file exists and is readable

3. **Read task specification:**
   - Load objective and acceptance criteria
   - Load context (data models, APIs, components)
   - Load task breakdown

4. **Check for risk profile (optional but recommended):**
   - Look for: `.claude/quality/assessments/{task-id}-risk-*.md`
   - If exists: Load risk scores for prioritization
   - If missing: Can proceed but warn user (recommend running risk-profile first)

**Output:** Configuration loaded with coverage targets/timeouts, task context understood, risk profile loaded if available, ready to analyze requirements

**Halt Conditions:** Config file missing | Task file missing/unreadable

**See:** `references/templates.md#step-0-output` for complete format

---

### Step 1: Analyze Test Requirements

**Purpose:** Identify what needs to be tested for each acceptance criterion

**Actions:**

1. **For each acceptance criterion:**
   - What needs to be validated? (testable outcomes)
   - What are the edge cases? (boundaries, limits)
   - What could go wrong? (error scenarios)
   - What are the security considerations? (injection, auth bypass)

2. **Identify test categories:**
   - **Happy path:** Normal, expected usage (most common scenarios)
   - **Error cases:** Invalid inputs, failures, exceptions
   - **Edge cases:** Boundaries, limits, unusual inputs
   - **Security:** Authentication, authorization, injection, XSS
   - **Performance:** Response time, resource usage, scalability
   - **Integration:** Component interactions, service boundaries

3. **Map to test levels:**
   - What needs unit tests? (Logic, validation, algorithms)
   - What needs integration tests? (API, database, service interactions)
   - What needs E2E tests? (User journeys, critical workflows)

4. **Consider technical constraints:**
   - External dependencies to mock (APIs, payment, email)
   - Database interactions (test DB or mock?)
   - Async operations (promises, callbacks)
   - File I/O (temp directories)
   - Network calls (mock or test endpoints?)

**Output:** Test requirements identified per AC, categories mapped (happy path/error/edge/security/performance/integration), test levels determined (unit/integration/E2E), technical considerations noted

**Halt Conditions:** ACs too vague to test | Missing context

**See:** `references/templates.md#step-1-output` for complete format with detailed examples

---

### Step 2: Design Test Scenarios

**Purpose:** Create specific test scenarios with Given-When-Then format, priorities, and test data

**Actions:**

For each test requirement from Step 1:

1. **Write test scenario description:**
   - Use **Given-When-Then** format for clarity (not BDD code, just format)
   - Specify exact inputs and expected outputs
   - Define clear pass/fail criteria
   - Include test data samples

2. **Assign test level:**
   - Unit, Integration, or E2E
   - Based on what's being tested (logic vs interaction vs journey)

3. **Assign priority (risk-informed):**
   - **P0 if:** Critical functionality, security, high-risk (score ≥6), data integrity
   - **P1 if:** Important functionality, medium-risk (score 3-5), core features
   - **P2 if:** Edge cases, low-risk (score 1-2), optional features

4. **Specify test data requirements:**
   - Valid samples (normal inputs)
   - Invalid samples (error scenarios)
   - Edge case values (boundaries, limits)
   - Security payloads (injection, XSS)

5. **Identify dependencies:**
   - What needs to be mocked? (external APIs, payment, email)
   - What requires real services? (database, file system)
   - What fixtures needed? (test data, mocks)

**Output:** Test scenarios with Given-When-Then format, test level assigned, priority assigned (P0/P1/P2 with risk linkage), test data specified, dependencies identified

**Halt Conditions:** Cannot define clear pass/fail criteria | Scenarios too ambiguous

**See:** `references/templates.md#step-2-output` for complete scenario examples (valid signup, SQL injection, duplicate email, E2E flow)

---

### Step 3: Develop Mock Strategies

**Purpose:** Define mocking approach for external dependencies to enable effective testing

**Actions:**

1. **Identify external dependencies:**
   - Third-party APIs (Stripe, SendGrid, etc.)
   - External services (email, payment, SMS, etc.)
   - Database (Postgres, MongoDB, etc.)
   - File system (uploads, logs, temp files)
   - Network resources (HTTP calls, websockets)

2. **For each dependency, decide mocking approach:**

   **Option A: Full Mock**
   - Replace with test double (jest.fn(), sinon stub)
   - Predictable, fast, isolated
   - **Use for:** Third-party APIs, external services

   **Option B: Test Instance**
   - Use real implementation with test data
   - More realistic, slower
   - **Use for:** Database (test DB), file system (temp dirs)

   **Option C: Partial Mock**
   - Real implementation, mock specific parts
   - Balance realism and speed
   - **Use for:** Service with mostly local logic but external call

3. **Specify mock data/fixtures:**
   - What responses to mock? (success, failure, timeout)
   - What fixtures to create? (test data, sample files)
   - What edge cases to simulate? (errors, delays)

4. **Document mock configuration:**
   - How to set up mocks? (jest.mock, setup files)
   - What libraries to use? (jest, sinon, nock)
   - How to verify mock interactions? (expect calls, spy on methods)

**Output:** Mock strategy for each dependency (full mock/test instance/partial mock), mock data/fixtures specified (success/failure/edge cases), configuration documented (setup/libraries/verification)

**Halt Conditions:** Cannot determine appropriate mock strategy | Dependency too complex to mock

**See:** `references/templates.md#step-3-output` for complete mock strategies (email service, database, JWT, payment API)

---

### Step 4: Plan CI/CD Integration

**Purpose:** Define test execution strategy for CI/CD pipeline with stages, parallelization, and coverage

**Actions:**

1. **Define test execution strategy:**
   - When do different test types run? (pre-commit, PR, pre-deploy, production)
   - What's the trigger for each? (git hook, PR event, deployment event)
   - What's the failure policy? (block merge, alert, rollback)

2. **Specify test environments:**
   - Local development (fast feedback)
   - CI pipeline (comprehensive validation)
   - Pre-deployment (staging verification)
   - Production (smoke tests only)

3. **Configure test parallelization:**
   - What can run in parallel? (unit tests - fully parallel)
   - What must run sequentially? (E2E tests - shared state)
   - Resource requirements? (CPU, memory, database)

4. **Define coverage requirements:**
   - Minimum coverage percentage (overall, new code)
   - Critical paths requiring 100% (security, payment, data integrity)
   - Coverage failure policy (block merge, warning)

5. **Plan test data management:**
   - How to seed test data? (global setup, fixtures)
   - How to clean up after tests? (global teardown, beforeEach)
   - How to handle shared resources? (isolated databases per worker)

**Output:** Test execution strategy (stages/triggers/failure policy), environment configuration, parallelization plan, coverage requirements, data management approach

**Halt Conditions:** Cannot determine CI/CD strategy | Environment requirements unclear

**See:** `references/templates.md#step-4-output` for complete CI/CD examples (GitHub Actions, GitLab CI, pre-commit hooks)

---

### Step 5: Calculate Test Summary

**Purpose:** Calculate test counts, priorities, and execution time estimates

**Actions:**

1. **Count tests by level:**
   - Total unit tests
   - Total integration tests
   - Total E2E tests
   - Total all tests

2. **Count tests by priority:**
   - P0 (Critical) - must pass before merge
   - P1 (High) - should pass before merge
   - P2 (Medium) - can defer if needed

3. **Estimate execution time:**
   - Unit: 50ms average × count
   - Integration: 500ms average × count
   - E2E: 5s average × count
   - Total execution time

4. **Calculate expected coverage:**
   - Based on scenarios vs acceptance criteria
   - Critical path coverage (should be 100%)
   - Overall coverage estimate (based on scope)

**Output:** Test count summary (by level and priority), priority breakdown (P0/P1/P2 counts), estimated execution time (by level and total), expected coverage (overall and critical paths)

**Halt Conditions:** None (calculation always possible)

**See:** `references/templates.md#step-5-output` for complete summary examples

---

### Step 6: Generate Test Design Document and Present Summary

**Purpose:** Generate complete test design document and present concise summary to user

**Actions:**

1. **Load test design template:**
   - Read `.claude/templates/test-design.md` (if exists)
   - Use default structure if template missing

2. **Populate all sections:**
   - Test summary (from Step 5)
   - Test scenarios by acceptance criterion (from Step 2)
   - Mock strategies (from Step 3)
   - CI/CD integration plan (from Step 4)
   - Risk-test mapping (if risk profile available)

3. **Generate file path:**
   - Format: `.claude/quality/assessments/{taskId}-test-design-{YYYYMMDD}.md`
   - Example: `.claude/quality/assessments/task-006-test-design-20251029.md`
   - Create directory if needed

4. **Write test design file**

5. **Present concise summary to user:**
   - Test counts and priorities
   - Key test scenarios (security, functionality, performance)
   - Mock strategy summary
   - CI/CD integration summary
   - Risk-test mapping (if available)
   - Next steps guidance

**Output:** Complete test design document written to file, concise summary presented to user with test counts/priorities/mock strategy/CI-CD/risk mapping, clear next steps guidance

**Halt Conditions:** File write fails

**See:** `references/templates.md#step-6-output` for complete user-facing summary example and test design document template

---

## Integration with Other Skills

**After risk-profile:** Risk profile identifies high-risk areas with P×I scores → test-design uses scores for prioritization (critical risks → P0 tests, high → P0/P1, medium/low → P2)

**Before implementation:** Test design complete with scenarios/mocks/CI-CD → Implementation writes tests following scenarios, uses mock strategies, achieves P0 tests first, targets 80%+ coverage

**With trace-requirements:** Test design provides scenarios mapped to ACs → trace-requirements verifies all scenarios implemented, all ACs covered by passing tests, coverage gaps identified

**See:** `references/templates.md#integration-examples` for complete workflows with data flow

## Best Practices

Test-first approach (design before code) | Risk-informed prioritization (critical risks → P0 tests) | Appropriate test levels (unit for logic, integration for interactions, E2E for critical journeys) | Realistic mock strategies (mock external APIs, real DB test instances) | CI/CD integration (fast feedback loops) | Coverage vs quality (focus on meaningful scenarios, 100% for critical paths)

## Common Pitfalls

Avoid: Too many E2E tests (slow/brittle) | Under-mocking (hitting real APIs) | Brittle tests (hard-coded values) | Ignoring test performance (slow suites) | Testing implementation details (private methods) | No CI/CD integration (manual only)

Instead: Unit test logic, E2E for critical journeys | Mock external dependencies | Use factories/fixtures | Keep unit <50ms, integration <500ms | Test public API/behavior | Automate in CI/CD

## Configuration

Configure in `.claude/config.yaml`: Test coverage targets (overall/criticalPaths/newCode), test timeouts (unit/integration/e2e), assessment location

**See:** `references/templates.md#configuration-examples` for complete config.yaml, package.json scripts, jest.config.js

## Reference Files

Detailed documentation in `references/`:

- **templates.md**: All output formats (Step 0-6), complete test scenario examples (Given-When-Then), mock strategies (email service, database, JWT, payment API), CI/CD examples (GitHub Actions, GitLab CI, pre-commit hooks), complete test design document template, configuration examples, JSON output format

- **test-scenarios.md**: Test scenario patterns (currently placeholder - see templates.md)

- **mock-strategies.md**: Mock strategy patterns (currently placeholder - see templates.md)

- **cicd-integration.md**: CI/CD integration patterns (currently placeholder - see templates.md)

- **test-examples.md**: Test design examples (currently placeholder - see templates.md)

---

**Version:** 2.0 (Refactored for skill-creator compliance and Minimal V2 architecture)
**Category:** Quality
**Depends On:** risk-profile (optional but recommended for risk-informed prioritization)
**Used By:** trace-requirements (verifies test coverage of acceptance criteria)
