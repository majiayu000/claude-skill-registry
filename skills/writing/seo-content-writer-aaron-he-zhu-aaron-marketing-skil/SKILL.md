---
name: seo-content-writer
description: 'Use when the user asks to "write SEO content"; drafts new posts, articles, and landing pages with keywords, headers, snippets, and evidence boundaries. Not for AI-citation/GEO readiness scoring — use geo-content-optimizer; not for updating decaying existing content — use content-refresher. SEO文章写作/内容优化'
version: "10.0.1"
license: Apache-2.0
compatibility: "Claude Code and compatible agent-skill hosts"
homepage: "https://github.com/aaron-he-zhu/aaron-marketing-skills"
when_to_use: "Use when writing SEO-optimized articles, blog posts, landing pages, or product descriptions. Also when the user asks to create content targeting a specific keyword."
argument-hint: "<topic> <target keyword>"
metadata:
  author: aaron-he-zhu
  version: "10.0.1"
  geo-relevance: "medium"
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

- **Reads**: the brief, target keywords, entity inputs, and quality constraints.
- **Writes**: a user-facing content deliverable and reusable summary.
- **Promotes**: approved angles, messaging choices, missing evidence, and publish blockers to `memory/hot-cache.md` and `memory/open-loops.md`; propose durable decisions as pending-decision items.
- **Done when**: the draft satisfies the target intent with the primary keyword placed naturally; H1/H2 structure, meta description, and at least one snippet-targetable block are present; and every claim needing a source is either cited or flagged.
- **Primary next skill**: [content-quality-auditor](../../cross-cutting/content-quality-auditor/SKILL.md) when the draft is ready for gating.

### Handoff Summary

> Emit the standard shape from [skill-contract.md §Handoff Summary Format](../../references/skill-contract.md).

## Data Sources

Use `~~SEO tool` and `~~search console` when connected; otherwise ask for keywords, intent, and competitors. See [CONNECTORS.md](../../CONNECTORS.md).

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

Any factual claim, statistic, or quote that requires a source must be cited or explicitly flagged `[needs source]`; never invent figures, studies, dates, or attributions to fill a gap.

**Quality bar**: before handing off, confirm the draft passes — (1) intent match: a reader with the target query gets their answer above the fold; (2) keyword placement reads naturally (no stuffing) in title, H1, first 100 words, and one H2; (3) structure is scannable (H2/H3, lists, one snippet-ready block); (4) zero fabricated facts — every source-needing claim is cited or `[needs source]`. If any item fails, fix it or report it in the handoff, do not ship silently.

> **Reference**: See [Instructions Detail](references/instructions-detail.md) for the compact workflow, pre-write checklist, issue-classification rules, and self-check format.

## Example

See [references/seo-writing-checklist.md](references/seo-writing-checklist.md) for the copy-start checklist and article template.

## Content Type Templates

Quick-start patterns for how-to guides, comparisons, listicles, pillar pages, reviews, and FAQ pages live in [references/content-structure-templates.md](references/content-structure-templates.md).

## Save Results

On user confirmation, save to `memory/content/YYYY-MM-DD-<topic>.md` — see [Skill Contract](../../references/skill-contract.md) §Save Results Template.

## Reference Materials

- [Instructions Detail](references/instructions-detail.md) — Workflow, CORE-EEAT constraints, issue handling, self-check
- [SEO Writing Checklist](references/seo-writing-checklist.md) — On-page checklist, snippet patterns, and copy-start template
- [Title Formulas](references/title-formulas.md) — Headline formulas and CTR patterns
- [Content Structure Templates](references/content-structure-templates.md) — Compact content blueprints

## Next Best Skill

- **Primary**: [content-quality-auditor](../../cross-cutting/content-quality-auditor/SKILL.md) — gate the draft before publishing.
