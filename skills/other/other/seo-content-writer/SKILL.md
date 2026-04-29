---
name: seo-content-writer
description: 'Write SEO blog posts, articles, landing pages with keyword integration, header optimization, and snippet targeting. SEO文章写作/内容优化'
version: "9.9.5"
license: Apache-2.0
compatibility: "Claude Code, skills.sh, ClawHub, Vercel Labs, Cursor, Windsurf, Codex CLI, Amp, Gemini CLI, Kimi Code, Qwen Code, CodeBuddy"
homepage: "https://github.com/aaron-he-zhu/seo-geo-claude-skills"
when_to_use: "Use when writing SEO-optimized articles, blog posts, landing pages, or product descriptions. Also when the user asks to create content targeting a specific keyword."
argument-hint: "<topic> <target keyword>"
metadata:
  author: aaron-he-zhu
  version: "9.9.5"
  geo-relevance: "medium"
  tags:
    - seo
    - content-writing
    - blog-writing
    - seo-copywriting
    - content-creation
    - article-writing
    - landing-page
    - SEO文章
    - 博客写作
    - SEOライティング
    - SEO글쓰기
    - redaccion-seo
  triggers:
    - "write SEO content"
    - "create blog post"
    - "SEO copywriting"
    - "write me a blog post"
    - "help me write about"
    - "how to write SEO friendly content"
    - "SurferSEO alternative"
    - "SEO文章写作"
    - "博客写作"
    - "帮我写文章"
    - "写一篇SEO文章"
    - "SEOライティング"
    - "ブログ記事作成"
    - "SEO 글쓰기"
    - "블로그 작성"
    - "redacción SEO"
    - "escribir artículo SEO"
    - "redação SEO"
    - "escrever artigo SEO"
---

# SEO Content Writer

Creates SEO content that aligns with search intent, integrates keywords naturally, and stays usable for readers.

## Quick Start

```
Write an SEO-optimized article about [topic] targeting the keyword [keyword]
```

```
Here's my content brief: [brief]. Write SEO-optimized content following this outline.
```

## Skill Contract

**Expected output**: a ready-to-use draft plus the standard handoff summary for `memory/content/`.

- **Reads**: the brief, target keywords, entity inputs, quality constraints, and prior decisions from [CLAUDE.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/CLAUDE.md) and the shared [State Model](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/state-model.md) when available.
- **Writes**: a user-facing content deliverable and reusable summary.
- **Promotes**: approved angles, messaging choices, missing evidence, and publish blockers to `memory/hot-cache.md`, `memory/decisions.md`, and `memory/open-loops.md`.
- **Primary next skill**: [content-quality-auditor](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/cross-cutting/content-quality-auditor/SKILL.md) when the draft is ready for gating.

### Handoff Summary

> Emit the standard shape from [skill-contract.md §Handoff Summary Format](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/skill-contract.md).

## Data Sources

Use `~~SEO tool` and `~~search console` when connected; otherwise ask for keywords, intent, and competitors. See [CONNECTORS.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/CONNECTORS.md).

## Instructions

When a user requests SEO content, run these nine steps:

1. **Gather Requirements** — confirm primary and secondary keywords, word count, content type, audience, intent, tone, CTA, and competitors.
2. **Load CORE-EEAT Constraints** — apply the 16 high-weight items listed in the companion reference.
3. **Research and Plan** — analyze the SERP, map keywords, and choose the content angle.
4. **Create Optimized Title** — keep it concise, keyword-led, and aligned with intent.
5. **Write Meta Description** — include the keyword, value proposition, and CTA.
6. **Structure Content and Write** — use a clean H1 > intro > H2/H3 > FAQ > conclusion flow.
7. **Apply On-Page Best Practices** — manage keyword placement, readability, snippets, and supporting visuals.
8. **Add Internal / External Links** — include relevant internal and authoritative external links.
9. **Run Final SEO + CORE-EEAT Review** — score the draft, auto-fix small issues, and surface any decisions that still need the user.

> **Reference**: See [references/instructions-detail.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/build/seo-content-writer/references/instructions-detail.md) for the compact workflow, pre-write checklist, issue-classification rules, and self-check format.

## Example

Sample outcome: a keyword-led H1, optimized meta description, clear H2 structure, FAQ section, and a brief Changes Made block after the self-check. See [references/seo-writing-checklist.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/build/seo-content-writer/references/seo-writing-checklist.md) for the copy-start checklist and article template.

## Content Type Templates

Quick-start patterns for how-to guides, comparisons, listicles, pillar pages, reviews, and FAQ pages live in [references/content-structure-templates.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/build/seo-content-writer/references/content-structure-templates.md).

## Tips for Success

Match intent, front-load value, support claims with evidence, and write for humans before optimizing for the SERP.

### Save Results

On user confirmation, save `memory/content/YYYY-MM-DD-<topic>.md` and promote key conclusions to `memory/hot-cache.md`.

## Reference Materials

- [Instructions Detail](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/build/seo-content-writer/references/instructions-detail.md) — Workflow, CORE-EEAT constraints, issue handling, self-check
- [SEO Writing Checklist](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/build/seo-content-writer/references/seo-writing-checklist.md) — On-page checklist, snippet patterns, and copy-start template
- [Title Formulas](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/build/seo-content-writer/references/title-formulas.md) — Headline formulas and CTR patterns
- [Content Structure Templates](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/build/seo-content-writer/references/content-structure-templates.md) — Compact content blueprints

## Next Best Skill

- **Primary**: [content-quality-auditor](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/cross-cutting/content-quality-auditor/SKILL.md) — gate the draft before publishing.
