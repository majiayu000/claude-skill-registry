---
type: playbook
name: competitor-monitoring-system
description: >
  Set up and run ongoing competitive intelligence monitoring for a client.
  Tracks competitor content, ads, reviews, social, and product moves.
graph:
  provides: [competitive-intelligence-report, competitor-alerts]
  requires: [competitor-list, client-context]
  connects_to:
    - skills/composites/competitor-intel/SKILL.md
    - skills/playbooks/seo-content-engine/SKILL.md
skills_used:
  - skills/composites/competitor-intel
  - skills/capabilities/meta-ad-scraper
  - skills/capabilities/google-ad-scraper
  - skills/capabilities/review-scraper
  - skills/capabilities/blog-scraper
  - skills/capabilities/linkedin-profile-post-scraper
  - skills/capabilities/twitter-scraper
  - skills/capabilities/reddit-scraper
  - skills/capabilities/hacker-news-scraper
---

# Competitor Monitoring System

Set up ongoing competitive intelligence for a client. Monitor competitor content, ads, reviews, social presence, and product moves. Produce regular intelligence reports.

## When to Use

- "Set up competitor monitoring for [client]"
- "Track what [competitors] are doing"
- "Monitor [competitor] content and ads"

## Prerequisites

- List of competitors to track (typically 3-7)
- Client context with competitive positioning
- Competitor founder/executive LinkedIn profiles (for social monitoring)

## Setup Steps

### 1. Define Competitor Watchlist

Create a competitor tracking file: `clients/<client-name>/intelligence/competitor-watchlist.md`

For each competitor, document:
- Company name and URL
- Key products/features
- Founder/exec LinkedIn profiles
- Known content channels (blog URL, YouTube, podcast)
- Review profiles (G2, Capterra URLs)
- Ad library pages (Meta, Google)

### 2. Initial Competitive Baseline

Run the full competitor-intel composite for each competitor to establish a baseline:

**Skill**: competitor-intel (chains reddit + twitter + linkedin + blog + review scrapers)

Plus:
- **Skill**: meta-ad-scraper — Scrape their current Meta ads
- **Skill**: google-ad-scraper — Scrape their current Google ads
- **Skill**: review-scraper — Pull latest G2/Capterra/Trustpilot reviews

**Output**: `clients/<client-name>/intelligence/competitor-baseline.md`

### 3. Configure Monitoring Cadence

| What to Monitor | Frequency | Skill | What to Look For |
|----------------|-----------|-------|-----------------|
| Blog/content output | Weekly | blog-scraper | New posts, topic shifts, SEO attacks |
| Social media posts | Weekly | linkedin-profile-post-scraper + twitter-scraper | Messaging changes, product announcements, engagement patterns |
| Reddit/HN mentions | Weekly | reddit-scraper + hacker-news-scraper | User sentiment, complaints, praise, feature requests |
| Ad creative changes | Bi-weekly | meta-ad-scraper + google-ad-scraper | New campaigns, messaging shifts, spend changes |
| Review sentiment | Monthly | review-scraper | New reviews, rating trends, common complaints |

### 4. Run Monitoring

Each monitoring cycle:

1. Run the relevant scrapers for the cycle type
2. Compare new data against the baseline/previous cycle
3. Flag significant changes:
   - New product features or pricing changes
   - New content targeting our client's keywords
   - Negative review trends (poaching opportunity)
   - New ad campaigns (messaging intelligence)
   - Founder/exec public statements about strategy

### 5. Produce Intelligence Report

After each cycle, produce a brief intelligence summary:

```
# Competitor Intelligence — [Client] — Week of [Date]

## Key Changes
- [Competitor A] published 3 new blog posts targeting "[keyword]"
- [Competitor B] launched new Meta ad campaign focused on [theme]
- [Competitor C] received 5 negative G2 reviews about [issue]

## Recommended Actions
- Publish response content for [Competitor A]'s keyword attack
- Create comparison page addressing [Competitor B]'s new messaging
- Target [Competitor C]'s unhappy customers with migration content

## Detailed Findings
[Per-competitor breakdown]
```

**Output**: `clients/<client-name>/intelligence/competitor-reports/[date].md`

## Ongoing Cadence

- **Weekly**: Content + social monitoring, brief report
- **Bi-weekly**: Ad monitoring
- **Monthly**: Full review scrape + comprehensive report
- **Quarterly**: Re-run full competitor-intel baseline, update watchlist

## Human Checkpoints

- **After setup**: Review competitor watchlist and monitoring plan
- **After each report**: Review recommended actions before executing
