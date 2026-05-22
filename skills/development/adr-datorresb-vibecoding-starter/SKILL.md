---
name: adr
description: Architecture Decision Records (ADR) for documenting significant architectural decisions with context, rationale, and consequences. Use when making technology choices, defining system boundaries, establishing patterns, after architecture reviews, or documenting trade-offs.
---

# Architecture Decision Records (ADR)

## Core Principle

**Document decisions, not just implementations. Capture the "why" when it's fresh.**

The most valuable documentation isn't what you built—it's why you built it that way. Architecture Decision Records capture the context, options considered, and trade-offs at decision time. Six months later, when someone asks "why did we choose this?", the ADR provides the answer.

**Good ADRs are:**
- Written when decisions are made (not after)
- Context-rich (capture constraints and alternatives)
- Consequence-aware (document trade-offs honestly)
- Living documents (can be superseded or deprecated)

---

## When to Use

Use ADRs when:
- Making significant architectural decisions
- Choosing technologies, frameworks, or libraries
- Defining system boundaries and service decomposition
- Establishing architectural patterns or standards
- Making security or compliance decisions
- After architecture review sessions
- Documenting performance trade-offs
- Introducing breaking changes
- Selecting deployment or infrastructure strategies
- Deciding on data storage or communication patterns

**Don't write ADRs for:**
- Routine implementation details
- Minor refactorings
- Bug fixes (unless they change architecture)
- Configuration changes
- Obvious or universally accepted choices

---

## ADR Formats

### 1. MADR (Markdown Architecture Decision Record)

**Most popular format. Lightweight and flexible.**

```markdown
# [Short title of solved problem and solution]

## Status

[proposed | accepted | rejected | deprecated | superseded by ADR-XXXX]

## Context

What is the issue we're seeing that is motivating this decision or change?

Include:
- Current situation
- Problem statement
- Relevant constraints (time, cost, skills, technology)
- Stakeholder concerns
- Dependencies and assumptions

## Decision

What is the change that we're actually proposing or have agreed to implement?

Be specific and actionable:
- What we will do
- What technologies/patterns we'll use
- How it fits into existing architecture
- Any implementation guidelines

## Consequences

What becomes easier or more difficult to do and any risks introduced by the change?

### Positive Consequences
- Benefits gained
- Problems solved
- Capabilities enabled

### Negative Consequences
- Trade-offs accepted
- Limitations introduced
- Technical debt incurred

### Risks
- Potential issues to monitor
- Mitigation strategies
```

**Example:**

```markdown
# Use PostgreSQL as Primary Database

## Status

Accepted

## Context

Our application needs a persistent data store for user data, content, and analytics.
We're a startup with 3 engineers, expecting 10K users in year one, with potential
for rapid growth if product-market fit is achieved.

Requirements:
- ACID transactions for financial data
- Complex queries across multiple entities
- Full-text search capability
- JSON data support for flexible schemas
- Team has SQL experience but not NoSQL
- Budget constraints ($500/month infrastructure)

Current state: Using SQLite for prototyping, but needs production-grade database.

## Decision

We will use PostgreSQL 15+ as our primary database for all application data.

Implementation details:
- Hosted on managed service (AWS RDS or similar)
- Single primary instance initially, with read replicas as traffic grows
- Use JSONB columns for flexible data alongside relational tables
- pg_trgm extension for full-text search
- Connection pooling via PgBouncer

Migration path: Export SQLite data to PostgreSQL using standard migration tools.

## Consequences

### Positive Consequences

- **ACID guarantees**: Financial data integrity assured
- **Rich query capabilities**: Complex joins, aggregations, window functions
- **JSONB support**: Flexible schema where needed, without giving up relational model
- **Team expertise**: Team already knows SQL, minimal learning curve
- **Mature ecosystem**: Extensive tooling, libraries, and community support
- **Cost-effective**: Can start small (~$50/month) and scale to large workloads
- **Full-text search**: Built-in via pg_trgm, no additional service needed initially
- **Battle-tested**: Used by millions of applications, proven at scale

### Negative Consequences

- **Scaling complexity**: Eventually need sharding or read replicas for massive scale
- **Operational overhead**: Requires maintenance windows, backups, monitoring
- **Vertical scaling limits**: Single instance has compute/memory ceiling
- **Not optimal for**: Time-series data, graph queries, or document-heavy workloads

### Risks

- **Vendor lock-in**: Using PostgreSQL-specific features (JSONB, extensions) makes migration harder
  - Mitigation: Abstract data access behind repository pattern
- **Performance at scale**: May need read replicas or caching layer as we grow
  - Mitigation: Plan monitoring and be ready to add Redis/read replicas
- **Backup/recovery**: Data loss if backups not configured properly
  - Mitigation: Use managed service with automated backups, test restore process

### Alternatives Considered

**MongoDB**
- Pro: Flexible schema, horizontal scaling
- Con: Team has no experience, eventual consistency complexity
- Why rejected: ACID guarantees more important than schema flexibility

**MySQL**
- Pro: Similar to PostgreSQL, large ecosystem
- Con: Weaker JSON support, less feature-rich
- Why rejected: PostgreSQL offers more advanced features for similar cost

**Firestore/DynamoDB**
- Pro: Fully managed, infinite scale
- Con: Limited query capabilities, higher cost at scale, vendor lock-in
- Why rejected: Query flexibility essential for our use cases
```

---

### 2. Nygard Format (Original ADR Format)

**Created by Michael Nygard. More structured.**

```markdown
# [Number]. [Title]

Date: [YYYY-MM-DD]

## Status

[proposed | accepted | deprecated | superseded]

## Context

[Describe the forces at play, including technological, political, social,
and project local. These forces are probably in tension, and should be
called out as such.]

## Decision

[State the decision and full justification.]

## Consequences

[Describe the resulting context, after applying the decision. All consequences
should be listed here, not just the "positive" ones. A particular decision may
have positive, negative, and neutral consequences, but all affect the team
and project in the future.]
```

**Example:**

```markdown
# 5. Adopt Microservices Architecture for Backend

Date: 2024-01-15

## Status

Accepted

## Context

Our monolithic Python application has grown to 150K lines of code over 3 years.
Development velocity has decreased as features become harder to add without
breaking existing functionality. We have 15 engineers and expect to grow to 40
within a year.

Current pain points:
- 45-minute build times for full test suite
- Deployment requires full system downtime (30-60 minutes)
- Teams blocked waiting for others to merge code
- One service outage takes down entire application
- Different components have different scaling needs (API vs background jobs)

Technological context:
- Deployed as single Docker container
- PostgreSQL database with 200+ tables
- Redis for caching and job queue
- React frontend (separate deployment)
- AWS infrastructure

Organizational context:
- Moving to team-based ownership model
- Each team owns specific domain (users, payments, content, etc.)
- Want to enable teams to deploy independently
- Different teams have different preferred technologies

## Decision

We will decompose the monolith into microservices architecture with the
following approach:

1. **Service Boundaries**: Decompose along business domain boundaries using
   Domain-Driven Design principles (user service, payment service, content
   service, notification service)

2. **Technology Stack**:
   - Services can choose their own tech stack (Python, Node.js, Go)
   - Each service owns its own database (no shared database)
   - REST APIs for synchronous communication
   - Event bus (Apache Kafka) for asynchronous communication
   - API Gateway (Kong) for routing and authentication

3. **Migration Strategy**:
   - Strangler fig pattern: incrementally extract services
   - Start with bounded contexts that are least coupled
   - Phase 1: Extract notification service (3 weeks)
   - Phase 2: Extract payment service (6 weeks)
   - Phase 3+: Continue with other services over 12 months

4. **Data Decomposition**:
   - Each service gets dedicated database instance
   - Data synchronization via event streaming
   - Accept eventual consistency where appropriate

5. **Deployment**:
   - Kubernetes for orchestration
   - Each service has independent CI/CD pipeline
   - Blue-green deployments per service

## Consequences

**Positive:**

- **Independent deployment**: Teams can deploy without coordinating
- **Technology flexibility**: Teams can choose best tool for their domain
- **Scaling efficiency**: Scale individual services based on load
- **Fault isolation**: One service failure doesn't crash entire system
- **Development velocity**: Smaller codebases easier to understand and modify
- **Team autonomy**: Clear ownership boundaries reduce coordination overhead
- **Build times**: Each service builds in 5-10 minutes instead of 45

**Negative:**

- **Operational complexity**: Now managing 8+ services instead of 1
- **Data consistency**: Eventual consistency requires careful design
- **Distributed debugging**: Tracing requests across services more complex
- **Network overhead**: Inter-service communication adds latency
- **Development environment**: Running all services locally is challenging
- **Transaction management**: Distributed transactions require saga pattern
- **Migration effort**: 12+ months of engineering time to fully decompose

**Neutral:**

- **Testing complexity**: Unit tests simpler, integration tests more complex
- **Monitoring requirements**: Need distributed tracing (Jaeger/OpenTelemetry)
- **Learning curve**: Team needs to learn distributed systems patterns

**Risks and Mitigation:**

- **Risk**: Service boundaries wrong, require major refactoring
  - **Mitigation**: Start with obvious bounded contexts, iterate based on learnings

- **Risk**: Data duplication and synchronization issues
  - **Mitigation**: Event sourcing for critical data, accept eventual consistency

- **Risk**: Network failures cause cascading failures
  - **Mitigation**: Implement circuit breakers, retries, timeouts (Resilience4j)

- **Risk**: Increased infrastructure costs
  - **Mitigation**: Share Kubernetes clusters, optimize resource allocation

- **Risk**: Loss of ACID guarantees across domains
  - **Mitigation**: Use saga pattern for distributed transactions, compensating actions
```

---

### 3. Y-Statement Format

**Most concise format. Good for simple decisions.**

```markdown
# [Title]

In the context of [use case/user story],
facing [concern],
we decided for [option]
to achieve [quality],
accepting [downside].
```

**Example:**

```markdown
# Use JWT for Authentication

In the context of **building a stateless REST API that can scale horizontally**,
facing **the need to authenticate users across multiple backend instances without session storage**,
we decided for **JWT (JSON Web Tokens) with RS256 signing**
to achieve **stateless authentication that works across service boundaries**,
accepting **inability to immediately revoke tokens and need for short expiration times**.

## Alternatives Considered

**Session-based authentication**: Rejected due to session storage requirements
**OAuth 2.0**: Overkill for first-party API, JWT is simpler
**API Keys**: Not suitable for user authentication, no expiration

## Implementation Notes

- Access tokens: 15-minute expiration
- Refresh tokens: 7-day expiration, stored in database for revocation
- Public key distributed to all services
- Include user_id, roles, and permissions in token payload
```

---

## ADR Workflow

### 1. Create ADR (Proposed Status)

When facing an architectural decision:

```bash
# Create new ADR file
# Use sequential numbering: 0001, 0002, etc.
touch docs/adr/0005-use-graphql-for-api.md
```

```markdown
# 5. Use GraphQL for Public API

## Status

Proposed

## Context

[Describe the decision context...]

## Decision

[Propose the solution...]

## Consequences

[List expected consequences...]
```

### 2. Discuss and Iterate

- Share ADR with team/stakeholders
- Discuss in architecture review meeting
- Update based on feedback
- Add alternatives considered
- Refine consequences

### 3. Accept Decision

Once decision is made:

```markdown
## Status

Accepted

Date: 2024-01-15
```

Commit the ADR with implementation:

```bash
git add docs/adr/0005-use-graphql-for-api.md
git commit -m "docs: ADR-0005 - Use GraphQL for public API"
```

### 4. Link to Implementation

```markdown
## Implementation

- PR #234: Initial GraphQL schema
- PR #235: Apollo Server setup
- PR #236: Frontend Apollo Client integration

See `/src/graphql` for implementation.
```

### 5. Update if Deprecated/Superseded

When decision changes:

```markdown
## Status

Superseded by ADR-0012

Reason: GraphQL complexity exceeded benefits for our use case.
We're migrating back to REST with OpenAPI.
```

---

## ADR Repository Structure

### Recommended Structure

```
docs/
└── adr/
    ├── README.md                                  # Index of all ADRs
    ├── 0001-record-architecture-decisions.md      # Meta-ADR
    ├── 0002-use-postgresql-database.md
    ├── 0003-adopt-microservices-architecture.md
    ├── 0004-use-react-for-frontend.md
    ├── 0005-implement-event-sourcing.md
    └── template.md                                # Template for new ADRs
```

### README.md Example

```markdown
# Architecture Decision Records

This directory contains Architecture Decision Records (ADRs) for [Project Name].

## What is an ADR?

An ADR is a document that captures an important architectural decision made along
with its context and consequences.

## ADR Index

| ADR | Title | Status | Date |
|-----|-------|--------|------|
| [0001](0001-record-architecture-decisions.md) | Record architecture decisions | Accepted | 2024-01-10 |
| [0002](0002-use-postgresql-database.md) | Use PostgreSQL as primary database | Accepted | 2024-01-12 |
| [0003](0003-adopt-microservices-architecture.md) | Adopt microservices architecture | Accepted | 2024-01-15 |
| [0004](0004-use-react-for-frontend.md) | Use React for frontend | Accepted | 2024-01-18 |
| [0005](0005-use-graphql-for-api.md) | Use GraphQL for public API | Superseded | 2024-01-20 |

## By Status

### Accepted
- 0001, 0002, 0003, 0004

### Superseded
- 0005 (superseded by 0012)

## By Category

### Data Storage
- 0002: PostgreSQL database

### Architecture Patterns
- 0003: Microservices

### Frontend
- 0004: React

## Process

1. Copy `template.md` to new file with next number
2. Fill in context, decision, and consequences
3. Mark as "Proposed"
4. Discuss with team
5. Mark as "Accepted" when decided
6. Link to implementation PRs
```

### Template.md Example

```markdown
# [Number]. [Short title]

## Status

Proposed

## Context

What is the issue we're seeing that is motivating this decision or change?

Include:
- Current situation
- Problem statement
- Constraints (time, cost, skills, technology)
- Stakeholder concerns
- Dependencies

## Decision

What is the change that we're proposing?

Be specific:
- What we will do
- What technologies/patterns we'll use
- How it integrates with existing architecture
- Implementation approach

## Consequences

What becomes easier or more difficult?

### Positive Consequences

-
-

### Negative Consequences

-
-

### Risks

-
-

## Alternatives Considered

### [Alternative 1]

- **Pros:**
- **Cons:**
- **Why rejected:**

### [Alternative 2]

- **Pros:**
- **Cons:**
- **Why rejected:**
```

---

## When to Write an ADR

### Write an ADR for:

**Technology Selection:**
- Database choice (PostgreSQL vs MongoDB)
- Framework selection (React vs Vue vs Angular)
- Cloud provider (AWS vs Azure vs GCP)
- Message queue (Kafka vs RabbitMQ vs SQS)
- Authentication system (Auth0 vs Cognito vs custom)

**Architectural Patterns:**
- Microservices vs monolith
- Event-driven architecture
- CQRS and Event Sourcing
- API design (REST vs GraphQL vs gRPC)
- Data storage patterns (normalized vs denormalized)

**Infrastructure Decisions:**
- Deployment strategy (Kubernetes vs Serverless)
- CI/CD approach (GitHub Actions vs Jenkins vs GitLab CI)
- Monitoring solution (Datadog vs New Relic vs Prometheus)
- CDN provider (CloudFlare vs AWS CloudFront)

**Security and Compliance:**
- Authentication mechanism (JWT vs sessions)
- Authorization model (RBAC vs ABAC)
- Data encryption approach
- Compliance strategy (GDPR, HIPAA)

**System Boundaries:**
- Service decomposition boundaries
- API contracts between teams
- Data ownership and access patterns

### Don't Write an ADR for:

- **Implementation details**: How you write a specific function
- **Minor refactorings**: Renaming variables, extracting functions
- **Bug fixes**: Unless they require architectural change
- **Configuration changes**: Adjusting timeout values, feature flags
- **Obvious choices**: Using Git for version control

**Rule of thumb:** If the decision will affect the system for >6 months and involves trade-offs, write an ADR.

---

## ADR Tools and Automation

### 1. adr-tools (Command Line)

```bash
# Install adr-tools
brew install adr-tools

# Initialize ADR directory
adr init docs/adr

# Create new ADR
adr new "Use microservices architecture"

# Create ADR that supersedes another
adr new -s 5 "Use REST API instead of GraphQL"

# Generate table of contents
adr generate toc

# List all ADRs
adr list
```

### 2. Manual Management

```bash
# Create new ADR (manual)
NUM=$(ls docs/adr/*.md | wc -l | xargs expr 1 +)
FILE=$(printf "docs/adr/%04d-my-decision.md" $NUM)
cp docs/adr/template.md "$FILE"
echo "Created $FILE"
```

### 3. Integration with Documentation Sites

**MkDocs:**

```yaml
# mkdocs.yml
nav:
  - Home: index.md
  - Architecture:
    - ADRs: adr/README.md
    - All Decisions: adr/
```

**Docusaurus:**

```javascript
// docusaurus.config.js
module.exports = {
  // ...
  plugins: [
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'adr',
        path: 'docs/adr',
        routeBasePath: 'adr',
        sidebarPath: require.resolve('./sidebarsAdr.js'),
      },
    ],
  ],
};
```

### 4. Linking ADRs to Code

**In code comments:**

```python
# Authentication implementation
# See ADR-0008: Use JWT for stateless authentication
# docs/adr/0008-use-jwt-authentication.md

def authenticate_request(token: str) -> User:
    """Authenticate JWT token.

    Implementation of decision in ADR-0008.
    """
    # ...
```

**In pull requests:**

```markdown
## Changes

This PR implements the API Gateway as described in ADR-0015.

## Related ADRs

- [ADR-0015: Implement API Gateway](../docs/adr/0015-implement-api-gateway.md)
- [ADR-0003: Microservices architecture](../docs/adr/0003-adopt-microservices-architecture.md)
```

---

## ADR Best Practices

### 1. Write ADRs When Making Decisions (Not After)

❌ **Bad:**
```
# Implementation complete 6 months ago
# Writing ADR now from memory
# Can't remember all alternatives considered
```

✅ **Good:**
```
# During architecture review
# Document context while fresh
# Capture all alternatives discussed
# Record actual constraints faced
```

### 2. Focus on "Why" Not "What"

❌ **Bad:**
```markdown
## Decision

We will use PostgreSQL. We will set up replication.
We will use connection pooling.
```

✅ **Good:**
```markdown
## Decision

We will use PostgreSQL because:
- We need ACID transactions for financial data integrity
- Team has 5 years SQL experience but no NoSQL experience
- JSONB support allows flexible schema where needed
- Budget constraints favor PostgreSQL over commercial databases
```

### 3. Document Trade-offs Honestly

❌ **Bad:**
```markdown
## Consequences

- Everything is better
- No downsides
- Perfect solution
```

✅ **Good:**
```markdown
## Consequences

### Positive
- ACID guarantees ensure data integrity
- Rich query capabilities support complex analytics

### Negative
- Vertical scaling limited by single instance
- Eventual need for sharding adds complexity
- Operational overhead for backups and maintenance

### Accepted Trade-offs
- Sacrificing horizontal scalability for ACID guarantees
- Accepting operational overhead for mature ecosystem
```

### 4. Include Alternatives Considered

```markdown
## Alternatives Considered

### MongoDB

**Pros:**
- Flexible schema supports rapid iteration
- Horizontal scaling built-in
- Native JSON document storage

**Cons:**
- Team has no production MongoDB experience
- Eventual consistency adds complexity
- Weaker ACID guarantees

**Why Rejected:**
ACID guarantees are non-negotiable for financial transactions.
Schema flexibility is nice-to-have, not must-have.

### MySQL

**Pros:**
- Similar to PostgreSQL
- Large ecosystem

**Cons:**
- Weaker JSON support
- Fewer advanced features
- Less active development

**Why Rejected:**
PostgreSQL offers more advanced features (JSONB, window functions,
full-text search) at similar operational cost.
```

### 5. Keep ADRs Immutable

**Don't edit old ADRs.** If a decision changes, create a new ADR that supersedes it.

```markdown
# 0005-use-graphql-for-api.md

## Status

Superseded by ADR-0012 on 2024-03-15

Reason: GraphQL added complexity without sufficient benefit.
Migration to REST API documented in ADR-0012.
```

```markdown
# 0012-migrate-to-rest-api.md

## Status

Accepted

Supersedes: ADR-0005

## Context

ADR-0005 decided to use GraphQL for our public API. After 6 months of
production use, we've identified several issues:

- Complex queries causing N+1 performance problems
- Clients only use simple queries, not complex graph traversals
- Team spending 40% of time on GraphQL-specific issues
- Tooling and monitoring more complex than expected

The original assumption that clients would benefit from flexible
queries has not proven true in practice.

## Decision

Migrate back to REST API with OpenAPI specification.
[...]
```

### 6. Review ADRs in Architecture Reviews

Include ADR review in your architecture review process:

```markdown
## Architecture Review Checklist

- [ ] ADR created for decision
- [ ] Context clearly documented
- [ ] Alternatives considered and documented
- [ ] Trade-offs explicitly stated
- [ ] Consequences (positive and negative) identified
- [ ] Implementation plan outlined
- [ ] Risks and mitigation strategies defined
- [ ] Team reviewed and approved ADR
```

---

## Common ADR Anti-Patterns

### 1. Writing ADRs After Implementation

**Problem:** Memory fades, context is lost, alternatives forgotten.

**Solution:** Write ADR during or immediately after decision-making, before implementation.

### 2. Overly Technical ADRs

**Problem:**
```markdown
## Decision

We will use PostgreSQL 15.2 with the following postgresql.conf settings:
- shared_buffers = 256MB
- max_connections = 100
[... 50 lines of config ...]
```

**Solution:** Focus on architectural decision, not implementation details.

### 3. No Alternatives Documented

**Problem:**
```markdown
## Decision

Use React for frontend.
```

**Solution:** Document what alternatives you considered and why you rejected them.

### 4. Missing Context

**Problem:**
```markdown
## Context

We need a database.
```

**Solution:** Provide rich context about constraints, requirements, and current situation.

### 5. Vague Consequences

**Problem:**
```markdown
## Consequences

- Good performance
- Easy to use
```

**Solution:** Be specific about trade-offs and measurable impacts.

### 6. Not Updating Superseded ADRs

**Problem:** ADR-0005 says "use GraphQL" but we switched to REST. No update to ADR-0005.

**Solution:** Update old ADR to reference superseding ADR.

---

## Quick Reference

### ADR Checklist

When writing an ADR:

- [ ] **Title**: Clear, specific (not vague)
- [ ] **Status**: Proposed/Accepted/Deprecated/Superseded
- [ ] **Context**: Current situation, constraints, stakeholders
- [ ] **Decision**: Specific, actionable solution
- [ ] **Consequences**: Positive, negative, and neutral
- [ ] **Alternatives**: What else was considered and why rejected
- [ ] **Trade-offs**: Explicitly stated
- [ ] **Date**: When decision was made
- [ ] **Authors**: Who made the decision
- [ ] **Reviewers**: Who approved it

### ADR Statuses

| Status | Meaning | When to Use |
|--------|---------|-------------|
| **Proposed** | Under discussion | Initial ADR creation |
| **Accepted** | Decision approved | After team approval |
| **Rejected** | Proposal declined | Decision not to proceed |
| **Deprecated** | No longer relevant | Decision obsolete |
| **Superseded** | Replaced by new ADR | Decision changed |

### Quick Commands

```bash
# Create new ADR
adr new "Decision title"

# Create superseding ADR
adr new -s 5 "New decision"

# List all ADRs
adr list

# Generate TOC
adr generate toc

# Search ADRs
grep -r "PostgreSQL" docs/adr/
```

---

## Integration with Other Skills

### With Architecture Review

ADRs are the **output** of architecture reviews:

1. **During architecture review**: Evaluate options, discuss trade-offs
2. **Document in ADR**: Capture decision, context, and consequences
3. **Reference in implementation**: Link code to ADR

```markdown
# Architecture Review → ADR Workflow

1. **Review Meeting**: Discuss architecture options
2. **Create ADR**: Document decision (marked as "Proposed")
3. **Team Review**: Iterate on ADR based on feedback
4. **Approve ADR**: Change status to "Accepted"
5. **Implement**: Reference ADR in code and PRs
6. **Retrospect**: Update ADR if needed (via superseding ADR)
```

### With Technical Writing

Apply technical writing principles to ADRs:

- **Audience-focused**: Write for future readers who lack context
- **Clear language**: Avoid jargon, explain technical terms
- **Show, don't tell**: Include examples and diagrams
- **Progressive disclosure**: Start with summary, add details
- **Active voice**: "We decided to X" not "X was decided"

### With Evaluation Skill

ADRs document the **outcome** of evaluations:

```markdown
# Evaluation Process → ADR

1. **Evaluation**: Compare options systematically (see evaluation skill)
2. **Decision**: Choose based on weighted criteria
3. **ADR**: Document the decision with evaluation summary

## Example:

### In Evaluation Doc:
| Criterion     | Weight | Option A | Option B | Option C |
|---------------|--------|----------|----------|----------|
| Performance   | 30%    | 8        | 6        | 9        |
| Cost          | 25%    | 7        | 9        | 5        |
| Team Skills   | 20%    | 9        | 5        | 6        |
| Ecosystem     | 25%    | 8        | 7        | 7        |
| **Total**     |        | **7.95** | 6.8      | 6.8      |

### In ADR:
"Based on evaluation (see docs/evaluation-database.md), we selected Option A
due to superior performance (8/10) and team expertise (9/10), despite higher
cost (7/10 vs 9/10 for Option B)."
```

### With Code Review

Reference ADRs during code review:

```markdown
# PR #234: Implement API Gateway

## Changes
- Add Kong API Gateway
- Configure routing rules
- Implement authentication plugin

## Relates to ADR-0015
This PR implements the API Gateway decision documented in:
[ADR-0015: Implement API Gateway](../docs/adr/0015-implement-api-gateway.md)

## Review Focus
- Does implementation match ADR-0015 decision?
- Are trade-offs from ADR appropriately handled?
- Should ADR be updated based on implementation learnings?
```

### With Documentation Writing

ADRs complement other documentation:

```
docs/
├── README.md              # What the project does
├── ARCHITECTURE.md        # How the system is structured
├── adr/                   # Why we made specific decisions
│   ├── 0001-*.md
│   └── 0002-*.md
└── api/                   # How to use the API
```

Link from architecture docs to ADRs:

```markdown
# Architecture Guide

## Database Layer

We use PostgreSQL as our primary database. See [ADR-0002](adr/0002-use-postgresql-database.md)
for the rationale behind this choice.

## Service Architecture

The system follows microservices architecture. See [ADR-0003](adr/0003-adopt-microservices-architecture.md)
for details on this decision and our migration strategy.
```

---

**Remember:** ADRs are not just documentation—they're institutional memory. They preserve the reasoning behind decisions long after team members leave. They prevent re-litigating settled questions. They help new team members understand "why things are the way they are." Write ADRs when making decisions, capture the context while it's fresh, and be honest about trade-offs. Your future self (and your team) will thank you.
