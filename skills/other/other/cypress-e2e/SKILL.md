---
name: cypress-e2e
description: |
  End-to-End testing patterns with Cypress for UAT tests.
  Covers test structure, cy.session(), batch execution, tags, POMs, and BDD documentation.
  Use this skill when writing UAT tests or creating new entity test files.
allowed-tools: Read, Glob, Grep, Bash(python:*), Bash(pnpm cy:run:*)
version: 1.0.0
---

# Cypress E2E Testing Skill

Patterns and tools for writing End-to-End UAT tests with Cypress.

## Architecture Overview

```
contents/themes/{theme}/tests/cypress/
├── e2e/
│   ├── api/                       # API tests (see cypress-api skill)
│   │   └── entities/
│   │       └── {entity}-crud.cy.ts
│   ├── uat/                       # UAT tests (this skill)
│   │   ├── {entity}/
│   │   │   ├── {entity}-owner.cy.ts
│   │   │   ├── {entity}-owner.bdd.md    # BDD documentation
│   │   │   └── {entity}-member.cy.ts
│   │   └── {feature}/
│   │       └── {feature}.cy.ts
│   └── _selectors/                # Selector validation tests
│       └── {feature}-selectors.cy.ts
├── src/
│   ├── core/                      # Base classes (DO NOT MODIFY)
│   │   ├── BasePOM.ts
│   │   ├── DashboardEntityPOM.ts
│   │   └── AuthPOM.ts
│   ├── entities/                  # Entity POMs
│   │   └── {Entity}POM.ts
│   ├── features/                  # Feature POMs
│   │   └── {Feature}POM.ts
│   ├── controllers/               # API controllers
│   │   └── {Entity}APIController.js
│   ├── helpers/
│   │   └── ApiInterceptor.ts
│   ├── session-helpers.ts         # Login functions
│   └── selectors.ts               # Theme selectors
└── fixtures/
    └── entities.json              # AUTO-GENERATED entity config
```

## When to Use This Skill

- Writing UAT tests for entity CRUD operations
- Creating role-based test suites (owner, member, viewer)
- Implementing cy.session() for cached authentication
- Using Page Object Model pattern
- Generating BDD documentation

## Test Tag System

### Permanent Tags (COMMIT)

| Tag | Purpose | When to Use |
|-----|---------|-------------|
| `@api` | API tests | Tests in `e2e/api/` |
| `@uat` | UAT tests | Tests in `e2e/uat/` |
| `@smoke` | Critical path tests | Must-pass tests |
| `@regression` | Full test suite | All tests |
| `@feat-{entity}` | Entity-specific | `@feat-tasks`, `@feat-customers` |
| `@role-{role}` | Role-based tests | `@role-owner`, `@role-member` |
| `@crud` | CRUD operations | Tests covering Create/Read/Update/Delete |

### Temporary Tags (NEVER COMMIT)

| Tag | Purpose | When to Use |
|-----|---------|-------------|
| `@in-develop` | Tests being fixed | During iteration loop |
| `@scope-{session}` | Session tests | All tests for current session |

**CRITICAL:** code-reviewer (Phase 16) BLOCKS if temporary tags remain.

## Test ID Convention

```
{ROLE}_{ENTITY_SLUG_UPPER}_{ACTION}_{NUMBER}

Examples:
- OWNER_TASK_CREATE_001
- MEMBER_CUSTOMER_READ_001
- ADMIN_POST_DELETE_001
```

## Session Helpers (cy.session)

### Available Login Functions

```typescript
import {
  loginAsOwner,
  loginAsAdmin,
  loginAsMember,
  loginAsEditor,
  loginAsViewer,
  loginAsSuperadmin,
  loginAsDeveloper
} from '../session-helpers'
```

### Test Users

```typescript
// Team-based users (password: 'Test1234')
DEFAULT_THEME_USERS = {
  OWNER: 'carlos.mendoza@tmt.dev',      // Everpoint Labs (owner)
  ADMIN: 'james.wilson@tmt.dev',        // Everpoint Labs (admin)
  MEMBER: 'emily.johnson@tmt.dev',      // Everpoint (member)
  EDITOR: 'diego.ramirez@tmt.dev',      // Everpoint Labs (editor)
  VIEWER: 'sarah.davis@tmt.dev',        // Ironvale Global (viewer)
}

// Core system users (password: 'Pandora1234')
CORE_USERS = {
  SUPERADMIN: 'superadmin@tmt.dev',     // Global superadmin
  DEVELOPER: 'developer@tmt.dev',       // Global developer
}
```

### Session Pattern

```typescript
describe('Entity CRUD - Owner Role', {
  tags: ['@uat', '@feat-tasks', '@role-owner', '@regression']
}, () => {
  const pom = TasksPOM.create()

  beforeEach(() => {
    // cy.session() handles caching automatically
    loginAsOwner()

    // Setup API intercepts BEFORE navigation
    pom.setupApiIntercepts()

    // Navigate with API wait
    pom.visitList()
    pom.api.waitForList()
  })

  it('OWNER_TASK_CREATE_001: should create new task', () => {
    // Test implementation
  })
})
```

## Page Object Model (POM) Pattern

### Entity POM Structure

```typescript
import { DashboardEntityPOM } from '../core/DashboardEntityPOM'
import entitiesConfig from '../../fixtures/entities.json'

export interface TaskFormData {
  title?: string
  description?: string
  priority?: string
  status?: string
}

export class TasksPOM extends DashboardEntityPOM {
  constructor() {
    // NEVER hardcode slugs - always from entities.json
    super(entitiesConfig.entities.tasks.slug)
  }

  // Factory pattern (MANDATORY)
  static create(): TasksPOM {
    return new TasksPOM()
  }

  // Entity-specific form filling
  fillTaskForm(data: TaskFormData): this {
    if (data.title) this.fillField('title', data.title)
    if (data.description) this.fillTextarea('description', data.description)
    if (data.priority) this.selectOption('priority', data.priority)
    return this
  }

  // Entity-specific workflows
  createTaskWithApiWait(data: TaskFormData): this {
    this.setupApiIntercepts()
    this.clickAdd()
    this.waitForForm()
    this.fillTaskForm(data)
    this.submitForm()
    this.api.waitForCreate()
    return this
  }
}
```

### DashboardEntityPOM Methods

| Method | Description |
|--------|-------------|
| `visitList()` | Navigate to entity list page |
| `visitCreate()` | Navigate to create form |
| `visitEdit(id)` | Navigate to edit form |
| `visitDetail(id)` | Navigate to detail page |
| `clickAdd()` | Click add button |
| `submitForm()` | Submit current form |
| `waitForList()` | Wait for list to load |
| `waitForForm()` | Wait for form to load |
| `waitForDetail()` | Wait for detail to load |
| `assertInList(text)` | Assert text in list |
| `assertNotInList(text)` | Assert text not in list |
| `assertTableVisible()` | Assert table is visible |

### ApiInterceptor Methods

| Method | Description |
|--------|-------------|
| `setupApiIntercepts()` | Setup all intercepts |
| `api.waitForList()` | Wait for GET list |
| `api.waitForCreate()` | Wait for POST create |
| `api.waitForUpdate()` | Wait for PATCH update |
| `api.waitForDelete()` | Wait for DELETE |

## Batch Execution Strategy

### Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| `BATCH_SIZE` | 5 | Tests per batch |
| `SUCCESS_THRESHOLD` | 0.9 | Minimum pass rate (90%) |
| `MAX_BATCH_RETRIES` | 3 | Max retries per batch |

### Workflow

```
1. PLAN: Document tests in tests.md
2. BATCH: Group into batches of 5
3. FOR EACH BATCH:
   a. TAG: Add @in-develop + @scope-{session}
   b. RUN: Execute with --env grepTags="@in-develop"
   c. FIX: Address failures
   d. RETRY: Until batch passes (max 3)
   e. UNTAG: Remove @in-develop (keep @scope)
4. FINAL: Run all with --env grepTags="@scope-{session}"
5. EVALUATE: Calculate pass rate
6. CLEANUP: Remove ALL temporary tags
```

### Pass Rate Thresholds

| Rate | Status | Action |
|------|--------|--------|
| 100% | GATE_PASSED | Continue to code-review |
| 90-99% | GATE_PASSED_WITH_WARNINGS | Document in pendings.md |
| <90% | GATE_FAILED | Block workflow |

## BDD Documentation Format

Each test file should have a corresponding `.bdd.md` file with bilingual documentation.

### UAT BDD Format

```markdown
# {Entity} UI - {Role} Role (Format: BDD/Gherkin - Bilingual)

> **Test File:** `{entity}-{role}.cy.ts`
> **Format:** Behavior-Driven Development (BDD) with Given/When/Then
> **Languages:** English / Spanish (side-by-side)
> **Total Tests:** N

---

## Feature: {Entity} Management - {Role} Role (Access Level)

<table>
<tr>
<th width="50%">English</th>
<th width="50%">Espanol</th>
</tr>
<tr>
<td>

As a **{Role}**
I want to **manage {entities} through the dashboard UI**
So that **I can perform operations for my team**

</td>
<td>

Como **{Role}**
Quiero **gestionar {entidades} a traves del dashboard**
Para **realizar operaciones para mi equipo**

</td>
</tr>
</table>

### Background

<table>
<tr>
<th width="50%">English</th>
<th width="50%">Espanol</th>
</tr>
<tr>
<td>

```gherkin
Given I am logged in as {Role} ({email})
And I have navigated to the {Entity} dashboard
And the list has loaded successfully
```

</td>
<td>

```gherkin
Given estoy logueado como {Role} ({email})
And he navegado al dashboard de {Entidad}
And la lista ha cargado exitosamente
```

</td>
</tr>
</table>

---

## CREATE - {Role} can create {entities}

### {ROLE}_{ENTITY}_CREATE_001: Create new {entity} successfully `@smoke` `@critical`

<table>
<tr>
<th width="50%">English</th>
<th width="50%">Espanol</th>
</tr>
<tr>
<td>

```gherkin
Scenario: {Role} creates a simple {entity}

Given I am logged in as {Role}
And I am on the {Entity} list page
When I click the "Add" button
Then the creation form should appear

When I enter "Test {Entity}" in the Title field
And I click the "Save" button
Then the form should submit successfully
And I should see a success message
And I should be redirected to the list
And I should see "Test {Entity}" in the list
```

</td>
<td>

```gherkin
Scenario: {Role} crea un/a {entidad} simple

Given estoy logueado como {Role}
And estoy en la pagina de lista de {Entidades}
When hago clic en el boton "Agregar"
Then deberia aparecer el formulario de creacion

When ingreso "Test {Entidad}" en el campo Titulo
And hago clic en el boton "Guardar"
Then el formulario deberia enviarse exitosamente
And deberia ver un mensaje de exito
And deberia ser redirigido a la lista
And deberia ver "Test {Entidad}" en la lista
```

</td>
</tr>
</table>

**Visual Flow:**
```
[List Page] → [Click Add] → [Form] → [Fill Fields] → [Save] → [List with new item]
```

---

## Summary

| Test ID | Operation | Description | Tags |
|---------|-----------|-------------|------|
| {ROLE}_{ENTITY}_CREATE_001 | CREATE | Create with title | `@smoke` `@critical` |
| {ROLE}_{ENTITY}_READ_001 | READ | View list | `@smoke` |
| {ROLE}_{ENTITY}_UPDATE_001 | UPDATE | Edit existing | |
| {ROLE}_{ENTITY}_DELETE_001 | DELETE | Delete | `@critical` |
```

## Scripts

### Generate UAT Test

```bash
# Generate test file + BDD documentation
python3 .claude/skills/cypress-e2e/scripts/generate-uat-test.py \
  --entity tasks \
  --theme default \
  --role owner \
  --with-bdd

# Preview without writing
python3 .claude/skills/cypress-e2e/scripts/generate-uat-test.py \
  --entity tasks \
  --theme default \
  --role owner \
  --with-bdd \
  --dry-run
```

### Generate Entity POM

Uses the `pom-patterns` skill script (shared, not duplicated):

```bash
# Generate POM from template
python3 .claude/skills/pom-patterns/scripts/generate-pom.py \
  --entity tasks \
  --theme default

# With custom fields
python3 .claude/skills/pom-patterns/scripts/generate-pom.py \
  --entity products \
  --theme default \
  --fields "name,description,price,category,status"
```

See `pom-patterns` skill for full documentation.

### Extract Selectors

```bash
# Scan component for data-cy attributes
python3 .claude/skills/cypress-e2e/scripts/extract-selectors.py \
  --component contents/themes/default/components/TaskList.tsx
```

## Test Execution Commands

```bash
# Run specific test file
pnpm cy:run --spec "contents/themes/default/tests/cypress/e2e/uat/tasks/tasks-owner.cy.ts"

# Run by tag
pnpm cy:run --env grepTags="@feat-tasks"
pnpm cy:run --env grepTags="@smoke"
pnpm cy:run --env grepTags="@role-owner"

# Run @in-develop tests only (during iteration)
pnpm cy:run --env grepTags="@in-develop"

# Run all session tests
pnpm cy:run --env grepTags="@scope-2025-12-30-tasks-v1"
```

## Anti-Patterns

```typescript
// NEVER: Hardcoded selectors
cy.get('[data-cy="task-title"]')

// CORRECT: Use cySelector from selectors.ts
import { cySelector } from '../selectors'
cy.get(cySelector('entities.form.field', { slug: 'tasks', name: 'title' }))

// NEVER: Fixed timeouts
cy.wait(3000)

// CORRECT: Use API interceptors
pom.api.waitForCreate()

// NEVER: Hardcoded entity slugs
super('tasks')

// CORRECT: From entities.json
super(entitiesConfig.entities.tasks.slug)

// NEVER: Login in every test
beforeEach(() => {
  cy.visit('/login')
  cy.get('[data-cy="email"]').type('user@test.com')
  // ...
})

// CORRECT: Use cy.session() via helpers
beforeEach(() => {
  loginAsOwner() // Session is cached
})

// NEVER: Commit temporary tags
{ tags: ['@in-develop', '@scope-2025-12-30-tasks-v1'] }

// CORRECT: Remove before commit
{ tags: ['@uat', '@feat-tasks', '@role-owner', '@regression'] }
```

## Checklist

Before finalizing UAT tests:

- [ ] Uses session helpers (`loginAsOwner()`, etc.)
- [ ] Uses POM pattern (extends DashboardEntityPOM)
- [ ] Uses API interceptors for deterministic waits
- [ ] Follows test ID convention (`{ROLE}_{ENTITY}_{ACTION}_{NUMBER}`)
- [ ] Includes permanent tags (`@uat`, `@feat-{entity}`, `@role-{role}`)
- [ ] NO temporary tags (`@in-develop`, `@scope-{session}`)
- [ ] Has corresponding `.bdd.md` documentation file
- [ ] BDD is bilingual (English/Spanish)

## Related Skills

- `cypress-api` - API testing patterns
- `cypress-selectors` - Selector architecture
- `pom-patterns` - Page Object Model patterns
