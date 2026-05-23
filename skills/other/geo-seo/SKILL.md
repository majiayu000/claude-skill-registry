---
name: geo-seo
description: >-
  Audits websites for AI search visibility (GEO/SEO) and generates
  deployable artifacts (llms.txt, schema JSON-LD, robots.txt). 7-dimension
  scorecard tailored by site type and size, grounded in Princeton KDD 2024,
  Toronto 2025, and ICLR 2026 research. This skill should be used when
  optimizing for ChatGPT, Perplexity, Google AI Overviews, or other AI
  search engines. Also triggered by queries about AI search optimization,
  generative engine optimization, llms.txt, AI crawler configuration,
  schema markup for AI, citation optimization, or Google AI Mode.
argument-hint: "[path] [--type=ecommerce|saas|content|local|docs|personal] [--size=small|medium|large|enterprise] [--mode=audit|generate|full|monitor]"
user-invocable: true
allowed-tools: Bash, Read, Glob, Grep, Write, Edit, Agent
---

# GEO/SEO: AI Search Visibility Audit & Artifact Generator

Audit a website for AI search visibility across 7 research-grounded dimensions, generate deployable artifacts (llms.txt, schema JSON-LD, robots.txt), and produce a prioritized action plan — all tailored to the site's type and scale.

**Complementary to `agentic-seo`**: This skill measures whether content gets cited when humans search via ChatGPT/Perplexity/Google AI Overviews. `agentic-seo` (run separately via `npx agentic-seo ./out`) measures whether AI agents can interact with the site (including `agent.json` manifests, skill discovery, permission systems). Run both for complete coverage.

## Arguments

Parse `` for:
- **path**: Project root to audit (default: current working directory)
- **--type**: Override auto-detected site type
- **--size**: Override auto-detected size tier
- **--mode**: `audit` (scorecard only), `generate` (artifacts only), `full` (both, default), `monitor` (compare to previous snapshot)

## Workflow

Execute these phases in order: Detect → Audit → Classify → Generate → Report → Cross-reference.

### Mode-to-Phase Mapping

| Mode | Detect | Audit | Classify | Generate | Report | Cross-ref |
|------|--------|-------|----------|----------|--------|-----------|
| `full` | Yes | Yes | Yes | Yes | Yes | Yes |
| `audit` | Yes | Yes | Yes | Skip | Yes | Yes |
| `generate` | Yes | Skip | Skip | Yes | Yes | Yes |
| `monitor` | Yes | Yes | Yes | Skip | Yes (diff) | Yes |

---

### Phase 1: Detect Site Profile

Auto-detect site type, size, and framework from codebase signals. Report findings before proceeding.

#### Site Type Detection

Examine the project for these signals (override with `--type`):

| Type | Detection Signals |
|------|------------------|
| **ecommerce** | Product schema, cart/checkout routes, Shopify/WooCommerce/Stripe markers, product listing templates |
| **saas** | Pricing page, docs section, API references, login/signup routes, dashboard templates |
| **content** | Blog templates, author pages, RSS feeds, high content-to-code ratio, CMS markers |
| **local** | LocalBusiness schema, address/map elements, service area pages, Google Maps embed |
| **docs** | Versioned docs structure, API reference, sidebar nav config, code blocks predominant |
| **personal** | Person schema, about page, project showcase, small page count (<20), portfolio layout |

```bash
# Detection heuristics — run these checks
grep -rl "Product\|AggregateOffer\|AddToCart\|checkout" --include="*.{tsx,jsx,html,json}" . 2>/dev/null | head -5
grep -rl "LocalBusiness\|GeoCoordinates\|serviceArea" --include="*.{tsx,jsx,html,json}" . 2>/dev/null | head -5
find . -path "*/docs/*" -name "*.md" 2>/dev/null | wc -l
find . -path "*/blog/*" -o -path "*/posts/*" 2>/dev/null | wc -l
ls pricing* docs/ api/ blog/ 2>/dev/null
```

#### Site Size Detection

Count indexable pages:

```bash
# For static sites with build output
find ./out ./dist ./build ./_site -name "*.html" 2>/dev/null | wc -l

# For dynamic sites, count route definitions
grep -r "path:\|route\|getStaticPaths\|generateStaticParams" --include="*.{ts,tsx,js,jsx}" . 2>/dev/null | wc -l

# For content sites, count content files
find . -name "*.md" -o -name "*.mdx" 2>/dev/null | grep -v node_modules | wc -l
```

| Tier | Pages | Approach |
|------|-------|----------|
| **small** | <50 | Manual audit, essential artifacts only, quick wins |
| **medium** | 50–500 | Selective optimization, programmatic schema for templates |
| **large** | 500+ | Template-based fixes, automated pattern detection |
| **enterprise** | 10K+ | Governance focus, CI/CD integration, sampling audit |

#### Framework Detection

```bash
# Check package.json, config files
cat package.json 2>/dev/null | grep -E '"(next|gatsby|nuxt|astro|svelte|remix|vite|hugo|jekyll)"'
ls next.config.* nuxt.config.* astro.config.* svelte.config.* gatsby-config.* vite.config.* 2>/dev/null
cat package.json 2>/dev/null | grep -E '"(react|vue|angular|svelte)"'
```

**Report format:**
```
Site Profile: [type] | [size] tier ([N] pages) | [framework]
```

---

### Phase 2: Audit — 7-Dimension Scoring

Score each dimension 0–4. The inline tables below are quick-reference summaries. Load `references/scoring-rubric.md` for the authoritative rubric with research citations and detailed check procedures — the reference version takes precedence when they differ.

#### Dimension 1: AI Crawler Access (0–4)

Check `robots.txt` for the 9 critical AI crawlers. Distinguish training bots (safe to block) from search/retrieval bots (blocking = invisible to AI search).

**Crawlers to check (three tiers):** See `references/ai-crawlers.md` for the full registry.

**Search-critical (blocking loses AI search):** OAI-SearchBot, PerplexityBot, Claude-SearchBot, Bingbot, Googlebot, Bravebot, YouBot.

**User-triggered fetch (recommended to allow, not search-critical):** ChatGPT-User, Perplexity-User, Claude-User.

**Training-only (safe to block):** GPTBot, ClaudeBot, Google-Extended, CCBot, Bytespider, Amazonbot, Diffbot, Applebot-Extended.

```bash
# Check robots.txt
cat robots.txt public/robots.txt static/robots.txt 2>/dev/null

# Check for CDN bot blocking (Cloudflare Bot Fight Mode, Vercel firewall)
grep -ri "bot.*fight\|bot.*manage\|firewall" wrangler.toml vercel.json netlify.toml _headers 2>/dev/null
```

**P0 check — JavaScript-only rendering:** AI crawlers do not execute JavaScript. If the site is client-side rendered (CSR/SPA) without SSR/SSG, flag as P0.

```bash
# Check for SSR/SSG configuration
grep -r "getServerSideProps\|getStaticProps\|generateStaticParams\|output.*export\|prerender\|ssr" --include="*.{ts,tsx,js,jsx,mjs}" . 2>/dev/null | head -5
```

| Score | Criteria |
|-------|----------|
| 0 | Search-critical bots blocked, OR CDN bot blocking, OR JS-only rendering (P0) |
| 1 | Some search bots allowed but OAI-SearchBot or PerplexityBot blocked |
| 2 | All search-critical bots allowed but user-triggered fetch bots blocked |
| 3 | All search-critical + user-triggered fetch bots allowed, no CDN blocking |
| 4 | All bots allowed + IndexNow configured + <500ms bot response |

#### Dimension 2: AI Discovery Infrastructure (0–4)

Check for llms.txt, sitemap, RSS/Atom feeds. Load `references/llms-txt-spec.md` for validation rules.

```bash
# Check for discovery files
ls public/llms.txt public/llms-full.txt llms.txt llms-full.txt 2>/dev/null
ls public/sitemap.xml sitemap.xml out/sitemap.xml 2>/dev/null
grep -r "application/rss\|application/atom\|feed\.xml\|rss\.xml" --include="*.{tsx,jsx,html,xml}" . 2>/dev/null | head -3
```

**llms.txt validation (if present):**
- Single H1 title (required)
- Blockquote summary after H1
- H2 sections with Markdown link lists in `[name](url): description` format
- `## Optional` section for lower-priority content

| Score | Criteria |
|-------|----------|
| 0 | No llms.txt, no AI-specific discovery files |
| 1 | llms.txt present but minimal (just H1) |
| 2 | llms.txt with H1 + blockquote + sections; OR sitemap with lastmod |
| 3 | Well-structured llms.txt + `## Optional`; sitemap with lastmod; RSS/Atom |
| 4 | llms.txt + llms-full.txt + sitemap + RSS + comprehensive coverage |

#### Dimension 3: Structured Data Quality (0–4)

Check JSON-LD structured data completeness. Load `references/schema-patterns.md` for site-type-specific requirements.

```bash
# Find all JSON-LD
grep -rl "application/ld+json" --include="*.{tsx,jsx,html}" . 2>/dev/null
grep -r "@type" --include="*.{tsx,jsx,html}" . 2>/dev/null | grep -o '"@type"[^,]*' | sort -u
```

**Rankeo finding: Minimal/generic schema (41.6% citation rate) performs WORSE than no schema (59.8%).** Only award points for complete, attribute-rich schema.

**Required @types by site type:**

| Type | Required | Bonus |
|------|----------|-------|
| ecommerce | Product, Organization, BreadcrumbList | AggregateRating, Review, Offer |
| saas | Organization, SoftwareApplication, FAQPage | HowTo, Article |
| content | Article, Organization, Person | NewsArticle, BlogPosting, LiveBlogPosting |
| local | LocalBusiness, Organization | Review, GeoCoordinates, OpeningHoursSpecification |
| docs | TechArticle, Organization | HowTo, SoftwareSourceCode |
| personal | Person, Organization | CreativeWork, Article |

| Score | Criteria |
|-------|----------|
| 0 | No JSON-LD structured data |
| 1 | Generic schema, <5 attributes — WORSE than absent |
| 2 | Correct @types for site type, 5+ attributes, but no sameAs or nesting |
| 3 | Complete schema with nested types, sameAs, 8+ attributes |
| 4 | Rich entity graph: Organization+Person+sameAs+(Wikipedia/Wikidata) + site-type-specific types |

**P0 check:** Duplicate singleton @types on same page (e.g., two FAQPage) — silently dropped by Google.

#### Dimension 4: Content Citability (0–4)

Evaluate content structure, passage length, front-loading, statistics density, and attribution patterns. This dimension requires reading actual content pages.

```bash
# Sample 3-5 content-heavy pages for analysis
find . -name "*.tsx" -o -name "*.jsx" -o -name "*.html" -o -name "*.md" 2>/dev/null | grep -v node_modules | grep -iE "about|blog|post|article|page|index" | head -5
```

**Research-grounded checks:**
- **Passage length**: 134–167 words optimal for AI extraction
- **Front-loading**: Key answer in first 30% of content (44.2% of ChatGPT citations come from there)
- **Statistics density**: Numbers per 150–200 words
- **Attribution patterns**: "According to [Authority]" — mimics what LLMs recognize from training
- **Declarative tone**: No hedging ("it seems," "may be") — declarative claims outperform
- **Section coherence**: Each H2/H3 section independently intelligible (Perplexity treats sections as first-class units)
- **Heading hierarchy**: Clear, semantic heading structure (44% of all AI citations from pages with clear hierarchy, per Yext 6.8M citation analysis)

| Score | Criteria |
|-------|----------|
| 0 | Wall-of-text prose, no headings, no data, no sources |
| 1 | Headings present but sections not self-contained; no statistics |
| 2 | Answer-first on some pages; some statistics; correct hierarchy |
| 3 | Self-contained passages; stats with sources; authoritative tone; front-loaded |
| 4 | All above + definition blocks, comparison tables, numbered lists, source attributions, quotable pull-quotes |

#### Dimension 5: Technical SEO Foundation (0–4)

Lily Ray's constraint: if SEO foundation is broken (score 0–1), flag P0 "Fix SEO before pursuing GEO." RAG requires crawl + index.

```bash
# Check meta tags, canonical, sitemap
grep -r "noindex" --include="*.{tsx,jsx,html}" . 2>/dev/null | grep -v node_modules | head -5
grep -r "canonical\|metadataBase" --include="*.{tsx,jsx,ts}" . 2>/dev/null | head -5
grep -r "<title\|metadata.*title\|Head.*title" --include="*.{tsx,jsx,ts}" . 2>/dev/null | head -5
grep -r "description\|meta.*description" --include="*.{tsx,jsx,ts}" . 2>/dev/null | head -5

# Check for Open Graph
grep -r "og:title\|openGraph\|twitter:card" --include="*.{tsx,jsx,ts,html}" . 2>/dev/null | head -5
```

| Score | Criteria |
|-------|----------|
| 0 | Critical crawl issues: unintended noindex, broken canonicals, no sitemap |
| 1 | Indexable but slow, no meta descriptions, broken links |
| 2 | Core pages have titles, meta descriptions, canonical URLs, sitemap |
| 3 | All above + semantic HTML, mobile-friendly, heading hierarchy |
| 4 | All above + fast LCP, 5+ internal links/page, image alt coverage, Open Graph complete |

#### Dimension 6: Entity & Brand Signals (0–4)

Ahrefs 75K-brand study: unlinked mentions correlate 0.664 with AI visibility; backlinks only 0.218. YouTube mentions strongest single factor (0.737).

```bash
# Check Organization/Person schema with sameAs
grep -r "sameAs\|Organization\|Person" --include="*.{tsx,jsx,ts,json}" . 2>/dev/null | head -10

# Check for consistent brand naming
grep -r "publisher\|author\|brand\|organizationName" --include="*.{tsx,jsx,ts,json}" . 2>/dev/null | head -5
```

| Score | Criteria |
|-------|----------|
| 0 | No entity signals, no Organization schema |
| 1 | Organization schema but no sameAs, no external references |
| 2 | Organization + sameAs to 2+ platforms; consistent brand name |
| 3 | All above + Wikipedia/Wikidata; author Person schema; consistent NAP |
| 4 | All above + earned media presence; YouTube; 5+ platform consistency |

#### Dimension 7: Multi-Engine Readiness (0–4)

Only 11% domain overlap between Perplexity and ChatGPT (U of Toronto). Engine-specific optimization is structurally required. Load `references/engine-profiles.md` for per-engine profiles.

```bash
# Check for engine-specific signals
grep -r "IndexNow\|indexnow" --include="*.{json,xml,ts,js}" . 2>/dev/null
grep -r "dateModified\|datePublished\|lastmod" --include="*.{tsx,jsx,ts,json,xml}" . 2>/dev/null | head -5
```

| Score | Criteria |
|-------|----------|
| 0 | No engine-specific considerations |
| 1 | Optimized for Google only |
| 2 | Google AIO + one other (Perplexity or ChatGPT) |
| 3 | Google AIO + Perplexity + ChatGPT; freshness signals; earned media references |
| 4 | All engines + Perplexity freshness gates + ChatGPT earned media + Google AIO fan-out + Bing IndexNow |

#### Site-Type Scoring Weights

Apply weight modifiers when interpreting scores. "Critical" dimensions with low scores warrant P0 findings.

| Dimension | Ecommerce | SaaS | Content | Local | Docs | Personal |
|-----------|-----------|------|---------|-------|------|----------|
| Crawler Access | High | High | High | Med | High | Low |
| Discovery | Med | High | Med | Low | **Critical** | Low |
| Structured Data | **Critical** | High | High | **Critical** | Med | Med |
| Citability | Med | High | **Critical** | Med | **Critical** | Med |
| Technical SEO | High | High | Med | Med | High | Low |
| Entity & Brand | High | **Critical** | High | **Critical** | Low | **Critical** |
| Multi-Engine | High | High | High | Med | Med | Low |

#### Score Bands

| Total (0–28) | Rating | Meaning |
|--------------|--------|---------|
| 24–28 | **Excellent** | AI-search ready; competitive advantage |
| 18–23 | **Good** | Solid foundation; targeted improvements yield gains |
| 12–17 | **Foundation** | Significant gaps; prioritized remediation needed |
| 0–11 | **Critical** | Not viable for AI search; fundamental work required |

---

### Phase 3: Classify Findings

Assign severity levels to each finding based on dimension scores and site-type weights:

| Severity | Criteria |
|----------|----------|
| **P0 — Critical** | Blocks AI search visibility entirely. CSR-only rendering, search bots blocked, SEO foundation broken (Dim 5 score 0–1). |
| **P1 — High** | Significant impact on citation rate. Missing schema for a "Critical" dimension, no llms.txt, no sameAs. |
| **P2 — Medium** | Optimization opportunity. Incomplete schema, weak citability, missing llms-full.txt. |
| **P3 — Low** | Informational. IndexNow not configured, minor content improvements, missing RSS. |

---

### Phase 4: Generate Artifacts

Skip this phase in `audit` mode. In `generate` or `full` mode, produce the artifacts below.

#### 4a. llms.txt

Generate `llms.txt` following Jeremy Howard's spec (AnswerDotAI, Sep 2024). Load `references/llms-txt-spec.md` for format details.

1. Detect site name from package.json, Organization schema, or site config
2. Write summary from homepage meta description or first content paragraph
3. Categorize pages by type (docs, blog, product, about, API)
4. Prioritize by internal link count and content depth
5. Mark lower-priority pages under `## Optional`

Load `assets/templates/llms-txt/` for site-type starter templates.

If `llms.txt` already exists, audit it against the spec instead of overwriting. Report improvements.

#### 4b. Schema JSON-LD

Generate complete, attribute-rich JSON-LD for the detected site type. Load `references/schema-patterns.md` for patterns and `assets/templates/schema/` for starters.

- Detect existing schema and identify gaps
- Generate schema with 8+ attributes per type (per Rankeo: completeness > presence)
- Include `sameAs` links to known entity references
- Use site-type-specific @types from the rubric
- Validate: no duplicate singleton types per page

If schema already exists, report what's missing rather than overwriting.

#### 4c. robots.txt AI Crawler Directives

Generate directives separating training bots from search bots. Load `references/ai-crawlers.md` for the full registry.

```
# AI Search Crawlers — allow for AI search visibility
User-agent: OAI-SearchBot
Allow: /

User-agent: PerplexityBot
Allow: /

# User-triggered fetch — recommended to allow
User-agent: ChatGPT-User
Allow: /

# AI Training Crawlers — block to protect content
User-agent: GPTBot
Disallow: /

User-agent: CCBot
Disallow: /
```

The inline example above is a minimal subset. Load `assets/templates/robots-ai-block.txt` for the complete template covering all search, fetch, and training crawlers.

If robots.txt already exists, check for conflicts and report them. Do not overwrite without confirmation.

---

### Phase 5: Report

Load `references/research-basis.md` when populating the Research Citations section with specific paper references supporting key findings.

Produce the audit report in this format:

```markdown
## GEO/SEO Audit Report

### Site Profile
- **Type:** [detected/override] | **Size:** [tier] ([N] pages) | **Framework:** [detected]
- **Score:** [X/28] — [Rating]
- **Complementary:** Run `npx agentic-seo ./out` for agent readability scoring

### Scorecard
| # | Dimension | Score | Key Finding |
|---|-----------|-------|-------------|
| 1 | AI Crawler Access | X/4 | ... |
| 2 | AI Discovery Infrastructure | X/4 | ... |
| 3 | Structured Data Quality | X/4 | ... |
| 4 | Content Citability | X/4 | ... |
| 5 | Technical SEO Foundation | X/4 | ... |
| 6 | Entity & Brand Signals | X/4 | ... |
| 7 | Multi-Engine Readiness | X/4 | ... |
| | **Total** | **X/28** | |

### Findings

#### P0 — Critical (blocks AI search visibility)
[findings or "None"]

#### P1 — High (significant citation impact)
[findings]

#### P2 — Medium (optimization opportunity)
[findings]

#### P3 — Low / Informational
[findings]

### Positive Findings
[what's already working well]

### Generated Artifacts
[paths to generated files, if any]

### Recommended Actions (prioritized)
1. [highest impact action]
2. ...

### Research Citations
[cite specific papers/studies supporting key findings]
```

---

### Phase 6: Cross-Reference

After the report, suggest complementary tools:
- `npx agentic-seo ./out` — agent readability (run after build)
- `/design-audit` — visual/UX quality (if available)
- Google Rich Results Test — validate generated JSON-LD
- llm-txt-validator.vercel.app — validate llms.txt

---

## Monitor Mode

When `--mode=monitor`:

1. Look for `.geo-seo-snapshot.json` in the project root
2. If found, run full audit and compare scores dimension-by-dimension
3. Report improvements, regressions, and unchanged dimensions
4. Save new snapshot

If no previous snapshot exists, run full audit and save the first snapshot. Save snapshots to `.geo-seo-snapshot.json` in the project root.

**Snapshot format:**
```json
{
  "date": "2026-05-12",
  "score": 22,
  "dimensions": {
    "crawler_access": 4,
    "discovery": 3,
    "structured_data": 3,
    "citability": 3,
    "technical_seo": 3,
    "entity_brand": 3,
    "multi_engine": 3
  },
  "site_type": "content",
  "site_size": "medium",
  "finding_count": { "p0": 0, "p1": 2, "p2": 4, "p3": 3 }
}
```

---

## Gotchas

Failure modes that produce wrong results without this section. Each represents a common mistake in AI search optimization.

1. **"Add FAQs everywhere"** — FAQ bloat damages traditional SEO, which undermines GEO (Lily Ray, Mar 2026). FAQPage schema lifts citations 2.7x, but filling pages with 50 thin Q&As hurts the overall SEO foundation. Score FAQPage schema appropriately but do not recommend FAQ content universally.

2. **Minimal schema worse than none** — 41.6% citation rate for generic schema vs 59.8% for no schema (Rankeo). An Organization with just `name` and `url` actively hurts. Enforce the 8+ attribute completeness threshold. When existing schema is too thin, recommend removing it or completing it — not leaving it as-is.

3. **All AI engines treated the same** — Only 11% domain overlap between Perplexity and ChatGPT (U of Toronto, 118K answers). Perplexity has a freshness hard gate; ChatGPT has earned media bias; Google AIO leans on traditional SEO signals. Provide engine-specific analysis, not generic "optimize for AI search."

4. **Ignoring earned media** — On-page optimization alone cannot overcome the systematic earned media bias that ChatGPT and Google show. Entity & Brand dimension exists to surface this gap. Do not promise citation improvements from on-page work alone when the site has no external mentions.

5. **CSR/SPA invisible to AI** — AI crawlers do not execute JavaScript. A React SPA with no SSR/SSG is completely invisible. Check rendering mode as the very first thing — all other optimization is pointless if the content can't be crawled.

6. **Silent CDN blocking** — Cloudflare Bot Fight Mode blocks AI crawlers without any robots.txt evidence. Check for CDN-level blocking, not just robots.txt directives.

7. **GEO without SEO foundation** — RAG requires crawl + index. If traditional SEO is broken (no sitemap, noindex on main pages, broken canonicals), no GEO optimization will help. Technical SEO Foundation score 0–1 is always P0.

8. **robots.txt training/search confusion** — Most sites only reference `GPTBot`, which is training-only. Blocking GPTBot doesn't lose search. Blocking `OAI-SearchBot` does. Always surface the training vs search distinction — most site owners don't know OpenAI has 3 separate crawlers.

9. **dateModified as decoration** — Setting dateModified to today's date without changing content is a freshness signal lie. Perplexity will eventually detect and penalize this. Only recommend updating dateModified when content actually changes.

10. **Overwriting existing artifacts** — When llms.txt or robots.txt already exists, audit and suggest improvements. Do not generate a replacement and overwrite without explicit confirmation. The site owner may have intentional customizations.

11. **Perplexity-User ignores robots.txt** — Per Perplexity's own documentation, `Perplexity-User` "generally ignores robots.txt" directives. A `Disallow` rule for this bot gives false confidence — the site owner thinks they've blocked user-triggered fetches but they haven't. When auditing, flag this distinction: only `PerplexityBot` reliably respects robots.txt. Server-side User-Agent filtering is the only reliable block for Perplexity-User.

12. **Zero-click outcomes are structural** — AI search optimization may increase citation frequency while decreasing click-through traffic. This is not a failure of optimization — it is the structural reality of AI-mediated search (Rand Fishkin, SparkToro). Set realistic expectations: GEO success means brand visibility and authority in AI answers, not necessarily more website visits. For sites that depend on direct traffic, note that citation ≠ click.

---

## Reference Documents

Load these on-demand when deeper context is needed:

| File | When to load |
|------|-------------|
| `references/scoring-rubric.md` | Full scoring criteria with research citations for each threshold |
| `references/schema-patterns.md` | JSON-LD patterns and examples by site type |
| `references/ai-crawlers.md` | Complete AI crawler registry with training vs search classification |
| `references/research-basis.md` | Academic paper summaries and key empirical findings |
| `references/llms-txt-spec.md` | llms.txt format specification and best practices |
| `references/engine-profiles.md` | Per-engine optimization profiles (Google AIO, Google AI Mode, Perplexity, ChatGPT, Bing) |

## Asset Templates

| Directory | Contents |
|-----------|----------|
| `assets/templates/llms-txt/` | Starter llms.txt templates by site type |
| `assets/templates/schema/` | JSON-LD starter templates for all 6 site types |
