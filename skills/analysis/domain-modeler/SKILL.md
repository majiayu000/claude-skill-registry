---
name: domain-modeler
description: "Extract domain model from user journeys/requirements. Reads user stories or journey docs, identifies business entities, relationships, attributes, and constraints, then produces structured data model documentation. Use when starting a new project, onboarding a new domain, or when user-journeys change significantly. Triggers: 'domain modeling', 'extract entities', 'data model from requirements', 'business abstraction', 'design data model', or when user-journeys.md is created/modified."
---

# Domain Modeler

Structured workflow for extracting a technology-agnostic domain model from user journeys and requirements documentation. Produces data model docs that serve as the single source of truth for both database schema and API design.

> **Design Philosophy:** Domain-model-first. The domain model is derived from business requirements and is technology-agnostic. Both the database schema (SQLAlchemy models) and API contract (OpenAPI spec) are downstream consumers of this model — neither is the "source of truth."

## When to Use

- **New project:** After writing user journeys, before any technical design
- **Major requirements change:** When user journeys are significantly modified
- **New bounded context:** When a new business domain is added to an existing project

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| User journeys / stories | **Yes** | The primary requirements doc (e.g., `docs/user-journeys.md`) |
| Existing specs | Optional | Any constraints, business rules, or technical requirements already documented |
| Domain expert feedback | Optional | Clarifications from stakeholders on ambiguous business logic |

## Outputs

| Output | Purpose | Downstream Consumer |
|--------|---------|-------------------|
| `docs/data-types.md` | Entity definitions (fields, types, constraints) | schema-to-openapi, api-builder |
| `docs/relationships.md` | Relationship definitions between entities | schema-to-openapi, api-builder |
| `docs/crud-operations.md` | CRUD operations and permission matrix | schema-to-openapi, api-builder |
| `specs/data-integrity.md` | Uniqueness, soft delete, cascade rules | api-builder (model generation) |
| `specs/cache-strategy.md` | Cached/computed field maintenance | api-builder (model generation) |
| `docs/rule-engine.md` | Business rule engine spec (if applicable) | schema-to-openapi |

## Workflow

### Step 1: Extract Business Entities

Read the user journey document end-to-end. For each journey, extract **nouns** that represent business objects.

**Technique:** Noun extraction with deduplication

```
User Journey: "参赛者在活动详情页点击报名，填写团队信息，提交参赛提案"

Extracted nouns:
  参赛者 → User (entity)
  活动   → Event (entity)
  团队   → Group (entity)
  提案   → Post (entity, type=proposal)
```

**Checklist:**
- [ ] Every journey has been scanned
- [ ] Synonyms have been merged (e.g., "参赛者" and "用户" → User)
- [ ] Each entity has a clear, single-word English name
- [ ] Aim for the **minimum number of entities** that cover all journeys

**Output:** Entity list with Chinese-English name mapping

### Step 2: Identify Relationships

For each pair of entities, determine if and how they relate based on the user journeys.

**Technique:** Verb extraction between entities

```
"用户 创建 帖子"    → User -[creates]-> Post (1:N, via created_by)
"帖子 关联到 活动"  → Event -[has]-> Post (M:N, via event_post)
"用户 加入 团队"    → Group -[has]-> User (M:N, via group_user)
```

**Relationship classification:**
| Type | Pattern | Example |
|------|---------|---------|
| Ownership (1:N) | "A creates B" | User creates Post |
| Association (M:N) | "A belongs to B" / "A joins B" | Post submitted to Event |
| Self-referential | "A relates to A" | Event stages/tracks |
| Polymorphic | "A targets any of B/C/D" | Interaction on Post/Event/Resource |

**Checklist:**
- [ ] Every entity pair has been considered
- [ ] Relationship cardinality is defined (1:1, 1:N, M:N)
- [ ] Junction table fields are identified for M:N relationships
- [ ] Self-referential and polymorphic patterns are explicitly noted

### Step 3: Define Attributes

For each entity, define its fields based on what the user journeys require.

**Principles:**
- **YAGNI:** Only add fields that are needed by at least one user journey
- **snake_case:** All field names use snake_case
- **created_by:** All content types use `created_by` for the author/creator
- **Soft delete:** All content types include `deleted_at` for soft delete

**Field definition template:**

```markdown
### Entity Name

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| id | string | auto | uuid | Primary key |
| name | string | yes | - | Display name |
| status | enum | yes | draft | draft/published/closed |
| created_by | string(FK→user) | yes | - | Creator |
| created_at | datetime | auto | now() | Creation timestamp |
| updated_at | datetime | auto | now() | Last modification |
| deleted_at | datetime | no | null | Soft delete marker |
```

**Checklist:**
- [ ] Every field is traceable to a user journey or business rule
- [ ] Field types are technology-agnostic (string, int, datetime, enum — not VARCHAR(255))
- [ ] Enum values are explicitly listed
- [ ] Foreign keys are marked with FK→target_entity
- [ ] Default values are defined where applicable

### Step 4: Define Constraints and Business Rules

Extract constraints that go beyond simple field types.

**Events of constraints:**

| Event | Examples | Output File |
|----------|----------|-------------|
| Uniqueness | username must be unique | `specs/data-integrity.md` |
| Soft delete | All types use deleted_at, queries exclude deleted | `specs/data-integrity.md` |
| Cascade rules | Deleting a user soft-deletes their posts | `specs/data-integrity.md` |
| Cached fields | post.like_count auto-maintained | `specs/cache-strategy.md` |
| Business rules | Only organizers can create events | `docs/crud-operations.md` |
| Complex rules | Rule engine with declarative checks | `docs/rule-engine.md` |

**Checklist:**
- [ ] Every "must", "cannot", "only...can" in user journeys is captured
- [ ] Cascade delete behavior is defined for every relationship
- [ ] Cached/computed fields are identified and maintenance triggers defined
- [ ] Permission matrix covers all roles × all operations

### Step 5: Define CRUD Operations

For each entity, define the full CRUD matrix with permissions.

**Template:**

```markdown
| Operation | Endpoint | Allowed Roles | Notes |
|-----------|----------|---------------|-------|
| Create | POST /api/entities | participant, organizer | - |
| List | GET /api/entities | all (public only) | Respects visibility |
| Get | GET /api/entities/{id} | all (if visible) | - |
| Update | PATCH /api/entities/{id} | owner, admin | Only own content |
| Delete | DELETE /api/entities/{id} | owner, admin | Soft delete |
```

**Checklist:**
- [ ] Every entity has all 5 CRUD operations defined
- [ ] Every relationship has create/delete operations defined
- [ ] Permission matrix covers all 3+ roles
- [ ] Special operations (status transitions, bulk ops) are documented
- [ ] **Symmetry check:** CREATE/DELETE operations have corresponding LIST operations (see below)

#### Symmetry Check

For every CREATE/DELETE operation pair, verify a corresponding LIST operation exists:

```
Rule: If user can CREATE item X and DELETE item X,
      then user should be able to LIST their own X items.

Example - Missing symmetry detected:
  ✓ CREATE interaction (type: like)  → 点赞
  ✓ DELETE interaction (type: like)  → 取消点赞
  ✗ READ interaction (type: like, created_by: current_user)  → 查看点赞列表 ← MISSING!

Fix: Add "查看点赞列表" to user journeys if the asymmetry is detected.
```

**Symmetry check matrix template:**

| Operation Pair | LIST Operation | Status |
|---------------|----------------|--------|
| like/unlike post | List my liked posts | ✓/✗ |
| follow/unfollow user | List my following | ✓/✗ |
| join/leave group | List my groups | ✓/✗ |
| create/delete post | List my posts | ✓/✗ |

### Step 6: Review and Validate

**Cross-check against user journeys:**

```
For each user journey in docs/user-journeys.md:
  1. Trace the journey step by step
  2. For each step, verify:
     - The required entity exists in data-types.md
     - The required relationship exists in relationships.md
     - The required operation exists in crud-operations.md
     - The required permission is granted in the permission matrix
  3. If any step cannot be fulfilled → identify gap and iterate
```

**Checklist:**
- [ ] Every user journey can be fully executed with the defined model
- [ ] No orphan entities (entities not referenced by any journey)
- [ ] No missing operations (journey steps that require undefined CRUD ops)
- [ ] Constraints don't block any valid journey path

## Adapting for Different Projects

This skill is project-agnostic. When using in a new project:

1. **Replace file paths** — The output files can be placed anywhere, but the naming convention (`data-types.md`, `relationships.md`, etc.) is recommended for consistency
2. **Adjust roles** — Replace "participant/organizer/admin" with your project's role definitions
3. **Skip optional outputs** — `rule-engine.md` and `cache-strategy.md` are only needed if your domain has those concerns
4. **Scale the process** — For simple CRUD apps, Steps 1-3 may be sufficient; for complex domains, all 6 steps are recommended

## Anti-Patterns

| Anti-Pattern | Why It's Wrong | What to Do Instead |
|-------------|----------------|-------------------|
| Copying field names from a database schema | Ties the model to a specific database | Define fields from business requirements |
| Adding fields "just in case" | YAGNI — unused fields create maintenance burden | Only add fields required by user journeys |
| Skipping relationship definition | Leads to ad-hoc joins and data integrity issues | Explicitly define every relationship |
| Defining API endpoints before entities | Puts the cart before the horse | Entities first, then operations, then endpoints |
| One giant entity for everything | God object anti-pattern | Split by business boundary, aim for minimal entities |
