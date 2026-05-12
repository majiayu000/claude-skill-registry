# Research Foundation

Academic papers and practitioner sources grounding the GEO/SEO scoring rubric.

---

## Primary Academic Sources

### 1. Aggarwal et al. — "GEO: Generative Engine Optimization"
**Princeton / IIT Delhi, KDD 2024, arXiv:2311.09735**

Tested 9 optimization strategies on GEO-bench (10K queries across BrightData, Perplexity, You.com):

| Strategy | Effect on citation rate |
|----------|----------------------|
| Adding citations | **+40%** |
| Adding statistics | **+30–40%** |
| Authoritative tone | **+10–25%** |
| Fluency rewrites | Negligible |
| Keyword stuffing | **Negative** |

**Rubric impact:** Grounds Dimension 4 (Content Citability). Statistics, citations, and authoritative tone are empirically validated. Keyword stuffing is counterproductive.

### 2. Chen et al. — "How to Dominate AI Search"
**U of Toronto, Sep 2025, arXiv:2509.08919**

Analyzed 118K answers from multiple AI search engines:
- "Systematic and overwhelming bias toward earned media"
- Only **11% domain overlap** between Perplexity and ChatGPT
- Engine-specific optimization is structurally required

**Rubric impact:** Grounds Dimension 7 (Multi-Engine Readiness) and Dimension 6 (Entity & Brand Signals). No single optimization works across all engines.

### 3. Wu et al. — "AutoGEO"
**CMU, ICLR 2026, arXiv:2510.11438**

- RL-based content rewriting achieves **+50.99%** over Princeton GEO baseline
- Engine-specific AND domain-specific rules required
- Demonstrates that automated optimization can significantly outperform manual approaches

**Rubric impact:** Reinforces multi-engine and domain-specific scoring in Dimensions 4 and 7.

### 4. Presenc AI — Synthesis of 34 GEO Papers
**April 2026, presenc.ai/research/geo-academic-papers-2026**

Meta-analysis finding: structured data + explicit entity tagging produce "disproportionate citation lift" compared to content-only optimization.

**Rubric impact:** Elevates Dimension 3 (Structured Data) and Dimension 6 (Entity & Brand Signals) as top-priority dimensions.

### 5. "SAGEO Arena: Benchmarking GEO at Scale"
**Preprint, arXiv:2602.12187, Feb 2026**

Large-scale arena-style benchmark comparing GEO strategies across multiple engines. Introduces standardized evaluation methodology for cross-engine optimization effectiveness.

**Rubric impact:** Strengthens Dimension 7 (Multi-Engine Readiness) scoring methodology. Provides comparative baselines for engine-specific optimization.

### 6. "AgentGEO: Agent-Based Generative Engine Optimization"
**Preprint, arXiv:2603.09296, Mar 2026**

Autonomous agent framework for GEO that iteratively optimizes content through multi-step reasoning. Demonstrates that agentic approaches to content optimization outperform single-pass rewriting.

**Rubric impact:** Validates our multi-phase audit→generate→monitor workflow. Supports iterative optimization over one-shot fixes.

### 7. "AgenticGEO: Agentic Approaches to GEO"
**Preprint, arXiv:2603.20213, Mar 2026**

Extends the agentic paradigm with environment-aware optimization—agents that read site structure, competitor content, and engine behavior before rewriting. Closest academic analog to our skill's detect→audit→generate approach.

**Rubric impact:** Reinforces site-type-aware optimization (our Phase 1 detection). Supports the principle that context-aware optimization outperforms generic strategies.

### 8. "MAGEO: Multi-Agent GEO"
**Preprint, arXiv:2604.19516, Apr 2026**

Multi-agent system where specialized agents handle different optimization dimensions (structure, citations, entity signals) and coordinate via shared state. Achieves state-of-the-art across multiple engines simultaneously.

**Rubric impact:** Validates our 7-dimension decomposition as architecturally sound. Multi-agent coordination for multi-engine optimization mirrors our dimension-by-dimension scoring approach.

---

## Key Empirical Findings

| Finding | Source | Dimension Affected |
|---------|--------|-------------------|
| 73% of AI-cited pages have schema (vs 30% avg) | Rankeo, 50K AI responses | Dim 3: Structured Data |
| FAQPage schema: 2.7x citation lift | Relixir 2025 | Dim 3: Structured Data |
| Minimal/generic schema (41.6%) WORSE than none (59.8%) | Rankeo | Dim 3: Structured Data |
| Unlinked mentions correlate 0.664 with AI visibility; backlinks only 0.218 | Ahrefs, 75K brands | Dim 6: Entity & Brand Signals |
| YouTube brand mentions: 0.737 (strongest single factor) | Ahrefs Dec 2025 | Dim 6: Entity & Brand |
| Only 11% domain overlap: ChatGPT vs Perplexity | Qwairy / U of Toronto, 118K answers | Dim 7: Multi-Engine |
| Content <3 months: 6 citations avg vs 3.9 for 2+ years | SE Ranking | Dim 7: Multi-Engine (Perplexity) |
| 44.2% of ChatGPT citations from first 30% of content | gtm-engineer-skills analysis | Dim 4: Citability |
| Optimal citable passage: 134–167 words | claude-seo GEO sub-skill | Dim 4: Citability |
| AI crawlers don't execute JavaScript | Multiple sources | Dim 1: Crawler Access |
| 89% more AI crawl completeness with flat architecture | Aether Research 2026 | Dim 1: Crawler Access |
| llms.txt: no measurable citation improvement (300K domains) | SERanking Nov 2025 | Dim 2: Discovery |
| Pages with clear heading hierarchy: 44% of all AI citations | Yext, 6.8M citations | Dim 4: Citability |
| JSON-LD + agent-optimized entity pages: +29.6% RAG accuracy | arXiv, March 2026 | Dim 3: Structured Data |

---

## Practitioner Sources

| Expert | Affiliation | Key Insight | Rubric Impact |
|--------|-------------|-------------|---------------|
| Lily Ray | Amsive Digital | "Your GEO Strategy Might Be Destroying Your SEO" (Mar 2026). Strong SEO is prerequisite for GEO. FAQ bloat, thin answer pages damage traditional SEO. Also: March 2026 core update analysis shows first-party source authority increasingly dominant — original research, proprietary data, and first-party studies get disproportionate citation lift vs. aggregator/summary content. | Dim 5 as floor: score ≤1 triggers P0. Dim 4 and 6: first-party data as citation signal. |
| Mike King | iPullRank | "Relevance Engineering" (SMX Advanced 2025+). Entity-first content strategy. Key concepts: atomic semantic chunks (self-contained passages as the unit of AI retrieval), AI simulation testing (running queries against AI engines to test citation outcomes), citation monitoring KPIs (track citation rate, citation position, and query coverage as ongoing metrics). | Dim 4 (atomic chunks), Dim 6 (entity-first), Dim 7 (AI simulation) |
| Jeremy Howard | AnswerDotAI | llms.txt proposal (Sep 2024). Near-mainstream by Apr 2026. | Dim 2 scoring criteria |
| Perplexity Research | Perplexity AI | "Architecting an AI-First Search API" (Sep 2025). Binary pass/fail pipeline. | Dim 7 Perplexity profile |
| Google Search Central | Google | "AI Features and Your Website" (May 2025). Traditional signals still primary. | Dim 5 weight |
| McKinsey | McKinsey & Co | "New front door to the internet" (Oct 2025). $750B US revenue via AI search by 2028. | Overall urgency framing |
| Ahrefs Brand Radar | Ahrefs | 75K brands, Dec 2025. Mentions > links. YouTube strongest. | Dim 6 scoring thresholds |
| Yext | Yext | 6.8M AI citation analysis, 2025. Heading hierarchy in 44% of cited pages. | Dim 4 heading check |
| Aether Research | Independent | Site architecture for AI, 2026. Flat = 89% more completeness. | Dim 1 architecture check |
| SERanking | SE Ranking | 300K-domain llms.txt study, Nov 2025. No citation lift, but low cost. | Dim 2 llms.txt calibration |

---

## Perplexity's Published Architecture

Binary pass/fail pipeline (not weighted scoring like Google):

1. **Freshness gate** — content with stale timestamps excluded regardless of quality. Content <3 months: ~6 citations avg. Content >2 years: ~3.9 citations avg.
2. **Semantic relevance** — embedding similarity threshold. XGBoost L3 reranker for final scoring.
3. **Engagement threshold** — early engagement signals required (social sharing, linking patterns).
4. **Crawl access** — must be crawlable by PerplexityBot. Blocked = invisible.
5. **Citation selection** — ~10 pages retrieved per query, 3–4 cited (30–40% citation rate).

Treats "individual sections and spans as first-class units" — section-level coherence matters, not just document-level.

**Implications for scoring:**
- Dimension 1: PerplexityBot must be allowed
- Dimension 4: Each section must stand alone
- Dimension 7: dateModified is a hard gate, not a nice-to-have

---

## Emerging Standards (Monitor Only)

These are not yet scoring criteria but are worth tracking for future rubric updates.

| Standard | What It Is | Status (May 2026) | Scoring Impact |
|----------|-----------|-------------------|----------------|
| **ai.txt** | Proposed DSL for AI crawler permissions and content licensing. More granular than robots.txt for AI-specific directives. | Draft proposal, no production traction. No major engine honors it yet. | None — monitor only. May become relevant if Google or OpenAI adopt. |
| **agent.json** | JSON manifest for AI agent capabilities, permissions, and tool discovery. | Gaining traction in the agentic ecosystem. | None for citation SEO — this is `agentic-seo` territory (agent-to-site interaction, not human-via-AI search). |
| **RSL (Rights Signaling Language)** | Structured vocabulary for expressing content licensing terms to AI crawlers. | Early specification stage. | Indirect — may affect crawler behavior as engines begin respecting licensing signals. |
| **Cloudflare Content Signals** | Cloudflare's mechanism for site owners to signal AI usage preferences at the CDN level. | Available to Cloudflare customers. | Indirect — affects which crawlers can access content. Check in Dimension 1 as a CDN-level access control. |

---

## Source Reliability Weighting

| Tier | Examples | How to treat |
|------|----------|-------------|
| Peer-reviewed | KDD 2024, ICLR 2026 | Scoring thresholds directly derived |
| Preprint (not yet peer-reviewed) | SAGEO Arena, AgentGEO, AgenticGEO, MAGEO | Directional validation, not threshold-setting |
| Large-N empirical | Rankeo 50K, Ahrefs 75K, Yext 6.8M, U of Toronto 118K | Strong evidence for specific checks |
| Practitioner synthesis | Lily Ray, Mike King | Qualitative guidance, P0 triggers |
| Tool-derived | claude-seo, gtm-engineer-skills | Heuristic benchmarks, not hard limits |
| Vendor research | SERanking, Presenc AI | Directional only, possible bias |
