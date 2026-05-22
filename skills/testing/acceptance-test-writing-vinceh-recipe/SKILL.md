---
name: acceptance-test-writing
description: Guide for writing high-quality acceptance criteria and acceptance tests using industry-standard BDD (Behavior-Driven Development) and ATDD (Acceptance Test-Driven Development) practices. Use this skill when creating acceptance criteria for user stories, writing Gherkin scenarios, or implementing acceptance test specifications following Given-When-Then format.
---

# Acceptance Test Writing

## Overview

To write effective acceptance criteria and acceptance tests, follow industry-standard BDD (Behavior-Driven Development) and ATDD (Acceptance Test-Driven Development) practices. This skill guides the creation of clear, testable, user-focused acceptance criteria using Gherkin syntax and best practices.

Acceptance criteria define the conditions that must be met for a user story to be considered complete. Well-written acceptance criteria serve as:
- A shared understanding between developers, testers, and stakeholders
- Executable specifications that can be automated as tests
- Documentation of expected system behavior
- Definition of "done" for user stories

## Decision Tree: Choosing Your Approach

```
User Request → What are you creating?
    |
    ├─ Writing acceptance criteria for a user story?
    │   ├─ Simple validation rules or constraints? → Use Rule-Oriented Format
    │   └─ User interactions or workflows? → Use Given-When-Then Format
    │
    ├─ Converting existing requirements to acceptance criteria?
    │   └─ Follow Workflow: Analyze → Identify Scenarios → Write Criteria → Validate
    │
    ├─ Reviewing existing acceptance criteria?
    │   └─ Use Quality Validation Checklist (below)
    │
    └─ Learning or providing guidance on acceptance testing?
        └─ Load appropriate reference file (gherkin-guide.md, anti-patterns.md, or examples.md)
```

## Workflow: Writing Acceptance Criteria

Follow this process to create high-quality acceptance criteria from user stories or requirements.

### Step 1: Analyze the User Story

To begin, understand the user story thoroughly:

1. **Identify the user role**: Who is performing the action?
2. **Identify the goal**: What does the user want to accomplish?
3. **Identify the value**: Why does the user want this?
4. **Identify the context**: What are the preconditions and constraints?

**User Story Format:**
```
As a [role]
I want to [goal]
So that [benefit]
```

### Step 2: Identify Scenarios

To define test scenarios, consider:

1. **Happy path**: The ideal, successful flow
2. **Error cases**: What can go wrong?
3. **Edge cases**: Boundary conditions and special cases
4. **Alternative paths**: Different ways to achieve the same goal

**Ask these questions:**
- What are the success criteria?
- What inputs are valid? What inputs are invalid?
- What are the boundary conditions?
- What happens when external dependencies fail?
- Are there permission or authorization requirements?
- Are there performance requirements?

### Step 3: Choose Format

Select the appropriate format based on the scenario type:

#### **Given-When-Then Format** (Preferred for most scenarios)

Use Gherkin syntax for behavior-driven scenarios:

```gherkin
Scenario: [Brief description]
  Given [precondition/initial context]
  And [additional precondition]
  When [action/trigger - EXACTLY ONE]
  Then [expected outcome]
  And [additional expected outcome]
```

**Best for:**
- User interactions and workflows
- Integration with BDD tools (Cucumber, SpecFlow, Behave)
- Scenarios requiring context setup
- Complex behavior with multiple steps

**Load [gherkin-guide.md](references/gherkin-guide.md) for complete Gherkin syntax reference.**

#### **Rule-Oriented Format**

Use checklist format for validation rules and constraints:

```
Acceptance Criteria:
- [Criterion 1]
- [Criterion 2]
- [Criterion 3]
```

**Best for:**
- Validation rules
- System constraints
- Simple requirements lists
- Configuration requirements

### Step 4: Write the Criteria

To write effective acceptance criteria, follow these principles:

#### **Core Writing Principles**

1. **Use Domain Language**
   - Write in business terms, not technical implementation
   - Use vocabulary from the user's domain
   - Avoid references to UI elements (button IDs, CSS classes)
   - Avoid technical details (APIs, databases, frameworks)

2. **Be Specific and Measurable**
   - Use concrete values, not vague terms
   - Bad: "The system should respond quickly"
   - Good: "The search completes in under 1 second"

3. **One Behavior Per Scenario**
   - Each scenario tests a single, specific behavior
   - Keep scenarios focused and independent
   - Split complex scenarios into multiple scenarios

4. **Write from User's Perspective**
   - Focus on what the user experiences
   - Describe observable outcomes
   - Avoid implementation details

5. **Use Active Voice**
   - Write "the user clicks submit" not "the submit button is clicked"
   - Make it clear who/what performs each action

6. **Single Trigger in When Clause**
   - The When clause should contain EXACTLY ONE action/trigger
   - Multiple setup steps belong in Given
   - Multiple outcomes belong in Then

#### **Example: Well-Written Acceptance Criteria**

```gherkin
Scenario: Successful user login with valid credentials
  Given a user account exists with email "user@example.com"
  And the user is on the login page
  When the user enters email "user@example.com" and password "SecurePass123"
  And the user clicks "Login"
  Then the user is redirected to the dashboard
  And the welcome message displays "Welcome back, John"
  And a user session is established

Scenario: Login fails with incorrect password
  Given a user account exists with email "user@example.com"
  When the user enters email "user@example.com" and incorrect password
  And the user clicks "Login"
  Then the error message "Invalid email or password" is displayed
  And the user remains on the login page
  And no session is established
  And the failed attempt is logged

Scenario: Account locks after multiple failed attempts
  Given a user account exists with email "user@example.com"
  And the account has 2 previous failed login attempts
  When the user enters incorrect credentials and clicks "Login"
  Then the account is locked for 15 minutes
  And the message "Account temporarily locked" is displayed
  And a security notification email is sent to the user
```

### Step 5: Validate Quality

To ensure quality, check each acceptance criterion against these standards:

#### **Quality Checklist**

- [ ] **Testable**: Can be verified with clear pass/fail result
- [ ] **Clear**: No ambiguity or room for interpretation
- [ ] **Specific**: Uses concrete examples and values
- [ ] **Independent**: Can be tested separately from other scenarios
- [ ] **User-Focused**: Written from user's perspective, not implementation
- [ ] **Complete**: Covers happy path, errors, and edge cases
- [ ] **Measurable**: Includes specific values, timeframes, or criteria
- [ ] **Concise**: Not more than 6-10 criteria per user story

#### **Format Checklist**

- [ ] Uses active voice (not passive)
- [ ] Uses domain language (not technical terms)
- [ ] One trigger per When clause (for Given-When-Then)
- [ ] Each scenario tests one behavior
- [ ] No UI element references (button IDs, CSS classes, HTML elements)
- [ ] No technical implementation details (API endpoints, database tables)
- [ ] No vague terms ("properly", "correctly", "quickly" without definition)

#### **Coverage Checklist**

- [ ] Happy path scenario exists
- [ ] Error/failure scenarios exist
- [ ] Edge cases and boundary conditions covered
- [ ] User permissions/authorization considered (if applicable)
- [ ] Performance requirements specified (if applicable)
- [ ] Accessibility requirements specified (if applicable)

**If any criteria fail validation, revise using the anti-patterns guide.**

## Common Patterns

### Pattern 1: Form Validation

```gherkin
Scenario: Submit form with all valid data
  Given the user is on the contact form
  When the user enters valid data and submits
  Then the form is submitted successfully
  And a confirmation message appears
  And the form fields are cleared

Scenario: Reject form with invalid email
  Given the user is on the contact form
  When the user enters invalid email format and submits
  Then the form is not submitted
  And an error "Invalid email format" appears
  And the email field is highlighted
```

### Pattern 2: Authentication

```gherkin
Scenario: Successful authentication
  Given valid user credentials exist
  When the user authenticates with valid credentials
  Then authentication succeeds
  And a session is established

Scenario: Failed authentication
  Given valid user credentials exist
  When the user authenticates with invalid credentials
  Then authentication fails
  And an error message is displayed
  And no session is established
```

### Pattern 3: Data Filtering

```gherkin
Scenario: Filter returns matching results
  Given the dataset contains [X] items
  And [Y] items match the filter criteria
  When the user applies the filter
  Then [Y] matching items are displayed
  And the count shows "[Y] results"

Scenario: Filter returns no results
  Given the dataset contains items
  And no items match the filter criteria
  When the user applies the filter
  Then the message "No results found" is displayed
  And the user can clear the filter
```

### Pattern 4: Error Handling

```gherkin
Scenario: Handle external service failure gracefully
  Given the user performs an action requiring external service
  And the external service is unavailable
  When the user attempts the action
  Then an error message "Service temporarily unavailable" is displayed
  And the user can retry the action
  And the system logs the failure
```

## Quick Reference: Signs of Quality

### ✅ Good Acceptance Criteria
- Describes user behavior and outcomes
- Uses domain language everyone understands
- Specific and measurable
- One behavior per scenario
- Single trigger in When clause
- Written in active voice
- Testable with clear pass/fail
- Independent and self-contained
- Includes relevant context
- Covers happy path, errors, and edge cases

### ❌ Poor Acceptance Criteria
- References UI elements (button IDs, CSS classes)
- Mentions technical implementation (APIs, databases)
- Uses vague terms ("properly", "quickly", "correctly")
- Tests multiple behaviors in one scenario
- Has multiple When clauses
- Written in passive voice
- Uses negative statements excessively
- Cannot be tested with clear pass/fail
- Depends on other scenarios
- Omits edge cases or error scenarios

## Resources

This skill includes reference materials and templates to support acceptance criteria creation:

### references/gherkin-guide.md
Complete reference for Gherkin syntax with detailed explanations of Given-When-Then format, keywords (Background, Scenario Outline, Examples), best practices, and automation integration guidance.

**Load when:** Writing Gherkin scenarios, learning Gherkin syntax, or needing syntax reference.

### references/anti-patterns.md
Comprehensive guide to common mistakes when writing acceptance criteria, including 14 anti-patterns with bad vs. good examples showing implementation-focused criteria, UI coupling, vague language, multiple behaviors, and more.

**Load when:** Reviewing acceptance criteria, learning what to avoid, or troubleshooting quality issues.

### references/examples.md
Real-world acceptance criteria examples across domains: e-commerce, authentication, forms, APIs, data management, reporting, notifications, accessibility, and performance. Includes both Given-When-Then and rule-oriented formats.

**Load when:** Looking for examples, learning by example, or finding patterns for specific domains.

### assets/acceptance-criteria-template.md
Ready-to-use template for teams to create acceptance criteria. Includes user story format, both Given-When-Then and rule-oriented formats, writing checklist, quality verification, and quick-start examples.

**Use when:** Providing a template to the user or their team for creating new acceptance criteria.

## Tips for Success

1. **Collaborate**: Write acceptance criteria with developers, testers, AND business stakeholders together
2. **Start Early**: Define acceptance criteria before development begins (ATDD approach)
3. **Keep Simple**: Use short, concise sentences; avoid complex conjunctions
4. **Be Consistent**: Follow the same format and style across all stories
5. **Iterate**: Review and refine criteria as understanding improves
6. **Automate**: Design criteria to be automatable with BDD tools
7. **Focus on Value**: Every criterion should tie back to user value

## When to Load Reference Files

To optimize context usage, load reference files strategically:

- **Load gherkin-guide.md** when:
  - Writing Given-When-Then scenarios
  - User asks about Gherkin syntax
  - Need detailed syntax reference
  - Working with Scenario Outlines or Examples tables

- **Load anti-patterns.md** when:
  - Reviewing or critiquing existing acceptance criteria
  - Acceptance criteria seem unclear or problematic
  - Teaching what NOT to do
  - Debugging quality issues

- **Load examples.md** when:
  - User asks for examples
  - Working in a specific domain (e-commerce, auth, forms, etc.)
  - Learning by example
  - Need inspiration for scenario structure

- **Use template (assets/acceptance-criteria-template.md)** when:
  - User needs a starting template
  - Creating acceptance criteria from scratch
  - Providing guidance to a team
  - Quick reference needed
