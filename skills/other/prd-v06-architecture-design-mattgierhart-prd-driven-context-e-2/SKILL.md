---
name: prd-v06-architecture-design
description: Define how system components connect, establishing boundaries, patterns, and integration approaches during PRD v0.6 Architecture. Triggers on requests to design architecture, create system design, define component relationships, or when user asks "design architecture", "system design", "how do components connect?", "architecture decisions", "technical architecture", "system overview". Consumes TECH- (stack selections), RISK- (constraints), FEA- (features). Outputs ARC- entries documenting architecture decisions with rationale. Feeds v0.6 Technical Specification.
---

# Architecture Design

Position in workflow: v0.5 Technical Stack Selection → **v0.6 Architecture Design** → v0.6 Technical Specification

Architecture defines how your system components connect. This skill transforms stack selections into a coherent system design with explicit boundaries and integration patterns.

## Architecture Decision Categories

| Category | What It Covers | Example Decisions |
|----------|----------------|-------------------|
| **Structure** | Component organization, boundaries | Monolith vs microservices, module structure |
| **Integration** | External service connections | API gateway pattern, webhook handlers |
| **Security** | Auth, authorization, data protection | JWT strategy, role-based access |
| **Performance** | Scaling, caching, optimization | CDN strategy, database indexing |
| **Data** | Storage, flow, consistency | Event sourcing, CQRS, replication |
| **DevOps** | Deployment, monitoring, CI/CD | Container orchestration, observability |

## Design Process

1. **Pull TECH- decisions** — What technologies are we building with?
2. **Pull RISK- constraints** — What must the architecture account for?
3. **Pull FEA- features** — What must the system do?
4. **Define system boundaries** — What's in/out of scope?
5. **Map component relationships** — How do parts connect?
6. **Document integration patterns** — How do Buy/Integrate items connect?
7. **Create ARC- entries** — Record decisions with rationale

## System Boundary Definition

Before designing components, define what's inside and outside your system:

**Inside (Build)**:
- Core business logic
- Differentiating features
- Custom workflows

**Outside (Buy/Integrate)**:
- Authentication provider
- Payment processor
- Email service
- Analytics

**Boundary Questions**:
- Where does data enter the system?
- Where does data leave the system?
- What trust boundaries exist?
- What must be fast vs. can be eventual?

## Component Relationship Patterns

### For Build Components

| Pattern | When to Use | Example |
|---------|-------------|---------|
| **Monolith** | MVP, small team, unclear boundaries | Single Next.js app |
| **Modular Monolith** | Growing codebase, clear domains | Modules with defined interfaces |
| **Microservices** | Clear boundaries, scaling needs | Separate auth, billing, core services |

**Rule for MVP**: Start monolith, extract services when you have evidence of need.

### For Buy/Integrate Components

| Pattern | When to Use | Example |
|---------|-------------|---------|
| **Direct Integration** | Simple, trusted service | Call Stripe API directly |
| **Adapter Layer** | Want to swap providers later | Abstract over auth provider |
| **Event Bridge** | Async, decoupled | Webhooks → event queue → handlers |

## Integration Architecture Patterns

### Pattern: Vendor Abstraction

When you Buy a service but want flexibility to switch:

```
┌─────────────────────────────────────┐
│           Your Application          │
├─────────────────────────────────────┤
│       Payment Abstraction Layer     │
│   interface PaymentProvider {       │
│     charge(amount, token): Result   │
│   }                                 │
├─────────────────────────────────────┤
│  StripeAdapter  │  PaddleAdapter    │
└─────────────────┴───────────────────┘
```

**When to use**: High switching cost, multiple viable providers, strategic flexibility needed.

### Pattern: Webhook Handler

When integrating with external events:

```
External Service → Webhook Endpoint → Event Queue → Handler
                        ↓
                   Signature Verify
                        ↓
                   Idempotency Check
                        ↓
                   Enqueue for processing
```

**When to use**: External services push events (Stripe, GitHub, etc.).

## ARC- Output Template

```
ARC-XXX: [Decision Title]
Category: [Structure | Integration | Security | Performance | Data | DevOps]
Context: [What prompted this decision]
Decision: [What we decided]
Rationale: [Why this choice]

Alternatives Rejected:
  - [Option A]: [Why not]
  - [Option B]: [Why not]

Consequences:
  - Enables: [What this makes possible]
  - Constrains: [What this limits]

Related IDs: [TECH-XXX, RISK-XXX, FEA-XXX]
Status: [Proposed | Accepted | Superseded]
```

**Example ARC- entry:**
```
ARC-001: Monolith with Module Boundaries
Category: Structure
Context: Need to choose application structure for MVP launch
Decision: Single Next.js application with domain-based module folders

Rationale:
  - Team of 2 developers, single deployment simplifies ops
  - Unclear domain boundaries at this stage
  - Can extract services later when patterns emerge

Alternatives Rejected:
  - Microservices: Premature; adds ops complexity without proven need
  - Serverless functions: Harder to share code, cold start concerns

Consequences:
  - Enables: Fast iteration, simple deployment, shared state
  - Constrains: Single scaling unit, must be disciplined about module boundaries

Related IDs: TECH-001 (Next.js), RISK-005 (scaling concerns)
Status: Accepted
```

**Example ARC- entry (Security):**
```
ARC-005: JWT with HTTP-Only Cookies
Category: Security
Context: Need session management strategy for authenticated users
Decision: JWTs stored in HTTP-only cookies, 1-hour expiry, refresh via /refresh endpoint

Rationale:
  - HTTP-only prevents XSS access to tokens
  - Short expiry limits damage from stolen tokens
  - Refresh flow handles long sessions gracefully

Alternatives Rejected:
  - localStorage: Vulnerable to XSS
  - Long-lived tokens: Security risk if compromised
  - Server-side sessions: Scaling complexity, Redis dependency

Consequences:
  - Enables: Stateless auth, horizontal scaling
  - Constrains: Must handle refresh flow in frontend, logout requires invalidation strategy

Related IDs: TECH-001 (Clerk handles this), RISK-008 (security compliance)
Status: Accepted
```

## System Diagram Elements

When creating architecture diagrams, include:

| Element | Symbol | Purpose |
|---------|--------|---------|
| **Service/Component** | Box | Internal services, modules |
| **External System** | Cloud/cylinder | Third-party services, DBs |
| **Trust Boundary** | Dashed line | Security perimeters |
| **Data Flow** | Arrow | How data moves |
| **Integration Point** | Diamond | Where systems connect |

### Example Diagram Structure

```
┌─────────────────────────────────────────────────────────┐
│                    TRUST BOUNDARY                        │
│  ┌─────────────┐     ┌─────────────┐    ┌────────────┐  │
│  │   Frontend  │────▶│   API       │───▶│  Database  │  │
│  │   (Next.js) │     │  (tRPC)     │    │  (Supabase)│  │
│  └─────────────┘     └──────┬──────┘    └────────────┘  │
│                             │                            │
└─────────────────────────────┼────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
        ┌──────────┐   ┌──────────┐   ┌──────────┐
        │  Stripe  │   │  Clerk   │   │  Resend  │
        │ (payments)│  │  (auth)  │   │ (email)  │
        └──────────┘   └──────────┘   └──────────┘
                    EXTERNAL SERVICES
```

## RISK- to Architecture Mapping

Every high-priority risk should have an architectural response:

| Risk | Architecture Response |
|------|----------------------|
| RISK-001: API dependency outage | ARC-010: Add retry + circuit breaker |
| RISK-003: Data breach | ARC-005: Encryption at rest + transit |
| RISK-007: Scaling bottleneck | ARC-012: Cache layer, read replicas |

## Anti-Patterns to Avoid

| Anti-Pattern | Signal | Fix |
|--------------|--------|-----|
| **Architecture astronaut** | Over-engineering for 1000x scale | Design for 10x current needs |
| **Missing boundaries** | Everything can call everything | Define clear interfaces |
| **Ignoring RISK-** | Architecture doesn't address risks | Map each High RISK- to ARC- |
| **Vendor lock-in** | No abstraction over critical services | Add adapter layer for switching |
| **Diagram without decisions** | Pretty pictures, no ARC- records | Every box needs documented rationale |
| **Premature microservices** | 5 services for MVP | Start monolith, extract later |

## Quality Gates

Before proceeding to Technical Specification:

- [ ] All TECH- Build items have component placement
- [ ] All TECH- Buy/Integrate items have integration pattern
- [ ] High-priority RISK- entries have architectural mitigation
- [ ] Trust boundaries clearly defined
- [ ] Data flow documented
- [ ] ARC- entries created for major decisions

## Downstream Connections

ARC- entries feed into:

| Consumer | What It Uses | Example |
|----------|--------------|---------|
| **Technical Specification** | ARC- informs API design | ARC-001 (monolith) → unified API surface |
| **v0.7 Build Execution** | ARC- defines EPIC scope | ARC-003 (auth module) → EPIC-02 |
| **Infrastructure Setup** | ARC- drives deployment | ARC-010 (edge caching) → CDN config |
| **Security Review** | Security ARC- entries | ARC-005 → pen test scope |

## Detailed References

- **Architecture pattern examples**: See `references/examples.md`
- **ARC- entry template**: See `assets/arc.md`
- **Diagram templates**: See `references/diagrams.md`
