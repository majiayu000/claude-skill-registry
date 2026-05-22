---
name: service-architecture
description: Service-oriented and microservices architecture patterns for cloud-scale systems. Covers service boundaries, API versioning and backward compatibility, eventual consistency at the API layer, idempotency keys, saga and choreography patterns, bulkheads, circuit breakers, service meshes, and the Vogels "you build it, you run it" operating principle. Use when designing service decomposition, API contracts, inter-service communication, or reviewing a proposed microservices architecture for coupling and resilience.
type: skill
category: cloud-systems
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/cloud-systems/service-architecture/SKILL.md
superseded_by: null
---
# Service Architecture

Service architecture is the discipline of decomposing a large system into cooperating services with explicit contracts, operational boundaries, and failure isolation. The goal is not to have as many services as possible — it is to minimize the coupling between parts of the system that change at different rates or have different operational requirements, while keeping the total operational and cognitive cost manageable. This skill catalogs the patterns, trade-offs, and anti-patterns that come up every time a team crosses the boundary from monolith to service-oriented, or from service-oriented to mesh.

**Agent affinity:** vogels (service-oriented architecture at Amazon scale), dean (internal Google service patterns), hamilton-cloud (economics of operating services at scale)

**Concept IDs:** cloud-multi-service-coordination, cloud-heat-stack-templates, cloud-runbook-structure

## The Core Principle: Coupling vs Cohesion

A well-designed service has high internal cohesion (things inside the service change together) and low external coupling (things outside the service change independently). The unit of service decomposition is not the noun from the domain model — it is the change rate and the failure domain. Two nouns that always change together belong in the same service even if they feel conceptually distinct. Two fields of the same noun may belong in different services if they are owned by different teams and have different availability requirements.

This is why "split every table into its own microservice" is an anti-pattern. Tables that are always read and updated together have high operational coupling even if they are logically separate, and splitting them produces distributed transactions that are much harder to get right than a local one.

## The Vogels Principle: You Build It, You Run It

Werner Vogels articulated the operating principle that the team that builds a service also operates it. Pager rotations, on-call burden, postmortem ownership, and feature velocity are all aligned under a single team. This is not primarily a technical pattern — it is an organizational pattern with technical consequences:

- Teams that feel operational pain invest in observability and automation.
- Teams that do not feel operational pain ship features that generate operational pain for others.
- The SLO for a service must be owned by the team that can change the service.

A service boundary is also an accountability boundary. If you cannot say which team owns a service's on-call, the service boundary is wrong.

## Service Contract Design

The API of a service is a long-term commitment. Clients depend on it. Breaking changes propagate blast radius across the organization. The design goal is to make it easy to add capability and hard to break existing clients.

### Backward Compatibility

- **Additive changes are free.** New optional fields in requests, new fields in responses, new endpoints, new enum values with a default "unknown" bucket.
- **Subtractive and type-change changes are expensive.** Removing fields, renaming fields, narrowing types, making optional fields required — all require coordinated client updates.
- **Versioning conventions.** Path-based (`/v1/`, `/v2/`), header-based (`Accept: application/vnd.service.v1+json`), or capability-based (clients negotiate features). Path-based is simplest and most commonly understood.

### The Must-Ignore Rule

Clients should ignore unknown fields in responses and servers should ignore unknown fields in requests. This allows both sides to evolve independently as long as the evolution stays within additive changes.

### Idempotency Keys

Network failures mean clients retry. Without idempotency, retries can double-charge, double-enroll, or double-ship. Every mutating endpoint should accept a client-supplied idempotency key (UUID), store it with the result for some retention period, and return the same result for duplicate requests. Stripe popularized this pattern and it is now table stakes for any external API.

## Inter-Service Communication Patterns

### Synchronous Request/Response

The default. Simple, but creates temporal coupling (the caller cannot proceed until the callee responds) and failure coupling (the callee's unavailability becomes the caller's unavailability). Appropriate when the caller genuinely needs the response to make progress.

### Asynchronous Messaging

Producer writes a message to a queue or topic; consumer processes it later. Decouples temporally and tolerates brief failures of either side. Introduces complexity around delivery semantics (at-most-once, at-least-once, exactly-once — the last of which is mostly a lie in practice) and message ordering.

### Events and Pub/Sub

A producer emits facts ("order placed") without knowing who consumes them. Consumers subscribe to event types they care about. This is the loosest coupling and the highest flexibility, and also the hardest to debug because the producer has no idea where its events end up.

### Request/Reply over Messaging

A hybrid: use messaging for transport but include a reply-to address. Gains retry-friendliness and decoupling at the cost of extra plumbing.

## Distributed Transactions: Sagas

Traditional two-phase commit is brittle at cloud scale — any participant failure stalls the entire transaction. The saga pattern decomposes a transaction into a sequence of local transactions, each of which has a compensating action that undoes its effect.

**Orchestrated saga.** A central coordinator invokes each step and triggers compensations if a step fails. Simpler to reason about, but the coordinator is a bottleneck and single point of failure.

**Choreographed saga.** Each step emits an event that triggers the next step. No central coordinator, but the control flow is distributed across the services, making it harder to debug.

Both forms give "eventual consistency with compensation" rather than atomic consistency. Applications must be designed to tolerate intermediate states visible to users (e.g., "order confirmed but payment not yet processed" — show "pending" in the UI).

## Resilience Patterns

### Circuit Breaker

Wraps a downstream call. Tracks failures in a sliding window; if the failure rate crosses a threshold, the circuit "opens" and subsequent calls fail fast without even trying the downstream. After a cooldown, the circuit goes "half-open" and allows a probe request through. This prevents a degraded downstream from consuming all the upstream's thread/connection resources.

### Bulkhead

Partition resources so that failure of one partition does not exhaust the whole system. Per-downstream thread pools, per-tenant connection limits, per-endpoint rate limits. Named after ship bulkheads — if one compartment floods, the ship stays afloat.

### Timeout and Deadline Propagation

Every RPC needs a timeout. Deadlines should propagate through the call graph: if the original request has 500ms to live, the sub-call should have less than that. Without deadline propagation, slow downstreams can tie up upstream resources for minutes.

### Retry with Exponential Backoff and Jitter

Retries help transient failures but can cause thundering herds if all clients retry at the same time. Exponential backoff (wait 1s, 2s, 4s, 8s) plus jitter (add a random factor) spreads the load.

### Graceful Degradation

When a downstream is unavailable, serve a reduced experience rather than failing entirely. Cache last-known values, return empty recommendation lists, hide non-essential UI. Users prefer a degraded site to a broken one.

## Service Mesh

A service mesh (Istio, Linkerd, Consul Connect) moves cross-cutting concerns — retries, timeouts, circuit breaking, mTLS, observability — out of application code and into a sidecar proxy. Each service pod gets an Envoy (or similar) proxy that handles ingress and egress traffic.

**Benefits.** Uniform policy, uniform observability, language-agnostic, centralized control plane.

**Costs.** Extra hop per RPC, extra operational surface area, debugging complexity (is the problem in the app, the sidecar, or the control plane?), and resource overhead per pod.

A service mesh is the right answer for a polyglot environment at scale. For a single-language system with 5 services, it is overkill — use a library.

## Anti-Patterns

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| Shared database between services | Schema change in one service breaks the other | Each service owns its data; expose via API |
| Distributed monolith | Services are split but must deploy together | Re-merge or fix the coupling driving lockstep deploys |
| Chatty APIs | N round-trips to render one page | Aggregate endpoints, or move the composition upstream |
| Nano-services | Service per function, operational overhead exceeds value | Merge cohesive functions into one service |
| Synchronous fan-out | P99 latency dominated by slowest downstream | Hedged requests, parallel with timeout, or async |
| Missing idempotency | Retries cause duplicate side effects | Require idempotency keys on all mutations |

## When to Use This Skill

- Planning a monolith-to-services migration or a service split.
- Designing a new API with backward compatibility and evolution in mind.
- Reviewing a proposed microservices architecture for hidden coupling.
- Debugging cascading failures that cross service boundaries.
- Introducing a service mesh or evaluating whether one is justified.

## When NOT to Use This Skill

- Designing in-process module boundaries. Service patterns are for network-separated failure domains.
- Small systems with 1-3 services and one team. Resilience patterns are overhead until you have the scale to need them.
- Batch processing pipelines, which follow different patterns (data-oriented, workflow engines).

## Decision Guidance

| Signal | Likely pattern |
|---|---|
| Two features always ship together | Merge services |
| One service paged for another's bug | Split services, fix observability boundary |
| One team owns the service's on-call | Good — keep boundary |
| Multi-team ownership | Split or assign clear primary |
| External clients with versioning needs | Path-based v1/v2, strict backward compat |
| Internal RPC, polyglot | Protobuf + gRPC |
| Cross-service transaction | Saga (orchestrated if simple, choreographed if complex) |

## References

- Vogels, W. (2006). "A Conversation with Werner Vogels." ACM Queue.
- Newman, S. (2015). *Building Microservices*. O'Reilly.
- Richardson, C. (2018). *Microservices Patterns*. Manning.
- Fowler, M. (2014). "Microservices." martinfowler.com.
- Nygard, M. (2007). *Release It!* Pragmatic Bookshelf.
- Hohpe, G., Woolf, B. (2003). *Enterprise Integration Patterns*. Addison-Wesley.
