---
name: decision-frameworks
model: reasoning
description: Structured decision-making patterns for common engineering choices — library selection, architecture, build vs buy, prioritization, reversibility analysis, and ADRs. Use when choosing between tools, architectures, or approaches, or when documenting technical decisions.
---

# Decision Frameworks (Meta-Skill)

Structured approaches for making engineering decisions with confidence and traceability.


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install decision-frameworks
```


---

## When to Use

- Choosing between libraries, frameworks, or tools
- Facing a build-vs-buy decision
- Selecting an architecture pattern (monolith vs microservices, SQL vs NoSQL, etc.)
- Multiple valid options exist and the team needs alignment
- Prioritizing a backlog or technical roadmap
- Documenting a significant technical decision for future reference

---

## Decision Matrix Template

Use a weighted scoring matrix when comparing 3+ options across measurable criteria.

| Criteria | Weight | Option A | Option B | Option C |
|----------------------|--------|----------|----------|----------|
| Performance | 5 | 4 (20) | 3 (15) | 5 (25) |
| Developer Experience | 4 | 5 (20) | 4 (16) | 3 (12) |
| Community Support | 3 | 5 (15) | 3 (9) | 2 (6) |
| Learning Curve | 3 | 3 (9) | 4 (12) | 2 (6) |
| Cost | 2 | 5 (10) | 3 (6) | 4 (8) |
| **Total** | | **74** | **58** | **57** |

**How to use:**

1. List criteria relevant to the decision
2. Assign weights (1-5) based on project priorities
3. Score each option per criterion (1-5)
4. Multiply score x weight, sum per option
5. Highest total wins — but sanity-check the result against gut feel

---

## Build vs Buy Framework

Follow this decision tree:

```
Is it a core differentiator for your product?
├── YES → Build it (own the competitive advantage)
└── NO
    ├── Does a mature, well-maintained solution exist?
    │   ├── YES → Buy / adopt it
    │   └── NO → Build, but keep it minimal
    └── Is the integration cost higher than building?
        ├── YES → Build
        └── NO → Buy / adopt
```

**Factor comparison:**

| Factor | Build | Buy / Adopt |
|----------------------|--------------------------------|---------------------------------|
| Maintenance cost | Ongoing — your team owns it | Vendor/community maintains it |
| Customization | Unlimited flexibility | Limited to extension points |
| Time to market | Slower — development required | Faster — ready-made |
| Team expertise | Must have or acquire skills | Abstracted away |
| Long-term cost | Scales with internal capacity | License/subscription fees |
| Vendor lock-in risk | None | Medium to high |
| Security control | Full audit capability | Dependent on vendor transparency |

---

## Library / Framework Selection

Evaluate candidate libraries against these criteria before adopting:

| Criterion | What to Check | Red Flag |
|--------------------------|----------------------------------------------------|------------------------------------|
| Maintenance activity | Commits in last 90 days, open issues trend | No commits in 6+ months |
| Community size | GitHub stars, npm weekly downloads, Discord/forum | < 1k weekly downloads for critical lib |
| Bundle size | Bundlephobia, tree-shaking support | > 50 KB gzipped for a utility lib |
| TypeScript support | Built-in types vs DefinitelyTyped, type quality | No types or outdated @types |
| Breaking change history | Changelog, semver adherence, migration guides | Frequent majors without guides |
| License | OSI-approved, compatible with your project | AGPL in a SaaS product, no license |
| Security audit | Snyk/Socket score, CVE history, dependency depth | Known unpatched CVEs |
| Documentation quality | Getting started guide, API reference, examples | README-only, no examples |

**Quick heuristic:** If you cannot replace the library within one sprint, treat the decision as a one-way door (see Reversibility Check below).

---

## Architecture Decision Framework

Use these tradeoff tables when choosing between architectural approaches.

### Monolith vs Microservices

| Factor | Monolith | Microservices |
|---------------------|----------------------------------|--------------------------------------|
| Complexity | Low at start, grows over time | High from day one |
| Deployment | Single artifact | Independent per service |
| Team scaling | Harder beyond 10-15 engineers | Enables autonomous teams |
| Data consistency | ACID transactions | Eventual consistency, sagas |
| Debugging | Single process, easy tracing | Distributed tracing required |
| Best when | Early-stage, small team, MVP | Proven domain boundaries, scale needs |

### SQL vs NoSQL

| Factor | SQL (Relational) | NoSQL (Document/Key-Value) |
|---------------------|----------------------------------|--------------------------------------|
| Schema | Strict, enforced | Flexible, schema-on-read |
| Relationships | Native joins, foreign keys | Denormalized, application-level joins |
| Scaling | Vertical (read replicas help) | Horizontal by design |
| Consistency | Strong (ACID) | Tunable (eventual to strong) |
| Query flexibility | Ad-hoc queries, aggregations | Limited to access patterns |
| Best when | Complex relations, reporting | High write volume, flexible schema |

### REST vs GraphQL

| Factor | REST | GraphQL |
|---------------------|----------------------------------|--------------------------------------|
| Simplicity | Simple, well-understood | Schema definition required |
| Over/under-fetching | Common — multiple endpoints | Clients request exact fields |
| Caching | HTTP caching built-in | Requires custom caching layer |
| Tooling | Mature ecosystem | Growing — Apollo, Relay, urql |
| Versioning | URL or header versioning | Schema evolution, deprecation |
| Best when | CRUD APIs, public APIs | Complex UIs, mobile + web clients |

### SSR vs CSR vs SSG

| Factor | SSR | CSR | SSG |
|---------------------|------------------------|------------------------|-----------------------------|
| Initial load | Fast (HTML from server) | Slow (JS bundle parse) | Fastest (pre-built HTML) |
| SEO | Excellent | Poor without hydration | Excellent |
| Best when | Personalized pages | Dashboards, SPAs | Blogs, docs, marketing |

### Monorepo vs Polyrepo

| Factor | Monorepo | Polyrepo |
|---------------------|----------------------------------|--------------------------------------|
| Code sharing | Trivial — same repo | Requires published packages |
| CI/CD complexity | Needs smart filtering (Turborepo) | Simple per-repo pipelines |
| Best when | Shared libs, aligned releases | Independent teams, different stacks |

---

## Priority Matrices — RICE Scoring

Score and rank features/tasks:

```
RICE Score = (Reach x Impact x Confidence) / Effort
```

| Factor | Scale |
|------------|--------------------------------------------------------|
| Reach | Number of users/events affected per quarter |
| Impact | 3 = massive, 2 = high, 1 = medium, 0.5 = low, 0.25 = minimal |
| Confidence | 100% = high, 80% = medium, 50% = low |
| Effort | Person-weeks (or person-sprints) |

### MoSCoW Method

| Category | Meaning | Budget Target |
|--------------|------------------------------------------------|----------------|
| **Must** | Non-negotiable for this release | ~60% of effort |
| **Should** | Important but not critical | ~20% of effort |
| **Could** | Desirable if time permits | ~15% of effort |
| **Won't** | Explicitly out of scope (this time) | ~5% (planning) |

---

## Reversibility Check

Classify every significant decision as a one-way or two-way door.

| Aspect | One-Way Door (Type 1) | Two-Way Door (Type 2) |
|------------------|-------------------------------------|-------------------------------------|
| Definition | Irreversible or very costly to undo | Easily reversed with low cost |
| Examples | Database engine migration, public API contract, language rewrite | UI framework for internal tool, feature flag experiment, library swap behind interface |
| How to identify | Would reverting require > 1 sprint of rework? Data migration? Customer communication? | Can you revert with a config change, flag toggle, or single PR? |
| Approach | Invest in analysis, prototype, get stakeholder sign-off | Decide fast, ship, measure, iterate |
| Time to decide | Days to weeks — thorough evaluation | Hours — bias toward action |

**Rule of thumb:** Wrap risky choices behind interfaces/abstractions. This converts many one-way doors into two-way doors by isolating the implementation from consumers.

---

## ADR Template

Document significant decisions using a lightweight Architecture Decision Record.

```markdown
# ADR-NNNN: [Short Title]

## Status
[Proposed | Accepted | Deprecated | Superseded by ADR-XXXX]

## Context
What is the problem or situation that motivates this decision?
Include constraints, requirements, and forces at play.

## Decision
What is the change being proposed or adopted?
State the decision clearly and concisely.

## Consequences

### Positive
- [Benefit 1]
- [Benefit 2]

### Negative
- [Tradeoff 1]
- [Tradeoff 2]

### Risks
- [Risk and mitigation]
```

Store in `docs/adr/` or `decisions/`. Number sequentially. Never delete — mark superseded. Review during onboarding and quarterly audits.

---

## Anti-Patterns

| Anti-Pattern | Description | Counter |
|--------------------------|------------------------------------------------------|---------------------------------------------|
| Analysis Paralysis | Endless evaluation, no decision made | Set a decision deadline; use the matrix |
| HiPPO | Highest Paid Person's Opinion overrides data | Require data or a scored matrix for all options |
| Sunk Cost Fallacy | Continuing because of past investment, not future value | Evaluate options as if starting fresh today |
| Bandwagon Effect | Choosing because "everyone uses it" | Score against your actual criteria |
| Premature Optimization | Optimizing before measuring or validating need | Profile first; optimize only proven bottlenecks |
| Resume-Driven Development | Picking tech to pad a resume, not to solve the problem | Align choices with team skills and project goals |
| Not Invented Here | Rejecting external solutions out of pride | Run the Build vs Buy framework honestly |

---

## NEVER Do

1. **NEVER skip writing down the decision** — undocumented decisions get relitigated endlessly
2. **NEVER decide by committee without a single owner** — assign a DRI (Directly Responsible Individual)
3. **NEVER treat all decisions as equal weight** — classify by reversibility and impact first
4. **NEVER ignore second-order effects** — ask "and then what?" at least twice
5. **NEVER lock in without an exit plan** — define how you would migrate away before committing
6. **NEVER conflate familiarity with superiority** — evaluate on criteria, not comfort
7. **NEVER defer a one-way door decision indefinitely** — the cost of delay often exceeds the cost of a wrong choice
