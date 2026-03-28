---
name: gtm-meta-skill
description: "Use this skill for GTM prospecting, enrichment, qualification, and outbound workflows, especially when users mention Deepline, CSV processing, lead/account/contact research, waterfall enrichment, email or LinkedIn lookup, personalization, scoring, or campaign activation. Route CSV-heavy and provider-driven requests through this skill, then rely on linked sub-docs and provider playbooks for execution details. Available providers: adyntel, ai_ark, apify, apollo, attio, builtwith, cloudflare, crustdata, deepline_native, deeplineagent, dropleads, exa, firecrawl, forager, heyreach, hubspot, hunter, icypeas, instantly, leadmagic, lemlist, parallel, peopledatalabs, prospeo, salesforce, serper, smartlead, snowflake, zerobounce."
---

# GTM Meta Skill

Use this skill for prospecting, account research, contact enrichment, verification, lead scoring, personalization, and campaign activation.

## 1) What this skill governs

- Route GTM decisions, safety gates, and provider/quality defaults before execution.
- Keep long command chains and tooling nuance in sub-docs; provider-specific implementation detail in `provider-playbooks/*.md`.
- Provide clear entry points for both paid and non-paid workflows, including `--rows 0:1` one-row pilots.

## Process/goal

Customer is generally trying to go from "I have an ICP" to "Here's a list of prospects with email/linkedin and very personalized content or signals". They may be anywhere in this process, but guide them along.

**Discovery order: companies first, then people.** When the task requires finding contacts at companies matching criteria (portfolio, ICP, hiring signal), discover the company set first, then find people at each company. Do not start with broad people-search queries.

### Documentation hierarchy

- Level 1 (`SKILL.md`): decision model, guardrails, approval gates, links to sub-docs.
- Level 2 (phase docs): [finding-companies-and-contacts.md](finding-companies-and-contacts.md), [enriching-and-researching.md](enriching-and-researching.md), [writing-outreach.md](writing-outreach.md), `prompts.json`.
- Level 2.5 (`recipes/*.md`): step-by-step playbooks for specific tasks (email lookup, LinkedIn resolution, waterfall patterns, contact finding, actor contracts). Search like code with Grep.
- Level 3 (`provider-playbooks/*.md`): provider-specific quirks, cost/quality notes, and fallback behavior.

No-loss rule: moved guidance remains fully documented at its canonical level and is linked from here.



## 2) Read behavior — MANDATORY before any execution

**STOP. Do not call any provider, run any `deepline tools execute`, or write any search command until you have opened the correct sub-doc for your task.**

These skill docs and sub-docs are not generic documentation — they are distilled from hundreds of real runs and encode exactly what works, what fails, and why. They contain validated parameter schemas, correct filter syntax, parallel execution patterns, tested sample payloads, and known pitfalls that took many iterations to discover. Think of them as shortcuts: reading a doc for 5 seconds saves you from 10 failed tool calls, wasted credits, and garbage output. Every time an agent skips reading the docs and tries to "figure it out" from first principles, it re-discovers the same failure modes that are already documented and solved.

SKILL.md is the routing layer — it tells you WHERE to go, not HOW to execute. The sub-docs and task-specific skills contain the HOW. Without them you will guess parameters, pick wrong providers, run searches sequentially instead of in parallel, and produce garbage results. This has happened repeatedly.

### Open the right doc BEFORE executing

**This is not optional.** Read the matching doc. Do not skip this step. Do not "just try Apollo real quick" or "just run one search to see." These docs exist because the correct approach was non-obvious and had to be learned through trial and error — they are shortcuts that let you skip straight to what works.

!important READING MULTIPLE DOCS IS A GREAT IDEA AND OFTEN SUPER ESSENTIAL. JUST READ MORE.

**Routing rules — match your task to a doc and READ IT:**

| When the task involves... | You MUST read this doc first | What it gives you (that SKILL.md doesn't) |
|---|---|---|
| **Finding companies, finding people, building lead lists, prospecting, portfolio/VC sourcing, contact finding at known companies, coverage completion at scale** | [finding-companies-and-contacts.md](finding-companies-and-contacts.md) | Provider filter schemas, parallel execution patterns, provider mix tables, role-based search rules, subagent orchestration, at-scale coverage completion, portfolio/VC shortcuts, contact finding patterns. |
| **Researching companies or people, understanding what they build, figuring out use cases, personalizing based on mission/product/industry, enriching a CSV, adding data columns, waterfall enrichment, finding emails/phones/LinkedIn, coalescing data, custom signals, `run_javascript` / `deeplineagent` steps, Apify actors — any task that adds or transforms row-level data** | [enriching-and-researching.md](enriching-and-researching.md) | `deepline enrich` syntax and all flags. Waterfall patterns with fallback chains. `run_javascript` / `deeplineagent` routing. Multi-pass pipeline patterns (research pass → generation pass). Coalescing patterns. Email/phone/LinkedIn waterfall orders. Custom signal buckets. Apify actor selection. GTM definitions and defaults. |
| **Writing cold emails, personalizing outreach, lead scoring, qualification, sequence design, campaign copy, inspecting CSVs in Playground.** If the task also requires researching companies/people to inform the writing, read [enriching-and-researching.md](enriching-and-researching.md) too — it has the multi-pass pipeline pattern. | [writing-outreach.md](writing-outreach.md) | Prompt templates from `prompts.json`. Scoring rubrics. Email length/tone/structure rules. Personalization patterns. Qualification frameworks. Playground inspection commands. |

### Recipes: step-by-step playbooks for specific tasks (check before executing)

The `recipes/` directory contains battle-tested playbooks. **Before you start executing, scan this list and read any recipe that matches your task.**

When a recipe matches: **follow it step-by-step as your execution plan.** Recipes encode hard-won sequencing and provider choices — trust them over generic guidance or your own intuition. If the user's request doesn't perfectly fit, adapt the recipe using the phase docs above, but keep the recipe's structure and ordering as your baseline.

| Recipe | Use when... |
|---|---|
| `build-tam.md` | Building a total addressable market list or large company list from ICP criteria |
| `enriching-and-researching.md` | Finding contacts/people at known companies via the persona lookup play |
| `enriching-and-researching.md` | Contact-to-email routing and native email recovery plays |
| `actor-contracts.md` | Apify actor selection, known actor IDs, input schemas |
| `enriching-and-researching.md` | Social listening — scrape LinkedIn post engagers (`linkedin_post_to_engagers`) and ICP-qualify them (`engagers_to_icp_qualification`) |

If none match, grep for more specific keywords: `Grep pattern="<keyword>" path="<directory containing this SKILL.md>/recipes/" glob="*.md" output_mode="files_with_matches"`

### Data

- When the user hands you a CSV, run `deepline csv show --csv <path> --summary` first to understand its shape (row count, columns, sample values) before deciding how to process it.
- **NEVER read a large CSV into context with the Read tool.** Reading CSV rows into the conversation window exhausts context and produces zero output. This is the single most common failure mode.
- Use `deepline enrich` for any row-by-row processing (enrichment, rewriting, research, scoring).
- To explore or understand CSV content without loading it, use `deepline csv show --csv <path> --rows 0:2` for a two-row sample, or spawn an Explore subagent to answer questions about the data.

### Tools

For signal-driven discovery (investor, funding, hiring, headcount, industry, geo, tech stack, compliance), start with `deepline tools search`. Do not guess fields.

Search 2-4 synonyms, execute in parallel:

```bash
deepline tools search investor
deepline tools search investor --prefix crustdata
deepline tools search --categories company_search --search_terms "structured filters,icp"
deepline tools search --categories people_search --search_terms "title filters,linkedin"
```

## 2.5) Session UI plan — MANDATORY for every task

**Always** publish your execution plan to the Session UI before running any commands. This is not optional — users monitor progress in real time via the Session UI. Without it, the UI shows nothing and users have no visibility.

```bash
# Post your plan (accepts JSON array of step labels)
deepline session plan --steps '["Inspect CSV and understand shape","Search for email finder tools","Run pilot on rows 0:1","Get approval for full run","Execute full enrichment","Post-run validation and delivery"]'

# As you complete each step, update its status (0-indexed)
deepline session plan --update 0 --status completed
deepline session plan --update 1 --status running
deepline session plan --update 1 --status completed
deepline session plan --update 2 --status running
# On error:
deepline session plan --update 2 --status error
```

Valid step statuses: `pending`, `running`, `completed`, `error`, `skipped`.

### Live status updates within a step

As you work through a running step, send status updates to show what you're currently doing. This is for emergent work the plan couldn't predict upfront (parsing responses, falling back to alternative providers, extracting data, etc.).

```bash
# While a step is running, send status updates (attaches to the currently-running step)
deepline session status --message "Extracting company domains from Apollo response"
deepline session status --message "LeadMagic returned no results — falling back to ZeroBounce"
deepline session status --message "Validating 23 catch-all emails"

# Optionally target a specific step by index
deepline session status --message "Retrying with different params" --step-index 2
```

Each new status message marks the previous one as done and appears as the active sub-step. These are lightweight — use them freely whenever you're doing something the user would want to see.

Rules:
- Post the plan **before** running any enrichment/tool commands. This is step zero of every task.
- Update steps as you go — mark `running` when starting, `completed` or `error` when done.
- Send `session status` messages during step execution to show what you're currently working on.
- Keep step labels short and descriptive (what, not how).
- If your plan changes mid-execution, re-post with `--steps` to replace the old plan.
- When writing output CSVs outside of `deepline enrich`, register them: `deepline session output --csv <path> --label "Label"`.

### Tool search categories

Use category filters when tool type matters more than provider breadth. Common categories:
- `company_search`: account/company discovery tools
- `people_search`: people/contact discovery tools
- `company_enrich`: company enrichment on known companies
- `people_enrich`: person/contact enrichment on known people
- `email_verify`: email verification / deliverability
- `email_finder`: email lookup / discovery
- `phone_finder`: phone lookup / discovery
- `research`: company research, ad intel, job search, technographics, web research
- `automation`: workflow-style tools, browser/actor runs, batch automation
- `outbound_tools`: all Lemlist/Smartlead/Instantly/HeyReach style actions
- `autocomplete`: canonical filter value discovery before search
- `admin`: credits, monitoring, logs, schemas, local/dev utilities

Use `--search_terms` for extra ranking hints like `structured filters`, `title filters`, `api native`, `autocomplete`, or `bulk`.

Good:
- `deepline tools search --categories company_search --search_terms "investors,funding"`
- `deepline tools search --categories research --search_terms "ads,technographics"`

Avoid:
- `deepline tools search stuff`
- `deepline tools search search across filters`

## 3) Core policy defaults

### 3.1 Definitions and defaults

GTM time windows, thresholds, and interpretation rules are defined in the Definitions section of [enriching-and-researching.md](enriching-and-researching.md).

## Provider Playbooks

- [adyntel playbook](provider-playbooks/adyntel.md)
  Summary: Use channel-native ad endpoints first, then synthesize cross-channel insights. Keep domains normalized and remember Adyntel bills per request except free polling endpoints.
  Last reviewed: 2026-02-27

- [ai_ark playbook](provider-playbooks/ai_ark.md)
  Summary: Use company and people search for prospecting, reverse lookup for identity resolution, mobile phone finder only for strong matches, and async export or email-finder flows when you need verified emails.
  Last reviewed: 2026-03-16

- [apify playbook](provider-playbooks/apify.md)
  Summary: Prefer sync run (`apify_run_actor_sync`) for actor execution. Use async run plus polling only when you need non-blocking execution. Reach for Apify before call_ai/WebSearch when the source is already known and a source-specific actor exists.
  Last reviewed: 2026-02-11

- [apollo playbook](provider-playbooks/apollo.md)
  Summary: Cheap but mediocre quality people/company search with include_similar_titles=true unless strict mode is explicitly requested.
  Last reviewed: 2026-02-11

- [attio playbook](provider-playbooks/attio.md)
  Summary: Use assert_* operations for upserts, query_* operations for filtered reads, standard-object wrappers when you know the Attio object family, and webhook subscriptions with typed event names when you need realtime sync.
  Last reviewed: 2026-03-20

- [builtwith playbook](provider-playbooks/builtwith.md)
  Summary: Use domain_lookup for live stack inspection, vector_search to discover the right tech label before lists/trends, and bulk_domain_lookup for row-heavy domain batches.
  Last reviewed: 2026-03-21

- [cloudflare playbook](provider-playbooks/cloudflare.md)
  Summary: Use cloudflare_crawl to crawl websites and extract content as markdown, HTML, or JSON. Returns partial results on timeout — check timedOut field. Browser rendering is enabled by default.
  Last reviewed: 2026-03-11

- [crustdata playbook](provider-playbooks/crustdata.md)
  Summary: Start with free autocomplete and default to fuzzy contains operators `(.)` for higher recall. Use ISO-3 country codes, prefer crunchbase_categories over linkedin_industries for niche verticals, and use employee_count_range for filtering instead of employee_metrics.latest_count.
  Last reviewed: 2026-02-11

- [deepline_native playbook](provider-playbooks/deepline_native.md)
  Summary: Launcher actions wait for completion and return final payloads with job_id; finder actions remain available for explicit polling.
  Last reviewed: 2026-02-23

- [deeplineagent playbook](provider-playbooks/deeplineagent.md)
  Summary: Use Vercel AI Gateway for plain inference or multi-step research with Deepline-managed tools and billing.
  Last reviewed: 2026-03-22

- [dropleads playbook](provider-playbooks/dropleads.md)
  Summary: Use Prime-DB search/count first to scope segments efficiently, then run finder/verifier steps only on shortlisted records. Prefer companyDomains over companyNames, split multi-word keywords into separate tokens, and use broad jobTitles plus seniority instead of exact-title matching.
  Last reviewed: 2026-02-26

- [exa playbook](provider-playbooks/exa.md)
  Summary: Use search/contents before answer for auditable retrieval, then synthesize with explicit citations. Write natural-language queries, expect discard/noise, and avoid mixing category searches with includeDomains-style source scoping.
  Last reviewed: 2026-02-11

- [firecrawl playbook](provider-playbooks/firecrawl.md)
  Summary: Web scraping, crawling, search, and AI extraction. Use firecrawl_scrape for single pages, firecrawl_search for web search + scraping, firecrawl_map for URL discovery, firecrawl_crawl for multi-page crawls, firecrawl_extract for structured extraction.
  Last reviewed: 2026-03-11

- [forager playbook](provider-playbooks/forager.md)
  Summary: Use totals endpoints first (free) to estimate volume, then search/lookup with reveal flags for contacts. Strong for verified mobiles.
  Last reviewed: 2026-02-28

- [heyreach playbook](provider-playbooks/heyreach.md)
  Summary: Resolve campaign IDs first, then batch inserts and confirm campaign stats after writes.
  Last reviewed: 2026-02-11

- [hubspot playbook](provider-playbooks/hubspot.md)
  Summary: Use list/get/search for flexible CRM reads, batch operations for large syncs, and the schema, pipeline, owner, and association tools to discover HubSpot-specific IDs before writing.
  Last reviewed: 2026-03-20

- [hunter playbook](provider-playbooks/hunter.md)
  Summary: Use discover for free ICP shaping first, then domain/email finder for credit-efficient contact discovery, and verifier as the final send gate.
  Last reviewed: 2026-02-24

- [icypeas playbook](provider-playbooks/icypeas.md)
  Summary: Use email-search for individual email discovery, bulk-search for volume. Scrape LinkedIn profiles for enrichment. Find-people for prospecting with 16 filters. Count endpoints are free.
  Last reviewed: 2026-02-28

- [instantly playbook](provider-playbooks/instantly.md)
  Summary: List campaigns first, then add contacts in controlled batches and verify downstream stats.
  Last reviewed: 2026-02-11

- [leadmagic playbook](provider-playbooks/leadmagic.md)
  Summary: Treat validation as gatekeeper and run email-pattern waterfalls before escalating to deeper enrichment.
  Last reviewed: 2026-02-11

- [lemlist playbook](provider-playbooks/lemlist.md)
  Summary: List campaign inventory first and push contacts in small batches with post-write stat checks.
  Last reviewed: 2026-03-01

- [parallel playbook](provider-playbooks/parallel.md)
  Summary: Prefer run-task/search/extract primitives and avoid monitor/stream complexity for agent workflows.
  Last reviewed: 2026-02-11

- [peopledatalabs playbook](provider-playbooks/peopledatalabs.md)
  Summary: Use clean/autocomplete helpers to normalize input before costly person/company search and enrich calls. Treat company search as a last-resort structured path, and prefer payload files or heredocs for non-trivial SQL-style queries.
  Last reviewed: 2026-02-11

- [prospeo playbook](provider-playbooks/prospeo.md)
  Summary: Use enrich-person for individual contacts, search-person for prospecting with 30+ filters, and search-company for account-level lists.
  Last reviewed: 2026-02-28

- [salesforce playbook](provider-playbooks/salesforce.md)
  Summary: Use field inspection before custom writes, object-specific create/update/delete tools for standard CRM records, and list tools for incremental reads with pagination handoff.
  Last reviewed: 2026-03-20

- [serper playbook](provider-playbooks/serper.md)
  Summary: Use Serper for broad live Google web search and local/maps recall. Strong first step before structured extraction or enrichment.
  Last reviewed: 2026-03-23

- [smartlead playbook](provider-playbooks/smartlead.md)
  Summary: List campaigns first, then push leads with Smartlead field names and confirm campaign stats afterward.
  Last reviewed: 2026-03-05

- [zerobounce playbook](provider-playbooks/zerobounce.md)
  Summary: Use as final email validation gate before outbound sends. Check sub_status for granular failure reasons. Use batch for 5+ emails.
  Last reviewed: 2026-02-28

- Apply defaults when user input is absent.
- User-specified values always override defaults.
- In approval messages, list active defaults as assumptions.

### 3.2 Output policy and User Interaction Pattern

- Always use `deepline enrich` for list enrichment or discovery at scale (>5 rows). It auto-opens a visual playground sheet so user can inspect rows, re-run blocks, and iterate.
- Even for company → ICP person flows, enrich works: search and filter as part of the process, with providers like Apify to guide.
- Even when you don't have a CSV, create one and use deepline enrich.
- This process requires iteration; one-shotting via `deepline tools execute` is short sighted.
- For `run_javascript` in `deepline enrich`, put JS in `payload.code`; the current row is auto-injected as `row` at runtime, so you usually should not pass `row` yourself.
- If a command created CSV outside enrich, register it with the Session UI so a table card appears: `deepline session output --csv <csv_path> --label "My Results"`. This is the lightweight alternative to `deepline enrich` for surfacing output in the Session UI.
- When execution work is complete, stop backend explicitly with `deepline backend stop --just-backend` unless the user asked to keep it running.
- In chat, send the file path + playground status, not pasted CSV rows, unless explicitly requested.
- Preserve lineage columns (especially `_metadata`) end-to-end. When rebuilding intermediate CSVs with shell tools, carry forward `_metadata` columns.
- Never enrich a user-provided or source CSV in-place. Use `--output` to write to your working directory on the first pass, then `--in-place` on that output for subsequent passes. `--in-place` is for iterating on your own prior outputs — never on source files.
- For reruns, keep successful existing cells by default; use `--with-force <alias>` only for targeted recompute.

See [enriching-and-researching.md](enriching-and-researching.md) for `deepline csv` commands, pre-flight/post-run script templates, and inspection details.

### 3.3 Final file + playground check (light)

- Keep one intended final CSV path: `FINAL_CSV="${OUTPUT_DIR:-/tmp}/<requested_filename>.csv"`
- Before finishing: use the post-run inspection script pattern from [enriching-and-researching.md](enriching-and-researching.md). Run it once instead of separate checks.
- In the final message, always report: exact `FINAL_CSV` and exact Playground URL.
- Before closing the session, follow the Section 7 consent step for session sharing.

## 4) Credit and approval gate (paid actions)

### 4.1 Required run order

1. Pilot on a narrow scope (example `--rows 0:1` for one row).
2. Request explicit approval.
3. Run full scope only after approval.

### 4.2 Execution sizing

- Use smaller sequential commands first.
- Keep limits low and windows bounded before scaling.
- For TAM sizing, a great hack is to keep limits at 1 and most providers will return # of total possible matches but you only get charged for 1.
- Do not depend on monthly caps as a hard risk control.

### 4.2.1 Over-provision, then filter — never chase missing rows

When the user asks for N rows, start with ~1.4×N (e.g., 35 for 25). Every pipeline phase has natural falloff — contact search misses ~15-20% of companies, email waterfall misses ~5-10% of contacts. Fighting to complete the hard rows is almost always a waste: the companies that providers can't find contacts for are the same ones that won't have email coverage either.

**Do this:**
1. Pull more candidates than needed at the top of funnel.
2. Run the full pipeline (contacts → emails → outbound).
3. At the end, filter to the best N complete rows and deliver those.
4. Drop incomplete rows — don't retry or manually patch them.

**Do NOT do this:**
- Trim results to exactly N before running the pipeline.
- Spend turns retrying failed lookups with fallback providers, `deeplineagent` research passes, or manual patching.
- Run enrichment on all rows just to fill gaps in a few (especially broad `deeplineagent` research passes).

Provider coverage is a property of the company, not something you can overcome with more effort. Tiny startups with 5 people will have zero coverage across all providers — no amount of retrying changes that. Over-provision at the top and let incomplete rows fall off naturally.

### 4.3 Approval message content

Include all of:

1. Provider(s)
2. Pilot summary and observed behavior
3. Intent-level assumptions (3–5 one-line bullets)
4. CSV preview from a real `deepline enrich --rows 0:1` one-row pilot
5. Credits estimate / range
6. Full-run scope size
7. Max spend cap
8. Approval question: `Approve full run?`

Note: `deepline enrich` already prints the ASCII preview by default, so use that output directly.

Strict format contract (blocking):

1. Use the exact four section headers: Assumptions, CSV Preview (ASCII), Credits + Scope + Cap, Approval Question.
2. If any required section is missing, remain in `AWAIT_APPROVAL` and do not run paid/cost-unknown actions.
3. Only transition to `FULL_RUN` after an explicit user confirmation to the approval question.
4. `run_javascript` is the non-AI path. `aiinference` is for general classification/structured reasoning, and `deeplineagent` is for context gathering / web research / signal extraction.


Approval template:

```markdown
Assumptions
- <intent assumption 1>
- <intent assumption 2>

CSV Preview (ASCII)
<paste verbatim output from deepline enrich --rows 0:1>
Credits + Scope + Cap
- Provider: <name>
- Estimated credits: <value or range>
- Full-run scope: <rows/items>
- Spend cap: <cap>
- Pilot summary: <one short paragraph>

Approval Question
Approve full run?
```

### 4.4 Mandatory checkpoint

- Must run a real pilot on the exact CSV for full run (`--rows 0:1`, end exclusive).
- Must include ASCII preview verbatim in approval.
- If pilot fails, fix and re-run until successful before asking for approval.
- Before using AskUserQuestion for the approval gate, notify the Session UI so the user knows to check the terminal:
  ```bash
  deepline session alert --message "Approval needed: run enrichment on N rows (~X credits)"
  ```

### 4.5 Billing commands

```bash
deepline billing balance
deepline billing limit
```

When credits at zero, link to https://code.deepline.com/dashboard/billing to top up.
10 credits == $1

## 5) Provider routing (high level)

**Reminder: you should have already read the relevant sub-doc from Section 2 before reaching this point. If you haven't, go back and read it now. This section is a quick-reference summary, NOT a substitute for the sub-docs.**

- **Search / discovery** → You MUST have [finding-companies-and-contacts.md](finding-companies-and-contacts.md) open. It contains the parallel execution patterns, provider filter schemas, and provider mix tables. Start with `deepline tools search <intent>` and execute field-matched provider calls in parallel; when the `deepline-list-builder` subagent is available, use subagent-based parallel search orchestration as the preferred pattern. Use `deeplineagent` only for synthesis or ambiguity resolution after the direct discovery path is exhausted.
- **Enrich / waterfall / coalesce** → You MUST have [enriching-and-researching.md](enriching-and-researching.md) open. It contains `deepline enrich` syntax, waterfall column patterns, and coalescing logic. Default waterfall order: dropleads → hunter → leadmagic → deepline_native → crustdata → peopledatalabs.
- **Custom signals / messaging** → Read [enriching-and-researching.md](enriching-and-researching.md) (custom signals section). Use `run_javascript` for deterministic transforms/template logic and `deeplineagent` for AI work. Start from `prompts.json`.
- **Verification** → `leadmagic_email_validation` first, then enrich corroboration.
- **LinkedIn scraping** → Apify actors, by far the best. Search `actor-contracts.md` for known actor IDs.
- For phone recovery, read [enriching-and-researching.md](enriching-and-researching.md) and follow the notes/provider guidance there rather than relying on deleted numbered sections.

Provider path heuristics:
- Broad first pass: direct tool calls for high-volume discovery.
- Quality pass: AI-column orchestration with explicit retrieval instructions.
- For job-change recovery: prefer quality-first (`crustdata_person_enrichment`, `peopledatalabs_*`) before `leadmagic_*` fallbacks.
- Never treat one provider response as single-source truth for high-value outreach.

## 6) Additional notes

Critical: keep [writing-outreach.md](writing-outreach.md) workflow context active when running any sequence task. It is not optional for ICP-driven messaging.

### Apify actor flow (short canonical policy)

### Operational troubleshooting: rate limits and CLI health

- Use `deepline enrich` for heavy row-by-row work whenever possible. It has built-in rate-limit handling (adaptive retries/backoff) for standard upstream limits. If you are building a homegrown script, assume it does not include the same automatic protection unless you explicitly implement it.
- If enrichment or CLI behavior is unstable, rerun the installer to ensure the latest CLI/client wiring is in place:

```bash
curl -s "https://code.deepline.com/api/v2/cli/install" | bash
```

**Sites requiring auth:** Don't use Apify. Tell the user to use Claude in Chrome or guide them through Inspect Element to get a curl command with headers (user is non-technical).

1. If user provides actor ID/name/URL: use it directly.
2. If not, search `actor-contracts.md` for the actor id, or try deepline tools search.
3. If not present, run discovery search.
4. Avoid rental-priced actors.
5. Pick value-over-quality-fit; when tied, choose best evidence-quality/price balance.
6. Honor `operatorNotes` over public ratings when conflicting.

```bash
deepline tools execute apify_list_store_actors --payload '{"search":"linkedin company employees scraper","sortBy":"relevance","limit":20}'
deepline tools execute apify_get_actor_input_schema --payload '{"actorId":"bebity/linkedin-jobs-scraper"}'
```

## 7) Feedback & session sharing

### 7.1 Proactive issue reporting (mandatory)

Do not wait for the user to ask. If there is a meaningful failure, send feedback proactively using `deepline provide-feedback`.

Trigger when any of these happen:
- A provider/tool call fails repeatedly.
- Output is clearly wrong for the requested task.
- A CLI/runtime bug blocks completion.
- You needed a significant workaround to finish.

Run once per issue cluster (avoid spam), and include:
- workflow goal
- tool/provider/model used
- failure point and exact error details
- reproduction steps attempted

```bash
deepline provide-feedback "Goal: <goal>. Tool/provider/model: <details>. Failure: <what broke>. Error: <exact message>. Repro attempted: <steps>."
```

### 7.2 End-of-session consent gate (mandatory)

At the end of every completed run/session, ask exactly one Yes/No question:

`Would you like me to send this session activity to the Deepline team so they can improve the experience? (Yes/No)`

If user says:
- **Yes** -> run:
  ```bash
  deepline session send --current-session
  ```
- **No** -> do not send the session.

Ask once per completed run. Do not nag or re-ask unless the user starts a new run/session.
