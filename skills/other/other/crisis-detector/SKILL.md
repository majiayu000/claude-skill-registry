---
name: crisis-detector
description: Identify early warning signals of potential PR crises through pattern recognition, escalation triggers, and risk assessment
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Crisis Detector

> Identify early warning signs of potential crises before they escalate through pattern recognition, signal monitoring, and risk assessment.

## When to Use This Skill

- Setting up early warning systems
- Assessing crisis probability
- Training teams on signals
- Building escalation criteria
- Post-crisis prevention planning

## Methodology Foundation

Based on **Institute for Crisis Management research** and **Burson crisis frameworks**, combining:
- Signal identification
- Pattern recognition
- Risk assessment matrices
- Escalation protocols

## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Identifies warning signals | Risk tolerance |
| Assesses crisis probability | Response resources |
| Creates detection criteria | Escalation authority |
| Designs monitoring systems | Communication strategy |
| Suggests response triggers | Final action calls |

## Instructions

### Step 1: Map Crisis Types

**Crisis Categories:**

| Category | Examples | Warning Time |
|----------|----------|--------------|
| **Operational** | Outage, product failure | Hours to days |
| **Reputational** | Executive scandal, viral complaint | Minutes to hours |
| **Legal/Regulatory** | Lawsuit, investigation | Days to weeks |
| **Financial** | Earnings miss, fraud | Hours to days |
| **Human** | Workplace incident, harassment | Hours to days |
| **External** | Natural disaster, market crash | Variable |

### Step 2: Identify Early Signals

**Signal Types:**

| Signal Type | Examples | Monitoring |
|-------------|----------|------------|
| **Internal** | Employee complaints, support tickets | HR, Support data |
| **Customer** | Review patterns, churn spikes | CX metrics |
| **Social** | Mention volume, sentiment shift | Social tools |
| **Media** | Press inquiries, journalist interest | PR inbox |
| **Regulatory** | Compliance notices, audit findings | Legal |
| **Financial** | Payment disputes, refund requests | Finance |

### Step 3: Build Detection Matrix

**Signal Strength Assessment:**

| Signal | Weak | Moderate | Strong | Critical |
|--------|------|----------|--------|----------|
| Volume spike | +25% | +50% | +100% | +300% |
| Sentiment shift | -10% | -20% | -30% | -50% |
| Media inquiries | 1 | 2-3 | 4-5 | 6+ |
| Support tickets | +10% | +25% | +50% | +100% |
| Social influencer | 10K | 50K | 100K | 500K+ |

### Step 4: Create Escalation Triggers

**Trigger Framework:**

| Level | Signals Present | Action |
|-------|-----------------|--------|
| Watch | 1 moderate signal | Monitor closely |
| Alert | 2+ moderate or 1 strong | Notify team |
| Warning | Multiple strong signals | Assemble team |
| Crisis | Any critical signal | Activate protocol |

### Step 5: Document and Improve

**Post-Detection Review:**
- How early did we detect?
- What signals did we miss?
- How accurate was assessment?
- What should we add to monitoring?

## Examples

### Example 1: Crisis Detection System Design

**Input:**
```
Design a crisis detection system for:
- E-commerce company (clothing)
- 500K customers
- Active on Instagram, TikTok, Twitter
- Past issue: Shipping delays during holiday
```

**Output:**
```
## Crisis Detection System: E-Commerce Fashion

### Crisis Risk Map

| Crisis Type | Probability | Impact | Priority |
|-------------|-------------|--------|----------|
| Shipping delays | High | High | P1 |
| Product quality issue | Medium | High | P1 |
| Social media backlash | Medium | High | P1 |
| Data breach | Low | Critical | P1 |
| Influencer controversy | Medium | Medium | P2 |
| Supply chain disruption | Medium | High | P2 |
| Payment fraud | Low | Medium | P3 |

---

### Early Warning Signals

#### P1: Shipping Delays

**Leading Indicators (3-5 days before crisis):**
| Signal | Source | Threshold |
|--------|--------|-----------|
| Carrier delay reports | Logistics API | >10% delayed |
| Warehouse backlog | WMS data | >24hr processing |
| Weather events | News/weather | Storm in hub |
| "Where's my order" tickets | Support | +50% daily |

**Lagging Indicators (crisis starting):**
| Signal | Source | Threshold |
|--------|--------|-----------|
| Social mentions | Social listening | "shipping" +100% |
| Review mentions | Trustpilot/G2 | Shipping 3/5 stars |
| Refund requests | Payment system | +30% |
| Chargeback rate | Payment processor | >1% |

---

#### P1: Product Quality Issue

**Leading Indicators:**
| Signal | Source | Threshold |
|--------|--------|-----------|
| Return rate spike | Returns data | >10% on SKU |
| Quality complaints | Support tickets | 3+ same issue |
| Photo complaints | Social | "damaged", "wrong color" |
| Batch-specific issues | QC data | Same lot number |

**Lagging Indicators:**
| Signal | Source | Threshold |
|--------|--------|-----------|
| Viral unboxing | TikTok/Instagram | >10K views negative |
| Review bomb | Product pages | Multiple 1-stars |
| Media inquiry | PR inbox | Journalist question |

---

#### P1: Social Media Backlash

**Leading Indicators:**
| Signal | Source | Threshold |
|--------|--------|-----------|
| Sentiment shift | Social tools | -20% in 24hr |
| Controversial post | Your social | Negative comments >10% |
| Influencer complaint | Social | >50K follower post |
| Screenshot spreading | Twitter/Reddit | Same image 5+ times |

**Lagging Indicators:**
| Signal | Source | Threshold |
|--------|--------|-----------|
| Viral negative | Any platform | >50K engagements |
| Hashtag trending | Twitter | Brand + negative |
| Media pickup | News sites | Article published |
| Competitor amplification | Social | Competitor sharing |

---

### Detection Dashboard

```
┌──────────────────────────────────────────────────────────┐
│  CRISIS DETECTION DASHBOARD                    🟢 NORMAL │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  SHIPPING STATUS                              🟢 Normal  │
│  ├─ Carrier delays: 3% (threshold: 10%)                 │
│  ├─ Backlog: 4 hours (threshold: 24hr)                  │
│  └─ "Where's my order": 45 (baseline: 50)               │
│                                                          │
│  PRODUCT QUALITY                              🟢 Normal  │
│  ├─ Return rate: 5.2% (threshold: 10%)                  │
│  ├─ Quality tickets: 2 (threshold: 3+ same)             │
│  └─ Photo complaints: 1 (threshold: 5)                  │
│                                                          │
│  SOCIAL SENTIMENT                             🟡 Watch   │
│  ├─ Sentiment: -15% (threshold: -20%)                   │
│  ├─ Volume: +40% (threshold: +50%)                      │
│  └─ Influencer: None flagged                            │
│                                                          │
│  SECURITY                                     🟢 Normal  │
│  ├─ Login anomalies: Normal                             │
│  └─ Payment fraud: 0.3%                                 │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

### Escalation Matrix

| Level | Criteria | Notification | Response |
|-------|----------|--------------|----------|
| 🟢 Normal | All metrics in range | None | Standard ops |
| 🟡 Watch | 1 metric at threshold | Slack alert | Increased monitoring |
| 🟠 Alert | 2+ metrics or 1 exceeded | Team notification | Standby team |
| 🔴 Crisis | Critical threshold breached | All-hands alert | Activate protocol |

---

### Alert Routing

| Signal Type | Primary | Backup | Escalation |
|-------------|---------|--------|------------|
| Shipping | Operations | COO | CEO |
| Product quality | Product | VP Ops | CEO |
| Social media | Marketing | CMO | CEO |
| Security | IT | CTO | CEO + Legal |
| Legal/PR | Legal | CEO | Board |

---

### Holiday Season Adjustments

During high-volume periods (Nov 15 - Dec 31):

| Metric | Normal Threshold | Holiday Threshold |
|--------|------------------|-------------------|
| Carrier delays | 10% | 15% |
| Support volume | +50% | +100% |
| Social volume | +50% | +75% |
| Response time | 4 hours | 8 hours |

**Rationale:** Higher baseline expected; adjust to avoid false alerts
while maintaining genuine crisis detection.
```

### Example 2: Real-Time Crisis Assessment

**Input:**
```
Assess this situation:
- Support tickets up 80% in 2 hours
- Twitter mentions up 150%
- Hashtag #[Brand]Scam trending locally
- 3 refund requests mentioning "charged twice"
- No known system issues
```

**Output:**
```
## Crisis Assessment: Potential Payment Issue

### Alert Level: 🔴 CRISIS

---

### Signal Analysis

| Signal | Value | Normal | Status |
|--------|-------|--------|--------|
| Support spike | +80% | <25% | CRITICAL |
| Social spike | +150% | <50% | CRITICAL |
| Trending hashtag | Yes | No | CRITICAL |
| Duplicate charge reports | 3 | 0 | CONCERNING |

---

### Probable Cause

**Most likely: Payment processing error**

Evidence:
1. Multiple "charged twice" complaints
2. No known system issues rules out outage
3. Sudden spike suggests batch problem
4. #Scam hashtag = customers think fraud

---

### Immediate Actions

| Priority | Action | Owner | Timeline |
|----------|--------|-------|----------|
| 1 | Check payment processor logs | Engineering | NOW |
| 2 | Identify affected transactions | Finance | 30 min |
| 3 | Prepare holding statement | Comms | 15 min |
| 4 | Alert customer service team | CX Lead | NOW |
| 5 | Monitor hashtag spread | Social | Ongoing |

---

### Holding Statement (Draft)

```
We're aware some customers may have experienced duplicate
charges. Our team is investigating urgently. If you've been
affected, please DM us or email [support] - we'll make this
right immediately.

Updates to follow shortly.
```

---

### Escalation Path

**Now:** CTO + CFO + CMO notified
**+30 min:** CEO briefing if not resolved
**+1 hour:** External statement if ongoing

---

### Crisis Trajectory

**If unaddressed (next 2-4 hours):**
- Hashtag goes national
- Media inquiries begin
- Trust pilot review bomb
- Social influencers amplify

**If addressed quickly (next 1-2 hours):**
- Contain to affected customers
- Flip narrative to "responsive company"
- Prevent media escalation
- Build goodwill through fast resolution

---

### Resolution Checklist

- [ ] Root cause identified
- [ ] Affected customers identified
- [ ] Refunds initiated
- [ ] Proactive communication sent
- [ ] Social response deployed
- [ ] Hashtag monitoring active
- [ ] Post-incident review scheduled
```

## Skill Boundaries

### What This Skill Does Well
- Identifying early warning signals
- Creating detection frameworks
- Assessing crisis probability
- Designing escalation systems

### What This Skill Cannot Do
- Access your actual systems
- Monitor in real-time
- Make response decisions
- Know your specific thresholds

## Iteration Guide

**Follow-up Prompts:**
- "Design detection for [specific crisis type]"
- "Create escalation protocol for [scenario]"
- "What signals should we add for [risk]?"
- "How do we prevent [past crisis] from recurring?"

## References

- Institute for Crisis Management
- Burson Crisis Playbook
- Harvard Business Review Crisis Research
- Edelman Trust Barometer

## Related Skills

- `social-listening` - Monitoring systems
- `response-coordinator` - Crisis response
- `reputation-recovery` - Post-crisis rebuild

## Skill Metadata

- **Domain**: Crisis
- **Complexity**: Intermediate-Advanced
- **Mode**: centaur
- **Time to Value**: 2-4 hours for system design
- **Prerequisites**: Access to metrics, stakeholder alignment
