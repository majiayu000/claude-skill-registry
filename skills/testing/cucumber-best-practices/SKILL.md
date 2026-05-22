---
name: cucumber-best-practices
description: Cucumber best practices, patterns, and anti-patterns
---

# Cucumber Best Practices

Master patterns and practices for effective Cucumber testing.

## Scenario Design Principles

### 1. Write Declarative Scenarios

Focus on **what** needs to happen, not **how** it happens.

❌ **Imperative** (implementation-focused):

```gherkin
Scenario: Add product to cart
  Given I navigate to "http://shop.com/products"
  When I find the element with CSS ".product[data-id='123']"
  And I click the button with class "add-to-cart"
  And I wait for the AJAX request to complete
  Then the element ".cart-count" should contain "1"
```

✅ **Declarative** (business-focused):

```gherkin
Scenario: Add product to cart
  Given I am browsing products
  When I add "Wireless Headphones" to my cart
  Then my cart should contain 1 item
```

### 2. One Scenario, One Behavior

Each scenario should test exactly one business rule or behavior.

❌ **Multiple behaviors in one scenario:**

```gherkin
Scenario: User registration and login and profile update
  Given I register a new account
  When I log in
  And I update my profile
  And I change my password
  Then everything should work
```

✅ **Separate scenarios:**

```gherkin
Scenario: Register new account
  When I register with valid details
  Then I should receive a confirmation email

Scenario: Login with new account
  Given I have registered an account
  When I log in with my credentials
  Then I should see my dashboard

Scenario: Update profile
  Given I am logged in
  When I update my profile information
  Then my changes should be saved
```

### 3. Keep Scenarios Independent

Each scenario should set up its own preconditions.

❌ **Dependent scenarios:**

```gherkin
Scenario: Create order
  When I create order #12345

Scenario: View order
  When I view order #12345  # Depends on previous scenario!
```

✅ **Independent scenarios:**

```gherkin
Scenario: View order
  Given an order exists with ID "12345"
  When I view the order details
  Then I should see the order information
```

### 4. Use Background Wisely

Use Background for common setup, but don't overuse it.

✅ **Good use of Background:**

```gherkin
Feature: Shopping Cart

  Background:
    Given I am logged in as a customer

  Scenario: Add product to cart
    When I add a product to my cart
    Then my cart should contain 1 item

  Scenario: Remove product from cart
    Given I have a product in my cart
    When I remove the product
    Then my cart should be empty
```

❌ **Background doing too much:**

```gherkin
Background:
  Given I am on the homepage
  And I click the menu
  And I navigate to products
  And I filter by category "Electronics"
  And I sort by price
  # Too much setup! Not all scenarios need all of this
```

## Feature Organization

### Group Related Scenarios

```gherkin
Feature: User Authentication

  Scenario: Successful login
    ...

  Scenario: Failed login with wrong password
    ...

  Scenario: Account lockout after multiple failures
    ...
```

### Use Tags Effectively

```gherkin
@smoke @critical
Scenario: Login with valid credentials
  ...

@slow @integration
Scenario: Password reset email workflow
  ...

@wip
Scenario: OAuth login
  # Work in progress
  ...
```

Run specific tags:

```bash
# Run smoke tests
cucumber --tags "@smoke"

# Run all except WIP
cucumber --tags "not @wip"

# Run smoke AND critical
cucumber --tags "@smoke and @critical"

# Run smoke OR critical
cucumber --tags "@smoke or @critical"
```

## Writing Good Gherkin

### Use Domain Language

Write in the language of the business domain, not technical terms.

❌ **Technical language:**

```gherkin
Scenario: POST request to /api/users
  When I send a POST to "/api/users" with JSON payload
  And the response status is 201
```

✅ **Domain language:**

```gherkin
Scenario: Register new user
  When I register a new user account
  Then the user should be created successfully
```

### Keep Steps at the Same Level

Don't mix high-level and low-level details.

❌ **Mixed levels:**

```gherkin
Scenario: Purchase product
  Given I am logged in
  When I add a product to cart
  And I click the element with ID "checkout-btn"  # Too detailed!
  And I enter credit card "4111111111111111"      # Too detailed!
  Then I complete the purchase
```

✅ **Consistent level:**

```gherkin
Scenario: Purchase product
  Given I am logged in
  And I have a product in my cart
  When I checkout with a credit card
  Then my order should be completed
  And I should receive a confirmation email
```

### Avoid Conjunctive Steps

Don't use "And" to combine multiple distinct actions in prose.

❌ **Conjunctive step:**

```gherkin
When I log in and add a product to cart and checkout
```

✅ **Separate steps:**

```gherkin
When I log in
And I add a product to my cart
And I proceed to checkout
```

## Scenario Outlines

### Use for True Variations

Use Scenario Outlines when you need to test the same behavior with different data.

✅ **Good use:**

```gherkin
Scenario Outline: Login validation
  When I log in with "<username>" and "<password>"
  Then I should see "<message>"

  Examples:
    | username | password | message                |
    | valid    | valid    | Welcome                |
    | invalid  | valid    | Invalid username       |
    | valid    | invalid  | Invalid password       |
    | empty    | empty    | Username required      |
```

❌ **Overusing Scenario Outline:**

```gherkin
# Don't use Scenario Outline for unrelated test cases
Scenario Outline: Multiple features
  When I use feature "<feature>"
  Then result is "<result>"

  Examples:
    | feature        | result    |
    | login          | success   |
    | registration   | success   |
    | cart           | empty     |  # These are different behaviors!
```

### Keep Examples Meaningful

```gherkin
Scenario Outline: Discount calculation
  Given a customer with "<membership>" status
  When they purchase items totaling $<amount>
  Then they should receive a $<discount> discount

  Examples: Standard discounts
    | membership | amount | discount |
    | silver     | 100    | 5        |
    | gold       | 100    | 10       |
    | platinum   | 100    | 15       |

  Examples: Minimum purchase thresholds
    | membership | amount | discount |
    | silver     | 49     | 0        |
    | silver     | 50     | 2.50     |
```

## Step Definition Patterns

### Create Reusable Steps

```javascript
// Generic, reusable
When('I fill in {string} with {string}', async function(field, value) {
  await this.page.fill(`[name="${field}"]`, value);
});

// Used in multiple scenarios:
When('I fill in "email" with "test@example.com"')
When('I fill in "password" with "secure123"')
When('I fill in "search" with "products"')
```

### Avoid Over-Generic Steps

Balance reusability with readability.

❌ **Too generic:**

```javascript
When('I do {string} with {string} and {string}', ...)
```

✅ **Specific and readable:**

```javascript
When('I log in with {string} and {string}', ...)
When('I search for {string} in {string}', ...)
```

## Data Management

### Use Factories for Test Data

```javascript
// support/factories.js
const faker = require('faker');

class UserFactory {
  static create(overrides = {}) {
    return {
      firstName: faker.name.firstName(),
      lastName: faker.name.lastName(),
      email: faker.internet.email(),
      password: 'Test123!',
      ...overrides
    };
  }
}

// Use in steps
Given('I register a new user', async function() {
  const user = UserFactory.create();
  this.currentUser = user;
  await this.api.register(user);
});
```

### Avoid Hardcoded IDs

❌ **Hardcoded:**

```gherkin
Given user "12345" exists
When I view order "67890"
```

✅ **Named entities:**

```gherkin
Given a user "john@example.com" exists
When I view my most recent order
```

## Error Handling

### Test Happy and Unhappy Paths

```gherkin
@happy-path
Scenario: Successful checkout
  Given I have items in my cart
  When I complete the checkout process
  Then my order should be confirmed

@error-handling
Scenario: Checkout with expired card
  Given I have items in my cart
  When I checkout with an expired credit card
  Then I should see an error message
  And my order should not be processed

@edge-case
Scenario: Checkout with insufficient inventory
  Given I have a product in my cart
  But the product is out of stock
  When I attempt to checkout
  Then I should be notified about stock unavailability
```

## Performance

### Tag Slow Tests

```gherkin
@slow @integration
Scenario: Full order workflow with email notifications
  # Takes 30 seconds to run
  ...
```

### Parallel Execution

Ensure scenarios can run in parallel:

```javascript
// cucumber.js
module.exports = {
  default: '--parallel 4'
};
```

## Maintenance

### Regular Review

- Remove obsolete scenarios
- Update scenarios when requirements change
- Refactor duplicate steps
- Keep features organized

### Version Control

```
features/
  authentication/
    login.feature
    registration.feature
  shopping/
    cart.feature
    checkout.feature
  admin/
    user-management.feature
```

## Common Anti-Patterns

❌ **Testing implementation details:**

```gherkin
Then the database should have 1 record in the users table
```

❌ **UI-specific assertions in business scenarios:**

```gherkin
Then I should see a red error message in the top right corner
```

❌ **Using Given for actions:**

```gherkin
Given I click the submit button  # This is a When, not a Given!
```

❌ **Technical jargon:**

```gherkin
When I POST to /api/v1/users with JSON body
```

## Testing Pyramid

Use Cucumber appropriately in your test strategy:

- **E2E Cucumber Tests**: Critical user journeys (20%)
- **Integration Tests**: API/service interactions (30%)
- **Unit Tests**: Business logic (50%)

Don't try to test everything with Cucumber. Use it for high-value acceptance tests.

Remember: Cucumber tests should document behavior, facilitate collaboration, and provide confidence that the system works as expected from a business perspective.
