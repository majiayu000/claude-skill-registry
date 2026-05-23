---
name: startup-business-models
description: Revenue model design, unit economics, pricing strategy, and monetization optimization
metadata:
  version: "1.0"
---

# Startup Business Models

Systematic framework for designing, analyzing, and optimizing revenue models and unit economics.

**Modern Best Practices (Dec 2025)**:
- Use consistent metric definitions (CAC, LTV, payback, NRR) and keep a glossary.
- Model unit economics by segment/cohort; blended averages can hide failures.
- Treat pricing & packaging as a product: value metric, discount policy, upgrade triggers, enforcement.
- For usage-based models, explicitly budget variable costs (infra, third-party) and add guardrails.

---

## When to Use This Skill

Use this skill when:

- Designing or analyzing revenue models (subscription, usage-based, marketplace, freemium)
- Calculating unit economics (LTV, CAC, payback period, gross margin)
- Creating or optimizing pricing strategy and tier design
- Evaluating business model viability for investors
- Building financial models for startups
- Analyzing customer economics by segment or cohort

**Related Skills**:

- [startup-idea-validation](../startup-idea-validation/) - Validate before building
- [startup-competitive-analysis](../startup-competitive-analysis/) - Market positioning
- [startup-fundraising](../startup-fundraising/) - Investor metrics and pitch
- [startup-go-to-market](../startup-go-to-market/) - GTM strategy

---

## Decision Tree: What Business Model Analysis?

```
BUSINESS MODEL QUESTION
    │
    ├─► "How should I charge?" ────────► Revenue Model Selection
    │                                     └─► Model comparison, hybrid strategies
    │
    ├─► "What price?" ─────────────────► Pricing Strategy
    │                                     └─► Value-based, competition, willingness-to-pay
    │
    ├─► "Is it profitable?" ───────────► Unit Economics Analysis
    │                                     └─► LTV, CAC, margins, payback
    │
    ├─► "Which customers are best?" ───► Customer Economics
    │                                     └─► Segment profitability, cohorts
    │
    ├─► "How do I grow revenue?" ──────► Revenue Expansion
    │                                     └─► Upsell, cross-sell, pricing tiers
    │
    └─► "Full model design" ───────────► COMPREHENSIVE ANALYSIS
                                          └─► All dimensions
```

---

## Revenue Model Types

### Model Taxonomy

| Model | Description | Best For | Examples |
|-------|-------------|----------|----------|
| **Subscription** | Recurring fee for access | Predictable value delivery | SaaS, media, software |
| **Usage-Based** | Pay per unit consumed | Variable consumption | Cloud, API, telecom |
| **Freemium** | Free tier + paid upgrades | Network effects, low marginal cost | Slack, Dropbox, Spotify |
| **Marketplace** | Take-rate on transactions | Two-sided platforms | Uber, Airbnb, eBay |
| **Transaction** | Fee per transaction | Payment, financial services | Stripe, PayPal |
| **License** | One-time or periodic fee | Enterprise software | Microsoft, Adobe (legacy) |
| **Advertising** | Monetize attention | Scale audiences | Google, Meta, TikTok |
| **Hardware + Service** | Device + recurring service | IoT, connected products | Peloton, Nest |
| **Outcome-Based** | Pay for results | High-value, measurable outcomes | Performance marketing |

### Model Selection Framework

```
HIGH VALUE, PREDICTABLE DELIVERY
         │
         ├─► Subscription
         │
VARIABLE VALUE, VARIABLE USAGE
         │
         ├─► Usage-Based or Hybrid
         │
PLATFORM/NETWORK EFFECTS
         │
         ├─► Freemium → Upgrade
         │
TWO-SIDED MARKET
         │
         ├─► Marketplace (Take-Rate)
         │
TRANSACTION-ENABLING
         │
         └─► Transaction Fees
```

### Hybrid Models (2024-2025 Trend)

| Hybrid | Components | Examples |
|--------|------------|----------|
| Subscription + Usage | Base fee + overage | AWS, Twilio |
| Freemium + Usage | Free tier + usage-based premium | OpenAI API |
| Subscription + Transaction | Platform fee + take-rate | Shopify |
| Outcome + Subscription | Base + success fee | Performance agencies |

---

## Unit Economics Framework

### Core Metrics

| Metric | Formula | Target | Notes |
|--------|---------|--------|-------|
| **LTV** | ARPU × Gross Margin × (1 / Churn Rate) | 3x+ CAC | Lifetime customer value |
| **CAC** | Sales & Marketing Spend / New Customers | LTV/3 | Customer acquisition cost |
| **LTV:CAC** | LTV / CAC | >3:1 | Efficiency ratio |
| **Payback** | CAC / (ARPU × Gross Margin) | <12 months | Months to recover CAC |
| **Gross Margin** | (Revenue - COGS) / Revenue | >70% (SaaS) | Profitability per unit |
| **Net Revenue Retention** | (Starting MRR + Expansion - Churn) / Starting MRR | >100% | Growth from existing |
| **Churn Rate** | Lost Customers / Total Customers | <5% annual | Customer retention |

### LTV Calculation Methods

**Simple LTV**:
```
LTV = ARPU × Average Customer Lifetime

Where: Average Customer Lifetime = 1 / Monthly Churn Rate
```

**Margin-Adjusted LTV**:
```
LTV = ARPU × Gross Margin × (1 / Churn Rate)
```

**Cohort-Based LTV** (Most Accurate):
```
LTV = Σ (Revenue per Cohort Month × Retention Rate at Month)
```

### CAC Calculation

**Fully-Loaded CAC**:
```
CAC = (Sales Salaries + Marketing Spend + Sales Tools +
       Marketing Tools + Content + Events + Agency Fees) /
       New Customers Acquired
```

**By Channel**:
| Channel | Spend | Customers | CAC |
|---------|-------|-----------|-----|
| Paid Search | $X | N | $X |
| Content/SEO | $X | N | $X |
| Sales Outbound | $X | N | $X |
| Referral | $X | N | $X |
| **Blended** | $X | N | $X |

### Unit Economics by Stage

| Stage | LTV:CAC | Payback | Focus |
|-------|---------|---------|-------|
| Pre-PMF | N/A | N/A | Finding product-market fit |
| Early | 1-2x | 18-24 mo | Proving unit economics work |
| Growth | 3-4x | 12-18 mo | Scaling efficiently |
| Scale | 4-5x+ | <12 mo | Optimizing profitability |

---

## Pricing Strategy

### Pricing Approaches

| Approach | Method | When to Use |
|----------|--------|-------------|
| **Value-Based** | Price = % of customer value | B2B, clear ROI |
| **Competition-Based** | Price relative to alternatives | Commoditized markets |
| **Cost-Plus** | Cost + target margin | Low differentiation |
| **Willingness-to-Pay** | Research-based WTP | New markets, no reference |

### Value-Based Pricing Framework

```
1. QUANTIFY CUSTOMER VALUE
   └─► What's the $ impact of your solution?

2. IDENTIFY VALUE DRIVERS
   └─► Time saved? Revenue gained? Cost reduced?

3. SET PRICE AS % OF VALUE
   └─► Typically 10-30% of quantified value

4. VALIDATE WITH CUSTOMERS
   └─► Willingness-to-pay research
```

### Pricing Tiers Design

| Element | Free | Starter | Pro | Enterprise |
|---------|------|---------|-----|------------|
| **Target** | Individuals | Small teams | Growth teams | Large orgs |
| **Price** | $0 | $X/mo | $X/mo | Custom |
| **Limits** | X users, Y usage | X users, Y usage | X users, Y usage | Unlimited |
| **Features** | Core only | Core + Basic | Core + Advanced | All + Custom |
| **Support** | Community | Email | Priority | Dedicated |
| **Billing** | — | Monthly/Annual | Monthly/Annual | Annual |

### Pricing Levers

| Lever | Options | Considerations |
|-------|---------|----------------|
| **Metric** | Per seat, per usage, flat | Align with value delivery |
| **Frequency** | Monthly, annual, one-time | Cash flow vs. commitment |
| **Discounts** | Volume, annual, startup | Incentive alignment |
| **Bundling** | All-in-one vs. à la carte | Simplicity vs. customization |
| **Anchoring** | Show expensive option first | Psychological pricing |

### Willingness-to-Pay Research

**Van Westendorp Method** (Price Sensitivity Meter):

| Question | Purpose |
|----------|---------|
| "At what price is this too expensive?" | Upper bound |
| "At what price is this expensive but acceptable?" | Premium threshold |
| "At what price is this a bargain?" | Value perception |
| "At what price is this too cheap (suspicious)?" | Lower bound |

**Gabor-Granger Method**:
```
1. Show product at price point A
2. "Would you buy at this price?" Y/N
3. If Yes → Show higher price
4. If No → Show lower price
5. Repeat to find demand curve
```

---

## SaaS Metrics Deep Dive

### MRR Components

| Component | Definition | Formula |
|-----------|------------|---------|
| **New MRR** | From new customers | Sum(New Customer MRR) |
| **Expansion MRR** | Upgrades + add-ons | Sum(Upsell + Cross-sell) |
| **Contraction MRR** | Downgrades | Sum(Downgrade MRR) |
| **Churn MRR** | Lost customers | Sum(Churned Customer MRR) |
| **Net New MRR** | Monthly change | New + Expansion - Contraction - Churn |

### Cohort Analysis Template

| Cohort | M0 | M1 | M2 | M3 | M6 | M12 |
|--------|-----|-----|-----|-----|-----|------|
| Jan 2024 | 100% | 95% | 90% | 88% | 82% | 75% |
| Feb 2024 | 100% | 93% | 88% | 85% | 80% | — |
| Mar 2024 | 100% | 94% | 89% | 86% | — | — |

### Net Revenue Retention (NRR)

```
NRR = (Starting MRR + Expansion - Contraction - Churn) / Starting MRR × 100%

Benchmarks:
- <100%: Leaky bucket (fix churn first)
- 100-110%: Healthy
- 110-120%: Strong
- >120%: Exceptional (enterprise, land-and-expand)
```

---

## Marketplace Economics

### Key Marketplace Metrics

| Metric | Formula | Benchmark |
|--------|---------|-----------|
| **GMV** | Total transaction value | Growth rate |
| **Take Rate** | Revenue / GMV | 5-30% |
| **Liquidity** | Successful transactions / Attempts | >80% |
| **CAC Supply** | Cost to acquire seller/provider | — |
| **CAC Demand** | Cost to acquire buyer/consumer | — |
| **ARPU** | Revenue per active user | — |

### Take Rate by Category

| Category | Typical Take Rate | Notes |
|----------|-------------------|-------|
| Rideshare | 20-30% | High service component |
| E-commerce | 10-15% | Logistics adds value |
| Services | 15-25% | Trust/vetting value |
| B2B | 5-15% | Lower, higher volume |
| Digital goods | 15-30% | No physical logistics |

### Marketplace Unit Economics

```
Buyer Side:
LTV = Transactions/Year × AOV × Take Rate × Retention Years

Seller Side:
LTV = GMV/Year × Take Rate × Retention Years

Combined:
Platform LTV = Buyer LTV + Seller LTV - Cross-Subsidization
```

---

## Revenue Expansion Strategies

### Expansion Revenue Levers

| Lever | Mechanism | Example |
|-------|-----------|---------|
| **Seat Expansion** | More users in org | Slack per-user pricing |
| **Usage Growth** | Natural consumption increase | AWS compute |
| **Tier Upgrade** | Move to higher plan | Free → Pro → Enterprise |
| **Add-on Sales** | Complementary products | Salesforce add-ons |
| **Cross-sell** | Related products | HubSpot suite |
| **Price Increase** | Annual adjustments | Annual price escalators |

### Land and Expand Framework

```
LAND (Initial Deal)
    │
    └─► Small team, specific use case, low ACV
                │
                ▼
ADOPT (Prove Value)
    │
    └─► Usage growth, success metrics, champions
                │
                ▼
EXPAND (Grow Account)
    │
    └─► More users, departments, use cases
                │
                ▼
STRATEGIC (Enterprise Deal)
    │
    └─► Company-wide, multi-year, executive sponsor
```

### Expansion Triggers

| Trigger | Signal | Action |
|---------|--------|--------|
| Usage hitting limits | 80%+ of tier limits | Proactive upgrade offer |
| New use case request | Feature request in adjacent area | Cross-sell motion |
| Team growth | New users being added | Seat expansion |
| Success metrics | Strong ROI demonstrated | Enterprise pitch |
| Contract renewal | 90 days before renewal | Annual review, expansion conversation |

---

## Model Comparison Framework

### Decision Matrix

| Factor | Subscription | Usage-Based | Freemium | Marketplace |
|--------|--------------|-------------|----------|-------------|
| **Predictability** | High | Low | Medium | Medium |
| **Scalability** | Medium | High | High | High |
| **Stickiness** | High | Low | Medium | High |
| **Sales complexity** | Medium | High | Low | Medium |
| **PMF signal** | Renewal | Usage | Conversion | Liquidity |
| **Best for stage** | Post-PMF | Scale | Pre-PMF | Platform |

### Revenue Model Scorecard

| Criterion | Weight | Model A | Model B | Model C |
|-----------|--------|---------|---------|---------|
| Customer alignment | 25% | | | |
| Predictability | 20% | | | |
| Scalability | 20% | | | |
| Competitive positioning | 15% | | | |
| Implementation complexity | 10% | | | |
| Expansion potential | 10% | | | |
| **Weighted Score** | 100% | | | |

---

## Resources

| Resource | Purpose |
|----------|---------|
| [unit-economics-calculator.md](resources/unit-economics-calculator.md) | LTV, CAC, payback calculations |
| [pricing-research-guide.md](resources/pricing-research-guide.md) | WTP research methodology |
| [saas-metrics-playbook.md](resources/saas-metrics-playbook.md) | SaaS-specific metrics deep dive |

## Templates

| Template | Purpose |
|----------|---------|
| [business-model-canvas.md](templates/business-model-canvas.md) | Full model design |
| [unit-economics-worksheet.md](templates/unit-economics-worksheet.md) | Calculate and track metrics |
| [pricing-tier-design.md](templates/pricing-tier-design.md) | Pricing & packaging worksheet |

## Data

| File | Purpose |
|------|---------|
| [sources.json](data/sources.json) | Business model resources |

---

## Do / Avoid (Dec 2025)

### Do

- Define your value metric (seat/usage/outcome) and validate willingness-to-pay early.
- Include COGS drivers in pricing decisions (especially usage-based).
- Use discount guardrails and renewal logic (avoid ad-hoc deals).

### Avoid

- Pricing as an afterthought (“we’ll figure it out later”).
- Margin blindness (shipping usage growth that destroys gross margin).
- Misleading LTV calculations from immature cohorts.

## What Good Looks Like

- Packaging: a clear value metric, tier logic, and discount policy (with enforcement rules).
- Unit economics: CAC, gross margin, churn, payback, and retention defined and tied to cohorts.
- Assumptions: one inputs sheet, ranges/sensitivities, and scenarios (base/best/worst).
- Experiments: pricing changes tested with decision rules (not “gut feel” rollouts).
- Risks: margin compression, adverse selection, channel conflict, and support cost modeled.

## Optional: AI / Automation

Use only when explicitly requested and policy-compliant.

- Summarize pricing research and competitor snapshots; verify manually before acting.
- Draft pricing page copy; humans verify claims and consistency with contracts.
