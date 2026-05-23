---
name: "sales-revenue"
description: "B2B sales - cold outreach, lead scoring, pipeline metrics, MEDDIC/BANT qualification, discovery calls, demos, objection handling. Use when: cold email, lead scoring, pipeline, forecast, discovery call, demo, MEDDIC, BANT, CAC, LTV, win rate, sales metrics, outreach sequence."
---

# Sales & Revenue Skill

Comprehensive B2B sales skill: outreach, revenue operations, and demo execution.

## Quick Reference

| Domain | Key Components | Reference File |
|--------|---------------|----------------|
| **Outreach** | Cold email, sequences, domain warming, lead scoring | `reference/outreach.md` |
| **Revenue Ops** | Pipeline metrics, forecasting, dashboards, attribution | `reference/revenue-ops.md` |
| **Discovery** | MEDDIC, SPIN, demo flow, objection handling | `reference/discovery.md` |

---

## Part 1: Sales Outreach

### The GTM Pipeline

```
Lead Scraping → Lead Scoring → Domain Warming → Sequences → Reply Detection
     ↓              ↓              ↓               ↓             ↓
 dealer-scraper  sales-agent   cold-reach     cold-reach    sales-agent
```

### Lead Tiering

| Tier | Criteria | Priority | Action |
|------|----------|----------|--------|
| GOLD | Multi-trade, $5-50M, website, reviews | Immediate | Personalized sequence |
| SILVER | Single trade, has reviews or website | Week 1 | Standard sequence |
| BRONZE | Basic listing only | Nurture | Drip campaign |

### Lead Scoring (0-100)

```python
scoring_factors = {
    'icp_fit': 0-30,        # Match to ideal customer profile
    'intent_signals': 0-25, # Buying signals detected
    'engagement': 0-20,     # Email opens, clicks, replies
    'timing': 0-15,         # Budget cycle, seasonality
    'budget_signals': 0-10  # Company size, funding
}
# Thresholds: Hot: 70+ | Warm: 40-69 | Nurture: <40
```

### 6-Agent Architecture

| Agent | Role | Output |
|-------|------|--------|
| RESEARCHER | Company intel, tech stack | Enriched company data |
| QUALIFIER | ICP fit scoring | 0-100 score + tier |
| ENRICHER | Contact discovery | Verified emails, org chart |
| WRITER | Personalized sequences | Multi-step email campaign |
| ANALYZER | Reply intent | Route to next action |
| ROUTER | Orchestration | Next-best-action |

### Cold Email Principles

1. **Short and specific** - Under 100 words
2. **Problem-forward** - Lead with their pain
3. **Clear CTA** - One ask (usually 10-min call)
4. **Personalization** - Company name, specific detail

### Email Sequence Structure

| Step | Timing | Purpose |
|------|--------|---------|
| 1 | Day 0 | Initial outreach - problem statement |
| 2 | Day 3 | Follow-up - different angle |
| 3 | Day 7 | Value add - insight or resource |
| 4 | Day 10 | Break-up - last chance |

---

## Part 2: Revenue Operations

### Core Metrics

#### Pipeline Metrics

```yaml
pipeline_coverage:
  formula: "Pipeline Value / Quota"
  healthy: "3-4x for SMB, 4-5x for Enterprise"
  warning: "Below 3x"

pipeline_velocity:
  formula: "(# Opps x Win Rate x Avg Deal) / Cycle Days"
  use: "Predict monthly revenue"

weighted_pipeline:
  formula: "Sum of (Deal Value x Stage Probability)"
```

#### Conversion Funnel

| Stage | Formula | Benchmark |
|-------|---------|-----------|
| Lead to MQL | MQLs / Total Leads | 15-30% |
| MQL to SQL | SQLs / MQLs | 30-50% |
| SQL to Opp | Opportunities / SQLs | 50-70% |
| Opp to Win | Closed Won / Opportunities | 20-30% |
| Overall | Closed Won / Total Leads | 1-5% |

#### Unit Economics

| Metric | Formula | Healthy |
|--------|---------|---------|
| CAC | (Sales + Marketing) / New Customers | Depends on ACV |
| LTV | (ARPU x Gross Margin) / Churn Rate | - |
| LTV:CAC | LTV / CAC | >3:1 |
| Payback | CAC / (ARPU x Gross Margin) | <12 months |

### Pipeline Stages

| Stage | Probability | Entry Criteria |
|-------|-------------|----------------|
| Lead | 5% | Contact captured |
| MQL | 10% | Meets ICP |
| SQL | 20% | BANT confirmed |
| Discovery | 30% | Meeting scheduled |
| Demo | 50% | Demo completed |
| Proposal | 70% | Proposal sent |
| Negotiation | 85% | Terms discussed |
| Closed Won | 100% | Contract signed |

### Forecasting Methods

| Method | Formula | Best For |
|--------|---------|----------|
| Pipeline-based | Sum(Deal x Stage Probability) | Simple, data-driven |
| Historical | Historical conversion x Pipeline | Past performance |
| Commit-based | Rep commits + Manager adjustment | Incorporates judgment |

---

## Part 3: Demo & Discovery

### Call Structure

| Stage | Goal | Duration |
|-------|------|----------|
| Opening | Build rapport, set agenda | 2-3 min |
| Discovery | Uncover pain, qualify | 15-20 min |
| Demo | Show relevant value | 15-20 min |
| Close | Agree next steps | 5 min |

### SPIN Questioning

| Type | Purpose | Example |
|------|---------|---------|
| **S**ituation | Understand context | "Walk me through your current process..." |
| **P**roblem | Surface pain | "What challenges do you face with...?" |
| **I**mplication | Deepen pain | "What happens when that goes wrong?" |
| **N**eed-Payoff | Envision solution | "If you could fix that, what would change?" |

### MEDDIC Qualification

| Letter | Element | Key Question |
|--------|---------|--------------|
| **M** | Metrics | What's the measurable impact? |
| **E** | Economic Buyer | Who controls budget? |
| **D** | Decision Criteria | How will they decide? |
| **D** | Decision Process | What are steps to buy? |
| **I** | Identify Pain | What's compelling reason to act? |
| **C** | Champion | Who's selling internally? |

### Demo Best Practices

```
1. RECAP (2 min)
   "Based on our discovery, you mentioned [pain 1], [pain 2]..."

2. AGENDA (1 min)
   "I'll show how we address each. Stop me anytime."

3. SHOW VALUE (15-20 min)
   Pain -> Feature -> Benefit -> Proof (repeat for each pain)

4. SUMMARIZE (2 min)
   "So you'd be able to [benefit 1], [benefit 2]..."

5. NEXT STEPS (5 min)
   "What questions? What's our next step?"
```

### Demo Rules

1. **Show, don't tell** - Open the product, demonstrate
2. **Connect to pain** - Every feature tied to their problem
3. **Pause for reactions** - "How does that compare to current?"

### Objection Handling (LAER)

```
L - Listen (fully, don't interrupt)
A - Acknowledge (validate the concern)
E - Explore (understand the root)
R - Respond (address specifically)
```

| Objection | Response Framework |
|-----------|-------------------|
| "Too expensive" | Acknowledge -> "Compared to what?" -> Show ROI |
| "Not ready" | Acknowledge -> "What would need to change?" -> Pilot option |
| "Looking at [competitor]" | Acknowledge -> "What draws you?" -> Differentiate |
| "Need boss approval" | Acknowledge -> "What will they ask?" -> Offer to join |

---

## Call Prep Checklist

```markdown
### Research (10 min)
- [ ] Company website - recent news
- [ ] LinkedIn - prospect background
- [ ] Tech stack - BuiltWith, job postings
- [ ] Competitors they might use

### Preparation (5 min)
- [ ] Hypothesis: Why might they need us?
- [ ] 3 discovery questions ready
- [ ] Demo environment ready
- [ ] Clear next step in mind

### Mindset
- [ ] Curiosity, not pitch mode
- [ ] Understand their world first
```

---

## Weekly Pipeline Review Template

```markdown
### Coverage Check
- Current pipeline: $___
- Quota this month: $___
- Coverage ratio: ___x (target: 3-4x)

### Stage Movement
| Stage | Start | End | Net |
|-------|-------|-----|-----|
| Discovery | | | |
| Demo | | | |
| Proposal | | | |

### Deals at Risk
| Deal | Amount | Days in Stage | Risk |
|------|--------|---------------|------|

### Action Items
- [ ] Stalled deals to address
- [ ] Proposals to follow up
- [ ] Deals to close this week
```

---

## Integration Notes

- **Email Tools:** Instantly.ai, Apollo.io, custom SMTP
- **CRM:** Salesforce, HubSpot, Airtable
- **Enrichment:** Clearbit, ZoomInfo, LinkedIn, Hunter.io
- **Related Projects:** cold-reach, sales-agent, dealer-scraper-mvp

## Reference Files

- `reference/outreach.md` - Email templates, domain warming, agent architecture
- `reference/revenue-ops.md` - Metrics, dashboards, forecasting
- `reference/discovery.md` - MEDDIC scorecard, demo scripts, objection library
