---
name: internal-linking-optimizer
description: 'Use when improving internal link structure, anchor text, orphan pages, crawl depth, site architecture, or link equity flow. 内链优化/站内架构'
version: "9.9.5"
license: Apache-2.0
compatibility: "Claude Code, skills.sh, ClawHub, Vercel Labs, Cursor, Windsurf, Codex CLI, Amp, Gemini CLI, Kimi Code, Qwen Code, CodeBuddy"
homepage: "https://github.com/aaron-he-zhu/seo-geo-claude-skills"
when_to_use: "Use when improving internal link structure, anchor text distribution, orphan pages, or site architecture."
argument-hint: "<URL or sitemap>"
metadata:
  author: aaron-he-zhu
  version: "9.9.5"
  geo-relevance: "low"
  tags:
    - seo
    - internal-linking
    - site-architecture
    - link-equity
    - orphan-pages
    - topical-authority
    - crawl-depth
    - 内链优化
    - 内部リンク
    - 내부링크
    - enlaces-internos
  triggers:
    # EN-formal
    - "fix internal links"
    - "improve site architecture"
    - "internal linking strategy"
    - "link equity"
    # EN-casual
    - "orphan pages"
    - "site architecture is messy"
    - "pages have no links"
    # EN-question
    - "how to improve internal linking"
    - "how to fix orphan pages"
    # ZH-pro
    - "内链优化"
    - "站内链接"
    - "网站架构"
    - "权重传递"
    - "锚文本优化"
    # ZH-casual
    - "内链怎么做"
    - "孤立页面"
    - "网站结构乱"
    # JA
    - "内部リンク最適化"
    - "サイト構造"
    - "サイト構造改善"
    - "孤立ページ"
    - "内部リンク戦略"
    - "アンカーテキスト最適化"
    # KO
    - "내부 링크 최적화"
    - "사이트 구조"
    - "사이트 구조 개선"
    - "고아 페이지"
    - "앵커 텍스트"
    # ES
    - "enlaces internos"
    - "arquitectura del sitio"
    - "páginas huérfanas"
    - "estructura del sitio"
    # PT
    - "links internos"
    - "arquitetura do site"
    - "páginas órfãs"
---

# Internal Linking Optimizer

Analyzes internal link structure, authority flow, orphan pages, anchor text, and topic clusters, then delivers a prioritized linking plan with source/target/anchor recommendations.

## Quick Start

Start with one of these prompts, then finish with the standard handoff summary from [Skill Contract](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/skill-contract.md).

```text
Analyze internal linking structure for [domain/sitemap]
Find internal linking opportunities for [URL]
Create internal linking plan for topic cluster about [topic]
Suggest internal links for this new article: [content/URL]
Find orphan pages on [domain]
Optimize anchor text across the site
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

Uses ~~web crawler and ~~analytics when connected; otherwise asks user for sitemap, key page URLs, and content categories. See [CONNECTORS.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/CONNECTORS.md) and [SECURITY.md §Scraping Boundaries](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/SECURITY.md).

## Instructions

When a user requests internal linking optimization:

1. **Analyze Current Structure** -- Capture domain, pages analyzed, total internal links, average links/page, link distribution, top linked pages, under-linked important pages, and a structure score. Flag crawl-depth and authority-flow problems.
2. **Identify Orphan Pages** -- List pages with no inbound internal links. Prioritize high-value orphans with traffic/rankings, medium-potential pages that need category/tag links, and low-value pages to delete, noindex, or redirect.
3. **Analyze Anchor Text Distribution** -- Check current anchor patterns, distribution by page, over-optimization, generic anchors, and CORE-EEAT R08 alignment.
   > **Reference**: [references/linking-templates.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/optimize/internal-linking-optimizer/references/linking-templates.md) contains the Step 3 output template.
4. **Create Topic Cluster Link Strategy** -- Map pillar/cluster links, recommend structure, and list specific links to add.
   > **Reference**: [references/linking-templates.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/optimize/internal-linking-optimizer/references/linking-templates.md) contains the Step 4 template.
5. **Find Contextual Link Opportunities** -- For each page, identify topic-relevant source/target/anchor opportunities and prioritize high-impact additions.
   > **Reference**: [references/linking-templates.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/optimize/internal-linking-optimizer/references/linking-templates.md) contains the Step 5 template.
6. **Optimize Navigation and Footer Links** -- Review main/footer/sidebar/breadcrumb navigation; recommend pages to add, demote, or remove.
   > **Reference**: [references/linking-templates.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/optimize/internal-linking-optimizer/references/linking-templates.md) contains the Step 6 template.
7. **Generate Implementation Plan** -- Include executive summary, current-state metrics, phased priority actions, implementation guide, and tracking plan.
   > **Reference**: [references/linking-templates.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/optimize/internal-linking-optimizer/references/linking-templates.md) contains the Step 7 template.

## Example

**User**: "Find internal linking opportunities for my blog post on 'email marketing best practices'"

**Output**: 5 high-value links with source paragraph, destination URL, recommended anchor text, and priority. Example targets might include list-building, subject-line, segmentation, automation, and tools pages.

> **Reference**: See [references/linking-example.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/optimize/internal-linking-optimizer/references/linking-example.md) for the full worked example.

## Tips for Success

- Prioritize relevance and user navigation over link volume.
- Use descriptive, varied anchors; avoid exact-match repetition.
- Link important pages from hubs, navigation, or strong contextual sources.
- Audit regularly as content grows.

### Save Results

Ask to save results; if yes, write a dated summary to `memory/audits/internal-linking-optimizer/YYYY-MM-DD-<topic>.md`. Append veto-level issues to `memory/hot-cache.md` automatically.

## Reference Materials

- [Link Architecture Patterns](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/optimize/internal-linking-optimizer/references/link-architecture-patterns.md) -- Architecture models, selection thresholds, migration safeguards, and measurement targets
- [Linking Templates](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/optimize/internal-linking-optimizer/references/linking-templates.md) -- Detailed output templates for steps 3-7
- [Linking Example](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/optimize/internal-linking-optimizer/references/linking-example.md) -- Full worked example for internal linking opportunities

## Next Best Skill

Primary: [on-page-seo-auditor](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/optimize/on-page-seo-auditor/SKILL.md) -- verify that revised internal links support page-level goals.
