---
name: content-gap-analysis
description: 'Find content gaps: topics and keywords competitors cover that you don''t, with editorial calendar. 内容缺口/选题规划'
version: "9.1.0"
license: Apache-2.0
compatibility: "Claude Code, skills.sh, ClawHub, Vercel Labs, Cursor, Windsurf, Codex CLI, Amp, Gemini CLI, Kimi Code, Qwen Code, CodeBuddy"
homepage: "https://github.com/aaron-he-zhu/seo-geo-claude-skills"
when_to_use: "Use when finding content gaps between two domains, discovering missing topics, or identifying coverage holes versus competitors."
argument-hint: "<your domain> <competitor domain>"
metadata:
  author: aaron-he-zhu
  version: "9.1.0"
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
    # EN-formal
    - "find content gaps"
    - "content opportunities"
    - "topic analysis"
    - "editorial calendar"
    # EN-casual
    - "what am I missing"
    - "what do competitors write about"
    - "what should I cover next"
    - "they cover this but I don't"
    # EN-question
    - "what topics am I missing"
    - "what content should I create"
    # ZH-pro
    - "内容缺口分析"
    - "选题规划"
    - "内容机会"
    - "竞品话题"
    # ZH-casual
    - "缺什么内容"
    - "竞品写了什么"
    - "还应该写什么"
    # JA
    - "コンテンツギャップ"
    - "コンテンツ機会"
    # KO
    - "콘텐츠 갭 분석"
    - "콘텐츠 기회"
    # ES
    - "brechas de contenido"
    - "oportunidades de contenido"
    # PT
    - "lacunas de conteúdo"
---

# Content Gap Analysis


Identifies content opportunities by comparing your site against competitors -- surfacing missing keywords, untapped topics, format gaps, and GEO-ready content worth creating.

## What This Skill Does

Finds keyword, topic, and format gaps between your site and competitors, scores them by impact and effort, and produces a prioritized content calendar to close the highest-value gaps.

## Quick Start

Start with one of these prompts. Finish with a short handoff summary using the repository format in [Skill Contract](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/skill-contract.md).

### Basic Gap Analysis

```
Find content gaps between my site [URL] and [competitor URLs]
```

```
What content am I missing compared to my top 3 competitors?
```

### Topic-Specific Analysis

```
Find content gaps in [topic area] compared to industry leaders
```

```
What [content type] do competitors have that I don't?
```

### Audience-Focused

```
What content gaps exist for [audience segment] in my niche?
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

Optional integrations: ~~SEO tool, ~~search console, ~~analytics, ~~AI monitor. Without tools, users provide site URL, content inventory, competitor URLs, and business goals manually. See [CONNECTORS.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/CONNECTORS.md).

## Instructions

When a user requests content gap analysis:

1. **Define Analysis Scope**

   Clarify parameters:
   
   ```markdown
   ### Analysis Parameters
   
   **Your Site**: [URL]
   **Competitors to Analyze**: [URLs or "identify for me"]
   **Topic Focus**: [specific area or "all"]
   **Content Types**: [blogs, guides, tools, videos, or "all"]
   **Audience**: [target audience]
   **Business Goals**: [traffic, leads, authority, etc.]
   ```

2. **Audit Your Existing Content**

   Document total indexed pages, content by type and topic cluster, top performing content, and content strengths/weaknesses.

3. **Analyze Competitor Content**

   For each competitor: document content volume, monthly traffic, content distribution by type, topic coverage vs. yours, and unique content they have.

4. **Identify Keyword Gaps**

   Find keywords competitors rank for that you do not. Categorize into High Priority (high volume, achievable difficulty), Quick Wins (lower volume, low difficulty), and Long-term (high volume, high difficulty). Include keyword overlap analysis.

5. **Map Topic Gaps**

   Create a topic coverage comparison matrix across all competitors. For each missing topic cluster, document business relevance, competitor coverage, opportunity size, sub-topics, and recommended pillar/cluster approach.

6. **Identify Content Format Gaps**

   Compare format distribution (guides, tutorials, comparisons, case studies, tools, templates, video, infographics, research) against competitors and industry averages. For each gap, assess effort and expected impact.

7. **Analyze GEO/AI Gaps**

   Identify topics where competitors get AI citations but you do not. Document missing Q&A content, definition/explanation content, and comparison content. Score each by traditional SEO value and GEO value.

8. **Map to Audience Journey**

   Compare funnel stage coverage (Awareness, Consideration, Decision, Retention) against competitor averages. Detail specific gaps at each stage.

9. **Prioritize and Create Action Plan**

   Produce a final report with: Executive Summary, Prioritized Gap List (Tier 1 Quick Wins, Tier 2 Strategic Builds, Tier 3 Long-term), Content Calendar, and Success Metrics.

   > **Reference**: See [references/analysis-templates.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/research/content-gap-analysis/references/analysis-templates.md) for detailed templates for each step.

## Example

> **Reference**: See [references/example-report.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/research/content-gap-analysis/references/example-report.md) for a complete example analyzing SaaS marketing blog gaps vs. HubSpot and Drift.

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

1. **Focus on actionable gaps** - Not all gaps are worth filling
2. **Consider your resources** - Prioritize based on ability to execute
3. **Quality over quantity** - Better to fill 5 gaps well than 20 poorly
4. **Track what works** - Measure gap-filling success
5. **Update regularly** - Gaps change as competitors publish
6. **Include GEO opportunities** - Don't just optimize for traditional search



### Save Results

After delivering, offer to save a dated summary to `memory/research/content-gap-analysis/YYYY-MM-DD-<topic>.md`. Promote key conclusions to `memory/hot-cache.md` if they influence ongoing strategy.

## Reference Materials

- [Analysis Templates](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/research/content-gap-analysis/references/analysis-templates.md) — Detailed templates for each analysis step (inventory, competitor content, keyword gaps, topic gaps, format gaps, GEO gaps, journey, prioritized report)
- [Gap Analysis Frameworks](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/research/content-gap-analysis/references/gap-analysis-frameworks.md) — Content audit matrices, funnel mapping, and gap prioritization scoring methodologies
- [Example Report](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/research/content-gap-analysis/references/example-report.md) — Complete example analyzing SaaS marketing blog gaps vs. HubSpot and Drift

## Next Best Skill

Primary: [seo-content-writer](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/build/seo-content-writer/SKILL.md).
