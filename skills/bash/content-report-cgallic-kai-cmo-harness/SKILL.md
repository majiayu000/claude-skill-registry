---
name: content-report
description: Pull performance data for published content across every surface — LinkedIn, Dev.to, Google Search Console, GA4, and AI citation tracking (Perplexity, Anthropic, OpenAI). Grades each piece as winner, average, or underperformer and surfaces whether an AI search engine has cited it.
---

# /content-report — The Analytics Lead

Pull performance data for your published content. Cross-references Google Search Console (position, CTR), GA4 (session duration), platform-native stats (LinkedIn impressions, Dev.to views), and AI citation checks (Perplexity, Anthropic, OpenAI web search) to grade each piece.

## Preamble

```bash
source "$(dirname "$0")/../lib/preamble.sh"
```

## Arguments

Optional:
- **--site**: Filter by site key (e.g., `kaicalls`, `connorgallic`, `meetkai`)
- **--all**: Show all published content (default if no args)

Example: `/content-report --site kaicalls`
Example: `/content-report`

## The Skill

### Step 0: Fold In Any Legacy Log

The CANONICAL publish log is `data/content_log.json` (the learning loop — performance_check, pattern_extract, weekly_report — reads only this file). If a legacy `~/.kai-marketing/content-log.jsonl` still exists, merge it first so its winners reach the learning loop (idempotent; safe to re-run):

```bash
python3 -m scripts.content.migrate_legacy_log
python3 -m scripts.self_improvement.performance_check --reconcile-only   # rebuild 30-day checks in data/pending_checks/
```

### Step 1: Refresh Data

Before the report, refresh the data sources you care about. Skip any step where you don't have the API key.

```bash
# Dev.to — requires DEVTO_API_KEY (https://dev.to/settings/extensions)
python3 -m scripts.content.tracker_cli pull-devto

# AI citations — requires at least one of PERPLEXITY_API_KEY, ANTHROPIC_API_KEY, OPENAI_API_KEY
python3 -m scripts.content.tracker_cli citations

# LinkedIn is manual — record per article (interactive):
python3 -m scripts.content.tracker_cli linkedin --id <entry_id> --interactive
# Or non-interactive:
python3 -m scripts.content.tracker_cli linkedin --id <entry_id> \
    --url https://linkedin.com/pulse/... \
    --impressions 1850 --reactions 34 --comments 7 --reshares 2 --dms 3
```

### Step 2: Load Enriched Report

```bash
python3 -m scripts.content.tracker_cli report --format json
```

If no published content is found, tell the user: "No published content in the log. Content is logged automatically when it passes `/content-gate`."

### Step 3: Display Performance Overview

Present the data:

```
CONTENT PERFORMANCE REPORT
══════════════════════════════════════════

Total pieces: {N}
  Winners:         {green} {count} ({pct}%)
  Average:         {yellow} {count} ({pct}%)
  Underperformers: {red} {count} ({pct}%)
  Pending (< 30d): {gray} {count}

GRADING THRESHOLDS (search surface):
  Position ≤ 5  |  CTR ≥ 5%  |  Session ≥ 90s

RECENT CONTENT:
  [+] kaicalls-20260316   "AI receptionists"       pos:3  CTR:7.2%  91s   WINNER   li=4.2K/86r/3dm  cits=2/4
  [+] connor-20260414     "MeetKai audit"          —      —         —     PENDING  li=1.9K/52r/1dm  cits=1/3
  [~] kaicalls-20260310   "law firm answering"     pos:12 CTR:2.1%  45s   AVERAGE  devto=320v/12r   cits=0/3
  [-] abp-20260308        "backyard design"        pos:28 CTR:0.4%  22s   UNDER    li=80/1r         cits=0/3
  [?] kaicalls-20260322   "virtual receptionist"   (pending — 8 days old)
```

Legend for the compact metric strings:
- `li=1850/34r/2dm` — LinkedIn impressions / reactions / DMs
- `devto=450v/12r` — Dev.to views / reactions
- `cits=2/4` — positive AI citations / total citation checks run

### Step 4: Insights

If there are 3+ graded pieces, provide insights:
- Which **format** performs best (blog vs linkedin vs devto vs email)
- Which **persona** performs best
- Which **hook type** performs best (if tracked)
- Average quality gate score of winners vs underperformers
- **AI citation patterns** — which providers cite our content most often, which queries trigger citations, whether articles with high GSC position also attract AI citations

Example:
```
INSIGHTS:
  Best performing format:  linkedin (3/4 winners)
  Best performing persona: Shock Absorber (2/2 winners)
  Avg gate score winners:  82/100  vs  underperformers: 61/100

  AI CITATIONS:
    Most citing provider:  Perplexity (4 citations across 3 articles)
    Top-cited article:     connor-20260414 — 3 citations
    Queries that cite us:  "best AI answering service", "Connor Gallic AI",
                           "answering service alternatives 2026"
    Articles never cited:  abp-20260308, kaicalls-20260310  →  strong GEO-rewrite candidates
```

### Step 5: Recommend Next Actions

Based on the data:
- **Pending 30-day review**: "3 pieces ready for 30-day review. Performance data will be pulled on next check."
- **Underperformers**: "Consider revising underperformers or running `/content-retro` to extract patterns."
- **Missing LinkedIn stats**: "N LinkedIn pieces published in the last 14 days have no recorded metrics. Run `kai-tracker linkedin --id <id> --interactive` to record them."
- **Missing citation checks**: "N tracked articles have no `citations-targets.json` entries. Use `kai-tracker targets --id <id> --add-query '...'` to configure."
- **No recent content**: "No content published in the last 14 days. Run `/content-ideas` for topic suggestions."

## Data Sources Behind This Skill

| Source | Where it lives | Refreshed by |
|--------|---------------|--------------|
| Publish log (canonical) | `data/content_log.json` | `/content-write` Step 6 / `scripts.content.content_log.log_entry` + `mark_published` |
| 30-day pending checks | `data/pending_checks/{id}.json` | Auto-created by `content_log` when a real URL is set; rebuilt by `performance_check --reconcile-only` |
| Legacy publish log | `~/.kai-marketing/content-log.jsonl` | Read-only — fold into the canonical log via `scripts.content.migrate_legacy_log` (Step 0) |
| Platform metrics (Dev.to, LinkedIn) | `~/.kai-marketing/metrics/{id}.json` | `kai-tracker pull-devto` / `kai-tracker linkedin` |
| AI citation events | `~/.kai-marketing/citations/{id}.jsonl` | `kai-tracker citations` (cron-compatible) |
| Citation targets | `~/.kai-marketing/citations-targets.json` | `kai-tracker targets --id <id> --add-query '...'` |
| GSC + GA4 grading | Live API calls via `scripts/self_improvement/performance_check.py` | Invoked automatically by `kai-tracker report` |

## Environment Variables

| Variable | Required for | How to get it |
|----------|--------------|---------------|
| `DEVTO_API_KEY` | Dev.to stat pulls | https://dev.to/settings/extensions |
| `PERPLEXITY_API_KEY` | Perplexity citation checks | https://www.perplexity.ai/settings/api |
| `ANTHROPIC_API_KEY` | Claude web-search citation checks | Console API key (already required by the harness) |
| `OPENAI_API_KEY` | OpenAI web-search citation checks | Existing harness API key |

If a key is missing, the corresponding check is skipped with a warning — the report still runs with whatever data is available.

## Error Handling

- **No content log**: Direct to `/content-write` to publish first piece
- **GSC/GA4 API unavailable**: Show content log with platform/citation data, note "Search surface performance unavailable — showing platform metrics only"
- **All AI citation providers missing keys**: Skip Step 1's citations call, note in the report "Citation tracking unavailable — set at least one of PERPLEXITY_API_KEY / ANTHROPIC_API_KEY / OPENAI_API_KEY"

## Chain State

**Reads from:** `data/content_log.json` (canonical publish log), `data/pending_checks/`, `~/.kai-marketing/metrics/`, `~/.kai-marketing/citations/` (platform/citation scratch)
**Feeds into:** `/content-retro` (weekly pattern analysis, now including citation patterns)

## Scheduling

Recommended cadence for a solo operator:
- **On publish**: `/content-gate` writes to the log automatically
- **Weekly**: `kai-tracker pull-devto` + `kai-tracker citations` (put in cron or weekly heartbeat)
- **Per LinkedIn post, 24h + 7d after publish**: `kai-tracker linkedin --id <id> --interactive`
- **30 days after publish**: the existing performance_check cron handles GSC + GA4 automatically
