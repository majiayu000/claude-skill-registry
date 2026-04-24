---
name: meta-tags-optimizer
description: 'Optimize title tags, meta descriptions, Open Graph, Twitter cards for maximum CTR with A/B variations. 标题优化/元描述/CTR'
version: "9.1.0"
license: Apache-2.0
compatibility: "Claude Code, skills.sh, ClawHub, Vercel Labs, Cursor, Windsurf, Codex CLI, Amp, Gemini CLI, Kimi Code, Qwen Code, CodeBuddy"
homepage: "https://github.com/aaron-he-zhu/seo-geo-claude-skills"
when_to_use: "Use when optimizing title tags, meta descriptions, Open Graph tags, or Twitter Cards for a page."
argument-hint: "<page URL or content>"
metadata:
  author: aaron-he-zhu
  version: "9.1.0"
  geo-relevance: "low"
  tags:
    - seo
    - meta-tags
    - title-tag
    - meta-description
    - open-graph
    - twitter-card
    - ctr-optimization
    - social-sharing
    - 标题优化
    - 元描述
    - メタタグ
    - 메타태그
    - meta-tags-seo
  triggers:
    # EN-formal
    - "optimize title tag"
    - "write meta description"
    - "improve CTR"
    - "Open Graph tags"
    - "title optimization"
    - "meta tags"
    # EN-casual
    - "my title tag needs work"
    - "low click-through rate"
    - "fix my meta tags"
    - "OG tags not showing"
    # EN-question
    - "how to write a good title tag"
    - "how to improve click-through rate"
    # EN-competitor
    - "Yoast SEO title tool"
    - "RankMath title optimizer"
    # ZH-pro
    - "标题标签优化"
    - "元描述优化"
    - "OG标签"
    - "点击率提升"
    - "社交预览"
    - "TDK优化"
    # ZH-casual
    - "标题不好"
    - "点击率太低"
    - "社交分享预览不对"
    - "标题怎么写"
    - "TDK怎么写"
    # JA
    - "メタタグ最適化"
    - "タイトルタグ"
    - "CTR改善"
    # KO
    - "메타 태그 최적화"
    - "제목 태그"
    - "클릭률 개선"
    # ES
    - "optimizar meta tags"
    - "mejorar CTR"
    - "etiquetas Open Graph"
    # PT
    - "otimizar meta tags"
---

# Meta Tags Optimizer

This skill creates compelling, optimized meta tags that improve click-through rates from search results and enhance social media sharing. It covers title tags, meta descriptions, and social meta tags.

## What This Skill Does

Creates optimized title tags, meta descriptions, Open Graph, and Twitter Card markup with proper character limits, CTR analysis, and A/B test variations.

## Quick Start

Start with one of these prompts. Finish with a short handoff summary using the repository format in [Skill Contract](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/skill-contract.md).

### Create Meta Tags

```
Create meta tags for a page about [topic] targeting [keyword]
```

```
Write title and meta description for this content: [content/URL]
```

### Optimize Existing Tags

```
Improve these meta tags for better CTR: [current tags]
```

### Social Media Tags

```
Create Open Graph and Twitter card tags for [page/URL]
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

Optional search console and SEO tool integrations pull CTR data and competitor patterns automatically; otherwise ask the user for current tags, keywords, and competitors. See [CONNECTORS.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/CONNECTORS.md) for integration placeholders.

## Instructions

When a user requests meta tag optimization, run these six steps:

1. **Gather Page Information** — URL, page type, primary/secondary keywords, target audience, primary CTA, unique value prop
2. **Create Optimized Title Tag** — 50-60 chars, primary keyword front-loaded; pick from 5 formula options (Keyword|Benefit|Brand, Number+Keyword+Promise, How-to, Question, Year+Keyword); generate 3 options with power word analysis
3. **Write Meta Description** — 150-160 chars, primary keyword, CTA; use `[Offer] + [Benefit] + [CTA]` formula; generate 3 options with CTA and emotional trigger labels
4. **Create Open Graph, Twitter Card, and Additional Meta Tags** — OG (og:type/url/title/description/image), Twitter Card, canonical, robots, viewport, author, article tags; combine into full block
5. **CORE-EEAT Alignment Check** — verify C01 (Intent Alignment) and C02 (Direct Answer) with Pass/Warn/Fail
6. **Provide CTR Optimization Tips** — power words analysis, CTR boosting elements table (Numbers +20-30%, Year +15-20%, Power Words +10-15%, Question +10-15%, Brackets +10%), A/B test suggestions

> **Reference**: See [references/instructions-detail.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/build/meta-tags-optimizer/references/instructions-detail.md) for full templates (page analysis, title/description formula options, CORE-EEAT alignment matrix, CTR optimization analysis), worked example, and tips. See [references/meta-tag-code-templates.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/build/meta-tags-optimizer/references/meta-tag-code-templates.md) for HTML code templates.

## Example

**User**: "Create meta tags for a blog post about 'how to start a podcast in [current year]'"

**Output** (abbreviated):
- Title: `<title>How to Start a Podcast in [year]: Complete Beginner's Guide</title>` (~55 chars, keyword front-loaded, power words: Complete, Beginner's)
- Description: `<meta name="description" content="Learn how to start a podcast in [year] with our step-by-step guide. Covers equipment, hosting, recording, and launching your first episode. Start podcasting today!">` (~163 chars, CTA included)

See the full example (with OG, Twitter, Article tags and 3 A/B variations) in [references/instructions-detail.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/build/meta-tags-optimizer/references/instructions-detail.md#example).

## Tips for Success

Front-load keywords; match intent; be specific; test variations; update regularly; check competitors. Full list in [references/instructions-detail.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/build/meta-tags-optimizer/references/instructions-detail.md#tips-for-success).


### Save Results

On user confirmation, save a dated summary to `memory/content/YYYY-MM-DD-<topic>.md` and promote key conclusions to `memory/hot-cache.md`.

## Reference Materials

- [Instructions Detail](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/build/meta-tags-optimizer/references/instructions-detail.md) — Full 6-step workflow, title/description formulas, CORE-EEAT alignment matrix, CTR analysis, worked example, tips
- [Meta Tag Formulas](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/build/meta-tags-optimizer/references/meta-tag-formulas.md) — Proven title and description formulas
- [Meta Tag Code Templates](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/build/meta-tags-optimizer/references/meta-tag-code-templates.md) — HTML templates (OG, Twitter, article tags)
- [CTR and Social Reference](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/build/meta-tags-optimizer/references/ctr-and-social-reference.md) — Page-type templates, CTR data, OG best practices

## Next Best Skill

- **Primary**: [schema-markup-generator](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/build/schema-markup-generator/SKILL.md) — complete the SERP packaging with structured data.
