---
name: requirements-writing
description: Write clear, testable requirements using User Stories and Gherkin scenarios for Manifest Logistics SaaS. Capture functional and non-functional requirements with proper acceptance criteria. Use when defining new features or documenting system behavior.
---

# Requirements Writing Skill

You are assisting with writing clear, testable requirements that drive development and testing for Manifest Logistics SaaS.

## Core Principles

### Requirements Should Be
- **Clear**: Unambiguous and understandable
- **Testable**: Can be verified through RSpec/Cucumber
- **Complete**: All necessary information included
- **Consistent**: No contradictions
- **Traceable**: Linked to business needs
- **Feasible**: Technically and economically possible

## Primary Format: User Stories + Gherkin

### User Stories (High-Level Features)

**Format**:
```
As a [role]
I want [feature/capability]
So that [benefit/value]
```

**Good Examples**:
```
As a Merchant
I want to create delivery tasks via API
So that my e-commerce orders are automatically dispatched

As a Carrier
I want to see bundled tasks on my route
So that I can deliver multiple packages efficiently

As an Account Admin
I want to configure SMS templates
So that recipients receive branded notifications
```

**Bad Examples**:
```
As a user, I want a button                    # Too vague
As a developer, I want to use Sidekiq         # Technical, not user-focused
The system should create tasks                # Not user-story format
```

### Acceptance Criteria (Detailed Requirements)

For each user story, define acceptance criteria using Gherkin scenarios.

**Gherkin Format**:
```gherkin
Feature: [Feature name and brief description]
  [Optional: Longer description explaining business value]

  Scenario: [Specific situation to test]
    Given [initial context/preconditions]
    And [additional context]
    When [action/event occurs]
    Then [expected outcome]
    And [additional expectations]
```

### Complete Example for Manifest

```gherkin
Feature: Zone-Based Task Bundling
  As a dispatch system
  I need to bundle delivery tasks by origin and destination zones
  So that carriers can deliver multiple packages efficiently

  Scenario: Tasks from same origin zone to same destination zone are bundled
    Given a Zone "Riyadh-North" exists as origin
    And a Zone "Riyadh-East" exists as destination
    And 3 pending tasks exist from "Riyadh-North" to "Riyadh-East"
    When the bundling service runs
    Then the tasks should be grouped into 1 bundle
    And the bundle status should be "ready_for_dispatch"

  Scenario: Tasks to different destination zones are not bundled together
    Given a Zone "Riyadh-North" exists as origin
    And a Zone "Riyadh-East" exists as destination
    And a Zone "Riyadh-West" exists as destination
    And 2 pending tasks exist from "Riyadh-North" to "Riyadh-East"
    And 1 pending task exists from "Riyadh-North" to "Riyadh-West"
    When the bundling service runs
    Then 2 separate bundles should be created

  Scenario: Express tasks are not bundled with Next-Day tasks
    Given 2 Express tasks exist for Zone "Riyadh-East"
    And 2 Next-Day tasks exist for Zone "Riyadh-East"
    When the bundling service runs
    Then Express tasks should be in a separate bundle
    And Next-Day tasks should be in a separate bundle

  Scenario: Single task creates single-item bundle
    Given only 1 pending task exists for Zone "Riyadh-East"
    When the bundling service runs
    Then the task should be bundled alone
    And the bundle should be dispatchable
```

## Gherkin Best Practices

### 1. Use Domain Language
Use terms from Manifest's ubiquitous language:
```gherkin
# GOOD
Given a Merchant "Salla Store" exists for the Account
When creating a Task with delivery_type "express"
And the recipient Zone is "Jeddah-Central"

# BAD
Given a store exists
When making a delivery order
And the area is downtown
```

### 2. One Scenario, One Behavior
```gherkin
# GOOD - Tests one thing
Scenario: OTP verification completes Express delivery
  Given a Task with status "out_for_delivery"
  And the Task requires OTP verification
  When the Carrier submits correct OTP "1234"
  Then the Task status should be "delivered"

# BAD - Tests multiple things
Scenario: OTP and payment and status
  Given a Task exists
  When carrier submits OTP and collects cash
  Then multiple things happen
```

### 3. Use Background for Common Setup
```gherkin
Feature: Carrier Task Assignment

  Background:
    Given an Account "Acme Logistics" exists
    And a Carrier "Mohammed" is active for the Account
    And the following Zones exist:
      | Zone Name      | City    |
      | Riyadh-North   | Riyadh  |
      | Riyadh-East    | Riyadh  |

  Scenario: Carrier assigned to tasks within their zones
    Given "Mohammed" is assigned to Zone "Riyadh-North"
    And a Task exists for Zone "Riyadh-North"
    When auto-assigning carriers
    Then "Mohammed" should be assigned to the Task

  Scenario: Carrier not assigned to tasks outside their zones
    Given "Mohammed" is assigned to Zone "Riyadh-North"
    And a Task exists for Zone "Riyadh-East"
    When auto-assigning carriers
    Then "Mohammed" should not be assigned to the Task
```

### 4. Use Scenario Outlines for Multiple Cases
```gherkin
Scenario Outline: Task status transitions
  Given a Task with status "<current_status>"
  When the event "<event>" occurs
  Then the Task status should be "<new_status>"

  Examples:
    | current_status     | event              | new_status         |
    | pending            | dispatch           | dispatched         |
    | dispatched         | pickup             | picked_up          |
    | picked_up          | out_for_delivery   | out_for_delivery   |
    | out_for_delivery   | deliver            | delivered          |
    | out_for_delivery   | fail_delivery      | failed_attempt     |
    | failed_attempt     | return_to_facility | sorting_facility   |
```

## Requirements Categories

### 1. Functional Requirements
What the system must do.

**User Story**:
```
As an Account Admin
I want to view all tasks ranked by priority and age
So that I can identify delayed deliveries
```

**Gherkin Scenario**:
```gherkin
Scenario: Tasks sorted by priority then creation date
  Given the following Tasks exist:
    | Reference | Priority | Created At |
    | TASK-001  | high     | 2 days ago |
    | TASK-002  | normal   | 1 day ago  |
    | TASK-003  | high     | 1 day ago  |
  When viewing the task queue
  Then the order should be:
    | Rank | Reference |
    | 1    | TASK-001  |
    | 2    | TASK-003  |
    | 3    | TASK-002  |
```

### 2. Non-Functional Requirements
How the system should behave.

**Categories**:
- Performance (response time, throughput)
- Security (authentication, authorization)
- Reliability (uptime, error handling)
- Scalability (concurrent users, data volume)
- Maintainability (code quality, documentation)

**Format**:
```
The system shall [requirement]
Measured by [metric]
```

**Examples**:
```
The system shall process webhook deliveries within 500ms
Measured by: Average response time for POST /api/v1/tasks

The system shall handle 10,000 concurrent task updates
Measured by: Load testing with simulated peak traffic

The system shall maintain 99.9% uptime
Measured by: Monthly uptime percentage

The system shall process SMS notifications within 5 seconds
Measured by: Time from task status change to SMS delivery
```

### 3. Business Rules
Constraints and policies from the domain.

```gherkin
Feature: 3PL Handoff Rules
  Business Rule: Tasks destined for cities without carrier coverage
  must be handed off to integrated 3PL providers after sorting.

  Scenario: Task handed to 3PL when destination city has no coverage
    Given the Account has no Carriers covering "Dammam"
    And the Account has 3PL integration with "SMSA" for "Dammam"
    And a Task exists with destination city "Dammam"
    When the Task arrives at sorting facility
    Then a 3PL label should be generated via "SMSA"
    And the Task should transition to "awaiting_3pl_pickup"
```

## Requirements Organization

### Directory Structure
```
requirements/
├── user-stories/
│   ├── merchant-stories.md
│   ├── carrier-stories.md
│   ├── admin-stories.md
│   └── recipient-stories.md
├── features/
│   ├── task-management.feature
│   ├── zone-bundling.feature
│   ├── carrier-dispatch.feature
│   ├── 3pl-integration.feature
│   ├── billing.feature
│   └── notifications.feature
├── business-rules/
│   ├── delivery-rules.md
│   ├── bundling-policies.md
│   └── cod-collection-rules.md
└── non-functional/
    ├── performance-requirements.md
    ├── security-requirements.md
    └── scalability-requirements.md
```

## Requirement Quality Checklist

Use the **INVEST** criteria for user stories:
- [ ] **Independent**: Can be developed independently
- [ ] **Negotiable**: Details can be discussed
- [ ] **Valuable**: Delivers value to users
- [ ] **Estimable**: Can estimate effort
- [ ] **Small**: Can be completed in one sprint
- [ ] **Testable**: Can verify when done

For Gherkin scenarios:
- [ ] Uses Manifest domain language
- [ ] Tests one specific behavior
- [ ] Has clear Given-When-Then structure
- [ ] Includes edge cases and error conditions
- [ ] Is executable (can be automated with Cucumber/RSpec)

## Example Mapping (Discovery Technique)

Before writing requirements, use Example Mapping to explore:

```
Rule: Express deliveries require OTP verification

Examples:
  ✓ Correct OTP submitted → Task delivered
  ✓ Incorrect OTP submitted → Rejected, retry allowed
  ✗ 3 failed OTP attempts → Task marked for callback
  ✗ OTP expired after 10 minutes → New OTP generated

Questions:
  ? What if recipient is unavailable and alternative contact accepts?
  ? Should OTP be required for zero-value (non-COD) deliveries?
  ? How to handle OTP when recipient has no phone?
```

Then write Gherkin scenarios for each example + questions.

## Integration with TDD

Requirements drive test development:

1. **Write User Story**: Define what's needed
2. **Write Gherkin Scenarios**: Define acceptance criteria
3. **Generate Step Definitions**: Convert scenarios to RSpec/Cucumber
4. **Implement TDD**: Red-Green-Refactor cycle

**Traceability**:
```
User Story → Gherkin Scenario → Cucumber/RSpec Test → Service Object Implementation
```

## Manifest Domain Examples

### Example 1: Cash on Delivery Collection
```
User Story:
As an Account Admin
I want COD amounts automatically tracked in Carrier wallets
So that I can reconcile cash collections accurately

Acceptance Criteria:
```

```gherkin
Feature: COD Wallet Tracking
  Cash collected by Carriers is tracked in their Wallet
  and must be reconciled before payout.

  Scenario: COD amount added to Carrier wallet on delivery
    Given a Carrier "Ahmed" has wallet balance 0 SAR
    And a Task with COD amount 150 SAR assigned to "Ahmed"
    When "Ahmed" marks the Task as delivered
    Then "Ahmed" wallet balance should be 150 SAR
    And a wallet transaction "cod_collection" should be recorded

  Scenario: Multiple COD collections accumulate
    Given a Carrier "Ahmed" has wallet balance 200 SAR
    And a Task with COD amount 100 SAR assigned to "Ahmed"
    When "Ahmed" marks the Task as delivered
    Then "Ahmed" wallet balance should be 300 SAR
```

### Example 2: SMS Notification Templates
```
User Story:
As an Account Admin
I want to customize SMS templates with placeholders
So that recipients receive branded, relevant notifications

Acceptance Criteria:
```

```gherkin
Feature: SMS Template Processing

  Scenario: Template placeholders are replaced with task data
    Given an SMS template with body:
      """
      Your order {{task_reference}} is out for delivery. 
      Track: {{tracking_url}}
      """
    And a Task with reference "ORD-12345"
    And tracking URL "https://track.manifest.sa/ORD-12345"
    When sending the delivery notification
    Then the SMS body should be:
      """
      Your order ORD-12345 is out for delivery. 
      Track: https://track.manifest.sa/ORD-12345
      """

  Scenario: Missing placeholder data handled gracefully
    Given an SMS template with body "Contact: {{alternative_phone}}"
    And a Task with no alternative contact
    When sending the notification
    Then the placeholder should be replaced with empty string
    And no error should be raised
```

### Example 3: Multi-Tenant Data Isolation
```gherkin
Feature: Account Data Isolation
  All data must be scoped to the owning Account
  to ensure multi-tenant security.

  Scenario: Tasks only visible to owning Account
    Given Account "Acme" has 5 Tasks
    And Account "Beta" has 3 Tasks
    When "Acme" admin queries their Tasks
    Then only 5 Tasks should be returned
    And no Tasks from "Beta" should be visible

  Scenario: Carrier cannot access other Account's Tasks
    Given Carrier "Ahmed" belongs to Account "Acme"
    And a Task belongs to Account "Beta"
    When "Ahmed" attempts to view the Task
    Then access should be denied
    And an authorization error should be logged
```

## Response Format

When writing requirements:
1. Start with a user story to capture WHO, WHAT, WHY
2. Add Gherkin scenarios for detailed acceptance criteria
3. Include happy path, edge cases, and error conditions
4. Use Manifest domain language consistently
5. Ensure scenarios are testable and executable
6. Link requirements to business rules
7. Consider non-functional requirements

## Tools for Requirements Management

- **BDD Tools**: RSpec, Cucumber (Ruby)
- **Documentation**: Markdown, Gherkin `.feature` files
- **Collaboration**: Example Mapping sessions
- **Traceability**: Link stories → scenarios → tests → code
