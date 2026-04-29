---
name: rank-tracker
description: 'Track keyword rankings and SERP feature changes in traditional search and AI responses over time. 排名追踪/SERP监控'
version: "9.9.5"
license: Apache-2.0
compatibility: "Claude Code, skills.sh, ClawHub, Vercel Labs, Cursor, Windsurf, Codex CLI, Amp, Gemini CLI, Kimi Code, Qwen Code, CodeBuddy"
homepage: "https://github.com/aaron-he-zhu/seo-geo-claude-skills"
when_to_use: "Use when tracking keyword rankings, monitoring position changes, comparing ranking snapshots, or detecting ranking drops."
argument-hint: "<domain> [keyword list]"
metadata:
  author: aaron-he-zhu
  version: "9.9.5"
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
    - "track rankings"
    - "check keyword positions"
    - "ranking changes"
    - "keyword tracking"
    - "position monitoring"
    - "how am I ranking"
    - "did my rankings change"
    - "where do I rank now"
    - "check my positions"
    - "how are my rankings doing"
    - "排名追踪"
    - "关键词排名"
    - "SERP位置监控"
    - "排名变化"
    - "查排名"
    - "排名变了吗"
    - "我排第几"
    - "ランキング追跡"
    - "検索順位チェック"
    - "順位変動"
    - "キーワード順位確認"
    - "순위 추적"
    - "키워드 순위"
    - "순위 확인"
    - "내 순위 어떻게 됐어?"
    - "seguimiento de rankings"
    - "posición en buscadores"
    - "posicionamiento SEO"
    - "en qué posición estoy"
    - "rastreamento de rankings"
    - "monitoramento de posições"
    - "posição no Google"
---

# Rank Tracker

Tracks keyword positions, SERP feature ownership, and AI visibility over time.

## Quick Start

```
Set up rank tracking for [domain] targeting these keywords: [keyword list]
```

```
Analyze ranking changes for [domain] over the past [time period]
```

## Skill Contract

**Expected output**: a ranking report or delta summary plus the standard handoff summary for `memory/monitoring/`.

- **Reads**: current metrics, baselines, alert thresholds, and reporting context from [CLAUDE.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/CLAUDE.md) and the shared [State Model](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/state-model.md) when available.
- **Writes**: a user-facing monitoring deliverable and reusable summary.
- **Promotes**: significant changes, confirmed anomalies, and follow-up actions to `memory/open-loops.md` and `memory/decisions.md`.
- **Primary next skill**: [alert-manager](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/monitor/alert-manager/SKILL.md) when recurring monitoring should become automated.

### Handoff Summary

> Emit the standard shape from [skill-contract.md §Handoff Summary Format](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/skill-contract.md).

## Data Sources

All integrations optional (see [CONNECTORS.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/CONNECTORS.md)). With tools, pull rankings from ~~SEO tool, impressions from ~~search console, traffic from ~~analytics, and AI citations from ~~AI monitor. Without tools, ask for positions, volumes, competitor data, and SERP feature status.

## Instructions

When a user requests rank tracking or analysis:

1. **Set Up Keyword Tracking** — configure domain, market, device, language, update frequency, priorities, and competitor watchlist.
2. **Record Current Rankings** — summarize position ranges, detailed rankings, ranking URLs, feature ownership, and movement.
3. **Analyze Ranking Changes** — highlight biggest wins, declines, stable terms, new rankings, lost rankings, likely causes, and recovery ideas.
4. **Track SERP Features** — compare ownership of snippets, PAA, image/video packs, local packs, and related feature shifts.
5. **Track GEO / AI Visibility** — monitor AI Overview presence, citation rate, citation position, and trend.
6. **Compare Against Competitors** — report share of voice, head-to-head comparisons, and threat levels.
7. **Generate Ranking Report** — summarize overall trend, key wins, concerns, opportunities, SERP feature changes, GEO visibility, and recommendations.

> **Reference**: See [references/ranking-analysis-templates.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/monitor/rank-tracker/references/ranking-analysis-templates.md) for the complete output templates for all seven steps.

## Example

Sample outcome: average position improves from 15.3 to 12.8, top-10 keywords rise from 12 to 17, and the report highlights the biggest winners, biggest drops, and next actions.

## Tips for Success

Track consistently, segment by intent, watch competitors, and include SERP feature plus GEO signals.

## Rank Change Quick Reference

### Response Protocol

| Change | Timeframe | Action |
|--------|-----------|--------|
| Drop 1-3 positions | Wait 1-2 weeks | Monitor — may be normal fluctuation |
| Drop 3-5 positions | Investigate within 1 week | Check technical issues and competitor changes |
| Drop 5-10 positions | Investigate immediately | Run a full diagnostic: technical, content, links |
| Drop off page 1 | Emergency response | Comprehensive audit + recovery plan |
| Position gained | Document and learn | Identify what worked and replicate |

> **Reference**: See [references/tracking-setup-guide.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/monitor/rank-tracker/references/tracking-setup-guide.md) for tracking setup, root-cause taxonomy, CTR benchmarks, SERP feature impact, and algorithm-update assessment.

### Save Results

Ask "Save these results?" If yes, write `memory/monitoring/YYYY-MM-DD-<topic>.md` with headline finding, actions, and open loops.

## Reference Materials

- [Tracking Setup Guide](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/monitor/rank-tracker/references/tracking-setup-guide.md) — Setup rules, feature tracking, and interpretation guidance

## Next Best Skill

Initial setup (no baseline) → [alert-manager](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/monitor/alert-manager/SKILL.md). Subsequent runs (baseline exists) → Terminal. Visited-set rule applies per [skill-contract.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/skill-contract.md).
