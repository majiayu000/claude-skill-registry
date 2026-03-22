---
name: cucumber
description: Gherkin/Cucumber BDD specification language
category: Testing BDD
---

# Skill: cucumber

## What I do

I provide Gherkin/Cucumber BDD expertise: feature files, scenario structure, step definitions, data tables, scenario outlines, and best practices for writing living documentation that drives tests.

## When to use me

- Writing Gherkin feature files for BDD
- Designing scenarios that serve as living documentation
- Implementing step definitions in Go (godog), Ruby, or JavaScript
- Using data tables, scenario outlines, and backgrounds
- Bridging business language and automated tests

## Core principles

1. **Business language first** - Scenarios describe behaviour in domain terms, not UI steps
2. **Given-When-Then** - Given (context), When (action), Then (outcome)
3. **One scenario, one behaviour** - Each scenario tests exactly one rule
4. **Declarative over imperative** - Say what, not how (avoid click/type steps)
5. **Living documentation** - Features are specs that stakeholders can read

## Patterns & examples

**Feature file structure:**
```gherkin
Feature: Order checkout
  As a customer
  I want to complete my purchase
  So that I receive my items

  Background:
    Given I am a registered customer
    And I have items in my cart

  Scenario: Successful checkout with valid payment
    Given my cart total is £25.00
    When I complete checkout with valid payment
    Then my order should be confirmed
    And I should receive a confirmation email

  Scenario: Checkout rejected with insufficient funds
    Given my cart total is £25.00
    When I complete checkout with insufficient funds
    Then I should see a payment declined message
    And my cart should remain unchanged
```

**Scenario outlines (parameterised):**
```gherkin
Scenario Outline: Shipping cost by region
  Given my delivery address is in <region>
  When I calculate shipping for <weight>kg
  Then the shipping cost should be £<cost>

  Examples:
    | region | weight | cost  |
    | UK     | 1      | 3.99  |
    | UK     | 5      | 7.99  |
    | EU     | 1      | 9.99  |
    | US     | 1      | 14.99 |
```

**Step definitions (Go with godog):**
```go
func (s *OrderSteps) InitializeScenario(ctx *godog.ScenarioContext) {
  ctx.Given(`^my cart total is £(\d+\.\d+)$`, s.cartTotalIs)
  ctx.When(`^I complete checkout with valid payment$`, s.checkoutWithValidPayment)
  ctx.Then(`^my order should be confirmed$`, s.orderConfirmed)
}

func (s *OrderSteps) cartTotalIs(total float64) error {
  s.cart.SetTotal(total)
  return nil
}

func (s *OrderSteps) checkoutWithValidPayment() error {
  s.result = s.checkout.Process(s.cart, validPayment)
  return nil
}
```

**Data tables:**
```gherkin
Scenario: Adding multiple items to cart
  When I add the following items:
    | name       | quantity | price |
    | Widget     | 2        | 5.99  |
    | Gadget     | 1        | 12.50 |
  Then my cart total should be £24.48
```

## Anti-patterns to avoid

- ❌ Imperative steps (`When I click the submit button`) — use declarative (`When I submit my order`)
- ❌ UI-coupled steps (`Then I should see div.success`) — use domain language
- ❌ Long scenarios with 10+ steps (break into smaller focused scenarios)
- ❌ Scenario dependencies (each scenario must be independent)
- ❌ Incidental details (`Given a user "alice@test.com" with password "abc123"`) — use roles/personas
- ❌ NEVER use `env.GetEvents()` or similar DB access in "Then" steps — use `env.GetView()` and check for substring/footer
- ❌ NEVER bypass UI with direct repo calls in "When" steps — call domain functions instead
- ❌ NEVER mix DB assertions with view assertions in same step file — migrate fully to one pattern

**WRONG** (DB-based Then step):
```go
func thereShouldBeNEvents(ctx context.Context, n int) (context.Context, error) {
    env := support.GetAppEnv(ctx)
    count := len(env.GetEvents())  // ❌ DB access
    if count != n { return ctx, fmt.Errorf("expected %d", n) }
    return ctx, nil
}
```

**CORRECT** (View-based Then step):
```go
func thereShouldBeNEvents(ctx context.Context, n int) (context.Context, error) {
    env := support.GetAppEnv(ctx)
    view := env.GetView()  // ✅ View access
    expectedFooter := fmt.Sprintf("Events: %d", n)
    if !strings.Contains(view, expectedFooter) {
        return ctx, fmt.Errorf("expected footer not found")
    }
    return ctx, nil
}
```

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Testing-BDD/Cucumber.md`

## Related skills

- `bdd-workflow` - Red-Green-Refactor cycle with Cucumber
- `godog` - Go-specific Cucumber runner
- `ginkgo-gomega` - Alternative BDD framework for Go
- `e2e-testing` - End-to-end patterns that Cucumber drives
