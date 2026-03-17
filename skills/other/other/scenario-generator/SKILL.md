---
name: scenario-generator
description: Generate comprehensive test scenarios, user stories, and acceptance criteria from requirements and specifications. Use this skill when planning testing efforts, writing user stories, creating test cases, documenting acceptance criteria, exploring edge cases, designing test coverage, or translating requirements into actionable scenarios. Supports BDD (Given-When-Then), Gherkin syntax, user story format, and test case documentation.
---

# Scenario Generator

Systematically generate test scenarios, user stories, and acceptance criteria from requirements. Ensures comprehensive coverage of functional paths, edge cases, and error conditions.

## Core Capabilities

### 1. User Story Generation

Create well-formed user stories:
- **As-a/I-want/So-that format** - Standard user story structure
- **Acceptance criteria** - Clear success conditions
- **Edge cases** - Boundary conditions and exceptions
- **Non-functional requirements** - Performance, security, usability
- **Story prioritization** - Business value assessment
- **Story sizing** - Estimation guidelines

### 2. Test Scenario Creation

Develop comprehensive test scenarios:
- **Happy path scenarios** - Expected normal usage
- **Alternative paths** - Valid variations
- **Error scenarios** - Invalid inputs and error handling
- **Boundary conditions** - Min/max values, limits
- **State transitions** - Different system states
- **Concurrency scenarios** - Simultaneous operations

### 3. BDD Scenario Writing

Generate Gherkin-style scenarios:
- **Given-When-Then format** - Behavior-driven structure
- **Scenario outlines** - Data-driven test templates
- **Background steps** - Common preconditions
- **Feature organization** - Logical grouping
- **Tag-based filtering** - Scenario categorization

### 4. Acceptance Criteria Definition

Specify clear success conditions:
- **Functional criteria** - What the feature must do
- **Non-functional criteria** - Performance, security, UX
- **Negative criteria** - What should not happen
- **Testable statements** - Verifiable conditions
- **Definition of Done** - Completion checklist

## Scenario Generation Workflow

### Step 1: Analyze Requirements

Understand what needs to be tested:

**Requirements analysis questions:**
- What is the main functionality?
- Who are the users/actors?
- What are the inputs and outputs?
- What are the business rules?
- What can go wrong?
- What are the constraints/limitations?

**Example requirement:**
```
Requirement: User Login System
Users should be able to log in with email and password.
After 3 failed attempts, the account is locked for 15 minutes.
Password must be at least 8 characters.
```

**Analysis:**
- **Actors**: User, System
- **Inputs**: Email, password
- **Outputs**: Login success/failure, account lock
- **Business rules**: 3 attempts limit, 15-minute lockout, 8-char minimum
- **Edge cases**: Invalid email, wrong password, locked account, expired session

### Step 2: Identify Scenario Types

Categorize scenarios to generate:

**Scenario categories:**

| Category | Purpose | Examples |
|----------|---------|----------|
| Happy Path | Normal, expected flow | Valid login, successful purchase |
| Alternative Path | Valid variations | Login with remember me, guest checkout |
| Boundary | Min/max values | Minimum password length, maximum cart items |
| Error Handling | Invalid inputs | Wrong password, network error |
| Security | Unauthorized access | SQL injection, XSS attempts |
| Performance | Load/stress | 1000 concurrent logins |
| State Transition | Different states | Login when already logged in |

**Example identification:**
```
For User Login:
- Happy Path: Valid credentials → Success
- Alternative: Remember me checkbox
- Boundary: Exactly 8 characters password
- Error: Wrong password (attempt 1, 2, 3)
- Error: Account locked scenario
- Security: SQL injection in email field
- State: Already logged in user
```

### Step 3: Generate Scenarios

Create specific, testable scenarios:

**Scenario structure:**
```
Scenario: [Descriptive name]
Given [Initial context/preconditions]
When [Action/event]
Then [Expected outcome]
And [Additional outcomes]
```

**Example scenarios:**

```gherkin
Feature: User Login

Scenario: Successful login with valid credentials
  Given a registered user with email "user@example.com"
  And the user is on the login page
  When the user enters email "user@example.com"
  And the user enters password "SecurePass123"
  And the user clicks "Login"
  Then the user should be logged in
  And the user should be redirected to the dashboard
  And a session cookie should be created

Scenario: Failed login with incorrect password
  Given a registered user with email "user@example.com"
  And the user has 0 failed login attempts
  When the user enters email "user@example.com"
  And the user enters password "WrongPassword"
  And the user clicks "Login"
  Then the login should fail
  And an error message "Invalid email or password" should be displayed
  And the failed attempt count should increment to 1

Scenario: Account locked after 3 failed attempts
  Given a registered user with email "user@example.com"
  And the user has 2 failed login attempts
  When the user enters email "user@example.com"
  And the user enters password "WrongPassword"
  And the user clicks "Login"
  Then the account should be locked
  And an error message "Account locked. Try again in 15 minutes" should be displayed
  And the user cannot login even with correct password

Scenario: Password does not meet minimum length
  Given a new user on the registration page
  When the user enters password "Short1"
  And the user submits the form
  Then a validation error should appear
  And the error should say "Password must be at least 8 characters"
```

### Step 4: Add Scenario Outlines for Data Variations

Use scenario outlines for data-driven tests:

**Format:**
```gherkin
Scenario Outline: [Template name]
  Given [context with <placeholder>]
  When [action with <placeholder>]
  Then [outcome with <placeholder>]

  Examples:
    | placeholder1 | placeholder2 | expected_result |
    | value1       | value2       | result1         |
    | value3       | value4       | result2         |
```

**Example:**
```gherkin
Scenario Outline: Password validation
  Given a user on the registration page
  When the user enters password "<password>"
  Then the validation should be "<result>"
  And the message should be "<message>"

  Examples:
    | password      | result  | message                                    |
    | Short1        | invalid | Password must be at least 8 characters     |
    | NoDigits      | invalid | Password must contain at least one digit   |
    | nouppercas1   | invalid | Password must contain an uppercase letter  |
    | NOLOWERCASE1  | invalid | Password must contain a lowercase letter   |
    | ValidPass1    | valid   | Password accepted                          |
```

### Step 5: Document Acceptance Criteria

Define clear success conditions:

**Format:**
```markdown
## User Story
As a [role]
I want [feature]
So that [benefit]

## Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

## Edge Cases
- [Edge case 1]
- [Edge case 2]

## Definition of Done
- [ ] Code complete
- [ ] Tests passing
- [ ] Documentation updated
```

**Example:**
```markdown
## User Story
As a registered user
I want to log in with my email and password
So that I can access my account securely

## Acceptance Criteria
- [ ] User can log in with valid email and password
- [ ] User sees error message with invalid credentials
- [ ] Account locks after 3 failed attempts for 15 minutes
- [ ] Locked account shows appropriate message
- [ ] Password must be at least 8 characters
- [ ] Login session persists for 7 days with "remember me"
- [ ] User is redirected to dashboard after successful login

## Edge Cases
- User tries to login with locked account
- User logs in while already logged in (different device)
- Password exactly 8 characters long
- Email with special characters
- Network timeout during login
- Session expires while user is active

## Definition of Done
- [ ] All acceptance criteria met
- [ ] All edge cases tested
- [ ] Unit tests coverage >80%
- [ ] Integration tests passing
- [ ] Security review completed
- [ ] Documentation updated
```

## Scenario Generation Patterns

### Pattern 1: CRUD Operations

**Requirement:**
```
Implement a task management system where users can create, read, update, and delete tasks.
```

**Generated Scenarios:**

```gherkin
Feature: Task Management

Background:
  Given a logged-in user "john@example.com"

Scenario: Create a new task
  When the user creates a task with title "Buy groceries"
  And the user sets due date to "2024-12-31"
  And the user sets priority to "High"
  Then the task should be saved
  And the task should appear in the task list
  And the task ID should be returned

Scenario: View existing task
  Given a task exists with title "Buy groceries"
  When the user views the task
  Then the task title should be "Buy groceries"
  And the due date should be "2024-12-31"
  And the priority should be "High"

Scenario: Update task title
  Given a task exists with title "Buy groceries"
  When the user updates the title to "Buy groceries and cook dinner"
  Then the task title should be updated
  And the updated timestamp should be recorded

Scenario: Delete task
  Given a task exists with title "Buy groceries"
  When the user deletes the task
  Then the task should be removed from the database
  And the task should not appear in the task list

Scenario: Cannot create task without title
  When the user creates a task without a title
  Then a validation error should occur
  And the error should say "Title is required"

Scenario: Cannot update non-existent task
  When the user tries to update task ID "99999"
  Then a 404 error should occur
  And the error should say "Task not found"

Scenario: Cannot delete another user's task
  Given user "alice@example.com" created task ID "123"
  And current user is "bob@example.com"
  When the user tries to delete task ID "123"
  Then a 403 error should occur
  And the error should say "Unauthorized"
```

### Pattern 2: E-commerce Checkout

**Requirement:**
```
Users should be able to add items to cart, apply discounts, and complete checkout.
```

**User Stories:**

```markdown
## User Story 1: Add Item to Cart
As a shopper
I want to add items to my shopping cart
So that I can purchase multiple items together

### Acceptance Criteria
- [ ] User can add item by clicking "Add to Cart"
- [ ] Cart quantity updates immediately
- [ ] Cart icon shows item count
- [ ] User can add multiple quantities at once
- [ ] Out-of-stock items cannot be added
- [ ] Cart persists across page refreshes

### Test Scenarios
1. Add single item → Cart count increases by 1
2. Add item with quantity 5 → Cart count increases by 5
3. Add out-of-stock item → Error message shown
4. Add item, refresh page → Item still in cart
5. Add more than available stock → Error shown
```

```markdown
## User Story 2: Apply Discount Code
As a shopper
I want to apply discount codes
So that I can save money on my purchase

### Acceptance Criteria
- [ ] User can enter discount code at checkout
- [ ] Valid code applies discount to total
- [ ] Invalid code shows error message
- [ ] Expired code shows "Code expired" message
- [ ] Discount is reflected in order total
- [ ] Only one discount code per order

### Test Scenarios
1. Valid code "SAVE10" → 10% discount applied
2. Invalid code "INVALID" → Error "Invalid code"
3. Expired code "EXPIRED" → Error "Code expired"
4. Apply two codes → Second code replaces first
5. Remove code → Discount removed from total
```

**BDD Scenarios:**

```gherkin
Feature: Shopping Cart

Scenario: Add item to empty cart
  Given the user's cart is empty
  When the user adds "Laptop" to cart
  Then the cart should contain 1 item
  And the cart total should be $999.99

Scenario: Add multiple quantities
  Given the user is viewing product "Mouse"
  When the user selects quantity 3
  And the user clicks "Add to Cart"
  Then the cart should contain 3 "Mouse" items
  And the cart total should be $89.97

Scenario: Cannot add out-of-stock item
  Given product "Keyboard" is out of stock
  When the user tries to add "Keyboard" to cart
  Then an error message should appear
  And the message should say "Product out of stock"
  And the cart should remain unchanged

Scenario Outline: Apply discount codes
  Given the cart total is $100
  When the user applies discount code "<code>"
  Then the result should be "<result>"
  And the final total should be "<total>"

  Examples:
    | code      | result  | total   |
    | SAVE10    | success | $90.00  |
    | SAVE20    | success | $80.00  |
    | EXPIRED   | error   | $100.00 |
    | INVALID   | error   | $100.00 |
```

### Pattern 3: Form Validation

**Requirement:**
```
User registration form with name, email, password validation.
```

**Generated Test Scenarios:**

```gherkin
Feature: User Registration

Scenario Outline: Email validation
  Given a user on the registration page
  When the user enters email "<email>"
  And the user submits the form
  Then the validation should be "<result>"

  Examples:
    | email                  | result  |
    | valid@example.com      | valid   |
    | invalid.email          | invalid |
    | @example.com           | invalid |
    | user@                  | invalid |
    | user@domain            | valid   |
    | user+tag@example.com   | valid   |
    | ""                     | invalid |

Scenario Outline: Password strength validation
  When the user enters password "<password>"
  Then the strength should be "<strength>"
  And the message should be "<message>"

  Examples:
    | password       | strength | message                        |
    | weak           | weak     | Password too short             |
    | Medium1        | medium   | Add special character          |
    | Strong1!       | strong   | Password accepted              |
    | VeryStrong1!@  | strong   | Password accepted              |

Scenario: All fields valid
  Given the user is on the registration page
  When the user enters name "John Doe"
  And the user enters email "john@example.com"
  And the user enters password "SecurePass1!"
  And the user confirms password "SecurePass1!"
  And the user submits the form
  Then the registration should succeed
  And the user should receive a confirmation email
  And the user should be redirected to dashboard

Scenario: Password mismatch
  When the user enters password "Password1!"
  And the user confirms password "Password2!"
  And the user submits the form
  Then a validation error should appear
  And the error should say "Passwords do not match"

Scenario: Email already registered
  Given a user exists with email "john@example.com"
  When a new user tries to register with email "john@example.com"
  Then the registration should fail
  And the error should say "Email already registered"
```

### Pattern 4: API Endpoint Testing

**Requirement:**
```
RESTful API for managing blog posts: GET, POST, PUT, DELETE
```

**Test Scenarios:**

```gherkin
Feature: Blog Post API

Scenario: Get all blog posts
  Given 3 blog posts exist in the database
  When I send a GET request to "/api/posts"
  Then the response status should be 200
  And the response should contain 3 posts
  And each post should have "id", "title", "content", "author"

Scenario: Get single post by ID
  Given a post exists with ID "123"
  When I send a GET request to "/api/posts/123"
  Then the response status should be 200
  And the response should contain post ID "123"

Scenario: Get non-existent post
  When I send a GET request to "/api/posts/99999"
  Then the response status should be 404
  And the error message should be "Post not found"

Scenario: Create new post
  Given I am authenticated as "author@example.com"
  When I send a POST request to "/api/posts" with:
    """
    {
      "title": "My New Post",
      "content": "This is the content"
    }
    """
  Then the response status should be 201
  And the response should contain the new post ID
  And the post should be saved in the database

Scenario: Create post without authentication
  When I send a POST request to "/api/posts" without auth token
  Then the response status should be 401
  And the error should be "Unauthorized"

Scenario: Update post
  Given a post exists with ID "123"
  And I am authenticated as the post author
  When I send a PUT request to "/api/posts/123" with:
    """
    {
      "title": "Updated Title"
    }
    """
  Then the response status should be 200
  And the post title should be updated

Scenario: Delete post
  Given a post exists with ID "123"
  And I am authenticated as the post author
  When I send a DELETE request to "/api/posts/123"
  Then the response status should be 204
  And the post should be removed from database

Scenario: Cannot delete another user's post
  Given a post exists with ID "123" by "alice@example.com"
  And I am authenticated as "bob@example.com"
  When I send a DELETE request to "/api/posts/123"
  Then the response status should be 403
  And the error should be "Forbidden"
```

### Pattern 5: State Machine Testing

**Requirement:**
```
Order processing with states: Pending → Confirmed → Shipped → Delivered
```

**State Transition Scenarios:**

```gherkin
Feature: Order State Management

Scenario: New order starts in Pending state
  When a customer places an order
  Then the order state should be "Pending"

Scenario: Confirm pending order
  Given an order in "Pending" state
  When the admin confirms the order
  Then the order state should be "Confirmed"
  And a confirmation email should be sent

Scenario: Ship confirmed order
  Given an order in "Confirmed" state
  When the warehouse ships the order
  And the tracking number is "TRACK123"
  Then the order state should be "Shipped"
  And the tracking number should be saved
  And a shipment notification should be sent

Scenario: Deliver shipped order
  Given an order in "Shipped" state
  When the order is marked as delivered
  Then the order state should be "Delivered"
  And the delivery timestamp should be recorded

Scenario: Cannot ship pending order
  Given an order in "Pending" state
  When the warehouse tries to ship the order
  Then an error should occur
  And the error should say "Order must be confirmed first"
  And the order state should remain "Pending"

Scenario: Cannot confirm delivered order
  Given an order in "Delivered" state
  When admin tries to confirm the order
  Then an error should occur
  And the error should say "Order already delivered"

Scenario: Cancel order in Pending or Confirmed state
  Given an order in "<state>" state
  When the customer cancels the order
  Then the order state should be "Cancelled"
  And a refund should be initiated

  Examples:
    | state     |
    | Pending   |
    | Confirmed |

Scenario: Cannot cancel shipped order
  Given an order in "Shipped" state
  When the customer tries to cancel the order
  Then an error should occur
  And the error should say "Cannot cancel shipped order"
```

### Pattern 6: Permission-Based Access

**Requirement:**
```
Document management with roles: Viewer, Editor, Admin
```

**Permission Scenarios:**

```gherkin
Feature: Document Permissions

Background:
  Given a document "Report.pdf" exists
  And user "alice@example.com" is the owner

Scenario Outline: Role-based access control
  Given user "<user>" has role "<role>"
  When the user tries to "<action>" the document
  Then the result should be "<result>"

  Examples:
    | user          | role   | action | result  |
    | bob@ex.com    | Viewer | view   | allowed |
    | bob@ex.com    | Viewer | edit   | denied  |
    | bob@ex.com    | Viewer | delete | denied  |
    | carol@ex.com  | Editor | view   | allowed |
    | carol@ex.com  | Editor | edit   | allowed |
    | carol@ex.com  | Editor | delete | denied  |
    | dave@ex.com   | Admin  | view   | allowed |
    | dave@ex.com   | Admin  | edit   | allowed |
    | dave@ex.com   | Admin  | delete | allowed |
    | alice@ex.com  | Owner  | delete | allowed |

Scenario: Share document with specific user
  Given I am the document owner
  When I share the document with "bob@example.com" as "Editor"
  Then "bob@example.com" should be able to edit the document
  And "bob@example.com" should receive a notification

Scenario: Revoke access
  Given "bob@example.com" has Editor access
  When I revoke access for "bob@example.com"
  Then "bob@example.com" should not be able to view the document

Scenario: Transfer ownership
  Given I am the document owner
  When I transfer ownership to "carol@example.com"
  Then "carol@example.com" should be the owner
  And I should become an Editor
```

## Scenario Templates

### Template 1: Basic CRUD
```gherkin
Feature: [Resource] Management

Scenario: Create [resource]
  Given [preconditions]
  When I create a [resource] with [attributes]
  Then the [resource] should be saved
  And I should receive [confirmation]

Scenario: Read [resource]
  Given a [resource] exists with ID "[id]"
  When I retrieve the [resource]
  Then I should see [expected data]

Scenario: Update [resource]
  Given a [resource] exists with ID "[id]"
  When I update [attribute] to "[value]"
  Then the [resource] should be updated

Scenario: Delete [resource]
  Given a [resource] exists with ID "[id]"
  When I delete the [resource]
  Then the [resource] should be removed
```

### Template 2: Form Submission
```gherkin
Scenario: Submit valid form
  Given I am on the [form name] form
  When I fill in "[field1]" with "[value1]"
  And I fill in "[field2]" with "[value2]"
  And I submit the form
  Then I should see "[success message]"
  And [expected action] should occur

Scenario Outline: Field validation
  When I fill in "[field]" with "<value>"
  And I submit the form
  Then I should see error "<error>"

  Examples:
    | value    | error           |
    | [val1]   | [error1]        |
    | [val2]   | [error2]        |
```

### Template 3: Authentication
```gherkin
Scenario: Successful login
  Given I am on the login page
  When I enter email "[email]"
  And I enter password "[password]"
  And I click "Login"
  Then I should be logged in
  And I should see [dashboard/page]

Scenario: Failed login
  When I enter invalid credentials
  Then I should see error "[error message]"
  And I should remain on login page

Scenario: Logout
  Given I am logged in
  When I click "Logout"
  Then I should be logged out
  And I should be redirected to [page]
```

## Best Practices

1. **Be specific** - Scenarios should be clear and unambiguous
2. **One scenario, one behavior** - Test one thing at a time
3. **Use concrete examples** - Avoid vague terms like "some data"
4. **Include negative cases** - Test error conditions and edge cases
5. **Keep scenarios independent** - Each should run in isolation
6. **Use scenario outlines** - Avoid duplicating similar scenarios
7. **Write from user perspective** - Focus on behavior, not implementation
8. **Make scenarios testable** - Include verifiable outcomes
9. **Organize with tags** - Use @smoke, @regression, @critical tags
10. **Keep scenarios readable** - Non-technical stakeholders should understand

## Common Scenario Types

### Happy Path
```gherkin
Scenario: User completes checkout successfully
  Given items are in the cart
  When the user completes payment
  Then the order is placed
  And confirmation email is sent
```

### Error Handling
```gherkin
Scenario: Payment fails due to insufficient funds
  Given the cart total is $100
  When the user's card has insufficient funds
  Then the payment should fail
  And an error message should be shown
  And the order should not be placed
```

### Boundary Conditions
```gherkin
Scenario: Password exactly minimum length
  When the user enters an 8-character password
  Then the password should be accepted

Scenario: Cart with maximum items
  Given the cart has 99 items (max limit)
  When the user tries to add another item
  Then an error should appear
```

### Concurrency
```gherkin
Scenario: Two users purchase last item simultaneously
  Given only 1 item remains in stock
  When user A adds it to cart
  And user B adds it to cart simultaneously
  Then only one user should successfully checkout
  And the other should see "Out of stock"
```

## Gherkin Best Practices

### Good Gherkin
```gherkin
Scenario: User updates profile picture
  Given I am logged in as "john@example.com"
  And I am on my profile page
  When I upload a new profile picture "avatar.jpg"
  And I click "Save"
  Then my profile picture should be updated
  And I should see a success message
```

### Poor Gherkin
```gherkin
Scenario: Profile picture
  Given logged in
  When upload picture
  Then success
```

### Use Background for Common Setup
```gherkin
Feature: Shopping Cart

Background:
  Given I am logged in as "customer@example.com"
  And I have an empty cart

Scenario: Add item
  When I add "Laptop" to cart
  Then cart count should be 1

Scenario: Remove item
  Given I have "Laptop" in cart
  When I remove "Laptop"
  Then cart should be empty
```

### Tag Scenarios
```gherkin
@smoke @critical
Scenario: Login with valid credentials
  ...

@regression @slow
Scenario: Generate monthly report
  ...

@wip
Scenario: New feature in development
  ...
```
