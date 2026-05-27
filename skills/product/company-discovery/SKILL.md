---
name: company-discovery
description: Discover and rank companies in a target industry. Evaluates fit against your constraints and generates optimized job search queries.
argument-hint: [industry-or-company-name]
---

# Company Discovery Workflow

**Load and execute:** `workflows/company-discovery/workflow.md`

Read the entire workflow file and execute it step by step. This workflow operates in two modes:

**Enrichment Mode** (specific company):
- Trigger: `/company-discovery Stripe` or "tell me more about Stripe"
- Deep-dive research on a single company
- Gathers remote policy, tech stack, salary data, funding news
- Creates detailed profile in `research/companies/{industry}/{company}.md`

**Discovery Mode** (industry):
- Trigger: `/company-discovery fintech` or "find companies in fintech"
- Discovers 5-10 companies in the target industry
- Evaluates and ranks each by fit
- Creates index and individual profiles in `research/companies/{industry}/`

**Both modes produce:**
- Fit scoring against your constraints
- Hiring signals (funding, growth, leadership changes)
- Optimized job search queries for LinkedIn and other platforms

**Opening Tracking:** Each company profile includes a "Tracked Openings" section that is automatically populated when you run `job-scan` on postings from that company. This creates a per-company view of all opportunities you've analyzed, with fit scores and links to detailed analyses.

Follow all steps exactly as written. Embody Scout's quality-over-quantity approach to company targeting.

$ARGUMENTS
