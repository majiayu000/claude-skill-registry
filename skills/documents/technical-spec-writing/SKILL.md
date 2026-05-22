---
name: technical-spec-writing
description: Creates technical design documents covering architecture, APIs, data models, and implementation approach. Bridges requirements to implementation. Use when designing system architecture, API contracts, or complex technical solutions.
version: 1.0.0
---

# Technical Spec Writing

## Purpose

Creates implementation-focused technical specifications that translate product requirements into concrete system designs, covering architecture, APIs, data models, and operational concerns.

## When NOT to Use This Skill

- Product requirements (use `prd-writing` instead)
- Feature specifications (use `feature-spec-writing` instead)
- Implementation task breakdown (use `sparc-planning` instead)
- API documentation for existing code (use `api-doc-writer` instead)
- Reviewing tech specs (use `technical-spec-reviewing` instead)

## Key Differences from Other Specs

| Aspect | PRD | Feature Spec | Technical Spec |
|--------|-----|--------------|----------------|
| Audience | Stakeholders | Engineers | Engineers |
| Focus | User value | User flows | System design |
| Content | User stories | Acceptance criteria | Architecture, APIs |
| Detail | High-level | Edge cases | Implementation |

## Workflow

### Step 1: Context Gathering

Invoke `check-history` to understand project context.

Reference source documents:
```markdown
Context to gather:
1. Parent PRD and relevant feature specs
2. Existing system architecture (what already exists)
3. Technical constraints (stack, patterns, limits)
4. Non-functional requirements (performance, scale, security)
5. Related systems and integration points
```

### Step 2: System Overview

Write a high-level description of the proposed solution:

```markdown
## System Overview

**Problem:** [What technical problem we're solving]

**Solution:** [High-level approach in 2-3 sentences]

**Key Design Decisions:**
1. [Decision 1]: [Why this approach]
2. [Decision 2]: [Why this approach]

**Scope:**
- In scope: [What this spec covers]
- Out of scope: [What's excluded, why]
```

### Step 3: Component Architecture

Define system components and their responsibilities:

```markdown
## Component Architecture

### Component Diagram
```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│   Client    │────▶│   API Layer  │────▶│   Service    │
└─────────────┘     └──────────────┘     └──────────────┘
                           │                    │
                           ▼                    ▼
                    ┌──────────────┐     ┌──────────────┐
                    │    Cache     │     │   Database   │
                    └──────────────┘     └──────────────┘
```

### Components

**[Component Name]**
- Responsibility: [What it does]
- Inputs: [What it receives]
- Outputs: [What it produces]
- Dependencies: [What it needs]
```

### Step 4: API Design

Define APIs with request/response schemas:

```markdown
## API Design

### Endpoints

#### [HTTP Method] [Path]

**Description:** [What this endpoint does]

**Authentication:** [Required/Optional, method]

**Request:**
```json
{
  "field": "type (description)",
  "nested": {
    "field": "type"
  }
}
```

**Response (200 OK):**
```json
{
  "data": {
    "id": "string",
    "field": "type"
  },
  "meta": {
    "timestamp": "ISO8601"
  }
}
```

**Error Responses:**
| Status | Code | Description |
|--------|------|-------------|
| 400 | INVALID_INPUT | [When this occurs] |
| 401 | UNAUTHORIZED | [When this occurs] |
| 404 | NOT_FOUND | [When this occurs] |
| 500 | INTERNAL_ERROR | [When this occurs] |
```

### Step 5: Data Model

Define data structures and persistence:

```markdown
## Data Model

### Entity: [Name]

**Table:** `table_name`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Primary identifier |
| field | VARCHAR(255) | NOT NULL | Description |
| status | ENUM | DEFAULT 'active' | Status enum |
| created_at | TIMESTAMP | NOT NULL | Creation time |

**Indexes:**
- `idx_field_status` on (field, status) - for [query type]

**Relationships:**
- Has many: [Related entities]
- Belongs to: [Parent entities]

### Entity Diagram
```
┌───────────────┐       ┌───────────────┐
│    Entity A   │───────│    Entity B   │
├───────────────┤   1:N ├───────────────┤
│ id (PK)       │       │ id (PK)       │
│ field         │       │ entity_a_id   │
└───────────────┘       └───────────────┘
```
```

### Step 6: Implementation Approach

Describe algorithms and key implementation details:

```markdown
## Implementation Approach

### Algorithm: [Name]

**Purpose:** [What it accomplishes]

**Pseudocode:**
```
function processRequest(input):
    1. Validate input
    2. Fetch dependencies from cache/db
    3. Apply business logic
    4. Persist changes
    5. Emit events
    6. Return response
```

**Key Considerations:**
- [Consideration 1 and how we handle it]
- [Consideration 2 and how we handle it]

### Design Patterns Used

| Pattern | Where Used | Why |
|---------|-----------|-----|
| Repository | Data access | Decouple from DB |
| Factory | Object creation | Complex instantiation |
| Observer | Events | Loose coupling |
```

### Step 7: Testing Strategy

Define testing approach:

```markdown
## Testing Strategy

### Unit Tests
- [Component]: [What to test]
- [Component]: [What to test]
- Coverage target: 90%+

### Integration Tests
- API endpoints: Happy path + error cases
- Database operations: CRUD + edge cases
- External services: Mock + contract tests

### E2E Tests
- [Critical flow 1]
- [Critical flow 2]

### Performance Tests
- Load test: [Scenario and expected results]
- Stress test: [Breaking point identification]
```

### Step 8: Performance Considerations

Define performance targets and optimization:

```markdown
## Performance Considerations

### Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| API Response Time | < 200ms p95 | APM |
| Database Query | < 50ms p95 | Query logging |
| Throughput | 1000 req/s | Load testing |

### Optimization Strategies

**Caching:**
- What: [Data to cache]
- Where: [Cache location]
- TTL: [Duration]
- Invalidation: [Strategy]

**Database:**
- Indexes: [Key indexes needed]
- Query optimization: [Specific optimizations]
- Connection pooling: [Pool size]

**Async Processing:**
- [What to make async and why]
```

### Step 9: Security Considerations

Address security concerns:

```markdown
## Security Considerations

### Authentication
- Method: [JWT, OAuth, etc.]
- Token handling: [How tokens are managed]

### Authorization
- Model: [RBAC, ABAC, etc.]
- Checks: [Where authorization is enforced]

### Data Protection
- At rest: [Encryption method]
- In transit: [TLS version]
- Sensitive fields: [Which fields, how protected]

### Input Validation
- [Input type]: [Validation rules]

### Security Checklist
- [ ] OWASP Top 10 addressed
- [ ] Input validation on all endpoints
- [ ] SQL injection prevention
- [ ] XSS prevention
- [ ] CSRF protection
- [ ] Rate limiting
- [ ] Audit logging
```

### Step 10: Migration & Rollback

Plan for deployment:

```markdown
## Migration & Rollback

### Migration Steps
1. [Step with validation]
2. [Step with validation]
3. [Step with validation]

### Database Migrations
```sql
-- Migration: [name]
ALTER TABLE ...
```

### Rollback Plan
1. [Rollback step]
2. [Rollback step]

### Feature Flags
| Flag | Purpose | Default |
|------|---------|---------|
| [name] | [control what] | Off |

### Rollout Plan
- Phase 1: Internal testing (0%)
- Phase 2: Beta users (5%)
- Phase 3: Gradual (25%, 50%, 100%)
```

### Step 11: Output Generation

Generate the technical spec using TEMPLATE.md. Verify:

- [ ] System overview is clear
- [ ] Component architecture defined
- [ ] APIs fully specified with schemas
- [ ] Data model complete
- [ ] Implementation approach clear
- [ ] Testing strategy comprehensive
- [ ] Performance targets defined
- [ ] Security considerations addressed
- [ ] Migration plan included

## Examples

### Example 1: E-Commerce - Shipping Rate API

**System Overview:**
```
Problem: Need real-time shipping rate calculation that integrates
with multiple carriers without impacting product page load time.

Solution: Create async shipping rate service with carrier abstraction
layer, caching, and fallback strategies.

Key Decisions:
1. Async API: Non-blocking for product page
2. Carrier abstraction: Swap carriers without code changes
3. Cache-first: Reduce API calls, improve latency
```

**Component Architecture:**
```
┌────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Product   │───▶│  Shipping Rate  │───▶│ Carrier Gateway │
│   Page     │    │     Service     │    │   (Abstraction) │
└────────────┘    └─────────────────┘    └─────────────────┘
                         │                       │
                         ▼                       ▼
                  ┌─────────────┐    ┌──────────────────────┐
                  │    Redis    │    │  UPS / FedEx / USPS  │
                  │   (Cache)   │    │      (External)      │
                  └─────────────┘    └──────────────────────┘
```

**API Design:**
```
POST /api/shipping/rates

Request:
{
  "destination_zip": "94102",
  "items": [{ "sku": "ABC123", "quantity": 2, "weight_oz": 8 }]
}

Response (200):
{
  "rates": [
    { "carrier": "UPS", "service": "Ground", "price": 5.99, "days": 5 },
    { "carrier": "FedEx", "service": "Express", "price": 12.99, "days": 2 }
  ],
  "cached": false,
  "calculated_at": "2024-01-15T10:30:00Z"
}
```

---

### Example 2: SaaS - Permission System

**System Overview:**
```
Problem: Need granular role-based access control that supports
custom roles, permission inheritance, and audit logging.

Solution: RBAC system with permission groups, role hierarchy,
and event-sourced audit trail.

Key Decisions:
1. Permission groups: Organize related permissions
2. Role hierarchy: Support inheritance
3. Event sourcing: Complete audit history
```

**Data Model:**
```
┌─────────────┐    ┌─────────────┐    ┌─────────────────┐
│    Role     │───▶│ Permission  │◀───│ PermissionGroup │
├─────────────┤ N:M├─────────────┤    ├─────────────────┤
│ id          │    │ id          │    │ id              │
│ name        │    │ name        │    │ name            │
│ org_id      │    │ resource    │    │ description     │
│ parent_id   │    │ action      │    └─────────────────┘
└─────────────┘    └─────────────┘

┌─────────────┐    ┌─────────────────┐
│    User     │───▶│ UserRoleAssign  │
└─────────────┘ 1:N└─────────────────┘
```

---

### Example 3: Fintech - Transaction Alert System

**System Overview:**
```
Problem: Deliver real-time transaction alerts to users within
seconds of transaction processing.

Solution: Event-driven architecture using message queue for
reliable delivery across push, SMS, and email channels.

Key Decisions:
1. Event-driven: Decouple from transaction processing
2. Multi-channel: Push, SMS, email with preferences
3. At-least-once: Ensure delivery with deduplication
```

**Component Architecture:**
```
┌───────────────┐    ┌─────────────────┐    ┌───────────────┐
│  Transaction  │───▶│   Message Queue │───▶│    Alert      │
│    Service    │    │    (Kafka)      │    │   Service     │
└───────────────┘    └─────────────────┘    └───────────────┘
                                                   │
                      ┌────────────────────────────┼────────────┐
                      ▼                            ▼            ▼
               ┌───────────┐              ┌───────────┐ ┌───────────┐
               │   Push    │              │    SMS    │ │   Email   │
               │  Service  │              │  Service  │ │  Service  │
               └───────────┘              └───────────┘ └───────────┘
```

**Performance Targets:**
| Metric | Target |
|--------|--------|
| Alert delivery latency | < 5 seconds from transaction |
| Throughput | 10,000 alerts/second |
| Availability | 99.99% |

## Anti-Patterns to Avoid

### Missing Rationale
```
❌ "Use Redis for caching"
✅ "Use Redis for caching (sub-ms latency needed, 100K reads/sec expected)"
```

### Vague Performance Targets
```
❌ "System should be fast"
✅ "API response < 200ms p95, database query < 50ms p95"
```

### No Error Handling
```
❌ Only happy path API responses
✅ Full error response catalog with codes and handling
```

### Implementation in Tech Spec
```
❌ Including actual code implementation
✅ Pseudocode and design patterns, leaving implementation to engineers
```

## Integration with Other Skills

**Receives From:**
- `prd-writing` - High-level requirements
- `feature-spec-writing` - Detailed feature requirements

**Works With:**
- `technical-spec-reviewing` - Review technical specs
- `api-doc-writer` - Document APIs after implementation

**Leads To:**
- `sparc-planning` - Implementation task breakdown

## Output Validation

Before finalizing:

- [ ] System overview explains the approach clearly
- [ ] All components have defined responsibilities
- [ ] APIs have complete request/response schemas
- [ ] Data model includes all entities and relationships
- [ ] Performance targets are specific and measurable
- [ ] Security considerations are addressed
- [ ] Migration and rollback plan included
- [ ] Open questions documented

## Resources

- See TEMPLATE.md for complete technical spec format
- See REFERENCE.md for architecture patterns and guidance


---

## Related Agent

For comprehensive specification guidance that coordinates this and other spec skills, use the **`specification-architect`** agent.
