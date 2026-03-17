---
name: competitive-strategy-tracker
version: 1.0.0
description: >
  Living competitive strategy system. Maintains persistent competitor profiles with
  timeline tracking of positioning, messaging, features, and pricing changes. Analyzes
  competitors' social content for what's working. Compares against your own positioning
  and recommends messaging, pricing, and strategy adjustments. Consumes competitor-intel
  raw data but focuses on strategic analysis, not data collection. Tool-agnostic —
  works with any data source and stores profiles as local files.
tags: [competitive-intel]

graph:
  provides:
    - competitor-profiles            # Persistent, evolving profiles per competitor
    - competitive-timeline           # History of competitor changes over time
    - positioning-recommendations    # How to adjust your messaging, positioning, pricing
    - social-content-analysis        # What's working for competitors on social
    - competitive-gap-analysis       # Where you're ahead, behind, and where there's whitespace
  requires:
    - competitor-list                # Which competitors to track
    - your-company-context           # Your positioning, messaging, pricing, product
  connects_to:
    - skill: competitor-intel
      when: "Need fresh raw data — social mentions, reviews, ads, content"
      passes: competitor slugs
    - skill: cold-email-outreach
      when: "Updated competitive angles are ready for outreach campaigns"
      passes: positioning-recommendations
    - skill: email-drafting
      when: "Need to rewrite outreach copy with new competitive framing"
      passes: positioning-recommendations
  capabilities: [web-search, data-analysis, reporting]
---

# Competitive Strategy Tracker

A living competitive intelligence system that accumulates knowledge about competitors over time and translates it into strategic recommendations for your business.

`competitor-intel` tells you what competitors DID. This composite tells you what it MEANS for you and what you should DO about it.

**What it maintains:**
- A persistent profile folder per competitor, updated with every scan
- A timeline of changes — when they shifted positioning, launched features, changed pricing
- Analysis of their social content — what topics get engagement, what formats work
- Your positioning relative to each competitor, updated as they move
- Actionable recommendations: what to change in your messaging, pricing, and strategy

**Two modes:**
- **Update:** Run periodically (monthly or triggered by a competitor move). Scans for changes, updates profiles, produces a change report with recommendations.
- **Review:** On-demand deep analysis. Produces a full competitive landscape review for team discussion or strategy sessions.

## When to Auto-Load

Load this composite when:
- User says "competitive review", "update competitor profiles", "what are competitors doing", "how should we position against X"
- User says "competitor changed their pricing", "competitor launched a new feature", "competitive messaging refresh"
- User asks "how should we differentiate", "what's our positioning vs. [competitor]", "competitive strategy"
- Monthly/quarterly review cadence triggers an update
- A specific competitor move triggers a reactive analysis

---

## Step 0: Configuration (One-Time Setup)

On first run, collect and store. Skip on subsequent runs.

### Competitor List

| Question | Purpose | Stored As |
|----------|---------|-----------|
| Who are your competitors? (names + websites) | Define tracking universe | `competitors` |
| Which are primary vs. secondary competitors? | Prioritize depth of tracking | `competitor_tiers` |
| Where do competitor profiles live? | File storage location | `profile_directory` |

```
competitors: [
  {
    name: "Competitor A"
    website: "https://competitora.com"
    tier: "primary"                   # Track deeply
    slug: "competitor-a"              # Folder name
  },
  {
    name: "Competitor B"
    website: "https://competitorb.com"
    tier: "secondary"                 # Track lightly
    slug: "competitor-b"
  }
]
profile_directory: "clients/<client>/competitors/"
```

### Your Company Context (for comparison)

| Question | Purpose | Stored As |
|----------|---------|-----------|
| What is your current positioning statement? (2-3 sentences) | Compare against competitors | `your_positioning` |
| What is your tagline / headline? | Track messaging changes | `your_tagline` |
| What are your key differentiators? (3-5 points) | Competitive gap analysis | `your_differentiators` |
| What is your pricing model and approximate pricing? | Pricing comparison | `your_pricing` |
| What are your core features? | Feature comparison | `your_features` |
| What is your ICP? | Evaluate competitor ICP overlap | `your_icp` |
| Where do you post content? (LinkedIn, blog, Twitter, etc.) | Social comparison | `your_channels` |

### Tracking Config

| Question | Options | Stored As |
|----------|---------|-----------|
| How often should we do a full update? | Monthly / Quarterly | `update_cadence` |
| What social platforms should we track for competitors? | LinkedIn / Twitter / Blog / YouTube / All | `social_platforms` |
| Where should reports be saved? | Local file / Google Sheets / Notion | `report_destination` |

**Store config in:** `clients/<client-name>/config/competitive-strategy.json` or equivalent.

---

## Step 1: Scan Competitor Landscape

**Purpose:** For each competitor, collect current-state data across five dimensions. Compare against the last saved profile to detect changes.

### Input Contract

```
competitors: [...]                    # From config
profile_directory: string             # From config
mode: "update" | "review"            # Update = periodic scan. Review = full deep dive.
trigger: string | null                # e.g., "Competitor A launched new pricing" — focuses the scan
```

### Process

For each competitor, scan across five dimensions:

#### A) Positioning & Messaging

| What to Capture | Where to Look | What Changes Mean |
|----------------|--------------|-------------------|
| Homepage headline / tagline | Their website (hero section) | Messaging shift — are they going upmarket? Downmarket? New audience? |
| "What we do" / "How it works" description | Website, about page | Positioning pivot — different problem being solved? |
| Key value propositions (3-5 listed on site) | Website, product page | Feature emphasis shift — what they're betting on |
| Target audience language | Website, case studies | ICP shift — new segments being targeted |
| Customer logos / case studies featured | Website, customers page | Social proof changes — new segments, enterprise moves, etc. |
| Comparison / "vs." pages | Website, search | How they position against YOU and others |
| Demo CTA / free trial framing | Website | GTM motion shift — PLG vs. sales-led |

#### B) Product & Features

| What to Capture | Where to Look | What Changes Mean |
|----------------|--------------|-------------------|
| Feature list | Website, product page, G2 profile | New capabilities = competitive threat or irrelevance |
| Recent product launches | Blog, press, Product Hunt, changelog | Innovation velocity — are they shipping fast or stalling? |
| Integrations | Website integrations page | Ecosystem play — who are they partnering with? |
| Product screenshots / UI | Website, G2 | UX direction — going simpler? More complex? Enterprise? |
| API / developer docs | Docs site | Platform play — building an ecosystem |

#### C) Pricing & Packaging

| What to Capture | Where to Look | What Changes Mean |
|----------------|--------------|-------------------|
| Pricing page (plans, tiers, pricing) | Website /pricing | Price increase = going upmarket. Decrease = race to bottom. New tier = new segment. |
| Free tier / freemium offering | Pricing page | PLG motion — competing on adoption, not sales |
| Enterprise / "Contact us" tier | Pricing page | Moving upmarket |
| Pricing model (per seat, per usage, flat rate) | Pricing page | Model shift = strategic pivot |
| Discounts / promotions visible | Website, ads | Aggressive competition — may be losing deals |

#### D) Content & Social Performance

| What to Capture | Where to Look | What Changes Mean |
|----------------|--------------|-------------------|
| Blog posts (last 30-90 days) | Their blog | Content themes = what they think their audience cares about |
| LinkedIn company page posts (last 30 days) | LinkedIn | Topics, formats, engagement levels |
| Founder/CEO LinkedIn posts | LinkedIn | Thought leadership direction, what narrative they're pushing |
| Twitter/X activity | Twitter | Real-time messaging, community engagement |
| YouTube content | YouTube | Investment in video = scaling education/brand |
| Podcast appearances | Web search | Where they're showing up, what topics they discuss |
| Top-performing content (by engagement) | LinkedIn, blog | What resonates with their audience (you should learn from this) |

#### E) Market Signals

| What to Capture | Where to Look | What Changes Mean |
|----------------|--------------|-------------------|
| Recent funding | Crunchbase, press | Capital injection = acceleration coming |
| Hiring patterns | LinkedIn jobs, job boards | What they're building next (ML engineer = AI features, enterprise AE = upmarket) |
| Leadership changes | LinkedIn, press | New leader = strategy shift incoming |
| Partnerships announced | Press, LinkedIn | Ecosystem moves, channel strategy |
| Customer reviews (recent) | G2, Capterra | What customers love/hate = your opportunity |
| Awards / recognition | Web search | Category validation or specific niche wins |
| Layoffs / contraction | Web search, news | Vulnerability — their customers may be anxious |

### Change Detection

For each dimension, compare current state to the last saved profile:

| Change Type | How to Detect | Significance |
|-------------|--------------|-------------|
| **Messaging change** | Headline/tagline differs from saved profile | They're repositioning — evaluate impact on your positioning |
| **Feature launch** | New feature not in saved profile | Competitive gap may have closed or opened |
| **Pricing change** | Pricing differs from saved profile | Market signal about their strategy |
| **New segment** | New customer logos, case studies in different industry | They're expanding — are they coming for your ICP? |
| **Content theme shift** | Blog/social topics changed significantly | Strategic direction shift |
| **Hiring signal** | New roles not previously posted | Building new capabilities |

### Output Contract

```
competitor_scans: [
  {
    competitor: {
      name: string
      slug: string
      tier: string
      website: string
    }
    current_state: {
      positioning: {
        headline: string
        description: string
        value_propositions: string[]
        target_audience: string
        customer_logos: string[]
        comparison_pages: string[]
      }
      product: {
        key_features: string[]
        recent_launches: [ { feature: string, date: string, description: string } ]
        integrations: string[]
      }
      pricing: {
        model: string                  # "per seat", "per usage", "flat rate"
        tiers: [ { name: string, price: string, key_features: string[] } ]
        free_tier: boolean
        enterprise_tier: boolean
      }
      content: {
        blog_themes: string[]          # Top themes from recent posts
        social_top_posts: [ { platform: string, topic: string, engagement: string, url: string } ]
        content_formats: string[]      # Video, long-form, infographic, etc.
        posting_frequency: string      # "3x/week", "daily", "sporadic"
      }
      market_signals: {
        recent_funding: string | null
        hiring_patterns: string[]
        partnerships: string[]
        recent_reviews_sentiment: string
      }
    }
    changes_detected: [
      {
        dimension: string              # "positioning", "product", "pricing", "content", "market"
        change: string                 # What changed
        previous: string               # What it was before
        current: string                # What it is now
        detected_date: string
        significance: "high" | "medium" | "low"
        implication: string            # What this means for you
      }
    ]
    scan_date: string
  }
]
```

### Human Checkpoint

```
## Competitive Scan Results

### Changes Detected

| Competitor | Dimension | Change | Significance |
|-----------|-----------|--------|-------------|
| Competitor A | Pricing | Dropped starter tier from $99 → $49/mo | High — undercutting our entry price |
| Competitor A | Product | Launched AI feature X | Medium — we have this, they're catching up |
| Competitor B | Positioning | New tagline: "Enterprise-grade Y" | Medium — moving upmarket |
| Competitor B | Content | 3 blog posts on [your category topic] | Low — entering your content territory |

### No Changes
| Competitor | Last Scan |
|-----------|-----------|
| Competitor C | [date] — no material changes |

Proceed with profile updates and strategic analysis? (Y/n)
```

---

## Step 2: Update Competitor Profiles

**Purpose:** Update the persistent competitor profile files with new data and maintain the change timeline. This is the institutional memory layer.

### Input Contract

```
competitor_scans: [...]               # From Step 1
profile_directory: string             # From config
```

### Profile File Structure

Each competitor gets a folder with persistent files:

```
clients/<client>/competitors/
├── competitor-a/
│   ├── profile.md                    # Current-state profile (overwritten each update)
│   ├── timeline.md                   # Append-only change log
│   ├── social-analysis.md            # Latest social content analysis
│   └── snapshots/
│       ├── 2026-01.md                # Monthly snapshot
│       ├── 2026-02.md
│       └── 2026-03.md
├── competitor-b/
│   └── ...
└── landscape-summary.md              # Cross-competitor overview
```

### Profile File Format (`profile.md`)

```markdown
# [Competitor Name] — Competitive Profile
**Last updated:** [date]
**Website:** [url]
**Tier:** [primary/secondary]

## Positioning
**Headline:** [their current tagline]
**Description:** [what they say they do]
**Target audience:** [who they sell to]
**Key value props:**
1. [value prop 1]
2. [value prop 2]
3. [value prop 3]

## Product
**Core features:**
- [feature 1]
- [feature 2]
- [feature 3]

**Recent launches:**
| Date | Feature | Description |
|------|---------|-------------|
| [date] | [feature] | [what it does] |

**Integrations:** [list]

## Pricing
| Tier | Price | Key Features |
|------|-------|-------------|
| [tier] | [price] | [features] |

**Model:** [per seat / per usage / flat rate]
**Free tier:** [yes/no]

## Social & Content
**Primary channels:** [where they post]
**Posting frequency:** [how often]
**Top themes:** [what they talk about]
**Best-performing content:** [topics/formats that get engagement]

## Market Position
**Funding:** [total raised, last round]
**Team size:** [approximate]
**Key customers:** [logos]
**Recent reviews sentiment:** [positive/mixed/negative]

## Our Positioning vs. Them
**Where we win:** [differentiators]
**Where they win:** [their advantages]
**Whitespace:** [areas neither covers well]
```

### Timeline File Format (`timeline.md`)

Append-only log. Never delete entries — this is the historical record.

```markdown
# [Competitor Name] — Change Timeline

## 2026-03-05 — Pricing Change
**What changed:** Dropped starter tier from $99/mo to $49/mo
**Previous:** $99/mo for starter plan
**Current:** $49/mo for starter plan
**Significance:** High
**Our interpretation:** Likely losing deals at the entry level. Competing on price suggests
they can't compete on value at this tier. We should NOT match — instead, emphasize what
our $99 tier includes that their $49 doesn't.

---

## 2026-02-20 — Feature Launch
**What changed:** Launched AI-powered analytics dashboard
**Previous:** Manual reporting only
**Current:** AI-generated insights from campaign data
**Significance:** Medium
**Our interpretation:** Closing a gap we had. Our analytics are still deeper, but the
"AI-powered" positioning is compelling. Consider adding AI framing to our analytics messaging.

---

## 2026-01-15 — Positioning Shift
**What changed:** Homepage tagline changed from "Simple outreach tool" to "Enterprise-grade outreach platform"
**Previous:** "Simple outreach tool"
**Current:** "Enterprise-grade outreach platform"
**Significance:** High
**Our interpretation:** Moving upmarket. Will start competing for enterprise deals. Their
product may not back this claim yet — watch for enterprise feature launches. This opens
up the "simple/easy" positioning for us or other competitors at the SMB tier.
```

### Process

1. **Read existing profile** (if it exists) for each competitor
2. **Update `profile.md`** with current-state data from Step 1
3. **Append new changes to `timeline.md`** with date, description, and interpretation
4. **Save a monthly snapshot** if one doesn't exist for the current month
5. **Update `landscape-summary.md`** with cross-competitor overview

### Output Contract

```
updated_profiles: [
  {
    competitor: string
    profile_path: string
    timeline_path: string
    changes_logged: integer
    snapshot_saved: boolean
  }
]
```

---

## Step 3: Analyze Competitive Dynamics

**Purpose:** Look across all competitors and your own position to identify strategic patterns, gaps, threats, and opportunities. Pure LLM reasoning.

### Input Contract

```
competitor_scans: [...]               # From Step 1
your_company: {
  positioning: string
  tagline: string
  differentiators: string[]
  pricing: string
  features: string[]
  icp: string
  channels: string[]
}
timelines: [...]                      # Historical change data from profiles
```

### Analysis Sections

#### A) Positioning Map

Where does each player sit in the market?

| Dimension | Your Company | Competitor A | Competitor B | Competitor C |
|-----------|-------------|-------------|-------------|-------------|
| Primary audience | [who] | [who] | [who] | [who] |
| Core promise | [what] | [what] | [what] | [what] |
| Price point | [tier] | [tier] | [tier] | [tier] |
| GTM motion | [sales/PLG/hybrid] | [motion] | [motion] | [motion] |
| Key differentiator | [what] | [what] | [what] | [what] |

**Positioning collision check:** Are any competitors converging on your positioning? Are they moving toward or away from your space?

#### B) Feature Gap Analysis

| Feature/Capability | You | Comp A | Comp B | Comp C | Status |
|-------------------|-----|--------|--------|--------|--------|
| [feature 1] | Yes | Yes | No | No | Parity with A |
| [feature 2] | Yes | No | Yes | No | Differentiated |
| [feature 3] | No | Yes | Yes | No | Gap — they have it, you don't |
| [feature 4] | No | No | No | No | Whitespace — nobody has it |

**Gap types:**
- **Your advantage:** You have it, they don't. Emphasize in messaging.
- **Parity:** Everyone has it. Not a differentiator — stop leading with it.
- **Their advantage:** They have it, you don't. Decide: build it, partner for it, or position around it.
- **Whitespace:** Nobody has it. Opportunity to lead.

#### C) Pricing Landscape

| Player | Lowest Tier | Mid Tier | Enterprise | Model |
|--------|-----------|---------|-----------|-------|
| You | [price] | [price] | [price] | [model] |
| Comp A | [price] | [price] | [price] | [model] |
| Comp B | [price] | [price] | [price] | [model] |

**Pricing dynamics:**
- Who's the cheapest? Are they winning on price or losing on value?
- Who's the most expensive? Does their product justify it?
- Where are you positioned? Premium, mid-market, or value?
- Any recent pricing moves? What do they signal?

#### D) Social & Content Competitive Analysis

For each competitor's social presence:

| Metric | You | Comp A | Comp B |
|--------|-----|--------|--------|
| Posting frequency | [X/week] | [X/week] | [X/week] |
| Primary platform | [platform] | [platform] | [platform] |
| Top content themes | [themes] | [themes] | [themes] |
| Avg engagement | [range] | [range] | [range] |
| Content format mix | [types] | [types] | [types] |

**What's working for competitors:**
- Which topics get the most engagement?
- Which formats (video, carousel, long-form, short-form)?
- What's their narrative? (Thought leadership, product updates, customer stories, industry trends)
- Are they engaging with YOUR audience?

**What you can learn:**
- Topics they cover that you don't (content gaps)
- Formats they use that you don't (format opportunities)
- Engagement patterns (when and how their audience responds)
- What their audience cares about (inferred from engagement)

**Where you're ahead:**
- Topics you own that they don't cover
- Higher engagement on specific themes
- Unique formats or approaches

#### E) Trend Analysis (From Timeline Data)

Look across the historical timeline for patterns:

| Pattern | What It Means |
|---------|--------------|
| Multiple competitors moving upmarket | Market maturation — SMB becoming commoditized |
| Competitors adding AI/automation features | Table stakes shifting — you need this too or you're behind |
| Pricing dropping across the board | Race to bottom — compete on value, not price |
| Competitors copying your positioning | You're the leader — but need to stay ahead |
| Competitor pivoting to new segment | They're abandoning a segment — opportunity for you |
| Increasing competitor content frequency | Category getting noisy — need to differentiate harder |

### Output Contract

```
competitive_analysis: {
  positioning_map: {
    players: [ { name: string, audience: string, promise: string, price_tier: string, motion: string, differentiator: string } ]
    collision_risks: string[]
    positioning_gaps: string[]
  }

  feature_gaps: {
    your_advantages: [ { feature: string, competitors_lacking: string[] } ]
    parity_features: [ { feature: string, note: string } ]
    their_advantages: [ { feature: string, who_has_it: string[], recommendation: string } ]
    whitespace: [ { opportunity: string, description: string } ]
  }

  pricing_landscape: {
    your_position: string
    dynamics: string[]
    recommendations: string[]
  }

  social_analysis: {
    competitor_strengths: [ { competitor: string, strength: string, evidence: string } ]
    your_content_gaps: string[]
    format_opportunities: string[]
    topics_to_own: string[]
    topics_to_enter: string[]
  }

  trend_patterns: [
    { pattern: string, implication: string, recommendation: string }
  ]
}
```

---

## Step 4: Generate Recommendations

**Purpose:** Turn competitive analysis into specific, actionable recommendations for messaging, positioning, pricing, content, and product. Pure LLM reasoning.

### Input Contract

```
competitive_analysis: { ... }        # From Step 3
your_company: { ... }                # From config
changes_detected: [...]              # From Step 1
```

### Recommendation Categories

#### A) Positioning Recommendations

Based on where competitors are moving and where gaps exist:

| Trigger | Recommendation Pattern |
|---------|----------------------|
| Competitor moved upmarket | "Consider owning the 'simple/fast/affordable' position they abandoned." |
| Competitor copying your positioning | "Sharpen your differentiation. They're converging — you need to be more specific." |
| Whitespace identified | "Position around [whitespace]. No one owns this yet." |
| Multiple competitors in same spot | "Avoid the crowded middle. Go premium or go niche." |

**Output format:**
```
Current positioning: "[your current tagline]"
Recommended adjustment: "[suggested new framing]"
Rationale: "[why, based on competitive data]"
Urgency: [high/medium/low]
```

#### B) Messaging & Outreach Angle Updates

Specific copy recommendations for outreach:

| Competitive Change | Messaging Update |
|-------------------|-----------------|
| Competitor dropped price | Add "value beyond price" messaging. Lead with ROI, not cost. |
| Competitor launched feature you have | Emphasize your version is more mature / better integrated. |
| Competitor launched feature you lack | Acknowledge it exists but frame your approach differently: "We solve this through [alternative approach]." |
| Competitor lost a big customer | Subtle opportunity: "Companies like [industry] are switching to [you]." |
| Competitor's reviews mention weakness | Address that weakness as your strength without naming them. |

**Output format:**
```
Angle: "[competitive angle name]"
When to use: "[which campaigns or call types]"
Messaging: "[specific copy suggestion]"
Proof point: "[evidence to back it up]"
Replace: "[what this replaces in current outreach]" or "New addition"
```

#### C) Pricing Recommendations

| Trigger | Recommendation |
|---------|---------------|
| Competitor undercut your price | Don't match unless you must. Instead: [specific value justification]. |
| Competitor raised prices | Opportunity to position as "better value at a similar price." |
| New free tier from competitor | Consider a limited free tier or an extended trial to compete on adoption. |
| Competitor changed pricing model | Evaluate if your model is still competitive. [Specific suggestion]. |

#### D) Content & Social Recommendations

| Finding | Recommendation |
|---------|---------------|
| Competitor gets high engagement on [topic] | "Start creating content about [topic]. Their audience is YOUR audience." |
| Competitor dominates [format] | "Test [format]. They've validated the audience responds to this." |
| Gap: no one covers [topic] | "Own [topic] as your content territory. First-mover advantage." |
| Your content outperforms on [topic] | "Double down on [topic]. You're already winning here." |
| Competitor engaging your audience | "Increase posting frequency and engagement on [platform]." |

#### E) Product / Feature Recommendations

| Finding | Recommendation |
|---------|---------------|
| Feature gap (they have, you don't) | "Prioritize building [feature] OR position around it: 'We solve this through [alternative].'" |
| Feature parity (everyone has it) | "Stop leading with [feature] in messaging. It's table stakes, not a differentiator." |
| Your advantage (you have, they don't) | "Double down on [feature] in all messaging. This is your edge." |
| Whitespace opportunity | "Consider building [capability]. No competitor covers this." |

### Output Contract

```
recommendations: {
  positioning: [
    {
      priority: "high" | "medium" | "low"
      current: string
      recommended: string
      rationale: string
      triggered_by: string            # Which competitive change triggered this
    }
  ]

  messaging_angles: [
    {
      angle_name: string
      when_to_use: string
      messaging: string
      proof_point: string
      replaces: string | null
      triggered_by: string
    }
  ]

  pricing: [
    {
      recommendation: string
      rationale: string
      urgency: string
      triggered_by: string
    }
  ]

  content: [
    {
      recommendation: string
      topic_or_format: string
      rationale: string
      effort: "low" | "medium" | "high"
    }
  ]

  product: [
    {
      recommendation: string
      type: "build" | "position_around" | "double_down" | "stop_leading_with"
      rationale: string
    }
  ]
}
```

---

## Step 5: Generate Report

**Purpose:** Produce the team-presentable competitive strategy report.

### Report Structure

```
# Competitive Strategy Report — [Date]
**Period covered:** [last scan date] to [current date]
**Competitors tracked:** [count]

---

## Executive Summary

**Market movement:** [2-3 sentences on what competitors did this period]
**Biggest threat:** [The most significant competitive change and what it means]
**Biggest opportunity:** [The gap or weakness you should exploit]
**Top recommendation:** [Single most impactful thing to do]

---

## Changes Since Last Review

| Date | Competitor | Change | Significance | Our Response |
|------|-----------|--------|-------------|-------------|
| [date] | [name] | [what changed] | [H/M/L] | [recommended action] |

---

## Competitive Landscape

### Positioning Map
| Player | Audience | Promise | Price Tier | Motion | Differentiator |
|--------|----------|---------|-----------|--------|---------------|
| **You** | [who] | [what] | [tier] | [motion] | [what] |
| [Comp] | [who] | [what] | [tier] | [motion] | [what] |

### Feature Comparison
| Feature | You | Comp A | Comp B | Status |
|---------|-----|--------|--------|--------|
| [feature] | [Y/N] | [Y/N] | [Y/N] | [advantage/parity/gap] |

### Pricing Landscape
| Player | Entry | Mid | Enterprise | Model |
|--------|-------|-----|-----------|-------|
| [name] | [price] | [price] | [price] | [model] |

---

## Competitor Deep Dives

### [Competitor A] — [Tier]
**What they did this period:** [summary]
**Key changes:** [list]
**Their strengths:** [what they're good at]
**Their weaknesses:** [where they struggle]
**Threat level:** [high/medium/low] — [why]
**Our positioning vs. them:** [how to differentiate]

[Repeat per competitor]

---

## Social & Content Intelligence

### What's Working for Competitors
| Competitor | Top Topic | Format | Engagement | Takeaway |
|-----------|-----------|--------|-----------|----------|
| [name] | [topic] | [format] | [level] | [what to learn] |

### Content Gaps & Opportunities
| Opportunity | Description | Effort | Impact |
|------------|-------------|--------|--------|
| [topic/format] | [why it's an opportunity] | [L/M/H] | [L/M/H] |

### Your Content vs. Theirs
| Dimension | You | Best Competitor | Gap |
|-----------|-----|----------------|-----|
| Posting frequency | [X/week] | [Y/week] | [behind/ahead] |
| Top engagement topic | [topic] | [topic] | [overlap/different] |
| Format diversity | [formats] | [formats] | [assessment] |

---

## Strategic Recommendations

### Positioning & Messaging
1. **[Recommendation]** — [Priority]
   Triggered by: [what happened]
   Action: [specific thing to do]

### Outreach Angle Updates
| # | Angle | When to Use | Copy Suggestion |
|---|-------|------------|-----------------|
| 1 | [angle name] | [context] | "[specific messaging]" |

### Pricing
1. **[Recommendation]** — [urgency]

### Content & Social
1. **[Recommendation]** — [effort level]

### Product
1. **[Recommendation]** — [type]

---

## Trends Over Time

[Analysis of patterns from timeline data across multiple review periods]

| Pattern | Period Observed | Direction | Implication |
|---------|----------------|-----------|------------|
| [trend] | [since when] | [accelerating/stable/slowing] | [what it means] |

---

## Action Items

| # | Action | Owner | Deadline | Category |
|---|--------|-------|----------|----------|
| 1 | [action] | [who] | [when] | Messaging |
| 2 | [action] | [who] | [when] | Content |
| 3 | [action] | [who] | [when] | Product |
```

### Human Checkpoint

```
[Executive Summary rendered]

---

Key changes detected: X across Y competitors
High-significance changes: Z

Top 3 recommended actions:
1. [Messaging] — [action + trigger]
2. [Content] — [action + trigger]
3. [Positioning] — [action + trigger]

Full report includes:
- Competitor deep dives with profile updates
- Feature gap analysis
- Pricing landscape comparison
- Social content intelligence
- Timeline trend analysis
- Specific messaging angle suggestions

View the full report? Or act on a specific recommendation?
```

---

## Execution Summary

| Step | Tool Dependency | Human Checkpoint | Typical Time |
|------|----------------|-----------------|--------------|
| 0. Config | None | First run only | 5-10 min (once) |
| 1. Scan | Web search (always available) + competitor-intel (optional) | Review detected changes | 3-5 min |
| 2. Update Profiles | Filesystem (write profile files) | None — automatic | Automatic |
| 3. Analyze | None (LLM reasoning) | None — feeds into report | Automatic |
| 4. Recommendations | None (LLM reasoning) | None — feeds into report | Automatic |
| 5. Generate Report | None (LLM reasoning) | Review report + approve actions | 5-10 min |

**Total human review time: ~15-20 minutes** for a strategic competitive review that would take 3-5 hours of manual research and analysis.

---

## Cadence Guide

| Mode | When | What It Produces |
|------|------|-----------------|
| **Monthly update** | First week of each month | Profile updates + change report + messaging refreshes |
| **Triggered update** | Competitor launches feature, changes pricing, makes news | Focused analysis of the specific change + response plan |
| **Quarterly review** | End of quarter | Full landscape analysis + trend report + strategic planning input |
| **On-demand** | Before a competitive deal, board meeting, pricing discussion | Deep dive on specific competitor or full landscape |

---

## Tips

- **The timeline is the most valuable artifact.** Individual scans are snapshots. The timeline reveals trajectory — is a competitor accelerating toward your position or moving away? Patterns only emerge over 3+ scans.
- **Don't react to every change.** Not every competitor move requires a response. Small feature additions or minor messaging tweaks are noise. Pricing changes, positioning pivots, and major launches are signal.
- **"Where they win" is as important as "where we win."** Acknowledging competitor strengths makes your competitive positioning credible. Reps who say "they're terrible at everything" lose deals to reps who say "they're strong at X, but we're better for you because Y."
- **Track their content performance, not just their content.** What a competitor publishes matters less than what their audience engages with. A post with 500 likes tells you more about the market than a post with 5.
- **Competitor job postings are leading indicators.** If they're hiring ML engineers, AI features are coming. If they're hiring enterprise AEs, they're going upmarket. Job postings predict product roadmaps 6-12 months out.
- **Feed updated messaging angles back into your outreach composites.** This composite's recommendations should directly update the outreach copy used in `cold-email-outreach`, `hiring-signal-outreach`, etc. Close the loop.
- **Keep profiles in version control.** The profile folder structure works with git. Each update is a commit. You get free history, diffing, and rollback.
