---
name: gherkin-authoring
description: Gherkin acceptance criteria authoring. Use when writing Given/When/Then scenarios, feature files, or BDD-style specifications. Provides syntax reference, best practices, and Reqnroll integration guidance.
allowed-tools: Read, Glob, Grep, Write, Edit
---

# Gherkin Authoring

Gherkin/BDD acceptance criteria authoring for executable specifications.

## When to Use This Skill

**Keywords:** Gherkin, Given/When/Then, BDD, behavior-driven development, feature files, scenarios, acceptance criteria, Reqnroll, Cucumber, SpecFlow, executable specifications

**Use this skill when:**

- Writing acceptance criteria in Given/When/Then format
- Creating .feature files for BDD testing
- Converting requirements to executable specifications
- Setting up Reqnroll tests in .NET projects
- Understanding Gherkin syntax and best practices

## Quick Syntax Reference

### Feature File Structure

```gherkin
Feature: <Feature Name>
  <Feature description>

  Background:
    Given <common precondition>

  Scenario: <Scenario Name>
    Given <precondition>
    When <action>
    Then <expected outcome>

  Scenario Outline: <Parameterized Scenario>
    Given <precondition with <parameter>>
    When <action with <parameter>>
    Then <expected outcome with <parameter>>

    Examples:
      | parameter |
      | value1    |
      | value2    |
```

### Step Keywords

| Keyword | Purpose | Example |
| --- | --- | --- |
| `Given` | Setup preconditions | Given a user is logged in |
| `When` | Describe action | When the user clicks submit |
| `Then` | Assert outcome | Then the form is saved |
| `And` | Additional step (same type) | And an email is sent |
| `But` | Negative condition | But no error is shown |

## Writing Effective Scenarios

### The Three A's Pattern

Gherkin maps to the Arrange-Act-Assert pattern:

| Gherkin | AAA | Purpose |
| --- | --- | --- |
| Given | Arrange | Set up the test context |
| When | Act | Perform the action under test |
| Then | Assert | Verify the expected outcome |

### Single Behavior Per Scenario

**Good - One behavior:**

```gherkin
Scenario: User login with valid credentials
  Given a registered user exists
  When the user enters valid credentials
  Then the user is logged in
```

**Bad - Multiple behaviors:**

```gherkin
Scenario: User login and profile update
  Given a registered user exists
  When the user enters valid credentials
  Then the user is logged in
  When the user updates their profile
  Then the profile is saved
```

### Declarative vs Imperative Style

**Declarative (Preferred) - What, not how:**

```gherkin
Scenario: Successful checkout
  Given a customer with items in cart
  When the customer completes checkout
  Then the order is confirmed
```

**Imperative (Avoid) - Too detailed:**

```gherkin
Scenario: Successful checkout
  Given a customer is on the home page
  And the customer clicks "Products"
  And the customer clicks "Add to Cart" on item 1
  And the customer clicks "Cart" icon
  And the customer clicks "Checkout" button
  ...
```

## Background Section

Use Background for common setup shared across all scenarios in a feature:

```gherkin
Feature: Shopping Cart

  Background:
    Given a customer is logged in
    And the product catalog is available

  Scenario: Add item to cart
    When the customer adds a product to cart
    Then the cart contains 1 item

  Scenario: Remove item from cart
    Given the cart contains a product
    When the customer removes the product
    Then the cart is empty
```

### Background Guidelines

- Keep Background short (1-3 steps)
- Only include truly common setup
- Don't include anything not needed by ALL scenarios
- Consider splitting features if Background grows large

## Scenario Outline

Use Scenario Outline for parameterized tests:

```gherkin
Scenario Outline: Validate email format
  Given a user registration form
  When the user enters email "<email>"
  Then the validation result is "<result>"

  Examples:
    | email              | result  |
    | user@example.com   | valid   |
    | invalid-email      | invalid |
    | @missing-local.com | invalid |
    | user@             | invalid |
```

### When to Use Scenario Outline

**Use for:**

- Testing same logic with different data
- Boundary testing
- Error message variations
- Multiple valid/invalid inputs

**Avoid when:**

- Scenarios have fundamentally different flows
- Setup differs significantly between examples
- Only 1-2 examples (use separate scenarios)

## Tags

Organize and filter scenarios with tags:

```gherkin
@smoke @authentication
Feature: User Login

  @happy-path
  Scenario: Successful login
    ...

  @security @negative
  Scenario: Account lockout after failed attempts
    ...
```

### Common Tag Categories

| Category | Examples |
| --- | --- |
| Priority | @critical, @high, @medium, @low |
| Type | @smoke, @regression, @e2e |
| Feature | @authentication, @checkout, @search |
| State | @wip, @pending, @manual |
| Non-functional | @security, @performance, @accessibility |

## Integration with Canonical Spec

Gherkin acceptance criteria map to canonical specification:

```yaml
requirements:
  - id: "REQ-001"
    text: "WHEN a user submits valid credentials, the system SHALL authenticate the user"
    priority: must
    ears_type: event-driven
    acceptance_criteria:
      - id: "AC-001"
        given: "a registered user with valid credentials"
        when: "the user submits the login form"
        then: "the user is authenticated"
        and:
          - "a session is created"
          - "the user is redirected to dashboard"
```

### Mapping Rules

| Canonical Field | Gherkin Element |
| --- | --- |
| `acceptance_criteria.given` | Given step(s) |
| `acceptance_criteria.when` | When step(s) |
| `acceptance_criteria.then` | Then step(s) |
| `acceptance_criteria.and` | Additional And/But steps |

## Best Practices

### Scenario Naming

**Good:**

- Describes the behavior being tested
- Uses domain language
- Specifies the outcome

```gherkin
Scenario: User receives confirmation email after registration
Scenario: Cart total updates when quantity changes
Scenario: Search returns relevant results sorted by relevance
```

**Bad:**

- Generic or vague
- Implementation-focused
- Missing outcome

```gherkin
Scenario: Test registration
Scenario: Click add button
Scenario: Verify database
```

### Step Reusability

Write steps that can be reused:

**Reusable:**

```gherkin
Given a user with role "<role>"
Given the user has "<count>" items in cart
When the user performs "<action>"
```

**Not Reusable:**

```gherkin
Given John Smith is logged in as admin
Given the user has 3 items in cart for checkout test
When the user clicks the blue submit button
```

### Avoid Coupling to UI

**Good - Behavior-focused:**

```gherkin
When the user submits the form with invalid data
Then an error message is displayed
```

**Bad - UI-coupled:**

```gherkin
When the user clicks the red Submit button at the bottom
Then a red error div appears below the form
```

## Reqnroll Integration (.NET)

### Step Definition Example

```csharp
[Binding]
public class LoginSteps
{
    private readonly ScenarioContext _context;

    public LoginSteps(ScenarioContext context)
    {
        _context = context;
    }

    [Given(@"a registered user exists")]
    public void GivenARegisteredUserExists()
    {
        var user = new User("test@example.com", "password123");
        _context["user"] = user;
    }

    [When(@"the user enters valid credentials")]
    public void WhenTheUserEntersValidCredentials()
    {
        var user = _context.Get<User>("user");
        var result = _authService.Login(user.Email, user.Password);
        _context["loginResult"] = result;
    }

    [Then(@"the user is logged in")]
    public void ThenTheUserIsLoggedIn()
    {
        var result = _context.Get<LoginResult>("loginResult");
        result.Success.Should().BeTrue();
    }
}
```

### Project Setup

```xml
<PackageReference Include="Reqnroll" Version="2.*" />
<PackageReference Include="Reqnroll.NUnit" Version="2.*" />
```

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Fix |
| --- | --- | --- |
| Feature-length scenarios | Hard to maintain | Split into focused scenarios |
| Imperative steps | Brittle, verbose | Use declarative style |
| Technical jargon | Not business-readable | Use domain language |
| Coupled to UI | Breaks on UI changes | Focus on behavior |
| No Background | Duplicated Given steps | Extract common setup |
| Too many Examples | Slow, redundant | Test boundary cases only |

## Validation Checklist

Before finalizing a Gherkin scenario:

- [ ] Single behavior per scenario
- [ ] Declarative, not imperative
- [ ] Uses domain language
- [ ] Given establishes context only
- [ ] When contains single action
- [ ] Then asserts observable outcomes
- [ ] No implementation details
- [ ] Scenario name describes behavior

## References

**Detailed Documentation:**

- [Syntax Reference](references/syntax-reference.md) - Complete Gherkin syntax
- [Best Practices](references/best-practices.md) - BDD best practices

**Related Skills:**

- `canonical-spec-format` - Canonical specification structure
- `spec-management` - Specification workflow navigation
- `ears-authoring` - EARS requirement patterns

---

**Last Updated:** 2025-12-24

## Version History

- **v1.0.0** (2025-12-26): Initial release

---
