---
name: bdd-anti-patterns
description: Library of common BDD mistakes and how to fix them
category: Testing BDD
---

# Skill: bdd-anti-patterns

## What I do

I identify common BDD anti-patterns and provide fixes to keep tests stable, maintainable, and business-focused.

## When to use me

- Auditing existing Gherkin scenarios for fragility
- Refactoring slow or flaky E2E tests
- Moving low-level UI tests into unit test suites
- Clarifying vague or ambiguous test language
- Stabilising tests that depend on hard-coded data

## Core principles

1. **Test Behaviour, Not Presentation** — Avoid testing modals, animations, or styling
2. **Workflow over Mechanics** — Don't test buttons, keys, or gestures directly
3. **Outcome over Process** — Focus on the goal achieved, not the steps taken
4. **Data Flexibility** — Use generated or relative data instead of hard-coded IDs
5. **Single Responsibility** — One business rule per scenario

## Patterns & examples

**Fixing Modal Testing:**
- ❌ **Bad:** `Then the settings modal should appear and be centred`
- ✅ **Fixed:** `Then I should be able to update my preferences`

**Fixing Keyboard Mechanics:**
- ❌ **Bad:** `When I press the "j" key`
- ✅ **Fixed:** `When I navigate down the list`

**Fixing Vague Outcomes:**
- ❌ **Bad:** `Then the output should be good`
- ✅ **Fixed:** `Then the total should be £108.25 (including 8.25% tax)`

**Fixing Brittle Data:**
- ❌ **Bad:** `Given user ID 12345 exists`
- ✅ **Fixed:** `Given I have a registered user account`

## Anti-patterns to avoid

- ❌ **Modal Mechanics** — Testing how a dialog opens instead of what it does
- ❌ **Keyboard Shortcuts** — Coupling tests to specific input methods
- ❌ **Form Mechanics** — Testing tab order or focus instead of data entry
- ❌ **Implementation Details** — Testing internal function calls or database queries
- ❌ **Vague Language** — Scenarios that a non-technical person cannot understand
- ❌ **The "Mega-Scenario"** — One scenario testing 20+ steps of an entire journey
- ❌ **Character-by-character typing** — Using `TypeText()` to fill form fields in BDD steps
- ❌ **Tab navigation in steps** — Using `Tab`/`PressKey(tea.KeyTab)` to move between form fields
- ❌ **Field clearing in steps** — Using `ClearTextField()`/`PressKey(tea.KeyCtrlU)`/backspace loops

## KaRiya TUI Form Mechanics (CRITICAL)

BDD steps MUST be declarative — create data via domain/service layer, test behaviour only.

### Anti-pattern: Form field typing

```go
// ❌ Types chars one-by-one into huh form
func iAddANewFact(ctx context.Context, text string) (context.Context, error) {
    env := support.GetAppEnv(ctx)
    env.TypeText(text)  // Fragile, timing-dependent, tests form mechanics
    env.Confirm()
    return ctx, nil
}
```

### Anti-pattern: Multi-step form navigation

```go
// ❌ WRONG: Tab-type-tab-type chain tests form layout, not behaviour
func iCreateABurst(ctx context.Context, name, desc string) (context.Context, error) {
    env := support.GetAppEnv(ctx)
    env.ClearTextField()           // Clear existing text
    env.TypeText(name)             // Type into name field
    env.PressKey(tea.KeyTab)       // Tab to description
    env.TypeText(desc)             // Type into description field
    env.Confirm()                  // Submit
    return ctx, nil
}
```

### Correct: Declarative data creation

```go
// ✅ CORRECT: Create data via domain/service, inject into intent state
func iAddANewFact(ctx context.Context, text string) (context.Context, error) {
    env := support.GetAppEnv(ctx)
    fact := &career.Fact{Text: text}
    // Create via service/repo
    err := env.Service.SaveFact(ctx, fact)
    if err != nil { return ctx, err }
    // Wire into active intent's review state so it appears in the view
    intent := env.GetActiveIntent()
    intent.AddFactToReview(fact)
    return ctx, nil
}
```

### Legitimate app interaction

Not anti-patterns — these test real app navigation:

- `env.PressKeyRune('f')` — Opening editors (app navigation)
- `env.PressKeyRune('q')` — Quitting (app navigation)
- `env.Confirm()` — Confirming dialogs/modals (app interaction)
- `env.Cancel()` / escape — Cancelling (app interaction)
- `env.NavigateDown()` — List navigation (app navigation)
- `env.PressKeyRune('y'/'n')` — Yes/no prompts (app interaction)

### Decision rule

> If the step is **filling form fields** or **navigating between form controls**, it is an anti-pattern.
> If the step is **triggering an app action** (open, close, navigate, confirm), it is legitimate.

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Testing-BDD/BDD Anti Patterns.md`

## Related skills

- `bdd-workflow` - The foundational BDD development cycle
- `bdd-best-practices` - Positive patterns to follow
- `e2e-testing` - The execution layer for BDD scenarios
- `test-fixtures` - Managing data to avoid brittleness
