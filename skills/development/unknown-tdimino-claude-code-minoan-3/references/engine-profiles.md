# AI Search Engine Profiles

Per-engine optimization profiles. Only 11% domain overlap between Perplexity and ChatGPT (U of Toronto, 118K answers) — engine-specific optimization is structurally required.

---

## Google AI Overviews

**Architecture:** Fan-out from existing Googlebot index. AIO generates answers from already-indexed content using traditional ranking signals + AI synthesis.

**Key characteristics:**
- Appears in ~50% of Google searches (McKinsey, Oct 2025)
- Builds on the existing Google index — traditional SEO signals heavily weighted
- Structured data matters more here than any other engine (it's Google)
- Entity resolution via Knowledge Graph, Wikipedia, Wikidata
- E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness) signals

**Optimization levers:**
| Lever | Impact | How to check |
|-------|--------|-------------|
| Complete JSON-LD schema | High | 8+ attributes per type, sameAs to Wikipedia |
| sameAs to Wikipedia/Wikidata | High | Organization/Person schema includes authoritative links |
| Strong traditional SEO | High | Core Web Vitals, meta tags, canonical, sitemap |
| FAQPage schema | High | 2.7x citation lift (Relixir 2025) |
| Heading hierarchy | Med | H1→H2→H3, no skipped levels |
| dateModified | Med | Present on content types |

**What differentiates it:** Most traditional-SEO-dependent. If traditional SEO is broken, this engine ignores the site entirely.

---

## Google AI Mode

**Architecture:** Gemini 3-powered conversational search (launched Jan 2026). Separate surface from AI Overviews — deeper multi-step reasoning, longer-form answers, different citation behavior.

**Key differences from AI Overviews:**
- Multi-step reasoning with follow-up questions
- Longer-form responses with more granular citations
- Can synthesize across more sources per answer
- More likely to cite specific passages (section-level extraction, similar to Perplexity)
- Accessible via explicit "AI Mode" toggle, not triggered automatically like AIO

**Key characteristics:**
- Builds on Googlebot index (same crawl infrastructure as AIO)
- Structured data and entity signals still critical (it's still Google)
- Favors content with clear section structure due to passage-level extraction
- Follow-up questions mean deeper page exploration — content depth matters more than in AIO

**Optimization levers:**
| Lever | Impact | How to check |
|-------|--------|-------------|
| Complete JSON-LD schema | High | Same as AIO — 8+ attributes, sameAs |
| Entity signals (sameAs, Wikipedia) | **Critical** | Organization/Person schema with authoritative links |
| Section-level coherence | **Critical** | Each H2/H3 independently intelligible (like Perplexity) |
| Content depth | High | Comprehensive coverage of subtopics |
| Strong traditional SEO | High | Core Web Vitals, meta tags, canonical |
| Earned media mentions | High | External references, press, citations |
| Heading hierarchy | High | H1→H2→H3, no skipped levels |

**What differentiates it:** Passage-level extraction behavior is closer to Perplexity than AIO. Content that scores well for both Perplexity and AIO tends to score well in AI Mode.

---

## Perplexity

**Architecture:** Binary pass/fail pipeline. Not weighted scoring — each gate eliminates content that fails.

**5-stage pipeline:**
1. **Freshness gate** — stale content excluded regardless of quality
2. **Semantic relevance** — embedding similarity with XGBoost L3 reranker
3. **Engagement threshold** — early engagement signals (social, linking patterns)
4. **Crawl access** — must be crawlable by PerplexityBot
5. **Citation selection** — ~10 pages retrieved per query, 3–4 cited (30–40% rate)

**Key characteristics:**
- Treats "individual sections and spans as first-class units"
- Section-level coherence matters, not just document-level
- Content <3 months: ~6 citations avg vs ~3.9 for 2+ years (SE Ranking)
- Freshness is a hard gate, not a soft signal

**Optimization levers:**
| Lever | Impact | How to check |
|-------|--------|-------------|
| dateModified <3 months | **Critical** | Present on all content pages |
| Self-contained sections | High | Each H2/H3 independently intelligible |
| PerplexityBot allowed | **Critical** | robots.txt User-agent: PerplexityBot Allow: / |
| 134–167 word passages | High | Average section length |
| Source attributions | High | "According to [Source]" patterns |
| Fresh publication dates | High | Regular content updates |

**Crawler caveat:** `Perplexity-User` (the user-triggered fetch bot) "generally ignores robots.txt" per Perplexity's own docs. Only `PerplexityBot` reliably respects `robots.txt`. To truly block Perplexity user-triggered fetches, use server-side User-Agent filtering.

**Sonar API (March 2026):** Perplexity's programmatic search API. Third-party applications can query Perplexity's index via Sonar, meaning your content may be cited in apps you've never heard of — not just perplexity.ai. Optimization for PerplexityBot covers Sonar consumers too, since they draw from the same index. For enterprise audits, note that Sonar API consumers may have different citation display behavior than perplexity.ai.

**What differentiates it:** Freshness is binary — pass or fail. Old content is invisible regardless of quality.

---

## ChatGPT Search

**Architecture:** Three separate crawlers feeding different systems. Search index built by OAI-SearchBot, real-time fetches by ChatGPT-User, training by GPTBot.

**Crawler split:**
| Crawler | Purpose | Block impact |
|---------|---------|-------------|
| GPTBot | Training only | None on search |
| OAI-SearchBot | Search index | Site disappears from ChatGPT Search |
| ChatGPT-User | Real-time page fetch | ChatGPT can't read the page when asked |

**Key characteristics:**
- "Systematic and overwhelming bias toward earned media" (U of Toronto)
- 44.2% of citations from first 30% of content (gtm-engineer-skills)
- Front-loading answers is critical
- Only 11% domain overlap with Perplexity — different optimization required

**Optimization levers:**
| Lever | Impact | How to check |
|-------|--------|-------------|
| OAI-SearchBot allowed | **Critical** | robots.txt check |
| ChatGPT-User allowed | High | robots.txt check (user-triggered fetch, not search-index) |
| Front-loaded answers | High | Key claim in first 30% of page |
| Earned media mentions | High | External mentions, press, citations |
| Authoritative tone | Med | No hedging, declarative claims |
| Statistics with sources | Med | Numbers per 150–200 words |

**What differentiates it:** Earned media bias is strongest here. On-page optimization alone can't overcome lack of external mentions.

---

## Bing Copilot

**Architecture:** Powered by Bing index. Microsoft's AI layer on top of traditional Bing search.

**Key characteristics:**
- IndexNow for instant indexing (Bing is primary IndexNow supporter)
- Bing Webmaster Tools for monitoring (includes AI Performance tab)
- Traditional Bing SEO signals apply
- Less studied than Google/Perplexity/ChatGPT, but growing

**Optimization levers:**
| Lever | Impact | How to check |
|-------|--------|-------------|
| IndexNow integration | High | API key file at root, POST endpoint configured |
| Bing Webmaster registration | High | Site verified in Bing Webmaster Tools |
| Structured data | Med | JSON-LD schema present |
| Sitemap submission | Med | Submitted via Bing Webmaster Tools |

**What differentiates it:** IndexNow provides instant notification of content changes — unique advantage over Google's crawl-based discovery.

---

## Cross-Engine Optimization Matrix

| Factor | Google AIO | Google AI Mode | Perplexity | ChatGPT | Bing Copilot |
|--------|-----------|---------------|------------|---------|--------------|
| Traditional SEO | **Critical** | **Critical** | Med | Med | High |
| Structured Data | **Critical** | **Critical** | Med | Med | Med |
| Freshness | Med | Med | **Critical** | Med | Med |
| Front-loading | Med | Med | Med | **Critical** | Med |
| Earned media | High | High | Med | **Critical** | Med |
| Section coherence | Med | **Critical** | **Critical** | Med | Low |
| Content depth | Med | High | Med | Med | Med |
| IndexNow | N/A | N/A | N/A | N/A | **Critical** |
| Entity signals | **Critical** | **Critical** | Low | High | Med |

**Universal requirements (all engines):**
1. Content must be server-rendered (SSR/SSG)
2. robots.txt must allow the engine's crawler
3. Schema must be complete (8+ attributes) or absent
4. Content must have clear heading hierarchy
