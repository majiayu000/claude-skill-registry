---
name: backend-engineering
version: 0.1.0
description: >
  Use this skill when designing backend systems, databases, APIs, or services.
  Triggers on schema design, database migrations, indexing strategies, distributed
  systems architecture, microservices, caching, message queues, observability setup,
  logging, metrics, tracing, SLO/SLI definition, performance optimization, query
  tuning, security hardening, authentication, authorization, API design (REST,
  GraphQL, gRPC), rate limiting, pagination, and failure handling patterns. Acts as
  a senior backend engineering advisor for mid-level engineers leveling up.
category: engineering
tags: [backend, databases, api-design, distributed-systems, security, observability]
recommended_skills: [api-design, database-engineering, observability, system-design]
platforms:
  - claude-code
  - gemini-cli
  - openai-codex
  - mcp
license: MIT
maintainers:
  - github: maddhruv
---

When this skill is activated, always start your first response with the 🧢 emoji.

# Backend Engineering

A senior backend engineer's decision-making framework for building production
systems. This skill covers the six pillars of backend engineering - schema design,
scalable systems, observability, performance, security, and API design - with an
emphasis on *when* to use each pattern, not just *how*. Designed for mid-level
engineers (3-5 years) who know the basics and need opinionated guidance on
trade-offs.

---

## When to use this skill

Trigger this skill when the user:
- Designs a database schema or plans a migration
- Chooses between monolith vs microservices or evaluates scaling strategies
- Sets up logging, metrics, tracing, or alerting
- Diagnoses a performance issue (slow queries, high latency, memory pressure)
- Implements authentication, authorization, or secrets management
- Designs a REST, GraphQL, or gRPC API
- Needs retry, circuit breaker, or idempotency patterns
- Plans data consistency across services (sagas, outbox, eventual consistency)

Do NOT trigger this skill for:
- Frontend-only concerns (CSS, React components, browser APIs)
- DevOps/infra provisioning (use a Terraform/Docker/K8s skill instead)

---

## Key principles

1. **Design for failure, not just success** - Every network call can fail. Every
   disk can fill. Every dependency can go down. The question is not "will it fail"
   but "how does it degrade?" Design graceful degradation paths before writing the
   happy path.

2. **Observe before you optimize** - Never guess where the bottleneck is. Instrument
   first, measure second, optimize third. A 10ms query called 1000 times matters more
   than a 500ms query called once.

3. **Simple until proven otherwise** - Start with a monolith, a single database, and
   synchronous calls. Add complexity (microservices, queues, caches) only when you
   have evidence the simple approach fails. Every architectural boundary is a new
   failure mode.

4. **Secure by default, not by afterthought** - Auth, input validation, and encryption
   are not features to add later. They are constraints to build within from day one.
   Use established libraries. Never roll your own crypto.

5. **APIs are contracts, not implementation details** - Once published, an API is a
   promise. Design from the consumer's perspective inward. Version explicitly. Break
   nothing silently.

---

## Core concepts

Backend engineering is the discipline of building reliable, performant, and secure
server-side systems. The six pillars form a hierarchy:

**Schema design** is the foundation - get the data model wrong and everything built
on top inherits that debt. **Scalable systems** define how components communicate and
grow. **Observability** gives you eyes into what's actually happening in production.
**Performance** is the art of making it fast *after* you've made it correct.
**Security** is the set of constraints that keep the system trustworthy. **API design**
is the surface area through which consumers interact with all of the above.

These pillars are not independent. A bad schema creates performance problems. Poor
observability makes security incidents invisible. A poorly designed API forces clients
into patterns that break your scaling strategy. Think of them as a connected system,
not a checklist.

---

## Common tasks

### Design a database schema

Start from access patterns, not entity relationships. Ask: "What queries will this
serve?" before drawing a single table.

**Decision framework:**
- Read-heavy, predictable queries -> Normalize (3NF), add targeted indexes
- Write-heavy, high throughput -> Consider denormalization, append-only tables
- Complex relationships with traversals -> Consider a graph model
- Unstructured/evolving data -> Document store (but think twice)

**Indexing rule of thumb:** Index columns that appear in WHERE, JOIN, and ORDER BY.
A composite index on `(a, b, c)` serves queries on `(a)`, `(a, b)`, and `(a, b, c)`
but NOT `(b, c)`. Check the references/ file for detailed indexing strategies.

> Always plan migration rollbacks. A deploy that adds a column is safe. A deploy that
> drops a column is a one-way door. Use expand-contract migrations for breaking changes.

### Choose a scaling strategy

```
Is a single server sufficient?
  YES -> Stay there. Optimize vertically first.
  NO  -> Is the bottleneck compute or data?
    COMPUTE -> Horizontal scale with stateless services + load balancer
    DATA    -> Is it read-heavy or write-heavy?
      READ  -> Add read replicas, then caching layer
      WRITE -> Partition/shard the database
```

Only introduce microservices when you have: (a) independent deployment needs,
(b) different scaling profiles per component, or (c) team boundaries that demand it.

> Never split a monolith along technical layers (API service, data service). Split
> along business domains (orders, payments, inventory).

### Set up observability

Implement the three pillars with correlation:

| Pillar | What it answers | Tool examples |
|---|---|---|
| **Logs** | What happened? | Structured JSON logs with correlation IDs |
| **Metrics** | How is the system performing? | RED metrics (Rate, Errors, Duration) |
| **Traces** | Where did time go? | Distributed traces across service boundaries |

Define SLOs before writing alerts. An SLO like "99.9% of requests complete in <200ms"
gives you an error budget. Alert when the burn rate threatens the budget, not on every
spike.

### Diagnose a performance issue

Follow this checklist in order:

1. **Check metrics** - is it CPU, memory, I/O, or network?
2. **Check slow query logs** - are there N+1 patterns or full table scans?
3. **Check connection pools** - are connections exhausted or leaking?
4. **Check external dependencies** - is a downstream service slow?
5. **Profile the code** - only after ruling out infrastructure causes

> The fix for "the database is slow" is almost never "add more database." It's
> usually: add an index, fix an N+1, or cache a hot read path.

### Secure a service

Minimum security checklist for any backend service:

- **Authentication**: Use OAuth 2.0 / OIDC for user-facing, API keys + HMAC for
  service-to-service. Never store plain-text passwords (bcrypt/argon2 minimum).
- **Authorization**: Implement at the middleware level. Default deny. Check
  permissions on every request, not just at the edge.
- **Input validation**: Validate at system boundaries. Use allowlists, not blocklists.
  Parameterize all SQL queries.
- **Secrets**: Use a secrets manager (Vault, AWS Secrets Manager). Never commit
  secrets to git. Rotate regularly.
- **Transport**: TLS everywhere. No exceptions.

### Design an API

**REST decision table:**

| Need | Pattern |
|---|---|
| Simple CRUD | REST with standard HTTP verbs |
| Complex queries with flexible fields | GraphQL |
| High-performance internal service calls | gRPC |
| Real-time bidirectional | WebSockets |
| Event notification to external consumers | Webhooks |

**Pagination**: Use cursor-based for large/changing datasets, offset-based only for
small/static datasets. Always include a `next_cursor` field.

**Versioning**: URL path versioning (`/v1/`) for public APIs, header versioning for
internal. Never break existing consumers silently.

**Rate limiting**: Token bucket for user-facing, fixed window for internal. Always
return `Retry-After` headers with 429 responses.

### Handle partial failures

When services depend on other services, failures cascade. Use these patterns:

- **Retry with exponential backoff + jitter** - for transient failures (network blips,
  503s). Cap at 3-5 retries.
- **Circuit breaker** - stop calling a failing dependency. States: closed (normal) ->
  open (failing, fast-fail) -> half-open (testing recovery).
- **Idempotency keys** - make retries safe. Every mutating operation should accept
  an idempotency key so duplicate requests produce the same result.
- **Timeouts** - always set them. A missing timeout is an unbounded resource leak.

### Plan data consistency

For distributed data across services:

- **Strong consistency needed?** -> Single database, ACID transactions
- **Can tolerate eventual consistency?** -> Event-driven with outbox pattern
- **Multi-step business process?** -> Saga pattern (prefer choreography over
  orchestration for simple flows, orchestration for complex ones)

> The outbox pattern: write the event to a local "outbox" table in the same
> transaction as the data change. A separate process publishes outbox events to
> the message broker. This guarantees at-least-once delivery without 2PC.

---

## Anti-patterns / common mistakes

| Mistake | Why it's wrong | What to do instead |
|---|---|---|
| Premature microservices | Creates distributed monolith, adds network failure modes | Start monolith, extract services when domain boundaries are proven |
| Missing indexes on query columns | Full table scans under load, cascading timeouts | Profile queries with EXPLAIN, add indexes for WHERE/JOIN/ORDER BY |
| Logging everything, alerting on nothing | Alert fatigue, real incidents get buried | Structured logs with levels, SLO-based alerting on burn rate |
| N+1 queries in loops | Linear query growth per record, kills DB under load | Batch fetches, eager loading, or dataloader pattern |
| Rolling your own auth/crypto | Subtle security bugs that go unnoticed for months | Use battle-tested libraries (bcrypt, passport, OIDC providers) |
| Designing APIs from the database out | Leaks internal structure, painful to evolve | Design from consumer needs inward, then map to storage |
| Destructive migrations without rollback | One-way door that can cause downtime | Expand-contract pattern, backward-compatible migrations |
| Caching without invalidation strategy | Stale data, cache-database drift, inconsistency | Define TTL, invalidation triggers, and cache-aside pattern upfront |

---

## Gotchas

1. **Expand-contract is the only safe way to remove a column** - Deploying code that removes a column before the column is dropped from the database causes immediate errors. Deploying a migration that drops a column while old code still reads it causes the same. The only safe path: deploy new code that ignores the old column, then deploy the migration that drops it, then optionally clean up the code.

2. **Connection pool exhaustion looks like a slow database** - When all connections in the pool are in use, new queries queue up indefinitely. Profiling shows slow queries; the real problem is too many concurrent requests or a connection leak. Check pool metrics (active, idle, waiting) before blaming the database.

3. **Outbox pattern requires an idempotent consumer** - The outbox pattern guarantees at-least-once delivery. If your message consumer isn't idempotent, it will process the same event twice after a crash and a restart. Every consumer must be able to handle duplicate messages safely.

4. **`N+1` queries in ORM code are invisible until production load** - Fetching a list of 50 orders and then calling `.customer` on each in a loop generates 51 queries. In development with 5 rows it's imperceptible; under production load it causes cascading timeouts. Always check query counts in integration tests and use eager loading for related data.

5. **Circuit breakers need a half-open timeout** - A circuit that opens on failure and never closes traps a service in permanent degraded mode even after the downstream dependency recovers. Always configure a half-open probe interval so the breaker tests recovery and transitions back to closed state automatically.

---

## References

For detailed patterns and implementation guidance on specific domains, read the
relevant file from the `references/` folder:

- `references/schema-design.md` - normalization, indexing strategies, migration patterns
- `references/scalable-systems.md` - distributed patterns, caching, queues, load balancing
- `references/observability.md` - logging, metrics, tracing, SLOs, alerting setup
- `references/performance.md` - profiling, query optimization, connection pooling, async
- `references/security.md` - auth flows, encryption, OWASP top 10, secrets management
- `references/api-design.md` - REST/GraphQL/gRPC conventions, versioning, pagination
- `references/failure-patterns.md` - circuit breakers, retries, idempotency, sagas

Only load a references file if the current task requires it - they are long and
will consume context.

---

## Companion check

> On first activation of this skill in a conversation: check which companion skills are installed by running `ls ~/.claude/skills/ ~/.agent/skills/ ~/.agents/skills/ .claude/skills/ .agent/skills/ .agents/skills/ 2>/dev/null`. Compare the results against the `recommended_skills` field in this file's frontmatter. For any that are missing, mention them once and offer to install:
> ```
> npx skills add AbsolutelySkilled/AbsolutelySkilled --skill <name>
> ```
> Skip entirely if `recommended_skills` is empty or all companions are already installed.
