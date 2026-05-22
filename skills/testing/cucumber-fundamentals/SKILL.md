---
name: cucumber-fundamentals
description: Core Cucumber concepts, Gherkin syntax, and feature file structure
---

# Cucumber Fundamentals

Master the core concepts of Cucumber and Gherkin for behavior-driven development.

## Gherkin Syntax

Use the Given-When-Then structure for scenarios:

```gherkin
Feature: User Authentication
  As a user
  I want to log in to the application
  So that I can access my account

  Scenario: Successful login with valid credentials
    Given I am on the login page
    When I enter valid credentials
    And I click the login button
    Then I should be redirected to the dashboard
    And I should see a welcome message
```

### Keywords

- **Feature**: High-level description of a software feature
- **Scenario**: Concrete example illustrating a business rule
- **Given**: Context or preconditions
- **When**: Action or event
- **Then**: Expected outcome
- **And/But**: Connect multiple steps
- **Background**: Common preconditions for all scenarios
- **Scenario Outline**: Template for multiple examples
- **Examples**: Data table for Scenario Outline

## Feature Files

Structure feature files logically:

```gherkin
Feature: Shopping Cart Management
  In order to purchase products
  As a customer
  I want to manage items in my shopping cart

  Background:
    Given I am logged in as a customer
    And my shopping cart is empty

  Scenario: Add product to cart
    When I add a "Laptop" to my cart
    Then my cart should contain 1 item
    And the cart total should be "$999.99"

  Scenario: Remove product from cart
    Given I have a "Laptop" in my cart
    When I remove the "Laptop" from my cart
    Then my cart should be empty
    And the cart total should be "$0.00"
```

## Scenario Outlines

Use data tables for parameterized tests:

```gherkin
Scenario Outline: Login with different user types
  Given I am on the login page
  When I log in as "<user_type>"
  Then I should see the "<dashboard>" dashboard
  And I should have "<permissions>" permissions

  Examples:
    | user_type | dashboard | permissions    |
    | admin     | Admin     | full_access    |
    | user      | User      | limited_access |
    | guest     | Public    | read_only      |
```

## Tags

Organize and filter scenarios with tags:

```gherkin
@smoke @authentication
Scenario: User login
  Given I am on the login page
  When I enter valid credentials
  Then I should be logged in

@wip
Scenario: Password reset
  Given I am on the password reset page
  # Work in progress
```

## Best Practices

1. **Write declarative scenarios** - Focus on *what*, not *how*
2. **Keep scenarios independent** - Each scenario should stand alone
3. **Use domain language** - Write in business terms, not technical implementation
4. **One scenario, one behavior** - Test one thing at a time
5. **Avoid UI details in Given/When/Then** - Stay at business logic level

## Example: Good vs Bad Scenarios

❌ **Bad** (imperative, implementation-focused):

```gherkin
Scenario: Update user profile
  Given I navigate to "http://example.com/profile"
  When I find the element with id "firstName"
  And I clear the input field
  And I type "John"
  And I click the button with class "save-btn"
  Then I should see the text "Profile updated"
```

✅ **Good** (declarative, business-focused):

```gherkin
Scenario: Update user profile
  Given I am on my profile page
  When I update my first name to "John"
  Then my profile should be saved
  And I should see a success message
```

## Data Tables

Pass structured data to steps:

```gherkin
Scenario: Register new user
  Given I am on the registration page
  When I fill in the registration form:
    | Field          | Value              |
    | First Name     | John               |
    | Last Name      | Doe                |
    | Email          | john@example.com   |
    | Password       | SecurePass123!     |
  Then I should be registered successfully
```

## Doc Strings

Pass multi-line text to steps:

```gherkin
Scenario: Submit contact form
  Given I am on the contact page
  When I submit a message:
    """
    Hello support team,

    I have a question about my recent order #12345.
    Please contact me at your earliest convenience.

    Best regards,
    John Doe
    """
  Then I should see a confirmation message
```

## Key Principles

- **Living Documentation**: Features serve as executable specifications
- **Collaboration**: Written by developers, testers, and business stakeholders
- **Ubiquitous Language**: Use domain terminology consistently
- **Examples over Rules**: Concrete examples clarify requirements
- **Automation**: Scenarios are automated tests

Remember: Cucumber scenarios are specifications first, tests second. They document expected behavior in a language everyone understands.
