---
name: prd-v06-technical-specification
description: Define implementation contracts (APIs and data models) that developers will build against during PRD v0.6 Architecture. Triggers on requests to define APIs, design database schema, create data models, or when user asks "define APIs", "data model", "database schema", "API contracts", "technical spec", "endpoint design", "schema design". Consumes ARC- (architecture), TECH- (Build items), UJ- (flows), SCR- (screens). Outputs API- entries for endpoints and DBT- entries for data models. Feeds v0.7 Build Execution.
context: fork
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Technical Specification

Position in workflow: v0.6 Architecture Design → **v0.6 Technical Specification** → v0.7 Build Execution

Technical specification defines the **contracts** developers build against: API endpoints and data models. This is the bridge between architecture and implementation.

## Consumes

This skill requires prior work from v0.3-v0.6:

- **ARC-\* architecture decisions** (from v0.6 Architecture Design) — System structure (monolith vs microservices) determines API organization; integration patterns guide webhook/adapter design
- **TECH-\* Build items** (from v0.5 Technical Stack Selection) — Technologies chosen define data model types (PostgreSQL requires relational schema; MongoDB requires document schema)
- **UJ-\* user journeys** (from v0.4 User Journey Mapping) — Journey steps determine API call sequences; value moments determine response contracts
- **SCR-\* screen entries** (from v0.4 Screen Flow Definition) — Screen data requirements determine API response shape; form submissions map to POST/PUT/PATCH endpoints
- **BR-\* business rules** (from v0.3 Commercial Model) — Business constraints enforced in API responses (rate limits, validation rules, field constraints)

This skill assumes v0.6 Architecture Design is complete with ARC- entries providing system structure.

## Produces

This skill creates/updates:

- **API-\* entries** (API endpoint contracts) — REST/GraphQL endpoint specifications with request/response shapes, auth requirements, error codes, tied to UJ-/SCR- consumers and DBT- data sources
- **DBT-\* entries** (database schema contracts) — Data model specifications with fields, relationships, indexes, constraints, tied to API- accessors and BR- rules
- **Screen-to-API validation matrix** — Verification showing every SCR-* has supporting API-* and every UJ-* step can be completed via API calls
- **API-to-Data validation matrix** — Verification showing every API-* response field maps to DBT-* and every DBT-* is used by at least one API-*

All API- and DBT- entries are implementation contracts (not confidence-based). They are:
- **Derivable from** upstream IDs (UJ-/SCR-/ARC-/BR-/TECH-)
- **Testable** (API responses have concrete shape, DBT constraints are verifiable)
- **Complete enough for developers** to implement without re-research

Example API- entry (from UJ- and SCR-):
```markdown
API-001: Create Report
Method: POST
Path: /api/reports
Purpose: Create new report from selected data source and template (implements UJ-001 Step 1)
Auth: User

Journey: UJ-001 (Step 1 - Create Report)
Screen: SCR-002 (Report Builder)

Request:
  Body:
    {
      title: string (required) — Report name
      templateId: string (required) — Selected template (FEA-008)
      dataSourceId: string (required) — Connected data source (FEA-001)
      options: { dateRange: { start, end }, filters: [...] }
    }

Response:
  Success (201):
    {
      data: { id, title, status: "pending|generating|ready", createdAt }
    }
  Errors:
    - 400: Invalid input — Missing required field
    - 403: Forbidden — User doesn't own data source
    - 404: Not found — Template or data source not found
    - 429: Rate limit exceeded

Business Rules: BR-015 (max 100 reports per user)
Data: DBT-001 (reports table), DBT-002 (data_sources table)
```

Example DBT- entry (referenced by API- entries):
```markdown
DBT-001: Reports
Purpose: Stores user-generated reports (entities created by API-001, updated by API-004)
Table: reports

Fields:
  - id: uuid — Primary key
  - user_id: uuid — Report owner (FK → users) [NOT NULL]
  - title: varchar(255) — Display name [NOT NULL]
  - status: enum('pending','generating','ready','failed') [NOT NULL]
  - created_at: timestamp [NOT NULL, DEFAULT now()]

Relationships:
  - belongs_to: users via user_id
  - belongs_to: templates via template_id

Indexes:
  - user_id — List reports by user (API-003)
  - (user_id, created_at DESC) — Recent reports (API-003)
  - status — Find pending reports (background job)

Constraints:
  - title: NOT NULL, length 1-255
  - status: valid enum only

Business Rules: BR-015 (max 100 per user — enforce in API-001)
APIs: API-001 (create), API-002 (get), API-003 (list), API-005 (delete)
```

## Specification Types

| Type | What It Defines | Example |
|------|-----------------|---------|
| **API-** | Endpoint contracts | POST /users, GET /reports/:id |
| **DBT-** | Data model/schema | Users table, Reports table |

**Rule**: Every API- should know which DBT- it reads/writes. Every DBT- should know which API- accesses it.

## Specification Process

1. **Pull ARC- decisions** — System structure and boundaries
2. **Pull TECH- Build items** — What we're implementing
3. **Pull UJ- journeys** — User flows the API must support
4. **Pull SCR- screens** — UI data requirements

5. **Define API contracts** for each endpoint:
   - What's the request/response shape?
   - What auth is required?
   - What errors can occur?

6. **Define data models** for each entity:
   - What fields exist?
   - What relationships?
   - What constraints?

7. **Validate consistency**:
   - Does every screen have APIs to fetch its data?
   - Does every API response map to DBT- fields?

## API- Output Template

```
API-XXX: [Endpoint Name]
Method: [GET | POST | PUT | PATCH | DELETE]
Path: [/resource/{id}/action]
Purpose: [What this endpoint does]
Auth: [Public | User | Admin | Service]

Journey: [UJ-XXX that uses this]
Screen: [SCR-XXX that calls this]

Request:
  Headers:
    - Authorization: Bearer <token>
    - Content-Type: application/json
  Params:
    - id: string (required) — Resource identifier
  Query:
    - limit: number (optional, default 20) — Pagination limit
  Body:
    {
      field: type — Description
    }

Response:
  Success (200/201):
    {
      data: { ... }
    }
  Errors:
    - 400: Invalid input — [when this occurs]
    - 401: Unauthorized — [when this occurs]
    - 404: Not found — [when this occurs]
    - 500: Server error — [when this occurs]

Business Rules: [BR-XXX enforced here]
Data: [DBT-XXX entities accessed]
Rate Limit: [requests/minute if applicable]
```

**Example API- entry:**
```
API-001: Create Report
Method: POST
Path: /api/reports
Purpose: Create a new report from selected data source and template
Auth: User

Journey: UJ-001 (Step 1 - Create Report)
Screen: SCR-002 (Report Builder)

Request:
  Headers:
    - Authorization: Bearer <token>
    - Content-Type: application/json
  Body:
    {
      title: string (required) — Report name
      templateId: string (required) — Selected template
      dataSourceId: string (required) — Connected data source
      options: {
        dateRange: { start: ISO8601, end: ISO8601 }
        filters: [{ field: string, operator: string, value: any }]
      }
    }

Response:
  Success (201):
    {
      data: {
        id: string
        title: string
        status: "pending" | "generating" | "ready"
        createdAt: ISO8601
      }
    }
  Errors:
    - 400: Invalid input — Missing required field or invalid templateId
    - 401: Unauthorized — Invalid or expired token
    - 403: Forbidden — User doesn't own data source
    - 404: Not found — Template or data source not found
    - 429: Too many requests — Rate limit exceeded

Business Rules: BR-015 (max 100 reports per user)
Data: DBT-001 (reports), DBT-002 (data_sources)
Rate Limit: 10 requests/minute
```

## DBT- Output Template

```
DBT-XXX: [Entity Name]
Purpose: [What this entity represents]
Table: [database_table_name]

Fields:
  - id: uuid — Primary key, auto-generated
  - [field_name]: [type] — Description [constraints]
  - created_at: timestamp — Record creation (auto)
  - updated_at: timestamp — Last modification (auto)

Relationships:
  - belongs_to: [DBT-YYY] via [foreign_key]
  - has_many: [DBT-ZZZ]

Indexes:
  - [field_name] — [Query pattern it supports]

Constraints:
  - [field]: [UNIQUE | NOT NULL | CHECK expression]

Business Rules: [BR-XXX that affect this entity]
APIs: [API-XXX that read/write this]
```

**Example DBT- entry:**
```
DBT-001: Reports
Purpose: Stores user-generated reports with configuration and status
Table: reports

Fields:
  - id: uuid — Primary key
  - user_id: uuid — Report owner (FK → users) [NOT NULL]
  - title: varchar(255) — Display name [NOT NULL]
  - template_id: uuid — Template used (FK → templates) [NOT NULL]
  - data_source_id: uuid — Data source (FK → data_sources) [NOT NULL]
  - status: enum('pending','generating','ready','failed') — Generation status [NOT NULL, DEFAULT 'pending']
  - options: jsonb — Report configuration (date range, filters) [DEFAULT '{}']
  - output_url: varchar(500) — Generated report file URL [NULL until ready]
  - created_at: timestamp — [NOT NULL, DEFAULT now()]
  - updated_at: timestamp — [NOT NULL, DEFAULT now()]

Relationships:
  - belongs_to: DBT-010 (users) via user_id
  - belongs_to: DBT-002 (templates) via template_id
  - belongs_to: DBT-003 (data_sources) via data_source_id

Indexes:
  - user_id — List reports by user
  - (user_id, created_at DESC) — List recent reports
  - status — Find pending reports for processing

Constraints:
  - title: NOT NULL, length 1-255
  - status: NOT NULL, valid enum value

Business Rules: BR-015 (max 100 reports per user — enforce in API)
APIs: API-001 (create), API-002 (get), API-003 (list), API-005 (delete)
```

## API Design Principles

| Principle | Guidance | Example |
|-----------|----------|---------|
| **Resource-oriented** | URLs are nouns, not verbs | `/reports` not `/createReport` |
| **Consistent naming** | Plural nouns, kebab-case | `/data-sources` not `/dataSource` |
| **Stateless** | No server-side sessions | Auth via token, not cookie session |
| **Versioned** | Prefix for breaking changes | `/v1/reports` |
| **Documented errors** | Clear codes and messages | `{ error: { code: "LIMIT_EXCEEDED", message: "..." } }` |

## Data Model Principles

| Principle | Guidance | Example |
|-----------|----------|---------|
| **Normalized** | Avoid redundancy (unless denormalized for performance) | User name in users table, not duplicated |
| **Audit trail** | created_at, updated_at on all tables | Track when records change |
| **Soft delete** | deleted_at instead of hard delete (when needed) | Recover deleted data |
| **Foreign keys** | Enforce referential integrity | user_id → users.id |
| **Index strategy** | Index fields in WHERE and JOIN | Filter fields, FK columns |

## Validation Checklist

Use this to ensure spec completeness:

### Screen-to-API Validation
- [ ] Every SCR- screen has APIs to fetch its data
- [ ] Every form submission maps to a POST/PUT/PATCH
- [ ] Every list view has a paginated GET

### Journey-to-API Validation
- [ ] Every UJ- step that needs data has an API call
- [ ] API sequence supports journey flow
- [ ] Error states in journey have error responses

### API-to-Data Validation
- [ ] Every API- response field maps to DBT- fields
- [ ] Every API- that writes data has a target DBT-
- [ ] Business rules (BR-) enforced in API or DB constraint

### Orphan Check
- [ ] No API- without SCR-/UJ- consumer
- [ ] No DBT- table unused by any API-
- [ ] No dead code paths

## Anti-Patterns to Avoid

| Anti-Pattern | Signal | Fix |
|--------------|--------|-----|
| **API/UI mismatch** | Screen needs data not in any API | Add API- or modify existing |
| **Schema sprawl** | 50+ tables for MVP | Consolidate; YAGNI applies |
| **Missing constraints** | No validation, anything accepted | Add BR- enforcement |
| **N+1 queries baked in** | API design requires multiple calls for one view | Add compound endpoints |
| **No error handling** | Only happy path documented | Define all error responses |
| **Vague types** | `data: any` | Specify exact shape |

## Quality Gates

Before proceeding to Build Execution:

- [ ] All SCR- screens have supporting API- endpoints
- [ ] All UJ- journeys can be completed via API- calls
- [ ] All API- responses map to DBT- fields
- [ ] All BR- rules enforced in API- or DBT- constraints
- [ ] No orphaned tables or endpoints
- [ ] Error responses documented for all endpoints

## Downstream Connections

API- and DBT- entries feed into:

| Consumer | What It Uses | Example |
|----------|--------------|---------|
| **v0.7 Epic Scoping** | API- and DBT- define EPIC scope | EPIC-01 implements API-001–005 |
| **v0.7 Test Planning** | API- defines test contracts | TEST-001 validates API-001 |
| **v0.7 Implementation Loop** | API-/DBT- are implementation tasks | Code implements API-001 |
| **API Documentation** | API- becomes OpenAPI spec | Swagger from API- entries |

## Detailed References

- **API and data model examples**: See `references/examples.md`
- **API- entry template**: See `assets/api.md`
- **DBT- entry template**: See `assets/dbt.md`
