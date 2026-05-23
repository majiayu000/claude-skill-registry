---
name: BMAD Method
description: Business Model and Architecture Design methodology for aligning technical architecture with business model sustainability and scalability
version: 1.0.0
category: business-architecture
triggers:
  - 'bmad-method'
  - 'bmad method'
  - 'business model architecture'
  - 'business architecture design'
  - 'align architecture with business model'
dependencies:
  required_mcps: []
  required_tools: []
  required_integrations: []
---

# BMAD Method (Business Model and Architecture Design)

## Overview

The BMAD Method bridges business strategy and technical architecture. It ensures your technical decisions support long-term business sustainability, not just immediate feature delivery.

**Core Insight:** Your architecture IS your business model in code form.

## When to Use This Skill

Use BMAD when:

- Starting a new product or major architectural redesign
- Technical decisions have direct revenue/cost implications
- Scaling challenges intersect with business model constraints
- Evaluating build vs. buy for core capabilities
- Transitioning from MVP to sustainable growth
- Business model changes require architectural shifts

## Key Capabilities

- Map business model to technical architecture decisions
- Identify architectural implications of revenue models
- Design for cost sustainability at scale
- Align technology investments with business value
- Evaluate infrastructure costs vs. revenue potential
- Plan architecture evolution alongside business growth

## Workflow

### Step 1: Business Model Analysis

**Understand the Revenue Engine:**

- How does money flow? (One-time, subscription, usage-based, marketplace, advertising)
- What's the unit economics? (CAC, LTV, gross margin, payback period)
- What are the scale expectations? (10 users? 10k? 10M?)
- What's the competitive moat? (Network effects, data, tech, brand)

**Key Questions:**

- Is this B2B or B2C?
- What's the pricing model?
- What drives costs? (Infrastructure, support, sales, dev)
- What's the target gross margin?

---

### Step 2: Architecture Alignment

**Map Business Model to Architecture:**

**Subscription SaaS (B2B):**

- Multi-tenancy architecture
- Pay-as-you-grow infrastructure (starts cheap)
- Enterprise features (SSO, RBAC, audit logs)
- 99.9%+ uptime SLA requirements
- Data isolation and security compliance

**Usage-Based (API/Platform):**

- Serverless/metered infrastructure
- Rate limiting and quota management
- Detailed usage tracking and billing
- Developer experience (docs, SDKs)
- Predictable per-request costs

**Marketplace/Network:**

- Support dual-sided interactions (buyers/sellers)
- Transaction processing and escrow
- Search, matching, and discovery algorithms
- Trust and safety systems
- Commission-based cost structure

**Freemium/Consumer:**

- Scales to millions of users efficiently
- Clear free vs. paid feature boundaries
- Low marginal cost per user
- Conversion funnel optimization
- Viral/growth mechanics

---

### Step 3: Cost Modeling

**Infrastructure Cost Analysis:**

**Calculate Unit Economics:**

- Cost per user/month
- Cost per transaction
- Cost per API call
- Infrastructure overhead vs. variable costs

**Example (SaaS):**

```
Target: $20/user/month subscription

Acceptable costs:
- Infrastructure: <$2/user/month (10% COGS)
- Support: <$4/user/month (20%)
- Sales/Marketing: <$60 CAC (3-month payback)

Architecture decisions:
- Shared infrastructure (not dedicated per customer)
- Self-service onboarding (reduce sales cost)
- In-app support tools (reduce support tickets)
- Efficient database design (reduce storage costs)
```

---

### Step 4: Scalability Planning

**Design for Growth Stages:**

**Stage 1: MVP (0-100 users)**

- **Goal:** Validate product-market fit
- **Architecture:** Simple, monolithic, managed services
- **Cost:** Fixed low monthly ($100-500/month)
- **Trade-off:** Speed over scalability

**Stage 2: Growth (100-10k users)**

- **Goal:** Prove unit economics work
- **Architecture:** Modular monolith, scale vertically first
- **Cost:** Linear with users ($0.50-5/user/month)
- **Trade-off:** Optimize for margin over features

**Stage 3: Scale (10k-1M users)**

- **Goal:** Efficient scaling without rewrites
- **Architecture:** Microservices for bottlenecks, caching, CDN
- **Cost:** Sublinear growth ($0.10-1/user/month)
- **Trade-off:** Operational complexity vs. efficiency

**Stage 4: Enterprise (1M+ users)**

- **Goal:** Dominant market position
- **Architecture:** Multi-region, custom infra, dedicated teams
- **Cost:** Economies of scale (<$0.10/user/month)
- **Trade-off:** Long-term investment over short-term agility

---

### Step 5: Build vs. Buy Framework

**Evaluate Core vs. Context:**

**Build when:**

- It's your competitive differentiator
- You need specific customization
- Recurring costs exceed build cost
- You have expertise in-house
- Control/security is critical

**Buy/Use SaaS when:**

- It's commodity functionality
- Time-to-market is critical
- You lack expertise
- Maintenance burden is high
- Cost predictability matters

**Examples:**

| Capability          | Decision              | Rationale                   |
| ------------------- | --------------------- | --------------------------- |
| Payment processing  | Buy (Stripe)          | Commodity, compliance heavy |
| Core algorithm      | Build                 | Competitive moat            |
| Email delivery      | Buy (SendGrid)        | Commodity infrastructure    |
| Analytics           | Buy (Mixpanel)        | Faster than building        |
| Custom AI model     | Build                 | Unique to your data         |
| Auth infrastructure | Buy (Auth0) initially | Build later at scale        |

---

### Step 6: Business Constraints Documentation

**Capture Non-Negotiable Requirements:**

**Regulatory/Compliance:**

- GDPR, HIPAA, SOC2, PCI-DSS
- Data residency requirements
- Audit trail and retention policies

**Business Commitments:**

- SLA commitments (uptime, response time)
- Data portability guarantees
- Security certifications required
- Integration promises to customers

**Financial Constraints:**

- Burn rate and runway
- Target gross margin
- Pricing commitments made
- Investor expectations

---

## Examples

### Example 1: B2B SaaS Analytics Platform

**Business Model:**

- $99-$499/month subscription
- Target: 1,000 customers = $1.5M ARR
- Target gross margin: 80%
- Max COGS: $3/customer/month

**Architecture Decisions:**

- **Multi-tenant database** (shared PostgreSQL)
- **Serverless data processing** (AWS Lambda)
- **Managed infrastructure** (AWS RDS, S3, CloudFront)
- **No dedicated resources per customer** (kills margin)

**Build vs. Buy:**

- Build: Core analytics engine (differentiator)
- Buy: Auth (Auth0), Email (SendGrid), Support (Intercom)

**Outcome:** $2.50/customer/month COGS, 83% margin

---

### Example 2: Usage-Based API Platform

**Business Model:**

- $0.01/API call pricing
- Target: 10M calls/month = $100k MRR
- Target gross margin: 70%
- Max COGS: $0.003/call

**Architecture Decisions:**

- **Serverless architecture** (AWS Lambda + API Gateway)
- **Pay-per-use infrastructure** (no idle costs)
- **Aggressive caching** (CloudFlare + Redis)
- **Efficient algorithms** (cost per call matters)

**Build vs. Buy:**

- Build: Core API logic (differentiator)
- Buy: API gateway (AWS), CDN (CloudFlare), Monitoring (Datadog)

**Outcome:** $0.0025/call COGS, 75% margin

---

### Example 3: Consumer Marketplace

**Business Model:**

- 10% commission on transactions
- Target: $1M GMV/month = $100k revenue
- Target gross margin: 60%
- Max COGS: $40k/month

**Architecture Decisions:**

- **Scalable to millions of users** (serverless + CDN)
- **Transaction processing** (Stripe Connect)
- **Search and matching** (Algolia or Elasticsearch)
- **Low marginal cost per user** (<$0.01/user/month)

**Build vs. Buy:**

- Build: Matching algorithm (differentiator)
- Buy: Payments (Stripe), Search (Algolia), Chat (Stream)

**Outcome:** Scales to 100k users at <$35k/month

---

## Best Practices

### 1. Start with Business Model, Not Tech Stack

Don't choose React/Node/AWS first. Choose after understanding:

- Revenue model
- User scale
- Unit economics
- Margin targets

### 2. Design for Current Stage +1

Build for where you are now, but don't lock yourself out of next stage.

**Bad:** Hard-coded single-tenant that can't scale
**Good:** Multi-tenant from day 1 (even at 10 users)

### 3. Measure Infrastructure Cost Per User

If you can't calculate cost per user, you can't predict profitability.

**Track monthly:**

- AWS/GCP/Azure spend
- Third-party SaaS costs
- Divide by active users

### 4. Align Architectural Investments with Revenue

If feature doesn't drive revenue/retention, defer expensive architecture.

**Example:** Don't build multi-region before proving PMF.

### 5. Plan for Architectural Pivot Points

Know when you'll need to refactor:

- 1,000 users → Optimize database queries
- 10,000 users → Add caching layer
- 100,000 users → Microservices for bottlenecks
- 1M users → Multi-region, custom infra

---

## Common Pitfalls

### 1. Over-Engineering for Scale You Don't Have

Building for 1M users when you have 100 wastes time and money.

**Antipattern:** Microservices + Kubernetes at MVP stage
**Better:** Monolith on Railway/Heroku, scale later

### 2. Under-Engineering for Business Model

Not building multi-tenancy in B2B SaaS kills margins at scale.

**Antipattern:** Dedicated database per customer
**Better:** Multi-tenant architecture from day 1

### 3. Ignoring Unit Economics

Not tracking cost per user means surprises at scale.

**Antipattern:** "We'll figure out costs later"
**Better:** Model costs before building

### 4. Building Everything In-House

Commodities don't need custom solutions.

**Antipattern:** Build custom auth, payments, email
**Better:** Buy Stripe, Auth0, SendGrid; build differentiation

### 5. Misaligned Tech Investments

Spending on features that don't drive business value.

**Antipattern:** Perfect CI/CD before proving PMF
**Better:** Ship fast, optimize later

---

## Related Skills

- **mvp-builder** - Rapid MVP development (BMAD guides what to build)
- **product-strategist** - Product-market fit validation (BMAD aligns architecture)
- **deployment-advisor** - Infrastructure and CI/CD (BMAD sets cost targets)
- **api-designer** - API design (BMAD determines pricing model)
- **performance-optimizer** - Optimize costs at scale (BMAD identifies when to optimize)

---

## Deliverables

When using BMAD Method, produce:

1. **Business Model Canvas**
   - Revenue streams, cost structure, value proposition
   - Unit economics (CAC, LTV, margin)

2. **Architecture Alignment Document**
   - How architecture supports business model
   - Cost per user calculations
   - Scalability plan for growth stages

3. **Build vs. Buy Decision Matrix**
   - Core capabilities to build
   - Context capabilities to buy
   - Cost-benefit analysis

4. **Architectural Roadmap**
   - Current stage architecture
   - Planned refactors at scale milestones
   - Investment priorities

---

## Success Metrics

You've successfully applied BMAD when:

- Infrastructure costs are predictable and within target margins
- Architecture supports current stage without over-engineering
- Clear plan exists for next scale milestone
- Build vs. buy decisions are justified by business value
- Technical debt is strategic, not accidental
- Team understands business implications of technical choices

---

**Remember:** The best architecture is the one that makes your business model sustainable and profitable.
