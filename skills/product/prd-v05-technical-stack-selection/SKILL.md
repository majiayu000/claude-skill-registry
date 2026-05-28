---
name: prd-v05-technical-stack-selection
description: Determine technologies needed to build the product, making build/buy/integrate decisions during PRD v0.5 Red Team Review. Triggers on requests to select tech stack, evaluate technologies, make build vs. buy decisions, or when user asks "what technologies?", "select tech stack", "build or buy?", "technical decisions", "what tools do we need?", "evaluate solutions". Consumes FEA- (features), SCR- (screens), RISK- (constraints). Outputs TECH- entries with decisions, rationale, and trade-offs. Feeds v0.6 Architecture Design.
---

# Technical Stack Selection

Position in workflow: v0.5 Risk Discovery Interview → **v0.5 Technical Stack Selection** → v0.6 Architecture Design

Technical stack selection is about making **build/buy/integrate/research** decisions for every technical capability your product needs.

## Decision Categories

| Category | Definition | When to Choose |
|----------|------------|----------------|
| **Build** | Create custom solution | Core differentiator, no good alternatives, full control needed |
| **Buy** | Use paid service/tool | Commodity capability, proven solutions exist, not a differentiator |
| **Integrate** | Connect to existing platform | Ecosystem play, user expects it, data lives elsewhere |
| **Research** | Need POC before deciding | High uncertainty, multiple viable options, significant commitment |

**Rule**: Default to Buy for everything that isn't a core differentiator. Build only when you must.

## Technology Layers to Address

For each layer, decide Build/Buy/Integrate/Research:

| Layer | Questions to Answer | Common Options |
|-------|---------------------|----------------|
| **Frontend** | Framework? Hosting? Mobile/Web? | React, Vue, Next.js, Vercel |
| **Backend** | Language? Framework? Serverless? | Node, Python, Go, AWS Lambda |
| **Database** | SQL/NoSQL? Managed? | PostgreSQL, MongoDB, Supabase |
| **Auth** | Build or buy? SSO? | Auth0, Clerk, Firebase Auth |
| **Payments** | If monetized, processor? | Stripe, Paddle, LemonSqueezy |
| **Infrastructure** | Cloud? Edge? CDN? | AWS, GCP, Vercel, Cloudflare |
| **Integrations** | External services? APIs? | Depends on product |
| **AI/ML** | Models? Services? | OpenAI, Anthropic, local models |
| **Analytics** | Product analytics? Error tracking? | Mixpanel, PostHog, Sentry |
| **DevOps** | CI/CD? Monitoring? | GitHub Actions, Datadog |

## Decision Process

1. **Inventory needs** from FEA- (features) and SCR- (screens)
   - What technical capabilities are required?

2. **Check RISK- constraints**
   - Do any risks constrain technology choices?
   - Performance? Security? Compliance?

3. **Categorize each need**: Build | Buy | Integrate | Research
   - Use decision framework below

4. **Research specific options** for Buy/Integrate
   - Evaluate against criteria

5. **Define research scope** for Research items
   - What must be learned? By when?

6. **Create TECH- entries** with full rationale

## Build vs. Buy Decision Framework

| Factor | Favors Build | Favors Buy |
|--------|--------------|------------|
| **Differentiation** | Core to your value prop | Commodity capability |
| **Control** | Must customize extensively | Standard behavior acceptable |
| **Expertise** | Team has deep knowledge | Team would need to learn |
| **Timeline** | Can invest time now | Need it working immediately |
| **Cost** | Long-term cost lower | Reasonable SaaS pricing |
| **Maintenance** | Willing to own forever | Want vendor to maintain |

**Strong Build signals:**
- "This is why users choose us over competitors"
- "No existing solution fits our specific need"
- "We need to change this weekly based on learning"

**Strong Buy signals:**
- "Every SaaS product needs this"
- "Multiple proven solutions exist"
- "We'd just be recreating what vendors already built"

## TECH- Output Template

```
TECH-XXX: [Technology/Capability Name]
Category: [Build | Buy | Integrate | Research]
Layer: [Frontend | Backend | Database | Auth | Payments | Infrastructure | Integrations | AI/ML | Analytics | DevOps]
Purpose: [What problem this solves]

Features Served: [FEA-XXX, FEA-YYY]
Screens Affected: [SCR-XXX, SCR-YYY]
Risk Constraints: [RISK-XXX that influenced this]

Decision: [Specific choice made]
Rationale: [Why this choice over alternatives]
Alternatives Considered:
  - [Option A]: [Why rejected]
  - [Option B]: [Why rejected]

Trade-offs:
  - Pro: [Advantage]
  - Con: [Disadvantage]

Cost: [Pricing model, estimated monthly cost]
Integration Complexity: [Low | Medium | High]
Lock-in Risk: [Low | Medium | High]

Research Needed: [If Category = Research]
Evaluation Criteria: [How to decide]
Decision Deadline: [When we must decide]
```

**Example TECH- entry (Buy):**
```
TECH-001: Authentication Service
Category: Buy
Layer: Auth
Purpose: User authentication, session management, social login

Features Served: FEA-010 (login), FEA-011 (signup), FEA-012 (social auth)
Screens Affected: SCR-000 (login), SCR-001 (signup), SCR-010 (settings)
Risk Constraints: RISK-008 (security compliance requirement)

Decision: Clerk
Rationale: Best DX for Next.js, includes social login, compliant
Alternatives Considered:
  - Auth0: Higher price at scale, more complex setup
  - Firebase Auth: Google ecosystem lock-in, less polished
  - Build custom: Would take 2+ weeks, security risk

Trade-offs:
  - Pro: <1 day integration, battle-tested security
  - Con: Vendor dependency, per-MAU pricing at scale

Cost: Free tier sufficient for MVP, ~$25/mo at 1K MAU
Integration Complexity: Low
Lock-in Risk: Medium (user data exportable, but migration work)
```

**Example TECH- entry (Research):**
```
TECH-005: Vector Database for Semantic Search
Category: Research
Layer: Database
Purpose: Store and query embeddings for AI-powered search

Features Served: FEA-025 (semantic search)
Screens Affected: SCR-008 (search results)
Risk Constraints: RISK-012 (query latency <200ms requirement)

Decision: TBD after POC
Rationale: Multiple viable options with different trade-offs
Alternatives to Evaluate:
  - Pinecone: Managed, easy setup, higher cost
  - Weaviate: Self-hosted option, more control
  - pgvector: Uses existing Postgres, simpler stack

Research Needed:
  - Latency benchmark with 1M vectors
  - Cost projection at 10M vectors
  - Query accuracy comparison

Evaluation Criteria:
  - P99 latency < 200ms
  - Cost < $500/mo at scale
  - Supports metadata filtering

Decision Deadline: End of EPIC-02
```

## Evaluation Criteria for Buy/Integrate

| Criterion | Questions to Ask |
|-----------|------------------|
| **Fit** | Does it solve our specific need? Any feature gaps? |
| **Cost** | What's the pricing model? Cost at 10x scale? |
| **Complexity** | How hard to integrate? Ongoing maintenance? |
| **Lock-in** | How hard to switch later? Data export? |
| **Maturity** | Production-ready? Good documentation? Active development? |
| **Support** | What help is available? Response time? |

## Anti-Patterns to Avoid

| Anti-Pattern | Signal | Fix |
|--------------|--------|-----|
| **Resume-driven development** | "Let's use [hot new tech]" | Choose boring technology for non-differentiators |
| **Build everything** | No Buy/Integrate decisions | Challenge: is this really a differentiator? |
| **Buy everything** | No Build decisions | Some things must be custom for your moat |
| **Analysis paralysis** | Research everything | Time-box research; decide with 70% confidence |
| **Ignoring constraints** | Tech choice conflicts with RISK- | Review RISK- before finalizing |
| **Cost blindness** | No cost estimates | Every TECH- needs cost projection |
| **Premature optimization** | "We need Kubernetes for scale" | Design for 10x current needs, not 1000x |

## Quality Gates

Before proceeding to Architecture Design:

- [ ] All technology layers addressed
- [ ] Build decisions justified as differentiators
- [ ] Buy decisions have cost estimates
- [ ] Research items have clear criteria and deadlines
- [ ] RISK- constraints reflected in choices
- [ ] No obvious vendor lock-in without acknowledgment

## Downstream Connections

TECH- entries feed into:

| Consumer | What It Uses | Example |
|----------|--------------|---------|
| **v0.6 Architecture Design** | TECH- selections define the system | TECH-001 (Next.js) → frontend architecture |
| **v0.6 Technical Specification** | TECH- informs API design | TECH-003 (Supabase) → data model constraints |
| **v0.7 Build Execution** | TECH- Research items become spikes | TECH-005 (Research) → EPIC-02 spike task |
| **Hiring/Resourcing** | TECH- Build items define skills | TECH-010 (custom ML) → need ML engineer |

## Detailed References

- **Tech stack examples by product type**: See `references/examples.md`
- **TECH- entry template**: See `assets/tech.md`
- **Evaluation scorecard**: See `assets/evaluation-scorecard.md`
