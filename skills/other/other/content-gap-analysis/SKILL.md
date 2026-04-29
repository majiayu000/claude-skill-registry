---
name: content-gap-analysis
description: 'Find content gaps: topics and keywords competitors cover that you don''t, with editorial calendar. 内容缺口/选题规划'
version: "9.9.5"
license: Apache-2.0
compatibility: "Claude Code, skills.sh, ClawHub, Vercel Labs, Cursor, Windsurf, Codex CLI, Amp, Gemini CLI, Kimi Code, Qwen Code, CodeBuddy"
homepage: "https://github.com/aaron-he-zhu/seo-geo-claude-skills"
when_to_use: "Use when finding content gaps between two domains, discovering missing topics, or identifying coverage holes versus competitors."
argument-hint: "<your domain> <competitor domain>"
metadata:
  author: aaron-he-zhu
  version: "9.9.5"
  geo-relevance: "medium"
  tags:
    - seo
    - geo
    - content-gaps
    - topic-analysis
    - content-strategy
    - editorial-calendar
    - competitive-gap
    - content-opportunities
    - 内容缺口
    - コンテンツギャップ
    - 콘텐츠갭
    - brechas-contenido
  triggers:
    - "find content gaps"
    - "content opportunities"
    - "topic analysis"
    - "editorial calendar"
    - "what am I missing"
    - "what do competitors write about"
    - "what should I cover next"
    - "they cover this but I don't"
    - "what topics am I missing"
    - "what content should I create"
    - "内容缺口分析"
    - "选题规划"
    - "内容机会"
    - "竞品话题"
    - "缺什么内容"
    - "竞品写了什么"
    - "还应该写什么"
    - "コンテンツギャップ"
    - "コンテンツ機会"
    - "콘텐츠 갭 분석"
    - "콘텐츠 기회"
    - "brechas de contenido"
    - "oportunidades de contenido"
    - "lacunas de conteúdo"
---

# Content Gap Analysis

Identifies content opportunities by comparing your site against competitors and scoring the gaps worth closing first.

## Quick Start

```
Find content gaps between my site [URL] and [competitor URLs]
```

```
What content am I missing compared to my top 3 competitors?
```

## Skill Contract

**Expected output**: a prioritized gap brief plus the standard handoff summary for `memory/research/`.

- **Reads**: goals, market inputs, tool data, and prior strategy from [CLAUDE.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/CLAUDE.md) and the shared [State Model](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/state-model.md) when available.
- **Writes**: a user-facing analysis and reusable summary.
- **Promotes**: durable keyword priorities, competitor facts, and strategy decisions to `memory/hot-cache.md`, `memory/decisions.md`, and `memory/research/`.
- **Primary next skill**: [seo-content-writer](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/build/seo-content-writer/SKILL.md) when the prioritized gap list is approved.

### Handoff Summary

> Emit the standard shape from [skill-contract.md §Handoff Summary Format](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/skill-contract.md).

## Data Sources

Optional integrations: ~~SEO tool, ~~search console, ~~analytics, ~~AI monitor. Without tools, ask for site URL, content inventory, competitor URLs, and business goals. See [CONNECTORS.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/CONNECTORS.md).

## Instructions

When a user requests content gap analysis:

1. **Define Analysis Scope** — confirm your site, competitors, topic focus, content types, audience, and business goals.
2. **Audit Your Existing Content** — map indexed pages, content types, topic clusters, winners, and weaknesses.
3. **Analyze Competitor Content** — compare content volume, traffic, type mix, topic coverage, and unique assets.
4. **Identify Keyword Gaps** — group gaps into High Priority, Quick Wins, and Long-term based on volume, difficulty, and relevance.
5. **Map Topic Gaps** — compare topic-cluster coverage and recommend pillar / cluster approaches for missing themes.
6. **Identify Content Format Gaps** — compare guides, tutorials, comparisons, case studies, tools, templates, video, and research.
7. **Analyze GEO / AI Gaps** — identify missing Q&A, definition, and comparison content that competitors get cited for.
8. **Map to Audience Journey** — compare Awareness, Consideration, Decision, and Retention coverage.
9. **Prioritize and Create Action Plan** — deliver an Executive Summary, Prioritized Gap List (Quick Wins / Strategic Builds / Long-term), Content Calendar, and Success Metrics.

> **Reference**: See [references/analysis-templates.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/research/content-gap-analysis/references/analysis-templates.md) for the compact templates used in each step.

## Example

See [references/example-report.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/research/content-gap-analysis/references/example-report.md) for a full SaaS marketing sample.

## Advanced Analysis

### Competitive Cluster Comparison

```
Compare our topic cluster coverage for [topic] vs top 5 competitors
```

### Temporal Gap Analysis

```
What content have competitors published in the last 6 months that we haven't covered?
```

### Intent-Based Gaps

```
Find gaps in our [commercial/informational] intent content
```

## Tips for Success

Focus on actionable gaps, respect execution constraints, and include GEO opportunities instead of only traditional search gaps.

### Save Results

After delivering, offer to save `memory/research/content-gap-analysis/YYYY-MM-DD-<topic>.md` and promote durable conclusions to `memory/hot-cache.md`.

## Reference Materials

- [Analysis Templates](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/research/content-gap-analysis/references/analysis-templates.md) — Gap-analysis templates
- [Gap Analysis Frameworks](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/research/content-gap-analysis/references/gap-analysis-frameworks.md) — Audit and prioritization frameworks
- [Example Report](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/research/content-gap-analysis/references/example-report.md) — Worked sample

## Next Best Skill

Primary: [seo-content-writer](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/build/seo-content-writer/SKILL.md).
