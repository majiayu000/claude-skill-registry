---
name: seo-content-writer
description: 'Write SEO blog posts, articles, landing pages with keyword integration, header optimization, and snippet targeting. SEO文章写作/内容优化'
version: "9.1.0"
license: Apache-2.0
compatibility: "Claude Code, skills.sh, ClawHub, Vercel Labs, Cursor, Windsurf, Codex CLI, Amp, Gemini CLI, Kimi Code, Qwen Code, CodeBuddy"
homepage: "https://github.com/aaron-he-zhu/seo-geo-claude-skills"
when_to_use: "Use when writing SEO-optimized articles, blog posts, landing pages, or product descriptions. Also when the user asks to create content targeting a specific keyword."
argument-hint: "<topic> <target keyword>"
metadata:
  author: aaron-he-zhu
  version: "9.1.0"
  geo-relevance: "medium"
  tags:
    - seo
    - content-writing
    - blog-writing
    - seo-copywriting
    - content-creation
    - featured-snippet-optimization
    - article-writing
    - landing-page
    - surferSEO-alternative
    - clearscope-alternative
    - SEO文章
    - 博客写作
    - SEOライティング
    - SEO글쓰기
    - redaccion-seo
  triggers:
    # EN-formal
    - "write SEO content"
    - "create blog post"
    - "write an article"
    - "content writing"
    - "write for SEO"
    - "SEO copywriting"
    # EN-casual
    - "write me a blog post"
    - "help me write about"
    - "I need a blog post"
    - "create content for my site"
    # EN-question
    - "how do I write content that ranks"
    - "how to write SEO friendly content"
    # EN-competitor
    - "SurferSEO alternative"
    - "Clearscope alternative"
    - "Jasper AI alternative for SEO"
    # ZH-pro
    - "SEO文章写作"
    - "SEO内容创作"
    - "博客写作"
    - "内容优化"
    - "内容创作"
    # ZH-casual
    - "帮我写文章"
    - "写一篇博客"
    - "排名上不去"
    - "帮我写SEO文章"
    - "写一篇SEO文章"
    # JA
    - "SEOライティング"
    - "SEO記事作成"
    - "ブログ記事作成"
    - "SEOコンテンツ"
    # KO
    - "SEO 글쓰기"
    - "블로그 작성"
    - "SEO 콘텐츠 작성"
    - "블로그 글 작성해줘"
    - "이 주제로 글 써봐"
    # ES
    - "redacción SEO"
    - "escribir artículo SEO"
    - "contenido optimizado"
    # PT
    - "redação SEO"
    - "escrever artigo SEO"
---

# SEO Content Writer

This skill creates search-engine-optimized content that ranks well while providing genuine value to readers. It applies proven SEO copywriting techniques, proper keyword integration, and optimal content structure.

## What This Skill Does

Produces keyword-integrated, well-structured content with optimized titles, headers, internal links, and featured-snippet formatting that ranks and reads well.

## Quick Start

Start with one of these prompts. Finish with a short handoff summary using the repository format in [Skill Contract](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/skill-contract.md).

### Basic Content Creation

```
Write an SEO-optimized article about [topic] targeting the keyword [keyword]
```

```
Create a blog post for [topic] with these keywords: [keyword list]
```

### With Specific Requirements

```
Write a 2,000-word guide about [topic] targeting [keyword],
include FAQ section for featured snippets
```

### Content Briefs

```
Here's my content brief: [brief]. Write SEO-optimized content following this outline.
```

## Skill Contract

**Expected output**: a ready-to-use asset or implementation-ready transformation plus a short handoff summary ready for `memory/content/`.

- **Reads**: the brief, target keywords, entity inputs, quality constraints, and prior decisions from [CLAUDE.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/CLAUDE.md) and the shared [State Model](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/state-model.md) when available.
- **Writes**: a user-facing content, metadata, or schema deliverable plus a reusable summary that can be stored under `memory/content/`.
- **Promotes**: approved angles, messaging choices, missing evidence, and publish blockers to `memory/hot-cache.md`, `memory/decisions.md`, and `memory/open-loops.md`.
- **Next handoff**: use the `Next Best Skill` below when the asset is ready for review or deployment.

### Handoff Summary

> Emit the standard shape from [skill-contract.md §Handoff Summary Format](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/skill-contract.md).

## Data Sources

Optional SEO tool and search console integrations pull keyword metrics and competitor data automatically; otherwise ask the user for keywords, intent, and competitors. See [CONNECTORS.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/CONNECTORS.md) for integration placeholders.

## Instructions

When a user requests SEO content, run these nine steps in order:

1. **Gather Requirements** — primary/secondary keywords, word count, content type, audience, search intent, tone, CTA goal, competitor URLs
2. **Load CORE-EEAT Quality Constraints** — 16 high-weight items (C01, C02, C06, C10, O01, O02, O06, O09, R01, R02, R04, R07, C03, O08, O10, E07)
3. **Research and Plan** — SERP analysis, keyword map (primary/secondary/LSI/questions), content angle
4. **Create Optimized Title** — ≤60 chars, primary keyword front-loaded, power words
5. **Write Meta Description** — 150-160 chars, primary keyword, CTA
6. **Structure Content and Write** — H1 > intro (hook + promise + keyword in first 100 words) > H2 sections > H3 sub-topics > FAQ > conclusion
7. **Apply On-Page SEO Best Practices** — keyword placement, readability, internal/external links, FAQ section with 40-60 word answers, featured snippet formats
8. **Add Internal/External Links** — 2-5 internal, 2-3 authoritative external
9. **Final SEO Review and CORE-EEAT Self-Check** — Score against 10 SEO factors and verify 16 CORE-EEAT constraints; classify issues (auto-correct vs. needs-decision)

> **Reference**: See [references/instructions-detail.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/build/seo-content-writer/references/instructions-detail.md) for the full step-by-step templates, CORE-EEAT constraint table, issue classification rules, and Changes Made block format.

## Example

**User**: "Write an SEO-optimized article about 'email marketing best practices' targeting small businesses"

**Output** (abbreviated):
- H1: `Email Marketing Best Practices: A 2026 Guide for Small Businesses` (keyword front-loaded; audience + year qualifier)
- Meta description: `Get 12 proven email marketing tactics that lift open rates 34% for small businesses. DMA-backed data, real subject-line examples, and a 30-day playbook.` (~156 chars, CTA implied, stat hook)
- Structure: H2 for each of 12 tactics, bullet lists, comparison table (Mailchimp vs Brevo vs ConvertKit), 6-question FAQ (40-60 word answers for featured snippets), CTA conclusion.

> **Reference**: See [references/seo-writing-checklist.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/build/seo-content-writer/references/seo-writing-checklist.md) for the full article with statistics citations, H1/H2/H3 hierarchy, and FAQ section.

## Content Type Templates

Quick-start prompts: How-to guide, Comparison article, Listicle, Ultimate guide. See [references/instructions-detail.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/build/seo-content-writer/references/instructions-detail.md#content-type-templates) for all 4 templates.

## Tips for Success

Match intent, front-load value, use data, write for humans first, include visuals, update regularly. Full list in [references/instructions-detail.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/build/seo-content-writer/references/instructions-detail.md#tips-for-success).


### Save Results

On user confirmation, save a dated summary to `memory/content/YYYY-MM-DD-<topic>.md` and promote key conclusions to `memory/hot-cache.md`.

## Reference Materials

- [Instructions Detail](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/build/seo-content-writer/references/instructions-detail.md) - Full step-by-step workflow, CORE-EEAT constraints, issue classification, content type templates, tips
- [SEO Writing Checklist](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/build/seo-content-writer/references/seo-writing-checklist.md) - On-page SEO checklist, writing template, featured snippet patterns, full example
- [Title Formulas](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/build/seo-content-writer/references/title-formulas.md) - Proven headline formulas, power words, CTR patterns
- [Content Structure Templates](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/build/seo-content-writer/references/content-structure-templates.md) - Templates for blog posts, comparisons, listicles, how-tos, pillar pages

## Next Best Skill

- **Primary**: [content-quality-auditor](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/cross-cutting/content-quality-auditor/SKILL.md) — gate the draft before publishing or handing it off.
