---
name: keyword-research
description: 'Find high-value SEO keywords: search volume, difficulty, intent classification, topic clusters. 关键词研究/内容选题'
version: "9.1.0"
license: Apache-2.0
compatibility: "Claude Code, skills.sh, ClawHub, Vercel Labs, Cursor, Windsurf, Codex CLI, Amp, Gemini CLI, Kimi Code, Qwen Code, CodeBuddy"
homepage: "https://github.com/aaron-he-zhu/seo-geo-claude-skills"
when_to_use: "Use when starting keyword research for a new page, topic, or campaign. Also when the user asks about search volume, keyword difficulty, topic clusters, long-tail keywords, or what to write about."
argument-hint: "<topic or seed keyword> [market/language]"
metadata:
  author: aaron-he-zhu
  version: "9.1.0"
  geo-relevance: "medium"
  tags:
    - seo
    - geo
    - keywords
    - keyword-research
    - search-volume
    - keyword-difficulty
    - topic-clusters
    - long-tail-keywords
    - search-intent
    - content-calendar
    - ahrefs
    - semrush
    - google-keyword-planner
    - 关键词研究
    - SEO关键词
    - キーワード調査
    - 키워드분석
    - palabras-clave
  triggers:
    # EN-formal
    - "keyword research"
    - "find keywords"
    - "keyword analysis"
    - "search volume analysis"
    - "keyword difficulty"
    - "topic research"
    - "identify ranking opportunities"
    # EN-casual
    - "what should I write about"
    - "what are people searching for"
    - "give me keyword ideas"
    - "which keywords should I target"
    - "why is my traffic low"
    - "I need content ideas"
    # EN-question
    - "how do I find good keywords"
    - "how competitive is this keyword"
    # EN-competitor
    - "Ahrefs keyword explorer alternative"
    - "Semrush keyword magic tool"
    - "Google Keyword Planner alternative"
    - "Ubersuggest alternative"
    # ZH-pro
    - "关键词研究"
    - "关键词分析"
    - "搜索量查询"
    - "关键词难度"
    - "SEO关键词"
    - "长尾关键词"
    - "词库整理"
    - "关键词布局"
    - "关键词挖掘"
    # ZH-casual
    - "写什么内容好"
    - "找选题"
    - "帮我挖词"
    - "不知道写什么"
    - "查关键词"
    - "选词"
    - "帮我找词"
    # JA
    - "キーワード調査"
    - "キーワードリサーチ"
    - "SEOキーワード分析"
    - "検索ボリューム"
    - "ロングテールキーワード"
    - "検索意図分析"
    # KO
    - "키워드 리서치"
    - "키워드 분석"
    - "검색량 분석"
    - "키워드 어떻게 찾아요?"
    - "검색어 분석"
    - "경쟁도 낮은 키워드는?"
    # ES
    - "investigación de palabras clave"
    - "análisis de palabras clave"
    - "volumen de búsqueda"
    - "posicionamiento web"
    - "cómo encontrar palabras clave"
    # PT
    - "pesquisa de palavras-chave"
---

# Keyword Research


Discovers, analyzes, and prioritizes keywords for SEO and GEO content strategies. Turns market signals into reusable strategic inputs (volume, difficulty, intent, clusters, GEO relevance).

## Quick Start

Start with one of these prompts. Finish with a short handoff summary using the repository format in [Skill Contract](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/skill-contract.md).

### Basic Keyword Research

```
Research keywords for [topic/product/service]
```

```
Find keyword opportunities for a [industry] business targeting [audience]
```

### With Specific Goals

```
Find low-competition keywords for [topic] with commercial intent
```

```
Identify question-based keywords for [topic] that AI systems might answer
```

### Competitive Research

```
What keywords is [competitor URL] ranking for that I should target?
```

## Skill Contract

**Expected output**: a prioritized research brief, evidence-backed findings, and a short handoff summary ready for `memory/research/`.

- **Reads**: user goals, target market inputs, available tool data, and prior strategy from [CLAUDE.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/CLAUDE.md) and the shared [State Model](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/state-model.md) when available.
- **Writes**: a user-facing research deliverable plus a reusable summary that can be stored under `memory/research/`.
- **Promotes**: durable keyword priorities, competitor facts, entity candidates, and strategic decisions to `memory/hot-cache.md`, `memory/decisions.md`, and `memory/research/`; hand canonical entity work to `entity-optimizer`.
- **Next handoff**: use the `Next Best Skill` below when the findings are ready to drive action.

### Handoff Summary

> Emit the standard shape from [skill-contract.md §Handoff Summary Format](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/skill-contract.md).

## Data Sources

Optional integrations: ~~SEO tool, ~~search console. Without tools, users provide seed keywords, audience, goals, and any known metrics manually. See [CONNECTORS.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/CONNECTORS.md).

## Instructions

When a user requests keyword research, run eight phases (announce each as `[Phase X/8: Name]`):

1. **Scope** — clarify product, audience, business goal, DR, geography, language
2. **Discover** — seed from core/problem/solution/audience/industry terms
3. **Variations** — expand with modifier and long-tail patterns
4. **Classify** — tag each by intent (informational/navigational/commercial/transactional)
5. **Score** — assign difficulty (1-100) and compute `Opportunity = (Volume × Intent Value) / Difficulty` with Intent Value 1/1/2/3
6. **GEO-Check** — flag AI-answer-friendly queries (questions, definitions, comparisons, lists, how-tos)
7. **Cluster** — group keywords into pillar + cluster topic hubs
8. **Deliver** — Executive Summary, Quick Wins / Growth / GEO opportunities, Topic Clusters, Content Calendar, Next Steps

**Quality bar** — every recommendation must include at least one specific number. Generic advice like "target long-tail keywords for better results" must be rewritten as "Target 'project management for nonprofits' (vol: 320, KD: 22) — no DR>40 sites in top 10" before including.

> **Reference**: See [references/instructions-detail.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/research/keyword-research/references/instructions-detail.md) for the full 8-phase templates, expansion patterns, intent classification table, difficulty tiers, opportunity matrix, GEO indicators, cluster template, deliverable quality bar with actionable vs. generic examples, and tips.

## Example

**User**: "Research keywords for a project management software company targeting small businesses"

**Output** (abbreviated): 150+ keywords analyzed, 23 high-priority opportunities with ~45K/month traffic potential across 3 focus areas (task management workflows, team collaboration, small business productivity). Quick Wins prioritized by KD × volume × intent fit.

> **Reference**: See [references/example-report.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/research/keyword-research/references/example-report.md) for the full report for "project management software for small businesses".

### Advanced Usage

Intent Mapping, Seasonal Analysis, Competitor Gap, Local Keywords — see [references/instructions-detail.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/research/keyword-research/references/instructions-detail.md#advanced-usage).

## Tips for Success

Start with seeds; don't ignore long-tail; match intent; cluster for topical authority; prioritize quick wins; include GEO keywords; review quarterly. See [references/instructions-detail.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/research/keyword-research/references/instructions-detail.md#tips-for-success).


### Save Results

After delivering, offer to save a dated summary to `memory/research/keyword-research/YYYY-MM-DD-<topic>.md`. Promote key conclusions to `memory/hot-cache.md` if they influence ongoing strategy.

## Reference Materials

- [Instructions Detail](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/research/keyword-research/references/instructions-detail.md) — Full 8-phase workflow, expansion patterns, scoring, cluster templates, advanced usage, tips
- [Keyword Intent Taxonomy](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/research/keyword-research/references/keyword-intent-taxonomy.md) — Complete intent classification with signal words and content strategies
- [Topic Cluster Templates](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/research/keyword-research/references/topic-cluster-templates.md) — Hub-and-spoke architecture templates for pillar and cluster content
- [Keyword Prioritization Framework](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/research/keyword-research/references/keyword-prioritization-framework.md) — Priority scoring matrix, categories, and seasonal keyword patterns
- [Example Report](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/research/keyword-research/references/example-report.md) — Complete example keyword research report for project management software

## Next Best Skill

Primary: [competitor-analysis](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/research/competitor-analysis/SKILL.md). Also: [content-gap-analysis](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/research/content-gap-analysis/SKILL.md), [serp-analysis](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/research/serp-analysis/SKILL.md).
