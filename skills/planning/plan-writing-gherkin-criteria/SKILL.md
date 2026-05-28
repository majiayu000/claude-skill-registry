---
description: Guide for writing Gherkin acceptance criteria using Given-When-Then syntax for testable requirements. Covers scenario structure, background blocks, scenario outlines with examples tables, common patterns for authentication/CRUD/validation/error handling, and best practices for clear testable specifications. Essential for writing user stories and plan acceptance criteria
---

# Gherkin Acceptance Criteria Skill

## Purpose

This Skill provides comprehensive guidance for writing **Gherkin acceptance criteria** using Given-When-Then syntax to create clear, testable specifications for features and user stories.

**When to use this Skill:**

- Writing acceptance criteria for user stories
- Defining testable requirements in plans
- Specifying expected behavior for features
- Creating scenarios for validation testing
- Documenting edge cases and error handling
- Communicating requirements to developers and testers

## Core Concepts

### What is Gherkin?

**Gherkin** is a structured language for writing acceptance criteria using Given-When-Then syntax. It enables:

- **Clear communication**: Non-technical stakeholders understand requirements
- **Testable specifications**: Scenarios map directly to automated tests
- **Complete coverage**: All scenarios and edge cases documented
- **Unambiguous expectations**: No room for interpretation

### Given-When-Then Structure

**Anatomy of a scenario**:

```gherkin
Scenario: [Brief description of scenario]
  Given [Initial context/preconditions]
  When [Action or event occurs]
  Then [Expected outcome/postconditions]
```

**Breakdown**:

- **Given**: Sets up the context (initial state, preconditions, setup)
- **When**: Describes the action or event (user action, system event, trigger)
- **Then**: Specifies expected outcome (assertions, verification, results)

**Example**:

```gherkin
Scenario: User logs in with valid credentials
  Given a registered user with email "alice@example.com" and password "secure123"
  When the user submits login form with correct credentials
  Then the user should be redirected to dashboard
  And the user should see welcome message "Welcome back, Alice!"
  And session token should be stored in cookies
```

## Basic Scenario Patterns

### Pattern 1: Simple Success Path

**Use case**: Straightforward happy path with clear steps

```gherkin
Scenario: Create new blog post
  Given I am logged in as a content editor
  When I navigate to "Create New Post" page
  And I fill in the title with "My First Post"
  And I fill in the content with "This is my content"
  And I click "Publish" button
  Then I should see success message "Post published successfully"
  And the post should appear in my posts list
  And the post should have status "Published"
```

### Pattern 2: Error Handling

**Use case**: Invalid input or error conditions

```gherkin
Scenario: Reject login with invalid password
  Given a registered user with email "alice@example.com"
  When the user submits login form with incorrect password
  Then the user should remain on login page
  And error message should display "Invalid email or password"
  And login attempt should be logged
  And no session token should be created
```

### Pattern 3: Boundary Conditions

**Use case**: Testing edge cases and limits

```gherkin
Scenario: Prevent posts with titles exceeding maximum length
  Given I am logged in as a content editor
  And maximum title length is 200 characters
  When I attempt to create post with title of 201 characters
  Then I should see validation error "Title must be 200 characters or less"
  And the post should not be created
  And I should remain on post creation page
```

## Advanced Gherkin Features

### Background Block

**Purpose**: Share common setup across multiple scenarios

```gherkin
Feature: User Authentication

Background:
  Given the application is running
  And the database contains the following users:
    | email              | password   | role   |
    | admin@example.com  | admin123   | admin  |
    | user@example.com   | user123    | user   |

Scenario: Admin login
  When user "admin@example.com" logs in with password "admin123"
  Then the user should have admin privileges

Scenario: Regular user login
  When user "user@example.com" logs in with password "user123"
  Then the user should have user privileges
```

**Rules**:

- Background runs before EACH scenario in the feature
- Use for common setup that applies to all scenarios
- Don't put scenario-specific setup in Background

### Scenario Outline with Examples

**Purpose**: Test same scenario with multiple data sets

```gherkin
Scenario Outline: Validate email format
  Given I am on registration page
  When I enter email "<email>"
  And I submit the form
  Then I should see "<result>"

  Examples:
    | email                | result                          |
    | valid@example.com    | Registration successful         |
    | invalid              | Please enter a valid email      |
    | missing@             | Please enter a valid email      |
    | @missing.com         | Please enter a valid email      |
    | spaces @example.com  | Please enter a valid email      |
```

**Benefits**:

- DRY (Don't Repeat Yourself) - One scenario tests multiple cases
- Easy to add new test cases (just add row to table)
- Clear documentation of all tested variations

### Data Tables

**Purpose**: Pass structured data to steps

```gherkin
Scenario: Bulk import users
  Given I am logged in as admin
  When I import the following users:
    | name    | email              | role   |
    | Alice   | alice@example.com  | editor |
    | Bob     | bob@example.com    | viewer |
    | Charlie | charlie@example.com| editor |
  Then all 3 users should be created
  And I should see success message "3 users imported successfully"
  And each user should receive welcome email
```

## Common Domain Patterns

### Authentication & Authorization

```gherkin
Feature: User Authentication

Scenario: Successful login with valid credentials
  Given a user with email "user@example.com" and password "secure123"
  When the user submits login credentials
  Then the user should be authenticated
  And session token should be created
  And user should be redirected to dashboard

Scenario: Rejected login with invalid credentials
  Given a user with email "user@example.com"
  When the user submits incorrect password
  Then authentication should fail
  And error message "Invalid credentials" should display
  And no session token should be created

Scenario: Access protected resource without authentication
  Given the user is not logged in
  When the user attempts to access "/dashboard"
  Then the user should be redirected to "/login"
  And error message "Please log in to continue" should display
```

### CRUD Operations

```gherkin
Feature: Article Management

Scenario: Create new article
  Given I am authenticated as editor
  When I create article with title "Test" and content "Content"
  Then article should be saved to database
  And article should have status "draft"
  And I should see success message "Article created"

Scenario: Update existing article
  Given I am authenticated as editor
  And article "Test" exists with id 123
  When I update article 123 title to "Updated Test"
  Then article 123 title should be "Updated Test"
  And article 123 updated_at timestamp should be current time
  And I should see success message "Article updated"

Scenario: Delete article
  Given I am authenticated as editor
  And article "Test" exists with id 123
  When I delete article 123
  Then article 123 should not exist in database
  And I should see success message "Article deleted"
  And I should be redirected to articles list
```

### Form Validation

```gherkin
Feature: User Registration Form Validation

Scenario Outline: Email validation
  Given I am on registration page
  When I enter email "<email>"
  And I submit the form
  Then I should see validation result "<result>"

  Examples:
    | email               | result                        |
    | valid@example.com   | Success                       |
    | invalid             | Invalid email format          |
    | missing@domain      | Invalid email format          |
    | user@              | Invalid email format          |

Scenario: Password strength validation
  Given I am on registration page
  When I enter password "weak"
  Then I should see error "Password must be at least 8 characters"
  And submit button should be disabled

Scenario: Matching password confirmation
  Given I am on registration page
  When I enter password "secure123"
  And I enter password confirmation "different"
  Then I should see error "Passwords do not match"
  And submit button should be disabled
```

### API Responses

```gherkin
Feature: REST API User Endpoints

Scenario: GET user by ID
  Given user with id 123 exists in database
  When client sends GET request to "/api/users/123"
  Then response status should be 200
  And response body should contain:
    """
    {
      "id": 123,
      "name": "Alice",
      "email": "alice@example.com"
    }
    """

Scenario: POST create new user
  Given client is authenticated as admin
  When client sends POST request to "/api/users" with body:
    """
    {
      "name": "Bob",
      "email": "bob@example.com",
      "password": "secure123"
    }
    """
  Then response status should be 201
  And response should contain user id
  And user should exist in database
  And welcome email should be sent to "bob@example.com"
```

## Best Practices

### Writing Clear Scenarios

**DO**:

- Use business language (not technical jargon)
- Write from user perspective
- Focus on WHAT, not HOW
- Keep scenarios independent
- Make scenarios atomic (one behavior per scenario)
- Use concrete examples (not abstract concepts)

**DON'T**:

- Mix UI details with business logic
- Create scenario dependencies
- Write implementation details
- Use ambiguous language
- Combine multiple behaviors in one scenario

**Example**:

```gherkin
# ✅ Good - Business language, clear behavior
Scenario: Purchase item with sufficient balance
  Given customer has account balance of $100
  When customer purchases item for $30
  Then customer balance should be $70
  And purchase should be confirmed

# ❌ Bad - Technical details, implementation-focused
Scenario: Click buy button and update database
  Given database table "accounts" has row with balance column = 100
  When user clicks button with id "btn-purchase"
  And system executes SQL UPDATE statement
  Then database table "accounts" balance column should equal 70
```

### Scenario Independence

**Each scenario should be runnable in isolation** (no dependencies on other scenarios).

```gherkin
# ❌ Bad - Scenario depends on previous scenario
Scenario: Create user
  When I create user "Alice"
  Then user "Alice" should exist

Scenario: Update user email (DEPENDS on previous scenario)
  When I update user "Alice" email to "newemail@example.com"
  Then user "Alice" email should be "newemail@example.com"

# ✅ Good - Each scenario independent
Scenario: Create user
  When I create user with name "Alice" and email "alice@example.com"
  Then user should exist in database

Scenario: Update user email
  Given user "Alice" exists with email "alice@example.com"
  When I update user email to "newemail@example.com"
  Then user email should be "newemail@example.com"
```

### Avoiding UI Coupling

**Focus on behavior, not UI elements**.

```gherkin
# ❌ Bad - Coupled to UI implementation
Scenario: Login
  Given I am on "https://example.com/login"
  When I type "user@example.com" into input field with id "email-input"
  And I type "password" into input field with id "password-input"
  And I click button with class "btn-submit"
  Then I should be redirected to "https://example.com/dashboard"

# ✅ Good - Focused on business behavior
Scenario: Login with valid credentials
  Given I am on login page
  When I log in with email "user@example.com" and password "password"
  Then I should see the dashboard
  And I should be authenticated
```

### Declarative vs Imperative Style

**Prefer declarative style** (what should happen) over imperative style (how to do it).

```gherkin
# ❌ Imperative - Describes HOW
Scenario: User registration
  When I click "Sign Up" link
  And I fill in "Name" with "Alice"
  And I fill in "Email" with "alice@example.com"
  And I fill in "Password" with "secure123"
  And I fill in "Confirm Password" with "secure123"
  And I click "Register" button
  Then I should see "Registration successful"

# ✅ Declarative - Describes WHAT
Scenario: User registration
  When I register with name "Alice", email "alice@example.com", and password "secure123"
  Then registration should succeed
  And I should receive welcome email
  And I should be logged in automatically
```

## Common Mistakes

### ❌ Mistake 1: Too many steps per scenario

**Problem**: Scenarios with 15+ steps become hard to read and maintain

**Solution**: Break into multiple scenarios or use Background for common setup

```gherkin
# ❌ Too long
Scenario: Complete purchase workflow
  Given I am on homepage
  When I search for "laptop"
  And I click first result
  And I click "Add to Cart"
  And I click "View Cart"
  And I click "Checkout"
  And I fill in shipping address
  And I fill in billing address
  And I select payment method
  And I enter card details
  And I click "Place Order"
  Then order should be confirmed
  # (continues for many more steps...)

# ✅ Better - Break into multiple scenarios
Scenario: Add item to cart
  When I search for "laptop" and add first result to cart
  Then cart should contain 1 item

Scenario: Complete checkout with valid payment
  Given cart contains "laptop" item
  When I complete checkout with shipping address and payment details
  Then order should be placed successfully
```

### ❌ Mistake 2: Asserting internal implementation

**Problem**: Coupling tests to implementation details that may change

```gherkin
# ❌ Bad - Asserts internal state
Then user object should have "lastLoginTimestamp" property
And "sessions" database table should have new row

# ✅ Good - Asserts observable behavior
Then user should be logged in
And user session should be active
```

### ❌ Mistake 3: Ambiguous language

**Problem**: Vague language open to interpretation

```gherkin
# ❌ Ambiguous
Then the system should respond quickly

# ✅ Specific
Then the response should be received within 200ms
```

### ❌ Mistake 4: Testing multiple behaviors in one scenario

**Problem**: Scenario tests multiple unrelated behaviors

```gherkin
# ❌ Bad - Multiple behaviors
Scenario: User management and article creation
  Given I create user "Alice"
  Then user "Alice" should exist
  And I create article "Test"
  Then article "Test" should exist

# ✅ Good - Separate scenarios
Scenario: Create new user
  When I create user "Alice"
  Then user "Alice" should exist in system

Scenario: Create new article
  Given I am logged in as editor
  When I create article "Test"
  Then article "Test" should be published
```

## Integration with Plans

### Plan Acceptance Criteria Format

Plans use Gherkin for phase-level acceptance criteria:

```gherkin
## Acceptance Criteria

Scenario: Phase 1 foundation complete
  Given Skills infrastructure is required
  When Phase 1 implementation is complete
  Then .opencode/skill/ directory should exist with README and TEMPLATE
  And 3 Skills should be created (maker-checker-fixer, color-accessibility, repository-architecture)
  And AI Agents Convention should document skills: frontmatter field
  And all 3 Skills should auto-load when relevant tasks described
  And existing agents should continue working without modification
```

### User Story Acceptance Criteria

User stories in requirements use detailed Gherkin scenarios:

```gherkin
User Story: As a content editor, I want to preview articles before publishing

Acceptance Criteria:

Scenario: Preview unpublished article
  Given I am logged in as content editor
  And I have draft article "Test Article"
  When I click "Preview" button for "Test Article"
  Then I should see article preview in new tab
  And preview should render markdown correctly
  And preview should display "DRAFT" watermark

Scenario: Preview shows latest changes
  Given I am editing article "Test Article"
  When I make changes to article content
  And I click "Preview" without saving
  Then preview should reflect unsaved changes
  And original article should remain unchanged in database
```

## Reference Documentation

**Related Conventions**:

- [Plans Organization](../../../governance/conventions/project/plans-organization.md) - Acceptance criteria in plans
- [Content Quality Principles](../../../governance/conventions/content/quality.md) - Clear specification writing

**Related Skills**:

- `trunk-based-development` - Understanding git workflow for implementing features
- `maker-checker-fixer-pattern` - Validation workflow that uses acceptance criteria

**Related Agents**:

- `plan__maker` - Creates plans with Gherkin acceptance criteria
- `plan__checker` - Validates acceptance criteria format
- `plan__execution-checker` - Verifies acceptance criteria are met

**External Resources**:

- [Official Gherkin Reference](https://cucumber.io/docs/gherkin/reference/) - Complete Gherkin syntax
- [Writing Better Gherkin](https://cucumber.io/docs/bdd/better-gherkin/) - Best practices guide

---

This Skill packages essential Gherkin acceptance criteria knowledge for writing clear, testable specifications. For additional patterns and examples, consult external Gherkin resources.

## References

**Primary Convention**: [Acceptance Criteria Convention](../../../governance/development/infra/acceptance-criteria.md)

**Related Conventions**:

- [Plans Organization](../../../governance/conventions/project/plans-organization.md) - Using Gherkin in plans
- [Maker-Checker-Fixer Pattern](../../../governance/development/pattern/maker-checker-fixer.md) - Validation workflow

**Related Skills**:

- `wow__practicing-trunk-based-development` - Git workflow for implementing features
- `wow__applying-maker-checker-fixer` - Validation workflow that uses acceptance criteria
