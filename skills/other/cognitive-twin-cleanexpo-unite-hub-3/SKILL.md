---
name: cognitive-twin
description: Continuous business health monitoring across 13 business domains. Scores domain health, generates periodic digests, detects anomalies, simulates decisions, and provides early warning signals for problems.
---

# Cognitive Twin Skill

## Overview

The Cognitive Twin is the **always-on business health monitor**. It:
- Continuously tracks 13 business domains
- Calculates domain-specific health scores (0-100)
- Detects anomalies and trends across domains
- Generates periodic health digests
- Simulates decision outcomes
- Provides early warning signals for problems

Like having a "twin" who watches your business 24/7 and alerts you when something seems off.

## Core Capabilities

### 1. The 13 Business Domains

**FINANCIAL DOMAIN (25% of overall score)**
```
Components:
- Revenue growth: Monthly growth rate, YoY comparison
- Profitability: Gross margin, net margin, unit economics
- Burn rate: Runway in months, cash position
- Customer LTV: Lifetime value per customer
- Churn: Monthly churn rate, trend direction
- Pricing power: Ability to raise prices without losing customers

Health Score Calculation:
- Revenue growing 10%+ MoM: +20 points
- Gross margin 60%+: +20 points
- Burn rate sustainable: +20 points
- LTV:CAC ratio 3+:1: +20 points
- Churn < 3%: +20 points

Example Score: 78/100
- Strong revenue (+20)
- Good margins (+18)
- 7-month runway (+15) ← Getting short
- Good LTV ratio (+20)
- Acceptable churn (+5)

Alerts trigger at:
- Runway dropping below 12 months
- Churn increasing 1%+ month-over-month
- Revenue growth dropping below 5%
```

**CUSTOMER DOMAIN (20% of overall score)**
```
Components:
- Customer satisfaction (NPS): Net Promoter Score, trend
- Customer acquisition cost: CAC, vs. industry benchmark
- Customer retention: Retention rate by cohort
- Customer diversity: Concentration risk (% from top 5 customers)
- Customer feedback: Support tickets, feature requests, sentiment
- Customer expansion: Revenue expansion from existing customers

Health Score Calculation:
- NPS 50+: +25 points
- CAC improving: +20 points
- Retention rate 90%+: +25 points
- No customer > 10% revenue: +15 points
- Positive feedback trend: +15 points

Example Score: 72/100
- NPS 45 (+20)
- CAC stable (+18)
- 85% retention (+20) ← Could be better
- Top customer = 12% (+10)
- Mixed feedback (+4)

Alerts trigger at:
- NPS dropping 5+ points
- CAC increasing without revenue increase
- Retention trending down
- Single customer > 20% revenue
```

**PRODUCT DOMAIN (18% of overall score)**
```
Components:
- Product-market fit: Usage frequency, feature adoption
- Roadmap execution: On-time delivery of planned features
- Bug/quality: Number of critical bugs, time to fix
- Performance: Page load time, uptime, reliability
- Feature parity: vs. competitors, what are you missing?
- User engagement: DAU/MAU ratio, feature usage depth

Health Score Calculation:
- 60%+ DAU/MAU ratio: +20 points
- Roadmap 90%+ on time: +20 points
- < 3 critical bugs: +20 points
- 99.5%+ uptime: +20 points
- Feature competitive: +20 points

Example Score: 68/100
- 50% DAU/MAU (+15) ← Could increase
- 70% on-time delivery (+14)
- 5 critical bugs (+10) ← Getting high
- 99.2% uptime (+16) ← Slight issue
- Missing 2 key features (+13)

Alerts trigger at:
- DAU/MAU dropping 5%+
- Uptime below 99%
- Critical bugs accumulating
- Major feature competitors have
- Roadmap delays exceeding 2 weeks
```

**TEAM DOMAIN (15% of overall score)**
```
Components:
- Headcount growth: Hiring pace, retention rate
- Team satisfaction: Employee engagement, satisfaction scores
- Key person dependency: Risk if someone leaves
- Team skill gaps: Missing expertise for roadmap
- Diversity & inclusion: Team composition representation
- Team productivity: Output per person, iteration speed

Health Score Calculation:
- Headcount growing on plan: +25 points
- Team satisfaction 7+/10: +25 points
- No person > 30% critical skills: +20 points
- Skill gaps being filled: +15 points
- Team diverse: +15 points

Example Score: 58/100
- Hiring on track (+25)
- Satisfaction 6.2/10 (+15) ← Getting low
- CEO/CTO key person risk (+0) ← Critical
- 3 skill gaps unfilled (+5) ← Problem
- Limited diversity (+8)

Alerts trigger at:
- Key person departure risk identified
- Team satisfaction dropping
- Hiring unable to keep pace
- Skill gaps growing
```

**MARKET DOMAIN (10% of overall score)**
```
Components:
- Market size: TAM, addressable market trends
- Market growth rate: Is market expanding or contracting?
- Competitive intensity: New entrants, consolidation
- Customer demand: Lead generation trends, sales pipeline
- Market timing: Are you ahead/behind market adoption curve?
- Regulatory environment: New regulations, restrictions

Health Score Calculation:
- Market growing 20%+: +25 points
- You growing faster than market: +25 points
- < 5 direct competitors: +20 points
- Strong customer demand signal: +20 points
- Regulatory tailwinds: +10 points

Example Score: 72/100
- Market growing 15% (+20)
- Growing faster (+25)
- 8 competitors (+10)
- Strong demand (+15) ← Good
- Neutral regulation (+2)

Alerts trigger at:
- Market growth slowing
- Competitive entrants increasing
- New unfavorable regulations
- Customer demand signals dropping
```

**OPERATIONS DOMAIN (5% of overall score)**
```
Components:
- Process efficiency: How fast can you execute?
- Cost control: Where is money going?
- Infrastructure: Technical debt, system reliability
- Compliance: Legal, regulatory, data handling
- Data management: Data quality, security, privacy

Health Score Calculation:
- Quarterly metrics within 10% of plan: +25 points
- No major compliance issues: +25 points
- Technical debt under control: +25 points
- No data breaches or incidents: +25 points

Example Score: 81/100
- Metrics tracking plan (+25)
- Clean compliance review (+20) ← Minor issue
- Some tech debt (+20)
- No incidents (+16)
```

**ADDITIONAL DOMAINS (covered by composite scoring)**
- Sales Domain (Lead generation, conversion rates, pipeline health)
- Marketing Domain (Brand awareness, lead quality, content performance)
- Partnership Domain (Strategic partners, partnership pipeline, co-marketing)
- Investor/Board Domain (Relationships, fundraising readiness, update cadence)
- Strategic Domain (Vision clarity, strategy execution, milestone achievement)
- Leadership Domain (Founder capability, leadership bench, decision-making)
- Culture Domain (Values alignment, retention, engagement, onboarding)

---

### 2. Periodic Health Digests

**Daily Quick Check (5 minutes)**
```
AUTOMATED - Sent every morning

Today's Health: 74/100 (↓1 point from yesterday)

RED FLAGS (Needs attention):
❌ Revenue tracking 5% below forecast (target: $42k, actual: $40k)
⚠️ 3 new critical bugs this week (normal: 1-2)

GREEN FLAGS (Good signs):
✅ Customer satisfaction up to 7.2/10
✅ Runway stable at 8.5 months

KEY METRICS AT A GLANCE:
- Monthly recurring revenue: $45,000 (↑12% MoM)
- Team size: 8 people (on track for 10 by Q2)
- NPS: 48 (good trend: ↑3 this month)
- Churn rate: 2.1% (stable)

RECOMMENDED ACTION:
Debug the 3 critical bugs this week. Don't let tech debt accumulate.
Everything else looks normal.
```

**Weekly Digest (30 minutes)**
```
SENT: Every Sunday evening

HEALTH SCORE: 74/100 (↑2 from last week)

DOMAIN BREAKDOWN:
Financial: 78/100 (↑1)
- Revenue: On track
- Burn: Stable
- Profitability: Improving

Customer: 72/100 (stable)
- NPS: 48 (good)
- Churn: 2.1% (acceptable)
- CAC: Improving

Product: 68/100 (↓2)
- DAU/MAU: Slightly down
- Bugs: 3 critical
- Uptime: Good

Team: 58/100 (stable)
- Hiring: On track
- Satisfaction: Slightly low
- Key person risk: CEO dependent

Market: 72/100 (stable)
- Market growing well
- Competition increasing
- Demand strong

ANOMALIES DETECTED:
1. Product domain dip (bugs + engagement)
   - Action: Prioritize bug fixes this week
   - Impact: Will recover if fixed quickly

2. Team satisfaction low (6.2/10)
   - Action: One-on-ones this week to understand why
   - Impact: Could lead to turnover if not addressed

WHAT'S WORKING WELL:
- Revenue growth trajectory
- Customer retention strong
- Market conditions favorable

WHAT NEEDS ATTENTION:
- Product quality (bugs)
- Team morale
- DAU/MAU slightly down

STRATEGIC IMPLICATIONS:
- You're in a strong position financially
- Don't let team satisfaction degrade
- Bug accumulation is concerning - address this week

NEXT WEEK FOCUS:
1. Fix 3 critical bugs
2. Check in with team about satisfaction
3. Continue revenue momentum
```

**Monthly Strategic Review (2 hours)**
```
SENT: First day of each month

MONTHLY HEALTH REPORT - November 2025
Generated: 2025-11-28

OVERALL HEALTH: 74/100
Month-over-month change: ↑3 points

FINANCIAL HEALTH: 78/100
- MRR: $45,000 (↑12% MoM)
- ARR: $540,000 (↑12% YoY)
- Gross Margin: 72% (industry avg: 70%)
- Churn Rate: 2.1% (industry avg: 5%)
- Runway: 8.5 months (target: 12+ months)
- Customer LTV: $2,400
- LTV:CAC Ratio: 2.8:1 (healthy target: 3:1)

Recommendation: You're financially healthy. Prioritize
customer acquisition to extend runway before Series A.

CUSTOMER HEALTH: 72/100
- NPS: 48 (trend: ↑3 from September)
- Retention: 85% (monthly, 95% annual)
- Customer Concentration: Top 5 = 35% of revenue
- Customer Expansion: 18% expansion from existing
- Support Satisfaction: 8.2/10
- Feature Requests: 42 (top 3 features identified)

Recommendation: You have strong customer loyalty.
Work on features customers are requesting (prioritize top 3).

PRODUCT HEALTH: 68/100
- DAU/MAU: 50% (trend: ↓3% from last month)
- Uptime: 99.2% (target: 99.5%)
- Page Load Time: 2.1s (target: <2.0s)
- Critical Bugs: 5 open
- Roadmap On-Time: 70% (target: 90%)
- Feature Parity vs. Competitors: 85%

Recommendation: This is the area to focus. Improve product
quality and engagement. Consider engineering hire to reduce
tech debt.

TEAM HEALTH: 58/100
- Current: 8 people
- Planned Growth: 10 by Q2 (on track)
- Satisfaction: 6.2/10 (trend: ↓0.8 from last month)
- Retention: 100% (no departures)
- Key Person Risk: CEO/CTO both critical
- Skill Gaps: 3 (backend engineer, designer, operations)

Recommendation: Team satisfaction is declining.
Investigate in 1-on-1s. Key person risk is concerning—
begin identifying successors for CEO/CTO roles.

MARKET HEALTH: 72/100
- TAM: $12B (growing 15% annually)
- Your TAM Penetration: 0.04%
- Competitors: 8 (major), 15+ (smaller)
- Market Growth: 15% (your growth: 12% MoM = strong)
- New Entrants: 2 raised Series B this month
- Regulatory: No changes

Recommendation: Market is healthy. Competitive intensity
increasing—accelerate your differentiation and brand building.

ANOMALY ANALYSIS:

CONCERN #1: Declining Product Engagement
- DAU/MAU down 3% (first decline in 6 months)
- Root cause hypothesis: New feature rollout created friction
- Action: Analyze user flows, identify friction points
- Timeline: Diagnose this week, fix next 2 weeks
- Impact if ignored: Could lead to churn acceleration

CONCERN #2: Team Satisfaction Declining
- Score dropped 0.8 points (first decline in 3 months)
- Root cause hypothesis: Heavy workload from new features?
- Action: 1-on-1s with all team members this week
- Timeline: Address concerns by end of month
- Impact if ignored: Risk losing team members

CONCERN #3: Key Person Risk
- If CEO or CTO leaves: Business at severe risk
- No succession plan identified
- Action: Document processes, identify backup
- Timeline: 30-day plan by end of December
- Impact if ignored: Business interruption if departure

---

WHAT'S WORKING WELL:
✅ Revenue growth strong and consistent
✅ Customer retention excellent for early stage
✅ Market timing favorable
✅ No team departures (retention 100%)

WHAT NEEDS FOCUS:
⚠️ Product quality and engagement (declining)
⚠️ Team satisfaction (declining trend)
⚠️ Key person dependency (unmitigated)
⚠️ Runway extension (need 12+ months soon)

STRATEGIC DECISIONS NEEDED THIS MONTH:
1. Engineering hire decision: Yes or No? (Impacts runway but improves product)
2. Feature prioritization: Which customer requests to tackle first?
3. Competitive response: 2 new competitors entered—differentiation strategy?

RECOMMENDED ACTIONS - NEXT 30 DAYS:

PRIORITY 1 (Do this week):
□ Diagnose product engagement decline (3 hours)
□ 1-on-1s with team to address satisfaction (8 hours)
□ Identify succession plans for CEO/CTO (2 hours)

PRIORITY 2 (Do this month):
□ Fix technical debt to improve uptime/performance (20 hours)
□ Implement customer feature requests (top 3) (40 hours)
□ Engineering hire: Post role, begin interviews (10 hours)
□ Competitive differentiation strategy (8 hours)

PRIORITY 3 (Planning):
□ Series A readiness assessment (for fundraising in 6 months)
□ Board/investor update deck (if applicable)
□ Annual strategy refresh (for Q1 planning)

FINANCIAL FORECAST - Q1 2026:
- Projected MRR: $48,500 (↑7.7% from November)
- Projected Churn: 2.3% (slight increase expected)
- Projected Runway: 7.2 months (declining due to hiring)
- Break-even timeline: 14 months (without changes)

CONFIDENCE LEVEL: HIGH (based on consistent metrics)
```

### 3. Anomaly Detection

**Real-time anomaly flags:**
```
ANOMALIES DETECTED IN LAST 7 DAYS:

FINANCIAL ANOMALIES:
1. CRITICAL: Daily active users down 15%
   - Normal range: ±5%
   - Severity: Could impact monthly revenue forecast
   - Hypothesis: New feature rollout or bug?
   - Action: Investigate user behavior changes immediately
   - Investigation: Check analytics for drop-off point

2. ALERT: Revenue forecast down 8% vs. plan
   - Plan: $42,000
   - Actual: $38,700 (on pace for month)
   - Severity: Moderate, still acceptable range
   - Hypothesis: Sales cycle extension?
   - Action: Review sales pipeline for stalled deals

TEAM ANOMALIES:
1. WARNING: Team satisfaction score dropped 1.2 points
   - Normal month-to-month: ±0.3
   - Severity: Potential warning sign
   - Hypothesis: High workload? Toxic situation? Burnout?
   - Action: 1-on-1s to diagnose
   - Monitor: Weekly check-ins for next month

PRODUCT ANOMALIES:
1. CRITICAL: 5 critical bugs reported this week
   - Normal: 1-2 per week
   - Severity: Quality is degrading
   - Hypothesis: Recent feature rollout introduced issues
   - Action: Pause feature releases, focus on stabilization
   - Timeline: Target resolution by end of week

2. ALERT: Page load time increased to 2.1s
   - Target: <2.0s
   - Normal range: 1.8-2.0s
   - Severity: Minor, but trending wrong direction
   - Hypothesis: Increased database queries from new features
   - Action: Database optimization
   - Monitor: Daily metrics for next week

MARKET ANOMALIES:
None detected - market conditions stable
```

### 4. Decision Simulation

**Simulate decisions before executing:**
```
DECISION: Should we hire an engineering manager?

SCENARIO MODELING:

BASE CASE (No hire):
- Current burn: $120k/month
- Runway: 8.5 months
- Team productivity: 8 people delivering features
- Tech debt: Accumulating slowly
- Product velocity: Steady but slowing

IF WE HIRE ENGINEERING MANAGER:
- Burn: +$180k/year salary = $135k/month (+12.5%)
- Runway: 7.2 months (↓1.3 months)
- Team productivity: +15-20% (less context switching)
- Tech debt: Managed proactively (reduced)
- Product velocity: +10% expected

WHAT'S THE IMPACT ON OTHER DOMAINS?

Financial Domain:
- Runway drops from 8.5 to 7.2 months
- Product velocity improves → higher revenue potential
- Net: Trade short-term runway for long-term capability

Product Domain:
- Quality improves (dedicated focus on tech debt)
- Velocity stays steady or improves
- Bug rate could decrease
- Impact: Product domain health +5-10 points

Team Domain:
- Better management = improved satisfaction
- Clear growth path = retention
- Team health: +3-5 points

OVERALL IMPACT:
Health score improvement: +2-4 points
Runway cost: -1.3 months
Verdict: Marginal improvement, but feasible

RECOMMENDATION:
HIRE if:
- You want to prioritize product quality and team health
- You can close Series A in next 9 months (extend runway)
- You want to accelerate feature velocity

DON'T HIRE if:
- Runway is critical concern
- Team is small enough for CEO/CTO to manage
- Focus is on revenue growth (not quality)

DECISION FRAMEWORK:
- If Series A likely: HIRE
- If bootstrapping: WAIT
- If runway < 6 months: WAIT

YOUR SITUATION: Series A in 6-9 months likely
RECOMMENDATION: HIRE now to improve metrics for investors
```

### 5. Trend Analysis & Alerts

**Predictive alerts:**
```
TREND ANALYSIS - 90 DAY OUTLOOK

POSITIVE TRENDS:
✅ Revenue growing 12% MoM consistently
   - Projection: $60k MRR by end of Q1
   - Confidence: HIGH (6 months consistent data)

✅ Customer satisfaction improving
   - NPS trend: 45 → 48 (↑0.5 pts/month)
   - Projection: 52 by end of Q1
   - Confidence: MEDIUM (recent improvement)

NEGATIVE TRENDS:
⚠️ Runway declining with hiring plans
   - Current: 8.5 months
   - Projection: 6.8 months by end of Q1
   - Action needed: Plan Series A or cut spending

⚠️ Product engagement declining
   - DAU/MAU: 55% → 50% (↓1.7% per month)
   - Projection: 45% by end of Q1 if unchanged
   - Action needed: Investigate and fix urgently

⚠️ Team satisfaction drifting down
   - Score: 6.8 → 6.2 (↓0.2 per month)
   - Projection: 5.6 by end of Q1 (unacceptable)
   - Action needed: Address this month

INFLECTION POINTS TO WATCH:
1. If churn increases 1%+ → Revenue growth stops → Crisis
   Current: 2.1%, Safe until: 3.1%
   Time to inflection: ~3-4 months if trend continues

2. If DAU/MAU drops below 40% → Product-market fit questioned
   Current: 50%, Safe until: 40%
   Time to inflection: ~2-3 months if trend continues

3. If runway drops below 6 months → Must fundraise or cut
   Current: 8.5 months, Safe until: 6 months
   Time to inflection: ~3-4 months with current burn
```

## Command Reference

### Monitoring & Digests

```
Today's health check
- Automatic daily digest
- 5-minute summary
- Red flags, green flags, action items

Weekly digest
- Comprehensive domain analysis
- Anomalies and trends
- Recommended focus areas

Monthly strategic review
- In-depth analysis of all 13 domains
- Anomaly investigation
- Decision frameworks
- 90-day forecast

Domain deep dive
- Focus on one domain (e.g., Financial)
- Detailed metrics and trends
- Benchmarking vs. industry
- Specific recommendations
```

### Simulations & Scenarios

```
Simulate decision
- Decision: what you're considering
- Timeframe: 3 months? 12 months?
- Output: Impact on all domains + health score

What-if analysis
- Variable: what's changing (e.g., "lose top customer")
- Impact: how does it cascade through business?
- Mitigation: what would you do?
- Output: Scenario modeling with probabilities

Stress test business
- Scenario: economic downturn, key person leaves, etc.
- Severity: severe, moderate, mild
- Output: Survival analysis + recovery options
```

### Alerts & Monitoring

```
Set alert threshold
- Domain: which domain to monitor
- Metric: specific metric
- Threshold: trigger point
- Action: what to do if triggered

Anomaly report
- Timeframe: last week, last month, all-time
- Severity: all, warnings only, critical only
- Output: List of anomalies with analysis

Trend analysis
- Domain: which domain
- Timeframe: 30, 60, 90 days
- Output: Trend lines, inflection points, projections
```

## Triggers & Keywords

User says any of:
- "How's my business doing?"
- "Health check"
- "Monthly digest"
- "What's wrong?"
- "Any anomalies?"
- "What if we..."
- "Simulate hiring..."
- "Trend analysis for..."
- "Domain health for..."
- "Should we..."
- "When will we..."
- "Is everything OK?"

## Integration Points

Cognitive Twin works with:
- **Founder OS** - Business data, metrics, vault
- **AI Phill** - Strategic implications of changes
- **Analytics systems** - Metrics ingestion
- **CRM systems** - Customer data
- **Financial systems** - Revenue, expense data
- **Team/HR systems** - Team metrics
- **Product analytics** - User behavior data
- **Claude Opus** - Extended Thinking for deep analysis

## Version 1 Scope

**What we deliver:**
- 13-domain health scoring system
- Daily, weekly, monthly digest templates
- Real-time anomaly detection
- Decision simulation framework
- Trend analysis and forecasting
- Alert trigger configuration

**What we don't deliver (Post-V1):**
- Real-time API integrations (Stripe, Slack, etc.)
- Automated data ingestion from all systems
- Machine learning for anomaly detection
- Predictive modeling (ML)
- Automated decision recommendations

---

**Core Philosophy**: Your business is a complex system.
Monitor all 13 domains regularly. Anomalies are warnings.
Simulate decisions before executing. The Cognitive Twin
is your always-on safety system.
