---
name: cypress-api
description: |
  API testing patterns with Cypress for CRUD operations.
  Covers BaseAPIController, entity controllers, test structure, and BDD documentation.
  Use this skill when writing API tests or creating new entity API controllers.
allowed-tools: Read, Glob, Grep, Bash(python:*), Bash(pnpm cy:run:*)
version: 1.0.0
---

# Cypress API Testing Skill

Patterns and tools for writing API tests with Cypress.

## Architecture Overview

```
contents/themes/{theme}/tests/cypress/
├── e2e/
│   └── api/                          # API tests (this skill)
│       ├── entities/
│       │   ├── {entity}-crud.cy.ts   # Entity CRUD tests
│       │   └── {entity}-crud.bdd.md  # BDD documentation
│       └── {feature}/
│           └── {feature}.cy.ts
├── src/
│   └── controllers/
│       ├── BaseAPIController.js      # Base class (DO NOT MODIFY)
│       └── {Entity}APIController.js  # Entity-specific controllers
└── fixtures/
    └── entities.json                 # AUTO-GENERATED entity config
```

## When to Use This Skill

- Writing API tests for entity CRUD operations
- Creating entity API controllers
- Testing authentication (API key, session)
- Validating API responses and error handling
- Testing pagination and filtering

## Test Tag System

### Permanent Tags (COMMIT)

| Tag | Purpose | When to Use |
|-----|---------|-------------|
| `@api` | API tests | Tests in `e2e/api/` |
| `@feat-{entity}` | Entity-specific | `@feat-tasks`, `@feat-customers` |
| `@crud` | CRUD operations | Tests covering Create/Read/Update/Delete |
| `@smoke` | Critical path tests | Must-pass tests |
| `@regression` | Full test suite | All tests |
| `@security` | Security tests | Auth validation tests |

### Temporary Tags (NEVER COMMIT)

| Tag | Purpose | When to Use |
|-----|---------|-------------|
| `@in-develop` | Tests being fixed | During iteration loop |
| `@scope-{session}` | Session tests | All tests for current session |

**CRITICAL:** code-reviewer (Phase 16) BLOCKS if temporary tags remain.

## Test ID Convention

```
{ENTITY_SLUG_UPPER}_API_{NUMBER}

Examples:
- TASKS_API_001    → List entities
- TASKS_API_010    → Create entity
- TASKS_API_020    → Get by ID
- TASKS_API_030    → Update entity
- TASKS_API_040    → Delete entity
- TASKS_API_100    → Integration/lifecycle test

Number ranges:
- 001-009: LIST operations
- 010-019: CREATE operations
- 020-029: GET BY ID operations
- 030-039: UPDATE operations
- 040-049: DELETE operations
- 100+: Integration tests
```

## BaseAPIController Pattern

### Key Methods

```javascript
class BaseAPIController {
  constructor(baseUrl, apiKey, teamId, entityConfig) {
    this.baseUrl = baseUrl
    this.apiKey = apiKey
    this.teamId = teamId
    this.entitySlug = entityConfig.slug
  }

  // CRUD Methods
  list(options = {})                    // GET /api/v1/{entity}
  getById(id, options = {})            // GET /api/v1/{entity}/{id}
  create(data, options = {})           // POST /api/v1/{entity}
  update(id, data, options = {})       // PATCH /api/v1/{entity}/{id}
  delete(id, options = {})             // DELETE /api/v1/{entity}/{id}

  // Validation Methods
  validateSuccessResponse(response, expectedStatus)
  validatePaginatedResponse(response)
  validateBaseEntityFields(entity)

  // Utility Methods
  setApiKey(key)                       // Change API key
  setTeamId(teamId)                    // Change team context
  getHeaders()                         // Get request headers
}
```

### Entity Controller Structure

```javascript
import BaseAPIController from './BaseAPIController'
import entitiesConfig from '../fixtures/entities.json'

const { slug } = entitiesConfig.entities.tasks

class TasksAPIController extends BaseAPIController {
  constructor(baseUrl, apiKey, teamId) {
    super(baseUrl, apiKey, teamId, { slug })
  }

  // Semantic aliases
  getTasks(options = {}) {
    return this.list(options)
  }

  getTaskById(id, options = {}) {
    return this.getById(id, options)
  }

  createTask(data, options = {}) {
    return this.create(data, options)
  }

  updateTask(id, data, options = {}) {
    return this.update(id, data, options)
  }

  deleteTask(id, options = {}) {
    return this.delete(id, options)
  }

  // Data generators
  generateRandomTaskData(overrides = {}) {
    return {
      title: `Test Task ${Date.now()}`,
      description: 'Generated test task',
      status: 'active',
      ...overrides
    }
  }

  // Entity-specific validation
  validateTaskObject(entity, allowMetas = false) {
    this.validateBaseEntityFields(entity)
    expect(entity).to.have.property('title')
    expect(entity).to.have.property('status')
  }
}
```

## Authentication

### Dual Auth System

```javascript
// API Key Authentication (primary for API tests)
const api = new TasksAPIController(baseUrl, SUPERADMIN_API_KEY, TEAM_ID)

// Headers sent:
// - Authorization: Bearer {apiKey}
// - x-team-id: {teamId}

// Session Authentication (for UAT tests)
// Uses cy.session() - see cypress-e2e skill
```

### Test Users & API Keys

```javascript
// Test API keys (from fixtures or environment)
const SUPERADMIN_API_KEY = 'sk_test_...'  // Full access
const MEMBER_API_KEY = 'sk_member_...'     // Limited access

// Team IDs
const TEAM_ID = 'team-tmt-001'

// For session-based tests, see cypress-e2e skill for login helpers
```

### Auth Test Patterns

```javascript
// Test without API key
it('should reject request without API key', () => {
  const originalApiKey = api.apiKey
  api.setApiKey(null)

  api.list().then((response) => {
    expect(response.status).to.eq(401)
    expect(response.body.success).to.be.false
  })

  api.setApiKey(originalApiKey)
})

// Test without team context
it('should reject request without x-team-id', () => {
  const originalTeamId = api.teamId
  api.setTeamId(null)

  api.list().then((response) => {
    expect(response.status).to.eq(400)
    expect(response.body.code).to.eq('TEAM_CONTEXT_REQUIRED')
  })

  api.setTeamId(originalTeamId)
})
```

## HTTP Status Codes

| Code | Meaning | When Used |
|------|---------|-----------|
| 200 | OK | Successful GET, PATCH, DELETE |
| 201 | Created | Successful POST |
| 400 | Bad Request | Validation error, missing x-team-id |
| 401 | Unauthorized | Missing/invalid API key |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Entity doesn't exist |
| 409 | Conflict | Duplicate entry, constraint violation |
| 500 | Server Error | Internal error |

## Error Codes

| Code | Description |
|------|-------------|
| `TEAM_CONTEXT_REQUIRED` | Missing x-team-id header |
| `MISSING_API_KEY` | No authentication provided |
| `INVALID_API_KEY` | API key doesn't exist or expired |
| `AUTHENTICATION_REQUIRED` | Must provide auth credentials |
| `INSUFFICIENT_PERMISSIONS` | User lacks required scope |
| `VALIDATION_ERROR` | Request body validation failed |
| `NOT_FOUND` | Entity doesn't exist |
| `CONFLICT` | Duplicate or constraint violation |

## Test Structure

```typescript
describe('{Entity} API - CRUD Operations', {
  tags: ['@api', '@feat-{entity}', '@crud', '@regression']
}, () => {
  let api: any
  let createdEntities: any[] = []

  const SUPERADMIN_API_KEY = '...'
  const TEAM_ID = 'team-tmt-001'
  const BASE_URL = Cypress.config('baseUrl')

  before(() => {
    api = new EntityAPIController(BASE_URL, SUPERADMIN_API_KEY, TEAM_ID)
  })

  beforeEach(() => {
    allure.epic('API')
    allure.feature('Entities')
  })

  afterEach(() => {
    // CRITICAL: Cleanup created entities
    createdEntities.forEach((entity) => {
      if (entity?.id) {
        api.delete(entity.id)
      }
    })
    createdEntities = []
  })

  // Tests...
})
```

## BDD Documentation Format (API)

API tests use YAML frontmatter + `## @test` sections:

```markdown
---
feature: {Entity} API
priority: high
tags: [api, feat-{entity}, crud, regression]
grepTags: ["@api", "@feat-{entity}"]
coverage: N tests
---

# {Entity} API

> API tests for /api/v1/{entity} endpoints.

## Endpoints Covered

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/{entity}` | GET | List entities |
| `/api/v1/{entity}` | POST | Create entity |
| `/api/v1/{entity}/{id}` | GET | Get entity by ID |
| `/api/v1/{entity}/{id}` | PATCH | Update entity |
| `/api/v1/{entity}/{id}` | DELETE | Delete entity |

---

## @test {ENTITY}_API_001: List entities

### Metadata
- **Priority:** Critical
- **Type:** Smoke
- **Tags:** api, {entity}, list
- **Grep:** `@smoke @feat-{entity}`

\`\`\`gherkin:en
Scenario: List entities with valid API key

Given I have a valid superadmin API key
And I have x-team-id header set
When I make a GET request to /api/v1/{entity}
Then the response status should be 200
And the response body should have success true
And the data should contain paginated results
\`\`\`

\`\`\`gherkin:es
Scenario: Listar entidades con API key válida

Given tengo una API key de superadmin válida
And tengo el header x-team-id configurado
When hago una solicitud GET a /api/v1/{entity}
Then el status de respuesta debería ser 200
And el body debería tener success true
And los datos deberían contener resultados paginados
\`\`\`

### Expected Results
- Status: 200 OK
- Response contains paginated data array
- Info contains total, page, limit

---

## Response Format

### Success Response (200)
\`\`\`json
{
  "success": true,
  "data": [...],
  "info": {
    "total": 10,
    "page": 1,
    "limit": 10
  }
}
\`\`\`

### Error Response (401)
\`\`\`json
{
  "success": false,
  "error": {
    "message": "Authentication required",
    "code": "AUTHENTICATION_REQUIRED"
  }
}
\`\`\`

---

## Test Summary

| Test ID | Endpoint | Description | Tags |
|---------|----------|-------------|------|
| {ENTITY}_API_001 | GET / | List with valid auth | `@smoke` |
| {ENTITY}_API_010 | POST / | Create with valid data | `@smoke` |
| {ENTITY}_API_020 | GET /{id} | Get by valid ID | |
| {ENTITY}_API_030 | PATCH /{id} | Update with valid data | |
| {ENTITY}_API_040 | DELETE /{id} | Delete by valid ID | |
```

## Scripts

### Generate API Controller

```bash
# Generate API controller from template
python3 .claude/skills/cypress-api/scripts/generate-api-controller.py \
  --entity tasks \
  --theme default

# Preview without writing
python3 .claude/skills/cypress-api/scripts/generate-api-controller.py \
  --entity tasks \
  --theme default \
  --dry-run
```

### Generate API Test

```bash
# Generate API test file + BDD documentation
python3 .claude/skills/cypress-api/scripts/generate-api-test.py \
  --entity tasks \
  --theme default \
  --with-bdd

# Preview without writing
python3 .claude/skills/cypress-api/scripts/generate-api-test.py \
  --entity tasks \
  --theme default \
  --with-bdd \
  --dry-run
```

## Test Execution Commands

```bash
# Run specific API test file
pnpm cy:run --spec "contents/themes/default/tests/cypress/e2e/api/entities/tasks-crud.cy.ts"

# Run all API tests
pnpm cy:run --env grepTags="@api"

# Run entity-specific API tests
pnpm cy:run --env grepTags="@feat-tasks,@api"

# Run smoke API tests
pnpm cy:run --env grepTags="@api,@smoke"

# Run @in-develop tests only (during iteration)
pnpm cy:run --env grepTags="@in-develop"
```

## Anti-Patterns

```javascript
// NEVER: Hardcoded entity slugs
const endpoint = '/api/v1/tasks'

// CORRECT: From entities.json
const { slug } = entitiesConfig.entities.tasks
const endpoint = `/api/v1/${slug}`

// NEVER: Fixed timeouts
cy.wait(3000)

// CORRECT: Use promise chaining
api.create(data).then((response) => {
  // Handle response
})

// NEVER: Skip cleanup
afterEach(() => {
  // Missing cleanup!
})

// CORRECT: Always cleanup created entities
afterEach(() => {
  createdEntities.forEach((entity) => {
    if (entity?.id) api.delete(entity.id)
  })
  createdEntities = []
})

// NEVER: Modify shared state without restoring
api.setApiKey(null)
// Tests continue with null key...

// CORRECT: Always restore original state
const original = api.apiKey
api.setApiKey(null)
// Test...
api.setApiKey(original)
```

## Checklist

Before finalizing API tests:

- [ ] Uses entity API controller (extends BaseAPIController)
- [ ] Uses correct test ID convention (`{ENTITY}_API_{NUMBER}`)
- [ ] Includes cleanup in `afterEach`
- [ ] Tests authentication (401 without key)
- [ ] Tests team context (400 without x-team-id)
- [ ] Includes permanent tags (`@api`, `@feat-{entity}`, `@crud`)
- [ ] NO temporary tags (`@in-develop`, `@scope-{session}`)
- [ ] Has corresponding `.bdd.md` documentation file
- [ ] BDD uses YAML frontmatter + `## @test` format
- [ ] BDD is bilingual (`:en` and `:es` gherkin blocks)

## Related Skills

- `cypress-e2e` - UAT testing patterns
- `cypress-selectors` - Selector architecture
- `better-auth` - Authentication patterns
