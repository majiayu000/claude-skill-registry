---
name: competitor-intel
description: >
  Competitor intelligence system. Track competitors across Reddit, Twitter/X, and LinkedIn.
  Run one-time deep research to create competitor profiles, then automate daily/weekly
  monitoring with consolidated reports and actionable signals. Reports delivered as markdown
  files and via email.
---

# Competitor Intelligence

Automated competitor monitoring and intelligence gathering system.

**Important:** Before running any competitor intel commands, ask the user which competitors they want to track. Do not assume or hardcode competitor names.

## Quick Start

### One-Time: Research a New Competitor

```bash
# Create a new competitor profile (agent-driven research)
python3 competitor-intel/scripts/setup_competitor.py --name "CompanyName" --website https://example.com --slug companyname
```

Then run an agent research session to populate the profile.

### Daily: Reddit + Twitter Monitoring

```bash
# Run daily signals collection (automated via cron)
python3 competitor-intel/scripts/run_daily.py

# Or for a specific competitor
python3 competitor-intel/scripts/run_daily.py --competitor <competitor-slug>
```

### Weekly: Deep Dive + LinkedIn

```bash
# Run weekly deep dive (Monday mornings)
python3 competitor-intel/scripts/run_weekly.py
```

### Generate Report

```bash
# Generate daily or weekly report
python3 competitor-intel/scripts/generate_report.py --type daily --date 2026-02-21
python3 competitor-intel/scripts/generate_report.py --type weekly --date 2026-02-21
```

## Data Structure

- `competitor-intel/competitors/[slug]/profile.md` - Deep research profile per competitor
- `competitor-intel/competitors/[slug]/snapshots/` - Point-in-time weekly snapshots
- `competitor-intel/reports/` - Daily and weekly digest reports
- `competitor-intel/raw-data/` - Raw JSON from Reddit/Twitter scrapes
- `competitor-intel/config.json` - Global configuration

## Tracked Competitors

Competitors are configured per-project. Ask the user which competitors to track, then add them here:

| Competitor | Slug | Status |
|---|---|---|
| *(ask user)* | — | — |

## Automation

- **Daily (8 AM PT)**: Reddit + Twitter scrape → daily report → email
- **Weekly (Monday 9 AM PT)**: Deep dive + LinkedIn + weekly report → email

## Dependencies

- Apify API (Reddit + Twitter scraping) - token in config.json
- Web search (LinkedIn founder tracking, one-time research)
- AgentMail (report delivery)
