---
name: lead-scoring
description: Build and apply lead scoring models combining firmographic fit, behavioral signals, and intent data for sales prioritization
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Lead Scoring

> Prioritize leads using a systematic scoring model that combines ICP fit, engagement behavior, and buying intent signals.

## When to Use This Skill

- Designing a new lead scoring model
- Prioritizing inbound leads for SDR follow-up
- Setting MQL thresholds for sales handoff
- Analyzing lead quality by source
- Optimizing marketing spend by lead score

## Methodology Foundation

Based on **HubSpot's Lead Scoring methodology** and **Forrester's B2B Buyer Journey research**, combining:
- Firmographic/demographic fit (who they are)
- Behavioral scoring (what they do)
- Intent signals (buying readiness)
- Negative scoring (disqualification)

## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Designs scoring model structure | Point values for your business |
| Calculates lead scores | MQL threshold for handoff |
| Identifies high-intent behaviors | Which behaviors matter most |
| Segments leads by score | Sales follow-up priorities |
| Suggests model improvements | Model weight adjustments |

## What This Skill Does

1. **Model design** - Create scoring framework with fit + behavior + intent
2. **Score calculation** - Apply model to lead data
3. **Threshold setting** - Define MQL/SQL qualification levels
4. **Segmentation** - Group leads by score for routing
5. **Optimization** - Analyze score-to-conversion correlation

## How to Use

### For Model Design:
```
Help me create a lead scoring model for [Business Type].

Our ICP:
- Company size: [Range]
- Industries: [List]
- Titles: [Target titles]
- Geography: [Regions]

Key buying signals we track:
- [List website pages, content, actions]

Current conversion rates:
- Lead to MQL: X%
- MQL to SQL: X%
- SQL to Won: X%
```

### For Lead Scoring:
```
Score this lead:

Company: [Name]
Size: [Employees]
Industry: [Industry]
Title: [Contact title]
Location: [Geography]

Behavior (last 30 days):
- [List pages visited, content downloaded, emails opened]
```

## Instructions

### Step 1: Define Fit Score (0-40 points)

**Company Firmographics:**
| Criteria | Points |
|----------|--------|
| Company size matches ICP | +10 |
| Industry in target list | +10 |
| Geography in target regions | +5 |
| Revenue in target range | +5 |
| Company size too small | -10 |
| Industry excluded | -20 |

**Contact Demographics:**
| Criteria | Points |
|----------|--------|
| Title is decision maker | +10 |
| Title is influencer | +5 |
| Title is end user | +3 |
| Student/Personal email | -15 |
| Competitor domain | -40 |

### Step 2: Define Behavior Score (0-40 points)

**Content Engagement:**
| Action | Points |
|--------|--------|
| Pricing page visit | +15 |
| Case study download | +10 |
| Product demo video watched | +10 |
| Blog post read | +2 |
| 5+ pages in session | +5 |
| Return visit within 7 days | +5 |

**Direct Engagement:**
| Action | Points |
|--------|--------|
| Demo request form | +30 |
| Contact sales form | +25 |
| Free trial signup | +20 |
| Webinar registration | +10 |
| Newsletter signup | +3 |
| Email opened | +1 |
| Email clicked | +3 |

### Step 3: Define Intent Score (0-20 points)

**Third-Party Intent:**
| Signal | Points |
|--------|--------|
| Researching your category (Bombora/G2) | +15 |
| Competitor comparison searches | +10 |
| Job posting for related role | +5 |
| Funding announcement | +5 |
| Technology install matches | +5 |

### Step 4: Apply Negative Scoring

| Signal | Points |
|--------|--------|
| Unsubscribed from email | -10 |
| Bounced email | -20 |
| No engagement 90+ days | -15 |
| Marked as spam | -30 |
| Competitor | -100 |

### Step 5: Set Thresholds

| Score Range | Qualification | Action |
|-------------|---------------|--------|
| 80-100 | Hot MQL | Immediate sales call |
| 60-79 | Warm MQL | SDR outreach 24hr |
| 40-59 | Marketing Qualified | Nurture sequence |
| 20-39 | Early Stage | Educational content |
| 0-19 | Not Qualified | Monitor only |
| Negative | Disqualified | Suppress |

## Examples

### Example 1: Scoring Model Design

**Input:**
```
Help me create a lead scoring model for B2B SaaS (marketing automation).

Our ICP:
- Company size: 50-500 employees
- Industries: Tech, E-commerce, SaaS
- Titles: VP Marketing, Director Marketing, CMO
- Geography: US, Canada, UK

Key buying signals:
- Pricing page, demo request, case studies
- Marketing automation category on G2
```

**Output:**
```
## Lead Scoring Model: Marketing Automation SaaS

### Fit Score (Max 40 points)

**Company Fit (20 points)**
| Criteria | Points |
|----------|--------|
| 50-500 employees | +10 |
| 500-1000 employees | +5 |
| <50 or >1000 employees | +0 |
| Tech/E-commerce/SaaS industry | +10 |
| Adjacent industry (Retail, Media) | +5 |
| Non-target industry | +0 |

**Contact Fit (20 points)**
| Criteria | Points |
|----------|--------|
| VP/Director Marketing, CMO | +15 |
| Marketing Manager | +10 |
| Marketing Coordinator | +5 |
| Non-marketing title | +0 |
| US/Canada/UK | +5 |
| Other geography | +0 |
| Personal email (@gmail) | -15 |
| Competitor domain | -40 |

### Behavior Score (Max 40 points)

**High-Intent Actions**
| Action | Points |
|--------|--------|
| Demo request submitted | +25 |
| Pricing page visit | +15 |
| Case study download | +10 |
| Product tour completed | +10 |

**Engagement Actions**
| Action | Points |
|--------|--------|
| 3+ pages in session | +5 |
| Return visit (7 days) | +5 |
| Webinar registered | +8 |
| Blog post read | +2 |
| Email clicked | +3 |
| Email opened | +1 |

### Intent Score (Max 20 points)

| Signal | Points |
|--------|--------|
| G2 category research | +10 |
| Competitor comparison | +8 |
| Marketing hire posting | +5 |
| Series A/B funding | +5 |

### Negative Scoring

| Signal | Points |
|--------|--------|
| Unsubscribed | -10 |
| No activity 90 days | -15 |
| Email bounced | -20 |
| Competitor | -100 |

### Thresholds

| Score | Status | SLA |
|-------|--------|-----|
| 70+ | 🔥 Hot MQL | Call within 5 min |
| 50-69 | 🟢 MQL | SDR contact 24hr |
| 30-49 | 🟡 Nurture | Email sequence |
| <30 | Monitor | No outreach |
```

### Example 2: Individual Lead Scoring

**Input:**
```
Score this lead using the model above:

Company: GrowthTech Inc
Size: 180 employees
Industry: SaaS
Title: VP of Marketing
Location: San Francisco, US

Behavior (last 30 days):
- Visited pricing page (2x)
- Downloaded "Email Automation Guide"
- Attended webinar "Marketing Automation 101"
- Opened 4 emails, clicked 2
- Visited 8 pages total

Intent: Showing on G2 for marketing automation research
```

**Output:**
```
## Lead Score: GrowthTech Inc

### Overall Score: 83/100 🔥 HOT MQL

### Score Breakdown

**Fit Score: 35/40**
| Factor | Points | Notes |
|--------|--------|-------|
| Company size (180) | +10 | Perfect ICP |
| Industry (SaaS) | +10 | Target industry |
| Title (VP Marketing) | +15 | Decision maker |
| Location (US) | +5 | Target geography |
| **Subtotal** | **35** | |

**Behavior Score: 38/40**
| Action | Points | Notes |
|--------|--------|-------|
| Pricing page (2x) | +15 | High intent signal |
| Content download | +5 | Educational engagement |
| Webinar attended | +8 | Active learning |
| 8 pages visited | +5 | Deep exploration |
| 4 emails opened | +4 | Engaged with nurture |
| 2 emails clicked | +6 | Taking action |
| **Subtotal** | **38** | |

**Intent Score: 10/20**
| Signal | Points | Notes |
|--------|--------|-------|
| G2 category research | +10 | Active buyer research |
| **Subtotal** | **10** | |

### Qualification: HOT MQL
- **Action Required**: Immediate SDR call (within 5 minutes)
- **Talking Points**: Reference webinar attendance, pricing interest
- **Ask**: "What prompted your marketing automation research?"

### Next Best Actions
1. Call within 5 minutes (hot lead SLA)
2. Reference webinar + pricing page visits
3. Offer personalized demo with VP Marketing use cases
4. Connect on LinkedIn (warm outreach)
```

## Skill Boundaries

### What This Skill Does Well
- Structuring scoring models systematically
- Calculating scores from provided data
- Recommending thresholds based on best practices
- Identifying model gaps

### What This Skill Cannot Do
- Access your CRM data directly
- Know your actual conversion rates
- Predict individual lead outcomes
- Account for offline interactions

### When to Escalate to Human
- Setting final MQL thresholds (needs sales alignment)
- Weighting decisions (requires business judgment)
- Model validation (needs historical data analysis)
- Edge cases (unusual company profiles)

## Iteration Guide

### Follow-up Prompts
- "Adjust the model for enterprise (1000+ employees) leads."
- "What score would trigger an immediate call for us?"
- "Compare scores for these 5 leads and rank them."
- "What behaviors should we add to increase accuracy?"

### Model Refinement Cycle
1. Build initial model → Deploy
2. Track score vs. conversion rate
3. Adjust weights based on data
4. Add new signals quarterly
5. Remove low-correlation factors

## Checklists & Templates

### Lead Scoring Model Template
```markdown
## [Company] Lead Scoring Model v[X]

### Fit Score (Max X points)
| Criteria | Points |
|----------|--------|

### Behavior Score (Max X points)
| Action | Points |
|--------|--------|

### Intent Score (Max X points)
| Signal | Points |
|--------|--------|

### Negative Scoring
| Signal | Points |
|--------|--------|

### Thresholds
| Score | Status | Action |
|-------|--------|--------|

### Review Schedule
- Quarterly weight review
- Monthly threshold check
```

### Model Audit Checklist
- [ ] All ICP criteria have point values
- [ ] High-intent behaviors weighted appropriately
- [ ] Negative scoring prevents bad leads
- [ ] Thresholds align with sales capacity
- [ ] Model reviewed in last 90 days

## References

- HubSpot Lead Scoring Guide
- Forrester B2B Buyer Journey Research
- Marketo Definitive Guide to Lead Scoring
- SiriusDecisions Demand Waterfall

## Related Skills

- `icp-matching` - Deep ICP definition
- `pipeline-forecasting` - Score aggregation to forecast
- `deal-risk-scoring` - Post-MQL deal health

## Skill Metadata

- **Domain**: RevOps
- **Complexity**: Intermediate
- **Mode**: centaur
- **Time to Value**: 30-60 min for model design, 2 min per lead
- **Prerequisites**: ICP definition, behavior tracking capability
