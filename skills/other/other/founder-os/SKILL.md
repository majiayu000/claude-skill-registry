---
name: founder-os
description: Manages founder business portfolio, signals, vault, and snapshots. Tracks business health, stores credentials securely, and generates AI-powered business analytics and recommendations.
---

# Founder OS Skill

## Overview

The Founder OS Skill is the **personal business command center** for founders. It:
- Registers and manages founder businesses and ventures
- Tracks business signals (revenue, growth, engagement metrics)
- Maintains secure vault for credentials and sensitive data
- Generates AI-powered business health snapshots
- Provides strategic recommendations based on performance data

## Core Capabilities

### 1. Business Portfolio Management

**When to use:**
- Register a new business/venture
- Update business profile information
- Track business lifecycle (startup → scale → exit)
- Manage multiple concurrent ventures

**Operations:**
```
REGISTER BUSINESS:
- Name, industry, stage
- Founders, team size
- Target market/geography
- Website, social handles

UPDATE BUSINESS:
- Change business metadata
- Update team composition
- Modify market focus
- Track acquisition/pivot status

LIST PORTFOLIO:
- All registered businesses
- Filter by stage, industry
- Sort by health score
- Show engagement timeline
```

**Example prompts:**
- "Register my new SaaS startup"
- "Update my business profile with new team members"
- "Show my complete business portfolio"
- "Which of my businesses needs attention?"

### 2. Business Signals & Metrics

**Signal types:**
- **Revenue signals** - MRR, ARR, growth rate, customer LTV
- **Growth signals** - User acquisition, activation rate, retention cohorts
- **Engagement signals** - Email opens, website visits, social engagement
- **Strategic signals** - Hiring progress, fundraising stage, partnership activity
- **Health signals** - Burn rate, runway, unit economics, market fit score

**When to track:**
- Weekly/monthly metrics updates
- Customer sentiment analysis
- Competitive positioning
- Market trend indicators
- Team productivity and satisfaction

**Example signals dashboard:**
```
Business: TechStartup Inc
Overall Health: 78/100

Revenue:
- MRR: $45,000 (↑12% MoM)
- ARR: $540,000
- LTV: $2,400
- Growth Rate: 8% MoM

Growth:
- New Customers: 34 this month
- Churn Rate: 2.1%
- NRR: 108%

Team:
- Current headcount: 8
- Hiring in progress: 2 roles
- Satisfaction: 8.2/10

Market:
- Market size: $12B
- TAM penetration: 0.04%
- Competitive ranking: #8 in category
```

### 3. Secure Credential Vault

**What to store:**
- API keys (Stripe, AWS, GitHub, etc.)
- Database credentials
- OAuth tokens (encrypted)
- Financial account access
- Customer account credentials
- Private keys and certificates

**Vault security:**
- End-to-end encryption (AES-256)
- Audit trail for all access
- Time-limited access tokens
- Automatic rotation for sensitive credentials
- Recovery codes for emergency access

**Example usage:**
```
STORE CREDENTIAL:
- Type: API Key
- Service: Stripe
- Value: sk_live_... (encrypted)
- Rotation: Every 90 days

RETRIEVE CREDENTIAL:
- Access audit log entry
- Decrypt with user key
- Return to requesting application
- Log access timestamp

SHARE CREDENTIAL:
- Generate limited-access token
- Set expiration (1 hour - 7 days)
- Require MFA for sensitive credentials
```

**Commands:**
- "Save my Stripe API key"
- "Retrieve my database password"
- "Share AWS credentials with Sarah"
- "Rotate all API keys"
- "Show credential access logs"

### 4. AI-Powered Business Snapshots

**Snapshot contents:**
- Executive summary (1-2 paragraphs)
- Key metrics and trends
- Health score with contributing factors
- SWOT analysis (Strengths, Weaknesses, Opportunities, Threats)
- Top 3 opportunities for next month
- Top 3 risks to monitor
- Recommended actions with estimated impact
- Competitive positioning analysis
- Financial forecast (3-month)
- Team health assessment

**Snapshot frequency:**
- Daily (automated): Quick health check (2 minutes)
- Weekly (on-demand): Comprehensive snapshot (10 minutes)
- Monthly (scheduled): Deep strategic analysis with Extended Thinking (20 minutes)
- Custom: Ad-hoc analysis for specific decisions

**Example monthly snapshot:**
```
BUSINESS SNAPSHOT - November 2025
Generated: 2025-11-28 | Next update: 2025-12-28

EXECUTIVE SUMMARY
TechStartup Inc is in a strong growth phase with 108% NRR and expanding
team capacity. Revenue tracking 12% MoM growth. Primary focus should shift
from customer acquisition to retention optimization and market expansion.

HEALTH SCORE: 78/100 (↑3 points from October)
├─ Revenue Health: 82 (strong MRR growth)
├─ Growth Health: 75 (good NRR, managing churn)
├─ Team Health: 72 (hiring on track, engagement solid)
├─ Market Position: 68 (consolidating market share)
└─ Financial Health: 71 (6 months runway, manageable burn)

KEY METRICS
Revenue:
  MRR: $45,000 (↑12% MoM, ↑34% YoY)
  CAC: $850 (↓8% YoY through optimization)
  LTV: $2,400 (↑18% YoY)
  LTV:CAC Ratio: 2.8:1 (healthy)

Growth:
  New Customers: 34 (↑5% vs last month)
  Churn Rate: 2.1% (↓0.3% YoY)
  NRR: 108% (↑2% YoY)
  Activation Rate: 67% (↑3% with onboarding improvements)

STRENGTHS
1. Strong unit economics with improving LTV:CAC ratio
2. Exceptional NRR (108%) indicates strong product-market fit
3. Efficient sales process (CAC payback in 4.2 months)

WEAKNESSES
1. Limited geographic expansion (99% from US market)
2. Team concentration in engineering (75% of headcount)
3. Dependency on single distribution channel (outbound sales)

OPPORTUNITIES
1. International expansion into EU market (2-3x TAM expansion)
2. Partner channel development (reduce CAC by 30%)
3. Product upsell to existing customers (increase LTV by 15%)

THREATS
1. Emerging competitor raising $20M Series B
2. Potential regulatory changes in target industry
3. Economic downturn impacting enterprise budget allocation

RECOMMENDED ACTIONS - NEXT 30 DAYS
1. Launch EU market pilot with $50k budget (expected ROI: 1.8x in 6 months)
2. Onboard first 2 strategic partners (reduce CAC by $200/customer)
3. Implement retention program (target 50 bps churn reduction)

FINANCIAL FORECAST - Q1 2026
Projected MRR: $48,500 (↑7.7% seasonal)
Projected runway: 7.2 months
Burn rate: $120,000/month (slight increase for hiring)
```

### 5. Decision Support & Strategic Analysis

**Use Extended Thinking for:**
- Major business decisions (fundraising, hiring, partnerships)
- Strategy pivots and market changes
- Competitive analysis and positioning
- Financial planning and forecasting
- Team and organizational design
- Product roadmap prioritization

**Decision framework:**
```
DECISION ANALYSIS
Question: "Should we expand to EU market?"

Research:
- Current EU TAM: ~$3.8B (vs $12B US)
- Estimated CAC in EU: +40% vs US
- Regulatory requirements: GDPR, VAT complexity
- Competition: 2 major players + 5 smaller

Analysis (with Extended Thinking):
- Breakeven timeline: 14 months
- Required investment: $250k
- Expected LTV improvement: +8%
- Team capacity: Can support with 2 hires

Recommendation: YES
- Phased approach: pilot > full launch
- Timeline: 6 months
- Success metrics: $15k MRR by month 6
```

## Agent Mode: HUMAN_GOVERNED

**CRITICAL**: Founder OS operates in **HUMAN_GOVERNED** mode:
- All strategic decisions require founder approval
- No automatic business changes
- Advisory only - founder makes final call
- Present options and recommendations
- Flag risks and opportunities
- Provide decision frameworks

**Example interaction:**
```
Founder: "Analyze our expansion options"

Founder OS:
"Based on your metrics, here are 3 expansion paths:

1. GEOGRAPHIC EXPANSION (EU)
   - Timeline: 6 months
   - Investment: $250k
   - Upside: +3x TAM
   - Risk: Regulatory complexity
   - Recommendation: START WITH PILOT

2. PRODUCT EXPANSION (New module)
   - Timeline: 3 months
   - Investment: $100k
   - Upside: +$8k MRR in 6 months
   - Risk: Engineering bandwidth
   - Recommendation: PARALLEL WITH CURRENT

3. ACQUISITION PATH (Buy competitor)
   - Timeline: 2 months to close
   - Investment: $1.2M
   - Upside: +$25k MRR immediate
   - Risk: Integration complexity
   - Recommendation: NOT READY (revenue insufficient)

Which path aligns with your vision?"
```

## Command Reference

### Registration & Portfolio

```
Register business
- Details: name, industry, stage
- Team: founders, headcount
- Market: geography, TAM
- Status: active/paused/exited

Update business profile
- Change any metadata
- Track team changes
- Update market focus

List my portfolio
- All businesses
- Filter by stage
- Sort by metrics

Archive business
- Preserve historical data
- Stop signal tracking
- Keep vault access
```

### Signals & Metrics

```
Track signal
- Type: revenue, growth, engagement, etc.
- Value: numeric or categorical
- Date: when recorded
- Notes: context

Get health score
- Business name
- Calculation includes: all signals
- Trend analysis: vs previous month
- Contributing factors breakdown

Alert setup
- Trigger: metric threshold
- Channel: email, Slack, dashboard
- Frequency: real-time, daily, weekly
```

### Vault Management

```
Store credential
- Service name
- Credential type
- Value (encrypted)
- Rotation schedule

Retrieve credential
- Service name
- Auto-decrypt with user key
- Log access

Share credential
- User/team
- Access duration
- Approval required (MFA)

Rotate credentials
- Automatic: every 90 days
- Manual: on demand
- Generate new key
- Deprecate old key
```

### Snapshots & Analysis

```
Quick snapshot
- 2-minute health check
- Current metrics only
- Trend indicators

Full snapshot
- 10-minute comprehensive review
- All signals + analysis
- SWOT assessment
- Recommendations

Strategic analysis
- Deep thinking with Extended Thinking
- 20+ minute deep analysis
- Decision framework
- Scenario planning
- Risk assessment

Custom analysis
- Specific question/area
- Time allocated: 15-30 minutes
- Focus depth: surface/moderate/deep
```

## Integration Points

Founder OS works with:
- **Business database** - Portfolio storage
- **Analytics engine** - Signal ingestion and trending
- **Vault service** - Encrypted credential storage
- **Claude Opus** - Extended Thinking for deep analysis
- **Calendar/scheduling** - Snapshot scheduling
- **Slack/Email** - Alerts and notifications
- **Other agents** - Business context for decisions

## Example Workflows

### Workflow 1: Daily Health Check

```
TIME: 9:00 AM (automated)

1. Generate quick snapshot for all businesses
2. Identify any metrics outside normal range
3. Flag urgent items (e.g., churn spike, runway < 6mo)
4. Send summary email with action items

OUTPUT:
"Your portfolio health: 76/100 (↓2 points)
- TechStartup Inc: Normal
- ConsultingCo: WARNING - revenue tracking below forecast
- SideProject: Good progress this week

Action item: Review pricing for ConsultingCo"
```

### Workflow 2: Strategic Decision Support

```
TRIGGER: Founder asks "Should we hire VP Sales?"

1. Load current team metrics
2. Analyze hiring capacity and burn rate
3. Model impact on revenue (with different scenarios)
4. Assess competitive hiring pressure
5. Use Extended Thinking for deep analysis
6. Present options with pros/cons

OUTPUT:
"Recommend WAIT 2 MONTHS because:
- Current runway: 8.2 months
- VP Sales salary: $200k/year
- Impact on runway: -3 months (becomes 5.2)
- Breakeven: Need $30k/month uplift
- Current growth trajectory: on pace for +$8k/month

ALTERNATIVE: Hire Sales Manager for $120k (safer option)"
```

### Workflow 3: Monthly Strategic Review

```
TIME: First Monday of month

1. Compile all metric data from past month
2. Calculate health score and trends
3. Run competitive analysis
4. Build 3-month financial forecast
5. Identify top opportunities and risks
6. Generate comprehensive snapshot with recommendations

DELIVERABLE:
- 8-10 page strategic analysis
- Presentation-ready summaries
- Decision frameworks for key areas
- Next month focus areas
```

## Triggers & Keywords

User says any of:
- "Register my business"
- "Track this metric"
- "Save a credential"
- "Generate business snapshot"
- "Should we hire..."
- "Should we pivot..."
- "Analyze our options"
- "How's my business doing?"
- "What's my runway?"
- "Who's the competition?"
- "Recommend next moves"
- "Strategic analysis"

## Error Handling

**Vault access denied:**
- Require MFA for sensitive credentials
- Log all access attempts
- Alert founder of suspicious access

**Metric data missing:**
- Estimate based on historical trends
- Flag gaps in data
- Request missing information

**Conflicting signals:**
- Highlight discrepancies
- Request clarification
- Note in analysis for manual review

**Credential rotation failed:**
- Manual intervention required
- Notify founder immediately
- Provide recovery steps

## Version 1 Scope

**What we deliver:**
- Business registration and portfolio management
- Signal tracking and trending
- Basic health scoring algorithm
- Vault for credential storage (encrypted)
- Weekly snapshot generation
- Email alerts for threshold violations

**What we don't deliver (Post-V1):**
- Real-time financial data integration (Stripe, etc.)
- Competitor real-time monitoring
- Team survey integration
- Revenue forecasting with ML
- Custom alert workflows

---

**Key Principle**: All strategic decisions remain with the founder. Founder OS provides data, analysis, and recommendations - the founder decides.
