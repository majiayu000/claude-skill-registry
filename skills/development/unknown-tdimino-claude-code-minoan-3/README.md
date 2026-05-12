# geo-seo

AI search visibility audit and artifact generator for Claude Code. 7-dimension scorecard, deployable artifacts, tailored by site type and scale.

## Origin Story

The author started his career as an SEO copywriter—writing meta descriptions, title tags, and keyword-optimized landing pages before "content marketing" had a name. A decade later, having crossed through microbiology, UX, enterprise AI, and cognitive agent architecture, the circle closes: the same discipline that once meant "put the keyword in the H1" now requires understanding retrieval-augmented generation pipelines, multi-engine citation behavior, and structured data at the entity graph level. This skill is that full circle—SEO reborn as GEO, built by someone who remembers what `<meta name="keywords">` used to do.

## What It Does

Reads a project's actual codebase and produces:

1. **Diagnostic scorecard** — 7 dimensions scored 0–4, grounded in peer-reviewed research (Princeton KDD 2024, CMU ICLR 2026, U of Toronto 2025)
2. **Deployable artifacts** — `llms.txt`, JSON-LD schema markup, `robots.txt` AI crawler directives
3. **Prioritized action plan** — P0–P3 findings with research citations

Everything is tailored to the site's type (ecommerce, SaaS, content, local, docs, personal) and scale (small → enterprise).

## The 7 Dimensions

| # | Dimension | What It Measures |
|---|-----------|-----------------|
| 1 | AI Crawler Access | Can AI search engines reach your content? (robots.txt, CDN blocking, rendering mode) |
| 2 | AI Discovery Infrastructure | llms.txt, sitemap, RSS — how AI engines find your pages |
| 3 | Structured Data Quality | JSON-LD schema completeness (minimal schema is *worse* than none) |
| 4 | Content Citability | Passage structure, front-loading, statistics, attribution patterns |
| 5 | Technical SEO Foundation | The floor — if traditional SEO is broken, GEO can't help |
| 6 | Entity & Brand Signals | Schema entity graph, sameAs links, earned media presence |
| 7 | Multi-Engine Readiness | Engine-specific optimization (only 11% domain overlap between Perplexity and ChatGPT) |

## Usage

```
/geo-seo                              # Full audit + generate + report
/geo-seo audit                        # Scorecard only, no artifacts
/geo-seo generate                     # Artifacts only, no scoring
/geo-seo monitor                      # Compare against previous snapshot
/geo-seo --type=saas --size=medium    # Override auto-detection
```

## Score Bands

| Score | Rating | Meaning |
|-------|--------|---------|
| 24–28 | Excellent | AI-search ready — competitive advantage in citation rates |
| 18–23 | Good | Solid foundation — targeted improvements yield measurable gains |
| 12–17 | Foundation | Significant gaps — prioritized remediation needed |
| 0–11 | Critical | Not viable for AI search — fundamental work required |

## Key Research Findings

The scoring rubric is grounded in specific empirical data, not opinion:

- **+40% citation rate** from adding citations to content (Princeton KDD 2024, 10K queries)
- **73% of AI-cited pages** have structured data vs 30% average (Rankeo, 50K responses)
- **41.6% citation rate** for minimal schema vs **59.8% for no schema** — half-done hurts (Rankeo)
- **0.664 correlation** between unlinked mentions and AI visibility; backlinks only 0.218 (Ahrefs, 75K brands)
- **Only 11% domain overlap** between Perplexity and ChatGPT results (U of Toronto, 118K answers)
- **Content <3 months old**: ~6 citations avg vs ~3.9 for 2+ years — freshness is a hard gate on Perplexity

## Crawler Classification

The skill distinguishes three tiers of AI crawlers — most sites get this wrong:

| Tier | Crawlers | What Blocking Does |
|------|----------|-------------------|
| **Search-critical** | OAI-SearchBot, PerplexityBot, Claude-SearchBot, Bingbot, Googlebot, Bravebot, YouBot | Removes site from that engine's AI search |
| **User-triggered fetch** | ChatGPT-User, Perplexity-User, Claude-User | Prevents live page reads but doesn't affect search index |
| **Training-only** | GPTBot, ClaudeBot, Google-Extended, CCBot, Bytespider, Applebot-Extended | No effect on search visibility |

Most robots.txt files only know `GPTBot`. OpenAI now has three crawlers — blocking `GPTBot` does nothing to search visibility, but blocking `OAI-SearchBot` makes the site invisible to ChatGPT Search.

## Complementary Tools

- **`agentic-seo`** (`npx agentic-seo ./out`) — measures agent-to-site interaction readability. Different concern from citation visibility. Run both.
- **Google Rich Results Test** — validate generated JSON-LD
- **llm-txt-validator.vercel.app** — validate generated llms.txt

## File Structure

```
geo-seo/
├── SKILL.md                           # Core skill (workflow, inline rubric, 12 gotchas)
├── README.md                          # This file
├── references/
│   ├── scoring-rubric.md              # Authoritative 0–4 criteria with research citations
│   ├── schema-patterns.md             # JSON-LD patterns by site type with anti-patterns
│   ├── ai-crawlers.md                 # 3-tier crawler registry + CDN bot blocking detection
│   ├── research-basis.md              # 8 academic papers + 14 empirical findings + practitioners
│   ├── llms-txt-spec.md               # Jeremy Howard spec + validation rules
│   └── engine-profiles.md             # Per-engine profiles (Google AIO, AI Mode, Perplexity, ChatGPT, Bing)
└── assets/templates/
    ├── llms-txt/                      # 6 site-type starter templates
    │   ├── ecommerce.txt
    │   ├── saas.txt
    │   ├── content.txt
    │   ├── local.txt
    │   ├── docs.txt
    │   └── personal.txt
    ├── schema/                        # 6 JSON-LD templates with {PLACEHOLDER} convention
    │   ├── ecommerce.json
    │   ├── saas.json
    │   ├── content.json
    │   ├── local.json
    │   ├── docs.json
    │   └── personal.json
    └── robots-ai-block.txt            # 3-tier training/fetch/search split template
```

## Research Sources

### Academic Papers
1. Aggarwal et al., "GEO: Generative Engine Optimization" — Princeton/IIT Delhi, KDD 2024
2. Chen et al., "How to Dominate AI Search" — U of Toronto, Sep 2025
3. Wu et al., "AutoGEO" — CMU, ICLR 2026
4. Presenc AI, Synthesis of 34 GEO Papers — April 2026
5. "SAGEO Arena" — arXiv:2602.12187, Feb 2026
6. "AgentGEO" — arXiv:2603.09296, Mar 2026
7. "AgenticGEO" — arXiv:2603.20213, Mar 2026
8. "MAGEO" — arXiv:2604.19516, Apr 2026

### Practitioner Sources
- **Lily Ray** (Amsive Digital) — GEO/SEO conflict analysis, first-party source authority
- **Mike King** (iPullRank) — Relevance Engineering: atomic semantic chunks, AI simulation, citation KPIs
- **Jeremy Howard** (AnswerDotAI) — llms.txt specification
- **Perplexity Research** — binary pass/fail pipeline architecture, Sonar API
- **Ahrefs** — 75K-brand study on mentions vs backlinks for AI visibility
- **Yext** — 6.8M AI citation analysis on heading hierarchy
- **Rand Fishkin** (SparkToro) — zero-click outcome framing

## Installation

```bash
# From claude-code-minoan
ln -s "$(pwd)/skills/research/geo-seo" ~/.claude/skills/geo-seo

# Or copy directly
cp -r skills/research/geo-seo ~/.claude/skills/geo-seo
```

## License

MIT
