---
name: create-architecture
description: Generate comprehensive system architecture documents from requirements, supporting Frontend, Backend, and Fullstack projects with scale-adaptive depth and Architecture Decision Records. Use when translating requirements (PRD/epic) into technical architecture for new projects or major features.
acceptance:
  - architecture_created: "Architecture document created at docs/architecture.md"
  - all_sections_present: "All required sections present for project type"
  - tech_stack_justified: "Technology stack decisions documented with justification"
  - adrs_created: "At least 3 Architecture Decision Records created"
  - nfrs_addressed: "Non-functional requirements addressed in architecture"
inputs:
  requirements_file:
    type: string
    required: true
    description: "Path to PRD or requirements document"
  project_type:
    type: string
    required: false
    description: "frontend | backend | fullstack (auto-detected if not provided)"
  complexity:
    type: string
    required: false
    description: "simple | medium | complex (auto-calculated if not provided)"
  existing_architecture:
    type: string
    required: false
    description: "Path to existing architecture (for brownfield projects)"
outputs:
  architecture_file:
    type: string
    description: "Path to created architecture document"
  project_type:
    type: string
    description: "Detected or specified project type"
  complexity_score:
    type: number
    description: "Calculated complexity score (0-100)"
  adrs_created:
    type: number
    description: "Number of ADRs created"
  sections_included:
    type: array
    description: "List of architecture sections included"
telemetry:
  emit: "skill.create-architecture.completed"
  track:
    - project_type
    - complexity_score
    - adrs_created
    - duration_ms
    - tech_stack_size
---

# Create Architecture

## Purpose

Generate comprehensive, production-ready system architecture documents from requirements. Supports Frontend, Backend, and Fullstack projects with scale-adaptive depth, proven architectural patterns, and Architecture Decision Records (ADRs).

**Core Principles:**
- **Multi-domain support:** Frontend, Backend, Fullstack architectures
- **Scale-adaptive:** Adjusts detail based on project complexity
- **Pattern-driven:** Leverages proven architectural patterns catalog
- **Decision-focused:** Documents key decisions as ADRs
- **Technology-agnostic:** Considers multiple options, recommends best fit

---

## Prerequisites

- Requirements document exists (PRD, epic, or user stories)
- Non-functional requirements (NFRs) defined or inferable
- Target user scale and data volume known or estimable
- Project constraints documented (team, timeline, budget)

---

## Workflow

### 1. Load and Analyze Requirements

**Action:** Read requirements document using bmad-commands

Execute:
```bash
python .claude/skills/bmad-commands/scripts/read_file.py \
  --path {requirements_file} \
  --output json
```

**Extract from requirements:**
- Functional requirements (features, capabilities)
- Non-functional requirements (performance, security, scalability)
- Business goals and constraints
- Technical constraints (technologies, platforms)
- User scale estimates
- Data volume estimates
- Integration requirements

**If brownfield:** Also load existing architecture for context.

**See:** `references/requirements-analysis-guide.md` for extraction techniques

---

### 2. Detect Project Type

**Analyze requirements to determine domain:**

**Frontend-only indicators:**
- UI/UX requirements are dominant
- No backend/API requirements mentioned
- Focus on components, state, routing, styling
- Technologies: React, Vue, Angular, Svelte

**Backend-only indicators:**
- API/service requirements dominant
- No UI requirements mentioned
- Focus on business logic, data processing, integrations
- Technologies: Node.js, Python, Java, Go, Rust

**Fullstack indicators:**
- Both frontend and backend requirements
- End-to-end user journeys described
- Integration between UI and services
- Technologies span both domains

**Default:** If unclear, select **Fullstack** (most comprehensive)

**See:** `references/project-type-patterns.md` for detailed detection criteria

---

### 3. Assess Complexity

**Calculate complexity score based on weighted factors:**

| Factor | Weight | Scoring |
|--------|--------|---------|
| User scale | 25% | <1K=10, 1K-10K=30, 10K-100K=60, >100K=90 |
| Data volume | 20% | <10GB=10, 10GB-1TB=40, >1TB=80 |
| Integration points | 20% | 0-2=10, 3-5=40, 6-10=70, >10=90 |
| Performance reqs | 15% | None=0, Standard=30, Strict=70 |
| Security reqs | 10% | Basic=10, Standard=40, Advanced=80 |
| Deployment | 10% | Single=10, Multi-region=50, Global=80 |

**Complexity Formula:**
```
Score = (scale × 0.25) + (data × 0.20) + (integrations × 0.20) +
        (perf × 0.15) + (security × 0.10) + (deploy × 0.10)
```

**Categories:**
- **0-30:** Simple (single-tier, standard patterns)
- **31-60:** Medium (multi-tier, moderate patterns)
- **61-100:** Complex (distributed, advanced patterns)

**This determines:** Architecture depth, pattern selection, ADR count

**See:** `references/complexity-assessment.md` for detailed scoring guide

---

### 4. Select Architectural Patterns

**Based on project type and complexity, select patterns:**

**Frontend Patterns:**
- Component architecture (atomic design, compound components)
- State management (Redux, Zustand, Context, Recoil)
- Routing strategies (file-based, declarative, nested)
- Styling approach (CSS-in-JS, Tailwind, CSS Modules)
- Data fetching (React Query, SWR, Apollo)

**Backend Patterns:**
- API design (REST, GraphQL, tRPC, gRPC)
- Service architecture (monolith, microservices, modular monolith)
- Data modeling (relational, document, event-sourced)
- Integration patterns (message queues, event buses, webhooks)
- Caching strategies (Redis, Memcached, CDN)

**Fullstack Patterns:**
- Framework selection (Next.js, Remix, SvelteKit, Nuxt)
- Monorepo structure (Turborepo, Nx, Lerna)
- API layers (BFF, API Gateway, tRPC)
- Deployment (Vercel, Netlify, AWS, Docker/K8s)
- Authentication (NextAuth, Passport, Auth0, Clerk)

**See:** `references/patterns-catalog.md` for complete pattern library

---

### 5. Evaluate Technology Stack

**For each architectural component, evaluate options:**

**Evaluation Criteria:**
1. Requirements fit (does it meet functional/NFRs?)
2. Team expertise (can team use this effectively?)
3. Community support (strong ecosystem?)
4. Performance (meets requirements?)
5. Scalability (scales with growth?)
6. Cost (licensing/infrastructure costs?)
7. Maintenance (long-term burden?)
8. Migration path (can we change later?)

**Decision Process:**
1. Identify requirements for component
2. Generate 3-5 alternatives
3. Evaluate against criteria
4. Select best fit
5. Document in ADR

**See:** `references/technology-decision-framework.md` for evaluation matrices

---

### 6. Generate Architecture Document

**Create comprehensive architecture at docs/architecture.md:**

**Structure (adapt based on project type):**

```markdown
# [Project Name] Architecture

## 1. System Overview
[High-level description, context, goals]

## 2. Architecture Diagrams
[C4 context, container, component diagrams]

## 3. Frontend Architecture (if applicable)
[Component design, state management, routing, styling, build]

## 4. Backend Architecture (if applicable)
[API design, services, data layer, business logic, integrations]

## 5. Fullstack Integration (if applicable)
[End-to-end flows, API contracts, auth, deployment]

## 6. Data Architecture
[Data models, relationships, migrations, caching]

## 7. Technology Stack
[All technologies with justifications]

## 8. Deployment Architecture
[Infrastructure, environments, CI/CD, monitoring]

## 9. Security Architecture
[Authentication, authorization, data protection, compliance]

## 10. Performance Architecture
[Caching, optimization, CDN, load balancing]

## 11. Scalability Plan
[Horizontal/vertical scaling, bottlenecks, growth plan]

## 12. Architecture Decision Records (ADRs)
[Key decisions with context, options considered, rationale]

## 13. Migration Strategy (brownfield only)
[Current state, target state, migration path, risks]

## 14. Open Questions & Risks
[Unknowns, risks, mitigation strategies]
```

**Scale adaptation:**
- **Simple:** Focus on sections 1, 3-7, 12 (10-15 pages)
- **Medium:** Include sections 1-12 (15-25 pages)
- **Complex:** All sections with deep analysis (25-40 pages)

**See:** `references/templates.md` for section templates

---

### 7. Create Architecture Decision Records (ADRs)

**For each significant decision, create ADR:**

**ADR Template:**
```markdown
# ADR-XXX: [Decision Title]

**Date:** YYYY-MM-DD
**Status:** Proposed | Accepted | Deprecated | Superseded

## Context
[Problem and constraints]

## Decision
[What we decided]

## Alternatives Considered
1. Option A: [pros/cons]
2. Option B: [pros/cons]
3. Option C: [pros/cons]

## Rationale
[Why this option]

## Consequences
[Positive and negative impacts]

## Related Decisions
[Links to other ADRs]
```

**Minimum ADRs:**
- Simple architecture: 3-5 ADRs
- Medium architecture: 5-10 ADRs
- Complex architecture: 10-15 ADRs

**Common ADR topics:**
- Primary technology stack selection
- Database choice
- API design approach
- State management strategy
- Authentication mechanism
- Deployment platform
- Monitoring and observability approach

**See:** `references/adr-examples.md` for ADR examples

---

### 8. Address Non-Functional Requirements

**Ensure architecture addresses all NFRs:**

**Performance:**
- Response time targets (p50, p95, p99)
- Throughput requirements (req/sec)
- Optimization strategies (caching, CDN, lazy loading)

**Scalability:**
- User growth projections
- Data growth projections
- Horizontal scaling strategy
- Bottleneck identification

**Security:**
- Authentication and authorization
- Data encryption (at rest, in transit)
- Input validation and sanitization
- Compliance requirements (GDPR, HIPAA, etc.)

**Reliability:**
- Availability targets (99%, 99.9%, 99.99%)
- Fault tolerance strategies
- Disaster recovery plan
- Backup and restore procedures

**Maintainability:**
- Code organization principles
- Testing strategy
- Documentation standards
- Technical debt management

**See:** `references/nfr-architecture-mapping.md` for NFR checklist

---

### 9. Generate Supplementary Artifacts (Optional)

**If requested or beneficial:**

**Architecture Diagrams:**
```bash
python .claude/skills/bmad-commands/scripts/generate_architecture_diagram.py \
  --architecture docs/architecture.md \
  --type c4-context \
  --output docs/diagrams/
```

**Technology Analysis Report:**
```bash
python .claude/skills/bmad-commands/scripts/analyze_tech_stack.py \
  --architecture docs/architecture.md \
  --output json
```

**Extract ADRs to separate files:**
```bash
python .claude/skills/bmad-commands/scripts/extract_adrs.py \
  --architecture docs/architecture.md \
  --output docs/adrs/
```

---

### 10. Validate Completeness

**Self-validate before marking complete:**

**Check all required sections present:**
- ✅ System Overview
- ✅ Architecture appropriate for project type
- ✅ Technology Stack documented
- ✅ NFRs addressed
- ✅ At least 3 ADRs created
- ✅ Security considerations included
- ✅ Scalability plan defined

**Quality check:**
- ✅ All technology choices justified
- ✅ Alternatives considered
- ✅ Risks identified
- ✅ No critical gaps

**If validation fails:** Address gaps before completion.

---

## Common Scenarios

### Scenario 1: Greenfield Frontend Application

**Input:** React dashboard requirements
**Output:** Frontend-only architecture with component design, state (Zustand), routing (React Router), styling (Tailwind), build (Vite)

### Scenario 2: Backend API Service

**Input:** REST API requirements for mobile app
**Output:** Backend-only architecture with Express.js, PostgreSQL, Prisma, Redis caching, JWT auth

### Scenario 3: Fullstack E-commerce Platform

**Input:** Comprehensive e-commerce requirements
**Output:** Fullstack architecture with Next.js, tRPC, PostgreSQL, Stripe integration, Vercel deployment

### Scenario 4: Brownfield System Modernization

**Input:** Legacy monolith + modernization requirements
**Output:** Migration architecture with incremental microservices extraction, API gateway, strangler fig pattern

**See:** `references/example-architectures.md` for complete examples

---

## Success Criteria

An architecture is complete and ready for implementation when:

### Documentation Completeness
- ✅ Architecture document created at `docs/architecture.md`
- ✅ All required sections present for project type:
  - System Overview & Context
  - Technology Stack (complete and justified)
  - Deployment Architecture
  - Security Architecture
  - Architecture Decision Records (ADRs)
  - Project-specific sections (Frontend/Backend/Fullstack)
- ✅ Architecture diagrams included (minimum 1, recommended 2-3)
- ✅ Technology stack fully documented with versions

### Decision Quality
- ✅ Minimum ADR count met:
  - Simple (0-30): ≥3 ADRs
  - Medium (31-60): ≥5 ADRs
  - Complex (61-100): ≥10 ADRs
- ✅ Each ADR includes:
  - Context and problem statement
  - Decision made
  - Alternatives considered (minimum 2)
  - Rationale with data/benchmarks
  - Consequences (positive and negative)
- ✅ Technology choices justified with alternatives

### NFR Coverage
- ✅ All Non-Functional Requirements addressed:
  - Performance: Targets specified (e.g., p95 <500ms)
  - Scalability: Growth projections and scaling plan
  - Security: Auth, authorization, encryption, compliance
  - Reliability: Availability target, redundancy, failover
  - Maintainability: Testing strategy, code organization
- ✅ NFRs mapped to concrete architecture decisions

### Quality Gates
- ✅ No critical gaps or missing sections
- ✅ No contradictory decisions
- ✅ Security considerations documented
- ✅ Scalability approach defined
- ✅ Deployment strategy clear
- ✅ Cost implications considered

### Validation Ready
- ✅ Architecture can be validated with validate-architecture skill
- ✅ Expected validation score ≥70
- ✅ Ready for team review
- ✅ Implementation-ready (developers can start coding)

**Checklist:**
```
[ ] Architecture document created
[ ] All required sections present
[ ] Minimum ADR count met
[ ] Technologies justified
[ ] NFRs addressed
[ ] Diagrams included
[ ] Security documented
[ ] Deployment defined
[ ] No critical gaps
[ ] Validation score ≥70
```

---

## Best Practices

1. **Start with requirements** - Architecture follows requirements, not the reverse
2. **Consider alternatives** - Evaluate 3-5 options for major decisions
3. **Document decisions** - Every significant choice becomes an ADR
4. **Think long-term** - Consider maintenance, scaling, team growth
5. **Be pragmatic** - Choose appropriate tools, not trendy ones
6. **Address NFRs explicitly** - Don't assume performance/security
7. **Plan for failure** - Include error handling, monitoring, resilience
8. **Keep it readable** - Architecture doc is for humans, not just completeness

---

## Reference Files

- `references/requirements-analysis-guide.md` - Requirement extraction techniques
- `references/project-type-patterns.md` - Project type detection criteria
- `references/complexity-assessment.md` - Detailed complexity scoring
- `references/patterns-catalog.md` - Complete architectural patterns library
- `references/technology-decision-framework.md` - Tech evaluation matrices
- `references/templates.md` - Architecture document templates
- `references/adr-examples.md` - ADR examples by domain
- `references/nfr-architecture-mapping.md` - NFR to architecture mapping
- `references/example-architectures.md` - Complete architecture examples

---

## When to Escalate

Escalate to user when:
- Requirements are insufficient or contradictory
- Conflicting NFRs (e.g., cost vs. performance)
- Missing critical information (user scale, data volume unknown)
- Highly complex system (score >80) requires expert input
- Compliance requirements (HIPAA, PCI-DSS, SOC2) need legal review
- Technology choices have significant business impact
- Budget constraints eliminate viable options

---

*Part of BMAD Enhanced Planning Suite*
