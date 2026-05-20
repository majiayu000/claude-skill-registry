---
name: cucumber-cypress
description: Cucumber BDD with Cypress policies. Use when writing Gherkin scenarios with Cypress step definitions. Do NOT use for Playwright-based BDD -- use cucumber-playwright instead. Do NOT use for non-BDD Cypress tests.
durability: encoded-preference
---

# Cucumber + Cypress Policies

Use `@badeball/cypress-cucumber-preprocessor` for Cypress + Cucumber.

## Project Structure

```
cypress/
├── e2e/
│   ├── features/*.feature
│   └── step_definitions/*.steps.ts
├── support/
cypress.config.ts
```

## Gherkin Best Practices

### Use Scenario Outline for Multiple Cases

```gherkin
Scenario Outline: Login validation
  Given I am on the login page
  When I enter "<email>" as email
  And I enter "<password>" as password
  Then I should see "<message>"

  Examples:
    | email            | password | message             |
    | user@example.com | valid    | Welcome             |
    | user@example.com | wrong    | Invalid credentials |
```

### Keep Steps Reusable

Write steps that can be shared across features.

## Step Definition Policies

### Use data-testid Selectors

```typescript
// GOOD
cy.get('[data-testid="email-input"]').type(email)

// BAD: Brittle CSS selectors
cy.get('.input-field-xyz').type(email)
```

### Import from Correct Package

```typescript
import { Given, When, Then } from '@badeball/cypress-cucumber-preprocessor'
```

### Hooks for Setup/Cleanup

```typescript
import { Before, After } from '@badeball/cypress-cucumber-preprocessor'

Before(() => {
  cy.clearCookies()
  cy.clearLocalStorage()
})
```

### Tagged Hooks for Specific Scenarios

```typescript
Before({ tags: '@login' }, () => {
  cy.fixture('users').as('users')
})
```

## Commands

```bash
npx cypress run
npx cypress run --spec "cypress/e2e/features/login.feature"
npx cypress open  # Interactive
```

## Configuration

For setup details, use context7 to query `@badeball/cypress-cucumber-preprocessor` documentation.
