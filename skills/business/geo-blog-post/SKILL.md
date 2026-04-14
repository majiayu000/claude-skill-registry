---
name: geo-blog-post
description: Use when writing or editing a blog post optimized for AI citations — covers post structure, frontmatter patterns, content rules, schema requirements, and a pre-publish GEO checklist based on Princeton research.
---

# GEO-Optimized Blog Post

GEO (Generative Engine Optimization) means structuring content so AI engines (ChatGPT, Perplexity, Claude) cite it when answering user questions. These patterns maximize citation rate based on Princeton research on what AI engines prefer to cite.

## Recommended Frontmatter

```yaml
title: "Post Title (And Practical Benefit)"   # required
date: "2026-04-08"                             # required
summary: "1–2 sentence TL;DR — shown in header and used as meta description"  # required
image: "/images/YYYY-MM-DD-slug.png"           # optional, 1200×628
alt: "Description of hero image"              # optional
lastUpdated: "2026-04-10"                      # optional, show when content is refreshed
author: "Author Name"                          # optional
faq:                                           # strongly recommended — source for FAQPage schema
  - question: "Short question (5–8 words)?"
    answer: "40–65 word plain-text answer. No markdown formatting."
```

**Schema to emit per post:** BlogPosting (headline, datePublished, dateModified, author, image) + FAQPage (one Question/Answer per faq entry). Frameworks like Astro can auto-generate from frontmatter; otherwise add JSON-LD manually.

## Post Anatomy

Recommended top-to-bottom order:

1. Byline — date and author
2. H1 — one per post
3. **TL;DR box** — `summary` displayed prominently at the top
4. Last updated notice (if content was refreshed)
5. Hero image with descriptive alt text
6. Table of contents (generated from headings)
7. Body
8. **FAQ section** — rendered as accordion or static; must also appear in schema
9. CTA
10. Author bio with credentials (strengthens E-E-A-T signal)

## Article Targets

| Target | Value |
|--------|-------|
| Body length | 2,000–3,000 words |
| H2 sections | 6–8 |
| H3 subsections per H2 | 0–6 |
| Pull quotes | 1 per post |
| Comparison table | 1 (only for "vs" topics) |
| FAQ pairs | 6–8 |
| External citations | 3+ with source links |

## Section Patterns

| Section type | Words | Paragraphs | Pattern |
|---|---|---|---|
| TL;DR | 40–60 | 1 | Single paragraph, standalone thesis |
| H2 intro (narrative) | 100–180 | 3–4 | **Bold lead sentence** → supporting paragraphs → bullet list |
| H2 intro (transitional) | 20–30 | 1 | One bold sentence bridging to H3s |
| H3 deep-dive | 70–120 | 2–3 | Short intro → bullet list (3–5 items) |
| H3 numbered tip | 40–55 | 1 | One sentence + 4–5 bullet items |
| H3 competitor/profile | 40–65 | 1 | One paragraph, **bold key descriptor** inline |
| FAQ answer | 40–65 | 1 | Plain text, no formatting |

## Structural Rules

1. **Bold lead sentences** — Every H2 opens with one bold sentence stating the section thesis. H3s may also. Never more than one per section opener.

2. **H2 = narrative arc, H3 = detail** — H2 intro is either a full narrative block (100–180 words) or a single transitional sentence (20–30 words) setting up its H3s.

3. **Lists are the workhorse** — Most H3s use bullet lists. Bullet items: 8–15 words each. Numbered lists only for sequences or rankings.

4. **One visual break per ~500–700 words** — A list, table, blockquote, or image roughly every 500–700 words. No prose block runs more than ~200 words without a break.

5. **FAQ = 6–8 pairs** — Questions: 5–8 words. Answers: 40–65 words, plain text only. Must appear in schema, not just the markdown body.

6. **Numbered H3s for actionable sections** — Tips/strategies get numbered H3s (`### 1. Do X`). Each: one sentence + bullets.

7. **Uniform competitor/tool profiles** — Exactly one paragraph each (~45–55 words), bold key descriptor inline. No bullets.

## Title Pattern

`[Topic Explanation] (And [Practical Benefit])`

Examples:
- "How ChatGPT Searches Work (And How to Get Your Brand Found)"
- "What is AEO Monitoring (And Why Your Brand Needs It)"

## Pull Quote Format

```markdown
> "Quoted text here."
>
> — Author Name, Role at Company
```

One per post. Place after a key insight lands, not at the top.

## Pre-Publish GEO Checklist

Based on Princeton GEO research — each item has a measurable citation lift:

- [ ] **External citations** (+40%) — link to source for every statistic; no unsourced numbers
- [ ] **Statistics present** (+37%) — at least 3 specific data points with percentages, counts, or timeframes
- [ ] **Pull quote with attribution** (+30%) — named expert, not anonymous
- [ ] **FAQ in schema** (+40%) — 6–8 pairs as FAQPage schema, not just markdown
- [ ] **Fresh signal** (pages updated within 30 days cited 3.2x more) — set `lastUpdated` when refreshing content
- [ ] **Internal links** — 2+ links to related posts on the same domain
- [ ] **Alt text** — descriptive, not a filename echo
- [ ] **Summary** — 1–2 punchy sentences usable as a standalone meta description
- [ ] **Author bio** — name, role, and credentials visible on the page (E-E-A-T)
