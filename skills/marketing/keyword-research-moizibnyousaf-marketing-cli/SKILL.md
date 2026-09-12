---
name: keyword-research
description: >
  Strategic keyword research powered by web search and brand context. Use this
  skill whenever the user mentions keywords, keyword research, SEO topics,
  content topics, 'what should I write about', content strategy, blog ideas,
  search traffic, or content planning. Also trigger when the user wants to plan
  what content to create, when existing content isn't attracting search traffic,
  when any skill needs keyword-plan.md but it doesn't exist, or when the user
  asks about SEO in the context of content creation. Even casual mentions like
  'I need blog post ideas' or 'what topics should I cover' warrant this skill.
  8-phase process from seed to content brief.
---


## On Activation

1. Check if `brand/` directory exists in the project root.
2. If it does, read available files: `voice-profile.md`, `positioning.md`, `audience.md`, `creative-kit.md`, `stack.md`, `learnings.md`.
3. Apply any loaded brand context to enhance output quality.
4. If `brand/` does not exist, proceed without it — this skill works standalone.

> **Note:** Examples below use fictional brands (Acme, Lumi, Helm). Replace with your own brand context.

## Backend Selection

Prefer measured KD/volume/CPC/intent/SERP/GSC via `openseo-keyword-research` when OpenSEO is configured; otherwise Exa-stack validation with metrics marked `unknown`. Full contract: `skills/openseo/references/backend-contract.md`.

# /keyword-research -- Data-Backed Keyword Strategy

Most keyword research is backwards. People start with tools, get overwhelmed by
data, and end up with a spreadsheet they never use.

This skill starts with strategy. What does your business need? Who are you trying
to reach? What would make them find you? Then it validates with live search data
and builds a content plan that actually makes sense.

No expensive tools required. Systematic thinking plus web search.

**Reads:** `positioning.md`, `audience.md`, `competitors.md`, `learnings.md`
**Writes:** `brand/keyword-plan.md`, `campaigns/content-plan/*.md`

---

## Iteration Detection

Before starting, check whether `./brand/keyword-plan.md` already exists.

### If keyword-plan.md EXISTS --> Refresh Mode

Do not start from scratch. Instead:

1. Read the existing plan.
2. Present a summary of the current keyword strategy:
   ```
   EXISTING KEYWORD PLAN (last updated {date})
   Pillars: {Pillar 1} {N} clusters {priority} · {Pillar 2} {N} {priority} · {Pillar 3} {N} {priority}
   Top keywords: {kw1} {priority} · {kw2} {priority} · {kw3} {priority}
   Content briefs: {N} created, {N} published

   What would you like to do?
   ① Refresh with new SERP data  ② Add a new topic area  ③ Re-prioritize clusters
   ④ Full rebuild from scratch   ⑤ Generate briefs for top keywords
   ```

3. Process the user's choice:
   - Option ① --> Re-run web search for existing keywords, update priorities based on fresh data
   - Option ② --> Gather new seed keywords, run full expansion, merge into existing plan
   - Option ③ --> Re-score all clusters with updated business context
   - Option ④ --> Full process from scratch
   - Option ⑤ --> Skip to content brief generation for highest-priority unfilled clusters

4. Before overwriting, show a compact diff of what changed (new clusters, priority changes, removals) and ask: "Save these changes? (y/n)"

5. Only overwrite after explicit confirmation.

### If keyword-plan.md DOES NOT EXIST --> Full Research Mode

Proceed to the full process below.

---

## The Core Job

Transform a business context into a **prioritized content plan** with:
- Keyword clusters organized by topic
- Priority ranking based on opportunity and live SERP data
- Content type recommendations
- Individual content briefs for top keywords
- A clear "start here" action

**Output format:** Clustered keywords mapped to content pieces, prioritized by
business value, competitive opportunity, and search demand. Saved to disk as
a keyword plan and individual content briefs.

---

## The Process

```
SEED --> EXPAND --> SEARCH --> CLUSTER --> VALIDATE --> PRIORITIZE --> MAP --> BRIEF
```

1. **Seed** -- Generate initial keywords from business context and brand memory
2. **Expand** -- Use the 6 Circles Method to build the full list
3. **Search** -- Pull live SERP data: autocomplete, People Also Ask, competitor rankings
4. **Cluster** -- Group related keywords into content pillars
5. **Validate** -- Run 4-check pillar validation with live competitive data
6. **Prioritize** -- Score by opportunity, business value, and search evidence
7. **Map** -- Assign clusters to specific content pieces
8. **Brief** -- Generate individual content briefs for top priorities

---

## Before Starting: Gather Context

Get these inputs before generating anything. If brand memory files exist, pre-fill
what you can and confirm with the user.

1. **What do you sell/offer?** (1-2 sentences)
   - Pre-fill from: ./brand/positioning.md
2. **Who are you trying to reach?** (Be specific)
   - Pre-fill from: ./brand/audience.md
3. **What is your website?** (To understand current content)
4. **Who are 2-3 competitors?** (Or help identify them)
   - Pre-fill from: ./brand/competitors.md
5. **What is the goal?** (Traffic? Leads? Sales? Authority?)
6. **Timeline?** (Quick wins or long-term plays?)

If brand memory supplies 3+ of these, present what you found and ask for
confirmation rather than re-asking:

```
  From your brand profile:

  ├── Offer       "{from positioning.md}"
  ├── Audience    "{from audience.md}"
  ├── Competitors {list from competitors.md}
  └── Positioning "{angle from positioning.md}"

  Does this still look right? And two more
  questions:

  1. What is the goal -- traffic, leads, sales,
     or authority?
  2. Timeline -- quick wins or long-term plays?
```

---

## Phase 1: Seed Generation

From the business context (and brand memory if loaded), generate 20-30 seed
keywords covering:

**Direct terms** -- What you actually sell
> "AI marketing automation", "fractional CMO", "marketing workflows"

**Problem terms** -- What pain you solve
> "can't keep up with content", "marketing team too small", "don't understand AI"

**Outcome terms** -- What results you deliver
> "faster campaign execution", "10x content production", "marketing ROI"

**Category terms** -- Broader industry terms
> "marketing automation", "AI marketing", "growth marketing"

**Brand-aligned terms** -- From positioning if loaded
> If positioning is "The Anti-Agency" → seed "agency alternatives", "in-house marketing",
> "DIY marketing strategy"
> If positioning is "AI-First Marketing" → seed "AI marketing tools", "automated campaigns",
> "machine learning marketing"

---

## Phase 2: Expand (The 6 Circles Method)

> See references/keyword-examples.md for detailed expansion techniques.

1. **What You Sell** -- Direct product/service terms
2. **Problems You Solve** -- Pain points and challenges
3. **Outcomes You Deliver** -- Results and benefits
4. **Your Unique Positioning** -- Differentiators
5. **Adjacent Topics** -- Related audience interests
6. **Entities to Associate With** -- People, brands, tools

---

## Phase 3: Web Search Validation (Exa-stack canonical)

Data-backed research layer for each pillar keyword + top 30-50 expansions. Canonical stack (mktg-native, no Ahrefs): Exa MCP (`web_search_advanced_exa`, `deep_search_exa`, `company_research_exa`) + Firecrawl (autocomplete + SERP scrape) + `/last30days` (Reddit/X/HN aggregation) + `gh` CLI (OSS GitHub-stars). For Ahrefs precision see appendix in `seo-machine/references/exa-recipes.md`.

### If Web Search Is Unavailable

Proceed with Phase 1 (seed generation) and Phase 2 (6 Circles expansion) using brand context only. Skip Phase 3 entirely but note the limitation to the user: 'Keyword clusters are based on strategic assessment, not live SERP data. Validate against actual search results before committing to content production.' Cluster and prioritize based on brand alignment and audience pain points rather than search volume.

### Step 1: Google Autocomplete Mining

For each seed and pillar keyword, search for autocomplete suggestions:

```
Search: "[keyword] a", "[keyword] b", ... "[keyword] z"
Search: "how to [keyword]"
Search: "best [keyword]"
Search: "why [keyword]"
Search: "[keyword] vs"
Search: "[keyword] for"
```

Capture every unique suggestion. These are real queries people type.

**What to look for:**
- Suggestions you did not think of (add to expanded list)
- Recurring modifiers (signals what people care about)
- Question patterns (signals informational intent)
- Brand/product mentions (signals commercial intent)
- Year modifiers ("2026") signal freshness demand

### Step 2: People Also Ask (PAA) Mining

For each pillar keyword, search Google and capture the People Also Ask boxes:

```
Search: "[pillar keyword]"
→ Capture PAA questions
→ Click/expand each PAA to get follow-up PAAs
→ Capture the second-level questions too
```

**What PAA data reveals:**
- The exact questions your audience asks (use as H2s in content)
- Related subtopics Google associates with this keyword
- Content gaps -- if PAA answers are thin, opportunity exists
- Semantic relationships between topics

**How to use PAA data:**
- Add new questions to your expanded keyword list
- Map PAA questions to content sections within pillar articles
- Identify PAA questions that deserve standalone articles
- Use PAA phrasing in headers (matches how people search)

### Step 3: SERP Analysis

For each priority keyword, examine the top search results:

```
Search: "[keyword]"
→ Analyze the top 5-10 results
→ Note: content type, word count, freshness, domain authority
```

**Capture for each result:**
- Title and URL
- Content type (guide, listicle, comparison, tool page, etc.)
- Freshness (when was it published/updated?)
- Quality assessment (comprehensive or thin?)
- Domain type (major publication, niche site, personal blog?)

**SERP signals:** Old results (2+ years) = freshness opportunity. Thin results (<1000 words) = depth opportunity. All big brands (DR 80+) = hard to win, try long-tail. Mixed big + small sites = winnable. Forums/Reddit in top 5 = huge content gap. Featured snippet = optimize for snippet format.

### Step 4: Competitor Content Analysis

If ./brand/competitors.md is loaded (or competitors were provided), search
for what they rank for:

```
Search: "site:{competitor-domain.com} [topic]"
Search: "{competitor name} [pillar keyword]"
Search: "{competitor name} blog"
```

**Build a competitor content map** for each competitor: topics covered, content types, keywords targeted, gaps, and quality. Identify three priority gap types: (1) catch-up — topics all competitors cover but you don't, (2) blue ocean — topics nobody covers well, (3) improvement — topics where competitors are weak/outdated.

### Search Integration Output

After web search, present a summary before clustering: total terms found, top 3 discoveries (unexpected keywords, competitor gaps, PAA insights), and new keywords added from search. Show counts for autocomplete suggestions, PAA questions, SERPs analyzed, and competitor pages reviewed.

---

## Phase 4: Cluster

Group expanded keywords (including web search discoveries) into content pillars
using the hub-and-spoke model:

```
                    [PILLAR]
                 Main Topic Area
                      |
        +-------------+-------------+
        |             |             |
   [CLUSTER 1]   [CLUSTER 2]   [CLUSTER 3]
    Subtopic       Subtopic       Subtopic
        |             |             |
    Keywords      Keywords      Keywords
```

### Identifying Pillars (5-10 per business)

A pillar is a major topic area that could support:
- One comprehensive guide (3,000-8,000 words)
- 3-7 supporting articles
- Ongoing content expansion

Ask: "Could this be a complete guide that thoroughly covers the topic?"

### Clustering Process

1. **Group by semantic similarity** -- Keywords that mean similar things
2. **Group by search intent** -- Keywords with same user goal
3. **Identify the pillar keyword** -- The broadest term in each group
4. **Identify supporting keywords** -- More specific variations
5. **Attach PAA questions** -- Map People Also Ask questions to the cluster they belong to
6. **Note competitor coverage** -- Mark which competitors cover this cluster


> See references/keyword-examples.md for example cluster with search data.

---

## Phase 5: Pillar Validation

> See references/keyword-examples.md for validation criteria.

Validate: search volume, competition, content-market fit, business alignment.

---

## Phase 6: Prioritize

Not all keywords are equal. Score each cluster using both strategic assessment
AND live search evidence from Phase 3.

Score each cluster on three dimensions:

- **Business Value** (High/Medium/Low): How directly does this connect to revenue? Commercial intent keywords close to purchase = High. Educational/authority content = Medium. Top-of-funnel brand awareness = Low.
- **Opportunity** (High/Medium/Low): What does the SERP data show? Forums ranking, outdated content, thin results = High opportunity. DR 80+ sites with comprehensive content = Low.
- **Speed to Win** (Fast/Medium/Long): Low competition with unique expertise = Fast (3 months). Moderate competition = Medium (6 months). High competition needing authority = Long (9-12 months).

**Priority:** High Value + High Opportunity + Fast = DO FIRST. High + High + Medium = DO SECOND. Medium + High + Fast = QUICK WIN. High + Low = LONG PLAY. Low value = BACKLOG.

### DR-Cap + Confidence Labels (mandatory filters)
Apply **DR-cap** (`KD > DR + buffer` → `out_of_reach` → BACKLOG) and tag every keyword with a 3-tier `confidence` label (`high`/`medium`/`estimated`). Table + output schema: `references/dr-cap-and-confidence.md`.

---

## Phase 7: Map to Content

For each priority cluster, assign a content type (Pillar Guide, How-To, Comparison, Listicle, Use Case, or Definition), match to search intent (Informational, Commercial, Transactional), and place in the content calendar (Tier 1-4 over 12 weeks).

Use PAA questions to build article outlines — each PAA question becomes an H2, aligning content structure with what Google knows people are asking.

> See references/keyword-examples.md for content type tables, intent matching rules, calendar tiers, and PAA-driven outline examples.

---

## Phase 8: Content Brief Generation

> See references/keyword-examples.md for brief template and keyword plan format.

Generate briefs for top-priority keywords: target keyword, search intent, content type, SERP snapshot, PAA questions, outline, angle.

---

## Output Format

See `references/keyword-examples.md` for the full terminal output template and keyword plan file format. Use the premium formatting system for terminal output (box-drawing characters, section headers) and standard markdown for files saved to disk.

---

## Chain to /seo-content

After presenting the keyword plan, actively offer to chain into content
creation for the top-priority keyword:

```
  ──────────────────────────────────────────────

  READY TO WRITE?

  Your top-priority keyword is "{keyword}" with
  a content brief ready at
  ./campaigns/content-plan/{slug}.md

  I can write this article now using /seo-content.
  It will use your brand voice, the content brief,
  and the SERP data I just gathered.

  → "Write it" to start /seo-content now
  → "Not yet" to save the plan and stop here

  ──────────────────────────────────────────────
```

If the user says "write it" or similar, hand off to /seo-content with:
- The content brief file path
- The keyword plan context
- The SERP analysis from Phase 3
- Brand memory context already loaded

---


> See references/keyword-examples.md for a complete worked example.

---

## Worked Example

**Cluster: 'verified meal delivery'**

| Keyword | Volume | Difficulty | Intent | Priority |
|---|---|---|---|---|
| verified meal delivery near me | 12,100 | 45 | Transactional | P1 |
| verified-source restaurants that deliver | 3,600 | 38 | Transactional | P1 |
| is doordash organic | 2,900 | 22 | Informational | P2 |
| verified meal prep delivery | 1,300 | 31 | Transactional | P2 |
| verifiedeats delivery | 880 | 15 | Navigational | P3 |

**Content brief:** Target 'verified meal delivery near me' with a city-specific landing page template (programmatic SEO). Target 'is doordash organic' with a comparison article linking to Acme.

---

## What This Skill Does NOT Do

This skill provides **strategic direction backed by search data**, not:
- Exact search volume numbers (use paid tools like exa MCP or web search for precision)
- Automated rank tracking (different tool category)
- Content writing (use /seo-content skill after brief generation)
- Technical SEO audits (different skill set)
- Link building strategy (separate from content strategy)

The output is a validated, prioritized plan with content briefs. Execution
is handled by /seo-content and other downstream skills.

---


> See references/keyword-examples.md for free tools.

---

## How This Skill Connects to Others

**keyword-research** creates the content strategy. Then: /seo-content writes articles from briefs, /positioning-angles finds the angle for each piece, /direct-response-copy handles commercial-intent landing pages, /content-atomizer repurposes pillar content, and /lead-magnet creates assets for top-of-funnel keywords.

---

## The Test

A good keyword research output is data-backed (SERP evidence, not intuition), actionable (clear "start here" with a brief ready), prioritized (ranked by opportunity), realistic (acknowledges competition), strategic (connects to business goals), specific (content types and outlines, not just keywords), and executable (briefs ready for /seo-content). If the output is "here's 500 keywords, good luck" — it failed.

---


## Progressive Enhancement Levels

| Level | Context Available | Output Quality |
|-------|------------------|---------------|
| L0 | Product name only, no web search | Basic seed keywords, strategic clusters, estimated priorities |
| L1 | + brand files (positioning, audience) | Brand-aligned keywords, audience-informed clusters |
| L2 | + competitors.md | Competitor gap analysis, differentiated content strategy |
| L3 | + web search available | Live SERP data, validated priorities, PAA-driven outlines |
| L4 | + existing keyword-plan.md (refresh) | Evolved plan with trend tracking, updated priorities |

---

## Feedback

After delivering the keyword plan, append learnings to `brand/learnings.md` when the user provides feedback on what worked or what they changed.
