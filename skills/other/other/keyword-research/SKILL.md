---
name: keyword-research
description: 'Find high-value SEO keywords: search volume, difficulty, intent classification, topic clusters. 关键词研究/内容选题'
version: "9.9.5"
license: Apache-2.0
compatibility: "Claude Code, skills.sh, ClawHub, Vercel Labs, Cursor, Windsurf, Codex CLI, Amp, Gemini CLI, Kimi Code, Qwen Code, CodeBuddy"
homepage: "https://github.com/aaron-he-zhu/seo-geo-claude-skills"
when_to_use: "Use when starting keyword research for a new page, topic, or campaign. Also when the user asks about search volume, keyword difficulty, topic clusters, long-tail keywords, what to write about, 关键词研究, 挖词, 内容选题, or 搜什么词."
argument-hint: "<topic or seed keyword> [market/language]"
metadata:
  author: aaron-he-zhu
  version: "9.9.5"
  geo-relevance: "medium"
  tags:
    - seo
    - geo
    - keyword-research
    - search-volume
    - keyword-difficulty
    - topic-clusters
    - search-intent
    - long-tail-keywords
    - 关键词研究
    - SEO关键词
    - キーワード調査
    - 키워드분석
    - palabras-clave
  triggers:
    - "keyword research"
    - "find keywords"
    - "search volume analysis"
    - "keyword difficulty"
    - "what should I write about"
    - "give me keyword ideas"
    - "how do I find good keywords"
    - "how competitive is this keyword"
    - "Ahrefs alternative"
    - "Ahrefs keyword explorer alternative"
    - "Semrush keyword magic tool"
    - "Google Keyword Planner alternative"
    - "Ubersuggest alternative"
    - "关键词研究"
    - "关键词分析"
    - "长尾关键词"
    - "写什么内容好"
    - "帮我挖词"
    - "内容机会"
    - "搜什么词"
    - "选题规划"
    - "キーワード調査"
    - "検索ボリューム"
    - "키워드 리서치"
    - "검색량 분석"
    - "investigación de palabras clave"
    - "volumen de búsqueda"
    - "pesquisa de palavras-chave"
    - "volume de busca"
---

# Keyword Research

Discovers, scores, and clusters keywords for SEO and GEO planning.

## Quick Start

```
Research keywords for [topic/product/service]
```

```
What keywords is [competitor URL] ranking for that I should target?
```

## Skill Contract

**Expected output**: a prioritized keyword brief plus the standard handoff summary for `memory/research/`.

- **Reads**: goals, market inputs, tool data, and prior strategy from [CLAUDE.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/CLAUDE.md) and the shared [State Model](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/state-model.md) when available.
- **Writes**: a user-facing research deliverable and reusable summary.
- **Promotes**: durable keyword priorities, competitor facts, and strategy decisions to `memory/hot-cache.md`, `memory/decisions.md`, and `memory/research/`.
- **Primary next skill**: [competitor-analysis](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/research/competitor-analysis/SKILL.md) when the keyword set is ready for market comparison.

### Handoff Summary

> Emit the standard shape from [skill-contract.md §Handoff Summary Format](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/skill-contract.md).

## Data Sources

Optional integrations: ~~SEO tool, ~~search console. Without tools, ask for seed keywords, audience, goals, and any known metrics. See [CONNECTORS.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/CONNECTORS.md).

## Instructions

When a user requests keyword research, run eight phases and announce each as `[Phase X/8: Name]`:

1. **Scope** — clarify product, audience, business goal, DR, geography, and language.
2. **Discover** — seed from core, problem, solution, audience, and industry terms.
3. **Variations** — expand with modifiers and long-tail patterns.
4. **Classify** — tag by intent (informational, navigational, commercial, transactional).
5. **Score** — assign difficulty (1-100) and compute `Opportunity = (Volume × Intent Value) / Difficulty`, with Intent Value `1 / 1 / 2 / 3`.
6. **GEO-Check** — flag AI-answer-friendly queries such as questions, definitions, comparisons, lists, and how-tos.
7. **Cluster** — group keywords into pillar + cluster topic hubs.
8. **Deliver** — output an Executive Summary, Quick Wins / Growth / GEO opportunities, Topic Clusters, Content Calendar, and Next Steps.

**Quality bar**: every recommendation includes at least one specific number. Rewrite generic advice into a concrete keyword + volume + difficulty + reason.

> **Reference**: See [references/instructions-detail.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/research/keyword-research/references/instructions-detail.md) for the full 8-phase templates, expansion patterns, intent table, difficulty tiers, opportunity matrix, GEO indicators, cluster template, actionable-vs-generic examples, and advanced usage.

## Example

Example outcome: 150+ keywords analyzed, 23 high-priority opportunities, ~45K/month traffic potential across 3 focus areas. See the full sample in [references/example-report.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/research/keyword-research/references/example-report.md).

### Advanced Usage

Intent mapping, seasonal analysis, competitor gaps, and local keyword workflows live in [references/instructions-detail.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/research/keyword-research/references/instructions-detail.md#advanced-usage).

## Tips for Success

Start with seeds, respect intent, cluster tightly, prioritize quick wins, and review quarterly. Full notes live in [references/instructions-detail.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/research/keyword-research/references/instructions-detail.md#tips-for-success).

### Save Results

After delivering, offer to save `memory/research/keyword-research/YYYY-MM-DD-<topic>.md` and promote durable conclusions to `memory/hot-cache.md`.

## Reference Materials

- [Instructions Detail](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/research/keyword-research/references/instructions-detail.md) — Workflow, scoring, cluster template, advanced usage
- [Keyword Intent Taxonomy](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/research/keyword-research/references/keyword-intent-taxonomy.md) — Intent signals and content mapping
- [Topic Cluster Templates](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/research/keyword-research/references/topic-cluster-templates.md) — Pillar and cluster patterns
- [Keyword Prioritization Framework](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/research/keyword-research/references/keyword-prioritization-framework.md) — Scoring and prioritization rules
- [Example Report](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/research/keyword-research/references/example-report.md) — Worked sample

## Next Best Skill

Primary: [competitor-analysis](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/research/competitor-analysis/SKILL.md). Also: [content-gap-analysis](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/research/content-gap-analysis/SKILL.md) and [serp-analysis](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/research/serp-analysis/SKILL.md).
