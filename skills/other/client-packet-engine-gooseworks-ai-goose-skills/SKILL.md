---
type: playbook
name: client-packet-engine
description: >
  Batch client packet generator. Takes company names/URLs, runs intelligence + strategy generation,
  presents strategies for human selection, executes selected strategies in pitch-packet mode
  (no live campaigns or paid enrichment), and packages into local delivery packets.
graph:
  provides: [client-packets, intelligence-packages, growth-strategies, sample-leads, sample-content, sample-sequences]
  requires: [company-list]
  connects_to:
    - skills/playbooks/outbound-prospecting-engine/SKILL.md
    - skills/playbooks/seo-content-engine/SKILL.md
skills_used:
  - skills/playbooks/client-onboarding
  - skills/playbooks/client-package-local
  - skills/capabilities/job-posting-intent
  - skills/capabilities/linkedin-post-research
  - skills/capabilities/review-scraper
  - skills/capabilities/company-contact-finder
  - skills/capabilities/email-drafting
  - skills/capabilities/content-asset-creator
  - skills/capabilities/apollo-lead-finder
  - skills/capabilities/web-archive-scraper
  - skills/capabilities/luma-event-attendees
  - skills/capabilities/conference-speaker-scraper
  - skills/capabilities/lead-qualification
  - skills/capabilities/cold-email-outreach
  - skills/capabilities/linkedin-outreach
---

# Client Packet Engine

Batch pipeline that takes a list of companies and produces finished GTM pitch packets — intelligence packages, growth strategies, and executed sample work (lead lists, content drafts, email sequences). Designed for prospective client pitches, not live campaign execution.

## When to Use

- "Build pitch packets for [company list]"
- "Create client packets for these companies"
- "Run the full pitch pipeline for [companies]"
- "Prepare GTM packets for prospective clients"

## Key Constraints

- **Pitch-packet mode**: Generates sample leads, content, and outreach drafts but does NOT launch live campaigns, send real emails, or spend on paid Apollo enrichment. The goal is demonstrating value.
- **Cost budget**: Default $5/company. Warn at 80% ($4). Hard stop at limit.
- **Parallelization**: Up to 3 companies concurrent (Phase 1), up to 5 strategy executions concurrent (Phase 3).
- **Human checkpoints**: (1) After cost estimate, (2) Strategy selection per company, (3) Before any single API call >$2.

## Input

```
companies:
  - name: "Company Name"
    url: "https://company.com"
  - name: "Another Company"
    url: "https://another.com"
```

Minimum: 1 company. No hard maximum, but warn if >10 (long runtime, high cost).

---

## Phase 0: Intake & Validation

### Steps

1. **Parse input**: Extract company names and URLs from the user's request. Normalize URLs (add https:// if missing, strip trailing slashes).

2. **Validate websites**: For each URL, do a quick web fetch to confirm:
   - Site is reachable (not 404/500)
   - It's the correct company (page title or content matches company name)
   - Flag any mismatches for user confirmation

3. **Estimate costs**: Calculate per-company estimate based on typical skill costs:
   - Phase 1 (research + audits): ~$1.50/company (Apify credits for SEO, ads, content scraping)
   - Phase 3 (strategy execution): ~$1.00-3.00/company depending on strategy count and types
   - Total estimate: $2.50-4.50/company typical

4. **Present summary for approval**:
   ```
   Batch Summary:
   ┌──────────────────┬─────────────────────────┬──────────┐
   │ Company          │ URL                     │ Est Cost │
   ├──────────────────┼─────────────────────────┼──────────┤
   │ Acme Corp        │ https://acme.com        │ ~$3.50   │
   │ Beta Inc         │ https://beta.io         │ ~$3.50   │
   └──────────────────┴─────────────────────────┴──────────┘
   Total estimated cost: ~$7.00
   Budget limit: $5.00/company ($10.00 total)
   ```

5. **Get user approval** before proceeding.

### Output

- Validated company list with confirmed URLs
- Cost estimate acknowledged by user

---

## Phase 1: Research & Strategy Generation

Run the **client-onboarding** playbook (Phases 1-3) for each company.

### Execution

- Process up to **3 companies in parallel** using Task agents
- Each company gets the full client-onboarding treatment:
  - Phase 1: Intelligence Gathering (company research, competitor research, founder research, SEO audit, AEO visibility, ads review, industry scan, GTM analysis)
  - Phase 2: Synthesis into Client Intelligence Package
  - Phase 3: Strategy Generation with execution tags (see Structured Execution Tags in client-onboarding)

### Cost Tracking

After each company completes:
- Log actual Apify/API costs
- Compare against per-company budget
- If at 80% of budget, warn before continuing
- If at limit, stop and report what was completed

### Output per Company

- `clients/<company>/intelligence-package.md`
- `clients/<company>/growth-strategies.md` (with `<!-- execution -->` tags on each strategy)
- All Phase 1 research files in `clients/<company>/intelligence/`

---

## Phase 2: Strategy Selection (Human Checkpoint)

Present all generated strategies across all companies for user selection.

### Presentation Format

For each company, show a summary table:

```
## Acme Corp — 7 strategies generated

| # | Strategy | Pattern | Priority | ICE | Est Leads | Est Cost |
|---|----------|---------|----------|-----|-----------|----------|
| 1 | Hiring signal outbound (DevOps roles) | signal-outbound | P0 | 8.2 | ~50 | $0.80 |
| 2 | Competitor displacement (vs BigCo) | competitive-displacement | P0 | 7.5 | ~30 | $1.20 |
| 3 | Conference speaker prospecting | event-prospecting | P1 | 6.8 | ~20 | $0.50 |
| 4 | SEO comparison content | content-lead-gen | P1 | 6.5 | ~40 | $0.60 |
| 5 | Quarterly business review timing | lifecycle-timing | P2 | 5.0 | ~15 | $0.30 |
| 6 | LinkedIn thought leadership | manual | P2 | 4.5 | — | — |
| 7 | Partner co-marketing | manual | P2 | 3.8 | — | — |

Select strategies to execute: [e.g., "1-4", "all P0", "top 3 by ICE"]
```

### Selection Options

Accept flexible input:
- Specific numbers: "1, 3, 5"
- Ranges: "1-4"
- Priority-based: "all P0", "P0 and P1"
- Score-based: "top 3 by ICE"
- All executable: "all" (skips `manual` pattern strategies)
- Per-company overrides: "Acme: 1-3, Beta: all P0"

### Validation

- Warn if selected strategies exceed remaining per-company budget
- Flag any strategies tagged `manual` (these produce a plan document but no automated execution)
- Confirm final selection before proceeding

---

## Phase 3: Strategy Execution (Pitch-Packet Mode)

Execute selected strategies using the execution pattern routing system.

### Execution Pattern Router

Read the `<!-- execution -->` tag from each selected strategy and route to the appropriate skill chain.

#### Pattern: `signal-outbound`

Detect buying signal → find contacts → draft outreach.

| Step | Skill | Pitch-Packet Behavior |
|------|-------|-----------------------|
| 1. Detect signals | `job-posting-intent` / `linkedin-post-research` / `review-scraper` (based on `signal_type`) | Run normally — free or low-cost scraping |
| 2. Find contacts | `company-contact-finder` | Run normally — uses Gooseworks MCP (free) |
| 3. Draft outreach | `email-drafting` | Draft sequences but do NOT send or set up campaigns |

**Output**: Signal report + lead CSV + draft email sequences

#### Pattern: `content-lead-gen`

Create content asset + find leads who'd care.

| Step | Skill | Pitch-Packet Behavior |
|------|-------|-----------------------|
| 1. Create content | `content-asset-creator` | Generate the asset (HTML report, comparison page, etc.) |
| 2. Find leads | `apollo-lead-finder` | **Free search only** — no paid enrichment. Show lead count + titles |

**Output**: Content asset (HTML) + lead list (names/titles/companies, no emails)

#### Pattern: `competitive-displacement`

Target competitor's unhappy customers.

| Step | Skill | Pitch-Packet Behavior |
|------|-------|-----------------------|
| 1. Mine competitor intel | `web-archive-scraper` + `review-scraper` | Scrape archived customer lists + negative reviews |
| 2. Find contacts | `company-contact-finder` | Find decision-makers at identified companies |
| 3. Draft outreach | `email-drafting` | Draft displacement-themed sequences |
| 4. Create comparison content | `content-asset-creator` | Build comparison page (client vs competitor) |

**Output**: Competitor intel report + lead CSV + email sequences + comparison page

#### Pattern: `event-prospecting`

Find event attendees/speakers matching ICP.

| Step | Skill | Pitch-Packet Behavior |
|------|-------|-----------------------|
| 1. Find events/people | `luma-event-attendees` / `conference-speaker-scraper` | Scrape relevant events |
| 2. Qualify leads | `lead-qualification` | Score against ICP |
| 3. Find contacts | `company-contact-finder` | Enrich qualified leads |

**Output**: Event attendee list + qualified leads CSV

#### Pattern: `lifecycle-timing`

Timed outreach based on trigger events.

| Step | Skill | Pitch-Packet Behavior |
|------|-------|-----------------------|
| 1. Research triggers | Web research | Identify timing triggers (fiscal year, renewal cycles, etc.) |
| 2. Find contacts | `company-contact-finder` | Find decision-makers at target companies |
| 3. Draft timed sequences | `email-drafting` | Draft timing-aware email sequences with send-date recommendations |

**Output**: Trigger research document + lead CSV + timing-aware email sequences

#### Pattern: `manual`

Strategy requires human execution or tools not yet automated.

| Step | Output |
|------|--------|
| 1. Generate execution plan | Detailed step-by-step plan with recommended tools, timelines, and KPIs |

**Output**: Strategy execution plan document (no automated work)

### Parallelization

- Run up to **5 strategy executions concurrently** across all companies
- Track cost per execution against remaining company budget
- If a single API call would exceed $2, pause and confirm with user

### Cost Tracking

Maintain a running cost log:
```
Cost Tracker:
┌──────────────┬─────────────┬───────┬──────────┬───────────┐
│ Company      │ Strategy    │ Spent │ Budget   │ Remaining │
├──────────────┼─────────────┼───────┼──────────┼───────────┤
│ Acme Corp    │ Phase 1     │ $1.40 │ $5.00    │ $3.60     │
│ Acme Corp    │ Strategy 1  │ $0.70 │          │ $2.90     │
│ Acme Corp    │ Strategy 2  │ $1.10 │          │ $1.80     │
└──────────────┴─────────────┴───────┴──────────┴───────────┘
```

### Output per Strategy

All outputs go to `clients/<company>/` in the appropriate subdirectory:
- Lead CSVs → `clients/<company>/leads/`
- Content assets → `clients/<company>/content/`
- Email sequences → `clients/<company>/campaigns/`
- Strategy plans → `clients/<company>/strategies/`
- Signal/research reports → `clients/<company>/intelligence/`

---

## Phase 4: Packaging

Run **client-package-local** for each company to produce the final deliverable.

### Steps

1. For each company, run the `client-package-local` playbook
2. This produces a dated package directory:
   ```
   clients/<company>/client-package/<YYYY-MM-DD>/
   ├── intelligence-package.md
   ├── growth-strategies.md
   ├── executed-strategies/
   │   ├── strategy-1-signal-outbound/
   │   │   ├── signal-report.md
   │   │   ├── leads.csv
   │   │   └── email-sequences.md
   │   ├── strategy-2-competitive-displacement/
   │   │   ├── competitor-intel.md
   │   │   ├── leads.csv
   │   │   ├── email-sequences.md
   │   │   └── comparison-page.html
   │   └── ...
   └── summary.md
   ```

3. Generate a `summary.md` for each packet that includes:
   - Company overview (from intelligence package)
   - Strategies generated and which were executed
   - Key metrics: total leads found, content assets created, email sequences drafted
   - Recommended next steps (what to do if the client signs)

### Final Report

After all companies are packaged, present a batch summary:

```
Batch Complete: 3/3 companies processed

┌──────────────┬────────────┬───────────┬────────┬──────────┬───────────┐
│ Company      │ Strategies │ Executed  │ Leads  │ Content  │ Total Cost│
├──────────────┼────────────┼───────────┼────────┼──────────┼───────────┤
│ Acme Corp    │ 7          │ 4         │ 142    │ 3 assets │ $4.20     │
│ Beta Inc     │ 5          │ 3         │ 89     │ 2 assets │ $3.80     │
│ Gamma Labs   │ 6          │ 4         │ 115    │ 3 assets │ $4.50     │
└──────────────┴────────────┴───────────┴────────┴──────────┴───────────┘

Total cost: $12.50 / $15.00 budget
Packets saved to: clients/<company>/client-package/<date>/
```

---

## Error Handling

- **Website unreachable**: Skip company, flag in report, continue with others
- **Skill failure**: Retry once. If still fails, log error, skip that strategy execution, continue with others
- **Budget exceeded**: Stop execution for that company, package whatever was completed
- **Rate limiting**: Back off and retry with exponential delay (max 3 retries)
- **No strategies tagged executable**: Generate all strategies but flag that manual selection will be needed for execution

## Configuration Overrides

Users can override defaults at invocation:

```
Override options:
  budget_per_company: $10      # Default $5
  max_parallel_companies: 5    # Default 3
  max_parallel_strategies: 8   # Default 5
  skip_phases: [4]             # Skip packaging
  strategy_filter: "P0 only"  # Pre-filter strategies
  pitch_packet_mode: false     # Enable live campaign mode (CAREFUL)
```

**WARNING**: Setting `pitch_packet_mode: false` enables live campaign execution — emails will be sent, Apollo credits will be spent. Only do this with explicit user confirmation.
