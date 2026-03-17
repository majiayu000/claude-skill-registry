---
name: architecture-decision-record
description: ADR format and methodology for documenting significant technical decisions with context, alternatives considered, and consequences. Use when making or documenting architectural decisions.
---

# Architecture Decision Records

## ADR Template

Every ADR follows this structure:

```markdown
# ADR-NNN: Title of the Decision

## Status

[Proposed | Accepted | Deprecated | Superseded by ADR-NNN]

## Context

What is the issue that we are seeing that motivates this decision or change?
Describe the forces at play (technical, political, social, project-related).
Include any constraints, requirements, or assumptions.

## Decision

What is the change that we are proposing and/or doing?
State the decision in full sentences using active voice.
Be specific about what will be done.

## Consequences

What becomes easier or more difficult because of this decision?
List both positive and negative consequences.
Include any follow-up actions required.
```

## When to Write an ADR

Write an ADR for any decision that meets one or more of these criteria:

| Trigger                                    | Example                                         |
|--------------------------------------------|-------------------------------------------------|
| Adopting or replacing a technology         | Switching from REST to GraphQL                  |
| Changing an architectural pattern          | Moving from monolith to microservices           |
| Infrastructure decisions                   | Choosing a cloud provider or database           |
| API design choices                         | Choosing pagination strategy                    |
| Authentication/authorization strategy      | Adopting OAuth2 with PKCE                       |
| Data model decisions                       | Choosing between SQL and NoSQL                  |
| Cross-cutting concerns                     | Standardizing error handling or logging         |
| Process or convention changes              | Adopting conventional commits                   |
| Build/deployment decisions                 | Choosing CI/CD platform                         |
| Decisions that are hard to reverse         | Anything with significant migration cost        |

### Do NOT Write an ADR For

- Routine implementation choices with low impact
- Temporary decisions that will be revisited within days
- Individual code-level decisions that are covered by style guides
- Choices that are trivially reversible

## Status Lifecycle

```
Proposed  -->  Accepted  -->  Deprecated
                          -->  Superseded by ADR-NNN
```

| Status                  | Meaning                                                          |
|-------------------------|------------------------------------------------------------------|
| **Proposed**            | Under discussion, not yet decided                                |
| **Accepted**            | Decision has been agreed upon and should be followed             |
| **Deprecated**          | No longer relevant due to changes in the project or environment  |
| **Superseded by ADR-NNN** | Replaced by a newer decision; link to the replacement          |

### Rules

- An ADR is immutable once accepted; never edit the original text
- To change a decision, write a new ADR that supersedes the old one
- Update the old ADR's status to "Superseded by ADR-NNN"
- Keep deprecated and superseded ADRs in the repository for history

## Evaluating Alternatives

Use a structured comparison for every ADR with multiple options.

### Pros/Cons Matrix

```markdown
### Option A: PostgreSQL

**Pros:**
- Mature, well-understood RDBMS
- Strong ACID guarantees
- Excellent tooling ecosystem

**Cons:**
- Horizontal scaling requires additional tooling
- Schema migrations needed for changes

### Option B: MongoDB

**Pros:**
- Flexible schema for evolving data models
- Built-in horizontal scaling (sharding)

**Cons:**
- Weaker transaction support (multi-document)
- Team has limited operational experience
```

### Weighted Criteria Matrix

For complex decisions, score each option against weighted criteria:

```markdown
| Criteria              | Weight | PostgreSQL | MongoDB | DynamoDB |
|-----------------------|--------|------------|---------|----------|
| Team expertise        | 5      | 5          | 2       | 2        |
| Scalability           | 4      | 3          | 4       | 5        |
| Query flexibility     | 4      | 5          | 3       | 2        |
| Operational cost      | 3      | 3          | 3       | 4        |
| ACID compliance       | 3      | 5          | 3       | 3        |
| **Weighted Total**    |        | **80**     | **57**  | **60**   |
```

Calculation: sum of (weight x score) for each option.

## File Naming and Storage

### Conventions

| Convention       | Rule                                           | Example                              |
|------------------|-------------------------------------------------|--------------------------------------|
| Numbering        | Zero-padded 4-digit sequential                  | `0001`, `0002`, `0015`              |
| File name        | `NNNN-title-slug.md`                            | `0003-use-postgresql.md`            |
| Storage location | `docs/adr/` at the repository root              | `docs/adr/0003-use-postgresql.md`   |
| Title format     | ADR-NNN: Imperative sentence                    | ADR-003: Use PostgreSQL for storage  |

### Directory Structure

```
project-root/
  docs/
    adr/
      0001-record-architecture-decisions.md
      0002-use-typescript-for-backend.md
      0003-use-postgresql-for-primary-storage.md
      0004-adopt-rest-api-style.md
      0005-use-jwt-for-authentication.md
      README.md   (optional index)
```

### Linking ADRs to Code and Issues

- Reference the ADR in code comments near the affected area:
  ```typescript
  // See ADR-003: Use PostgreSQL for primary storage
  // docs/adr/0003-use-postgresql.md
  const db = new Pool({ connectionString: DATABASE_URL });
  ```
- Link to the relevant issue or PR in the ADR footer:
  ```markdown
  ## References
  - GitHub Issue: #142
  - Pull Request: #158
  - Related: ADR-002
  ```

## Example ADR 1: Choosing a Primary Database

```markdown
# ADR-003: Use PostgreSQL for Primary Storage

## Status

Accepted

## Context

Our application needs a primary data store for user accounts, orders,
and product inventory. We expect the following requirements:

- Strong consistency for financial transactions
- Complex queries across related entities (joins)
- Team has 5 years of collective PostgreSQL experience
- Expected scale: 10M rows in the largest table within 2 years
- Read-heavy workload with occasional write bursts

We evaluated three options: PostgreSQL, MongoDB, and DynamoDB.

## Decision

We will use PostgreSQL 16 as our primary database.

We will manage schema changes with a migration tool (golang-migrate)
and enforce that all schema changes go through reviewed migration files.

We will use connection pooling via PgBouncer for production deployments.

## Consequences

**Positive:**
- Team can be productive immediately with existing expertise
- ACID transactions simplify order and payment logic
- Rich query capabilities reduce application-level data manipulation
- Large ecosystem of monitoring and backup tools

**Negative:**
- Horizontal write scaling will require sharding or read replicas
  if we exceed expected growth significantly
- Schema migrations add friction to data model changes
- We need to manage connection pooling and tuning ourselves

**Follow-up actions:**
- Set up PgBouncer in the infrastructure configuration
- Create a migration workflow and document in the developer guide
- Establish backup and point-in-time recovery procedures
```

## Example ADR 2: API Style

```markdown
# ADR-004: Adopt REST for Public API

## Status

Accepted

## Context

We are building a public API for third-party integrations. The API
will be consumed by partners with varying levels of technical
sophistication. We need to choose between REST, GraphQL, and gRPC.

Key factors:
- Partners expect a well-documented, stable API
- Most consumers are web applications and mobile clients
- We want to minimize onboarding friction for partners
- Internal services also need to communicate, but that is a
  separate concern (see future ADR for internal RPC)

## Decision

We will adopt RESTful API design for our public-facing API.

Conventions:
- JSON request and response bodies
- Plural resource nouns in URL paths (e.g., /api/v1/orders)
- Cursor-based pagination for list endpoints
- Versioning via URL path prefix (/api/v1/, /api/v2/)
- Standard HTTP status codes per our api-design skill

We will use OpenAPI 3.1 for specification and generate
documentation from it.

## Consequences

**Positive:**
- Low learning curve for partners (REST is widely understood)
- OpenAPI tooling enables auto-generated SDKs
- Cacheable via HTTP standards (ETags, Cache-Control)
- Easy to test with curl, Postman, or any HTTP client

**Negative:**
- Over-fetching and under-fetching compared to GraphQL
- Multiple roundtrips for complex data needs
- Versioning requires maintaining parallel implementations

**Follow-up actions:**
- Create the OpenAPI specification file
- Set up API documentation generation pipeline
- Define the error response format (see api-design skill)
```

## Example ADR 3: Authentication Strategy

```markdown
# ADR-005: Use JWT with Short-Lived Access Tokens for Authentication

## Status

Accepted

## Context

We need to authenticate users and authorize API requests. The
application has both a web frontend and mobile clients. Requirements:

- Stateless authentication to simplify horizontal scaling
- Support for token refresh without full re-authentication
- Revocation capability for compromised tokens
- Compatibility with OAuth2 for future third-party integrations

Options evaluated:
1. Session-based authentication with server-side storage
2. JWT with long-lived tokens
3. JWT with short-lived access tokens and refresh tokens

## Decision

We will use JWT-based authentication with:

- **Access tokens:** 15-minute expiry, signed with RS256
- **Refresh tokens:** 7-day expiry, stored in the database, rotated
  on each use (refresh token rotation)
- **Token storage:** Access token in memory (frontend), refresh token
  in httpOnly secure cookie
- **Revocation:** Refresh tokens can be revoked by deleting from the
  database; access tokens are short-lived enough to not require
  explicit revocation in most cases
- **Key rotation:** RSA key pairs rotated quarterly with JWKS endpoint

## Consequences

**Positive:**
- Stateless verification of access tokens (no database lookup per request)
- Refresh token rotation limits the window for stolen tokens
- RS256 allows verification without sharing the signing key
- JWKS endpoint enables key rotation without downtime

**Negative:**
- Cannot instantly revoke access tokens (15-minute window)
  - Mitigation: for critical actions (password change, detected breach),
    maintain a short-lived deny list checked by middleware
- Refresh token storage adds database dependency
- Token handling complexity on the client side
- Key rotation process needs careful implementation

**Follow-up actions:**
- Implement the JWKS endpoint
- Create middleware for token verification
- Document the token refresh flow for frontend and mobile teams
- Set up monitoring for failed authentication attempts
```

## ADR Review Checklist

Before accepting an ADR, verify:

- [ ] Context explains the problem clearly enough that someone new can understand it
- [ ] All viable alternatives are listed and evaluated
- [ ] The decision is stated explicitly and unambiguously
- [ ] Both positive and negative consequences are acknowledged
- [ ] Follow-up actions are identified
- [ ] The ADR is linked to relevant issues or PRs
- [ ] The file follows naming conventions (NNNN-title-slug.md)
- [ ] Status is set to "Proposed" for review, "Accepted" after approval
- [ ] At least two team members have reviewed the ADR
