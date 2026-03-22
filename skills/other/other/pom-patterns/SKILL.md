---
name: pom-patterns
description: |
  Page Object Model patterns for Cypress tests with hierarchical structure.
  Covers BasePOM, DashboardEntityPOM, entity POMs, and selector integration.
  Use this skill when creating new POMs or extending existing ones.
allowed-tools: Read, Glob, Grep, Bash(python:*)
version: 1.0.0
---

# POM Patterns Skill

Patterns and tools for creating Page Object Models (POMs) for Cypress tests.

## Architecture Overview

```
contents/themes/{theme}/tests/cypress/src/
├── core/
│   ├── BasePOM.ts                # Base class for all POMs
│   └── DashboardEntityPOM.ts     # Entity POM base (CRUD operations)
├── entities/
│   ├── TasksPOM.ts               # Entity-specific POM
│   ├── PostsPOM.ts               # Entity-specific POM
│   └── {Entity}POM.ts            # Pattern: extend DashboardEntityPOM
├── features/
│   └── {Feature}POM.ts           # Non-entity feature POMs
├── selectors.ts                  # Re-exports from lib/selectors.ts
└── fixtures/
    └── entities.json             # Auto-generated entity config
```

## When to Use This Skill

- Creating a new entity POM
- Creating a feature-specific POM
- Extending DashboardEntityPOM with custom methods
- Understanding POM inheritance hierarchy
- Working with selectors in tests

## POM Hierarchy

```
BasePOM
    │
    ├── DashboardEntityPOM (entities with CRUD)
    │       ├── TasksPOM
    │       ├── PostsPOM
    │       └── {Entity}POM
    │
    └── {Feature}POM (non-entity features)
            ├── AuthPOM
            ├── OnboardingPOM
            └── SettingsPOM
```

## Core Concepts

### 1. BasePOM

**Location:** `contents/themes/{theme}/tests/cypress/src/core/BasePOM.ts`

Provides:
- Selector pattern replacement (`{index}`, `{id}`)
- Fluent interface support (return `this`)
- `cy()` helper method for cleaner selectors

```typescript
// Key methods
export abstract class BasePOM {
  // Get Cypress chainable by selector
  protected cy(selector: string): Cypress.Chainable<JQuery<HTMLElement>> {
    return cy.get(`[data-cy="${selector}"]`)
  }

  // Replace placeholders in selector patterns
  protected replacePattern(pattern: string, replacements: Record<string, string>): string {
    let result = pattern
    for (const [key, value] of Object.entries(replacements)) {
      result = result.replace(`{${key}}`, value)
    }
    return result
  }
}
```

### 2. DashboardEntityPOM

**Location:** `contents/themes/{theme}/tests/cypress/src/core/DashboardEntityPOM.ts`

Extends BasePOM with:
- Standard CRUD navigation (`visitList()`, `visitCreate()`, `visitEdit()`)
- Table operations (`getTableRow()`, `selectRow()`, `selectAllRows()`)
- Form operations (`getField()`, `fillField()`)
- API interceptors (`interceptList()`, `interceptCreate()`, `interceptUpdate()`, `interceptDelete()`)
- Bulk actions (`executeBulkAction()`)
- Status management (`changeStatus()`)

```typescript
export class DashboardEntityPOM extends BasePOM {
  protected entitySlug: string

  constructor(entitySlug: string) {
    super()
    this.entitySlug = entitySlug
  }

  // Navigation
  visitList(): this { /* ... */ return this }
  visitCreate(): this { /* ... */ return this }
  visitEdit(id: string): this { /* ... */ return this }

  // Table operations
  getTableRow(index: number): Cypress.Chainable { /* ... */ }
  clickTableRow(index: number): this { /* ... */ return this }

  // API Interceptors
  interceptList(alias: string = 'getList'): this { /* ... */ return this }
  interceptCreate(alias: string = 'postCreate'): this { /* ... */ return this }

  // Form operations
  fillField(fieldName: string, value: string): this { /* ... */ return this }
}
```

### 3. Entity POM Pattern

**Location:** `contents/themes/{theme}/tests/cypress/src/entities/{Entity}POM.ts`

```typescript
import { DashboardEntityPOM } from '../core/DashboardEntityPOM'
import { cySelector } from '../selectors'
import entitiesConfig from '../fixtures/entities.json'

// Form interface based on entity fields
interface TaskFormData {
  title?: string
  description?: string
  priority?: string
  status?: string
}

export class TasksPOM extends DashboardEntityPOM {
  constructor() {
    // Use entity slug from config
    super(entitiesConfig.entities.tasks.slug)
  }

  // Factory pattern (MANDATORY)
  static create(): TasksPOM {
    return new TasksPOM()
  }

  // Entity-specific selectors
  get elements() {
    return {
      // Use cySelector for all selectors
      priorityFilter: cySelector('entities.tasks.filters.priority'),
      statusBadge: cySelector('entities.tasks.list.statusBadge'),
    }
  }

  // Entity-specific form filling
  fillTaskForm(data: TaskFormData): this {
    if (data.title) this.fillField('title', data.title)
    if (data.description) this.fillField('description', data.description)
    if (data.priority) this.selectField('priority', data.priority)
    if (data.status) this.selectField('status', data.status)
    return this
  }

  // Entity-specific workflows
  createTask(data: TaskFormData): this {
    return this
      .visitCreate()
      .interceptCreate()
      .fillTaskForm(data)
      .submitForm()
      .waitForCreate()
  }
}
```

## Selector Integration

### Using cySelector()

**CRITICAL: Always use `cySelector()` from the selectors module, never hardcode selectors.**

```typescript
import { cySelector, sel } from '../selectors'

class MyPOM extends BasePOM {
  get elements() {
    return {
      // ✅ CORRECT - Use cySelector
      loginForm: cySelector('auth.login.form'),
      submitButton: cySelector('auth.login.submit'),

      // For dynamic selectors with replacements
      tableRow: (id: string) => cySelector('entities.tasks.row', { id }),
      faqItem: (index: number) => cySelector('blocks.faqAccordion.item', { index: String(index) }),
    }
  }

  // ❌ WRONG - Never hardcode selectors
  // get loginForm() { return cy.get('[data-cy="login-form"]') }
}
```

### Selector Paths

```typescript
// Core selectors (from CORE_SELECTORS)
cySelector('auth.login.form')        // Login form
cySelector('auth.login.submit')      // Submit button
cySelector('dashboard.sidebar')      // Sidebar
cySelector('common.toast.success')   // Success toast

// Entity selectors (from CORE_SELECTORS)
cySelector('entities.{entity}.list.table')     // Entity table
cySelector('entities.{entity}.list.row')       // Table row (needs {id})
cySelector('entities.{entity}.form.submit')    // Form submit

// Block selectors (from BLOCK_SELECTORS)
cySelector('blocks.hero.container')            // Hero block
cySelector('blocks.faqAccordion.item', { index: '0' })  // FAQ item
```

## API Interceptor Pattern

**CRITICAL: Use interceptors for deterministic waits, never `cy.wait(timeout)`.**

```typescript
class TasksPOM extends DashboardEntityPOM {
  // Intercept before action
  interceptList(alias: string = 'getTasksList'): this {
    cy.intercept('GET', `/api/v1/entities/${this.entitySlug}*`).as(alias)
    return this
  }

  // Wait after action
  waitForList(alias: string = 'getTasksList'): this {
    cy.wait(`@${alias}`)
    return this
  }

  // Combined pattern
  loadList(): this {
    return this
      .interceptList()
      .visitList()
      .waitForList()
  }
}
```

## Fluent Interface

**All methods that perform actions should return `this` for chaining.**

```typescript
class TasksPOM extends DashboardEntityPOM {
  // ✅ CORRECT - Returns this for chaining
  fillTitle(value: string): this {
    cy.get(this.elements.titleInput).type(value)
    return this
  }

  // ❌ WRONG - Breaks the chain
  fillTitle(value: string): void {
    cy.get(this.elements.titleInput).type(value)
  }
}

// Usage with fluent interface
TasksPOM.create()
  .visitCreate()
  .interceptCreate()
  .fillTitle('My Task')
  .fillDescription('Description')
  .submitForm()
  .waitForCreate()
  .assertSuccessToast()
```

## entities.json Fixture

**Location:** `contents/themes/{theme}/tests/cypress/fixtures/entities.json`

Auto-generated fixture containing entity configurations:

```json
{
  "entities": {
    "tasks": {
      "slug": "tasks",
      "singular": "Task",
      "plural": "Tasks",
      "tableName": "tasks",
      "fields": {
        "title": { "type": "text", "required": true },
        "description": { "type": "textarea" },
        "priority": { "type": "select", "options": ["low", "medium", "high"] },
        "status": { "type": "select", "options": ["draft", "active", "completed"] }
      },
      "filters": ["status", "priority"]
    }
  }
}
```

**Usage in POM:**

```typescript
import entitiesConfig from '../fixtures/entities.json'

class TasksPOM extends DashboardEntityPOM {
  constructor() {
    super(entitiesConfig.entities.tasks.slug)
  }

  get entityConfig() {
    return entitiesConfig.entities.tasks
  }
}
```

## Scripts

### Generate Entity POM

```bash
# Generate a new entity POM
python3 .claude/skills/pom-patterns/scripts/generate-pom.py \
  --entity products \
  --theme default

# Preview without writing
python3 .claude/skills/pom-patterns/scripts/generate-pom.py \
  --entity products \
  --theme default \
  --dry-run

# Specify custom fields
python3 .claude/skills/pom-patterns/scripts/generate-pom.py \
  --entity products \
  --theme default \
  --fields "title,description,price,category,status"
```

## Standard Methods

### Navigation Methods

| Method | Description |
|--------|-------------|
| `visitList()` | Navigate to entity list page |
| `visitCreate()` | Navigate to create form |
| `visitEdit(id)` | Navigate to edit form |
| `visitView(id)` | Navigate to detail view |

### Table Methods

| Method | Description |
|--------|-------------|
| `getTableRow(index)` | Get row by index |
| `clickTableRow(index)` | Click row by index |
| `selectRow(index)` | Select row checkbox |
| `selectAllRows()` | Select all rows |
| `getRowCount()` | Get number of rows |

### Form Methods

| Method | Description |
|--------|-------------|
| `fillField(name, value)` | Fill text field |
| `selectField(name, value)` | Select dropdown option |
| `checkField(name)` | Check checkbox |
| `submitForm()` | Click submit button |

### Assertion Methods

| Method | Description |
|--------|-------------|
| `assertSuccessToast()` | Assert success toast visible |
| `assertErrorToast()` | Assert error toast visible |
| `assertOnListPage()` | Assert on list page |
| `assertOnCreatePage()` | Assert on create page |
| `assertRowExists(text)` | Assert table row with text |

### Interceptor Methods

| Method | Description |
|--------|-------------|
| `interceptList()` | Intercept GET list request |
| `interceptCreate()` | Intercept POST create request |
| `interceptUpdate()` | Intercept PATCH update request |
| `interceptDelete()` | Intercept DELETE request |
| `waitForList()` | Wait for list response |
| `waitForCreate()` | Wait for create response |

## Anti-Patterns

```typescript
// ❌ NEVER: Hardcoded selectors
cy.get('[data-cy="task-title"]')

// ✅ CORRECT: Use cySelector
cy.get(cySelector('entities.tasks.form.title'))

// ❌ NEVER: Fixed timeouts
cy.wait(3000)

// ✅ CORRECT: Use interceptors
this.interceptCreate().submitForm().waitForCreate()

// ❌ NEVER: Direct page visits without interceptor
visitList() {
  cy.visit('/dashboard/tasks')
}

// ✅ CORRECT: Intercept before navigation
loadList() {
  return this.interceptList().visitList().waitForList()
}

// ❌ NEVER: Breaking fluent interface
fillTitle(value: string): void { ... }

// ✅ CORRECT: Return this
fillTitle(value: string): this { ... return this }

// ❌ NEVER: Missing factory pattern
const pom = new TasksPOM()

// ✅ CORRECT: Use factory
const pom = TasksPOM.create()
```

## Checklist

Before finalizing a POM:

- [ ] Extends correct base class (DashboardEntityPOM for entities)
- [ ] Uses factory pattern (`static create()`)
- [ ] All methods return `this` (fluent interface)
- [ ] Uses `cySelector()` for all selectors (no hardcoded strings)
- [ ] Uses API interceptors for all async operations
- [ ] Form interface defined based on entity fields
- [ ] Entity-specific methods documented
- [ ] Follows naming convention: `{Entity}POM.ts`
