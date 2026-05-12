# GEO/SEO Scoring Rubric

7 dimensions, 0–4 each, 28 points total. Every threshold grounded in published research.

---

## Dimension 1: AI Crawler Access

**Why it matters:** AI crawlers don't execute JavaScript. If they can't reach your content, no optimization helps.

### Checks

1. Parse `robots.txt` for AI crawlers in three tiers: search-critical, user-triggered fetch, and training-only
2. Search-critical: OAI-SearchBot, PerplexityBot, Claude-SearchBot, Bingbot, Googlebot, Bravebot, YouBot
3. User-triggered fetch (recommended to allow): ChatGPT-User, Perplexity-User, Claude-User
4. Training-only (safe to block): GPTBot, ClaudeBot, Google-Extended, CCBot, Bytespider, Amazonbot, Diffbot, Applebot-Extended
5. Detect CDN bot blocking: Cloudflare Bot Fight Mode, Akamai Bot Manager, Vercel firewall, AWS WAF
6. Check rendering mode: SSR/SSG vs CSR/SPA

### Scoring

| Score | Criteria |
|-------|----------|
| 0 | Search-critical bots blocked in robots.txt, OR CDN bot blocking detected, OR JavaScript-only rendering (P0) |
| 1 | Some search bots allowed but OAI-SearchBot or PerplexityBot blocked |
| 2 | All search-critical bots allowed but user-triggered fetch bots (ChatGPT-User, Perplexity-User) blocked |
| 3 | All search-critical + user-triggered fetch bots allowed, no CDN blocking |
| 4 | All bots allowed + IndexNow configured + server responds <500ms to bot User-Agents |

**P0 trigger:** Score 0 → "AI crawlers cannot access this site. Fix rendering/access before any GEO work."

**Research basis:** AI crawlers don't execute JS (multiple sources). 89% more crawl completeness with flat architecture (Aether Research 2026).

---

## Dimension 2: AI Discovery Infrastructure

**Why it matters:** llms.txt is the emerging standard for AI-readable site summaries. Near-zero cost, adopted by Anthropic and Perplexity.

### Checks

1. `llms.txt` — exists, follows Jeremy Howard spec (H1, blockquote, H2 sections, link lists)
2. `llms-full.txt` — extended version with full content inlining
3. `sitemap.xml` — exists with `<lastmod>` dates
4. RSS/Atom feed — exists and is valid
5. `robots.txt` — contains `LLMs-Txt:` discovery directive

### Scoring

| Score | Criteria |
|-------|----------|
| 0 | No llms.txt, no AI-specific discovery files |
| 1 | llms.txt present but minimal (H1 only, no blockquote or sections) |
| 2 | llms.txt with H1 + blockquote + H2 sections; OR sitemap with `<lastmod>` dates |
| 3 | Well-structured llms.txt with `## Optional` section + sitemap with lastmod + RSS/Atom feed |
| 4 | llms.txt + llms-full.txt + sitemap + RSS + `LLMs-Txt:` directive in robots.txt |

**Research basis:** SE Ranking 300K-domain study: no measurable citation improvement from llms.txt alone, but near-zero implementation cost and it forces content inventory (Nov 2025). Anthropic and Perplexity confirmed support.

---

## Dimension 3: Structured Data Quality

**Why it matters:** 73% of AI-cited pages have schema vs 30% average (Rankeo, 50K AI responses). FAQPage schema produces 2.7x citation lift (Relixir 2025). But minimal schema is WORSE than none.

### Checks

1. JSON-LD presence — grep for `application/ld+json`
2. @type coverage — list all types, compare against site-type requirements
3. Attribute count — count per primary type (threshold: 8+)
4. sameAs links — present and pointing to real profiles
5. Nesting — author as Person, publisher as Organization
6. Duplicate singletons — two FAQPage on same page (silently dropped by Google)
7. dateModified — present on content types

### Required @types by Site Type

| Type | Required | Bonus |
|------|----------|-------|
| ecommerce | Product, Organization, BreadcrumbList | AggregateRating, Review, Offer |
| saas | Organization, SoftwareApplication, FAQPage | HowTo, Article |
| content | Article, Organization, Person | NewsArticle, BlogPosting, LiveBlogPosting |
| local | LocalBusiness, Organization | Review, GeoCoordinates, OpeningHoursSpecification |
| docs | TechArticle, Organization | HowTo, SoftwareSourceCode |
| personal | Person, Organization | CreativeWork, Article |

### Scoring

| Score | Criteria |
|-------|----------|
| 0 | No JSON-LD structured data found |
| 1 | Generic schema with <5 attributes — **worse than absent** (Rankeo: 41.6% vs 59.8%) |
| 2 | Correct @types for site type, 5+ attributes, but no sameAs or nested types |
| 3 | Complete schema: correct types + nested author/publisher + sameAs to 2+ platforms + 8+ attributes + dateModified |
| 4 | Rich entity graph: all from 3 + sameAs to Wikipedia/Wikidata + site-type bonus types + no duplicate singletons |

**P0 trigger:** Score 1 on a "Critical" site-type dimension → "Minimal schema actively hurts. Either complete it or remove it."

**Research basis:** Rankeo 50K study: generic schema 41.6% citation rate vs 59.8% for no schema. JSON-LD + entity pages: +29.6% RAG accuracy (arXiv, March 2026).

---

## Dimension 4: Content Citability

**Why it matters:** Princeton's GEO paper (KDD 2024) tested 9 optimization strategies. Adding citations: +40%. Statistics: +30–40%. Authoritative tone: +10–25%. Keyword stuffing: negative.

### Checks

1. **Passage length** — sample 3-5 content pages, measure average section length in words (optimal: 134–167)
2. **Front-loading** — is the key answer/claim in the first 30% of each page?
3. **Statistics density** — count numbers per 150-200 words
4. **Attribution patterns** — presence of "According to [Authority]" constructions
5. **Hedging** — flag "it seems," "may be," "possibly," "it's thought that"
6. **Section coherence** — can each H2/H3 stand alone without prior context? (iPullRank: "atomic semantic chunks" — the self-contained passage is the unit of AI retrieval)
7. **Heading hierarchy** — correct H1→H2→H3 nesting, no skipped levels

### Scoring

| Score | Criteria |
|-------|----------|
| 0 | Wall-of-text prose, no headings, no data points, no source citations |
| 1 | Headings present but sections not self-contained; no statistics or source citations |
| 2 | Answer-first on some pages; some statistics present; correct heading hierarchy |
| 3 | Self-contained passages (134–167 words avg); stats with source attribution; authoritative tone; key answer in first 30% |
| 4 | All above + definition blocks + comparison tables + numbered lists + "According to [Source]" attributions + quotable pull-quotes |

**Research basis:** 44.2% of ChatGPT citations from first 30% of content (gtm-engineer-skills). Optimal passage: 134–167 words (claude-seo). Yext 6.8M analysis: 44% of AI citations from pages with clear heading hierarchy. Perplexity treats "sections and spans as first-class units."

---

## Dimension 5: Technical SEO Foundation

**Why it matters:** Lily Ray (Mar 2026): "Strong SEO is a prerequisite for GEO, not an alternative." RAG requires traditional crawl + index. GEO tactics that damage SEO are self-defeating.

### Checks

1. `noindex` directives — unintended pages blocked from indexing
2. Canonical URLs — present, consistent, no conflicts
3. Sitemap — exists, submitted to search consoles
4. Meta titles — present, unique per page, <60 chars
5. Meta descriptions — present, unique, 120-160 chars
6. Semantic HTML — proper heading hierarchy, landmark elements
7. Mobile-friendly — viewport meta, responsive design
8. Core Web Vitals — LCP, FID/INP, CLS
9. Internal linking — 5+ internal links per page
10. Image alt text — coverage percentage
11. Open Graph — og:title, og:description, og:image, twitter:card

### Scoring

| Score | Criteria |
|-------|----------|
| 0 | Critical crawl issues: unintended noindex on main pages, broken/missing canonicals, no sitemap (P0) |
| 1 | Indexable but: slow (>3s LCP), no meta descriptions, or broken internal links |
| 2 | Core pages have: titles, meta descriptions, canonical URLs, sitemap present |
| 3 | All above + semantic HTML (proper headings, landmarks) + mobile-friendly + correct heading hierarchy |
| 4 | All above + <1s LCP + 5+ internal links/page + >80% image alt coverage + complete Open Graph |

**P0 trigger:** Score 0-1 → "Fix SEO foundation before pursuing GEO. RAG requires crawl + index."

---

## Dimension 6: Entity & Brand Signals

**Why it matters:** Ahrefs 75K-brand study (Dec 2025): unlinked mentions correlate 0.664 with AI visibility; backlinks only 0.218. YouTube brand mentions: 0.737 (strongest single factor).

### Checks

1. Organization schema — present with 8+ attributes
2. Person schema — for author/founder (if applicable)
3. sameAs links — to social profiles, Wikipedia, Wikidata
4. Brand name consistency — same name across schema, meta, content, social profiles
5. NAP consistency — Name, Address, Phone (for local businesses)
6. External entity references — Wikipedia page, Wikidata entry, Google Knowledge Panel
7. Video/YouTube presence — brand YouTube channel linked

### Scoring

| Score | Criteria |
|-------|----------|
| 0 | No entity signals: no Organization schema, inconsistent brand naming across pages |
| 1 | Organization schema present but no sameAs, no external entity references |
| 2 | Organization + sameAs to 2+ social platforms; consistent brand name across site |
| 3 | All above + Wikipedia or Wikidata link + author Person schema + NAP consistency (if local) |
| 4 | All above + earned media presence documented + YouTube channel linked + 5+ platform consistency |

---

## Dimension 7: Multi-Engine Readiness

**Why it matters:** Only 11% domain overlap between Perplexity and ChatGPT (U of Toronto, 118K answers). Optimizing for one engine misses the others.

### Checks

1. **Google AIO** — strong traditional SEO + structured data + entity signals
2. **Perplexity** — freshness signals (dateModified <3 months), section-level coherence, PerplexityBot allowed
3. **ChatGPT** — front-loaded answers, OAI-SearchBot + ChatGPT-User allowed, earned media references
4. **Bing Copilot** — IndexNow integration, Bing Webmaster registration
5. **Freshness signals** — dateModified on content pages, recent content publication dates

### Scoring

| Score | Criteria |
|-------|----------|
| 0 | No engine-specific considerations; content stale (>6 months without updates) |
| 1 | Optimized for Google only (traditional SEO signals, no AI-specific work) |
| 2 | Google AIO awareness + one other engine (Perplexity freshness OR ChatGPT front-loading) |
| 3 | Google AIO + Perplexity (freshness + section coherence) + ChatGPT (front-loading + earned media); dateModified present |
| 4 | All engines: Perplexity freshness gates + ChatGPT earned media + Google AIO fan-out + Bing IndexNow configured |

**Research basis:** SE Ranking: content <3 months gets ~6 citations avg vs 3.9 for 2+ years. Perplexity's binary pipeline makes freshness a hard gate.

---

## Site-Type Scoring Weights

"Critical" dimensions with scores ≤1 always generate P0 findings regardless of total score.

| Dimension | Ecommerce | SaaS | Content | Local | Docs | Personal |
|-----------|-----------|------|---------|-------|------|----------|
| 1. Crawler Access | High | High | High | Med | High | Low |
| 2. Discovery | Med | High | Med | Low | **Critical** | Low |
| 3. Structured Data | **Critical** | High | High | **Critical** | Med | Med |
| 4. Citability | Med | High | **Critical** | Med | **Critical** | Med |
| 5. Technical SEO | High | High | Med | Med | High | Low |
| 6. Entity & Brand | High | **Critical** | High | **Critical** | Low | **Critical** |
| 7. Multi-Engine | High | High | High | Med | Med | Low |

---

## Score Bands

| Total (0–28) | Rating | Interpretation |
|--------------|--------|----------------|
| 24–28 | **Excellent** | AI-search ready. Competitive advantage in citation rates. |
| 18–23 | **Good** | Solid foundation. Targeted improvements in weak dimensions yield measurable gains. |
| 12–17 | **Foundation** | Significant gaps. Prioritized remediation on P0/P1 findings needed. |
| 0–11 | **Critical** | Not viable for AI search. Fundamental infrastructure and content work required. |
