---
name: shipflow-market-study
description: Complete market study for a product/niche — demand analysis, competition audit, keyword volumes, monetization strategy, GO/NO-GO verdict with structured report
disable-model-invocation: true
argument-hint: <niche or product idea>
---

## Context

- Current directory: !`pwd`
- Project CLAUDE.md: !`head -40 CLAUDE.md 2>/dev/null || echo "no CLAUDE.md"`
- DataForSEO MCP available: !`echo "dfs-mcp tools available — use mcp__dfs-mcp__* tools"`

## Mode detection

- **`$ARGUMENTS` is provided** → Run market study on that niche/product.
- **`$ARGUMENTS` is empty** → Use AskUserQuestion to ask what niche/product to study.

---

## Flow

### Step 1: Define the study scope

If `$ARGUMENTS` is empty, use **AskUserQuestion**:
- Question: "What niche or product idea should I study?"
- Options:
  - **Digital product** — "SaaS, app, online course, membership site"
  - **Content site** — "Blog, media, affiliate, niche authority site"
  - **E-commerce** — "Physical or digital goods marketplace"
  - **Service** — "Freelance, agency, consulting, coaching"

Then ask for the specific niche via a second question.

Once the niche is defined, use **AskUserQuestion** for target markets:
- Question: "Which geographic markets should I analyze?"
- `multiSelect: true`
- Options:
  - **France** — "French market (fr)"
  - **USA** — "US market (en-US)"
  - **UK** — "UK market (en-GB)"
  - **Global** — "Worldwide overview"
  - **Other** — "Specify country"

---

### Step 2: Market Demand Analysis (DataForSEO)

**Goal**: Quantify actual search demand — not guesses, real data.

#### 2a. Keyword Volume Research

Use **`mcp__dfs-mcp__kw_data_google_ads_search_volume`** for primary keywords:

1. Brainstorm 15-25 seed keywords across intent levels:
   - **High intent** (ready to act): "acheter X", "meilleur X", "X avis", "alternative à X"
   - **Medium intent** (researching): "comment X", "X vs Y", "X guide"
   - **Low intent** (awareness): "qu'est-ce que X", "X définition", "X statistiques"

2. Get search volumes, CPC, and competition for each market selected.

3. Use **`mcp__dfs-mcp__dataforseo_labs_google_keyword_suggestions`** to expand the keyword list — find long-tail opportunities the user hasn't thought of.

4. Use **`mcp__dfs-mcp__dataforseo_labs_google_keyword_ideas`** for semantically related keywords.

5. Use **`mcp__dfs-mcp__dataforseo_labs_google_related_keywords`** for adjacent niches.

#### 2b. Trend Analysis

Use **`mcp__dfs-mcp__kw_data_dfs_trends_explore`** or **`mcp__dfs-mcp__kw_data_google_trends_explore`**:
- Is the market growing, stable, or declining?
- Seasonal patterns?
- Compare main keywords over time.

Use **`mcp__dfs-mcp__kw_data_dfs_trends_subregion_interests`** for geographic distribution within target markets.

Use **`mcp__dfs-mcp__kw_data_dfs_trends_demography`** for demographic insights.

#### 2c. Search Intent Classification

Use **`mcp__dfs-mcp__dataforseo_labs_search_intent`** on the top 30 keywords:
- Classify each keyword: informational, navigational, commercial, transactional
- Identify the highest-value intent clusters

---

### Step 3: Competition Audit

**Goal**: Map who's already there and find gaps.

#### 3a. SERP Analysis

Use **`mcp__dfs-mcp__serp_organic_live_advanced`** on the top 10 high-intent keywords:
- Who ranks #1-10?
- Are they dedicated niche sites or generic big sites?
- Are there featured snippets, People Also Ask, knowledge panels?
- How hard would it be to compete?

#### 3b. Competitor Domain Analysis

For the top 3-5 competitors found in SERPs:

Use **`mcp__dfs-mcp__dataforseo_labs_google_domain_rank_overview`**:
- Domain authority / rank
- Total organic keywords
- Estimated traffic

Use **`mcp__dfs-mcp__dataforseo_labs_google_ranked_keywords`**:
- What keywords do they rank for?
- Where are their weak spots (positions 5-20)?

Use **`mcp__dfs-mcp__dataforseo_labs_google_competitors_domain`**:
- Who else competes in this space?

Use **`mcp__dfs-mcp__backlinks_summary`** for each competitor:
- How many backlinks?
- How hard to match their authority?

#### 3c. Content Gap Analysis

Use **`mcp__dfs-mcp__dataforseo_labs_google_domain_intersection`**:
- Keywords competitors rank for but no single competitor dominates
- Uncovered topics where a new entrant could win

Use **`mcp__dfs-mcp__dataforseo_labs_google_relevant_pages`**:
- Which competitor pages drive the most traffic?
- What content formats work (guides, lists, tools, comparisons)?

#### 3d. App Competition

Use **WebSearch** + **mcp__exa__web_search_exa**:
- Search app stores (Google Play, App Store) for competing apps
- Search "best [niche] app" and "[niche] app review"
- Count reviews, ratings, last update date
- Identify feature gaps

---

### Step 4: Market Sizing & Population Data

**Goal**: Quantify the addressable market beyond search volume.

Use **WebSearch** + **mcp__exa__web_search_exa** + **WebFetch** for:

1. **Total addressable market (TAM)**:
   - How many people have this problem/need?
   - Official statistics (government data, industry reports, academic studies)
   - Market value in $ or EUR

2. **Serviceable addressable market (SAM)**:
   - How many could realistically use a digital product?
   - Geographic and demographic filters

3. **Serviceable obtainable market (SOM)**:
   - Conservative capture rate (0.1% - 1% of SAM)
   - Revenue projection at target price point

4. **Market dynamics**:
   - Growth rate (CAGR)
   - Regulatory environment
   - Barriers to entry
   - Substitute products

Sources to check:
- Government statistics (INSEE, BLS, Eurostat)
- Industry reports (cite source + year)
- Academic research
- Press articles with data
- Existing market research (Statista, IBISWorld, etc.)

---

### Step 5: Monetization Strategy Analysis

**Goal**: Determine viable revenue models.

Use **WebSearch** + **mcp__exa__web_search_exa** to research:

1. **What competitors charge** (pricing pages, app store pricing)
2. **Willingness to pay** signals from CPC data (high CPC = advertisers pay = users have value)
3. **Revenue model options**:
   - Freemium (free tier + premium subscription)
   - One-time purchase
   - Subscription
   - Advertising
   - Affiliate
   - B2B / enterprise
   - Government/institutional funding

4. **Price benchmarking**:
   - What do similar products charge?
   - What's the "sweet spot" price point?
   - What's the pricing psychology angle?

5. **Revenue projections** (conservative):
   - Month 1-3, 3-6, 6-12, Year 2, Year 3
   - Based on: traffic → conversion rate → ARPU
   - Use industry benchmarks for conversion rates (2-5% freemium, 1-3% SaaS)

---

### Step 6: Domain & Brand Availability

Use **WebSearch** to check:

1. **Domain availability**:
   - .com, .fr, .io, country-specific TLDs
   - Exact keyword match domains
   - Brandable short domains
   - List available + taken domains

2. **Social handles**: @brand on Twitter/X, Instagram, TikTok, YouTube

3. **Trademark conflicts**: Quick search for existing trademarks

---

### Step 7: AI & LLM Visibility Analysis (Optional but recommended)

Use **`mcp__dfs-mcp__ai_optimization_llm_response`**:
- Ask LLMs about the niche — what do they recommend?
- Is there an opportunity for GEO (Generative Engine Optimization)?

Use **`mcp__dfs-mcp__ai_opt_llm_ment_search`**:
- Are existing competitors mentioned by LLMs?
- Is there a visibility gap in AI-generated answers?

---

### Step 8: Risk Assessment

Synthesize all data into a risk matrix:

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Strong competitor enters | Low/Med/High | High | [specific strategy] |
| Market too small | — | — | [data-backed assessment] |
| Regulation blocks | — | — | [analysis] |
| Can't monetize | — | — | [evidence from CPC/pricing] |
| SEO too competitive | — | — | [difficulty scores] |

---

### Step 9: GO / NO-GO Verdict

Based on all collected data, deliver a clear verdict:

**Scoring matrix** (score each 1-5):

| Criterion | Score | Evidence |
|-----------|-------|----------|
| Market demand (search volume) | /5 | [volumes] |
| Market growth (trends) | /5 | [trend data] |
| Competition level | /5 | [5=low competition, 1=saturated] |
| Monetization potential | /5 | [CPC, pricing, willingness to pay] |
| Content/product feasibility | /5 | [gap analysis] |
| Barrier to entry | /5 | [5=easy to enter, 1=high barriers] |
| **TOTAL** | **/30** | |

**Verdict scale**:
- **25-30**: GO — Strong opportunity, execute immediately
- **20-24**: GO CONDITIONNEL — Good opportunity with specific conditions
- **15-19**: PRUDENT — Opportunity exists but significant risks
- **10-14**: NO-GO SOFT — Market exists but not worth the effort
- **< 10**: NO-GO — Do not pursue

Include a **one-paragraph executive summary** justifying the verdict.

---

### Step 10: Action Plan (if GO)

If verdict is GO or GO CONDITIONNEL, provide:

1. **Domain strategy**: Which domains to buy immediately
2. **Content strategy**: First 20 pages to create, organized by priority
3. **Product strategy**: MVP feature set
4. **SEO strategy**: Quick wins vs long-term plays
5. **Launch timeline**: Pre-launch → Launch → Growth → Scale (4 phases)
6. **Revenue projections**: Conservative monthly estimates
7. **Competitive moat**: What makes this defensible

---

### Step 11: Save Report

Determine save location:
- If inside a project directory: save to `MARKET-STUDY.md` at project root
- If at workspace root (`~/`): save to `~/research/market-study-[niche-slug].md`

Generate a URL-safe slug from the niche: lowercase, hyphens, no special chars.

### Step 12: Final Report

```
MARKET STUDY COMPLETE: [niche]
═══════════════════════════════════════════════════════
Verdict:            [GO / GO CONDITIONNEL / PRUDENT / NO-GO]
Score:              [X/30]
Total keywords:     [count] analyzed
Search volume:      [total monthly volume across target markets]
Top keyword:        "[keyword]" — [volume]/mo
Competitors found:  [count] ([count] serious)
Market size (TAM):  [value]
Best price point:   [price]
Report saved to:    [file path]
═══════════════════════════════════════════════════════

KEY METRICS
  Monthly search demand:  [total]
  Market growth:          [trend] ([CAGR]%)
  Competition density:    [low/medium/high]
  Average CPC:            [value] (indicates monetization potential)
  App competition:        [count] apps ([count] with >100 reviews)

QUICK WIN KEYWORDS (low difficulty, decent volume)
  "[kw1]" — [vol]/mo — difficulty [X]
  "[kw2]" — [vol]/mo — difficulty [X]
  "[kw3]" — [vol]/mo — difficulty [X]

RECOMMENDED FIRST ACTIONS
  1. [action]
  2. [action]
  3. [action]
═══════════════════════════════════════════════════════
```

---

## MCP Tools Reference

### DataForSEO MCP (primary — pay-as-you-go, ~$0.0006/request)

**Keyword Research:**
- `mcp__dfs-mcp__kw_data_google_ads_search_volume` — Search volumes + CPC + competition
- `mcp__dfs-mcp__dataforseo_labs_google_keyword_suggestions` — Expand keyword list
- `mcp__dfs-mcp__dataforseo_labs_google_keyword_ideas` — Semantically related keywords
- `mcp__dfs-mcp__dataforseo_labs_google_related_keywords` — Adjacent niche keywords
- `mcp__dfs-mcp__dataforseo_labs_google_keyword_overview` — Quick keyword stats
- `mcp__dfs-mcp__dataforseo_labs_bulk_keyword_difficulty` — Difficulty scores in bulk
- `mcp__dfs-mcp__dataforseo_labs_search_intent` — Classify intent (informational/commercial/transactional)

**Trends:**
- `mcp__dfs-mcp__kw_data_google_trends_explore` — Google Trends data
- `mcp__dfs-mcp__kw_data_dfs_trends_explore` — DataForSEO trends (broader)
- `mcp__dfs-mcp__kw_data_dfs_trends_subregion_interests` — Geographic distribution
- `mcp__dfs-mcp__kw_data_dfs_trends_demography` — Demographic breakdown

**Competition:**
- `mcp__dfs-mcp__serp_organic_live_advanced` — Live SERP results
- `mcp__dfs-mcp__dataforseo_labs_google_domain_rank_overview` — Domain authority
- `mcp__dfs-mcp__dataforseo_labs_google_ranked_keywords` — Competitor keywords
- `mcp__dfs-mcp__dataforseo_labs_google_competitors_domain` — Find competitors
- `mcp__dfs-mcp__dataforseo_labs_google_domain_intersection` — Content gap analysis
- `mcp__dfs-mcp__dataforseo_labs_google_relevant_pages` — Top competitor pages
- `mcp__dfs-mcp__backlinks_summary` — Backlink profile overview
- `mcp__dfs-mcp__backlinks_competitors` — Backlink competitors

**AI/LLM Visibility:**
- `mcp__dfs-mcp__ai_optimization_llm_response` — What LLMs say about the niche
- `mcp__dfs-mcp__ai_opt_llm_ment_search` — Brand/product mentions in LLM outputs
- `mcp__dfs-mcp__ai_opt_llm_ment_top_domains` — Top domains cited by LLMs

**On-Page / Technical:**
- `mcp__dfs-mcp__on_page_instant_pages` — Quick page analysis
- `mcp__dfs-mcp__on_page_content_parsing` — Content extraction
- `mcp__dfs-mcp__on_page_lighthouse` — Performance audit

### Complementary Tools

**Web Research:**
- `WebSearch` — Broad search for market data, statistics, reports
- `mcp__exa__web_search_exa` — Technical/deep web search
- `WebFetch` — Fetch specific URLs for data extraction

**Content Analysis:**
- `mcp__dfs-mcp__content_analysis_search` — Content landscape analysis
- `mcp__dfs-mcp__content_analysis_summary` — Content metrics summary
- `mcp__dfs-mcp__content_analysis_phrase_trends` — Trending phrases

**Business Data:**
- `mcp__dfs-mcp__business_data_business_listings_search` — Local business competition
- `mcp__dfs-mcp__domain_analytics_whois_overview` — Domain registration info
- `mcp__dfs-mcp__domain_analytics_technologies_domain_technologies` — Tech stack detection

---

## Important

- **Every data point must have a source.** No invented volumes or market sizes.
- **Use DataForSEO MCP as primary data source** — it's the most cost-effective ($0.0006/request) and directly integrated.
- **Run API calls in parallel** where possible (multiple keyword research calls in one message).
- **Always get REAL search volumes** — never estimate or guess. If DataForSEO doesn't have data, note it explicitly.
- **Be honest about data limitations**: Google Ads blocks some sensitive keyword data. DataForSEO Labs often captures what Google Ads blocks.
- **Convert currencies**: Show both EUR and USD for international context.
- **Include competitor screenshots/descriptions**: Name names, give URLs, count reviews.
- **Conservative projections only**: Better to under-promise. Use pessimistic conversion rates (1-2%).
- **The verdict must be data-driven**: Every score in the matrix must reference specific data collected.
- **Save the report** — don't just print it. Market studies are reference documents.
- **If the market looks bad, say so clearly.** A good consultant saves the client from bad investments. A NO-GO verdict is valuable.
- **Language**: Write the report in the same language as the user's query. If French query → French report.
- **Cost awareness**: A full market study typically costs $2-5 in DataForSEO credits. Warn the user upfront.
- **Accents français obligatoires.** Lors de la rédaction de rapports en français, vérifier systématiquement que TOUS les accents sont présents et corrects (é, è, ê, à, â, ù, û, ô, î, ï, ç, œ, æ). Les accents manquants sont une faute d'orthographe. Relire chaque texte produit pour s'assurer qu'aucun accent n'a été oublié — c'est une erreur très fréquente à corriger impérativement.
