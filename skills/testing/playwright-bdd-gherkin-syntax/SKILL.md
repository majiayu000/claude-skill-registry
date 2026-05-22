---
name: playwright-bdd-gherkin-syntax
description: Use when writing Gherkin feature files, using Scenario Outline with Examples, applying tags for test organization, and leveraging Background sections for shared setup.
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
---

# Playwright BDD Gherkin Syntax

Expert knowledge of Gherkin syntax for writing feature files in Playwright BDD, including scenarios, outlines, backgrounds, tags, and internationalization.

## Overview

Gherkin is a domain-specific language for describing software behavior in plain text. Playwright BDD uses Gherkin feature files (`.feature`) that are transformed into Playwright test files via `bddgen`.

## Feature File Structure

### Basic Structure

```gherkin
Feature: User Authentication
  As a user
  I want to be able to log in
  So that I can access my account

  Background:
    Given I am on the login page

  Scenario: Successful login
    When I enter valid credentials
    And I click the login button
    Then I should see the dashboard

  Scenario: Failed login
    When I enter invalid credentials
    And I click the login button
    Then I should see an error message
```

### Feature Declaration

```gherkin
Feature: Short descriptive title

  Optional description spanning
  multiple lines explaining the
  feature's purpose and context.
```

## Keywords

### Given - Preconditions

Describes the initial context or state:

```gherkin
Given I am logged in as "admin"
Given the shopping cart is empty
Given the following users exist:
  | name  | email           |
  | Alice | alice@test.com  |
  | Bob   | bob@test.com    |
```

### When - Actions

Describes the action or event:

```gherkin
When I click the "Submit" button
When I fill in "email" with "test@example.com"
When I select "Express" from the shipping options
When 24 hours have passed
```

### Then - Outcomes

Describes the expected outcome:

```gherkin
Then I should see "Welcome back!"
Then the cart should contain 3 items
Then I should be redirected to the dashboard
Then an email should be sent to "test@example.com"
```

### And / But - Continuation

Continues the previous Given/When/Then:

```gherkin
Given I am logged in
And I have items in my cart
But I have not entered a shipping address

When I click checkout
And I enter my payment details

Then I should see the confirmation page
And I should receive an order email
But I should not be charged twice
```

## Scenario Types

### Basic Scenario

```gherkin
Scenario: Add item to cart
  Given I am on the product page
  When I click "Add to Cart"
  Then the cart count should be 1
```

### Scenario Outline (Data-Driven)

Run the same scenario with different data:

```gherkin
Scenario Outline: Login with different roles
  Given I am on the login page
  When I login as "<role>"
  Then I should see the "<dashboard>" dashboard

  Examples:
    | role    | dashboard |
    | admin   | Admin     |
    | user    | User      |
    | manager | Manager   |
```

Multiple example tables:

```gherkin
Scenario Outline: Product pricing
  Given I am viewing product "<product>"
  Then the price should be "<price>"
  And the discount should be "<discount>"

  Examples: Regular Products
    | product | price  | discount |
    | Laptop  | $999   | 0%       |
    | Mouse   | $29    | 0%       |

  Examples: Sale Products
    | product    | price  | discount |
    | Keyboard   | $79    | 20%      |
    | Headphones | $149   | 15%      |
```

### Background (Shared Setup)

Runs before each scenario in the feature:

```gherkin
Feature: Shopping Cart

  Background:
    Given I am logged in
    And I have an empty cart

  Scenario: Add single item
    When I add "Product A" to cart
    Then the cart should have 1 item

  Scenario: Add multiple items
    When I add "Product A" to cart
    And I add "Product B" to cart
    Then the cart should have 2 items
```

### Rule (Grouping Related Scenarios)

Group scenarios under business rules:

```gherkin
Feature: Discount System

  Rule: Bulk discounts apply to orders over 10 items

    Scenario: Order with 10 items gets no discount
      Given I have 10 items in my cart
      Then I should see no discount applied

    Scenario: Order with 11 items gets bulk discount
      Given I have 11 items in my cart
      Then I should see a 10% discount applied

  Rule: VIP members get additional discounts

    Scenario: VIP member gets member discount
      Given I am a VIP member
      When I view my cart
      Then I should see a 5% member discount
```

## Tags

### Basic Tags

```gherkin
@smoke
Feature: User Authentication

  @critical
  Scenario: Successful login
    Given I am on the login page
    When I enter valid credentials
    Then I should see the dashboard

  @regression @slow
  Scenario: Password recovery
    Given I am on the forgot password page
    When I request a password reset
    Then I should receive an email
```

### Special Playwright BDD Tags

```gherkin
# Skip this scenario
@skip
Scenario: Feature not ready
  Given this is skipped

# Run only this scenario (like test.only)
@only
Scenario: Debug this specific test
  Given I need to focus on this

# Mark as known failure
@fail
Scenario: Known bug #123
  Given this is expected to fail

# Mark as flaky but continue
@fixme
Scenario: Intermittently failing test
  Given this sometimes fails
```

### Tag Expressions

Filter tests by tags when running:

```bash
# Run only smoke tests
npx playwright test --grep @smoke

# Run critical tests
npx playwright test --grep @critical

# Run everything except slow tests
npx playwright test --grep-invert @slow

# Combine tags (AND)
npx playwright test --grep "@smoke.*@critical"
```

### Tag Inheritance

Tags on Feature apply to all scenarios:

```gherkin
@authentication @web
Feature: User Login

  @happy-path
  Scenario: Successful login
    # Has tags: @authentication, @web, @happy-path
    ...

  @error-handling
  Scenario: Invalid password
    # Has tags: @authentication, @web, @error-handling
    ...
```

## Data Tables

### Simple Lists

```gherkin
Scenario: Add multiple items
  When I add the following items:
    | Milk   |
    | Bread  |
    | Butter |
```

### Key-Value Tables

```gherkin
Scenario: Fill registration form
  When I fill in the form with:
    | First Name | John           |
    | Last Name  | Doe            |
    | Email      | john@test.com  |
    | Password   | secret123      |
```

### Tables with Headers

```gherkin
Scenario: Create multiple users
  Given the following users exist:
    | username | email           | role  |
    | alice    | alice@test.com  | admin |
    | bob      | bob@test.com    | user  |
    | carol    | carol@test.com  | user  |
```

### Complex Tables

```gherkin
Scenario: Order with multiple products
  When I create an order with:
    | product   | quantity | price | discount |
    | Laptop    | 1        | 999   | 0%       |
    | Mouse     | 2        | 29    | 10%      |
    | Keyboard  | 1        | 79    | 5%       |
  Then the order total should be $1123.55
```

## Doc Strings

### Plain Text

```gherkin
Scenario: Submit feedback
  When I enter the following feedback:
    """
    Great product! Would recommend.
    Fast shipping and excellent quality.
    """
  And I click submit
  Then I should see "Thank you for your feedback"
```

### JSON Content

```gherkin
Scenario: Create product via API
  When I send a POST request with:
    """json
    {
      "name": "New Product",
      "price": 49.99,
      "category": "electronics",
      "tags": ["new", "featured"]
    }
    """
  Then the response status should be 201
```

### Code Blocks

```gherkin
Scenario: Execute script
  When I run the following script:
    """javascript
    const result = await page.evaluate(() => {
      return document.title;
    });
    console.log(result);
    """
```

## Internationalization (i18n)

### Language Header

```gherkin
# language: de
Funktionalität: Benutzeranmeldung

  Grundlage:
    Angenommen ich bin auf der Anmeldeseite

  Szenario: Erfolgreiche Anmeldung
    Wenn ich gültige Anmeldedaten eingebe
    Dann sollte ich das Dashboard sehen
```

### Supported Languages

Common languages and their keywords:

**German (de):**

```gherkin
# language: de
Funktionalität: Feature title
  Szenario: Scenario title
    Angenommen: Given
    Wenn: When
    Dann: Then
    Und: And
    Aber: But
```

**French (fr):**

```gherkin
# language: fr
Fonctionnalité: Feature title
  Scénario: Scenario title
    Soit: Given
    Quand: When
    Alors: Then
    Et: And
    Mais: But
```

**Spanish (es):**

```gherkin
# language: es
Característica: Feature title
  Escenario: Scenario title
    Dado: Given
    Cuando: When
    Entonces: Then
    Y: And
    Pero: But
```

## Comments

```gherkin
Feature: Product Catalog
  # This feature covers the product listing pages

  # TODO: Add search functionality tests
  Scenario: View all products
    Given I am on the catalog page
    # Check that products load
    Then I should see at least 10 products
```

## Best Practices

### Write Declarative Steps

**Good (declarative):**

```gherkin
Given I am logged in as an admin
When I create a new product
Then the product should be visible in the catalog
```

**Bad (imperative):**

```gherkin
Given I navigate to "/login"
And I type "admin@test.com" in the email field
And I type "password123" in the password field
And I click the login button
And I wait for the dashboard to load
When I click the "Products" menu item
And I click "Add New"
...
```

### Use Meaningful Scenario Names

**Good:**

```gherkin
Scenario: Logged-in user can add items to wishlist
Scenario: Guest users are prompted to register before checkout
Scenario: Expired promo codes show clear error message
```

**Bad:**

```gherkin
Scenario: Test 1
Scenario: Check wishlist
Scenario: Error test
```

### Keep Scenarios Independent

Each scenario should work in isolation:

```gherkin
# Good - each scenario sets up its own state
Scenario: Edit existing product
  Given a product "Test Product" exists
  When I edit the product name to "Updated Product"
  Then I should see "Updated Product" in the list

# Bad - depends on previous scenario
Scenario: Edit the product
  # Assumes product from previous scenario exists
  When I edit the product name
  Then it should be updated
```

### Use Background Wisely

Only put truly common setup in Background:

```gherkin
# Good - common setup
Background:
  Given I am logged in

# Bad - too specific
Background:
  Given I am logged in
  And I have created a product "Widget"
  And the product has 5 reviews
  And the product is on sale
```

### Organize with Tags

```gherkin
@e2e @checkout
Feature: Checkout Process

  @smoke @critical
  Scenario: Complete checkout with credit card
    ...

  @regression
  Scenario: Checkout with PayPal
    ...

  @slow @integration
  Scenario: Checkout with inventory sync
    ...
```

### Avoid Too Many Steps

Keep scenarios focused (ideally 3-7 steps):

**Good:**

```gherkin
Scenario: Add item to cart
  Given I am viewing a product
  When I click "Add to Cart"
  Then the cart should show 1 item
```

**Bad (too many steps):**

```gherkin
Scenario: Complete purchase
  Given I am logged in
  And I am on the home page
  And I search for "laptop"
  And I click on the first result
  And I select color "silver"
  And I select memory "16GB"
  And I click add to cart
  And I view my cart
  And I click checkout
  And I enter my address
  And I select shipping method
  And I enter credit card details
  And I confirm the order
  Then I should see order confirmation
  # Too long - break into multiple scenarios
```

## Common Patterns

### Setup and Verification Pattern

```gherkin
Scenario: Delete a product
  Given a product "Test Product" exists     # Setup
  When I delete "Test Product"               # Action
  Then "Test Product" should not be visible  # Verification
```

### State Transition Pattern

```gherkin
Scenario: Order lifecycle
  Given an order in "pending" status
  When I process the order
  Then the order status should be "processing"

  When I ship the order
  Then the order status should be "shipped"

  When the order is delivered
  Then the order status should be "completed"
```

### Error Handling Pattern

```gherkin
@error-handling
Scenario: Invalid form submission
  Given I am on the registration page
  When I submit the form with:
    | email    | invalid-email |
    | password | 123           |
  Then I should see the following errors:
    | field    | message                    |
    | email    | Please enter a valid email |
    | password | Password too short         |
```

## File Organization

```
features/
├── authentication/
│   ├── login.feature
│   ├── logout.feature
│   └── password-reset.feature
├── products/
│   ├── catalog.feature
│   ├── search.feature
│   └── product-details.feature
├── checkout/
│   ├── cart.feature
│   ├── payment.feature
│   └── shipping.feature
└── admin/
    ├── user-management.feature
    └── product-management.feature
```

## When to Use This Skill

- Writing new feature files
- Converting requirements to Gherkin scenarios
- Using Scenario Outline for data-driven tests
- Organizing tests with tags
- Setting up shared Background steps
- Working with internationalized features
- Reviewing and improving feature file quality
- Training team members on BDD syntax
