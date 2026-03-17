---
name: sales-performance-review
version: 1.0.0
description: >
  Periodic sales performance review composite. Aggregates ALL sales initiatives
  taken in a given period — outbound campaigns, inbound efforts, events, partnerships,
  content, referrals — and measures the impact of each on pipeline and revenue.
  Produces a team-presentable report covering initiative-level performance, cross-initiative
  comparisons, pipeline attribution, what's working, what's not, and where to invest next.
  Tool-agnostic — pulls data from any combination of CRM, outreach tools, and tracking systems.
tags: [research]

graph:
  provides:
    - sales-performance-report       # Full periodic review, presentation-ready
    - initiative-scorecards          # Per-initiative performance cards
    - cross-initiative-comparison    # Side-by-side effectiveness ranking
    - investment-recommendations     # Where to double down, scale back, or kill
  requires:
    - initiative-data                # Data from all sales initiatives in the period
    - pipeline-data                  # Deal/meeting data for attribution
    - your-company-context           # Goals, targets, team structure
  connects_to:
    - skill: sequence-performance
      when: "A specific campaign needs deeper diagnosis"
      passes: campaign_id
    - skill: pipeline-review
      when: "Pipeline state needs deeper analysis"
      passes: period, pipeline_data
  capabilities: [data-analysis, attribution, reporting]
---

# Sales Performance Review

The all-up periodic report. Every other analytics composite looks at one slice — a single campaign's emails, or the pipeline's current state. This one answers the question a founder or sales leader asks in every team meeting: **"What did we do this period, and did it move the needle?"**

It inventories every sales initiative, measures each one's contribution to pipeline and revenue, compares them against each other, and produces a presentation-ready report that the team can review together.

**What makes this different from `pipeline-review` and `sequence-performance`:**

| Composite | Scope | Question It Answers |
|-----------|-------|-------------------|
| `sequence-performance` | One email campaign | "Is this specific campaign working?" |
| `pipeline-review` | Pipeline state | "What does our pipeline look like right now?" |
| `sales-performance-review` | ALL initiatives across the period | "What did we do, what worked, and where should we invest next?" |

This composite can call `sequence-performance` for deeper campaign-level diagnosis and `pipeline-review` for pipeline state — but its primary job is the cross-initiative view.

## When to Auto-Load

Load this composite when:
- User says "sales review", "periodic review", "what did we do this month", "team performance report", "sales standup report"
- User says "prepare for the weekly/monthly/quarterly sales meeting"
- User asks "what's working", "where should we focus", "are our initiatives paying off"
- End of period (weekly, biweekly, monthly, quarterly) review is due

---

## Step 0: Configuration (One-Time Setup)

On first run, collect and store these preferences. Skip on subsequent runs.

### Data Sources

| Question | Purpose | Stored As |
|----------|---------|-----------|
| Where do you track deals/pipeline? | Pipeline attribution | `crm_tool` |
| What outreach tools do you use? | Campaign data pull | `outreach_tools` (list) |
| Do you track initiatives anywhere? (spreadsheet, Notion, project tool) | Initiative inventory | `initiative_tracker` |
| What other sales channels are active? | Ensure complete coverage | `active_channels` |

**Common `active_channels`:**
```
active_channels: [
  "outbound_email",        # Cold email campaigns
  "outbound_linkedin",     # LinkedIn outreach
  "inbound_content",       # Blog, SEO, content marketing
  "inbound_website",       # Website conversions, demo requests
  "events",                # Conferences, webinars, meetups
  "referrals",             # Partner/customer referrals
  "paid_ads",              # Google Ads, LinkedIn Ads, Meta Ads
  "social_organic",        # LinkedIn posts, Twitter, community
  "partnerships",          # Co-selling, integrations, channel
  "product_led",           # Free trial, freemium, PLG
  "warm_outbound"          # Re-engagement, nurture, expansion
]
```

### Team & Goals

| Question | Purpose | Stored As |
|----------|---------|-----------|
| Who is on the sales team? (names + roles) | Per-rep breakdown | `team_members` |
| What are the period targets? | Gap analysis | `targets` |
| What is the review cadence? | Default period length | `review_cadence` |
| Who is the audience for this report? | Adjust depth/tone | `report_audience` |

**Targets structure:**
```
targets: {
  meetings_booked: integer | null
  qualified_opportunities: integer | null
  pipeline_created: number | null       # Dollar value
  deals_closed: integer | null
  revenue_closed: number | null
  other: [                              # Custom KPIs
    { name: string, target: number }
  ]
}
```

**Report audience options:**
- `"team"` — Sales team standup. Tactical, action-oriented. "What do we do next week?"
- `"leadership"` — VP/Founder review. Strategic, trend-focused. "Are we on track? Where to invest?"
- `"board"` — Board/investor update. High-level, metric-heavy. "Is the GTM motion working?"

### Initiative Categories

Define the categories of initiatives the team runs. This creates the taxonomy for the report.

```
initiative_categories: [
  {
    name: "Outbound Email Campaigns"
    data_source: "smartlead"           # or "instantly", "outreach", etc.
    metrics_available: ["sent", "opens", "replies", "meetings"]
  },
  {
    name: "LinkedIn Outreach"
    data_source: "manual_tracking"     # or "dripify", "expandi"
    metrics_available: ["connections_sent", "accepted", "replies", "meetings"]
  },
  {
    name: "Events & Webinars"
    data_source: "spreadsheet"
    metrics_available: ["attended", "leads_captured", "meetings", "pipeline"]
  },
  {
    name: "Inbound / Content"
    data_source: "hubspot"             # or "website_analytics"
    metrics_available: ["visitors", "leads", "mqls", "meetings"]
  },
  {
    name: "Referrals & Partnerships"
    data_source: "crm"
    metrics_available: ["intros", "meetings", "pipeline", "closed"]
  }
]
```

**Store config in:** `clients/<client-name>/config/sales-performance-review.json` or equivalent.

---

## Step 1: Inventory All Initiatives

**Purpose:** Build a complete inventory of every sales initiative executed during the review period. Nothing should be missing from the report.

### Input Contract

```
period: {
  type: "weekly" | "fortnightly" | "monthly" | "quarterly" | "custom"
  start_date: string
  end_date: string
  comparison_period: boolean          # Default: true
}
initiative_categories: [...]          # From config
data_sources: { ... }                 # From config
```

### Process

For each initiative category, pull the list of specific initiatives run during the period:

#### A) Outbound Email Campaigns

Pull from configured outreach tool:

| Tool | How to List Campaigns |
|------|---------------------|
| **Smartlead** | `get_campaigns` → filter by date range |
| **Instantly** | API or CSV export of campaigns active in period |
| **Others** | API, CSV, or user provides list |

For each campaign, capture:
- Campaign name
- Launch date
- Status (active / paused / completed)
- Target audience description
- Total leads loaded
- Current metrics snapshot (sent, opens, replies — detailed analysis comes in Step 3)

#### B) LinkedIn Outreach

Pull from LinkedIn automation tool or manual tracking:
- Campaign/sequence name
- Connection requests sent
- Messages sent
- Period of activity

#### C) Events & Webinars

Pull from tracking spreadsheet, CRM, or user provides:
- Event name
- Date
- Type (conference, webinar, meetup, hosted event)
- Attendees/leads captured
- Follow-up status

#### D) Inbound / Content

Pull from website analytics, CRM, or marketing tool:
- Content published (blog posts, case studies, whitepapers)
- Website traffic / lead form submissions
- Demo requests
- MQL count

#### E) Referrals & Partnerships

Pull from CRM or manual tracking:
- Referral sources (who referred)
- Intro count
- Meeting count

#### F) Any Other Initiatives

Ask the user: "Were there any other sales initiatives this period not captured above?"
- Ad campaigns launched
- Product-led growth experiments
- New channel tests
- One-off outreach efforts (conference follow-up blast, etc.)

### Output Contract

```
initiative_inventory: [
  {
    id: string                         # Generated identifier
    name: string                       # Initiative name
    category: string                   # Which category it belongs to
    channel: string                    # "email", "linkedin", "event", "inbound", "referral", etc.
    launch_date: string
    status: "active" | "paused" | "completed"
    description: string                # 1-2 sentence summary of what this initiative was
    target_audience: string            # Who it was aimed at
    data_source: string                # Where the data came from
    raw_data_available: boolean        # Can we pull detailed metrics?
  }
]
```

### Human Checkpoint

```
## Initiative Inventory — [Period]

Found X initiatives across Y categories:

| # | Initiative | Category | Channel | Launched | Status |
|---|-----------|----------|---------|----------|--------|
| 1 | Q1 Series A Outbound | Outbound Email | Email | Jan 15 | Active |
| 2 | LinkedIn ABM Campaign | LinkedIn Outreach | LinkedIn | Jan 20 | Active |
| 3 | SaaStr Conference | Event | In-person | Feb 5 | Completed |
| 4 | Blog: "State of X" report | Inbound Content | Content | Feb 10 | Active |
| 5 | Partner intro program w/ Acme | Referral | Partner | Jan 1 | Active |

Missing anything? Any initiatives not captured here?
```

---

## Step 2: Pull Initiative-Level Metrics

**Purpose:** For each initiative in the inventory, pull the detailed performance metrics. This is the data collection step — no analysis yet.

### Input Contract

```
initiative_inventory: [...]           # From Step 1
period: { ... }
outreach_tools: [...]                 # From config
crm_tool: string                     # From config
```

### Process

For each initiative, pull metrics appropriate to its channel:

#### Outbound Email Metrics

| Metric | Source |
|--------|--------|
| Emails sent | Outreach tool |
| Unique recipients | Outreach tool |
| Open rate | Outreach tool |
| Reply rate | Outreach tool |
| Positive reply rate | Outreach tool (if categorized) or estimate from reply analysis |
| Bounce rate | Outreach tool |
| Meetings booked | Outreach tool + CRM cross-reference |
| Pipeline created ($) | CRM — deals sourced from this campaign |
| Deals won ($) | CRM — closed deals sourced from this campaign |

#### LinkedIn Outreach Metrics

| Metric | Source |
|--------|--------|
| Connection requests sent | LinkedIn tool or manual count |
| Connections accepted | LinkedIn tool |
| Accept rate | Calculated |
| Messages sent | LinkedIn tool |
| Replies received | LinkedIn tool |
| Reply rate | Calculated |
| Meetings booked | Manual tracking or CRM |
| Pipeline created ($) | CRM |

#### Event Metrics

| Metric | Source |
|--------|--------|
| Attendees / leads captured | Event tool, badge scans, signup list |
| Follow-ups sent | Outreach tool or manual |
| Meetings booked from event | CRM or manual |
| Pipeline created ($) | CRM |
| Cost of event | Finance/budget tracking |
| Cost per meeting | Calculated |

#### Inbound / Content Metrics

| Metric | Source |
|--------|--------|
| Content pieces published | CMS or manual count |
| Website visitors (organic) | Analytics tool |
| Lead form submissions | CRM or marketing tool |
| Demo requests | CRM |
| MQLs generated | CRM or marketing tool |
| Pipeline created ($) | CRM |

#### Referral / Partnership Metrics

| Metric | Source |
|--------|--------|
| Intros received | Manual tracking or CRM |
| Meetings from intros | CRM |
| Conversion rate (intro → meeting) | Calculated |
| Pipeline created ($) | CRM |
| Deals won ($) | CRM |

### Pipeline Attribution

**Critical step:** Connect initiatives to pipeline and revenue. For each deal in the CRM created during the period:
- What initiative sourced it? (first touch attribution)
- What initiative influenced it? (multi-touch, if trackable)
- Current stage
- Dollar value

This creates the bridge between "what we did" and "what it produced."

**Attribution methods (use the best available):**

| Method | Accuracy | When to Use |
|--------|----------|------------|
| CRM source field | High | If reps consistently tag lead source |
| Campaign ID match | High | If outreach tool logs campaign ID on the deal |
| Email/name match | Medium | Match deal contact email to campaign lead lists |
| Time-based proximity | Low | Deal created within 7 days of an initiative = attributed |
| Ask the user | High | For small volume, just ask "where did this deal come from?" |

### Output Contract

```
initiative_metrics: [
  {
    id: string                         # Matches inventory
    name: string
    category: string
    channel: string
    metrics: {
      # Activity metrics (what we did)
      activity_volume: integer          # Emails sent, connections sent, leads captured, etc.
      activity_label: string            # "emails sent", "connections sent", etc.

      # Response metrics (what happened)
      responses: integer                # Replies, accepts, form fills, etc.
      response_rate: percentage
      response_label: string            # "replies", "accepted", "submitted", etc.

      # Meeting metrics (pipeline entry)
      meetings_booked: integer
      meeting_rate: percentage           # Meetings / activity_volume
      meetings_qualified: integer | null
      qualification_rate: percentage | null

      # Pipeline metrics (business impact)
      pipeline_created: number | null    # Dollar value
      deals_created: integer | null
      avg_deal_size: number | null

      # Revenue metrics (if deals closed)
      deals_won: integer | null
      revenue_closed: number | null

      # Efficiency metrics
      cost: number | null                # If cost data available
      cost_per_meeting: number | null
      cost_per_pipeline_dollar: number | null
      roi: number | null                 # Revenue / cost

      # Comparison period
      vs_prior: {
        activity_change: percentage
        response_rate_change: percentage
        meetings_change: percentage
        pipeline_change: percentage
      } | null
    }
  }
]
```

### Human Checkpoint

```
## Metrics Pulled

| Initiative | Activity | Responses | Meetings | Pipeline | Revenue |
|-----------|----------|-----------|----------|----------|---------|
| Q1 Series A Outbound | 2,500 sent | 125 replies (5%) | 18 | $240K | $0 |
| LinkedIn ABM | 300 requests | 180 accepted (60%) | 8 | $120K | $45K |
| SaaStr Conference | 150 leads | 45 follow-ups | 12 | $180K | $0 |
| Blog content | 5 posts | 28 leads | 4 | $50K | $0 |
| Partner intros | 15 intros | 12 meetings | 12 | $200K | $80K |

Pipeline attribution notes:
- X deals could not be attributed to a specific initiative
- Y deals have multi-touch attribution (counted in primary source)

Data look accurate? Any corrections?
```

---

## Step 3: Analyze Initiative Performance

**Purpose:** Score each initiative, compare them against each other, and identify what's working, what's not, and where the gaps are. Pure LLM reasoning + computation.

### Input Contract

```
initiative_metrics: [...]             # From Step 2
targets: { ... }                      # From config
team_members: [...]                   # From config
period: { ... }
```

### Analysis Sections

#### A) Initiative Scorecards

For each initiative, produce a scorecard:

```
Initiative: [Name]
Category: [Category] | Channel: [Channel]
Status: [Active/Paused/Completed]

Activity:    [X sent/captured/etc.]    [+/-Y% vs prior]
Response:    [X replies/accepts]       [Z% rate] [above/at/below benchmark]
Meetings:    [X booked]               [Z% conversion]
Pipeline:    $[X]                     [+/-Y% vs prior]
Revenue:     $[X]                     [if applicable]
Efficiency:  $[X] cost per meeting    [if cost data available]

Grade: [A/B/C/D/F]
Verdict: [One sentence — "Strong performer, scale up" / "Underperforming, diagnose copy" / etc.]
```

**Grading criteria:**

| Grade | Criteria |
|-------|---------|
| **A** | Above benchmark on response rate AND meeting conversion AND pipeline creation. Clear ROI. |
| **B** | At or above benchmark on most metrics. Producing pipeline. Room to optimize. |
| **C** | Mixed results. Some metrics above, some below. Needs specific fixes. |
| **D** | Below benchmark on most metrics. Producing minimal pipeline. Needs overhaul or kill decision. |
| **F** | Failing across all metrics. Negative ROI. Should be stopped or completely rebuilt. |

#### B) Cross-Initiative Comparison

Rank all initiatives on consistent metrics:

| Ranking Dimension | Why It Matters |
|-------------------|---------------|
| **Meetings per dollar** (if cost data available) | Which channel gives most meetings for the spend |
| **Meetings per activity unit** | Email sends vs. LinkedIn requests vs. event attendance — what converts best |
| **Pipeline per meeting** | Which channels produce bigger deals once meetings happen |
| **Speed to pipeline** | Time from initiative start to first pipeline dollar |
| **Win rate by source** | Which channels produce deals that actually close |

#### C) Funnel Analysis (Full Funnel View)

Map the complete funnel across ALL initiatives combined:

```
Total activity → Total responses → Total meetings → Qualified → Pipeline → Won
[X emails+      [Y replies+       [Z meetings]    [W qual]    [$P]      [$R]
 connections+    accepts+
 leads+etc.]     leads]

Conversion rates at each stage:
Activity → Response: X%
Response → Meeting: X%
Meeting → Qualified: X%
Qualified → Pipeline: X%
Pipeline → Won: X%
```

#### D) Gap Analysis

Compare actuals to targets:

| Target | Actual | Gap | Status |
|--------|--------|-----|--------|
| Meetings booked: X | Y | +/-Z | On track / Behind / Ahead |
| Pipeline created: $X | $Y | +/-$Z | On track / Behind / Ahead |
| Revenue closed: $X | $Y | +/-$Z | On track / Behind / Ahead |

If behind on any target:
- Which initiatives need to increase output?
- How much incremental activity is needed to close the gap?
- At current conversion rates, how many more [emails/events/intros] to hit the target?

#### E) Effort vs. Impact Matrix

Classify each initiative into a 2x2:

```
                    HIGH IMPACT
                        │
    SCALE UP            │           OPTIMIZE
    (High impact,       │       (High impact,
     low effort)        │        high effort)
                        │
────────────────────────┼─────────────────────
                        │
    MAINTAIN            │           QUESTION
    (Low impact,        │       (Low impact,
     low effort)        │        high effort)
                        │
                    LOW IMPACT
```

- **Scale Up:** High pipeline/meetings relative to effort. Pour fuel on this fire.
- **Optimize:** Producing results but resource-intensive. Find ways to make it more efficient.
- **Maintain:** Low effort, modest results. Keep running, don't invest more.
- **Question:** High effort, low results. Diagnose why or shut it down.

#### F) Trend Analysis (If Comparison Period Available)

| Metric | Prior Period | Current Period | Trend | Commentary |
|--------|-------------|----------------|-------|-----------|
| Total meetings | X | Y | +/-Z% | [Accelerating/Decelerating] |
| Pipeline created | $X | $Y | +/-Z% | [context] |
| Best channel | [channel] | [channel] | [Same/Shifted] | [context] |
| Qualification rate | X% | Y% | +/-Z pts | [context] |

### Output Contract

```
analysis: {
  initiative_scorecards: [
    {
      id: string
      name: string
      category: string
      grade: "A" | "B" | "C" | "D" | "F"
      verdict: string
      key_metrics_summary: string
    }
  ]

  cross_initiative_ranking: {
    by_meetings_per_dollar: [ { name: string, value: number } ] | null
    by_meeting_conversion: [ { name: string, value: percentage } ]
    by_pipeline_per_meeting: [ { name: string, value: number } ] | null
    by_win_rate: [ { name: string, value: percentage } ] | null
    overall_best_performer: string
    overall_worst_performer: string
  }

  funnel: {
    total_activity: integer
    total_responses: integer
    total_meetings: integer
    total_qualified: integer | null
    total_pipeline: number | null
    total_won: number | null
    stage_conversions: [ { from: string, to: string, rate: percentage } ]
    biggest_drop_off: string          # Which stage loses the most
  }

  gap_analysis: {
    targets_summary: [ { metric: string, target: number, actual: number, gap: number, status: string } ]
    behind_on: string[]               # Which targets are behind
    incremental_needed: string        # "Need X more meetings from Y channel to close the gap"
  } | null

  effort_impact_matrix: {
    scale_up: [ { name: string, reason: string } ]
    optimize: [ { name: string, reason: string } ]
    maintain: [ { name: string, reason: string } ]
    question: [ { name: string, reason: string } ]
  }

  trends: {
    overall_direction: "improving" | "stable" | "declining"
    notable_shifts: string[]
  } | null
}
```

---

## Step 4: Generate Insights & Recommendations

**Purpose:** Distill the analysis into actionable insights — what to double down on, what to fix, what to kill, and what to start. Pure LLM reasoning.

### Process

#### A) What's Working (Double Down)

Identify initiatives or patterns that are clearly producing results:

| Signal | Recommendation |
|--------|---------------|
| Initiative has A/B grade + above-benchmark metrics | "Scale [initiative]: increase volume by X%. It's converting at Y% — the highest across all channels." |
| One channel produces 50%+ of qualified meetings | "Double down on [channel]. It accounts for X% of qualified meetings at Y cost per meeting." |
| Specific audience segment responding well | "The [segment] audience converts at 2x the overall rate. Build a dedicated campaign for this segment." |
| Referral/partner channel has highest win rate | "Invest in the referral program. Win rate is X% vs. Y% for cold outbound. Each intro is worth $Z in expected pipeline." |

#### B) What's Not Working (Fix or Kill)

| Signal | Recommendation |
|--------|---------------|
| Initiative has D/F grade | "Consider killing [initiative]. It's consumed [resources] and produced [minimal results]. Reallocate to [better performer]." |
| Channel has high activity but no pipeline | "Diagnose [channel]. High volume (X sent) but near-zero pipeline. Either targeting, copy, or the channel itself isn't working." |
| Large gap between meetings and qualified meetings | "Meeting quality issue. X meetings booked but only Y qualified (Z%). Review ICP targeting and qualification criteria." |
| High effort, low impact quadrant | "[Initiative] is in the 'Question' quadrant. It's consuming [effort] for [minimal return]. Fix within 2 weeks or shut down." |

#### C) What's Missing (Start)

| Signal | Recommendation |
|--------|---------------|
| Only 1-2 channels active | "Channel concentration risk. X% of pipeline comes from one channel. Test [suggested new channel] as a hedge." |
| No inbound or content effort | "100% outbound. Consider starting a lightweight inbound play (blog, LinkedIn content) to build a compounding pipeline source." |
| No referral program | "Referrals typically convert at 3-5x cold outbound. Start a structured referral ask to existing customers and partners." |
| Strong outbound but no event presence | "Consider attending [industry event]. Events produce higher-ACV pipeline for [segment]." |

#### D) Resource Allocation Recommendation

Based on the effort-impact analysis, recommend how to allocate the team's time next period:

```
Recommended time allocation (next period):
- [Channel A]: Increase from X% → Y% of team time (reason)
- [Channel B]: Maintain at X% (reason)
- [Channel C]: Reduce from X% → Y% or eliminate (reason)
- [New Channel]: Allocate Z% for testing (reason)
```

### Output Contract

```
insights: {
  double_down: [
    { initiative: string, recommendation: string, expected_impact: string, data_point: string }
  ]
  fix_or_kill: [
    { initiative: string, recommendation: string, deadline: string, data_point: string }
  ]
  start: [
    { recommendation: string, rationale: string, effort_estimate: string }
  ]
  resource_allocation: {
    current: [ { channel: string, effort_percentage: percentage } ]
    recommended: [ { channel: string, effort_percentage: percentage, change: string, reason: string } ]
  }
  key_risks: string[]                 # Top 3 risks to next period's targets
}
```

---

## Step 5: Generate Report

**Purpose:** Produce a presentation-ready report that the team can review together. Two formats: the full detailed report and a slide-ready summary.

### Input Contract

```
initiative_inventory: [...]           # From Step 1
initiative_metrics: [...]             # From Step 2
analysis: { ... }                     # From Step 3
insights: { ... }                     # From Step 4
targets: { ... }                      # From config
report_audience: string               # From config
period: { ... }
```

### Report Structure

Adapt depth and tone based on `report_audience`:

| Section | Team | Leadership | Board |
|---------|------|-----------|-------|
| Executive summary | Brief | Detailed | Concise + metrics |
| Initiative scorecards | Full detail | Summary | Top/bottom only |
| Cross-initiative comparison | Full tables | Rankings | Top 3 chart |
| Funnel analysis | Detailed with actions | Stage conversion focus | High-level conversion |
| Stuck/problem areas | Detailed with fix plans | Summary with owners | Mention only |
| Recommendations | Tactical, this-week actions | Strategic, this-quarter | Investment themes |

```
# Sales Performance Review — [Period Type]: [Start Date] to [End Date]

## Executive Summary

**Period overview:** [2-3 sentences: what happened, headline result]

### Scorecard
| Metric | Target | Actual | Status | Trend |
|--------|--------|--------|--------|-------|
| Meetings booked | X | Y | [ahead/behind] | [+/-Z% vs prior] |
| Qualified meetings | X | Y | [ahead/behind] | [+/-Z%] |
| Pipeline created | $X | $Y | [ahead/behind] | [+/-Z%] |
| Revenue closed | $X | $Y | [ahead/behind] | [+/-Z%] |

### Headline Insights
1. **Best performer:** [Initiative] — [one-line result with key number]
2. **Biggest concern:** [Issue] — [one-line description]
3. **Biggest opportunity:** [What to do next] — [expected impact]

---

## Initiative Performance

### Overview
| # | Initiative | Channel | Grade | Meetings | Pipeline | Verdict |
|---|-----------|---------|-------|----------|----------|---------|
| 1 | [name] | Email | A | 18 | $240K | Scale up |
| 2 | [name] | LinkedIn | B | 8 | $120K | Optimize |
| 3 | [name] | Event | B+ | 12 | $180K | Repeat |
| 4 | [name] | Content | C | 4 | $50K | Needs time |
| 5 | [name] | Referral | A | 12 | $200K | Invest more |

### Detailed Scorecards

#### [Initiative 1 Name] — Grade: [X]
**What it is:** [1-sentence description]
**Target audience:** [Who]

| Metric | Value | Benchmark | Status |
|--------|-------|-----------|--------|
| [Activity] | X | — | — |
| Response rate | X% | Y% | [above/below] |
| Meetings booked | X | — | — |
| Meeting conversion | X% | Y% | [above/below] |
| Pipeline created | $X | — | — |
| Cost per meeting | $X | — | [if available] |

**What worked:** [Specific things that performed well]
**What didn't:** [Specific issues]
**Recommendation:** [Scale / Optimize / Fix / Kill]

[Repeat for each initiative]

---

## Cross-Initiative Comparison

### Efficiency Rankings
| Rank | Initiative | Meetings Booked | Meeting Conversion | Pipeline per Meeting | Cost per Meeting |
|------|-----------|----------------|-------------------|---------------------|-----------------|
| 1 | [name] | X | Y% | $Z | $W |
| 2 | [name] | X | Y% | $Z | $W |
| ... |

### Effort vs. Impact Matrix
```
SCALE UP (high impact, efficient):
  • [Initiative] — [why]
  • [Initiative] — [why]

OPTIMIZE (high impact, resource-heavy):
  • [Initiative] — [why]

MAINTAIN (low effort, moderate results):
  • [Initiative] — [why]

QUESTION (high effort, low results):
  • [Initiative] — [why]
```

---

## Full Funnel Analysis

### Aggregate Funnel
```
[Total Activity] → [Responses] → [Meetings] → [Qualified] → [Pipeline] → [Won]
    X,XXX             XXX            XX           XX          $XXX K      $XX K
              X.X%          X.X%          XX%          XX%          XX%
```

### Funnel by Channel
| Channel | Activity | → Response | → Meeting | → Qualified | → Pipeline | → Won |
|---------|----------|-----------|-----------|-------------|-----------|-------|
| Email | X | Y% | Z% | W% | $V | $U |
| LinkedIn | X | Y% | Z% | W% | $V | $U |
| Events | X | Y% | Z% | W% | $V | $U |
| Inbound | X | Y% | Z% | W% | $V | $U |
| Referral | X | Y% | Z% | W% | $V | $U |

**Biggest drop-off:** [Stage] — [X% of pipeline is lost here. Why and what to do.]

---

## Gap Analysis (vs. Targets)

| Target | Goal | Actual | Gap | To Close the Gap |
|--------|------|--------|-----|-----------------|
| Meetings | X | Y | -Z | Need Z more from [best-converting channel] |
| Pipeline | $X | $Y | -$Z | At avg deal size of $W, need Z more qualified meetings |
| Revenue | $X | $Y | -$Z | Need to close X more deals from current pipeline |

**Path to target:** [Specific plan — "If we increase [channel] volume by X% and maintain current conversion, we close the gap in Y weeks."]

---

## Trends (vs. Prior Period)

| Metric | Prior Period | Current Period | Change | Signal |
|--------|-------------|---------------|--------|--------|
| Total meetings | X | Y | +/-Z% | [Improving/Declining] |
| Qualification rate | X% | Y% | +/-Z pts | [context] |
| Pipeline created | $X | $Y | +/-Z% | [context] |
| Best channel | [channel] | [channel] | [Shifted?] | [context] |
| Avg deal size | $X | $Y | +/-Z% | [context] |

[Commentary on what the trends mean]

---

## What's Working (Double Down)

1. **[Initiative/Channel]** — [Evidence with numbers]. Recommendation: [Specific action + expected impact].
2. **[Initiative/Channel]** — [Evidence]. Recommendation: [Action].
3. **[Pattern]** — [Evidence]. Recommendation: [Action].

## What's Not Working (Fix or Kill)

1. **[Initiative/Channel]** — [Evidence]. Recommendation: [Fix plan with deadline OR kill decision].
2. **[Initiative/Channel]** — [Evidence]. Recommendation: [Action].

## What's Missing (Start)

1. **[New initiative]** — [Rationale]. Expected effort: [X]. Expected impact: [Y].

---

## Recommended Resource Allocation (Next Period)

| Channel | Current Effort | Recommended | Change | Reason |
|---------|---------------|-------------|--------|--------|
| Outbound email | X% | Y% | [+/-Z%] | [reason] |
| LinkedIn | X% | Y% | [+/-Z%] | [reason] |
| Events | X% | Y% | [+/-Z%] | [reason] |
| Content/Inbound | X% | Y% | [+/-Z%] | [reason] |
| Referrals | X% | Y% | [+/-Z%] | [reason] |

---

## Action Items

### This Week
| # | Action | Owner | Deadline | Expected Impact |
|---|--------|-------|----------|----------------|
| 1 | [action] | [name] | [date] | [impact] |
| 2 | [action] | [name] | [date] | [impact] |

### This Month
| # | Action | Owner | Expected Impact |
|---|--------|-------|----------------|
| 1 | [action] | [name] | [impact] |

### Key Risks
1. [Risk with mitigation plan]
2. [Risk with mitigation plan]
```

---

## Step 6: Export & Distribute

**Purpose:** Save and optionally distribute the report.

### Output Options

| Destination | Format | Use Case |
|-------------|--------|----------|
| **Markdown file** | `.md` | Default — save to `clients/<client>/reports/` |
| **Google Slides** | Presentation | Team meeting — one slide per section |
| **Notion page** | Database entry | Running log of periodic reviews |
| **Google Sheets** | Data tables | Supplement to the report — raw data for filtering |
| **Email** | Summary | Send executive summary to leadership |
| **stdout** | Display | Quick review in terminal |

---

## Execution Summary

| Step | Tool Dependency | Human Checkpoint | Typical Time |
|------|----------------|-----------------|--------------|
| 0. Config | None | First run only | 5-10 min (once) |
| 1. Inventory | Configurable (CRM, outreach tools) | Confirm all initiatives captured | 3-5 min |
| 2. Pull Metrics | Configurable (CRM, outreach tools) | Verify metrics accuracy | 3-5 min |
| 3. Analyze | None (computation + LLM reasoning) | None — feeds into report | Automatic |
| 4. Insights | None (LLM reasoning) | None — feeds into report | Automatic |
| 5. Generate Report | None (LLM reasoning) | Review final report | 5-10 min |
| 6. Export | Configurable (file, Slides, Notion) | Optional | 1-2 min |

**Total human review time: ~15-25 minutes** for a report that would take 2-4 hours of manual data gathering, spreadsheet building, and analysis.

---

## Cadence Guide

| Review Type | Period | Best For | Focus |
|-------------|--------|----------|-------|
| **Weekly standup** | 7 days | Sales team | Activity metrics, stuck items, this week's priorities |
| **Fortnightly review** | 14 days | Sales manager | Initiative performance, early trend detection |
| **Monthly review** | 30 days | VP Sales / Founder | Full diagnostic, cross-initiative comparison, resource allocation |
| **Quarterly business review** | 90 days | Leadership / Board | Strategic assessment, channel ROI, next quarter planning |

The report depth scales with period length. A weekly review focuses on activity and blockers. A quarterly review focuses on trends, ROI, and strategic allocation.

---

## Tips

- **Attribution is the hardest part.** Don't let perfect be the enemy of good. If you can't do multi-touch attribution, first-touch is fine. If CRM source fields are empty, use email/name matching. Some attribution is infinitely better than none.
- **Compare channels on the same metric.** "We sent 2,500 emails and attended 1 conference" is meaningless. "Email produced 18 meetings at $0.50/meeting. The conference produced 12 meetings at $400/meeting" is actionable.
- **The effort-impact matrix drives resource allocation.** This is the most important visual in the report. It turns a complex multi-channel discussion into four simple quadrants.
- **Include cost data when possible.** Revenue numbers without cost data tell half the story. A $200K pipeline from referrals (free) is very different from $200K from events ($50K cost).
- **Trend direction matters more than absolute numbers.** A 3% reply rate that was 1.5% last month is great. A 5% reply rate that was 8% last month is concerning. Always show the trajectory.
- **End every report with specific action items and owners.** A beautiful report with no actions is a waste. Every insight should map to "who does what by when."
- **Save historical reports.** The real power comes from comparing Q1 review to Q2 to Q3. Trends across review periods reveal strategic shifts that no single report can show.
