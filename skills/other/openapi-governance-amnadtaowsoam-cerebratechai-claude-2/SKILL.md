---
name: OpenAPI Governance
description: Comprehensive guide to OpenAPI governance, API design standards, automated linting, breaking change detection, and API lifecycle management
---

# OpenAPI Governance

## What is OpenAPI Governance?

**Definition:** Enforcing API design standards across an organization through automated validation and lifecycle management.

### Key Components

1. **API Design Standards:** Consistent patterns (naming, structure, errors)
2. **Automated Validation:** Linting rules enforced in CI/CD
3. **Breaking Change Detection:** Prevent accidental breaking changes
4. **API Lifecycle Management:** Design → Deploy → Deprecate

### Example
```
Developer creates API endpoint:
POST /api/users (wrong - should be /api/v1/users)

Linter catches in CI:
❌ Error: Missing version prefix in URL
❌ Error: Missing operation description
❌ Error: No example provided

Developer fixes → CI passes → Merge allowed
```

---

## Why Governance Matters

### 1. Consistency (Developers Know What to Expect)

**Without Governance:**
```
Service A: GET /api/v1/users?page=1&limit=20
Service B: GET /users?offset=0&count=20
Service C: GET /api/users?p=1&size=20

→ Every API is different, hard to learn
```

**With Governance:**
```
All services: GET /api/v1/{resource}?page=1&limit=20

→ Consistent patterns, easy to learn
```

### 2. Quality (Catch Issues Before Production)

**Automated Checks:**
- Missing descriptions
- Inconsistent naming
- Missing examples
- Security schemes not defined
- Breaking changes

### 3. Documentation (Auto-Generated, Always in Sync)

**Flow:**
```
OpenAPI spec → Swagger UI (interactive docs)
             → ReDoc (beautiful static docs)
             → Postman collection
             → Client SDKs

Spec is source of truth → Docs always accurate
```

### 4. Breaking Change Prevention

**Example:**
```
Developer removes field from response:

- name: string  (removed)
+ email: string (added)

Breaking change detector:
❌ Breaking change: Field 'name' removed from response
→ Requires major version bump (v1 → v2)
```

---

## OpenAPI Specification (OAS) 3.0/3.1

### Structure

```yaml
openapi: 3.0.3
info:
  title: User API
  version: 1.0.0
  description: API for managing users
  contact:
    name: API Team
    email: api@example.com

servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://staging-api.example.com/v1
    description: Staging

paths:
  /users:
    get:
      summary: List users
      operationId: listUsers
      tags: [Users]
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
            maximum: 100
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserList'
        '400':
          $ref: '#/components/responses/BadRequest'

components:
  schemas:
    User:
      type: object
      required: [id, email, name]
      properties:
        id:
          type: string
          format: uuid
          example: "123e4567-e89b-12d3-a456-426614174000"
        email:
          type: string
          format: email
          example: "user@example.com"
        name:
          type: string
          example: "John Doe"
        createdAt:
          type: string
          format: date-time
          example: "2024-01-15T10:00:00Z"
    
    UserList:
      type: object
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/User'
        pagination:
          $ref: '#/components/schemas/Pagination'
    
    Pagination:
      type: object
      properties:
        page:
          type: integer
        limit:
          type: integer
        total:
          type: integer
  
  responses:
    BadRequest:
      description: Bad request
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
  
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

security:
  - bearerAuth: []
```

### Data Types and Schemas

**Primitive Types:**
```yaml
string:
  type: string
  minLength: 1
  maxLength: 255

integer:
  type: integer
  minimum: 0
  maximum: 100

number:
  type: number
  format: float

boolean:
  type: boolean

date:
  type: string
  format: date-time  # ISO 8601
```

**Complex Types:**
```yaml
array:
  type: array
  items:
    type: string
  minItems: 1
  maxItems: 10

object:
  type: object
  properties:
    name:
      type: string
  required: [name]

enum:
  type: string
  enum: [ACTIVE, INACTIVE, PENDING]
```

### Request/Response Definitions

**Request Body:**
```yaml
requestBody:
  required: true
  content:
    application/json:
      schema:
        type: object
        required: [email, name]
        properties:
          email:
            type: string
            format: email
          name:
            type: string
      examples:
        example1:
          value:
            email: "user@example.com"
            name: "John Doe"
```

**Response:**
```yaml
responses:
  '201':
    description: User created
    headers:
      Location:
        schema:
          type: string
        description: URL of created user
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/User'
```

### Authentication Schemes

**Bearer Token:**
```yaml
securitySchemes:
  bearerAuth:
    type: http
    scheme: bearer
    bearerFormat: JWT
```

**API Key:**
```yaml
securitySchemes:
  apiKey:
    type: apiKey
    in: header
    name: X-API-Key
```

**OAuth 2.0:**
```yaml
securitySchemes:
  oauth2:
    type: oauth2
    flows:
      authorizationCode:
        authorizationUrl: https://auth.example.com/oauth/authorize
        tokenUrl: https://auth.example.com/oauth/token
        scopes:
          read: Read access
          write: Write access
```

---

## API Design Standards

### RESTful Conventions

**Resource Naming:**
```
✅ Good:
GET    /api/v1/users
POST   /api/v1/users
GET    /api/v1/users/{id}
PUT    /api/v1/users/{id}
DELETE /api/v1/users/{id}

❌ Bad:
GET    /api/v1/getUsers
POST   /api/v1/createUser
GET    /api/v1/user/{id}  (singular)
```

**HTTP Methods:**
- **GET:** Retrieve resource (idempotent, safe)
- **POST:** Create resource
- **PUT:** Replace resource (idempotent)
- **PATCH:** Update resource (partial)
- **DELETE:** Delete resource (idempotent)

### URL Structure

**Standard:**
```
https://api.example.com/v1/resources/{id}/subresources/{subId}

Examples:
GET /api/v1/users/123
GET /api/v1/users/123/orders
GET /api/v1/users/123/orders/456
```

**Rules:**
- Always include version (`/v1/`, `/v2/`)
- Use plural nouns (`users`, not `user`)
- Use kebab-case for multi-word resources (`user-profiles`)
- No trailing slashes
- Keep URLs short (max 3 levels deep)

### Query Parameters

**Pagination:**
```
GET /api/v1/users?page=1&limit=20

Response:
{
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "totalPages": 5
  }
}
```

**Filtering:**
```
GET /api/v1/users?status=active&role=admin
GET /api/v1/users?createdAfter=2024-01-01
```

**Sorting:**
```
GET /api/v1/users?sort=createdAt:desc
GET /api/v1/users?sort=-createdAt  (- means desc)
```

**Field Selection:**
```
GET /api/v1/users?fields=id,name,email
```

### Request/Response Format

**Request (JSON):**
```json
POST /api/v1/users
Content-Type: application/json

{
  "email": "user@example.com",
  "name": "John Doe",
  "role": "member"
}
```

**Response (JSON):**
```json
201 Created
Location: /api/v1/users/123
Content-Type: application/json

{
  "id": "123",
  "email": "user@example.com",
  "name": "John Doe",
  "role": "member",
  "createdAt": "2024-01-15T10:00:00Z"
}
```

### Error Format (RFC 7807 Problem Details)

**Standard Error:**
```json
400 Bad Request
Content-Type: application/problem+json

{
  "type": "https://example.com/errors/validation-error",
  "title": "Validation Error",
  "status": 400,
  "detail": "Email is required",
  "instance": "/api/v1/users",
  "errors": [
    {
      "field": "email",
      "message": "Email is required"
    }
  ]
}
```

**OpenAPI Schema:**
```yaml
components:
  schemas:
    Error:
      type: object
      required: [type, title, status]
      properties:
        type:
          type: string
          format: uri
        title:
          type: string
        status:
          type: integer
        detail:
          type: string
        instance:
          type: string
        errors:
          type: array
          items:
            type: object
            properties:
              field:
                type: string
              message:
                type: string
```

### Date Format (ISO 8601)

**Standard:**
```
2024-01-15T10:00:00Z  (UTC)
2024-01-15T10:00:00+07:00  (with timezone)
```

**OpenAPI:**
```yaml
createdAt:
  type: string
  format: date-time
  example: "2024-01-15T10:00:00Z"
```

### Pagination

**Cursor-Based (Recommended for Large Datasets):**
```
GET /api/v1/users?cursor=abc123&limit=20

Response:
{
  "data": [...],
  "pagination": {
    "nextCursor": "def456",
    "prevCursor": "xyz789",
    "hasMore": true
  }
}
```

**Offset-Based (Simple):**
```
GET /api/v1/users?page=1&limit=20

Response:
{
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100
  }
}
```

---

## Naming Conventions

### Resource Names: Plural Nouns

```
✅ Good:
/users
/projects
/orders
/user-profiles

❌ Bad:
/user (singular)
/getUsers (verb)
/userList (not RESTful)
```

### Fields: camelCase or snake_case (Be Consistent)

**camelCase (JavaScript, Java):**
```json
{
  "userId": "123",
  "firstName": "John",
  "createdAt": "2024-01-15T10:00:00Z"
}
```

**snake_case (Python, Ruby):**
```json
{
  "user_id": "123",
  "first_name": "John",
  "created_at": "2024-01-15T10:00:00Z"
}
```

**Rule:** Pick one, use everywhere

### Enums: UPPER_SNAKE_CASE

```yaml
status:
  type: string
  enum:
    - ACTIVE
    - INACTIVE
    - PENDING
```

### Boolean Fields: is/has Prefix

```yaml
isActive:
  type: boolean
hasAccess:
  type: boolean
canEdit:
  type: boolean
```

---

## OpenAPI Linting

### Spectral (Popular Linter)

**Install:**
```bash
npm install -g @stoplight/spectral-cli
```

**Run:**
```bash
spectral lint openapi.yaml
```

**Output:**
```
openapi.yaml
  10:5  warning  operation-description  Operation must have a description
  25:7  error    no-$ref-siblings       $ref cannot be placed next to other properties
  40:3  warning  operation-tags         Operation must have tags

✖ 3 problems (1 error, 2 warnings, 0 infos, 0 hints)
```

### Custom Rules (Organization-Specific)

**`.spectral.yaml`:**
```yaml
extends: spectral:oas

rules:
  # Require version in URL
  path-must-have-version:
    description: Paths must include version (e.g., /v1/)
    given: $.paths[*]~
    then:
      function: pattern
      functionOptions:
        match: "^/v[0-9]+/"
  
  # Require examples
  operation-examples:
    description: Operations must have examples
    given: $.paths[*][*].responses[*].content[*]
    then:
      field: examples
      function: truthy
  
  # Require pagination for list endpoints
  list-must-paginate:
    description: List endpoints must have pagination parameters
    given: $.paths[*].get
    then:
      field: parameters
      function: schema
      functionOptions:
        schema:
          type: array
          contains:
            properties:
              name:
                enum: [page, limit]
  
  # Consistent error format
  error-must-use-problem-json:
    description: Errors must use RFC 7807 Problem Details
    given: $.paths[*][*].responses[?(@property >= 400)]
    then:
      field: content.application/problem+json
      function: truthy
```

### CI/CD Integration

**GitHub Actions:**
```yaml
name: API Governance

on: [pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Install Spectral
        run: npm install -g @stoplight/spectral-cli
      
      - name: Lint OpenAPI spec
        run: spectral lint openapi.yaml --fail-severity warn
      
      - name: Check breaking changes
        run: |
          npm install -g oasdiff
          oasdiff breaking main:openapi.yaml HEAD:openapi.yaml
```

---

## Common Linting Rules

### All Operations Have Description

```yaml
rules:
  operation-description:
    description: Operations must have a description
    given: $.paths[*][*]
    then:
      field: description
      function: truthy
```

**Example:**
```yaml
paths:
  /users:
    get:
      description: List all users  # Required
      summary: List users
```

### All Parameters Have Description

```yaml
rules:
  parameter-description:
    description: Parameters must have a description
    given: $.paths[*][*].parameters[*]
    then:
      field: description
      function: truthy
```

### All Responses Have Schema

```yaml
rules:
  response-schema:
    description: Responses must have a schema
    given: $.paths[*][*].responses[*].content[*]
    then:
      field: schema
      function: truthy
```

### No Empty Descriptions

```yaml
rules:
  no-empty-description:
    description: Descriptions must not be empty
    given: $..description
    then:
      function: pattern
      functionOptions:
        notMatch: "^\\s*$"
```

### Consistent Naming Conventions

```yaml
rules:
  path-kebab-case:
    description: Paths must use kebab-case
    given: $.paths[*]~
    then:
      function: pattern
      functionOptions:
        match: "^(/[a-z0-9-]+)+$"
  
  property-camelCase:
    description: Properties must use camelCase
    given: $..properties[*]~
    then:
      function: casing
      functionOptions:
        type: camel
```

### Security Schemes Defined

```yaml
rules:
  security-defined:
    description: Security schemes must be defined
    given: $.components
    then:
      field: securitySchemes
      function: truthy
```

### Examples Provided

```yaml
rules:
  schema-examples:
    description: Schemas must have examples
    given: $.components.schemas[*]
    then:
      field: example
      function: truthy
```

---

## Breaking Change Detection

### openapiDiff Tool

**Install:**
```bash
npm install -g oasdiff
```

**Check Breaking Changes:**
```bash
oasdiff breaking old.yaml new.yaml
```

**Output:**
```
Breaking changes:
1. DELETE /api/v1/users/{id}/profile
   Endpoint removed

2. GET /api/v1/users
   Response field 'name' removed

3. POST /api/v1/users
   Request field 'email' is now required

Non-breaking changes:
1. GET /api/v1/users
   Response field 'avatar' added

2. GET /api/v1/projects
   New endpoint added
```

### Breaking Changes

**Examples:**
- Remove endpoint
- Remove field from response
- Add required field to request
- Change field type (string → integer)
- Rename field
- Change semantics (field means something different)
- Remove enum value
- Tighten validation (maxLength 100 → 50)

### Non-Breaking Changes

**Examples:**
- Add new endpoint
- Add optional field to request
- Add field to response
- Add enum value (at end)
- Relax validation (maxLength 50 → 100)
- Add new response code

### Semver for API Versions

**Versioning:**
```
v1.0.0 → v1.1.0  (non-breaking: add endpoint)
v1.1.0 → v1.1.1  (patch: bug fix)
v1.1.1 → v2.0.0  (breaking: remove field)
```

**URL Versioning:**
```
/v1/users  (major version in URL)
/v2/users  (breaking changes)
```

---

## API Documentation Generation

### Swagger UI (Interactive Docs)

**Setup:**
```javascript
const swaggerUi = require('swagger-ui-express');
const YAML = require('yamljs');
const swaggerDocument = YAML.load('./openapi.yaml');

app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerDocument));
```

**Features:**
- Interactive (try API in browser)
- Auto-generated from OpenAPI spec
- OAuth support
- Examples

**URL:** `https://api.example.com/api-docs`

### ReDoc (Beautiful Static Docs)

**Setup:**
```html
<!DOCTYPE html>
<html>
  <head>
    <title>API Documentation</title>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">
    <style>
      body { margin: 0; padding: 0; }
    </style>
  </head>
  <body>
    <redoc spec-url='openapi.yaml'></redoc>
    <script src="https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js"></script>
  </body>
</html>
```

**Features:**
- Beautiful design
- Three-panel layout
- Search
- Responsive

### Stoplight (Design-First Platform)

**Features:**
- Visual OpenAPI editor
- Mock servers
- Documentation hosting
- Collaboration

**Pricing:** $49-199/user/month

### Postman (Import OpenAPI)

**Import:**
```
Postman → Import → OpenAPI spec → Auto-generate collection
```

**Features:**
- Test API
- Generate code snippets
- Share with team

---

## Design-First vs Code-First

### Design-First (Write OpenAPI Spec, Generate Code)

**Process:**
```
1. Write OpenAPI spec (openapi.yaml)
2. Review with stakeholders
3. Generate server stubs (openapi-generator)
4. Implement business logic
5. Generate client SDKs
```

**Pros:**
- API design reviewed before implementation
- Spec is source of truth
- Auto-generate clients

**Cons:**
- Extra step (write spec)
- Need to keep spec in sync with code

**Tools:**
- openapi-generator (generate servers, clients)
- Stoplight Studio (visual editor)

### Code-First (Write Code, Generate OpenAPI Spec)

**Process:**
```
1. Write code with annotations
2. Generate OpenAPI spec from code
3. Publish docs
```

**Example (NestJS):**
```typescript
@Controller('users')
@ApiTags('users')
export class UsersController {
  @Get()
  @ApiOperation({ summary: 'List users' })
  @ApiResponse({ status: 200, type: [User] })
  async findAll(): Promise<User[]> {
    return this.usersService.findAll();
  }
}
```

**Pros:**
- No separate spec to maintain
- Spec always in sync with code

**Cons:**
- API design happens in code (less review)
- Harder to review API design

### Hybrid (Write Spec + Code, Keep in Sync)

**Process:**
```
1. Write OpenAPI spec (design)
2. Implement code
3. Validate code matches spec (automated)
```

**Tools:**
- Specmatic (contract testing)
- openapi-validator

**Recommendation:** Design-first for public APIs, code-first for internal

---

## OpenAPI Tooling

### Editor

**Swagger Editor:**
- Online: https://editor.swagger.io
- Features: Live preview, validation, export

**Stoplight Studio:**
- Desktop app
- Visual editor
- Mock servers
- Pricing: Free for open source, $49+/user/month

### Linter

**Spectral:**
```bash
npm install -g @stoplight/spectral-cli
spectral lint openapi.yaml
```

### Validator

**openapi-validator:**
```bash
npm install -g ibm-openapi-validator
lint-openapi openapi.yaml
```

### Generator

**openapi-generator:**
```bash
npm install -g @openapitools/openapi-generator-cli

# Generate server
openapi-generator-cli generate \
  -i openapi.yaml \
  -g nodejs-express-server \
  -o ./server

# Generate client
openapi-generator-cli generate \
  -i openapi.yaml \
  -g typescript-axios \
  -o ./client
```

**Supported Languages:**
- Servers: Node.js, Python, Java, Go, Ruby, PHP
- Clients: TypeScript, JavaScript, Python, Java, Go, Swift, Kotlin

### Diff

**oasdiff:**
```bash
npm install -g oasdiff
oasdiff breaking old.yaml new.yaml
```

**openapi-diff:**
```bash
npm install -g openapi-diff
openapi-diff old.yaml new.yaml
```

---

## Governance Workflow

### Step 1: Developer Writes/Updates OpenAPI Spec

**Process:**
```
1. Create feature branch
2. Update openapi.yaml
3. Add new endpoint or modify existing
4. Add examples
5. Commit and push
```

### Step 2: Automated Linting (CI)

**GitHub Actions:**
```yaml
- name: Lint OpenAPI
  run: spectral lint openapi.yaml --fail-severity warn
```

**Checks:**
- All operations have descriptions
- All parameters have descriptions
- Consistent naming
- Examples provided

### Step 3: Breaking Change Check (CI)

```yaml
- name: Check breaking changes
  run: |
    oasdiff breaking origin/main:openapi.yaml HEAD:openapi.yaml
    if [ $? -ne 0 ]; then
      echo "Breaking changes detected. Requires major version bump."
      exit 1
    fi
```

### Step 4: Review by API Guild

**API Guild:**
- Cross-team group of API experts
- Reviews API design
- Ensures consistency
- Approves changes

**Review Checklist:**
- [ ] Follows naming conventions
- [ ] RESTful design
- [ ] Proper error handling
- [ ] Examples provided
- [ ] No breaking changes (or justified)

### Step 5: Merge to Main

**After Approval:**
- Merge PR
- Spec is now source of truth

### Step 6: Auto-Publish Docs

**GitHub Actions:**
```yaml
- name: Publish docs
  run: |
    # Generate Swagger UI
    docker run -p 80:8080 -e SWAGGER_JSON=/openapi.yaml \
      -v $(pwd):/usr/share/nginx/html/openapi.yaml \
      swaggerapi/swagger-ui
    
    # Deploy to docs site
    aws s3 cp openapi.yaml s3://api-docs/
```

---

## API Versioning Strategy

### URL Versioning (/v1/, /v2/)

**Format:**
```
/api/v1/users
/api/v2/users
```

**Pros:**
- Clear and visible
- Easy to route
- Can run multiple versions simultaneously

**Cons:**
- URL changes
- Need to maintain multiple codebases

**When to Use:** Public APIs, major breaking changes

### Header Versioning (Accept-Version: v1)

**Format:**
```
GET /api/users
Accept-Version: v1
```

**Pros:**
- URL doesn't change
- More RESTful

**Cons:**
- Less visible
- Harder to test (need to set header)

**When to Use:** Internal APIs, minor versioning

### No Versioning (Only Non-Breaking Changes)

**Strategy:**
- Never make breaking changes
- Always backward compatible
- Deprecate old fields (but keep them)

**Pros:**
- Simple (no versioning needed)
- No migration needed

**Cons:**
- Technical debt accumulates
- Eventually need to clean up

**When to Use:** Internal APIs, early stage

### Deprecation Policy (6-12 Months Notice)

**Timeline:**
```
Month 0: Announce deprecation
Month 3: Warn users (headers, emails)
Month 6: Final warning
Month 12: Remove deprecated version
```

---

## Deprecation Headers

**Sunset Header (RFC 8594):**
```
HTTP/1.1 200 OK
Sunset: Sat, 31 Dec 2024 23:59:59 GMT
Link: <https://docs.example.com/migration>; rel="sunset"
```

**Deprecation Header:**
```
HTTP/1.1 200 OK
Deprecation: true
Link: <https://docs.example.com/migration>; rel="deprecation"
```

**Warning Header:**
```
HTTP/1.1 200 OK
Warning: 299 - "This endpoint is deprecated. Use /v2/users instead."
```

---

## Multi-Team API Governance

### Centralized API Registry

**Purpose:** Single source of truth for all APIs

**Contents:**
- All OpenAPI specs
- Ownership (which team owns which API)
- Status (active, deprecated, sunset)
- Dependencies (which APIs call which)

**Tools:**
- Backstage (Spotify's developer portal)
- Custom registry (database + UI)

### API Review Board

**Members:**
- API architects
- Representatives from each team
- Product managers

**Responsibilities:**
- Review API designs
- Approve breaking changes
- Maintain style guide
- Resolve conflicts

**Meeting:** Weekly or bi-weekly

### Style Guide Document

**Contents:**
- Naming conventions
- URL structure
- Error format
- Pagination format
- Authentication
- Examples

**Location:** Confluence, Notion, GitHub

### Shared Spectral Ruleset

**Repository:**
```
api-governance/
  .spectral.yaml  (shared rules)
  README.md       (how to use)
```

**Usage:**
```yaml
# team-a/.spectral.yaml
extends: ../api-governance/.spectral.yaml

rules:
  # Team-specific rules
  team-a-custom-rule:
    ...
```

---

## Monitoring API Compliance

### Spec Coverage (% of Endpoints Documented)

**Metric:**
```
Spec Coverage = Documented Endpoints / Total Endpoints

Target: 100%
```

**How to Measure:**
```
1. Scan code for API endpoints
2. Compare with OpenAPI spec
3. Report missing endpoints
```

### Linting Violations Over Time

**Dashboard:**
```
Jan: 50 violations
Feb: 40 violations
Mar: 30 violations
Apr: 20 violations

Trend: Improving ✅
```

### Breaking Changes Deployed

**Metric:**
```
Breaking Changes Deployed = Breaking Changes / Total Deployments

Target: 0% (no breaking changes without major version bump)
```

---

## Real-World Governance Examples

### Stripe API

**Characteristics:**
- Excellent consistency
- Comprehensive docs
- Versioning via headers
- Extensive examples

**Learn From:**
- Error format (detailed, helpful)
- Pagination (cursor-based)
- Idempotency keys
- Webhooks (event-driven)

### GitHub API

**Characteristics:**
- RESTful design
- GraphQL alternative
- Deprecation notices
- Rate limiting

**Learn From:**
- Deprecation headers
- Preview features (opt-in)
- Comprehensive SDKs

### Internal API Gateway Patterns

**Pattern:**
```
All APIs go through API gateway
→ Gateway enforces governance
→ Rate limiting, auth, logging
→ Consistent experience
```

---

## Implementation

### Spectral Ruleset (YAML)

See "Custom Rules" section above

### CI/CD Pipeline (GitHub Actions)

```yaml
name: API Governance

on:
  pull_request:
    paths:
      - 'openapi.yaml'

jobs:
  governance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
        with:
          fetch-depth: 0  # Fetch all history for diff
      
      - name: Setup Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '16'
      
      - name: Install tools
        run: |
          npm install -g @stoplight/spectral-cli
          npm install -g oasdiff
      
      - name: Lint OpenAPI spec
        run: spectral lint openapi.yaml --fail-severity warn
      
      - name: Check breaking changes
        run: |
          git show origin/main:openapi.yaml > old.yaml
          oasdiff breaking old.yaml openapi.yaml
          if [ $? -ne 0 ]; then
            echo "::error::Breaking changes detected. Requires major version bump."
            exit 1
          fi
      
      - name: Generate docs
        run: |
          npx redoc-cli bundle openapi.yaml -o docs.html
      
      - name: Upload docs
        uses: actions/upload-artifact@v2
        with:
          name: api-docs
          path: docs.html
```

### OpenAPI Spec Templates

**Minimal Template:**
```yaml
openapi: 3.0.3
info:
  title: My API
  version: 1.0.0
  description: API description
  contact:
    name: API Team
    email: api@example.com

servers:
  - url: https://api.example.com/v1

paths:
  /resource:
    get:
      summary: List resources
      operationId: listResources
      tags: [Resources]
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Resource'

components:
  schemas:
    Resource:
      type: object
      required: [id, name]
      properties:
        id:
          type: string
        name:
          type: string
  
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer

security:
  - bearerAuth: []
```

---

## Summary

### Quick Reference

**OpenAPI Governance:** Enforcing API design standards through automated validation

**Why:**
- Consistency across APIs
- Quality (catch issues early)
- Documentation (auto-generated)
- Breaking change prevention

**OpenAPI Structure:**
- info, servers, paths, components, security

**Design Standards:**
- RESTful conventions
- URL: `/api/v1/resources/{id}`
- Pagination: `?page=1&limit=20`
- Error format: RFC 7807 Problem Details
- Date format: ISO 8601

**Naming:**
- Resources: Plural nouns (`users`)
- Fields: camelCase or snake_case (consistent)
- Enums: UPPER_SNAKE_CASE
- Booleans: is/has prefix

**Linting:**
- Spectral (popular linter)
- Custom rules (organization-specific)
- CI/CD integration

**Breaking Changes:**
- Remove endpoint/field
- Change type
- Add required field
- Detect with oasdiff

**Documentation:**
- Swagger UI (interactive)
- ReDoc (beautiful)
- Auto-generated from spec

**Versioning:**
- URL: `/v1/`, `/v2/`
- Header: `Accept-Version: v1`
- Deprecation: 6-12 months notice

**Tools:**
- Editor: Swagger Editor, Stoplight Studio
- Linter: Spectral
- Generator: openapi-generator
- Diff: oasdiff

**Workflow:**
1. Write/update spec
2. Automated linting (CI)
3. Breaking change check (CI)
4. API guild review
5. Merge
6. Auto-publish docs

## Overview

OpenAPI Governance is the practice of enforcing API design standards across an organization through automated validation and lifecycle management.

### Key Components

1. **API Design Standards:** Consistent patterns (naming, structure, errors)
2. **Automated Validation:** Linting rules enforced in CI/CD
3. **Breaking Change Detection:** Prevent accidental breaking changes
4. **API Lifecycle Management:** Design → Deploy → Deprecate

### Example

Developer creates API endpoint:
POST /api/users (wrong - should be /api/v1/users)

Linter catches in CI:
❌ Error: Missing version prefix in URL
❌ Error: Missing operation description
❌ Error: No example provided

Developer fixes → CI passes → Merge allowed

---

## Best Practices

### API Design
- [ ] Follow RESTful conventions
- [ ] Use consistent naming patterns
- [ ] Document all endpoints
- [ ] Provide examples for all endpoints
- [ ] Use appropriate HTTP methods
- [ ] Implement proper error handling
- [ ] Use consistent error formats
- [ ] Use pagination for list endpoints
- [ ] Implement filtering and sorting
- [ ] Use appropriate status codes
- [ ] Document rate limits
- [ ] Use versioning in URLs
- [ ]

### Validation
- [ ] Implement automated linting in CI/CD
- [ ] Use Spectral for OpenAPI validation
- [ ] Define custom organization rules
- [ ] Check for breaking changes
- [ ] Validate all operations have descriptions
- [ ] Validate all parameters have descriptions
- [ ] Validate all responses have schemas
- [ ] Ensure examples are provided
- [ ] Check for security schemes
- [ ] Validate consistent naming conventions
- [ ]

### Documentation
- [ ] Use OpenAPI spec as source of truth
- [ ] Auto-generate documentation
- [ ] Use Swagger UI for interactive docs
- [ ] Use ReDoc for beautiful static docs
- [ ] Keep documentation in sync with code
- [ ]

### Breaking Changes
- [ ] Use semantic versioning
- [ ] Communicate breaking changes early
- [ ] Provide migration guides
- [ ] Hold breaking change meetings
- [ ] Create data contracts with consumers
- [ ] Document breaking changes clearly
- [ ] Use multi-step migrations
- [ ] Use zero-downtime migration pattern
- [ ]

### Governance
- [ ] Create API review board
- [ ] Establish API guild
- [ ] Define API lifecycle
- [ ] Maintain style guide
- [ ] Review API designs
- [ ] Approve breaking changes
- [ ] Resolve conflicts
- [ ] Maintain spec registry
- [ ]

### Tools
- [ ] Use Spectral for linting
- [ ] Use openapi-diff for detecting breaking changes
- [ ] Use graphql-inspector for GraphQL
- [ ] Use buf for Protobuf
- [ ] Use Swagger Editor for visual editing
- [ ] Use Stoplight Studio for design-first
- [ ] Use openapi-generator for code generation
- [ ]

### Versioning
- [ ] Use URL versioning (/v1/, /v2/)
- [ ] Use header versioning (Accept-Version: v1)
- [ ] Use semantic versioning (SemVer)
- [ ] Document version compatibility matrix
- [ ] Maintain backward compatibility
- [ ] Deprecate old versions properly
- [ ] Provide migration guides
- [ ]

### Monitoring
- [ ] Monitor spec coverage
- [ ] Track linting violations
- [ ] Monitor breaking changes deployed
- [ ] Set up dashboards for API health
- [ ] Track consumer adoption
- [ ]

### Checklist
- [ ] Define API design standards
- [ ] Implement automated linting
- [ ] Set up breaking change detection
- [ ] Create API review board
- [ ] Document all breaking changes
- [ ] Provide migration guides
- [ ] Use semantic versioning
- [ ] Maintain backward compatibility
- [ ] Set up deprecation process
- [ ] Monitor deprecated endpoint usage
- [ ] Test backward compatibility
- [ ] Use design-first approach
- [ ] Use consistent naming conventions
- [ ] Provide examples for all endpoints
- [ ] Document all API changes
- [ ] Train team on governance
