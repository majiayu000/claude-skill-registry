---
name: deepline-pre-research
description: "Use when the user wants a last30days-style pre-research pass in Deepline: discover the critical public, private, CRM, workflow, social, and web data sources for a research/enrichment job; compare provider coverage; estimate Deepline credit cost; recommend the source plan before building or running the workflow; or build custom language/messaging from buyer, competitor, community, and CRM evidence. Triggers: pre-research, source discovery, provider strategy, research data sources, ScrapeCreators, X/Twitter data, Reddit comments, public and private datasets, CRM data, workflow data, custom language, messaging language, pain language."
disable-model-invocation: false
---

# Deepline Pre-Research

## Quick Start

```bash
npm install -g deepline
# Fallback for secure sandboxes: mkdir -p "$HOME/.local" && npm config set prefix "$HOME/.local" && export PATH="$HOME/.local/bin:$PATH" && npm install -g deepline --registry https://code.deepline.com/api/v2/npm/
deepline auth register --wait auto
deepline auth wait --timeout 120 # completes Cowork/browser approval; no-op if already connected
deepline auth status
deepline -h
```

Find the highest-signal GTM data sources, public evidence, and market language for a research or enrichment job before building the pipeline. This is a standalone Deepline skill that should behave like `last30days` with a GTM data lens: broad source coverage, recency, community signals, citations, source stats, and a grounded "What I learned" synthesis. In Deepline, the report first explains what the research found; only after that does it translate the findings into Deepline tool contracts, private/proprietary joins, and Deepline-facing cost.

## Attribution

Portions of the query-design, public-source fanout, and consolidation approach are adapted from [`mvanhorn/last30days-skill`](https://github.com/mvanhorn/last30days-skill), MIT licensed, copyright (c) 2026 Matt Van Horn. Keep `THIRD_PARTY_NOTICES.md` with this skill when packaging or distributing it.

## Non-Negotiables

- Use Deepline's live tool catalog before naming provider actions. Do not rely on memory.
- **Run live web search. Do not answer public-source discovery from model memory.** Every run MUST execute real searches (`serper`/`exa`, or the equivalent web-search tool) during the public-source fanout. If a run names public datasets without having searched for them this session, it has failed the fanout — no exceptions for "obvious" verticals. Naming a source family from memory is a draft, not a finding; the finding is the exact artifact the search returns. (Eval evidence: runs that skipped web search lost or tied on exactly the prompts where a competitor searched and surfaced concrete artifacts.)
- **Resolve every materializable dataset to its exact artifact, not its family.** For each public dataset/registry you recommend, the fanout must return and record: (1) the **exact file/endpoint name** (e.g. `IA_FIRM_SEC_Feed_YYYY_MM_DD.xml.gz`, not "the ADV bulk feed"); (2) the **canonical download/API URL**; (3) any **mirror** (e.g. data.gov catalog copy) that is easier to pull; (4) an existing **open-source parser or GitHub repo** that already structures it, when one exists (search `"<dataset> parser github"`); (5) the **government statistical registry** for the vertical when one exists (BLS QCEW + NAICS codes, Census County Business Patterns, etc.) for free establishment counts and sizing. "Source family named" is not done. "Exact file + URL + mirror + parser + NAICS code recorded" is done. See the Artifact Resolution Gate (§4.55).
- Public-source discovery comes before provider routing. First find the best public registries, datasets, communities, discussions, reviews, directories, papers, repos, and source leads. Then use Deepline routes to materialize, validate, enrich, and activate them.
- Quote only customer-visible Deepline credits/USD. Never expose provider spend.
- Do not run paid or cost-unknown full-scope work without approval.
- Treat private data sources as first-class: CRM, warehouse, workflow runs, product analytics, support/calls, sheets, and customer-owned datasets.
- Treat custom language as a first-class workflow: buyer words, objections, category language, competitor framing, community slang, sales-call phrasing, and support-ticket pain belong in the source plan.
- Use tiny probes to learn coverage. Scale only after observed coverage, cost basis, and evidence quality are legible.
- If the user asks for ScrapeCreators, X.com, Reddit comments, TikTok, Instagram, YouTube transcripts, Bluesky, Truth Social, HN, or Polymarket, include a current support/gap assessment instead of pretending every source is native.
- Do not depend on `/last30days` at runtime. Reference it only as a design benchmark for source breadth and synthesis discipline.
- Public registries and niche datasets that do not have native Deepline tools are still valid sources through generic web/search/extraction routes. For example, the NPI registry for healthcare provider taxonomy can be discovered and pulled through generic web/API search and extraction even when no native `npi` tool exists. Classify this as `available through generic route`, not as an unusable gap.
- Every recommended source must be classified as `native`, `available through generic route`, `private connector`, or `missing provider to add`.

## Start Here

1. Read `references/source-map.md`.
2. For GTM use cases, also read `references/last30days-gtm-corpus.md`; it summarizes the relevant saved `last30days` runs and the source patterns they proved useful.
3. If the task asks for query design, source fanout, or `last30days` parity, also read `references/query-design.md` and `references/fanout-consolidation.md`.
4. If the task is GTM/prospecting/enrichment, also read `../deepline-gtm/SKILL.md` and the sub-doc it routes to.
5. If the task asks about existing warehouse metrics or RevOps analytics, also read `../deepline-analytics/SKILL.md`.
6. Verify the latest upstream `last30days` release when using it as a design reference:

```bash
git ls-remote --tags https://github.com/mvanhorn/last30days-skill.git | tail -20
```

Do not copy `last30days` local scripts into Deepline and do not call it as a required sub-skill. Use it for source taxonomy and output discipline, then route execution through Deepline tools, plays, workflows, and private-data connectors.

## Optional Skill Handoffs

This skill owns pre-research and source planning. It may hand off after the source plan is clear:

- `deepline-gtm`: execute GTM sourcing, enrichment, waterfalls, personalization, contact discovery, or CRM activation.
- `deepline-analytics`: query warehouse/semantic-layer metrics and RevOps/customer datasets.
- `deepline-plays`: build, wrap, fork, run, inspect, or automate the final repeatable workflow/play.
- Similar community research skills such as `last30days`: design reference only, never a dependency for Deepline execution.

## Standard Flow

### 1. Parse The Research Job

Extract:

- `OBJECTIVE`: what decision or output the research should support
- `ENTITY_SCOPE`: companies, people, markets, accounts, customers, workflows, competitors, or topics
- `TIME_WINDOW`: default to last 30 days for trend/community research; preserve user-provided windows
- `PRIVATE_SOURCES`: CRM, warehouse, product events, workflow runs, support/calls, sheets, user CSVs
- `PUBLIC_SOURCES`: web, social, jobs, ads, technographics, funding, news, communities, app stores, directories
- `DATASET_LEADS`: public registries, open datasets, papers, GitHub repos, government records, niche directories, or platform posts that point to materializable data
- `CUSTOM_LANGUAGE_OUTPUTS`: outbound snippets, ad hooks, landing-page copy, objection language, category positioning, call scripts, lead magnets, or CRM personalization fields
- `OUTPUT`: source plan, workflow design, CSV schema, play spec, or final research brief

Tell the user the parsed scope before provider calls.

### 2. Publish A Session Plan

Before tool execution:

```bash
deepline session start --steps '["Parse segment","Run public-source fanout","Find hidden datasets","Synthesize what matters","Search Deepline routes","Estimate cost","Recommend workflow handoff"]' --user-prompt "Original user request"
deepline session start --update 0 --status running
```

Keep the Session UI current with `deepline session status --message "..."`.

### 2.5. Prefer External APIs, Not Scraping

Do not default to browser scraping, raw x.com scraping, or unvetted actors. Prefer managed external APIs and private connectors:

| Source family | Preferred provider | Credential needed | Notes |
| --- | --- | --- | --- |
| Reddit threads/comments | `scrapecreators` | Deepline integration API key | Required for managed Reddit comments/thread coverage. |
| TikTok / Instagram / YouTube fallback | `scrapecreators` | Deepline integration API key | Preferred managed API for captions, engagement, and transcript fallback. Search ScrapeCreators unfiltered when profile/contact tools matter; some profile tools are categorized as `admin`, not `research`. |
| X/Twitter | `twitterapi` | Deepline integration API key | Managed X/Twitter search; avoids scraping x.com. |
| Web/news/docs | `serper` | Deepline integration API key or `SERPER_API_KEY` for server-owned dev/prod use | Search API, not search-page scraping. |
| Web extraction fallback | `firecrawl` or `exa` | Deepline integration API key | Use after URL discovery; do not use for blind scrape-at-scale. |
| Hacker News | `hackernews` | none | Public Algolia API. |
| Bluesky | `bluesky` | none | Public AppView API. |
| CRM/private | Salesforce, HubSpot, Attio | Deepline OAuth/private connector | Query customer-authorized APIs, not UI scraping. |
| Warehouse/product/workflow | Snowflake/customer DB/workflow runtime | Deepline private connector | Use scoped warehouse/runtime access. |
| Last-resort social actor fallback | `apify` | Deepline integration API key | Optional fallback only after explicit approval and provider gap status. |

Treat any route not covered by a described Deepline tool contract, key/auth plan, test endpoint, and Deepline-facing pricing as unapproved until after the public research synthesis is complete.

### 3. Run Public-Source Fanout First

Before provider routing, run a `last30days`-style public discovery pass. The goal is to produce the research synthesis first: what public evidence, communities, registries, directories, reviews, posts, docs, and datasets actually teach us about the GTM problem.

Search across:

- community/social: Reddit threads/comments, X/Twitter, LinkedIn posts if available, YouTube, TikTok, Instagram, HN, Bluesky, Polymarket when relevant
- web/source discovery: news, blogs, docs, review sites, directories, associations, forums, GitHub, public data inventories
- public records and niche datasets: registries, licenses, inspections, permits, government datasets, open CSVs/APIs, professional directories, accreditation/member lists
- market-language sources: reviews, comments, clinic/business websites, job posts, competitor pages, support/community language

This pass is search-driven, not recall-driven. Issue real queries. For any vertical dataset, run at minimum these query shapes and read the top results before writing the source line:

- `"<vertical> <entity> registry OR bulk data OR dataset download"` — find the authoritative file
- `"<dataset name> download"` / `site:data.gov <vertical>` — find the canonical URL and any mirror
- `"<dataset name> parser github"` / `"<dataset name> python"` — find an existing parser/repo so you don't reinvent extraction
- `"<vertical> NAICS code"` + `BLS QCEW <NAICS>` / Census County Business Patterns — free establishment counts and sizing

For each useful source lead, record:

- why it matters
- **exact artifact**: the specific file/endpoint name, canonical URL, mirror, and any open-source parser/repo (not just "the X bulk feed" or "search Google") — see Non-Negotiables and the Artifact Resolution Gate (§4.55)
- whether it can become rows
- stable join keys such as NPI, CRD, USDOT#, NAICS, domain, address, phone, license id, provider id, LinkedIn URL, or CRM account id
- extraction risks and likely false-positive patterns

Do not stop at "Serper can search this." Search tools are routes; the deliverable is the public source or dataset discovered through them. If you find yourself writing a dataset name you did not just see in a search result, stop and search for it.

### 3.5. Use The Deepline Pre-Research API After Public Synthesis

When running inside Deepline or the V2 SDK, use the native planning endpoint only after the public-source fanout has produced a first synthesis and source map. The API is for translating the research into Deepline routes, gaps, approval gates, and cost, not for replacing the research pass:

```bash
curl -s "$DEEPLINE_API_BASE_URL/api/v2/pre-research/plan" \
  -H "Authorization: Bearer $DEEPLINE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"objective":"best GTM data sources for SMB consumer services companies","depth":"deep"}'
```

Agent validation endpoint:

```bash
curl -s "$DEEPLINE_API_BASE_URL/api/v2/pre-research/test" \
  -H "Authorization: Bearer $DEEPLINE_API_KEY"
```

The endpoint returns the query plan, source coverage, current Deepline tool candidates, sanitized Deepline-facing pricing metadata, explicit provider gaps, and approval gate. It does not execute paid provider calls.

For SDK V2 users, this is the recipe-backed path:

```bash
deepline quickstart
# Pick "Pre-Research Source Plan"
```

The selected recipe prompts the agent to call `/api/v2/pre-research/plan`, inspect the returned `providerRequirements`, and only then decide whether to run probes or build a play.

### 4. Search For Deepline Candidate Tools

Run several focused searches, usually in parallel:

```bash
deepline tools search "web search news source discovery" --categories research --search_terms "web search,news,recency,source discovery"
deepline tools search "social posts reddit x twitter youtube tiktok instagram" --categories research --search_terms "social posts,reddit,x twitter,youtube,tiktok,instagram"
deepline tools search scrapecreators --json
deepline tools search "facebook profile email scrapecreators" --json
deepline tools search "instagram profile bio links scrapecreators" --json
deepline tools search "company dataset firmographics funding technographics jobs" --categories company_search --search_terms "company dataset,firmographics,funding,technographics,jobs"
deepline tools search "crm warehouse workflow session usage" --categories admin --search_terms "crm,warehouse,workflow,session,usage"
```

For CRM/private data, also search by provider name when relevant:

```bash
deepline tools search salesforce
deepline tools search hubspot
deepline tools search attio
deepline tools search snowflake
```

### 4.25. Design Queries Before Running Tools

Do not send the raw user prompt to every provider. Generate a source-specific query plan first:

```bash
for dir in \
  "$PWD/.skills/deepline-pre-research" \
  "$HOME/.claude/skills/deepline-pre-research" \
  "$HOME/.agents/skills/deepline-pre-research"; do
  [ -f "$dir/scripts/query_design.py" ] && SKILL_ROOT="$dir" && break
done
[ -n "${SKILL_ROOT:-}" ] || { echo "Could not find deepline-pre-research skill root" >&2; exit 1; }
python3 "$SKILL_ROOT/scripts/query_design.py" "$OBJECTIVE" --depth default
```

Use the plan to decide:

- query type and source tiers
- cleaned core subject
- Reddit global/review/problem variants
- X literal keyword, compound-term, shorter-keyword, and strongest-token fallbacks
- video/transcript and caption queries
- web, dataset, and GitHub discovery queries
- CRM, warehouse, workflow, support, and custom-language private queries
- supplemental keys to extract after phase-one retrieval

For production Deepline implementation, port this helper to the runtime language or call equivalent logic before `deepline tools execute`/`deepline enrich`.

### 4.5. Required Coverage Gate

Before recommending a plan, check every required source family in `references/source-map.md`:

- community/social discussion
- custom language and messaging evidence
- web/news/search and URL extraction
- video/transcript sources
- prediction/market/community ranking sources
- dataset-discovery leads from social/community results
- company/account datasets
- person/contact datasets
- jobs/hiring/technographic/funding signals
- CRM/private datasets
- warehouse/product/workflow datasets

For each family, mark one of:

- `native`: a Deepline tool/play exists and can be described
- `generic route`: use `apify`, `serper`, `exa`, `parallel`, `firecrawl`, or `deeplineagent`
- `private connector`: use CRM, warehouse, workflow, or customer dataset access
- `gap`: provider/action should be added before Deepline can replicate that part well

Do not skip a family just because it is inconvenient. Missing coverage is part of the pre-research output.

### 4.55. Artifact Resolution Gate

Before writing the report, verify every materializable public dataset has been resolved from a *family* to an *artifact*. For each recommended public dataset/registry, confirm you can fill this row from something you actually searched or fetched this session:

| Dataset | Exact file/endpoint | Canonical URL | Easier mirror | OSS parser/repo | Vertical stat registry (NAICS/QCEW/CBP) |
| --- | --- | --- | --- | --- | --- |

Rules:

- A cell you filled from memory instead of a live result is not verified. Search for it.
- `n/a` is allowed only when the artifact genuinely does not exist (e.g. no public bulk file, no known parser) — and you must have searched to establish that, not assumed it.
- If the user's ask contains "dataset", "github", "repo", "download", "the file", "the data", or a request to hand something over, this gate is the primary deliverable, not an appendix: lead the report with the resolved artifacts.
- The government statistical registry column (BLS QCEW + NAICS, Census County Business Patterns) is required for any US industry vertical — it is free establishment-count and sizing data that public-source fanout consistently leaves on the table.

A report that names "the SEC ADV bulk feed" fails this gate; a report that names `IA_FIRM_SEC_Feed_YYYY_MM_DD.xml.gz` at its sec.gov URL, notes the data.gov mirror, and links an existing ADV parser repo passes it.

When you cite a parser/repo alongside a dataset, name the **exact input file that repo actually consumes** — check its README. A vertical often has multiple real distributions (e.g. SEC publishes both the `IA_FIRM_SEC_Feed_*.xml.gz` bulk feed and the `ia<MMDDYY>.zip` IAPD compilation); pairing a parser with the wrong-but-real file is a precision error, not a fabrication, but it still breaks the handoff. Match the parser to its file.

### 4.6. Fanout And Consolidation Gate

For `last30days` parity, preserve the public-source fanout mechanics described in `references/fanout-consolidation.md`:

- broad parallel search before synthesis
- supplemental searches from discovered handles, subreddits, domains, datasets, CRM ids, account lists, workflow ids, and persona language
- common evidence rows before scoring
- relevance, recency, engagement, source-quality, materializability, private-outcome, join-confidence, custom-language, and cost/coverage scoring
- URL/source-id/text dedupe plus company/person/dataset identity joins
- coverage nudges for searched, weak, errored, missing-credential, unavailable, and not-relevant sources

If implementation coverage is being audited, run the local evaluator:

```bash
for dir in \
  "$PWD/.skills/deepline-pre-research" \
  "$HOME/.claude/skills/deepline-pre-research" \
  "$HOME/.agents/skills/deepline-pre-research"; do
  [ -f "$dir/scripts/evaluate_examples.py" ] && SKILL_ROOT="$dir" && break
done
[ -n "${SKILL_ROOT:-}" ] || { echo "Could not find deepline-pre-research skill root" >&2; exit 1; }
python3 "$SKILL_ROOT/scripts/evaluate_examples.py"
```

Use `evals/side-by-side.md` to compare saved `last30days` examples against this skill's coverage contract.

For standalone eval harness runs, write reports into the harness output directory:

```bash
python3 "$SKILL_ROOT/scripts/evaluate_examples.py" \
  --out-md "${OUTPUT_DIR:-$SKILL_ROOT/evals}/side_by_side_pre_research.md" \
  --out-json "${OUTPUT_DIR:-$SKILL_ROOT/evals}/side_by_side_pre_research.json"
python3 "$SKILL_ROOT/scripts/evaluate_public_private_corpus.py" \
  --out-md "${OUTPUT_DIR:-$SKILL_ROOT/evals}/public_private_corpus_results.md" \
  --out-json "${OUTPUT_DIR:-$SKILL_ROOT/evals}/public_private_corpus_results.json"
```

### 5. Describe Before Pricing Or Execution

For every candidate, inspect the live contract:

```bash
deepline tools describe <tool-id> --json
```

Record:

- input fields and required identifiers
- output evidence fields and citations
- pricing summary, billing basis, and whether BYOK changes Deepline credit cost
- rate limits, async behavior, and sample payloads
- extraction quality risks and identity-matching requirements

If a source family is not present in Deepline, mark it as a provider gap and propose the integration path.

### 6. Probe Coverage When Useful

Use free/low-cost probes first. For paid probes, ask before running unless the user already approved a specific pilot budget.

Good probe shapes:

- one entity, one query, or one row
- `limit: 1` or `numResults: 3`
- one source per probe so coverage and cost are attributable
- saved raw output path or run id for later workflow design

At scale, use `deepline enrich` rather than ad hoc loops so results are inspectable in Playground.

### 7. Return A Last30days-Style GTM Research Report

Use the same output discipline as `last30days` agent mode. The report should feel like a real research result, not a bespoke segment-analysis template or provider catalog.

```markdown
## Research Report: <topic>
Generated: <date> | Sources: Reddit, X, YouTube, TikTok, Instagram, HN, Polymarket, Web, Public registries, Deepline catalog

### Key Findings
- <3-5 highest-signal findings grounded in public/source evidence>

### What I learned

**<Theme 1>** - <1-2 sentences about the segment, source, buyer language, or dataset reality. Cite sparingly using source names, handles, communities, registries, or domains.>

**<Theme 2>** - <1-2 sentences.>

**<Theme 3>** - <1-2 sentences.>

KEY PATTERNS from the research:
1. <Pattern, source family, and why it matters for GTM>
2. <Pattern, source family, and why it matters for GTM>
3. <Pattern, source family, and why it matters for GTM>

### GTM Data Sources Found
| Source family | Best source / route | Status | Rows / join keys | Caveat |
| --- | --- | --- | --- | --- |

### Materializable Datasets (exact artifacts)
| Dataset | Exact file/endpoint | URL | Mirror | OSS parser/repo | Stat registry (NAICS/QCEW/CBP) |
| --- | --- | --- | --- | --- | --- |
<!-- One row per public dataset you can turn into rows. No "family" placeholders — exact filename, canonical URL, mirror, and an existing parser repo where one exists. This table is the answer when the ask is "give me the dataset/github". -->


### Market Language
| Source | What to extract | How to use it | Guardrail |
| --- | --- | --- | --- |

### Proprietary Data To Join Later
| Dataset | Owner / connector | Join key | Why it changes the answer |
| --- | --- | --- | --- |

### Deepline Route
| Public source family | Route status | Deepline route | Probe needed | Cost basis |
| --- | --- | --- | --- | --- |

### Gaps To Add
| Missing source | Why it matters | Suggested provider/integration | Required fields |
| --- | --- | --- | --- |

### Recommended Workflow
1. <first retrieval/probe>
2. <second retrieval/probe>
3. <synthesis/scoring/join step>

### Stats
---
✅ All agents reported back!
├─ <source family>: <count / coverage / engagement when available>
├─ <source family>: <count / coverage / engagement when available>
├─ 🌐 Web/Public data: <pages, registries, directories, datasets>
└─ 🗣️ Top sources: <handles, communities, registries, domains, datasets>
---

### Cost Estimate
- Pilot: <credits or range>
- Full run: <credits or range and assumptions>
- Unknowns: <what must be described/probed before quoting>
```

For `--agent`-style or non-interactive use, stop after the report. For interactive use, end with a short, specific invitation based on the actual findings, mirroring `last30days`:

```markdown
---
I'm now an expert on <topic>. Some things I can help with:
- <specific follow-up grounded in the findings>
- <specific workflow/probe to run next>
- <specific segment or source to go deeper on>
```

If the user wants execution, hand off to `deepline-gtm` after this output.

Match `last30days` cleanup rules:

- Omit any source line that returned zero results. Do not show "0 results", "0 stories", or "no results".
- Do not append a separate trailing "Sources used" section.
- Do not paste raw URLs or Markdown source links in the report body or stats. Use clean source names inline, such as `NPI Registry`, `Google Maps`, `r/SaaS`, `G2`, `Meta docs`, or `Hike Medical site`.
- Citations should prove the research is real without turning the report into a bibliography. Prefer handles, communities, source names, registries, domains, and doc names.
- Use the `last30days` stats block style exactly: start with `✅ All agents reported back!`, use `├─`, `└─`, and `│` separators where useful, and include source emojis when they clarify the source family.
- Keep the Deepline route and cost after the research synthesis, never before it.

## Approval Gate

Before any full paid run, include:

- providers/tools
- pilot result or reason a pilot is not possible
- full-run scope
- Deepline credit estimate/range
- max spend cap
- exact approval question

If the user approves, execute through `deepline enrich`, `deepline tools execute`, or a Deepline play/workflow as appropriate.

## Finish Criteria

The task is done only when the user has:

- a ranked data-source map
- a `last30days`-style GTM research synthesis grounded in public sources
- **every materializable dataset resolved to an exact artifact** (file/endpoint name + canonical URL + mirror + OSS parser + vertical NAICS/QCEW), verified via live search this session — not named from memory (see §4.55)
- live tool ids or explicit provider gaps
- a Deepline-facing cost estimate
- the recommended first workflow/play shape
- any blockers for credentials, private-data access, or missing provider support
