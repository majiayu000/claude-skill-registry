---
name: kai-topical-map
description: Build an AEO-first topical map optimized for AI search citation — entity clusters, query fan-out coverage, information gain scoring, and multi-platform distribution. Produces entity map, content node architecture, schema blueprint, and 90-day publishing calendar. Use when "topical map", "content architecture", "site structure", "topic clusters", "pillar content plan", "AEO map", "AI search architecture", "entity map", "what content should we build", or any request to plan a site's topical structure for AI search visibility.
---

Build a topical map optimized for AI search engines and traditional search together. Every decision is driven by retrievability, entity clarity, source quality, and measurable user demand, not by promises that a specific AI engine will cite a page.

## Why This Matters

AI search visibility is sampled, volatile, and engine-specific. Treat any traffic, citation, or conversion benchmark as context until it is verified for the client with a source, retrieval date, evidence tier, and confidence label.

This skill builds the map that can be measured: pages to create, entities to clarify, passages to make retrievable, sources to cite, and follow-up checks to run.

---

## Phase 0: Load Product Context

Check if `MARKETING.md` exists in the **project root** (same directory as CLAUDE.md, README.md, package.json).

**If it exists:** Read it — skip product discovery questions. It has the product name, ICP, value prop, monetization, brand voice, current channels, and competitive landscape.

**If it does NOT exist:** Auto-explore the codebase to create it in the **project root** (next to CLAUDE.md). Do NOT ask the user what the product is. Read CLAUDE.md, README.md, PROJECT.md, package.json, landing pages, and any project files. Search for email/ad/analytics config. Then create `MARKETING.md` using the template from `/kai-email-system`. Present draft to user for confirmation.

---

## Phase 1: Topic Space Discovery

Load before starting:
- `E:\Dev2\kai-cmo-harness-work\knowledge\frameworks\aeo-ai-search\aeo-ai-search-playbook-2026.md`

Read from `MARKETING.md`. Only ask about things not covered there:

1. **Brand/product** — what entity should AI engines associate with this topic space?
2. **Topic space** — the broad domain (e.g., "AI receptionist software", "personal injury law", "B2B cold email")
3. **Existing content inventory** — blog post URLs, podcast episode titles, landing pages, guides already published
4. **Competitor URLs** — 2-3 sites currently winning AI citations in this topic space
5. **Target queries** — what questions should AI answer with YOUR brand? (e.g., "What's the best AI phone answering service?")
6. **Current AI presence** — sample 3-5 category queries in ChatGPT, Perplexity, Bing/Copilot, and Google AI surfaces where available. Record prompt, location, date, engine, account state, citations, mentions, and missing-data caveats.

Output: `workspace/topical-map/_discovery.md`

### Baseline AI Presence Scorecard

| Query | ChatGPT | Perplexity | Google AI | Brand Mentioned? | Who IS Mentioned? |
|-------|---------|------------|-----------|-----------------|-------------------|
| [category query 1] | | | | Y/N | [competitors] |
| [category query 2] | | | | Y/N | [competitors] |
| ... | | | | | |

This scorecard becomes the "before" measurement. Run it again at 30/60/90 days to track progress.

---

## Phase 2: Entity Map

Load before starting:
- `E:\Dev2\kai-cmo-harness-work\knowledge\frameworks\aeo-ai-search\entity-seo-knowledge-graph-deep-dive.md`

### Map the Entity Landscape

Identify every entity the brand needs to establish, strengthen, or associate with in the Knowledge Graph. Organize into three tiers:

**Tier 1 — Own:** Entities the brand must be the canonical authority for. These get Entity Home pages.
- Brand name, product name, founder/CEO, proprietary methodology or framework names
- Each Tier 1 entity needs: Entity Home URL, Wikidata QID (or submission plan), Schema.org markup

**Tier 2 — Associate:** Entities the brand should appear in context with. These become content cluster topics.
- Industry terms, use cases, methodologies, problem categories, competitor categories
- Appearing alongside these entities builds "context vectors" (Bill Slawski's patent analysis) that signal expertise

**Tier 3 — Reference:** Authoritative entities to cite for credibility amplification.
- Research institutions, industry standards, regulatory bodies, recognized experts
- Cite these entities to improve provenance and passage usefulness. Do not promise a fixed citation or visibility lift from citations.

### Entity Map Output

```
| Entity | Type | Current KG Status | Tier | Entity Home URL | Wikidata QID | Schema Types | Action |
|--------|------|-------------------|------|-----------------|--------------|--------------|--------|
```

### Schema.org Blueprint

Generate a `@graph` structure for the site showing:
- `Organization` or `Person` as the root entity with `sameAs` links (Wikidata, LinkedIn, Crunchbase, social profiles)
- `knowsAbout` properties listing Tier 2 entities
- `mentions` and `about` properties connecting content pages to entities
- `sameAs` links for every entity that has a Wikidata or Wikipedia entry

**Evidence requirement:** Treat Knowledge Graph, Wikidata, and vector-search claims as source-dependent. Add source URL, retrieval date, evidence tier, and confidence before using any quantitative claim in a client-facing map.

**Gate:** Every Tier 1 entity must have a proposed Entity Home URL and a Wikidata action plan.

Output: `workspace/topical-map/_entity-map.md`

---

## Phase 3: Query Fan-Out Coverage Matrix

Load before starting:
- `E:\Dev2\kai-cmo-harness-work\knowledge\frameworks\aeo-ai-search\query-fan-out-guide.md`
- `E:\Dev2\kai-cmo-harness-work\knowledge\frameworks\content-copywriting\qdp-qdh-qds-content-architecture.md`

### How AI Search Decomposes Queries

Google's AI Mode uses "Query Fan-Out" (Liz Reid, Google I/O 2025): complex queries are broken into ~8 simultaneous sub-queries, results are retrieved in parallel, then synthesized into a single answer with layered citations. To rank for a pillar topic, your content must satisfy multiple sub-intents.

### Build the Matrix

For each pillar topic identified from Phase 2's entity clusters:

1. **Identify the primary query** — the question a user asks AI about this topic
2. **Decompose into ~8 sub-queries** using PAA mining (3-4 levels deep):
   - Mine "People Also Ask" for the primary query
   - Click through PAA 3-4 levels to discover recursive sub-topics
   - Categorize each sub-query by intent facet:

| Facet | Example for "AI phone answering" |
|-------|----------------------------------|
| **Definition** | "What is an AI phone answering service?" |
| **Cost** | "How much does AI phone answering cost?" |
| **Process** | "How does AI phone answering work?" |
| **Comparison** | "AI phone answering vs live receptionist" |
| **Safety/Risk** | "Are AI phone answering services reliable?" |
| **Timeline** | "How long to set up AI phone answering?" |
| **Alternatives** | "Best AI phone answering services 2026" |
| **Technical** | "AI phone answering integrations with CRM" |

3. **Map existing content** against sub-queries:

```
| Pillar | Primary Query | Definition | Cost | Process | Comparison | Safety | Timeline | Alternatives | Technical | Coverage |
|--------|--------------|------------|------|---------|------------|--------|----------|-------------|-----------|----------|
| [topic] | [query] | [covered/partial/gap] | ... | ... | ... | ... | ... | ... | ... | X/8 |
```

4. **Apply QDP/QDH/QDS** to each sub-query:
   - **QDP (Query Deserves Page)**: High demand + distinct intent → dedicated URL
   - **QDH (Query Deserves Heading)**: Moderate demand → section within hub or spoke page
   - **QDS (Query Deserves Sentence)**: Low demand → inline mention

**Gate:** Every pillar must have ≥6/8 sub-queries identified. Pillars with <4/8 currently covered = priority gaps.

Output: `workspace/topical-map/_fan-out-matrix.md`

---

## Phase 4: Information Gain Audit

Load before starting:
- `E:\Dev2\kai-cmo-harness-work\knowledge\frameworks\aeo-ai-search\patent-information-gain-US12013887B2.md`
- `E:\Dev2\kai-cmo-harness-work\knowledge\frameworks\aeo-ai-search\hidden-aeo-edges.md`

### Why Information Gain Matters

Google's Information Gain patent (US12013887B2) calculates content novelty using word2vec embeddings. Content that paraphrases what already exists — even in different words — scores LOW. Content must be "orthogonal to consensus" to earn citations.

**The math:** `IG Score = f(V_new, V_history)` where high KL-divergence from existing content = high score.

### Audit Process

For each pillar topic:

1. **Analyze top 5-10 ranking results** — list the facts, angles, data points, and framing that ALL of them share. This is the "consensus content."
2. **Identify Information Gain opportunities** in five categories:

| IG Category | Description | Citation Multiplier |
|-------------|-------------|-------------------|
| **Proprietary Data** | Original research, internal metrics, case studies you own | 3.2x more citations (Perplexity study) |
| **Contrarian Position** | Evidence-backed views contradicting consensus | Triggers Perplexity entropy diversity signal |
| **Experience Gap** | First-person specifics AI cannot fabricate | Required for E-E-A-T "Experience" (QRG 4.6.6) |
| **Novel Framing** | Unique terminology, frameworks, mental models | Creates semantic distance from competitors |
| **Second-Click Content** | Optimized for the follow-up query after user views #1 result | Captures recursive fan-out queries |

3. **Score each opportunity:**
   - **High**: Brand has proprietary data or unique experience ready to publish
   - **Medium**: Angle exists but requires research/data collection first
   - **Low**: Theoretical advantage but no current evidence to support it

### Information Gain Map

```
| Pillar | Consensus Content (what everyone says) | IG Angle | IG Category | Novelty Score | Source/Evidence Available |
|--------|----------------------------------------|----------|-------------|---------------|--------------------------|
```

**Gate:** Every pillar must have ≥2 "High" novelty opportunities. Pillars with no proprietary data or unique experience = flag for research/data collection before content creation.

Output: `workspace/topical-map/_information-gain-audit.md`

---

## Phase 5: Content Node Architecture

Load before starting:
- `E:\Dev2\kai-cmo-harness-work\knowledge\frameworks\aeo-ai-search\geo-academic-research-synthesis.md`
- `E:\Dev2\kai-cmo-harness-work\knowledge\frameworks\aeo-ai-search\perplexity-ranking-reverse-engineered.md`

### Synthesize Into Hub-and-Spoke Architecture

Combine Phases 2-4 into the actual pages to create:

- Each **entity cluster** (Phase 2) becomes a **Hub**
- Each **QDP sub-query** (Phase 3) becomes a **Spoke**
- Each **QDH sub-query** becomes a section within a Hub or Spoke
- Each **QDS item** becomes a sentence within the relevant page

### Content Node Specification

For each node, define:

**Identity:**
- URL (clean, entity-descriptive)
- Title
- Node type: Hub / Spoke / Entity Home

**AEO Signals:**
- Primary entity served (from Phase 2)
- Fan-out queries answered (from Phase 3)
- Information Gain angle (from Phase 4)

**Citation Signal Requirements** (evidence-safe operating targets):
- Statistics: at least 3 sourced data points per page when the topic benefits from data
- Expert quotes: at least 1 permissioned quote or attributed expert source when claims need authority
- External citations: at least 5 primary or high-quality secondary sources for research-heavy pages
- Atomic fact density: 2-3 verifiable facts per paragraph
- Paragraph length: 60-100 words when it improves scannability and passage retrieval
- Sentence length: 15-20 words maximum
- Answer position: direct answer in first 30-50 words after H2

**Schema Prescription** (eligibility and clarity, not guaranteed citation lift):

| Content Node Type | Primary Schema | Why Use It |
|-------------------|---------------|-----------------|
| FAQ / Q&A content | `FAQPage` where eligible | Clarifies question-answer structure |
| How-to / Process guides | `HowTo` where eligible | Clarifies steps, tools, and prerequisites |
| Data / Research / Stats pages | `Dataset` where eligible | Clarifies dataset ownership and fields |
| All informational content | `Article` or `BlogPosting` | Clarifies authorship, dates, and subject |
| Entity Home pages | `Organization` or `Person` + `sameAs` | Clarifies canonical entity identity |

**Rule:** All schema must have EVERY relevant attribute populated. Generic/incomplete schema produces an **18% citation penalty** vs having no schema at all (Growth Marshal, Feb 2026).

### Citation Impact Score

Score each node to prioritize publishing order:

```
Citation Impact Score (1-10) =
  (Fan-Out Coverage × 0.3)           # How many sub-queries does this page answer?
+ (Information Gain Novelty × 0.3)   # How novel is this content vs consensus?
+ (Entity Authority × 0.2)           # Does this page strengthen the entity graph?
+ (GEO Signal Density × 0.2)         # How citation-dense is this page?
```

Where:
- Fan-Out Coverage: (sub-queries answered / total sub-queries for pillar) × 10
- IG Novelty: Low (3), Medium (6), High (10)
- Entity Authority: Entity Home (10), Hub with Schema (7), Spoke (4), QDH section (2)
- GEO Signal Density: (planned stats + quotes + citations per page, normalized to 10)

### Content Node Output

```markdown
## Hub: [Entity Cluster Name]

### Hub Page: [Title]
- URL: /[slug]
- Primary Entity: [entity]
- Fan-Out Queries Answered: [list]
- Information Gain Angle: [description]
- Citation Signals: { stats: 5, quotes: 2, citations: 8 }
- Schema: FAQPage + Article
- Citation Impact Score: 8.4/10

### Spoke 1: [Title]
- URL: /[slug]
...
```

### Approval Gate

Present the full content node architecture to the user. Confirm:
- Entity clusters make strategic sense for the brand
- Hub-and-Spoke groupings are correct
- Information Gain angles are achievable (brand has the data/experience)
- No critical sub-queries are missing
- Priority order by CIS is correct

Output: `workspace/topical-map/_content-nodes.md`, `workspace/topical-map/_schema-blueprint.json`

---

## Phase 6: 90-Day Publishing Calendar + Distribution Plan

Load before starting:
- `E:\Dev2\kai-cmo-harness-work\harness\brief-schema.md`
- `E:\Dev2\kai-cmo-harness-work\harness\skills\kai-content-calendar\SKILL.md` (for format compatibility)

### AEO Sequencing Rules

Sort content nodes by Citation Impact Score, then apply sequencing:

1. **Entity Home pages first (Week 1-2)** — You cannot build entity authority without canonical pages. Deploy Schema.org + Wikidata submissions simultaneously.
2. **Hubs before Spokes** — The hub establishes the semantic center of each cluster.
3. **High-IG pages early (Month 1)** — Pages updated within 60 days are 1.9x more likely to appear in AI answers (BrightEdge). Novel content has a freshness advantage.
4. **Cross-cluster pages distributed** — Pages answering sub-queries shared across pillars spread throughout the calendar to build ongoing entity connections.

### Multi-Platform Distribution Plan

Each content node gets a distribution plan. Publishing on your site alone leaves 325% of potential citations on the table.

**Per-node distribution template:**

| Platform | Format | Why | Timing |
|----------|--------|-----|--------|
| **Own site** | Hub/Spoke page | Gemini cites brand-owned sites 52% of the time | Day 0 (publish) |
| **LinkedIn** | Article adaptation (500-2,000 words) | #2 most-cited domain; 11% of all AI responses; #1 for professional queries | Day 1-2 |
| **Reddit** | Discussion thread / comparison post | #1 most-cited domain across all AI platforms. Apollo.io achieved 63% citation rate from Reddit alone | Day 3-5 |
| **Industry directories** | Listing / review | ChatGPT gets 49% of citations from directories (G2, Yelp, Capterra per vertical) | Week 1 |
| **Guest post / PR** | Adapted article | Brands 6.5x more likely cited through third-party sources (Ahrefs) | Week 2-3 |

**Platform-specific AI citation strategy:**

| AI Engine | What It Trusts | Your Move |
|-----------|---------------|-----------|
| **Gemini** | Your domain (52% of citations from brand-owned sites) | Schema markup, structured content, consistent subdomains |
| **ChatGPT** | Third-party consensus (49% from directories) | G2/Capterra listings, review sites, "best of" inclusions |
| **Perplexity** | Industry experts + niche directories | Zocdoc (health), Avvo (legal), G2 (SaaS) — vertical-specific |
| **Google AI Overviews** | Entity authority + freshness | Knowledge Graph presence, Wikidata, recent updates |

### Calendar Output

```
| Week | Date | Content Node | Type | CIS | Schema Deploy | Distribution | Entity Action |
|------|------|-------------|------|-----|---------------|-------------|---------------|
| 1 | Mon | Entity Home: About [Brand] | Entity Home | 9.2 | Organization + sameAs | LinkedIn, directories | Wikidata submission |
| 1 | Thu | [Pillar 1 Hub] | Hub | 8.4 | FAQPage + Article | LinkedIn article, Reddit | Deploy @graph |
| 2 | Mon | [Pillar 1 Spoke 1] | Spoke | 7.8 | HowTo | LinkedIn post, Reddit | - |
| 2 | Thu | [Pillar 2 Hub] | Hub | 7.5 | Dataset + Article | LinkedIn article | Deploy schema |
```

### Brief Generation

Generate briefs for the first 4 weeks using the schema from `E:\Dev2\kai-cmo-harness-work\harness\brief-schema.md`, extended with AEO-specific fields:

```json
{
  "standard_brief_fields": "...",

  "aeo_extensions": {
    "information_gain_angle": "What novel content does this piece contribute?",
    "fan_out_queries": ["Sub-query 1", "Sub-query 2", "..."],
    "citation_signals": {
      "statistics_required": 5,
      "expert_quotes_required": 2,
      "external_citations_required": 8
    },
    "entity_targets": ["Entity 1", "Entity 2"],
    "schema_type": "FAQPage + Article",
    "schema_completeness_note": "All attributes must be populated — incomplete schema = -18% penalty",
    "distribution_plan": {
      "linkedin": "Article adaptation, 800 words, publish Day 1",
      "reddit": "Discussion thread in r/[relevant], Day 3",
      "directory": "Update G2 listing with new feature mention, Week 1"
    }
  }
}
```

Output:
- `workspace/topical-map/_90-day-calendar.md`
- `workspace/topical-map/_distribution-plan.md`
- `workspace/topical-map/briefs/w[N]-[slug].json`

**Integration:** Calendar format is directly consumable by `/kai-content-calendar` for production mode.

---

## Phase 7: Quality Report + Next Steps

Output a summary report at `workspace/topical-map/_quality-report.md`:

```markdown
# AEO Topical Map — Quality Report

## Entity Coverage
- Total entities mapped: [N]
- Tier 1 (Own): [N] — Entity Homes defined: [N/N]
- Tier 2 (Associate): [N]
- Tier 3 (Reference): [N]
- Wikidata submissions planned: [N]
- Schema deployments needed: [N]

## Fan-Out Coverage
- Total pillar topics: [N]
- Sub-queries identified: [N]
- Average coverage per pillar: [X/8]
- Critical gaps (< 4/8): [list]

## Information Gain
- Total IG opportunities: [N]
- High novelty: [N] | Medium: [N] | Low: [N]
- Requires data collection before writing: [N]
- Achievable with existing assets: [N]

## Content Nodes
- Total pages planned: [N]
- Entity Homes: [N] | Hubs: [N] | Spokes: [N]
- Average Citation Impact Score: [X/10]
- Top 5 by CIS: [list with scores]

## Distribution Plan
- Total on-site pages: [N]
- LinkedIn articles planned: [N]
- Reddit threads planned: [N]
- Directory updates planned: [N]
- Guest posts / PR planned: [N]

## 90-Day Calendar
- Total pieces scheduled: [N]
- Schema deployments scheduled: [N]
- Entity actions scheduled: [N]

## Recommended Next Steps
1. `/kai-content-calendar` — Move into production mode with the calendar
2. `/kai-surround-sound` — Build off-site consensus web (complements the distribution plan)
3. `/kai-seo-audit` — Ensure technical foundation supports search and agent readability (crawlability, renderability, optional llms.txt, schema, accessibility tree)
4. `/kai-write` — Produce content using briefs (AEO extensions auto-loaded)
5. Re-run AI Presence Scorecard (Phase 1) at 30/60/90 days to measure progress
```

---

## Reference: Benchmark Handling

Do not paste benchmark numbers into client-facing maps unless each claim has a source URL, retrieval date, evidence tier, confidence label, and fit note. Use the following as a research checklist, not as promised outcomes.

### Case Study Evidence To Collect

- Method: what changed, what stayed constant, and whether a control or holdout existed
- Measurement: engine, prompt set, sample size, dates, geography, account state, and citation definition
- Source quality: official study, academic paper, vendor report, practitioner benchmark, or internal measurement
- Applicability: whether the client's category, site authority, content depth, and distribution match the case
- Caveat: what data is missing and what should be treated as hypothesis

### Citation Signal Guidance

| Signal | Use As | Caveat |
|--------|--------|--------|
| External citations | Provenance and source-quality support | Not a guaranteed AI visibility lift |
| Expert quotes | Attributable authority and customer language | Requires permission and context |
| Statistics / data | Specificity and answer usefulness | Must be sourced and current |
| Proprietary research | Information gain and PR asset | Needs methodology disclosure |
| Topic clusters | Coverage and internal linking | Measure by queries and conversions, not vanity citation counts alone |
| Freshness | Accuracy maintenance | Update only when facts or examples change |
| Multi-platform distribution | Legitimate audience discovery | Avoid astroturfing, hidden ownership, or fake consensus |
| Schema | Entity and content clarity | Schema does not substitute for useful visible content |

### Platform Citation DNA

| AI Engine | Primary Citation Source | Implication |
|-----------|----------------------|-------------|
| Gemini / Google AI surfaces | Google Search crawl and index systems | Invest in helpful, crawlable, snippet-eligible pages |
| ChatGPT | Mixed retrieval, browsing, and partner/source behavior | Earn coverage in trusted sources and make pages retrievable |
| Perplexity | Industry-specific directories | Zocdoc (health), Avvo (legal), G2 (SaaS) |
| Google AI Overviews | Search ranking, retrieval, and query fan-out | Focus on Search fundamentals, source quality, and page-level answers |
| Community/social platforms | Public discussion and professional context | Participate transparently; do not seed fake threads |

### AI Traffic Measurement

Track AI traffic with source/medium rules, referrer inspection, landing-page cohorts, assisted conversions, and qualitative lead-source notes. Do not compare AI and organic conversion rates without channel definitions, attribution windows, sample sizes, and confidence labels.

### Sources

- HubSpot AEO Case Studies: https://blog.hubspot.com/marketing/answer-engine-optimization-case-studies
- Superlines AI Search Statistics: https://www.superlines.io/articles/ai-search-statistics/
- Yext AI Visibility Study: https://www.yext.com/blog/ai-visibility-in-2025-how-gemini-chatgpt-perplexity-cite-brands
- Semrush LinkedIn Citations: https://almcorp.com/blog/linkedin-ai-search-citations-2026/
- Schema App Entity Linking: https://www.schemaapp.com/schema-markup/case-study-entity-linking-increases-aio-visibility/
- Google AI Overview Rankings: https://wellows.com/blog/google-ai-overviews-ranking-factors/
- AI Overview Citation Shifts: https://almcorp.com/blog/google-ai-overview-citations-drop-top-ranking-pages-2026/
- Reddit AEO Signal Source: https://discoveredlabs.com/blog/reddit-as-an-aeo-signal-source-how-llms-pull-brand-mentions-to-drive-ai-citations
- GEO Paper: Aggarwal et al. (2024), Princeton/Georgia Tech
- Information Gain Patent: US12013887B2 (Carbune & Gonnet, 2024)
- Query Fan-Out: Liz Reid, Google I/O 2025
