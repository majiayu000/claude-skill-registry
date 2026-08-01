---
name: kai-topical-map
description: Build an AEO-first topical map optimized for AI search citation — entity clusters, query fan-out coverage, information gain scoring, and multi-platform distribution. Produces entity map, content node architecture, schema blueprint, and 90-day publishing calendar. Use when "topical map", "content architecture", "site structure", "topic clusters", "pillar content plan", "AEO map", "AI search architecture", "entity map", "what content should we build", or any request to plan a site's topical structure for AI search visibility.
---

# /kai-topical-map — the map of pages, entities, and passages a team can start building

## Objective

A topical map built for AI search and traditional search together: which entities the brand must own, which sub-queries each pillar has to satisfy, where the brand can say something nobody else can, which pages that implies, and in what order they publish. Every decision traces to retrievability, entity clarity, source quality, and measurable demand.

AI search visibility is sampled, volatile, and engine-specific. This skill does not promise citations. It builds the thing that can be measured — pages to create, entities to clarify, passages to make retrievable, sources to cite, and the follow-up checks that show whether any of it worked.

## Done when

Work type `strategy-plan` (`also_covers: topical-map`) — floor **E3/C3/O1** (`harness/eco-floors.yaml`).

- **E3** — a named human approved the exact content node architecture: entity clusters make strategic sense, hub-and-spoke groupings are right, information gain angles are achievable with data the brand actually has, no critical sub-query is missing, and the priority order by Citation Impact Score is correct.
- **C3** — `banned_word_check` clean, every structural gate below met, and a named non-producer read the map end to end.
- **O1** — the baseline AI Presence Scorecard is recorded before any page ships, with the re-read scheduled at 30/60/90 days. Each priority node names the query set it targets and who owns publishing it.

**Structural gates, all mandatory:**

| Gate | Bar |
|---|---|
| Entity map | Every Tier 1 entity has a proposed Entity Home URL and a Wikidata action plan |
| Fan-out matrix | Every pillar has ≥6/8 sub-queries identified; pillars under 4/8 covered are priority gaps |
| Information gain | Every pillar has ≥2 "High" novelty opportunities, or is flagged for research before content creation |
| Schema | Every prescribed schema type has every relevant attribute populated |

## Constraints

- **Read `MARKETING.md` from the project root before asking the user anything.** If it does not exist, build it from the codebase — CLAUDE.md, README.md, PROJECT.md, package.json, landing pages, email/ad/analytics config — using the template from `/kai-email-system`, and confirm the draft.
- **Know these before mapping:** the brand entity, the topic space, the existing content inventory (blog URLs, episodes, landing pages, guides), 2–3 competitors currently winning citations in the space, the target queries, and the current AI presence.
- **Baseline the AI presence with recorded conditions.** Sample 3–5 category queries across ChatGPT, Perplexity, Bing/Copilot, and Google AI surfaces where available. Record prompt, location, date, engine, account state, citations, mentions, and missing-data caveats. This becomes the "before" measurement; re-run at 30/60/90 days.
- **Never paste a benchmark into a client-facing map without a source URL, retrieval date, evidence tier, confidence label, and fit note.** Treat Knowledge Graph, Wikidata, vector-search, traffic, citation, and conversion claims as source-dependent context, not promised outcomes.
- **Case-study evidence needs method, measurement, source quality, applicability, and caveat** before it informs a recommendation: what changed and whether a control existed; engine, prompt set, sample size, dates, geography, account state, and citation definition; official study vs vendor report vs internal measurement; whether the client's category, authority, depth, and distribution match; and what is still hypothesis.
- **Distribution must be transparent.** Participate in communities openly. No astroturfing, no seeded fake threads, no hidden ownership, no manufactured consensus.
- **Do not compare AI and organic conversion rates** without channel definitions, attribution windows, sample sizes, and confidence labels. Track AI traffic through source/medium rules, referrer inspection, landing-page cohorts, assisted conversions, and qualitative lead-source notes.
- **Schema does not substitute for useful visible content**, and `llms.txt` is useful for cooperative agents, not a Google AI Overview ranking requirement.
- **This skill plans. It does not write pages or publish anything.** The calendar hands off to `/kai-content-calendar` and `/kai-write`.

## Context

| Need | Load |
|---|---|
| AEO strategy foundation | `knowledge/frameworks/aeo-ai-search/aeo-ai-search-playbook-2026.md` |
| Entity tiers, Knowledge Graph, sameAs | `knowledge/frameworks/aeo-ai-search/entity-seo-knowledge-graph-deep-dive.md` |
| Query decomposition | `knowledge/frameworks/aeo-ai-search/query-fan-out-guide.md` |
| Page vs heading vs sentence | `knowledge/frameworks/content-copywriting/qdp-qdh-qds-content-architecture.md` |
| Novelty scoring | `knowledge/frameworks/aeo-ai-search/patent-information-gain-US12013887B2.md` + `knowledge/frameworks/aeo-ai-search/hidden-aeo-edges.md` |
| Retrieval and ranking behavior | `knowledge/frameworks/aeo-ai-search/geo-academic-research-synthesis.md` + `knowledge/frameworks/aeo-ai-search/perplexity-ranking-reverse-engineered.md` |
| Brief structure | `harness/brief-schema.md` |
| Calendar format compatibility | `harness/skills/kai-content-calendar/SKILL.md` |
| Product, ICP, voice, competitors | `MARKETING.md` (project root) |

**Entity tiers** — every entity lands in one:

| Tier | Meaning | Treatment |
|---|---|---|
| **1 — Own** | Brand, product, founder, proprietary methodology names | Entity Home URL + Wikidata QID (or submission plan) + Schema.org markup |
| **2 — Associate** | Industry terms, use cases, methodologies, problem categories, competitor categories | Content cluster topics; co-occurrence builds context vectors that signal expertise |
| **3 — Reference** | Research institutions, standards bodies, regulators, recognized experts | Cite for provenance and passage usefulness — no promised visibility lift |

The site's `@graph` roots at `Organization` or `Person` with `sameAs` links (Wikidata, LinkedIn, Crunchbase, socials), `knowsAbout` listing Tier 2 entities, and `mentions`/`about` connecting pages to entities.

**Query fan-out.** Google's AI Mode decomposes a complex query into roughly 8 parallel sub-queries and synthesizes one answer with layered citations (Liz Reid, Google I/O 2025). Mine PAA 3–4 levels deep and categorize each sub-query by facet:

| Facet | Example for "AI phone answering" |
|---|---|
| Definition | "What is an AI phone answering service?" |
| Cost | "How much does AI phone answering cost?" |
| Process | "How does AI phone answering work?" |
| Comparison | "AI phone answering vs live receptionist" |
| Safety/Risk | "Are AI phone answering services reliable?" |
| Timeline | "How long to set up AI phone answering?" |
| Alternatives | "Best AI phone answering services 2026" |
| Technical | "AI phone answering integrations with CRM" |

Route each sub-query by demand: **QDP** (high demand + distinct intent) gets its own URL, **QDH** (moderate) becomes a section inside a hub or spoke, **QDS** (low) becomes an inline sentence.

**Information gain.** The patent (US12013887B2) scores novelty against existing content via embeddings — paraphrase scores low however it is worded. Find the consensus across the top 5–10 results, then place the brand's angle:

| IG category | What it is | Why it works |
|---|---|---|
| Proprietary data | Original research, internal metrics, owned case studies | Reported 3.2x citation rate in Perplexity analysis |
| Contrarian position | Evidence-backed views against consensus | Triggers Perplexity's entropy diversity signal |
| Experience gap | First-person specifics a model cannot fabricate | Required for E-E-A-T "Experience" (QRG 4.6.6) |
| Novel framing | Unique terminology, frameworks, mental models | Creates semantic distance from competitors |
| Second-click content | Answers the follow-up query after the #1 result | Captures recursive fan-out |

Score each opportunity High (data or experience ready to publish), Medium (angle exists, research needed first), or Low (theoretical, no evidence).

**Content nodes.** Entity clusters become Hubs, QDP sub-queries become Spokes, QDH items become sections, QDS items become sentences. Each node declares URL, title, node type (Hub / Spoke / Entity Home), primary entity, fan-out queries answered, IG angle, and its citation-signal targets:

- ≥3 sourced data points per page when the topic benefits from data
- ≥1 permissioned quote or attributed expert source when claims need authority
- ≥5 primary or high-quality secondary sources for research-heavy pages
- 2–3 verifiable atomic facts per paragraph
- 60–100 word paragraphs where that improves scannability and passage retrieval
- 15–20 word sentence ceiling
- Direct answer in the first 30–50 words after the H2

**Schema prescription** (eligibility and clarity, not guaranteed citation lift):

| Node type | Schema | Purpose |
|---|---|---|
| FAQ / Q&A | `FAQPage` where eligible | Clarifies question-answer structure |
| How-to / process | `HowTo` where eligible | Clarifies steps, tools, prerequisites |
| Data / research / stats | `Dataset` where eligible | Clarifies dataset ownership and fields |
| All informational | `Article` or `BlogPosting` | Clarifies authorship, dates, subject |
| Entity Home | `Organization` or `Person` + `sameAs` | Clarifies canonical identity |

Incomplete or generic schema carries a reported **18% citation penalty** versus no schema at all (Growth Marshal, Feb 2026) — populate every relevant attribute.

**Citation Impact Score** sets publishing order:

```
CIS (1-10) = (Fan-Out Coverage × 0.3) + (IG Novelty × 0.3) + (Entity Authority × 0.2) + (GEO Signal Density × 0.2)

Fan-Out Coverage  = (sub-queries answered / total for pillar) × 10
IG Novelty        = Low 3 · Medium 6 · High 10
Entity Authority  = Entity Home 10 · Hub with schema 7 · Spoke 4 · QDH section 2
GEO Signal Density= planned stats + quotes + citations per page, normalized to 10
```

**Sequencing.** Entity Home pages first (weeks 1–2, with Schema.org and Wikidata submissions together — entity authority has no shortcut). Hubs before their spokes. High-IG pages inside month 1, where freshness compounds novelty. Cross-cluster pages spread through the calendar to keep building entity connections.

**Distribution.** Each node gets a plan; publishing only on the site leaves most of the reachable surface untouched.

| Surface | Format | Timing |
|---|---|---|
| Own site | Hub / Spoke page | Day 0 |
| LinkedIn | Article adaptation, 500–2,000 words | Day 1–2 |
| Reddit | Discussion or comparison thread | Day 3–5 |
| Industry directories | Listing or review (G2, Capterra, Yelp per vertical) | Week 1 |
| Guest post / PR | Adapted article | Week 2–3 |

| Engine | What it leans on | The move |
|---|---|---|
| Gemini / Google AI surfaces | Google Search crawl and index | Helpful, crawlable, snippet-eligible pages; schema; consistent subdomains |
| ChatGPT | Mixed retrieval, browsing, third-party consensus | Directory and review-site presence, "best of" inclusion, retrievable pages |
| Perplexity | Industry experts and niche directories | Vertical-specific: Zocdoc (health), Avvo (legal), G2 (SaaS) |
| Google AI Overviews | Search ranking, retrieval, query fan-out | Search fundamentals, source quality, page-level answers, entity presence, freshness |
| Community / social | Public discussion, professional context | Participate transparently |

**What each citation signal is actually good for** — use the left column for the middle column only, and carry the caveat:

| Signal | Use as | Caveat |
|---|---|---|
| External citations | Provenance and source-quality support | Not a guaranteed AI visibility lift |
| Expert quotes | Attributable authority and customer language | Requires permission and context |
| Statistics / data | Specificity and answer usefulness | Must be sourced and current |
| Proprietary research | Information gain and PR asset | Needs methodology disclosure |
| Topic clusters | Coverage and internal linking | Measure by queries and conversions, not vanity citation counts |
| Freshness | Accuracy maintenance | Update only when facts or examples change |
| Multi-platform distribution | Legitimate audience discovery | No astroturfing, hidden ownership, or fake consensus |
| Schema | Entity and content clarity | No substitute for useful visible content |

**Briefs** for the first 4 weeks follow `harness/brief-schema.md` plus AEO extensions: `information_gain_angle`, `fan_out_queries[]`, `citation_signals` (statistics/quotes/external citations required), `entity_targets[]`, `schema_type`, a schema-completeness note, and a per-channel `distribution_plan`.

**Output** goes to `workspace/topical-map/`: `_discovery.md`, `_entity-map.md`, `_fan-out-matrix.md`, `_information-gain-audit.md`, `_content-nodes.md`, `_schema-blueprint.json`, `_90-day-calendar.md`, `_distribution-plan.md`, `briefs/w[N]-[slug].json`, `_quality-report.md`. The calendar is directly consumable by `/kai-content-calendar`.

**Sources for the figures above:** HubSpot AEO case studies (blog.hubspot.com/marketing/answer-engine-optimization-case-studies) · Superlines AI search statistics (superlines.io/articles/ai-search-statistics) · Yext AI visibility study (yext.com/blog/ai-visibility-in-2025-how-gemini-chatgpt-perplexity-cite-brands) · Semrush/ALM LinkedIn citations (almcorp.com/blog/linkedin-ai-search-citations-2026) · Schema App entity linking case study · Wellows AI Overview ranking factors · ALM AI Overview citation shifts · Discovered Labs on Reddit as an AEO signal source · GEO paper, Aggarwal et al. 2024 (Princeton/Georgia Tech) · Information Gain patent US12013887B2 (Carbune & Gonnet, 2024) · Query Fan-Out, Liz Reid, Google I/O 2025.

## Escalate when

- The brand has no proprietary data or first-hand experience for a pillar — that pillar needs research before it earns a content plan.
- The topic space is regulated and the obvious content angles carry compliance risk.
- Competitor citation positions cannot be observed and the gap analysis would be guesswork.
- The user wants a citation, traffic, or ranking guarantee — that promise cannot be made.
- Entity Home pages would require site changes the user has not authorized.
- The plan's volume exceeds what the team can produce, and the priority cut needs a human decision.
