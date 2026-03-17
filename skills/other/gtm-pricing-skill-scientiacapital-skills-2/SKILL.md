---
name: "gtm-pricing"
description: "B2B go-to-market strategy, pricing models, ICP development, positioning, and competitive intelligence. Use when planning GTM strategy, setting pricing, defining ICP, or evaluating opportunities."
---

<objective>
Comprehensive B2B go-to-market framework covering ICP development (firmographics, technographics, psychographics), positioning (April Dunford canvas), pricing strategy (value-based, tiered, feature gating), and opportunity evaluation (scoring, red flags, complexity levels).
</objective>

<quick_start>
**ICP scoring:** 80+ = Ideal | 60-79 = Good | 40-59 = Marginal | <40 = Pass

**Positioning statement:**
```
For [target] who [need], [product] is a [category] that [benefit].
Unlike [alternative], our product [differentiator].
```

**Value-based pricing:** Price at 10-20% of quantified value delivered

**Opportunity score:** /100 across Market Fit, Technical Fit, GTM Fit, Personal Fit, Economics
</quick_start>

<success_criteria>
GTM strategy is successful when:
- ICP documented with scoring criteria (firmographics, technographics, psychographics)
- Positioning statement follows April Dunford framework
- Pricing anchored to quantified value (not cost-plus)
- Tier structure follows Good/Better/Best with clear feature gates
- Opportunity scoring identifies red flags and good signals
- Battle cards created for top 3 competitors
- Launch checklist completed (pre-launch, launch, post-launch)
</success_criteria>

<core_content>
Comprehensive guide for B2B go-to-market strategy, pricing, and opportunity evaluation.

## Quick Reference

| Framework | Purpose | When to Use |
|-----------|---------|-------------|
| ICP Development | Define ideal customer | Before any outreach |
| Positioning | Differentiate in market | Product launch, pivot |
| Messaging Hierarchy | Consistent communication | Sales enablement |
| Competitive Intel | Understand landscape | Deal strategy, positioning |
| Value-Based Pricing | Price by value delivered | Setting initial prices |
| Tier Structure | Package offering | Feature gating decisions |
| Opportunity Scoring | Evaluate fit | New client/project decisions |

---

## Part 1: Go-To-Market Strategy

### ICP Development Framework

#### Three Dimensions of ICP

```yaml
icp_framework:
  firmographics:
    - company_size: "50-500 employees"
    - revenue_range: "$10M-$100M ARR"
    - industry: ["Primary vertical", "Secondary vertical"]
    - geography: "North America"
    - growth_stage: "Series A-C or profitable"

  technographics:
    - current_stack: ["CRM", "ERP", "Industry tools"]
    - tech_maturity: "Mid - has CRM, considering automation"
    - integration_needs: ["ERP", "Accounting", "Field Service"]
    - cloud_adoption: "Hybrid or cloud-first"

  psychographics:
    - pain_awareness: "Problem-aware, solution-seeking"
    - change_readiness: "Has budget, executive sponsor"
    - buying_process: "Committee (3-5 stakeholders)"
    - risk_tolerance: "Moderate - needs proof points"
```

#### ICP Scoring Template

| Criterion | Weight | Score (1-5) | Weighted |
|-----------|--------|-------------|----------|
| Company size fit | 20% | | |
| Industry match | 20% | | |
| Tech stack compatibility | 15% | | |
| Pain point alignment | 25% | | |
| Budget availability | 20% | | |
| **Total** | 100% | | |

**Tiers**: 80+ = Ideal | 60-79 = Good Fit | 40-59 = Marginal | <40 = Poor Fit

### Positioning Framework

#### April Dunford's Positioning Canvas

```markdown
## [Product] Positioning Statement

**Competitive Alternatives**: What would customers use if we didn't exist?
> [List 2-3 alternatives]

**Unique Attributes**: What do we have that alternatives don't?
> [List differentiators]

**Value**: What capability do those attributes enable?
> [Translate features to benefits]

**Target Customers**: Who cares most about this value?
> [Specific customer characteristics]

**Market Category**: What context makes our value obvious?
> [Category or create new one]
```

#### Positioning Statement Template

```
For [target customer] who [statement of need],
[product name] is a [market category]
that [key benefit/differentiation].
Unlike [competitive alternative],
our product [primary differentiator].
```

### Messaging Hierarchy

```
Level 1: Strategic Narrative (Company)
├── Who we are
├── What we believe
└── Why we exist

Level 2: Solution Messaging (Product)
├── What it does
├── Key differentiators (3 max)
└── Proof points

Level 3: Persona Messaging (Audience)
├── Pain points by role
├── Value props by role
└── Objection handling by role
```

#### Persona Messaging Matrix

| Persona | Pain Points | Value Props | Proof Points |
|---------|-------------|-------------|--------------|
| CFO | Cost visibility, compliance | ROI, audit trail | Case study: 30% savings |
| Ops Director | Manual processes, errors | Automation, accuracy | Demo: 10x faster |
| End User | Clunky tools, training | Easy to use, mobile | G2 reviews: 4.8/5 |

### Competitive Intelligence

#### Battle Card Structure

```markdown
## Competitor: [Name]

### Overview
- Founded: YYYY | HQ: Location | Funding: $XXM
- Target market: [description]
- Pricing: [model and range]

### Strengths (acknowledge honestly)
- [Strength 1]
- [Strength 2]

### Weaknesses (our opportunities)
- [Weakness 1 -> our advantage]
- [Weakness 2 -> our advantage]

### Common Objections When We Compete
| Objection | Response |
|-----------|----------|
| "They're cheaper" | [Value-based response] |
| "They have feature X" | [Alternative or roadmap] |

### Win Strategy
1. Lead with [differentiator]
2. Demonstrate [proof point]
3. Reference [customer story]
```

### Channel Strategy

#### GTM Motion Selection

| Motion | Best For | CAC | Sales Cycle | Team |
|--------|----------|-----|-------------|------|
| Product-Led | Low ACV (<$5K), self-serve | Low | Days | Growth |
| Sales-Assisted | Mid ACV ($5-50K) | Medium | Weeks | SDR+AE |
| Enterprise | High ACV ($50K+) | High | Months | AE+SE |
| Partner/Channel | Geographic expansion | Variable | Variable | Partner Mgr |

### Launch Playbook Checklist

```markdown
## Pre-Launch (T-30 days)
- [ ] ICP documented and validated
- [ ] Positioning finalized
- [ ] Messaging hierarchy complete
- [ ] Battle cards created
- [ ] Sales enablement materials ready
- [ ] Pricing approved

## Launch Week
- [ ] Press release distributed
- [ ] Website updated
- [ ] Sales team trained
- [ ] Customer references lined up
- [ ] Outbound sequences activated

## Post-Launch (T+30 days)
- [ ] Win/loss analysis started
- [ ] Messaging refinement based on feedback
- [ ] Pipeline review
- [ ] Competitive response documented
```

---

## Part 2: Pricing Strategy

### Pricing Models Overview

| Pricing Model | Best For | Complexity |
|---------------|----------|------------|
| Flat rate | Simple products | Low |
| Per seat | Team collaboration tools | Medium |
| Usage-based | APIs, infrastructure | High |
| Tiered | Feature differentiation | Medium |
| Hybrid | Enterprise SaaS | High |

### Value-Based Pricing Process

```yaml
value_pricing_steps:
  1_understand_value:
    - "What problem does this solve?"
    - "What's the cost of the problem?"
    - "What's the value of the solution?"

  2_quantify_value:
    - "Time saved x hourly rate"
    - "Revenue increased"
    - "Costs avoided"
    - "Risk mitigated"

  3_capture_value:
    - "Price at 10-20% of value delivered"
    - "Anchor to alternatives"
    - "Leave money on table for adoption"

  4_communicate_value:
    - "ROI calculators"
    - "Case studies with numbers"
    - "Value-based proposals"
```

### Value Calculation Template

```markdown
## Value Calculation: [Product/Service]

### Time Savings
- Hours saved per week: __
- Hourly rate of user: $__
- Weekly savings: $__
- Annual savings: $__

### Revenue Impact
- Additional deals/month: __
- Average deal value: $__
- Monthly revenue increase: $__
- Annual revenue increase: $__

### Cost Avoidance
- Errors prevented: __
- Cost per error: $__
- Annual savings: $__

### Total Annual Value: $__

### Suggested Price Point
- 10% of value: $__/year
- 15% of value: $__/year
- 20% of value: $__/year
```

### Tiered Pricing Structure

#### Good/Better/Best Framework

```markdown
## Tier Structure

### Good (Entry)
**Price**: $X/month
**Target**: [Entry segment]
**Core value**: [Primary use case]
**Limitations**: [What's not included]

### Better (Growth) <- ANCHOR
**Price**: $Y/month (most popular)
**Target**: [Primary segment]
**Core value**: [Expanded use cases]
**Includes**: Everything in Good, plus:
- [Feature 1]
- [Feature 2]
- [Feature 3]

### Best (Scale)
**Price**: $Z/month or Custom
**Target**: [Enterprise segment]
**Core value**: [Full platform]
**Includes**: Everything in Better, plus:
- [Advanced feature 1]
- [Advanced feature 2]
- [Enterprise requirements]
```

### Feature Gating Strategy

```yaml
feature_gating:
  gate_by_scale:
    - "Number of users"
    - "Number of projects"
    - "API calls"
    - "Storage"

  gate_by_sophistication:
    - "Advanced features in higher tiers"
    - "Integrations at higher tiers"
    - "Automation at higher tiers"

  gate_by_control:
    - "Admin controls"
    - "SSO/SAML"
    - "Audit logs"
    - "Custom roles"

  never_gate:
    - "Security features"
    - "Core functionality"
    - "Data export"
```

### Pricing Psychology

```yaml
pricing_psychology:
  anchoring:
    principle: "First price seen influences perception"
    application: "Show enterprise tier first, or '60% choose Pro'"

  decoy_effect:
    principle: "Irrelevant option changes preference"
    application: "Add tier that makes target tier look good"

  price_ending:
    principle: "9s feel like deals, 0s feel premium"
    application: "$99 for SMB, $100 for enterprise"

  bundling:
    principle: "Bundles feel like better value"
    application: "Package features vs. selling a la carte"

  annual_discount:
    principle: "Upfront commitment = better terms"
    application: "20% discount for annual (2 months free)"
```

### Discounting Strategy

```yaml
discount_types:
  volume:
    trigger: "Commitment to scale"
    range: "10-30%"
    example: "20% off for 100+ seats"

  term:
    trigger: "Annual commitment"
    range: "15-25%"
    example: "2 months free on annual"

  competitive:
    trigger: "Switching from competitor"
    range: "20-40%"
    example: "Match remaining contract"

  strategic:
    trigger: "Reference customer, logo value"
    range: "Up to 50%"
    example: "Name brand + case study"
```

#### When NOT to Discount

- Customer hasn't articulated value
- No competitive pressure
- Early in negotiation
- Customer is price shopping
- Deal doesn't meet minimum size

**Alternatives to Discounting:**
- Extended payment terms
- Additional services/training
- Extended trial
- Success milestones unlock features
- Multi-year lock-in

---

## Part 3: Opportunity Evaluation

### Brainstorming Lens

I'm a sounding board, not a scorecard. I'll help you:
- Think out loud about what excites you (and what doesn't)
- Spot patterns you might be missing
- Ask the uncomfortable questions early
- Explore angles you haven't considered

### Key Evaluation Angles

#### For Project Ideas

| Angle | What to Consider |
|-------|------------------|
| Excitement | What specifically pulls you toward this? |
| Fit | Does this build on what you're already doing? |
| Effort | What would this actually take to build/ship? |
| Learning | What new skills or knowledge would you gain? |
| Alternatives | What else could you do with this time/energy? |
| Worst Case | If this totally fails, what happens? |

#### For Potential Clients/Customers

| Angle | What to Consider |
|-------|------------------|
| Fit | Are they your kind of customer? |
| Red Flags | Anything that makes you pause? |
| Relationship | How did they find you? Who referred them? |
| Budget | Can they actually pay for what they need? |
| Scope | Is this a one-off or could it grow? |
| Exit | How easy would it be to part ways if needed? |

#### For Partnerships/Collaborations

| Angle | What to Consider |
|-------|------------------|
| Alignment | Do you want the same things? |
| Contribution | What does each side bring? |
| Dependencies | What happens if they don't deliver? |
| Upside | What does success look like for you specifically? |
| Downside | What's the realistic worst case? |
| Track Record | Have they done this before? |

### Quick Opportunity Score

| Section | Points | Weight |
|---------|--------|--------|
| Market Fit | /25 | Problem clarity, market size, timing |
| Technical Fit | /20 | Can build it, infrastructure, maintenance |
| GTM Fit | /20 | Sales complexity, channel access, competition |
| Personal Fit | /20 | Interest, growth, lifestyle |
| Economics | /15 | Revenue potential, time to revenue, risk/reward |
| **Total** | /100 | |

**Interpretation:**
- 80-100: **STRONG PURSUE** - Prioritize this
- 60-79: **EXPLORE** - Worth time investment
- 40-59: **CONDITIONAL** - Only if specific factor changes
- 0-39: **PASS** - Opportunity cost too high

### Red Flags to Watch

These aren't deal-breakers, but point them out:
- Unclear who's paying or how
- Scope that keeps expanding before you start
- "We'll figure out the details later" on important things
- Pressure to decide quickly without good reason
- Misalignment between what they say and what they do
- You're more excited than they are
- The economics don't make sense even optimistically

### Good Signals

- Clear problem with clear customer
- Builds on what you already know/have
- You'd do a version of this anyway
- The timing makes sense for you
- Reasonable worst case
- Good people involved
- Learning opportunity even if it fails

### GTM Complexity Levels

| Level | Buyer | ACV | Cycle | Solo Fit |
|-------|-------|-----|-------|----------|
| 1: PLG | Individual | <$2K | Days | Excellent |
| 2: Low-Touch | Manager | $2-15K | 1-4 weeks | Excellent |
| 3: Mid-Market | Director/VP | $15-100K | 1-3 months | Good |
| 4: Enterprise | C-suite | $100K-1M | 6-18 months | Moderate |
| 5: Complex | Board | $1M+ | 12-36 months | Low |

---

## Reference Files

- `reference/gtm.md` - ICP templates, launch playbooks, channel strategy
- `reference/pricing.md` - Models, value-based pricing, psychology
- `reference/opportunity.md` - Scoring, unit economics, complexity
