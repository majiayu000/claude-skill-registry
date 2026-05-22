---
name: sequence-performance
version: 1.0.0
description: >
  Email campaign/sequence performance review composite. Pulls campaign data
  (sends, opens, replies, bounces), reads actual email copy and subject lines,
  analyzes reply content (objections, positive interest, questions), and produces
  a diagnostic report covering quantitative metrics, copy quality, lead quality,
  and actionable recommendations. Tool-agnostic — works with any outreach
  platform (Smartlead, Instantly, Outreach, Lemlist, Apollo, or CSV data).
tags: [research]

graph:
  provides:
    - campaign-performance-report    # Full diagnostic with metrics + qualitative analysis
    - copy-quality-assessment        # Analysis of subject lines and email body effectiveness
    - lead-quality-assessment        # Analysis of who we're sending to and response patterns
    - optimization-recommendations   # What to double down on, what to fix, what to kill
  requires:
    - campaign-data                  # Campaign metrics, email copy, reply content
    - your-company-context           # What you sell, who you sell to (for copy evaluation)
  connects_to:
    - skill: email-drafting
      when: "Report recommends rewriting email copy or testing new variants"
      passes: copy-quality-assessment, optimization-recommendations
    - skill: cold-email-outreach
      when: "Report recommends launching a new variant or re-engagement campaign"
      passes: optimization-recommendations
  capabilities: [data-analysis, email-analysis, reporting]
---

# Sequence Performance

Goes beyond vanity metrics. Most campaign reports tell you open rate and reply rate. This composite reads the actual emails you sent, reads every reply you received, classifies the responses, evaluates your copy, evaluates your lead quality, and tells you specifically what's working, what's not, and what to do about it.

**Three layers of analysis:**
1. **Quantitative:** The numbers — sends, opens, replies, bounces, conversions, by touch and by variant
2. **Qualitative (Copy):** Are the subject lines, email bodies, CTAs, and personalization actually good? What's landing and what's falling flat?
3. **Qualitative (Replies):** What are people actually saying? What objections keep coming up? What's generating genuine interest?

## When to Auto-Load

Load this composite when:
- User says "how's my campaign doing", "sequence performance", "campaign review", "email analytics"
- User says "analyze my outreach", "why isn't my campaign working", "review my email results"
- An upstream workflow (Pipeline Ops, weekly review) triggers a campaign performance check
- A campaign has been running for 7+ days and has meaningful data

---

## Step 0: Configuration (One-Time Setup)

On first run, collect and store these preferences. Skip on subsequent runs.

### Outreach Tool Config

| Question | Options | Stored As |
|----------|---------|-----------|
| What outreach tool do you use? | Smartlead / Instantly / Outreach.io / Lemlist / Apollo / Other | `outreach_tool` |
| How do we access campaign data? | MCP tools / API / CSV export / Dashboard screenshots | `access_method` |

### Your Company Context (for copy evaluation)

| Question | Purpose | Stored As |
|----------|---------|-----------|
| What does your company do? | Evaluate if copy communicates value clearly | `company_description` |
| Who is your ICP? (titles, industries, company size) | Evaluate lead quality | `icp_definition` |
| What problem do you solve? | Evaluate if copy addresses the right pain | `pain_point` |
| What proof points do you have? | Evaluate if copy uses them effectively | `proof_points` |
| What's your CTA goal? (book meeting, get reply, drive to page) | Evaluate CTA effectiveness | `cta_goal` |

### Benchmark Context

| Question | Purpose | Stored As |
|----------|---------|-----------|
| Is this cold outreach or warm/nurture? | Benchmark calibration — cold has lower expected rates | `outreach_type` |
| What industry are you selling into? | Industry-specific benchmarks | `target_industry` |
| Are you selling to SMB, mid-market, or enterprise? | Segment-specific benchmarks | `target_segment` |

**Store config in:** `clients/<client-name>/config/sequence-performance.json` or equivalent.

---

## Step 1: Pull Campaign Data

**Purpose:** Extract all campaign data: metrics, email copy, and reply content.

### Input Contract

```
campaign_selection: {
  campaign_id: string | null        # Specific campaign ID (if known)
  campaign_name: string | null      # Campaign name to search for
  date_range: {                     # Optional — pull all data if not specified
    start_date: string
    end_date: string
  } | null
  include_replies: boolean          # Default: true — pull actual reply text
}
outreach_tool: string               # From config
access_method: string               # From config
```

### Process

Pull three categories of data:

#### A) Campaign Metrics

| Data Point | What We Need |
|-----------|-------------|
| Total emails sent | By touch (Touch 1, Touch 2, Touch 3, etc.) |
| Total unique recipients | Deduplicated count of people emailed |
| Opens | By touch, unique opens vs. total opens |
| Replies | By touch, total reply count |
| Bounces | Hard bounces + soft bounces |
| Unsubscribes | Count |
| Clicks | If link tracking is on (by touch) |
| Positive replies | If categorized in the tool |
| Meetings booked | If tracked in the tool |

**By outreach tool:**

| Tool | How to Pull Metrics |
|------|-------------------|
| **Smartlead** | `get_campaign_stats`, `get_campaign_analytics`, `get_campaign_variant_statistics`, `get_campaign_sequence_analytics` |
| **Instantly** | CSV export from dashboard or API |
| **Outreach.io** | Sequence analytics API or CSV export |
| **Lemlist** | Campaign analytics API or CSV export |
| **Apollo** | Sequence analytics or CSV export |
| **Other/CSV** | User provides CSV with columns: email, status, opened, replied, bounced |

#### B) Email Copy (Sequence Content)

Pull the actual email templates/copy for every touch in the sequence:

| Data Point | What We Need |
|-----------|-------------|
| Subject lines | For each touch and each variant (A/B tests) |
| Email body | Full text for each touch and each variant |
| Personalization fields | What merge fields are used |
| Sequence timing | Days between touches |
| Variant split | If A/B testing, what % goes to each variant |

**By outreach tool:**

| Tool | How to Pull Copy |
|------|-----------------|
| **Smartlead** | `get_campaign_sequences` |
| **Instantly** | CSV export or API |
| **Others** | CSV export or user pastes the copy |

#### C) Reply Content

Pull the actual text of every reply received:

| Data Point | What We Need |
|-----------|-------------|
| Reply text | Full reply body |
| Reply sender | Name, title, company |
| Which touch triggered the reply | Touch 1, 2, 3, etc. |
| Reply category | If already categorized in the tool (interested, not interested, etc.) |
| Thread context | The email they replied to |

**By outreach tool:**

| Tool | How to Pull Replies |
|------|-------------------|
| **Smartlead** | `get_campaign_leads_history`, `fetch_master_inbox_replies`, `get_campaign_lead_message_history` |
| **Instantly** | CSV export of replies |
| **Others** | CSV export or user provides reply dump |

### Data Standardization

Normalize into a standard structure:

```
campaign_data: {
  campaign_name: string
  campaign_id: string
  date_range: { start: string, end: string }
  status: "active" | "paused" | "completed"

  metrics: {
    total_sent: integer
    unique_recipients: integer
    total_opens: integer
    unique_opens: integer
    total_replies: integer
    bounces: integer
    unsubscribes: integer
    clicks: integer | null
    meetings_booked: integer | null
  }

  sequence: [
    {
      touch_number: integer
      delay_days: integer               # Days after previous touch
      variants: [
        {
          variant_id: string            # "A", "B", etc.
          subject: string
          body: string
          personalization_fields: string[]
          metrics: {
            sent: integer
            opens: integer
            replies: integer
            bounces: integer
          }
        }
      ]
    }
  ]

  replies: [
    {
      sender_name: string
      sender_title: string | null
      sender_company: string | null
      sender_email: string
      reply_text: string
      reply_date: string
      triggered_by_touch: integer
      triggered_by_variant: string | null
      existing_category: string | null  # Tool's categorization if any
    }
  ]

  lead_list_summary: {
    total_leads: integer
    by_title: [ { title: string, count: integer } ] | null
    by_industry: [ { industry: string, count: integer } ] | null
    by_source: [ { source: string, count: integer } ] | null
  } | null
}
```

### Human Checkpoint

```
## Campaign Data Pulled

Campaign: [name]
Status: [active/paused/completed]
Date range: [start] to [end]
Sent: X emails to Y recipients
Replies received: Z (full text pulled for analysis)
Touches: N touches, M variants
Lead data available: [yes/partial/no]

Data looks complete? (Y/n)
```

---

## Step 2: Quantitative Analysis

**Purpose:** Calculate all performance metrics, benchmark against industry standards, and identify statistical patterns. Pure computation.

### Input Contract

```
campaign_data: { ... }                # From Step 1
outreach_type: string                 # From config ("cold" or "warm")
target_segment: string                # From config ("smb", "mid-market", "enterprise")
```

### Benchmarks

Calibrate expectations based on outreach type and segment:

| Metric | Cold (SMB) | Cold (Mid-Market) | Cold (Enterprise) | Warm/Nurture |
|--------|-----------|-------------------|-------------------|-------------|
| Open rate | 40-60% | 30-50% | 25-40% | 50-70% |
| Reply rate | 3-8% | 2-5% | 1-3% | 10-20% |
| Positive reply rate | 1-3% | 0.5-2% | 0.3-1% | 5-10% |
| Bounce rate | <3% | <3% | <2% | <1% |
| Unsubscribe rate | <1% | <1% | <0.5% | <0.5% |

### Metrics Calculation

#### A) Overall Campaign Metrics

| Metric | Formula | Benchmark Comparison |
|--------|---------|---------------------|
| Open rate | unique_opens / (total_sent - bounces) | vs. benchmark |
| Reply rate | total_replies / (total_sent - bounces) | vs. benchmark |
| Bounce rate | bounces / total_sent | vs. benchmark |
| Unsubscribe rate | unsubscribes / (total_sent - bounces) | vs. benchmark |
| Click rate | clicks / (total_sent - bounces) | If tracked |
| Positive reply rate | positive_replies / (total_sent - bounces) | vs. benchmark |
| Meeting conversion | meetings_booked / total_replies | If tracked |
| Deliverability rate | (total_sent - bounces) / total_sent | Should be >97% |

#### B) Per-Touch Breakdown

For each touch in the sequence:

| Metric | What It Tells You |
|--------|------------------|
| Touch-level open rate | Which subject lines are working |
| Touch-level reply rate | Which emails generate responses |
| Marginal reply rate | Replies from THIS touch / people who received this touch but hadn't replied yet |
| Drop-off rate | % of recipients who opened previous touch but didn't open this one |
| Touch contribution | What % of total replies came from each touch |

#### C) Variant Analysis (A/B Testing)

If multiple variants exist per touch:

| Metric | What It Tells You |
|--------|------------------|
| Variant open rate | Which subject line wins |
| Variant reply rate | Which email body wins |
| Statistical confidence | Is the difference real or noise? (Need ~100+ sends per variant for meaningful data) |
| Winner declaration | Which variant to scale, which to kill |

**Statistical significance check:**
- <50 sends per variant → "Insufficient data — too early to call"
- 50-100 sends → "Directional — [variant] is leading but not conclusive"
- 100-250 sends → "Likely winner — [variant] outperforms by X%"
- 250+ sends → "Statistically significant — scale [variant], kill [other]"

#### D) Temporal Patterns

| Metric | What It Tells You |
|--------|------------------|
| Reply rate by day of week | When do people respond most? |
| Reply rate by time of day | Morning vs. afternoon vs. evening response patterns |
| Open-to-reply time | How long between opening and replying? (Instant = strong hook. Days later = mulled it over) |
| Reply velocity trend | Are replies accelerating or decelerating over the campaign's life? |

### Output Contract

```
quantitative_analysis: {
  overall: {
    open_rate: percentage
    reply_rate: percentage
    positive_reply_rate: percentage
    bounce_rate: percentage
    unsubscribe_rate: percentage
    click_rate: percentage | null
    meeting_conversion: percentage | null
    deliverability_rate: percentage
  }
  vs_benchmark: {
    open_rate: "above" | "at" | "below"
    reply_rate: "above" | "at" | "below"
    bounce_rate: "healthy" | "concerning" | "critical"
    assessment: string                 # One-line summary
  }
  by_touch: [
    {
      touch_number: integer
      sent: integer
      open_rate: percentage
      reply_rate: percentage
      marginal_reply_rate: percentage
      reply_contribution: percentage   # What % of total replies came from this touch
    }
  ]
  by_variant: [
    {
      touch_number: integer
      variant_id: string
      subject: string                  # For quick reference
      sent: integer
      open_rate: percentage
      reply_rate: percentage
      confidence: string               # "insufficient", "directional", "likely", "significant"
      recommendation: string           # "scale", "keep testing", "kill"
    }
  ] | null
  temporal: {
    best_day: string
    best_time: string
    avg_open_to_reply_hours: float
    velocity_trend: "accelerating" | "steady" | "decelerating"
  } | null
}
```

No human checkpoint — feeds directly into the next analyses.

---

## Step 3: Reply Analysis

**Purpose:** Read every reply, classify it, extract objection patterns, and assess what the replies tell us about copy and lead quality. Pure LLM reasoning.

### Input Contract

```
replies: [...]                        # From Step 1 campaign_data.replies
your_company: {
  description: string
  pain_point: string
  icp_definition: string
}
```

### Process

#### A) Reply Classification

Read each reply and classify into categories:

| Category | Definition | Example |
|----------|-----------|---------|
| **Positive interest** | Wants to learn more, open to a conversation | "Sure, let's set up a call" |
| **Meeting request** | Explicitly asks to meet or provides availability | "How about Tuesday at 2pm?" |
| **Warm / Curious** | Interested but non-committal, asks questions | "Interesting — what does pricing look like?" |
| **Objection — Timing** | Not now, but potentially later | "We're locked into a contract until Q4" |
| **Objection — Budget** | Can't afford or not a priority | "Not in our budget right now" |
| **Objection — Competitor** | Already using a competing solution | "We already use [competitor]" |
| **Objection — Relevance** | Doesn't see the fit | "We don't have that problem" |
| **Objection — Authority** | Not the right person | "I'm not the one who handles this" |
| **Not interested** | Flat no, don't contact again | "Not interested, please remove me" |
| **Auto-reply / OOO** | Automated response, out of office | "I'm out of the office until..." |
| **Bounce / Undeliverable** | Technical failure | "Mailbox not found" |
| **Referral** | Redirects to someone else at the company | "You should talk to Sarah on our team" |
| **Question** | Asks a specific question about product/offering | "Does this integrate with Salesforce?" |

#### B) Objection Pattern Analysis

Group objections and identify patterns:

| Analysis | What to Look For |
|----------|-----------------|
| Top objection type | Which objection appears most? This reveals a systemic issue. |
| Objection by touch | Do objections cluster at Touch 1 (bad targeting) vs. Touch 3 (fatigue)? |
| Objection by variant | Does one variant trigger more "not relevant" objections? |
| Objection language | What exact words do people use? (Reveals how they think about the problem) |
| Handleable vs. terminal | Which objections can be overcome (timing, authority) vs. which are disqualifying (relevance)? |

#### C) Positive Signal Analysis

For positive replies and warm responses:

| Analysis | What to Look For |
|----------|-----------------|
| What triggered interest | Which touch/variant generated the positive reply? What did it say that worked? |
| Common interest patterns | What do positive responders have in common? (Title, industry, company size) |
| Specific phrases that resonated | Quote the exact lines from replies that show what hooked them |
| Questions asked | What do warm leads want to know? (Reveals what's missing from the email) |

#### D) Reply Quality Score

Aggregate assessment:

| Score | Criteria |
|-------|---------|
| **Strong** | >50% of replies are positive/warm/questions. Objections are handleable (timing, authority). Few "not relevant." |
| **Mixed** | 30-50% positive. Mix of handleable and terminal objections. Some "not relevant" — possible targeting issue. |
| **Weak** | <30% positive. Dominated by "not interested" and "not relevant." Signals a targeting or copy problem. |
| **Toxic** | High unsubscribe + "remove me" + angry replies. Something is fundamentally wrong (bad list, offensive copy, too aggressive). |

### Output Contract

```
reply_analysis: {
  total_replies: integer
  classification: [
    { category: string, count: integer, percentage: percentage }
  ]
  reply_quality_score: "strong" | "mixed" | "weak" | "toxic"
  reply_quality_reasoning: string

  objection_patterns: {
    top_objection: { type: string, count: integer, example_quotes: string[] }
    objections_by_touch: [ { touch: integer, objection_type: string, count: integer } ]
    handleable_objections: [ { type: string, count: integer, suggested_handle: string } ]
    terminal_objections: [ { type: string, count: integer, implication: string } ]
  }

  positive_signals: {
    interest_triggers: [ { touch: integer, variant: string | null, pattern: string } ]
    common_responder_traits: string     # What positive responders have in common
    resonating_phrases: string[]        # Exact quotes from positive replies
    common_questions: string[]          # Questions warm leads are asking
  }

  notable_replies: [                    # 5-10 most instructive replies
    {
      category: string
      sender_info: string               # Title @ Company
      quote: string                     # Key excerpt
      insight: string                   # What this tells us
    }
  ]
}
```

---

## Step 4: Copy Quality Assessment

**Purpose:** Evaluate the actual email copy — subject lines, body, personalization, CTA — against best practices and against what the reply data tells us. Pure LLM reasoning.

### Input Contract

```
sequence: [...]                       # From Step 1 campaign_data.sequence (the actual emails)
quantitative_analysis: { ... }        # From Step 2 (which touches/variants perform)
reply_analysis: { ... }               # From Step 3 (what replies say about the copy)
your_company: {
  description: string
  pain_point: string
  proof_points: string[]
  cta_goal: string
}
```

### Process

Evaluate each touch and variant across these dimensions:

#### A) Subject Line Analysis

For each subject line:

| Criterion | What to Check | Red Flags |
|-----------|--------------|-----------|
| Length | Under 50 characters? | >60 chars gets truncated on mobile |
| Specificity | Does it reference something specific (signal, company, pain)? | Generic "Quick question" or "Checking in" |
| Curiosity gap | Does it create a reason to open? | Obvious pitch in subject line |
| Spam trigger words | Any words that trigger spam filters? | "Free", "Limited time", "Act now", ALL CAPS |
| Consistency with body | Does the email deliver on the subject line's promise? | Clickbait subject → unrelated body |
| Open rate correlation | Cross-reference with Step 2 open rates | Low open rate = subject line problem |

**Subject line verdict per variant:**
- **Working:** Above-benchmark open rate. Keep it.
- **Underperforming:** Below-benchmark open rate. Diagnose why and suggest alternatives.
- **Spam-flagged:** Very low open rate + high bounce rate. Likely hitting spam filters.

#### B) Email Body Analysis

For each email body:

| Criterion | What to Check | Red Flags |
|-----------|--------------|-----------|
| **Hook (first line)** | Does it lead with the recipient or with you? | "I'm reaching out because..." or "We are a company that..." |
| **Length** | Touch 1: 50-90 words. Touch 2+: 30-50 words. | Walls of text. Over 150 words. |
| **Value proposition clarity** | Can a reader understand what you do in one sentence? | Jargon, vague language, buzzwords |
| **Proof points** | Does it include specific evidence (numbers, customers, results)? | No proof = no credibility. Generic claims. |
| **Personalization** | Does it reference something specific to the recipient? | Only {first_name} merge field. No company or role context. |
| **CTA** | Single, clear, low-friction call to action? | Multiple CTAs. High-friction asks ("book a 60-min demo"). No CTA at all. |
| **Tone** | Matches the audience? Casual for SMB, professional for enterprise? | Too formal for startups. Too casual for enterprise VP. |
| **Filler language** | Any banned phrases from email-drafting hard rules? | "Hope this finds you well", "just checking in", "touching base" |
| **Sequence progression** | Does each touch add new value or just repeat? | Touch 2 is a "bump" of Touch 1. Same CTA repeated. |
| **Reply correlation** | Cross-reference body quality with reply rates from Step 2 | Good copy + low replies = targeting problem. Bad copy + low replies = copy problem. |

#### C) Personalization Assessment

| Level | What It Looks Like | Assessment |
|-------|-------------------|-----------|
| **None** | Same email to everyone, no merge fields | "Personalization is absent — this reads like a mass blast" |
| **Tier 1 (Fields only)** | {first_name}, {company} — but template is identical | "Minimal personalization — merge fields but no segment-specific content" |
| **Tier 2 (Segment)** | Different templates per industry/role/signal | "Segment-level personalization — good for scale" |
| **Tier 3 (Individual)** | Unique references per person (their post, their signal) | "Deep personalization — excellent for high-value targets" |

#### D) Sequence Architecture Assessment

| Criterion | What to Check |
|-----------|--------------|
| Touch count | Are there enough touches? (3-5 is standard. 1-2 is too few. 7+ is too many.) |
| Timing | Are delays appropriate? (Too short = annoying. Too long = forgotten.) |
| Angle diversity | Does each touch bring a new angle or just repeat? |
| Escalation | Does the sequence build urgency or stay flat? |
| Breakup | Is there a clean exit ramp at the end? |

### Output Contract

```
copy_assessment: {
  overall_grade: "A" | "B" | "C" | "D" | "F"
  overall_summary: string              # 2-3 sentence assessment

  subject_lines: [
    {
      touch: integer
      variant: string
      subject: string
      open_rate: percentage
      verdict: "working" | "underperforming" | "spam_risk"
      issues: string[]
      suggested_alternative: string | null
    }
  ]

  email_bodies: [
    {
      touch: integer
      variant: string
      word_count: integer
      hook_quality: "strong" | "adequate" | "weak"
      value_prop_clarity: "clear" | "muddled" | "missing"
      proof_usage: "strong" | "weak" | "none"
      personalization_level: "tier_1" | "tier_2" | "tier_3" | "none"
      cta_quality: "clear_low_friction" | "clear_high_friction" | "unclear" | "missing"
      issues: string[]
      rewrite_suggestions: string[]
    }
  ]

  sequence_architecture: {
    touch_count_verdict: string
    timing_verdict: string
    angle_diversity_verdict: string
    overall_flow: string
  }

  strongest_element: string            # What's working best in the copy
  weakest_element: string              # What needs the most work
}
```

---

## Step 5: Lead Quality Assessment

**Purpose:** Evaluate whether we're sending to the right people. Even perfect copy will fail if the audience is wrong. Cross-references reply patterns with lead data.

### Input Contract

```
lead_list_summary: { ... } | null     # From Step 1 (if available)
reply_analysis: { ... }               # From Step 3
quantitative_analysis: { ... }        # From Step 2
icp_definition: string                # From config
```

### Process

#### A) Targeting Assessment

| Check | What to Look For | Red Flags |
|-------|-----------------|-----------|
| Title match | Do lead titles match ICP buyer/champion/user personas? | Sending to roles that don't buy or use |
| Industry match | Are leads in target industries? | Off-ICP industries in the list |
| Seniority match | Right level for the ask? | Too junior (can't buy) or too senior (won't read cold email) |
| Company size match | Are companies in the target range? | Too small (can't afford) or too large (won't respond to cold) |

#### B) Signal Quality (Inferred from Replies)

| Pattern | What It Tells You |
|---------|------------------|
| High "not relevant" replies | We're sending to people who don't have the problem |
| High "wrong person" replies | Right companies, wrong roles |
| High "already have a solution" replies | Right problem, but late to the party |
| High "timing" objections | Right people, right problem, wrong moment — not a targeting issue |
| Low reply rate + high open rate | People open but don't find it relevant — copy/targeting mismatch |
| High bounce rate | List quality issue — bad emails, old data |

#### C) Responder Profile Analysis

If we have data on who replied positively:
- What titles responded most?
- What industries?
- What company sizes?
- Is there a pattern that differs from the overall send list?

This reveals the "actual ICP" vs. the "intended ICP" — sometimes they diverge.

### Output Contract

```
lead_quality: {
  overall_grade: "A" | "B" | "C" | "D" | "F"
  overall_summary: string

  targeting_assessment: {
    title_fit: "aligned" | "partially_aligned" | "misaligned"
    industry_fit: "aligned" | "partially_aligned" | "misaligned"
    issues: string[]
  }

  signal_quality: {
    primary_signal: string              # What the reply patterns suggest about targeting
    evidence: string[]                  # Specific data points
  }

  responder_profile: {
    most_responsive_titles: string[]
    most_responsive_industries: string[]
    actual_vs_intended_icp: string      # How the responding audience differs from targeting
  } | null

  recommendations: string[]
}
```

---

## Step 6: Generate Report

**Purpose:** Synthesize all analyses into a single diagnostic report with two sections: executive summary and detailed breakdown. Plus a prioritized list of actions.

### Input Contract

```
quantitative_analysis: { ... }        # From Step 2
reply_analysis: { ... }               # From Step 3
copy_assessment: { ... }              # From Step 4
lead_quality: { ... }                 # From Step 5
benchmarks: { ... }                   # Calibrated in Step 2
```

### Report Structure

```
# Sequence Performance Review: [Campaign Name]
**Period:** [date range] | **Status:** [active/paused/completed]

---

## Executive Summary

**Overall verdict:** [One sentence: "This campaign is [performing well / underperforming / in trouble] because [key reason]."]

| Dimension | Grade | One-Line Assessment |
|-----------|-------|-------------------|
| Metrics | [A-F] | [e.g., "Reply rate 2x benchmark — strong performance"] |
| Copy Quality | [A-F] | [e.g., "Touch 1 is strong, Touch 2-3 need new angles"] |
| Lead Quality | [A-F] | [e.g., "Targeting is tight but volume is too low"] |
| Reply Quality | [Strong/Mixed/Weak/Toxic] | [e.g., "60% positive — objections are handleable"] |

### What's Working (Double Down)
- [Specific thing that's working, with data]
- [Another]

### What's Not Working (Fix or Kill)
- [Specific thing that's failing, with data]
- [Another]

### Top 3 Actions
1. [Highest-impact action with expected result]
2. [Second]
3. [Third]

---

## Detailed Metrics

### Overall Performance
| Metric | Actual | Benchmark | Status |
|--------|--------|-----------|--------|
| Emails sent | X | — | — |
| Deliverability | X% | >97% | [flag] |
| Open rate | X% | Y% | [above/below] |
| Reply rate | X% | Y% | [above/below] |
| Positive reply rate | X% | Y% | [above/below] |
| Bounce rate | X% | <3% | [flag] |
| Meeting conversion | X% | — | — |

### Performance by Touch
| Touch | Sent | Open Rate | Reply Rate | Marginal Reply Rate | % of Total Replies |
|-------|------|-----------|------------|--------------------|--------------------|
| 1 | X | Y% | Z% | Z% | W% |
| 2 | X | Y% | Z% | Z% | W% |
| 3 | X | Y% | Z% | Z% | W% |

[Commentary: which touches are carrying the campaign? Is Touch 2+ adding value or wasting sends?]

### Variant Performance (if A/B testing)
| Touch | Variant | Subject | Sent | Open Rate | Reply Rate | Confidence | Action |
|-------|---------|---------|------|-----------|------------|------------|--------|
| 1 | A | "..." | X | Y% | Z% | Likely | Scale |
| 1 | B | "..." | X | Y% | Z% | Likely | Kill |

---

## Reply Deep Dive

### Reply Classification
| Category | Count | % of Replies | Trend |
|----------|-------|-------------|-------|
| Positive interest | X | Y% | — |
| Meeting request | X | Y% | — |
| Warm / Curious | X | Y% | — |
| Objection — Timing | X | Y% | — |
| Objection — Relevance | X | Y% | [flag if high] |
| Not interested | X | Y% | — |
| Auto-reply / OOO | X | Y% | — |

### Top Objections
| Objection | Count | Handleable? | Suggested Response |
|-----------|-------|------------|-------------------|
| [objection] | X | Yes/No | [how to handle or what it implies] |

### Notable Replies
[5-10 most instructive replies with quotes and what they teach us]

---

## Copy Assessment

### Subject Lines
| Touch | Subject | Open Rate | Verdict | Issue |
|-------|---------|-----------|---------|-------|
| 1 | "..." | X% | Working | — |
| 2 | "..." | X% | Underperforming | Too generic |

### Email Body
| Touch | Grade | Hook | Value Prop | Proof | Personalization | CTA |
|-------|-------|------|-----------|-------|----------------|-----|
| 1 | B+ | Strong | Clear | One proof point | Tier 2 | Clear, low-friction |
| 2 | C | Weak ("just following up") | Repeat of T1 | None new | Tier 1 | Same CTA as T1 |

[Specific rewrite suggestions for underperforming touches]

### Sequence Architecture
- Touch count: [verdict]
- Timing: [verdict]
- Angle diversity: [verdict]
- Overall flow: [verdict]

---

## Lead Quality

### Targeting
| Dimension | Intended | Actual (from responders) | Fit |
|-----------|---------|------------------------|-----|
| Titles | VP Sales, CRO | Sales Managers (mostly) | Partial |
| Industries | SaaS, FinTech | SaaS (90%) | Aligned |
| Company size | 50-500 | 20-200 | Shift down |

[Commentary on targeting gaps]

---

## Recommendations (Prioritized)

### High Priority (Do This Week)
1. **[Action]** — [Data point] → [Expected impact]
2. **[Action]** — [Data point] → [Expected impact]

### Medium Priority (Do This Month)
3. **[Action]** — [Data point] → [Expected impact]
4. **[Action]** — [Data point] → [Expected impact]

### Low Priority (Backlog)
5. **[Action]** — [Data point]

### Kill List
- [Anything that should be stopped — a variant, a touch, a segment]
```

### Recommendation Generation Logic

| Finding | Recommendation Category |
|---------|----------------------|
| Open rate below benchmark | **Subject line rewrite.** Suggest 3 alternatives based on what's working in the best-performing touch/variant. |
| Reply rate below benchmark + open rate fine | **Body copy issue.** The subject line gets them to open, but the email doesn't compel a reply. Focus on hook, proof, CTA. |
| Reply rate below benchmark + open rate below too | **Both.** Subject lines AND body need work. Consider a full sequence rewrite. |
| High "not relevant" objections | **Targeting issue.** Tighten ICP filters. Remove [specific segments] from the list. |
| High "wrong person" referrals | **Title targeting issue.** Shift to [suggested titles] based on who people refer you to. |
| High "already have solution" objections | **Positioning issue.** Add competitive differentiation to the copy. Or consider a displacement-specific variant. |
| High "timing" objections | **Not a problem.** These are future pipeline. Set up a re-engagement sequence for 90 days out. |
| One variant clearly winning | **Scale the winner.** Send 100% to variant [X]. Use the losing variant's slot to test a new idea. |
| Touch 2/3 near-zero marginal replies | **Cut the sequence short** or rewrite later touches with genuinely new angles. |
| High bounce rate | **List hygiene issue.** Verify emails before sending. Remove invalid addresses. Check your data source. |
| Deliverability <95% | **Infrastructure issue.** Check SPF/DKIM/DMARC, warm up sending domains, reduce daily volume. |

### Output Contract

```
report: {
  executive_summary: string           # Markdown formatted
  detailed_report: string             # Markdown formatted
  recommendations: [
    {
      priority: "high" | "medium" | "low" | "kill"
      category: "subject_line" | "body_copy" | "targeting" | "sequence" | "variant" | "infrastructure" | "list_hygiene"
      action: string
      data_point: string
      expected_impact: string
    }
  ]
  rewrite_suggestions: [              # Ready-to-use copy alternatives
    {
      touch: integer
      element: "subject" | "body" | "cta"
      current: string
      suggested: string
      rationale: string
    }
  ] | null
}
```

### Human Checkpoint

Present the executive summary, then offer drill-down:

```
[Executive Summary rendered]

---

Full detailed report available with:
- Touch-by-touch breakdown with open/reply rates
- Every reply classified with quotes
- Copy scored on 6 dimensions per touch
- Lead quality assessment with actual vs intended ICP
- Prioritized recommendations with rewrite suggestions

Want to see the full report? Or act on a specific recommendation?
```

---

## Execution Summary

| Step | Tool Dependency | Human Checkpoint | Typical Time |
|------|----------------|-----------------|--------------|
| 0. Config | None | First run only | 5 min (once) |
| 1. Pull Data | Configurable (Smartlead MCP, API, CSV) | Verify data completeness | 1-2 min |
| 2. Quantitative | None (computation) | None — feeds into report | Automatic |
| 3. Reply Analysis | None (LLM reasoning) | None — feeds into report | Automatic |
| 4. Copy Assessment | None (LLM reasoning) | None — feeds into report | Automatic |
| 5. Lead Quality | None (LLM reasoning) | None — feeds into report | Automatic |
| 6. Generate Report | None (LLM reasoning) | Review executive summary | 5-10 min |

**Total human review time: ~10-15 minutes** for an analysis that would take 1-2 hours of manual campaign review.

---

## Adapting to Data Availability

| Missing Data | What Gets Skipped | Report Still Useful? |
|-------------|-------------------|---------------------|
| Reply text | Steps 3 (reply classification, objection patterns) | Partially — metrics + copy analysis still run |
| Variant data | Variant analysis in Step 2, variant-level copy assessment | Yes — single-variant analysis still runs |
| Lead demographics | Step 5 (lead quality targeting assessment) | Yes — infers targeting quality from reply patterns |
| Open tracking | Open rate analysis | Partially — reply rate + copy analysis still run |
| Meeting/conversion data | Conversion metrics | Yes — everything else still runs |

**Minimum viable data:** Emails sent + reply count + email copy text. Everything else enriches.

---

## Tips

- **Run this at Day 7 and Day 14 of a campaign.** Day 7 catches early problems (deliverability, subject lines). Day 14 gives enough reply volume for meaningful objection analysis.
- **Reply analysis is where the gold is.** Metrics tell you WHAT is happening. Replies tell you WHY.
- **High open rate + low reply rate is a copy problem.** People are interested enough to open but the email doesn't deliver on the subject line's promise.
- **Low open rate + decent reply rate (among openers) is a subject line problem.** The email works — people just aren't seeing it. Fix the subject line and watch replies scale.
- **"Not relevant" objections are the most important signal.** If >20% of replies say "this isn't for me," you have a targeting problem, not a copy problem. No amount of copy rewriting fixes a bad list.
- **Don't kill a variant too early.** You need 100+ sends per variant for directional data. Calling a winner at 30 sends is just reading noise.
- **Touch 2/3 should contribute 30-40% of total replies.** If Touch 1 accounts for 90%+ of replies, your follow-ups aren't adding value — rewrite them with genuinely new angles.
- **Save the objection analysis.** It's product marketing gold. The exact language prospects use to object is the language your website and sales deck should preemptively address.
