---
name: content-refresher
description: 'Use when updating outdated content, fixing traffic/ranking decay, refreshing stats, adding new sections, or improving freshness signals. 内容更新/排名恢复'
version: "9.9.5"
license: Apache-2.0
compatibility: "Claude Code, skills.sh, ClawHub, Vercel Labs, Cursor, Windsurf, Codex CLI, Amp, Gemini CLI, Kimi Code, Qwen Code, CodeBuddy"
homepage: "https://github.com/aaron-he-zhu/seo-geo-claude-skills"
when_to_use: "Use when updating outdated content, refreshing old articles, improving declining pages, or adding new information to existing content."
argument-hint: "<URL of outdated content>"
metadata:
  author: aaron-he-zhu
  version: "9.9.5"
  geo-relevance: "medium"
  tags:
    - seo
    - geo
    - content-refresh
    - content-update
    - content-decay
    - ranking-recovery
    - evergreen-content
    - content-lifecycle
    - 内容更新
    - コンテンツ更新
    - 콘텐츠갱신
    - actualizar-contenido
  triggers:
    # EN-formal
    - "update old content"
    - "refresh content"
    - "content is outdated"
    - "content decay"
    - "content refresh strategy"
    # EN-casual
    - "traffic is dropping"
    - "ranking dropped"
    - "this post is outdated"
    - "my old content needs updating"
    # EN-question
    - "how to fix declining traffic"
    - "how often should I update content"
    # EN-competitor
    - "Clearscope content refresh"
    - "MarketMuse content update"
    # ZH-pro
    - "内容更新"
    - "内容刷新"
    - "排名恢复"
    - "内容衰减"
    - "内容生命周期"
    # ZH-casual
    - "排名下降了"
    - "文章过时了"
    - "流量掉了"
    - "老文章怎么办"
    # JA
    - "コンテンツ更新"
    - "コンテンツリフレッシュ"
    - "記事更新"
    # KO
    - "콘텐츠 갱신"
    - "콘텐츠 업데이트"
    - "순위 하락"
    - "순위 하락 원인"
    - "오래된 글 어떻게 해?"
    # ES
    - "actualizar contenido"
    - "refrescar contenido antiguo"
    # PT
    - "atualizar conteúdo"
---

# Content Refresher

Identifies outdated content, scores decay/freshness, prioritizes refresh work, and produces update plans with GEO and republishing guidance.

## Quick Start

```text
Find content on [domain] that needs refreshing
Which of my blog posts have lost the most traffic?
Refresh this article for [current year]: [URL/content]
Update this content to outrank [competitor URL]: [your URL]
Create a content refresh strategy for [domain/topic]
```

## Skill Contract

**Expected output**: a scored diagnosis, prioritized repair plan, and a short handoff summary ready for `memory/audits/`.

- **Reads**: the current page or site state, symptoms, prior audits, and current priorities from [CLAUDE.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/CLAUDE.md) and the shared [State Model](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/state-model.md) when available.
- **Writes**: a user-facing audit or optimization plan plus a reusable summary that can be stored under `memory/audits/`.
- **Promotes**: blocking defects, repeated weaknesses, and fix priorities to `memory/open-loops.md` and `memory/decisions.md`.
- **Next handoff**: use the `Next Best Skill` below when the repair path is clear.

### Handoff Summary

> Emit the standard shape from [skill-contract.md §Handoff Summary Format](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/skill-contract.md).

## Data Sources

Use ~~analytics, ~~search console, and ~~SEO tool when connected; otherwise ask for traffic data, ranking history, publish dates, candidate URLs, and competitor examples. See [CONNECTORS.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/CONNECTORS.md).

## Instructions

When a user requests content refresh help:

1. **CORE-EEAT Quick Score** -- Estimate all 8 dimensions, prioritize red/yellow areas, and hand off to [content-quality-auditor](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/cross-cutting/content-quality-auditor/SKILL.md) for full scoring when needed.
2. **Identify Refresh Candidates** -- Use age, dated claims, declining traffic, lost rankings, broken links, SERP shifts, and missing topics.
3. **Analyze Page-Level Decay** -- Compare 6-month-old vs current performance, keyword deltas, SERP intent, competitor updates, and the why-refresh rationale.
4. **Define Updates Needed** -- Capture outdated elements, competitor/PAA gaps, SEO updates, GEO updates, links, images, sources, and dates.
5. **Create Refresh Plan** -- Specify title, structure, new sections, refreshed statistics, internal/external links, images, and validation requirements.
6. **Write Refresh Content** -- Draft updated intro, replacement sections, refreshed facts, FAQ answers, and Changes Made notes.
7. **Optimize for GEO** -- Add 40-60 word definitions, quotable statements, Q&A, dated citations, and standalone factual statements.
8. **Set Republishing Strategy** -- Use published-date update for 50%+ new content, last-updated date for 20-50%, original date for <20%; update schema, sitemap `lastmod`, cache, Search Console, and 4-6 week monitoring.
9. **Create Refresh Report** -- Summarize completed changes, expected outcomes, owners, next review date, and open loops.

> **Reference**: [references/refresh-templates.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/optimize/content-refresher/references/refresh-templates.md) has compact templates for steps 2-9.

## Example

**User**: "Refresh my blog post about 'best cloud hosting providers'"

**Output**: CORE-EEAT quick score flags weak Referenceability, Experience, and Trust; recommends pricing refresh, broken-link fixes, author credential additions, affiliate disclosure, and a Changes Made block ready for republish.

> **Reference**: See [references/refresh-example.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/optimize/content-refresher/references/refresh-example.md) for the full worked example and checklist.

## Tips for Success

Prioritize by ROI/search demand, make substantive improvements instead of date-only edits, add stronger evidence than competitors, track post-publish rankings/traffic, and treat every refresh as a GEO citation opportunity.

> **Reference data**: [references/content-decay-signals.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/optimize/content-refresher/references/content-decay-signals.md) covers decay signals, lifecycle stages, refresh-vs-rewrite decisions, and content-type strategy.

### Save Results

Ask to save results; if yes, write a dated summary to `memory/audits/content-refresher/YYYY-MM-DD-<topic>.md`. Append veto-level issues to `memory/hot-cache.md` automatically.

**Gate check recommended**: Run content-quality-auditor on refreshed content before republishing.

## Reference Materials

- [Content Decay Signals](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/optimize/content-refresher/references/content-decay-signals.md) -- Decay indicators, lifecycle stages, and refresh triggers by content type
- [Refresh Templates](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/optimize/content-refresher/references/refresh-templates.md) -- Compact templates for steps 2-9
- [Refresh Example & Checklist](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/optimize/content-refresher/references/refresh-example.md) -- Full worked example and pre/post-refresh checklist

## Next Best Skill

Primary: [content-quality-auditor](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/cross-cutting/content-quality-auditor/SKILL.md) -- re-score refreshed content before shipping.
