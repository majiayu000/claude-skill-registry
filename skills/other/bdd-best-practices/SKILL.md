---
name: bdd-best-practices
description: Universal BDD best practices for writing high-quality executable specifications
category: Testing BDD
---

# Skill: bdd-best-practices

## What I do

I provide universal best practices for Behaviour-Driven Development, focusing on bridge building between business and technical stakeholders through clear, outcome-oriented executable specifications.

## When to use me

- Defining business-critical workflows (registration, payments, data export)
- Establishing shared language through concrete examples
- Structuring scenarios for long-term maintainability
- Deciding what should be a BDD test versus a unit test
- Refining Gherkin steps to be survivable across UI changes
- Applying BDD-style describe/context/it structure to unit tests (RSpec, Ginkgo, Jest)

## Core principles

1. **Business Outcomes** — Describe WHAT the system does, not HOW it works
2. **Concrete Examples** — Use real data points to ground abstract rules
3. **The Three Amigos** — Collaborate early with PO, Tester, and Developer
4. **Declarative Style** — Focus on the goal, hide the implementation in step definitions
5. **Living Documentation** — Ensure specs are readable by non-technical stakeholders

## Patterns & examples

**Outcome-focused Scenario:**
```gherkin
# ✅ Correct: Business value documentation
Scenario: Customer receives bulk discount
  Given I have items worth £100 in my basket
  And a "10% off £50+" promotion is active
  When I complete the checkout
  Then the total should be £90
  And the confirmation email should show the discount
```

**Step Definition Encapsulation:**
```javascript
// ✅ Correct: HOW is hidden in step definitions
When("I log in", () => {
  page.fill("#email", "alice@example.com")
  page.fill("#password", "secret")
  page.click("#submit")
  page.waitForNavigation()
})
```

**The Test Pyramid Ratio:**
- **Acceptance/E2E (20%)** — Critical user journeys; Gherkin/Cucumber, Godog, Cypress
- **Integration (40%)** — Service boundaries and data transformations
- **Unit (40%)** — Algorithms, calculations, UI mechanics; RSpec, Ginkgo, Jest describe/it blocks are BDD at this level

## Anti-patterns to avoid

- ❌ **UI Mechanics** (`When I click the blue button`) — Use business actions instead
- ❌ **Keyboard Shortcuts** (`When I press Tab`) — Test the workflow goal
- ❌ **Incidental Detail** — Don't include IDs or internal data structures in Gherkin
- ❌ **Scenario Bloat** — Keep scenarios to 3-8 steps; split if they exceed 15
- ❌ **Duplicate Coverage** — Don't test validation logic in BDD if unit tests cover it
- ❌ **Form Field Typing** (`env.TypeText()` in steps) — Create data via domain/service instead
- ❌ **Form Navigation** (Tab between fields in steps) — Data creation should bypass form UI entirely

## KaRiya TUI: Declarative Data Creation

**ARCHITECTURAL DECISION**: BDD steps that create or modify data MUST do so via the domain/service layer, not by driving form UI.

**Why**: `TypeText()` sends characters one-by-one through the Bubble Tea update loop. This is timing-dependent, fragile, and tests huh form mechanics rather than business behaviour.

**Pattern**:
1. **Given/When steps that create data** → Use service/repository to create, inject into intent state
2. **When steps that trigger actions** → Use app navigation keys (legitimate interaction)
3. **Then steps that verify outcomes** → Use `env.GetView()` to check what the user would see

**Legitimate app interactions** (NOT anti-patterns):
- Opening editors (`env.PressKeyRune('f')`)
- Navigation (`env.NavigateDown()`, `env.PressKeyRune('j')`)
- Confirmation (`env.Confirm()`)
- Cancellation (`env.Cancel()`)

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Testing-BDD/BDD Best Practices.md`

## Related skills

- `bdd-workflow` - The overall BDD outside-in development cycle
- `bdd-anti-patterns` - Comprehensive library of mistakes to avoid
- `cucumber` - Executable specification runner
- `bdd-workflow` - The inner loop of technical implementation
