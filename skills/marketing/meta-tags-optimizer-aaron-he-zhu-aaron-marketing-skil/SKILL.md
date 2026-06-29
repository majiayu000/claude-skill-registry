---
name: meta-tags-optimizer
description: 'Use when the user asks to "optimize meta tags"; improves titles, descriptions, Open Graph, Twitter cards, and CTR test variants. Not for JSON-LD structured data — use schema-markup-generator; not for body copy — use seo-content-writer. 标题优化/元描述/CTR'
version: "10.0.1"
license: Apache-2.0
compatibility: "Claude Code and compatible agent-skill hosts"
homepage: "https://github.com/aaron-he-zhu/aaron-marketing-skills"
when_to_use: "Use when optimizing title tags, meta descriptions, Open Graph tags, or Twitter Cards for a page."
argument-hint: "<page URL or content>"
metadata:
  author: aaron-he-zhu
  version: "10.0.1"
  geo-relevance: "low"
---

# Meta Tags Optimizer

Creates title tags, meta descriptions, and social meta tags that improve CTR and sharing quality.

## Quick Start

```
Create meta tags for a page about [topic] targeting [keyword]
```

```
Improve these meta tags for better CTR: [current tags]
```

## Skill Contract

**Expected output**: a ready-to-use metadata package plus the standard handoff summary for `memory/content/`.

- **Reads**: the brief, target keywords, entity inputs, and quality constraints.
- **Writes**: a user-facing metadata deliverable and reusable summary.
- **Promotes**: approved angles, messaging choices, missing evidence, and publish blockers to `memory/hot-cache.md` and `memory/open-loops.md`; propose durable decisions as pending-decision items.
- **Done when**: three title and three description options are provided within the character limits with the keyword front-loaded; a complete OG/Twitter tag block is included; and C01 (Intent Alignment) and C02 (Direct Answer) pass.
- **Primary next skill**: [schema-markup-generator](../schema-markup-generator/SKILL.md) when the metadata package is ready for structured-data support.

### Handoff Summary

> Emit the standard shape from [skill-contract.md §Handoff Summary Format](../../references/skill-contract.md).

## Data Sources

Optional search console and SEO tool integrations pull CTR data and competitor patterns automatically; otherwise ask for current tags, keywords, and competitors. See [CONNECTORS.md](../../CONNECTORS.md).

## Instructions

When a user requests meta-tag optimization, run these six steps:

1. **Gather Page Information** — URL, page type, primary and secondary keywords, audience, CTA, and value proposition.
2. **Create Optimized Title Tag** — keep it near 50-60 characters, front-load the keyword, and generate three options using the supported title formulas.
3. **Write Meta Description** — target 150-160 characters, include the keyword and CTA, and generate three options.
4. **Create Open Graph, Twitter Card, and Additional Meta Tags** — include OG, Twitter, canonical, robots, viewport, author, and article tags as needed.
5. **CORE-EEAT Alignment Check** — verify C01 (Intent Alignment) and C02 (Direct Answer).
6. **Provide CTR Optimization Tips** — explain the winning elements, tradeoffs, and A/B test options.

Label every metric **Measured** (tool/export), **User-provided**, or **Estimated** (model inference); never present an estimate as measured; if a required metric is unavailable, mark it N/A — do not invent it.

> **Reference**: See [Instructions Detail](references/instructions-detail.md) for the compact workflow, formulas, alignment matrix, CTR analysis, and example. See [Meta Tag Code Templates](references/meta-tag-code-templates.md) for HTML blocks.

## Example

See the full worked sample in [Instructions Detail — Example](references/instructions-detail.md#example).

## Save Results

On user confirmation, save to `memory/content/YYYY-MM-DD-<topic>.md` — see [Skill Contract](../../references/skill-contract.md) §Save Results Template.

## Reference Materials

- [Instructions Detail](references/instructions-detail.md) — Workflow, formulas, alignment matrix, example
- [Meta Tag Formulas](references/meta-tag-formulas.md) — Title and description formulas
- [Meta Tag Code Templates](references/meta-tag-code-templates.md) — HTML templates
- [CTR and Social Reference](references/ctr-and-social-reference.md) — CTR patterns and social guidance

## Next Best Skill

- **Primary**: [schema-markup-generator](../schema-markup-generator/SKILL.md) — complete the SERP package with structured data.
