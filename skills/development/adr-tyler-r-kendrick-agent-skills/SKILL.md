---
name: adr
description: |
    Use when writing Architecture Decision Records to capture significant technical decisions with their context, rationale, and consequences. Covers the Nygard format, MADR format, ADR numbering, linking, lifecycle management, and adr-tools CLI.
    USE FOR: recording architecture decisions, documenting technical trade-offs, decision rationale capture, technology selection justification, ADR lifecycle management, lightweight decision documentation, Nygard format ADRs, MADR format
    DO NOT USE FOR: full technical design (use trd), requirements gathering (use prd or brd), design proposals seeking feedback (use rfc)
license: MIT
metadata:
  displayName: "ADR (Architecture Decision Records)"
  author: "Tyler-R-Kendrick"
compatibility: claude, copilot, cursor
references:
  - title: "Architectural Decision Records"
    url: "https://adr.github.io/"
  - title: "ADR Tools — GitHub Repository"
    url: "https://github.com/npryce/adr-tools"
---

# Architecture Decision Records (ADR)

## Overview
An Architecture Decision Record (ADR) is a short document that captures a single significant architecture decision along with its context and consequences. ADRs answer the question future developers always ask: *"Why did we do it this way?"*

ADRs are lightweight, version-controlled, and stored alongside the code they describe. They form a decision log that accumulates over the life of a project, creating an invaluable history of the reasoning behind the system's architecture.

## The Nygard Format (Original ADR)

Michael Nygard defined the original ADR format in his blog post "Documenting Architecture Decisions" (2011). It has five sections:

### Structure

```markdown
# [ADR-NNNN] [Short Title of Decision]

## Status

[Proposed | Accepted | Deprecated | Superseded by ADR-XXXX]

## Context

[What is the issue that we are seeing that is motivating this decision
or change? Describe the forces at play -- technical, political,
social, project-specific. This section is factual, not opinionated.]

## Decision

[What is the change that we are proposing and/or doing?
State the decision in active voice: "We will..."]

## Consequences

[What becomes easier or more difficult to do because of this change?
Include both positive and negative consequences. Be honest about
trade-offs.]
```

### Complete Example (Nygard Format)

```markdown
# ADR-0007: Use PostgreSQL as the Primary Database

## Status

Accepted

## Context

The Order Service requires a persistent data store for order and
payment data. We need ACID transactions for financial operations,
strong consistency guarantees, and the ability to handle complex
queries involving joins across orders, items, and payments.

The team has evaluated three options:
1. **PostgreSQL** -- relational, ACID-compliant, mature ecosystem
2. **MongoDB** -- document store, flexible schema, eventual consistency
3. **CockroachDB** -- distributed SQL, strong consistency, higher cost

Key constraints:
- The operations team has production experience with PostgreSQL
- Our cloud provider offers managed PostgreSQL (RDS/Cloud SQL)
- Financial data requires ACID transactions (not eventual consistency)
- Budget does not support CockroachDB licensing for this phase

## Decision

We will use PostgreSQL as the primary database for the Order Service.

We will use the managed PostgreSQL offering from our cloud provider
(AWS RDS) to reduce operational burden. Schema migrations will be
managed with Entity Framework Core Migrations in the application
repository.

## Consequences

**Positive:**
- ACID transactions guarantee financial data integrity
- Rich query capabilities for reporting and analytics
- Team familiarity reduces onboarding and debugging time
- Managed service reduces operational burden
- Large ecosystem of tools, extensions, and community support

**Negative:**
- Vertical scaling limits compared to distributed databases
- Schema changes require migration management
- Horizontal scaling (read replicas, sharding) adds complexity
  if we outgrow a single instance
- Document-style data (order metadata) requires JSONB columns
  rather than native document storage

**Neutral:**
- We will revisit this decision if order volume exceeds 10,000
  transactions per second, which would require a distributed
  database strategy (see future ADR)
```

## MADR Format (Markdown Any Decision Records)

MADR extends the Nygard format with additional structure for options evaluation. It is well-suited for decisions where multiple alternatives need formal comparison.

### Structure

```markdown
# [Short Title of Solved Problem and Solution]

- Status: [proposed | accepted | deprecated | superseded by ADR-XXXX]
- Deciders: [list of people involved in the decision]
- Date: YYYY-MM-DD

## Context and Problem Statement

[Describe the context and the problem statement. What is the issue?
Why does it need to be decided now?]

## Decision Drivers

- [Driver 1: e.g., team expertise]
- [Driver 2: e.g., performance requirements]
- [Driver 3: e.g., cost constraints]
- [Driver 4: e.g., time to market]

## Considered Options

1. [Option 1]
2. [Option 2]
3. [Option 3]

## Decision Outcome

Chosen option: "[Option N]", because [justification].

### Positive Consequences

- [Consequence 1]
- [Consequence 2]

### Negative Consequences

- [Consequence 1]
- [Consequence 2]

## Pros and Cons of the Options

### [Option 1]

[Description]

- Good, because [argument]
- Good, because [argument]
- Bad, because [argument]
- Bad, because [argument]

### [Option 2]

[Description]

- Good, because [argument]
- Good, because [argument]
- Bad, because [argument]

### [Option 3]

[Description]

- Good, because [argument]
- Bad, because [argument]
- Bad, because [argument]

## Links

- [Link to PRD or TRD]
- [Link to related ADR]
- [Link to RFC if this decision originated from an RFC]
```

### Complete Example (MADR Format)

```markdown
# Use React with TypeScript for the Customer Portal Frontend

- Status: Accepted
- Deciders: Frontend Team, Tech Lead, VP Engineering
- Date: 2025-01-20

## Context and Problem Statement

We are building a new customer self-service portal (see PRD-042).
We need to choose a frontend framework and language that supports
a component-based architecture, strong typing, and can be maintained
by our team of 6 frontend developers over a 3+ year lifespan.

## Decision Drivers

- Team expertise (4 of 6 developers have React experience)
- Type safety to reduce runtime errors in a financial application
- Component library availability for rapid UI development
- Long-term framework stability and community support
- Server-side rendering capability for SEO and performance

## Considered Options

1. React with TypeScript
2. Angular
3. Blazor (C# / WebAssembly)

## Decision Outcome

Chosen option: "React with TypeScript", because it aligns with
team expertise, has the largest component ecosystem, and TypeScript
provides the type safety required for a financial application.

### Positive Consequences

- Leverages existing team skills, reducing ramp-up time
- TypeScript catches type errors at compile time
- Vast ecosystem of libraries (MUI, React Query, React Hook Form)
- Next.js provides SSR/SSG when needed
- Strong hiring pool for future team growth

### Negative Consequences

- React's flexibility requires establishing conventions (state
  management, folder structure, testing patterns)
- TypeScript adds build step complexity compared to plain JS
- Must choose and maintain a state management approach (we will
  use React Query + Zustand per team preference)

## Pros and Cons of the Options

### React with TypeScript

- Good, because 4/6 developers already proficient
- Good, because largest npm ecosystem for UI components
- Good, because TypeScript adds compile-time type safety
- Good, because Next.js provides SSR capability
- Bad, because requires convention decisions (no opinionated structure)
- Bad, because JSX/TSX templating has a learning curve for non-React devs

### Angular

- Good, because highly opinionated (less convention decisions)
- Good, because built-in TypeScript support
- Good, because comprehensive framework (routing, forms, HTTP, DI)
- Bad, because only 1 developer has Angular experience
- Bad, because steeper learning curve for the team
- Bad, because smaller component library ecosystem than React

### Blazor (C# / WebAssembly)

- Good, because team has strong C# backend skills
- Good, because code sharing between frontend and backend
- Good, because strong typing with C# language features
- Bad, because WebAssembly bundle sizes impact initial load time
- Bad, because smaller ecosystem than React or Angular
- Bad, because limited SSR story compared to Next.js
- Bad, because fewer frontend-specific libraries available

## Links

- PRD-042: Customer Self-Service Portal
- ADR-0005: Use .NET 8 for Backend Services
- ADR-0007: Use PostgreSQL as Primary Database
```

## ADR Numbering

ADRs are numbered sequentially starting from 0001 (or 001). The number is immutable -- even deprecated or superseded ADRs keep their original number.

```
docs/decisions/
  0001-use-markdown-for-documentation.md
  0002-adopt-microservices-architecture.md
  0003-use-postgresql-for-persistence.md
  0004-use-rabbitmq-for-async-messaging.md
  0005-use-dotnet-8-for-backend-services.md
  0006-use-react-typescript-for-frontend.md
  0007-adopt-trunk-based-development.md
```

File naming convention: `NNNN-short-kebab-case-title.md`

## ADR Lifecycle

```
Proposed  -->  Accepted  -->  Deprecated
                  |                |
                  |                v
                  +--------->  Superseded by ADR-NNNN
```

| Status | Meaning |
|--------|---------|
| **Proposed** | Decision is under discussion, not yet finalized |
| **Accepted** | Decision has been agreed upon and is in effect |
| **Deprecated** | Decision is no longer relevant (system decommissioned, context changed) |
| **Superseded** | A newer ADR replaces this one. Link to the superseding ADR |

### Superseding an ADR

When a decision is replaced, update both the old and new ADRs:

**Old ADR (updated):**
```markdown
## Status
Superseded by [ADR-0015](0015-switch-to-kafka-for-messaging.md)
```

**New ADR:**
```markdown
## Status
Accepted. Supersedes [ADR-0004](0004-use-rabbitmq-for-async-messaging.md)

## Context
Since ADR-0004 was accepted, our message volume has grown from 1,000/min
to 50,000/min. RabbitMQ's single-node architecture cannot sustain this
throughput without significant operational complexity...
```

## ADR Linking

ADRs often reference each other and external documents:

```markdown
## Context

As described in [ADR-0002](0002-adopt-microservices-architecture.md),
we are decomposing the monolith into microservices. Each service needs
its own data store (see [ADR-0003](0003-database-per-service.md)).

This decision addresses the messaging infrastructure needed for
inter-service communication as specified in the
[TRD: Service Communication](../trd/service-communication.md).
```

## Where to Store ADRs

### Recommended Locations

| Location | When to Use |
|----------|-------------|
| `docs/decisions/` | Most common. Clear, discoverable, conventional |
| `docs/adr/` | Alternative convention, equally valid |
| `docs/architecture/decisions/` | When decisions are part of a larger architecture documentation set |
| Root `decisions/` | Smaller projects |

### Monorepo Considerations
In a monorepo, ADRs can be scoped:

```
repo/
  docs/
    decisions/           # Cross-cutting decisions
      0001-monorepo-structure.md
      0002-shared-ci-pipeline.md
  services/
    order-service/
      docs/decisions/    # Service-specific decisions
        0001-use-event-sourcing.md
    user-service/
      docs/decisions/
        0001-use-cqrs-pattern.md
```

## adr-tools CLI

[adr-tools](https://github.com/npryce/adr-tools) is a command-line tool for managing ADRs.

### Installation

```bash
# macOS
brew install adr-tools

# npm (cross-platform)
npm install -g adr-tools

# Manual
git clone https://github.com/npryce/adr-tools.git
cd adr-tools && sudo make install
```

### Usage

```bash
# Initialize ADR directory
adr init docs/decisions

# Create a new ADR
adr new "Use PostgreSQL as Primary Database"
# Creates: docs/decisions/0003-use-postgresql-as-primary-database.md

# Create a new ADR that supersedes an existing one
adr new -s 4 "Switch to Kafka for Async Messaging"
# Creates new ADR and updates ADR-0004 status to "Superseded"

# List all ADRs
adr list

# Generate a table of contents
adr generate toc

# Generate a dependency graph
adr generate graph | dot -Tpng -o adr-graph.png

# Link two ADRs
adr link 5 "Complements" 3 "Is complemented by"
```

### adr-tools Template

When you run `adr new`, it generates a file with this template:

```markdown
# [NUMBER]. [TITLE]

Date: YYYY-MM-DD

## Status

Proposed

## Context

[Describe the context here]

## Decision

[Describe the decision here]

## Consequences

[Describe the consequences here]
```

## When to Write an ADR

Write an ADR when you make a decision that:

- **Is hard to reverse** -- choosing a database, message broker, or framework
- **Affects the team** -- adopting a coding convention, branching strategy, or testing approach
- **Has trade-offs** -- there were multiple viable options with different strengths
- **Will be questioned later** -- future developers will wonder "why did they do it this way?"
- **Crosses a boundary** -- affects multiple services, teams, or systems

### Do NOT write an ADR for:
- Trivial implementation choices (variable naming, which assertion library to use)
- Decisions that are easily reversible with no downstream impact
- Decisions that are organizational standard with no alternative (mandated by policy)

## ADR vs RFC

| Aspect | ADR | RFC |
|--------|-----|-----|
| **Purpose** | Record a decision that has been made | Propose a change for discussion |
| **Timing** | Written when a decision is finalized | Written before a decision is made |
| **Scope** | Single decision with context | Broad design proposal with alternatives |
| **Length** | Short (1-2 pages) | Longer (3-10 pages) |
| **Workflow** | Author writes, team reviews | Author proposes, team debates |
| **Lifecycle** | Proposed -> Accepted -> Deprecated/Superseded | Draft -> Review -> Accepted/Rejected |
| **Relationship** | An RFC may result in one or more ADRs | An ADR may reference the RFC that led to it |

A common workflow: write an RFC to propose a significant change, gather feedback, then record the final decision as an ADR.

## Best Practices

- **Write ADRs at decision time** -- do not try to reconstruct decisions retroactively. The context is freshest when the decision is made.
- **Keep ADRs short** -- an ADR should be readable in 5 minutes. If it needs more than 2 pages, consider whether it should be an RFC or TRD instead.
- **Be honest about consequences** -- include both positive and negative consequences. Hiding trade-offs undermines trust in the decision log.
- **Never delete ADRs** -- ADRs are immutable records. Supersede or deprecate them, but never delete them. The history matters.
- **Number sequentially** -- do not reuse numbers. Gaps in numbering are fine (they indicate deleted drafts or abandoned proposals).
- **Use active voice in the Decision section** -- "We will use PostgreSQL" is clearer than "PostgreSQL was selected."
- **Link ADRs to each other** -- decisions often build on or relate to previous decisions. Cross-references create a navigable decision graph.
- **Store ADRs in the repository** -- ADRs should live alongside the code they describe, versioned in Git, and reviewed in pull requests.
- **Review ADRs in pull requests** -- treat ADRs as code. The team should review and approve decisions before they are accepted.
- **Include decision drivers** -- explicitly listing what mattered (cost, team skill, performance, time-to-market) makes the rationale transparent.
- **Revisit ADRs periodically** -- during architecture reviews, check if accepted ADRs still hold. If the context has changed, write a new ADR.
- **Use a consistent template** -- adopt either Nygard or MADR and stick with it across the project for uniformity.
