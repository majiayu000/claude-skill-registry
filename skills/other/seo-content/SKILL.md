---
name: seo-content
description: >
  Create high-quality, SEO-optimized content that ranks AND reads like a human
  wrote it. Performs live SERP gap analysis, writes with anti-AI detection
  techniques, and adds schema markup. Use when someone needs a blog post,
  article, SEO page, or wants content that drives search traffic. Triggers on
  'SEO content', 'blog post', 'article', 'SERP', 'programmatic SEO', 'content
  at scale', 'template pages at scale', 'write a post about', 'rank for', or
  'search-optimized content'. Two modes: single article or programmatic SEO at
  scale. Owns programmatic SEO and content-at-scale generation. For a single
  alternatives or vs/comparison page, see /competitor-alternatives; for a
  multi-phase page roadmap with a persistent tracker, see /seo-machine.
category: copy-content
tier: must-have
reads:
  - brand/voice-profile.md
  - brand/keyword-plan.md
  - brand/audience.md
  - brand/landscape.md
writes:
  - brand/assets.md
  - brand/learnings.md
triggers:
  - blog post
  - SEO article
  - long-form content
  - rankable content
  - programmatic SEO
  - pages at scale
  - write SEO content for X
  - create article for keyword
  - refresh article
  - update blog post
---

# /seo-content -- Publication-Ready SEO Content

SEO content has a reputation problem. Most of it is low-value -- keyword-stuffed,
AI-sounding, says nothing new. It ranks for a month, then dies.

This skill creates content that ranks AND builds trust. Content that sounds like
an expert sharing what they know, not a content mill churning out filler.

The goal: Would someone bookmark this? Would they share it? Would they come back?

If yes, Google will reward it. If no, no amount of optimization saves it.

---

## On Activation

1. Read `brand/` directory: load `voice-profile.md`, `keyword-plan.md`,
   `audience.md`, `positioning.md`, `competitors.md`, `learnings.md` if present.
2. Show what loaded:
   ```
   Brand context loaded:
   ├── Voice Profile   ✓ "{tone summary}"
   ├── Keyword Plan    ✓ {N} pillars, {N} briefs
   ├── Audience        ✓ "{audience summary}"
   ├── Positioning     ✓ "{primary angle}"
   ├── Competitors     ✓ {N} competitors profiled
   └── Learnings       ✓ {N} entries
   ```
3. If files missing, note suggestions at the end (e.g., run /brand-voice).
4. Check for existing content file at `./campaigns/content/{keyword-slug}.md`.
   - **If exists** --> Content Refresh Mode (see below).
   - **If not** --> Full Creation Mode.
5. Determine mode: **Single article** or **Scale mode** (programmatic SEO).
6. Read `brand/landscape.md` if it exists — check the Claims Blacklist before making ecosystem or competitive claims. If stale (>14 days) or missing, warn that market claims may be outdated.

## Prioritization (defer to seo-machine's publishing order)

When the user asks "what should I write next?" — the answer follows seo-machine's **conversion-intent-first publishing order**, not "whatever has highest volume":

| Order | Pattern | Why |
|---|---|---|
| 1 | `/alternatives/[competitor]` | Highest conversion intent — reader is already in market |
| 2 | `/compare/[a]-vs-[b]` | Be the third option in any two-vendor comparison |
| 3 | `/for/[use-case]` and `/for/[audience]` | JTBD without competitor name — high TP/volume ratio |
| 4 | Long-form playbooks (this skill's wheelhouse) | Authority + AI-citation + inbound link draw |
| 5 | Generic blog posts | Lowest conversion — defer until ~10 indexed pages exist |

If `docs/seo-machine.md` exists at the project root, route the user to that skill's Resume mode instead of writing standalone articles — the roadmap there already encodes the priority order. seo-content is the right tool for **single articles** and **playbook-pattern long-form**; alternatives/compare/use-case pages belong in seo-machine's programmatic sprint.

---

## Brand Memory

### Reads (if they exist)

| File | What it provides | How it shapes output |
|------|-----------------|---------------------|
| voice-profile.md | Tone, personality, vocabulary, rhythm | Directly shapes writing style |
| keyword-plan.md | Prioritized keywords, content briefs, SERP data | Target keyword, cluster, intent, content type |
| audience.md | Buyer profiles, sophistication level, pain points | How technical to write, what examples to use |
| positioning.md | Market angles, differentiators | Unique angle for the piece |
| competitors.md | Named competitors, their positioning | What angle competitors take |
| learnings.md | Past performance data | What content approaches worked before |

### Writes

| File | What it contains |
|------|-----------------|
| ./campaigns/content/{keyword-slug}.md | Publication-ready article with frontmatter |
| ./brand/assets.md | Appends entry for the created content piece |
| ./brand/learnings.md | Appends findings after feedback collection |

---

## Required Inputs

1. **Target keyword** -- Primary keyword to rank for
2. **Keyword cluster** -- Related keywords to include naturally
3. **Search intent** -- Informational / Commercial / Transactional
4. **Content type** -- Pillar guide / How-to / Comparison / Listicle / etc.
5. **Brand voice profile** -- (from voice-profile.md, if available)
6. **Unique angle** -- What perspective makes this different?

Pre-fill from brand memory when available. Ask the user only for what's missing.

---

## The Workflow (Single Article)

```
RESEARCH --> BRIEF --> OUTLINE --> DRAFT --> HUMANIZE --> OPTIMIZE --> SCHEMA --> REVIEW --> SAVE
```

### Phase 1: Research (SERP Analysis)

Use Exa MCP or firecrawl for live SERP research. Analyze top 5 results.

**For each result capture:** Title/URL, content type, word count, structure,
unique angles, gaps, recency, domain type.

**Extract SERP features:** People Also Ask (ALL of them), Featured Snippet
format, AI Overview presence.

**Gap analysis:** What's missing? What's outdated? What's generic? What's your edge?

Present findings in structured format. See `references/serp-analysis-format.md`.

If web search unavailable: flag to user, prefix SERP claims with `~`, skip to
Phase 2 using brand context instead.

### Phase 2: Content Brief

Create or enhance an existing brief from /keyword-research. Include: target
keyword, secondary keywords, search intent, content type, target word count,
audience, unique angle, key points, PAA questions, competitor gaps, internal
links, CTA.

### Phase 3: Outline

Structure based on content type. See `references/content-structures.md` for
templates (Pillar Guide, How-To, Comparison, Listicle).

Map PAA questions: depth-worthy ones become H2s, brief ones go to FAQ section.

### Phase 4: Draft

**Voice calibration:** Match voice-profile.md if loaded. Default: direct,
conversational, specific, opinionated.

**Rules:**
- Answer the search query in the first 2-3 sentences
- Apply the "So What?" chain -- write from the bottom, not the top
- Specificity over generality (numbers, examples, always)
- Show your work (how you know, not just what you claim)
- Use positioning angle from positioning.md to shape perspective

### Phase 5: Humanize (Critical)

This is the soul of the skill. See `references/anti-ai-detection.md` for the
full detection pattern guide.

**Summary checklist:**
- Kill AI words (delve, comprehensive, crucial, leverage, landscape, etc.)
- Kill AI phrases ("In today's...", "It's important to note...", "Let's dive in")
- Break the triple pattern -- humans are messier
- Inject: personal experience, opinions with reasoning, admitted limitations,
  specific examples, honest uncertainty, tangents and asides
- Vary rhythm: short punches, long explanations, fragments, questions

**The Read-Aloud Test:** If you stumble reading it aloud, rewrite it.

### Phase 6: Optimize (On-Page SEO)

```
[ ] Primary keyword in title (front-loaded), H1, first 100 words, 1+ H2, meta, URL slug
[ ] Secondary keywords in H2s naturally
[ ] Meta description: 150-160 chars, compelling, includes keyword
[ ] Internal links: 4-8 per piece
[ ] External links: 2-4 authoritative sources
[ ] Featured snippet optimization (definition/list/table format)
[ ] Image alt text with relevant keywords
```

**Title format:** [Primary Keyword]: [Benefit or Hook] ([Year] if relevant)
Under 60 characters, front-load keyword.

### Phase 7: Schema Markup (JSON-LD)

Generate for EVERY article:

1. **Article schema** -- headline, description, author, dates, publisher, keywords
2. **FAQ schema** -- from PAA questions answered in the article
3. **HowTo schema** -- if content type is how-to tutorial

Include schema in article frontmatter. See `references/schema-templates.md`.

### Phase 8: Quality Review

Run all checklists before saving:
- **Content quality:** Answers title in first 300 words, 3+ specific examples,
  unique angle present, all PAA answered, SERP gaps addressed
- **Voice quality:** No AI-isms, personality present, matches voice-profile.md
- **SEO quality:** Keywords placed, meta compelling, links included, schema valid
- **E-E-A-T:** Experience shown, expertise demonstrated, sources cited

See `references/eeat-examples.md` for 20 top-performing human content examples.

---

## Content Refresh Mode

Triggered when content file already exists for the target keyword.

1. Present existing content summary with options: Refresh / Rewrite / Expand / Start Fresh
2. **If Refresh:** Re-run SERP analysis, compare against article:
   - New competitors since publication?
   - New PAA questions not covered?
   - Featured Snippet format changed?
   - Search intent shifted?
3. Generate specific, actionable update recommendations (not "update the content"
   but "add section on {topic} after {section} because {evidence}")
4. Apply updates, bump `last_updated` and `serp_snapshot_date` in frontmatter

---

## Scale Mode (Programmatic SEO)

Triggered when user wants template-driven pages at scale ("programmatic SEO",
"pages at scale", "100 pages for...", "location pages", etc.).

### Core Principles

1. **Unique value per page** -- not just swapped variables in a template
2. **Proprietary data wins** -- hierarchy: proprietary > product-derived >
   user-generated > licensed > public
3. **Clean URL structure** -- use subfolders, not subdomains
4. **Search intent match** -- pages must answer what people are searching
5. **Quality over quantity** -- 100 great pages beat 10,000 thin ones

### The 12 Playbooks

| Playbook | Pattern | Example |
|----------|---------|---------|
| Templates | "[Type] template" | "resume template" |
| Curation | "best [category]" | "best website builders" |
| Conversions | "[X] to [Y]" | "$10 USD to GBP" |
| Comparisons | "[X] vs [Y]" | "webflow vs wordpress" |
| Examples | "[type] examples" | "landing page examples" |
| Locations | "[service] in [location]" | "dentists in austin" |
| Personas | "[product] for [audience]" | "crm for real estate" |
| Integrations | "[product A] + [product B]" | "slack asana integration" |
| Glossary | "what is [term]" | "what is pSEO" |
| Translations | Content in multiple languages | Localized content |
| Directory | "[category] tools" | "ai copywriting tools" |
| Profiles | "[entity name]" | "stripe ceo" |

See `references/pseo-playbooks.md` for detailed implementation of each playbook.

### Choosing a Playbook

| If you have... | Consider... |
|----------------|-------------|
| Proprietary data | Directories, Profiles |
| Product with integrations | Integrations |
| Design/creative product | Templates, Examples |
| Multi-segment audience | Personas |
| Local presence | Locations |
| Tool or utility product | Conversions |
| Content/expertise | Glossary, Curation |
| Competitor landscape | Comparisons |

You can layer multiple playbooks (e.g., "Best coworking spaces in San Diego").

### Scale Mode Implementation

1. **Keyword pattern research** -- identify repeating structure, variables, combinations
2. **Data requirements** -- what populates each page, how it's updated
3. **Template design** -- page structure with conditional content for uniqueness
4. **Internal linking architecture** -- hub and spoke model, no orphan pages
5. **Indexation strategy** -- prioritize high-volume, noindex thin variations,
   separate sitemaps by type

### Scale Mode Quality Checks

- [ ] Each page provides unique value (not just variable swaps)
- [ ] Unique titles and meta descriptions per page
- [ ] Proper heading structure and schema markup
- [ ] Connected to site architecture, no orphan pages
- [ ] In XML sitemap, crawlable, no conflicting noindex

---

## Worked Example

**Target keyword:** 'is doordash organic'
**SERP gap:** Top 5 results are forum posts and outdated blog articles. No definitive guide exists.

**Article outline:**
1. H1: Is DoorDash Organic? The Complete Guide for Health-Conscious Families
2. Quick answer (Featured Snippet target): 'DoorDash itself doesn't verify verification status...'
3. How to find verified-source restaurants on DoorDash (step-by-step with screenshots)
4. The problem with DoorDash's verification filter (cross-contamination, no certification)
5. Better alternatives for guaranteed verified meal delivery
6. FAQ schema: 'Does DoorDash have verified-source options?' / 'How do I know if a restaurant is really verified?'

**Word count:** 1,800 (benchmark: top 3 results average 1,200 — we go deeper)

---

## File Output Format

### File Location

```
./campaigns/content/{keyword-slug}.md
```

Slug: lowercase kebab-case, remove stop words if over 60 chars.

### Frontmatter

```yaml
---
title: "{SEO-Optimized Title}"
meta_description: "{150-160 character meta description}"
primary_keyword: "{target keyword}"
secondary_keywords: ["{kw1}", "{kw2}", "{kw3}"]
content_type: "{pillar-guide / how-to / comparison / listicle}"
search_intent: "{informational / commercial / transactional}"
target_word_count: {number}
actual_word_count: {number}
author: "{author name}"
date_created: "{YYYY-MM-DD}"
last_updated: "{YYYY-MM-DD}"
status: "draft"
serp_snapshot_date: "{YYYY-MM-DD}"
paa_questions_answered: {number}
schema_article: |
  {Article JSON-LD}
schema_faq: |
  {FAQ JSON-LD}
---
```

---

## Chain Offers

After saving, present:

- `/content-atomizer` -- distribute across social (3-5 LinkedIn, 8-12 Twitter, 2-3 IG carousels)
- `/newsletter` -- feature article in next edition
- `/email-sequences` -- nurture readers into subscribers
- `/seo-content` -- write next article from keyword plan
- "Refresh" to update this article later

---

## Error States

- **No web search:** Skip Phase 1, note limitation, proceed with brand context
- **No target keyword:** Ask user or suggest /keyword-research
- **No voice profile:** Use defaults (direct, conversational), suggest /brand-voice
- **Can't save:** Display content for manual copy, suggest checking permissions

---

## Anti-Patterns

| Anti-pattern | Instead | Why |
|-------------|---------|-----|
| Skipping Phase 5 (Humanize) to save time | Cut research depth before cutting humanization | Unhumanized content reads like AI slop — readers bounce, Google devalues it, and the brand takes a credibility hit. Content that sounds like a committee wrote it doesn't earn trust, links, or shares. |
| Skipping schema markup | Always add Article + FAQ JSON-LD — it takes minutes | Schema compounds over time: rich results, AI citations, and structured search features for the life of the content. Skipping it leaves free visibility on the table. |
| Keyword-stuffing headings | One keyword in H1, natural secondary keywords in H2s | Google detects keyword stuffing and users find it off-putting. If every heading reads like an SEO template, it's over-optimized. |
| Starting with a generic intro | Answer the search query in sentence one | "In today's digital world..." tells the reader nothing. The search query brought them here — if the value prop isn't instant, they bounce. |

---

## Implementation Notes

1. **Never skip SERP analysis** when web search is available -- it's the differentiator
2. **Always check for existing content first** -- refresh mode is high value
3. **Always generate schema markup** -- Article + FAQ JSON-LD minimum
4. **Always save to disk** -- the file IS the deliverable
5. **PAA questions are mandatory** -- every one appears as H2 or FAQ entry
6. **Phase 5 (Humanize) is non-negotiable** -- run the full AI detection checklist
7. **Always offer chain to /content-atomizer** -- one article = 10+ social assets
8. **Register every piece** in `./brand/assets.md`
9. **Feedback closes the loop** -- always present, always log
