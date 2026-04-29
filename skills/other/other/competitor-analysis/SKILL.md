---
name: competitor-analysis
description: 'Analyze competitor SEO/GEO: keywords, content, backlinks, AI citations, traffic share gaps. 竞品分析/竞争对手'
version: "9.9.5"
license: Apache-2.0
compatibility: "Claude Code, skills.sh, ClawHub, Vercel Labs, Cursor, Windsurf, Codex CLI, Amp, Gemini CLI, Kimi Code, Qwen Code, CodeBuddy"
homepage: "https://github.com/aaron-he-zhu/seo-geo-claude-skills"
when_to_use: "Use when analyzing competitor SEO strategy, comparing domains, benchmarking against competitors, or finding competitor keywords and content gaps."
argument-hint: "<competitor URL or domain>"
metadata:
  author: aaron-he-zhu
  version: "9.9.5"
  geo-relevance: "medium"
  tags:
    - seo
    - geo
    - competitor-analysis
    - competitive-intelligence
    - benchmarking
    - competitor-keywords
    - competitor-backlinks
    - market-analysis
    - spyfu-alternative
    - 竞品分析
    - 競合分析
    - 경쟁분석
    - analisis-competitivo
  triggers:
    - "analyze competitors"
    - "competitor SEO"
    - "competitive analysis"
    - "competitor keywords"
    - "competitive intelligence"
    - "what are my competitors doing"
    - "why do they rank higher"
    - "spy on competitor SEO"
    - "why do they outrank me"
    - "who are my SEO competitors"
    - "how do I beat my competitors"
    - "SpyFu alternative"
    - "Semrush competitor analysis"
    - "Ahrefs competitor tool"
    - "竞品分析"
    - "竞争对手分析"
    - "竞品SEO"
    - "对标分析"
    - "竞争情报"
    - "竞品怎么做的"
    - "他们排名为什么比我高"
    - "看看对手在干什么"
    - "为什么他们排名好"
    - "競合分析"
    - "競合SEO分析"
    - "ライバル分析"
    - "경쟁 분석"
    - "경쟁사 SEO"
    - "경쟁사 키워드"
    - "análisis de competidores"
    - "análisis competitivo SEO"
    - "análise de concorrentes"
---

# Competitor Analysis

Analyzes competitor SEO and GEO strategies to reveal repeatable wins, weak spots, and market gaps.

## Quick Start

```
Analyze SEO strategy for [competitor URL]
```

```
Compare my site [URL] against [competitor 1], [competitor 2], [competitor 3]
```

## Skill Contract

**Expected output**: a prioritized competitor brief plus the standard handoff summary for `memory/research/`.

- **Reads**: goals, market inputs, tool data, and prior strategy from [CLAUDE.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/CLAUDE.md) and the shared [State Model](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/state-model.md) when available.
- **Writes**: a user-facing analysis and reusable summary.
- **Promotes**: durable competitor facts, keyword priorities, entity candidates, and strategy decisions to `memory/hot-cache.md`, `memory/decisions.md`, and `memory/research/`.
- **Primary next skill**: [content-gap-analysis](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/research/content-gap-analysis/SKILL.md) when the competitive landscape is clear.

### Handoff Summary

> Emit the standard shape from [skill-contract.md §Handoff Summary Format](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/skill-contract.md).

## Data Sources

Optional integrations: ~~SEO tool, ~~analytics, ~~AI monitor. Without tools, ask for competitor URLs, your site metrics, and industry context. See [CONNECTORS.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/CONNECTORS.md).

## Instructions

When a user requests competitor analysis:

1. **Identify Competitors** — separate direct competitors, indirect alternatives, and content competitors if the user has not named them already.
2. **Gather Competitor Data** — capture URL, domain age, estimated traffic, domain authority, business model, target audience, and key offerings.
3. **Analyze Keyword Rankings** — document total rankings, top 10/top 3 counts, high-value keywords, intent mix, and keyword gaps.
4. **Audit Content Strategy** — review content volume, top performers, publishing patterns, themes, and success factors.
5. **Analyze Backlink Profile** — review backlink totals, quality mix, top linking domains, link acquisition patterns, and linkable assets.
6. **Technical SEO Assessment** — evaluate Core Web Vitals, mobile-friendliness, architecture, internal linking, URL structure, and standout strengths/weaknesses.
7. **GEO / AI Citation Analysis** — test which queries cite competitors, what formats get cited, and where competitors still leave openings.
8. **Synthesize Competitive Intelligence** — deliver an Executive Summary, comparison table, CITE comparison, strengths to learn from, weaknesses to exploit, keyword opportunities, content recommendations, and an Immediate / Short-term / Long-term plan.

> **Reference**: See [references/analysis-templates.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/research/competitor-analysis/references/analysis-templates.md) for the compact templates used at each step.

## Example

See [references/example-report.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/research/competitor-analysis/references/example-report.md) for a full sample analyzing HubSpot's marketing keyword dominance.

## Advanced Analysis Types

### Content Gap Analysis

```
Show me content [competitor] has that I don't, sorted by traffic potential
```

### Link Intersection

```
Find sites linking to [competitor 1] AND [competitor 2] but not me
```

### SERP Feature Analysis

```
What SERP features do competitors win? (Featured snippets, PAA, etc.)
```

### Historical Tracking

```
How has [competitor]'s SEO strategy evolved over the past year?
```

## Tips for Success

Analyze 3-5 competitors, include indirect players, and study both strengths and failures.

### Save Results

After delivering, offer to save `memory/research/competitor-analysis/YYYY-MM-DD-<topic>.md` and promote durable conclusions to `memory/hot-cache.md`.

## Reference Materials

- [Analysis Templates](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/research/competitor-analysis/references/analysis-templates.md) — Step-by-step analysis templates
- [Battlecard Template](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/research/competitor-analysis/references/battlecard-template.md) — Quick-reference battlecard format
- [Positioning Frameworks](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/research/competitor-analysis/references/positioning-frameworks.md) — Positioning and differentiation frameworks
- [Example Report](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/research/competitor-analysis/references/example-report.md) — Worked sample

## Next Best Skill

Primary: [content-gap-analysis](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/research/content-gap-analysis/SKILL.md). Also: [serp-analysis](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/research/serp-analysis/SKILL.md) and [backlink-analyzer](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/monitor/backlink-analyzer/SKILL.md).
