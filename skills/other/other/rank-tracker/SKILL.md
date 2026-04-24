---
name: rank-tracker
description: 'Track keyword rankings and SERP feature changes in traditional search and AI responses over time. 排名追踪/SERP监控'
version: "9.1.0"
license: Apache-2.0
compatibility: "Claude Code, skills.sh, ClawHub, Vercel Labs, Cursor, Windsurf, Codex CLI, Amp, Gemini CLI, Kimi Code, Qwen Code, CodeBuddy"
homepage: "https://github.com/aaron-he-zhu/seo-geo-claude-skills"
when_to_use: "Use when tracking keyword rankings, monitoring position changes, comparing ranking snapshots, or detecting ranking drops."
argument-hint: "<domain> [keyword list]"
metadata:
  author: aaron-he-zhu
  version: "9.1.0"
  geo-relevance: "medium"
  tags:
    - seo
    - geo
    - rank-tracking
    - keyword-rankings
    - serp-positions
    - ranking-changes
    - position-tracking
    - 排名追踪
    - ランキング追跡
    - 순위추적
    - seguimiento-rankings
  triggers:
    # EN-formal
    - "track rankings"
    - "check keyword positions"
    - "ranking changes"
    - "keyword tracking"
    - "position monitoring"
    # EN-casual
    - "how am I ranking"
    - "did my rankings change"
    - "where do I rank now"
    - "check my positions"
    # EN-question
    - "how are my rankings doing"
    # ZH-pro
    - "排名追踪"
    - "关键词排名"
    - "SERP位置监控"
    - "排名变化"
    # ZH-casual
    - "查排名"
    - "排名变了吗"
    - "我排第几"
    # JA
    - "ランキング追跡"
    - "検索順位チェック"
    - "順位変動"
    - "キーワード順位確認"
    # KO
    - "순위 추적"
    - "키워드 순위"
    - "순위 확인"
    - "내 순위 어떻게 됐어?"
    # ES
    - "seguimiento de rankings"
    - "posición en buscadores"
    - "posicionamiento SEO"
    - "en qué posición estoy"
    # PT
    - "rastreamento de rankings"
    - "monitoramento de posições"
    - "posição no Google"
---

# Rank Tracker


Tracks, analyzes, and reports on keyword ranking positions over time. Monitors both traditional SERP rankings and AI/GEO visibility to provide comprehensive search performance insights.

## What This Skill Does

Tracks keyword positions, detects ranking movements, benchmarks against competitors, monitors SERP features and AI citations, and generates ranking performance reports.

## Quick Start

Start with one of these prompts. Finish with a short handoff summary using the repository format in [Skill Contract](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/skill-contract.md).

### Set Up Tracking

```
Set up rank tracking for [domain] targeting these keywords: [keyword list]
```

### Analyze Rankings

```
Analyze ranking changes for [domain] over the past [time period]
```

### Compare to Competitors

```
Compare my rankings to [competitor] for [keywords]
```

### Generate Reports

```
Create a ranking report for [domain/campaign]
```

## Skill Contract

**Expected output**: a delta summary, alert/report output, and a short handoff summary ready for `memory/monitoring/`.

- **Reads**: current metrics, previous baselines, alert thresholds, and reporting context from [CLAUDE.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/CLAUDE.md) and the shared [State Model](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/state-model.md) when available.
- **Writes**: a user-facing monitoring deliverable plus a reusable summary that can be stored under `memory/monitoring/`.
- **Promotes**: significant changes, confirmed anomalies, and follow-up actions to `memory/open-loops.md` and `memory/decisions.md`.
- **Next handoff**: use the `Next Best Skill` below when a change needs action.

### Handoff Summary

> Emit the standard shape from [skill-contract.md §Handoff Summary Format](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/skill-contract.md).

## Data Sources

All integrations optional (see [CONNECTORS.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/CONNECTORS.md)). With tools connected, pulls rankings from ~~SEO tool, impressions from ~~search console, traffic from ~~analytics, and AI citations from ~~AI monitor. Without tools, ask user for keyword positions, search volumes, competitor data, and SERP feature status.

## Instructions

When a user requests rank tracking or analysis:

1. **Set Up Keyword Tracking** -- Configure domain, location, device, language, update frequency. Add keywords with volume, current rank, type, and priority. Set up competitor tracking and keyword categories (brand/product/informational/commercial).

2. **Record Current Rankings** -- Ranking overview by position range (#1, #2-3, #4-10, #11-20, etc.), position distribution visualization, detailed rankings with URL, SERP features, and change.

3. **Analyze Ranking Changes** -- Overall movement metrics, biggest improvements and declines with hypothesized causes, recommended recovery actions, stable keywords, new rankings, lost rankings.

4. **Track SERP Features** -- Feature ownership comparison vs competitors (snippets, PAA, image/video pack, local pack), featured snippet status, PAA appearances.

5. **Track GEO/AI Visibility** -- AI Overview presence per keyword, citation rate and position, GEO performance trend over time, improvement opportunities.

6. **Compare Against Competitors** -- Share of voice table, head-to-head comparison per keyword, competitor movement alerts with threat level.

7. **Generate Ranking Report** -- Executive summary with overall trend, position distribution, key highlights (wins/concerns/opportunities), detailed analysis, SERP feature report, GEO visibility, competitive position, recommendations.

   > **Reference**: See [references/ranking-analysis-templates.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/monitor/rank-tracker/references/ranking-analysis-templates.md) for complete output templates for all 7 steps.

## Example

**User**: "Analyze my ranking changes for the past month"

**Output**:

```markdown
# Ranking Analysis: [current month, year]

## Summary

Your average position improved from 15.3 to 12.8 (-2.5 positions = better)
Keywords in top 10 increased from 12 to 17 (+5)

## Biggest Wins

| Keyword | Old | New | Change | Possible Cause |
|---------|-----|-----|--------|----------------|
| email marketing tips | 18 | 5 | +13 | Likely driven by content refresh |
| best crm software | 24 | 11 | +13 | Correlates with new backlinks acquired |
| sales automation | 15 | 7 | +8 | Correlates with schema markup addition |

## Needs Attention

| Keyword | Old | New | Change | Action |
|---------|-----|-----|--------|--------|
| marketing automation | 4 | 12 | -8 | Likely displaced by new HubSpot guide |

**Recommended**: Update your marketing automation guide with [current year] statistics and examples.
```

## Tips for Success

1. **Track consistently** - Same time, same device, same location
2. **Include enough keywords** - 50-200 for meaningful data
3. **Segment by intent** - Track brand, commercial, informational separately
4. **Monitor competitors** - Context makes your data meaningful
5. **Track SERP features** - Position 1 without snippet may lose to position 4 with snippet
6. **Include GEO metrics** - AI visibility increasingly important

## Rank Change Quick Reference

### Response Protocol

| Change | Timeframe | Action |
|--------|-----------|--------|
| Drop 1-3 positions | Wait 1-2 weeks | Monitor -- may be normal fluctuation |
| Drop 3-5 positions | Investigate within 1 week | Check for technical issues, competitor changes |
| Drop 5-10 positions | Investigate immediately | Full diagnostic: technical, content, links |
| Drop off page 1 | Emergency response | Comprehensive audit + recovery plan |
| Position gained | Document and learn | What worked? Can you replicate? |

> **Reference**: See [references/tracking-setup-guide.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/monitor/rank-tracker/references/tracking-setup-guide.md) for root cause taxonomy, CTR benchmarks by position, SERP feature CTR impact, algorithm update assessment, tracking configuration best practices, keyword selection and grouping strategies, and data interpretation guidelines.


### Save Results

Ask "Save these results?" If yes, write a dated summary to `memory/monitoring/YYYY-MM-DD-<topic>.md` with headline finding, actionable items, and open loops.

## Reference Materials

- [Tracking Setup Guide](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/monitor/rank-tracker/references/tracking-setup-guide.md) — Configuration best practices, device/location settings, and SERP feature tracking setup

## Next Best Skill

Initial setup (no baseline) → [alert-manager](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/monitor/alert-manager/SKILL.md). Subsequent runs (baseline exists) → Terminal. Visited-set rule applies per [skill-contract.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/skill-contract.md).
