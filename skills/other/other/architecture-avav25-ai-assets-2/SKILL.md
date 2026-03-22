---
name: architecture
description: Architecture workflow — produce architectural documentation (ARD, design docs, API contracts, C4 diagrams, ARCHITECTURE.md updates) from a feature PRD, analysis request, or architectural initiative. Routes to solution-architect and system-architect roles based on scope. Input from product managers or direct analysis requests.
context: fork
argument-hint: [feature PRD or analysis request]
---

# Architecture

Produce architecture deliverables from a feature PRD, module/service analysis request, or architectural initiative. This workflow creates documentation — no code is written here. Output feeds into `/feature-plan` and `/feature-dev` for implementation.

## 1. Receive Input and Classify Scope

Gather the input from the user and classify the type of work:

- **Accepted inputs**: Feature PRD, architecture analysis request, technical initiative brief, verbal description
- Read every provided document thoroughly

### Scope Classification

Determine scope type based on the input:

| Scope Type | Trigger | Primary Role | Deliverables |
|---|---|---|---|
| **Feature Design** | PRD, feature request, new capability | `Agent(solution-architect)` | ARD, API contracts, data models, sequence diagrams, NFR spec |
| **Architecture Analysis** | "analyze service X", "document architecture of Y" | `Agent(system-architect)` | ARCHITECTURE.md, C4 diagrams, component map, tech debt register |
| **Cloud Architecture** | Cloud infra design, landing zones, migration, multi-cloud, networking, cost | `Agent(cloud-architect)` | Cloud architecture doc, networking diagrams, cost model, DR plan |
| **CI/CD Architecture** | Pipeline design, deployment strategy, GitHub org, platform engineering | `Agent(devops-architect)` | CI/CD architecture doc, pipeline diagrams, DORA targets, governance |
| **Architecture Evolution** | "migrate to X", "redesign Y", tech debt initiative | Multiple | ARD + ARCHITECTURE.md updates, migration plan, fitness functions |

If the input spans multiple scope types — execute the corresponding sections for each. If ambiguous — ask the user to clarify.

### Extract Context

From the input, extract and organize:

- **Goal**: What architectural problem we are solving (1–2 sentences)
- **Scope boundary**: Which services, modules, or system areas are affected
- **Stakeholders**: Who consumes the deliverables (engineering, product, ops)
- **Constraints**: Timeline, compatibility, regulatory, team capacity
- **Non-goals**: What is explicitly out of scope

If the input is incomplete — ask before proceeding. Do not assume missing requirements.

## 2. Understand Current Architecture

Before designing anything, map the existing state.

### 2a. Read Architecture Documentation

Read the following files (if they exist):

1. **`ARCHITECTURE.md`** — system overview, component boundaries, data flow, deployment topology
2. **`CLAUDE.md`** (root) — tech stack, project structure, conventions
3. **Subdirectory `CLAUDE.md` files** — per-service/module context
4. **Existing ADRs** — `docs/adr/`, `docs/architecture/`, or similar directories
5. **API specs** — OpenAPI files, Protobuf definitions, GraphQL schemas

### 2b. Scan Affected Areas

If documentation is incomplete or absent:

```
// turbo
find . -name "ARCHITECTURE.md" -o -name "*.openapi.*" -o -name "*.proto" -o -name "docker-compose*" -o -name "*.tf" | head -30
```

Map:
- **Service boundaries**: What services/modules exist, their responsibilities
- **Communication patterns**: REST, gRPC, events, shared DB, message queues
- **Data stores**: Databases, caches, queues — types, ownership
- **External integrations**: Third-party APIs, identity providers, payment systems
- **Deployment topology**: How services are deployed, scaled, networked

### 2c. Build Context Map

```
## Current Architecture Context

| Component | Tech Stack | Owner | Relevant to Scope |
|---|---|---|---|
| [service/module] | [lang + framework] | [team/role] | [yes/no — how] |

## Existing Decisions
- ADR-NNN: [title] — [status] — [relevance to current work]

## Gaps Identified
- [missing documentation, undocumented decisions, stale diagrams]
```

## 3. Define Non-Functional Requirements

**Apply `Agent(solution-architect)` role.**

NFRs must be defined before any design work begins. Skip this step only for pure analysis scope.

<nfr_specification>

For each relevant category, define concrete targets:

| Category | Specification |
|---|---|
| **Availability** | SLO target (e.g., 99.9%), redundancy, failover strategy |
| **Latency** | p50/p95/p99 budgets per endpoint or operation |
| **Scalability** | Expected load, scaling strategy (horizontal/vertical), limits |
| **Cost** | Per-request/per-operation budgets, infrastructure cost bounds |
| **Security** | Auth requirements, data classification, compliance (GDPR, SOC2) |
| **Observability** | Tracing, logging, metrics requirements, alerting thresholds |
| **Data** | Retention, consistency model (strong/eventual), backup/recovery RPO/RTO |

Only include categories relevant to the scope. Omit categories that add no signal.

</nfr_specification>

Present NFRs to the user for validation before proceeding.

## 4. Architecture Design

Route to the appropriate section(s) based on scope type from Step 1.

### 4a. Feature Design → `Agent(solution-architect)`

For feature-level design (PRD input), produce deliverables in this order:

**1. Options Analysis** — Propose 2–3 design options with trade-offs:

```
## Option [N]: [Name]
- **Approach**: [Description]
- **Pros**: [List]
- **Cons**: [List]
- **Risk**: [High/Med/Low] — [why]
- **Effort**: [S/M/L/XL]
- **NFR impact**: [How it affects availability, latency, cost, etc.]
```

**2. Architecture Decision Record (ARD/ADR)**:

```
# ADR-NNN: [Title]

## Status
Proposed

## Context
[Problem statement, business drivers, technical constraints]

## Decision
[Selected option with clear rationale]

## Consequences
- **Positive**: [benefits]
- **Negative**: [trade-offs, risks accepted]
- **Neutral**: [side effects]

## Alternatives Considered
[Brief summary of rejected options and why]
```

**3. Detailed Design**:
- **C4 diagrams** (Mermaid) — Context and/or Container level showing the feature's impact
- **Sequence diagrams** — for multi-service interactions, async flows
- **API contracts** — new or modified endpoints (OpenAPI fragments or structured tables)
- **Data models** — new entities, schema changes, migration strategy
- **Error handling** — failure modes, retry strategy, degradation behavior

**4. Security Review**:
- Threat scenarios (3–5 concrete abuse cases)
- Auth/authz design for new endpoints
- Data protection requirements (PII, encryption, access control)

### 4b. Architecture Analysis → `Agent(system-architect)`

For analysis scope, produce:

**1. Architecture Assessment**:
- C4 diagrams (Context + Container level) of current state
- Component inventory with responsibilities, tech stack, dependencies
- Data flow diagrams for critical paths
- Integration point map (sync/async, contracts, SLAs)

**2. Gap Analysis**:

| Area | Current State | Desired State | Gap | Priority |
|---|---|---|---|---|
| [area] | [what exists] | [what should exist] | [delta] | High/Med/Low |

**3. Technical Debt Register**:

| Item | Impact | Effort | Priority | Recommendation |
|---|---|---|---|---|
| [debt item] | High/Med/Low | S/M/L/XL | [rank] | [action] |

**4. ARCHITECTURE.md Update** — create or update following `templates/architecture.template.md`.

### 4c. Architecture Evolution → Both Roles

For migration/evolution initiatives, produce both:
- ADR (from 4a) documenting the migration decision
- ARCHITECTURE.md update (from 4b) showing target state
- **Migration plan**: phased approach (strangler fig, expand-contract, branch by abstraction)
- **Fitness functions**: automated architectural checks to enforce during transition
- **Rollback strategy**: how to revert if migration fails at each phase

## 5. Quality Gates

Review all deliverables against the checklist:

<quality_checklist>

- [ ] NFRs are concrete (numbers, not "should be fast")
- [ ] Every decision has documented rationale and alternatives
- [ ] Diagrams match the described architecture (no stale diagrams)
- [ ] API contracts are complete (request, response, errors, auth)
- [ ] Data models include migration strategy for schema changes
- [ ] Security review covers OWASP Top 10 (+ LLM Top 10 for AI systems)
- [ ] Backward compatibility is preserved or migration path documented
- [ ] Observability requirements defined (traces, logs, metrics, alerts)
- [ ] No contradictions with existing ADRs or ARCHITECTURE.md
- [ ] Cost impact estimated for infrastructure/service changes

</quality_checklist>

If any check fails — fix the deliverable before presenting.

## 6. Engineering Estimates

For feature design scope, produce estimates to feed `/feature-plan`:

| Component | Task | Complexity | Role |
|---|---|---|---|
| [component] | [task description] | S / M / L / XL | `@role` |

- **Critical path**: Longest dependency chain (e.g., DB Migration → Backend API → Frontend → E2E Tests)
- **Parallelization**: Which tasks can run concurrently by different roles
- **Constraints**: Hard dependencies on external teams, services, or decisions
- **Risks**: Dependency/integration risks with mitigations

Skip this step for pure analysis scope.

## 7. Present Deliverables

Compile and present all architecture deliverables:

```
# Architecture Deliverables: [Title]

## Scope
[1–2 sentences — what was designed/analyzed]

## Deliverables Produced
| Document | Type | Status |
|---|---|---|
| ADR-NNN: [title] | Architecture Decision Record | Proposed |
| [Feature] HLD | High-Level Design | Draft |
| API Contract: [endpoint] | OpenAPI spec | Draft |
| ARCHITECTURE.md | System documentation | Updated |

## Key Decisions
1. [Decision]: [rationale in one sentence]
2. [Decision]: [rationale in one sentence]

## Risks
| Risk | Impact | Mitigation |
|---|---|---|
| [risk] | High/Med/Low | [mitigation] |

## Next Steps
- [ ] Stakeholder review and approval
- [ ] Run `/feature-plan` to decompose into work packages
- [ ] Run `/feature-dev` per work package with designated roles
```

Wait for user review. The user may request changes, additional analysis, or approve.

## 8. Persist Artifacts

After approval, save deliverables to the project:

1. **ADRs** → `docs/adr/` or `docs/architecture/decisions/` (create dir if missing)
2. **Design docs** → `docs/architecture/` or `docs/design/`
3. **API contracts** → alongside existing API specs or in `docs/api/`
4. **ARCHITECTURE.md** → project root (update existing or create new)

For each file:
- Use consistent naming: `ADR-NNN-[kebab-case-title].md`, `[feature]-design.md`
- Verify file was created successfully

If the project has no established `docs/` structure — propose one and confirm with user.

## 9. Handoff

Guide the next steps based on scope:

- **Feature Design** → Run `/feature-plan` with the produced ARD and design docs as input
- **Architecture Analysis** → Share findings with stakeholders. If action items identified — create tickets or run `/feature-plan` for each initiative
- **Architecture Evolution** → Run `/feature-plan` for each migration phase

## Integration

- **Input from**: `/feature-design` (PRD output), `/feature-plan` (architecture questions during planning), direct analysis requests
- **Followed by**: `/feature-plan` (work decomposition), `/feature-dev` (implementation)
- **Roles**: `Agent(solution-architect)` (feature design, ADRs, API contracts), `Agent(system-architect)` (system analysis, ARCHITECTURE.md, component boundaries), `Agent(cloud-architect)` (cloud platform design, landing zones, networking, cost), `Agent(devops-architect)` (CI/CD architecture, deployment strategies, platform engineering)
- **Templates**: `templates/architecture.template.md` (ARCHITECTURE.md structure)
- **Skills**: `context-engineering` skill (for AI/agent system architecture)
