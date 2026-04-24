---
name: internal-linking-optimizer
description: 'Optimize internal links: site architecture, authority distribution, orphan pages, crawl depth analysis. 内链优化/站内架构'
version: "9.1.0"
license: Apache-2.0
compatibility: "Claude Code, skills.sh, ClawHub, Vercel Labs, Cursor, Windsurf, Codex CLI, Amp, Gemini CLI, Kimi Code, Qwen Code, CodeBuddy"
homepage: "https://github.com/aaron-he-zhu/seo-geo-claude-skills"
when_to_use: "Use when improving internal link structure, anchor text distribution, orphan pages, or site architecture."
argument-hint: "<URL or sitemap>"
metadata:
  author: aaron-he-zhu
  version: "9.1.0"
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


This skill analyzes your site's internal link structure and provides recommendations to improve SEO through strategic internal linking. It helps distribute authority, establish topical relevance, and improve crawlability.

## What This Skill Does

Analyzes internal link structure, authority flow, orphan pages, anchor text, and topic clusters, then delivers a prioritized linking plan with specific source/target/anchor recommendations.

## Quick Start

Start with one of these prompts. Finish with a short handoff summary using the repository format in [Skill Contract](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/skill-contract.md).

### Analyze Current Structure

```
Analyze internal linking structure for [domain/sitemap]
```

```
Find internal linking opportunities for [URL]
```

### Create Linking Strategy

```
Create internal linking plan for topic cluster about [topic]
```

```
Suggest internal links for this new article: [content/URL]
```

### Fix Issues

```
Find orphan pages on [domain]
```

```
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

1. **Analyze Current Internal Link Structure**

   ```markdown
   ## Internal Link Structure Analysis
   
   ### Overview
   
   **Domain**: [domain]
   **Total Pages Analyzed**: [X]
   **Total Internal Links**: [X]
   **Average Links per Page**: [X]
   
   ### Link Distribution
   
   | Links per Page | Page Count | Percentage |
   |----------------|------------|------------|
   | 0 (Orphan) | [X] | [X]% |
   | 1-5 | [X] | [X]% |
   | 6-10 | [X] | [X]% |
   | 11-20 | [X] | [X]% |
   | 20+ | [X] | [X]% |
   
   ### Top Linked Pages
   
   | Page | Internal Links | Authority | Notes |
   |------|----------------|-----------|-------|
   | [URL 1] | [X] | High | [notes] |
   | [URL 2] | [X] | High | [notes] |
   | [URL 3] | [X] | Medium | [notes] |
   
   ### Under-Linked Important Pages
   
   | Page | Current Links | Traffic | Recommended Links |
   |------|---------------|---------|-------------------|
   | [URL 1] | [X] | [X]/mo | [X]+ |
   | [URL 2] | [X] | [X]/mo | [X]+ |
   
   **Structure Score**: [X]/10
   ```

2. **Identify Orphan Pages**

   ```markdown
   ## Orphan Page Analysis
   
   ### Definition
   Orphan pages have no internal links pointing to them, making them 
   hard for users and search engines to discover.
   
   ### Orphan Pages Found: [X]
   
   | Page | Traffic | Priority | Recommended Action |
   |------|---------|----------|-------------------|
   | [URL 1] | [X]/mo | High | Link from [pages] |
   | [URL 2] | [X]/mo | Medium | Add to navigation |
   | [URL 3] | 0 | Low | Consider deleting/redirecting |
   
   ### Fix Strategy
   
   **High Priority Orphans** (have traffic/rankings):
   1. [URL] - Add links from: [relevant pages]
   2. [URL] - Add links from: [relevant pages]
   
   **Medium Priority Orphans** (potentially valuable):
   1. [URL] - Add to category/tag page
   2. [URL] - Link from related content
   
   **Low Priority Orphans** (consider removing):
   1. [URL] - Redirect to [better page]
   2. [URL] - Delete or noindex
   ```

3. **Analyze Anchor Text Distribution** — Current anchor patterns, distribution-by-page breakdown, over-optimization/generic flag, per-page recommendations (CORE-EEAT R08)

   > **Reference**: See [references/linking-templates.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/optimize/internal-linking-optimizer/references/linking-templates.md) for the anchor text analysis template (Step 3) including the CORE-EEAT R08 alignment note.

4. **Create Topic Cluster Link Strategy** — Map current pillar/cluster links, recommend link structure, list specific links to add

   > **Reference**: See [references/linking-templates.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/optimize/internal-linking-optimizer/references/linking-templates.md) for the topic cluster link strategy template (Step 4).

5. **Find Contextual Link Opportunities** — Analyze each page for topic-relevant link opportunities, prioritize high-impact additions

   > **Reference**: See [references/linking-templates.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/optimize/internal-linking-optimizer/references/linking-templates.md) for the contextual link opportunities template (Step 5).

6. **Optimize Navigation and Footer Links** — Analyze main/footer/sidebar/breadcrumb navigation, recommend pages to add or remove

   > **Reference**: See [references/linking-templates.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/optimize/internal-linking-optimizer/references/linking-templates.md) for the navigation optimization template (Step 6).

7. **Generate Link Implementation Plan** — Executive summary, current state metrics, phased priority actions (weeks 1-4+), implementation guide, tracking plan

   > **Reference**: See [references/linking-templates.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/optimize/internal-linking-optimizer/references/linking-templates.md) for the full implementation plan template (Step 7).


## Example

**User**: "Find internal linking opportunities for my blog post on 'email marketing best practices'"

**Output** (abbreviated): 5 high-value links identified — `/blog/grow-email-list/` for "building your email list" (para 2), `/blog/email-subject-lines/` for "subject lines" (para 5), `/blog/email-segmentation-guide/` for "audience segments", `/services/email-automation/` for CTA section, `/blog/best-email-tools/` for conclusion — each with paragraph location and recommended anchor text.

> **Reference**: See [references/linking-example.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/optimize/internal-linking-optimizer/references/linking-example.md) for the full worked example (email marketing best practices internal linking opportunities).

## Tips for Success

1. **Quality over quantity** - Add relevant links, not random ones
2. **User-first thinking** - Links should help users navigate
3. **Vary anchor text** - Avoid over-optimization
4. **Link to important pages** - Distribute authority strategically
5. **Regular audits** - Internal links need maintenance as content grows


### Save Results

Ask to save results; if yes, write a dated summary to `memory/audits/internal-linking-optimizer/YYYY-MM-DD-<topic>.md`. Append veto-level issues to `memory/hot-cache.md` automatically.

## Reference Materials

- [Link Architecture Patterns](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/optimize/internal-linking-optimizer/references/link-architecture-patterns.md) — Architecture models (hub-and-spoke, silo, flat, pyramid, mesh), anchor text diversity framework, link equity flow model, and internal link audit checklist
- [Linking Templates](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/optimize/internal-linking-optimizer/references/linking-templates.md) — Detailed output templates for steps 3-7 (anchor text analysis, topic cluster strategy, contextual opportunities, navigation optimization, implementation plan)
- [Linking Example](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/optimize/internal-linking-optimizer/references/linking-example.md) — Full worked example for internal linking opportunities

## Next Best Skill

Primary: [on-page-seo-auditor](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/optimize/on-page-seo-auditor/SKILL.md) -- verify that revised internal links support the page-level goals.
