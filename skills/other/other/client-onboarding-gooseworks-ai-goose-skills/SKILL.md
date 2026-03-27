---
type: playbook
name: client-onboarding
description: >
  Full client onboarding: intelligence gathering, synthesis into Client Intelligence Package,
  and growth strategy generation. Phases 1-3 of the Client Launch Playbook.
graph:
  provides: [intelligence-package, growth-strategies, client-folder-structure]
  requires: [company-name, company-url]
  connects_to:
    - skills/playbooks/client-package-notion/SKILL.md
    - skills/playbooks/outbound-prospecting-engine/SKILL.md
    - skills/playbooks/seo-content-engine/SKILL.md
    - skills/playbooks/competitor-monitoring-system/SKILL.md
skills_used:
  - skills/composites/seo-content-audit
  - skills/capabilities/aeo-visibility
  - skills/capabilities/meta-ad-scraper
  - skills/capabilities/google-ad-scraper
  - skills/composites/industry-scanner
  - skills/composites/company-current-gtm-analysis
---

# Client Onboarding

Full onboarding playbook for a new client. Produces a Client Intelligence Package and Growth Strategy Recommendations.

Reference: docs/agency-playbook/client-launch-playbook.md for the full process documentation.

## When to Use

- "Onboard [company name] as a new client"
- "Run the full intelligence gathering for [company]"
- "Create a growth strategy for [company]"

## Prerequisites

- Company name and website URL
- Basic understanding of what the company does (or the agent will research it)

## Phase 1: Intelligence Gathering (~30 min parallel agent work)

### Setup

First, create the client folder structure:

```
clients/<client-name>/
├── context.md              # Will be populated during research
├── notes.md                # Running log
├── intelligence/           # All Phase 1 outputs go here
├── strategies/             # Will be populated after strategy approval
├── campaigns/
├── leads/
└── content/
```

### Step 1: Company Deep Research
- Deep web research: product, pricing, team, funding, customers, tech stack, recent news
- **Method**: Web search + web fetch
- **Output**: `clients/<client-name>/intelligence/company-research.md`

### Step 2: Competitor Deep Research
- Identify top 5-10 competitors, research positioning, pricing, strengths, weaknesses
- **Method**: Web search + web fetch
- **Output**: `clients/<client-name>/intelligence/competitor-research.md`

### Step 3: Founder Deep Research
- Research founders: backgrounds, LinkedIn presence, thought leadership, public visibility
- **Method**: Web search + linkedin-profile-post-scraper
- **Output**: `clients/<client-name>/intelligence/founder-research.md`

### Step 4: SEO Content Audit
- Full SEO footprint: content inventory, domain metrics, competitive gaps, brand voice
- **Skill**: seo-content-audit (orchestrates site-content-catalog + seo-domain-analyzer + brand-voice-extractor)
- **Output**: `clients/<client-name>/intelligence/seo-content-audit.md`

### Step 5: AEO Visibility Check
- Test visibility across AI answer engines for key queries
- **Skill**: aeo-visibility
- **Output**: `clients/<client-name>/intelligence/aeo-visibility.md`

### Step 6: Paid Ads Strategy Review
- Scrape active Meta and Google ads for client and top competitors
- **Skill**: meta-ad-scraper + google-ad-scraper
- **Output**: `clients/<client-name>/intelligence/ad-strategy.md`

### Step 7: Industry Intelligence Scan
- Scan everything happening in the client's industry in the past week
- **Skill**: industry-scanner
- **Output**: `clients/<client-name>/intelligence/industry-scan.md`

### Step 8: Current GTM Analysis
- Score the client's current GTM across all dimensions
- **Skill**: company-current-gtm-analysis
- **Output**: `clients/<client-name>/intelligence/gtm-analysis.md`

### Parallel Execution Plan

```
Parallel Group A (general research — run simultaneously):
  Step 1: Company Deep Research
  Step 2: Competitor Deep Research
  Step 3: Founder Deep Research

Parallel Group B (automated audits — run simultaneously):
  Step 4: SEO Content Audit
  Step 5: AEO Visibility Check
  Step 6: Paid Ads Strategy Review
  Step 7: Industry Intelligence Scan
  Step 8: Current GTM Analysis
```

Groups A and B can run in parallel with each other.

## Phase 2: Synthesis & Diagnosis

Read all Phase 1 outputs and synthesize into a single Client Intelligence Package.

**Reference framework**: docs/growth-frameworks.md

### Diagnostic Steps

1. **Assess PMF**: Does the retention curve flatten? (Pre-PMF / PMF / Strong PMF)
2. **Determine ACV tier**: What viable channels does their price point support?
3. **Identify growth motion**: Product-led, marketing-led, sales-led, or blended?
4. **Assess scaling stage**: Pre-PMF → PMF → GTM Fit → Growth & Moat
5. **Score current GTM**: Rate each dimension A-F (from gtm-analysis output)
6. **Map competitive landscape**: Top 5 competitors with strengths/weaknesses
7. **Identify opportunity gaps**: Which Growth Matrix cells are empty?
8. **Flag risk factors**: Competitive threats, market risks, internal constraints

### Output

**File**: `clients/<client-name>/intelligence-package.md`

Structure:
1. Company Profile
2. Stage Assessment (PMF, ACV, Motion, Scaling Stage)
3. Current GTM Scorecard (A-F per dimension)
4. Competitive Landscape
5. Industry Context
6. Opportunity Map (Growth Matrix gaps)
7. Risk Factors

## Phase 3: Strategy Generation

Read the Intelligence Package and generate prioritized growth strategies.

### Strategy Generation Process

For each identified opportunity gap:

1. **Name the system**: Map to the Growth Systems Taxonomy (Intelligence / Demand Creation / Pipeline)
2. **Describe the gap**: What's missing or broken?
3. **Propose the solution**: What system do we build? What skills power it?
4. **Estimate impact**: Expected lift based on available data
5. **Sequence**: P0 (immediate), P1 (4-6 weeks), P2 (8-10 weeks)
6. **Score**: ICE score (Impact x Confidence x Ease, each 1-10)
7. **Tag the execution pattern**: Add a structured `<!-- execution ... -->` YAML block identifying the pattern, signal type, required skills, estimated cost, and estimated lead volume. See [Structured Execution Tags](#structured-execution-tags) below for the format.

### Prioritization Rules

1. Activation before acquisition (if activation is broken, fix that first)
2. One channel deep before expanding
3. Engine over boost (compounding loops > one-time campaigns)
4. Always include at least one quick-win Pipeline strategy alongside longer-term Demand Creation
5. Match channel to ACV (no field sales for <$5K ACV)

### Output

**File**: `clients/<client-name>/growth-strategies.md`

Format: P0/P1/P2 grouped strategies with gap, solution, tactical steps, expected impact, timeline.

See `clients/vapi/growth-strategies.md` as a reference example.

### Structured Execution Tags

Every strategy in `growth-strategies.md` must include a machine-readable execution tag as an HTML comment block. This allows the `client-packet-engine` playbook to automatically route strategies to the correct skill chains.

#### Format

```markdown
<!-- execution
pattern: signal-outbound
signal_type: job-posting
signal_keywords: ["DevOps", "SRE", "platform engineer"]
target_titles: ["VP Engineering", "CTO", "Head of Platform"]
estimated_leads: 50
estimated_cost: 0.80
skills_required:
  - job-posting-intent
  - company-contact-finder
  - email-drafting
-->
```

#### Fields

| Field | Required | Description |
|-------|----------|-------------|
| `pattern` | Yes | Execution pattern: `signal-outbound`, `content-lead-gen`, `competitive-displacement`, `event-prospecting`, `lifecycle-timing`, or `manual` |
| `signal_type` | If signal-outbound | Signal source: `job-posting`, `linkedin-post`, `review-sentiment`, `funding`, `product-launch` |
| `signal_keywords` | If signal-outbound | Keywords to detect the signal |
| `target_titles` | If applicable | Decision-maker titles to target |
| `competitor_name` | If competitive-displacement | Competitor to displace |
| `event_keywords` | If event-prospecting | Keywords to find relevant events |
| `content_type` | If content-lead-gen | Asset type: `comparison-page`, `industry-report`, `blog-post`, `landing-page` |
| `trigger_type` | If lifecycle-timing | Trigger: `fiscal-year-end`, `contract-renewal`, `quarterly-review`, `seasonal` |
| `timing_window` | If lifecycle-timing | When to execute (e.g., "Q4", "30 days before renewal") |
| `estimated_leads` | Yes | Conservative estimate of leads this strategy will produce |
| `estimated_cost` | Yes | Estimated Apify/API cost in dollars |
| `skills_required` | Yes | Ordered list of skills in the execution chain |

#### Pattern Selection Guide

| Pattern | Use When | Primary Signal |
|---------|----------|---------------|
| `signal-outbound` | A buying signal (hiring, social activity, review complaints) maps to outreach | Job posts, LinkedIn posts, reviews |
| `content-lead-gen` | Strategy involves creating a content asset to attract or nurture leads | SEO gaps, thought leadership opportunities |
| `competitive-displacement` | Strategy targets a competitor's unhappy or at-risk customers | Negative reviews, competitor weaknesses, archived customer lists |
| `event-prospecting` | Strategy involves finding and engaging event attendees or speakers | Conferences, meetups, webinars |
| `lifecycle-timing` | Strategy depends on timing a trigger event (renewals, fiscal year, seasonal) | Business cycle triggers |
| `manual` | Strategy requires human judgment, relationships, or tools not yet automated | Partnerships, enterprise sales, brand campaigns |

#### Examples

**Signal-Outbound (job posting intent)**:
```markdown
### Strategy 1: DevOps Hiring Signal Outbound

Companies hiring DevOps/SRE roles likely need infrastructure tooling...

<!-- execution
pattern: signal-outbound
signal_type: job-posting
signal_keywords: ["DevOps", "SRE", "platform engineer", "infrastructure"]
target_titles: ["VP Engineering", "CTO", "Head of Platform"]
estimated_leads: 50
estimated_cost: 0.80
skills_required:
  - job-posting-intent
  - company-contact-finder
  - email-drafting
-->
```

**Competitive-Displacement**:
```markdown
### Strategy 3: Capture Unhappy BigCo Customers

BigCo has declining review scores on G2 and recent feature removals...

<!-- execution
pattern: competitive-displacement
competitor_name: BigCo
target_titles: ["Head of Operations", "VP Product", "CTO"]
estimated_leads: 30
estimated_cost: 1.20
skills_required:
  - web-archive-scraper
  - review-scraper
  - company-contact-finder
  - email-drafting
  - content-asset-creator
-->
```

**Manual (no automation available)**:
```markdown
### Strategy 6: Partner Co-Marketing Program

Build joint content and referral agreements with complementary tools...

<!-- execution
pattern: manual
estimated_leads: 0
estimated_cost: 0
skills_required: []
-->
```

#### Rules

1. **Every strategy gets tagged** — even manual ones. This ensures the packet engine can account for all strategies.
2. **Be specific with `signal_type`** — don't use generic descriptions. Map to the exact signal source the skill will scan.
3. **List all skills in chain** — in execution order. The packet engine uses this to plan parallel execution.
4. **Estimate conservatively** — overestimate cost, underestimate leads. Better to over-deliver than under-deliver.
5. **Use `manual` sparingly** — if a strategy can be even partially automated, tag it with the automatable pattern and note limitations in the strategy description.

## Human Checkpoints

- **After Phase 2**: Review the Intelligence Package for accuracy before generating strategies
- **After Phase 3**: Review strategies with client before implementation
