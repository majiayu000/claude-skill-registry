---
name: deepline-gtm
description: "GTM prospecting, enrichment, outreach, plays. Providers: adyntel,affinity,ai_ark,akta,allegrow,amplemarket,apify,attention,attio,aviato,bettercontact,bigquery,bluesky,bounceban,browserbase,builtwith,clay,clickhouse,cloudflare,contactout,contextdev,crustdata-v3,customer_db,databricks,dataforseo,datagma,deepline_ip_to_company,deepline_native,deeplineagent,discolike,dropleads,emailbison,emailguard,enformion,enigma,exa,findymail,firecrawl,fireflies,firmable,forager,fullenrich,generic_http,gong,google_ads_audiences,google_workspace,hackernews,harvestapi,heyreach,hubspot,hunter,icypeas,instantly,intercom,ipqs,kernel,leadmagic,lemlist,limadata,linkedin_ads_audiences,linkedin_scraper,lusha,meta_audiences,nooks,openmart,opensosdata,openwebninja,outreach,parallel,peopledatalabs,podscan,predictleads,prospeo,quickenrich,redshift,rocketreach,salesforce,salesforge,salesloft,scrapecreators,sentrion,serper,slack,smartlead,snowflake,sumble,theirstack,trestle,twitterapi,upcell,versium,wiza,zerobounce,zoho_crm,zoominfo."
---

# GTM Meta Skill

## Quick Start

```bash
npm install -g deepline
# Fallback for secure sandboxes: mkdir -p "$HOME/.local" && npm config set prefix "$HOME/.local" && export PATH="$HOME/.local/bin:$PATH" && npm install -g deepline --registry https://code.deepline.com/api/v2/npm/
deepline auth register --wait auto
deepline auth wait --timeout 120 # completes Cowork/browser approval; no-op if already connected
deepline auth status
deepline -h
```

## CLI resolution

Run `deepline` commands bare — no pipes, redirection, `2>&1`, command chaining, or backgrounding around them. The CLI already formats, truncates, and prints what you need; `deepline billing usage | head` reads as parsing and loses output.

Run `deepline` when it is available. If the shell reports that command is missing, use `<workspace-root>/.deepline/runtime/bin/deepline` (or the npm-created `.cmd` shim on Windows). If neither exists, follow `https://code.deepline.com/INSTALL.md` to set up Deepline.

Before the first Deepline fanout in a task, run `deepline preflight --json` as
one standalone command and wait for it to finish. Never submit preflight beside
another Deepline command. It combines health, authentication, and balance in
one process and gives any automatic CLI update a serial boundary.

After preflight succeeds, prefix every Deepline command that may run
concurrently with `DEEPLINE_SKIP_SELF_UPDATE=1`. This environment prefix is the
only exception to the bare-command rule above. Serial commands may stay bare;
the opt-out is required for every member of a parallel batch.

**Ask for requirements, not implementation instructions.** Requirements are the
business outcome, target population, constraints, time horizon, requested
destination, and any stated spend or authority boundary. The provider, tool,
query shape, identifier recovery, filter expression, fallback order, and
workflow structure are implementation decisions. Infer and execute the latter;
do not turn them into a questionnaire. When a requirement is genuinely absent
and materially changes the result or external action, ask one concise question
with a recommendation. Otherwise state a reasonable assumption in the result
and keep moving.

**Decision-ready communication.** The user should never have to infer the
answer from a status update. When work produces people, companies, events, or
rows that determine the next move, show those real records in a readable
Markdown table first. Link a person's name to their verified LinkedIn profile
when one was returned; do not hide the decision behind counts, summaries, or a
generic `Profile` column. For choices, show the comparison; for copy, show the
draft; for research, show the evidence that supports the conclusion.

Then make one plain-language recommendation based on what is visible. State the
concrete boundary—who is in, out, or what changes—not a label such as “keep” or
“refine.” Do not ask the user to design routine filters or choose plumbing.
Keep validation, raw ids, feeds, and tool mechanics internal unless they change
scope, cost, risk, confidence, or action.

When the user is calibrating, choosing a scope, prioritizing a list, or
authorizing a change, use this complete envelope:

```markdown
<the table, comparison, draft, or evidence>

Recommendation: <one concrete next state and why>.
Want me to use that, or adjust it?
```

End with `Want me to use that, or adjust it?` exactly. The user can say “yes”
or name the adjustment. A calibration, scope, or prioritization response is
incomplete without that final line, even when it starts no external action. Do
not add a second question, a menu, or an implementation checklist. If no user
decision is needed, state the outcome and stop.

**Paid monitors.** Before deployment show the recommended scope, live
Deepline price, and delivery in the smallest useful shape. Check Slack first;
recommend a real connected channel when one is available, otherwise offer Slack
or the configured CRM. The monitor recipe covers consent, history, and
similar-company scope.

**Discovery order: companies first, then people.** When the task requires finding contacts at companies matching criteria (portfolio, ICP, hiring signal), discover the company set first, then find people at each company. Do not start with broad people-search queries.

**Named companies are enough to start.** When the user gives company names but
not domains, resolve each canonical company domain before asking them for
anything. A domain is a recoverable identifier, not clarification debt. Carry
the resolved domain and its official-page evidence into the downstream lookup;
do not ask the user to paste a domain list merely because a later tool needs
one. Read [finding-companies-and-contacts.md](finding-companies-and-contacts.md)
for the identity gate and ambiguity handling.

**Known companies + nuanced roles: qualify the real title roster first.** For requests such as "AI leadership at Mount Sinai," "job titles at these companies," or "find the RevOps buyers at these accounts," read and follow [`recipes/find-qualified-titles.md`](recipes/find-qualified-titles.md): `company_titles` -> qualify exact roster titles -> `deepline_native_search_contact` with `title_lists`. Use Exa afterward for public-profile gaps and DropLeads last for supplemental database rows. Broad audience sizing remains a valid DropLeads use case.

### CLI recovery

The SDK CLI is the supported CLI. If it is unavailable, run `deepline update`
or reinstall it with `npm install -g deepline@latest`; do not switch CLI families.

## 2) Read the matching workflow before execution

SKILL.md routes; the matching doc supplies the execution contract. Read it before
using a provider so its schema, sequencing, and known failure modes govern the
run.

**Routing rules — match your task to a doc and READ IT:**

| When the task involves...                                                                                                                                                                                                                                                                                                                                                          | You MUST read this doc first                                                 | What it gives you (that SKILL.md doesn't)                                                                                                                                                                                                                                                                                            |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Finding companies, finding people, building lead lists, prospecting, portfolio/VC sourcing, contact finding at known companies, coverage completion at scale**                                                                                                                                                                                                                   | [finding-companies-and-contacts.md](finding-companies-and-contacts.md)       | Provider filter schemas, parallel execution patterns, provider mix tables, role-based search rules, subagent orchestration, at-scale coverage completion, portfolio/VC shortcuts, contact finding patterns.                                                                                                                          |
| **Researching companies or people, understanding what they build, figuring out use cases, personalizing based on mission/product/industry, enriching a CSV, adding data columns, waterfall enrichment, finding emails/phones/LinkedIn, coalescing data, custom signals, `run_javascript` / `deeplineagent` columns, Apify actors — any task that adds or transforms row-level data** | [enriching-and-researching.md](enriching-and-researching.md)                 | Play routing per scenario (`deepline plays run` + batch prebuilts + fork/wrap), waterfall orders for email/phone/LinkedIn, `run_javascript` / `deeplineagent` routing inside custom plays, multi-pass pipeline patterns, coalescing, custom signal buckets, Apify actor selection, GTM definitions and defaults. |
| **Writing or running custom Deepline plays** — composing multiple tools and/or other plays, mapping over CSV rows, fallback logic, joins/projections, durable datasets, custom run/export behavior, webhook/cron-style orchestration, or a reusable `.play.ts` scratchpad. Read it whenever no prebuilt play fits a batch job. | [recipes/deepline-plays.md](recipes/deepline-plays.md)                       | Direct vs compose decision, play search/describe discipline, bootstrap/wrap/fork rules, durable authoring basics, webhook/cron replacement routing, run/export/repair routing, and exact SDK/API reference pointers.                                                                                                                |
| **Writing cold emails, personalizing outreach, lead scoring, qualification, sequence design, campaign copy, inspecting CSVs in Playground.** If the task also requires researching companies/people to inform the writing, read [enriching-and-researching.md](enriching-and-researching.md) too — it has the multi-pass pipeline pattern.                                         | [writing-outreach.md](writing-outreach.md)                                   | Prompt templates from `prompts.json`. Scoring rubrics. Email length/tone/structure rules. Personalization patterns. Qualification frameworks. Playground inspection commands.                                                                                                                                                        |
| **Deepline Monitors** — continuously capturing a provider's webhook events (email replies, new job postings, intent signals) into a Customer DB table, or deploying/listing/managing those upstream provider pipes. Event-driven streaming, NOT an on-demand enrich/sourcing run. **Conditional gate:** run `deepline monitors status --json` first. Read the recipe only when the command exits 0 with `has_access: true`. Exit 1 with `has_access: false` means rollout access is absent. For exit 3, fix auth/permission; for exit 5, diagnose configuration/server reachability. Do not reinterpret other failures as rollout denial. | [recipes/deepline-monitors.md](recipes/deepline-monitors.md) | What Monitors are, when to use them vs plays, the full `deepline monitors` command set (status, available, check, deploy, list, get, update, delete, reactivate), monitor definition shape, the provider-webhook → Customer DB → triggered-play data flow, and the access gating. |

If you are hand-authoring enrich columns instead of using a native play, jump straight to the "Handmade step shape quick reference" section in [enriching-and-researching.md](enriching-and-researching.md). That section spells out the exact runtime contract for `run_javascript`, `extract_js`, `result`, and persisted `matched_result`.

### Recipes: step-by-step playbooks for specific tasks (check before executing)

Read the matching recipe before executing. Follow its sequence; adapt it only
when the request requires it.

| Recipe                          | Use when...                                                                                                                                |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `account-orgchart.md`           | Building an org chart, account map, buying committee, stakeholder map, or multi-threading plan around a target person or company          |
| `build-tam.md`                  | Building a total addressable market list or large company list from ICP criteria                                                           |
| `clay-to-deepline.md`           | Converting a Clay table to Deepline (deprecated enrich-era recipe — use its action mappings, author the result as a custom play)           |
| `deepline-monitors.md`          | **ACCESS-GATED.** Deepline Monitors continuously capture a provider's webhook events into a Customer DB table and trigger plays. Run `deepline monitors status --json` first; only exit 1 with `has_access: false` is a clean rollout denial. Diagnose auth, configuration, and server failures by their actual exit code. |
| `deepline-plays.md`             | Creating custom `.play.ts` scripts that compose multiple tools/plays, durable datasets, fallback logic, joins/projections, webhook/cron-style orchestration, and custom run/export behavior |
| `find-qualified-titles.md`      | **Primary path** for nuanced roles at known companies: "AI leadership at Mount Sinai", "find all job titles at these companies", or "find the marketing-ops/RevOps/Salesforce buyers". Pull each company's real title roster (free `company_titles`), qualify exact titles, then find contacts with tiered (LinkedIn, email, phone) reveal. |
| `linkedin-url-lookup.md`        | Resolving a person's LinkedIn profile URL from their name and company with strict identity validation                                      |
| `portfolio-prospecting.md`      | Finding companies backed by a specific investor or accelerator, then finding contacts and building personalized outbound                   |
| `small-business-prospecting.md` | Finding local small businesses or storefront/service-area companies using Maps-style search. Doctors, services business, restaurants, etc. |

> **Public/social source discovery, community-language pulls, pre-research source planning, or provider-coverage/cost comparison → use the standalone `deepline-pre-research` skill, not a recipe here.** It owns X/Twitter, Reddit, Hacker News, Bluesky, and public-registry fanout plus the source-plan + Deepline-cost synthesis.

If none match, grep for more specific keywords: `Grep pattern="<keyword>" path="<directory containing this SKILL.md>/recipes/" glob="*.md" output_mode="files_with_matches"`

### Data

- When the user hands you a CSV, run `deepline csv show --csv <path> --summary` first to understand its shape (row count, columns, sample values) before deciding how to process it.
- **NEVER read a large CSV into context with the Read tool.** Reading CSV rows into the conversation window exhausts context and produces zero output. This is the single most common failure mode.
- For row-by-row processing (enrichment, rewriting, research, scoring), use a Deepline play per §2.5: prebuilt if one fits, fork/wrap when close, author when not.
- To explore or understand CSV content without loading it, use `deepline csv show --csv <path> --rows 0:2` for a two-row sample, or spawn an Explore subagent to answer questions about the data.
- Pilot before scale: slice the CSV (`head -3 in.csv > pilot.csv`), run the play on the slice, `deepline runs export` and inspect, then run the full file. **Small-input exception:** when an exact-fit prebuilt covers a small input (≤ ~25 rows) whose scope the user already stated, the full file IS the pilot — run it once.
- **The pilot is never the deliverable.** A task is not done until the FULL input has run and the result is exported to the exact requested output path: `deepline runs export <run-id> --out "$FINAL_CSV"`. Finishing with only a pilot CSV, or an export under a play-derived name, is the single most common way to fail the task while feeling done.

### Tools

For signal-driven discovery (investor, funding, hiring, headcount, industry, geo, tech stack, compliance), start with `deepline tools search`. Do not guess fields. Its syntax is `deepline tools search [query] [--categories <categories>] [--search_terms <terms>] [--json]`: provide a query, or at least one of `--categories` and `--search_terms`. The query is optional only for structured filtering. Use commas for multiple categories or search terms. There is no `--prefix` flag; include a provider name in the query when needed.

Search 2-4 synonyms, execute in parallel only after the standalone preflight:

```bash
DEEPLINE_SKIP_SELF_UPDATE=1 deepline tools search investor
DEEPLINE_SKIP_SELF_UPDATE=1 deepline tools search "crustdata investor"
DEEPLINE_SKIP_SELF_UPDATE=1 deepline tools search --categories company_search --search_terms "structured filters,icp"
DEEPLINE_SKIP_SELF_UPDATE=1 deepline tools search --categories people_search --search_terms "title filters,linkedin"
```

## 2.5) Plays are the surface

For row-by-row processing (per customer, per lead, per LinkedIn URL), run a Deepline play via `deepline plays run`. `deepline enrich` is deprecated — do not use or document it; when no play fits, author one.

1. **Discover live, then run.** `deepline plays search <query>` and `deepline plays describe <name>` — choose from the live catalog and its contract, never from memory. Search results include a `runCommand` and a `cloneEditStarter` for every prebuilt.
2. **Prebuilt fits** → run it. Batch prebuilts take a CSV directly: `deepline plays run prebuilt/name-and-domain-to-email-waterfall-batch --input '{"csv":"leads.csv"}'`, then `deepline runs export <run-id> --out "$FINAL_CSV"`.
3. **Close but not exact** → pull and edit it. Every prebuilt is forkable:

   ```bash
   deepline plays get prebuilt/<name> --source --out ./<name>.play.ts
   deepline plays check ./<name>.play.ts   # mandatory before running
   deepline plays run --file ./<name>.play.ts --input '{...}'
   ```

   If `plays check` fails on a missing local import, that prebuilt is multi-file — wrap it instead of forking: `deepline plays bootstrap <family> --from <source> --using play:prebuilt/<name> --limit 5 --out workflow.play.ts`.
4. **No play fits** → author one from scratch per [recipes/deepline-plays.md](recipes/deepline-plays.md): compose tools and other plays, map CSVs, add fallback logic and joins.

**Results live in the Customer DB.** Every batch play persists its dataset as a durable table: `deepline db query --sql 'select * from "storage"."<table>" limit 20' --max-rows 20 --json` (the run output names the table). Columns are the play's snake_case fields plus per-leg columns like `email_result__hunter_email` — the per-provider audit trail. Rerunning reuses filled cells instead of re-buying them; exports are projections of this table, so nothing is lost if a CSV goes missing.

**The iterate loop — pilot, price, fix, then scale:**

1. Run a few rows (slice the CSV or run 2-3 scalar inputs).
2. Read price and performance: `deepline runs get <run-id> --full --json` reports billing and per-step outcomes; the storage table's per-leg columns show which providers hit, missed, or erred.
3. Fix what the pilot exposed BEFORE scaling: a provider that misses or flakes on your segment gets dropped or reordered in a fork; wrong columns get a `columns` map; weak coverage gets a different route. Do not buy the same failure at full scale.
4. Run the full file, export to `FINAL_CSV`, and report to the user: rows delivered, coverage, observed credits, and what you changed after the pilot.

## 3) Core policy defaults

### 3.1 Definitions and defaults

GTM time windows, thresholds, and interpretation rules are defined in the Definitions section of [enriching-and-researching.md](enriching-and-researching.md).

## Provider Playbooks

Provider-specific playbooks are bundled as separate reference files. Open the relevant playbook when provider-specific behavior, pricing, caveats, or payload conventions matter.

[adyntel](provider-playbooks/adyntel.md), [affinity](provider-playbooks/affinity.md), [ai_ark](provider-playbooks/ai_ark.md), [akta](provider-playbooks/akta.md), [allegrow](provider-playbooks/allegrow.md), [amplemarket](provider-playbooks/amplemarket.md), [apify](provider-playbooks/apify.md), [attention](provider-playbooks/attention.md), [attio](provider-playbooks/attio.md), [aviato](provider-playbooks/aviato.md), [bettercontact](provider-playbooks/bettercontact.md), [bigquery](provider-playbooks/bigquery.md), [bloomberry](provider-playbooks/bloomberry.md), [bluesky](provider-playbooks/bluesky.md), [bounceban](provider-playbooks/bounceban.md), [browserbase](provider-playbooks/browserbase.md), [builtwith](provider-playbooks/builtwith.md), [clay](provider-playbooks/clay.md), [clickhouse](provider-playbooks/clickhouse.md), [cloudflare](provider-playbooks/cloudflare.md), [contactout](provider-playbooks/contactout.md), [contextdev](provider-playbooks/contextdev.md), [crustdata](provider-playbooks/crustdata.md), [crustdata-v2](provider-playbooks/crustdata-v2.md), [crustdata-v3](provider-playbooks/crustdata-v3.md), [databricks](provider-playbooks/databricks.md), [dataforseo](provider-playbooks/dataforseo.md), [datagma](provider-playbooks/datagma.md), [deepline_ip_to_company](provider-playbooks/deepline_ip_to_company.md), [deepline_native](provider-playbooks/deepline_native.md), [deeplineagent](provider-playbooks/deeplineagent.md), [discolike](provider-playbooks/discolike.md), [dropleads](provider-playbooks/dropleads.md), [emailbison](provider-playbooks/emailbison.md), [emailguard](provider-playbooks/emailguard.md), [enformion](provider-playbooks/enformion.md), [enigma](provider-playbooks/enigma.md), [exa](provider-playbooks/exa.md), [findymail](provider-playbooks/findymail.md), [firecrawl](provider-playbooks/firecrawl.md), [fireflies](provider-playbooks/fireflies.md), [forager](provider-playbooks/forager.md), [fullenrich](provider-playbooks/fullenrich.md), [generic_http](provider-playbooks/generic_http.md), [gong](provider-playbooks/gong.md), [google_ads_audiences](provider-playbooks/google_ads_audiences.md), [hackernews](provider-playbooks/hackernews.md), [harvestapi](provider-playbooks/harvestapi.md), [heyreach](provider-playbooks/heyreach.md), [hubspot](provider-playbooks/hubspot.md), [hunter](provider-playbooks/hunter.md), [icypeas](provider-playbooks/icypeas.md), [instantly](provider-playbooks/instantly.md), [intercom](provider-playbooks/intercom.md), [ipqs](provider-playbooks/ipqs.md), [kernel](provider-playbooks/kernel.md), [leadmagic](provider-playbooks/leadmagic.md), [lemlist](provider-playbooks/lemlist.md), [limadata](provider-playbooks/limadata.md), [linkedin_ads_audiences](provider-playbooks/linkedin_ads_audiences.md), [lusha](provider-playbooks/lusha.md), [meta_audiences](provider-playbooks/meta_audiences.md), [nooks](provider-playbooks/nooks.md), [openmart](provider-playbooks/openmart.md), [opensosdata](provider-playbooks/opensosdata.md), [openwebninja](provider-playbooks/openwebninja.md), [outreach](provider-playbooks/outreach.md), [parallel](provider-playbooks/parallel.md), [peopledatalabs](provider-playbooks/peopledatalabs.md), [pipedrive](provider-playbooks/pipedrive.md), [podscan](provider-playbooks/podscan.md), [predictleads](provider-playbooks/predictleads.md), [prospeo](provider-playbooks/prospeo.md), [quickenrich](provider-playbooks/quickenrich.md), [redshift](provider-playbooks/redshift.md), [salesforce](provider-playbooks/salesforce.md), [salesforge](provider-playbooks/salesforge.md), [salesloft](provider-playbooks/salesloft.md), [scrapecreators](provider-playbooks/scrapecreators.md), [sentrion](provider-playbooks/sentrion.md), [serper](provider-playbooks/serper.md), [smartlead](provider-playbooks/smartlead.md), [snowflake](provider-playbooks/snowflake.md), [sumble](provider-playbooks/sumble.md), [theirstack](provider-playbooks/theirstack.md), [trestle](provider-playbooks/trestle.md), [twitterapi](provider-playbooks/twitterapi.md), [upcell](provider-playbooks/upcell.md), [versium](provider-playbooks/versium.md), [wiza](provider-playbooks/wiza.md), [wizleads](provider-playbooks/wizleads.md), [zerobounce](provider-playbooks/zerobounce.md), [zoho_crm](provider-playbooks/zoho_crm.md), [zoominfo](provider-playbooks/zoominfo.md)

- Apply defaults when user input is absent.
- User-specified values always override defaults.
- In approval messages, list active defaults as assumptions.

### 3.2 Working directory — set up BEFORE any file writes

**NEVER write files to `/tmp/` or any absolute temp directory.** Files in system `/tmp/` are wiped on reboot — users permanently lose enriched CSVs, research outputs, and hours of paid enrichment work. This is a critical data-loss risk.

Set up a descriptive project-local working directory as your first action:

```bash
WORKDIR="deepline/data/<descriptive-task-slug>" && mkdir -p "$WORKDIR" && echo "$WORKDIR"
```

The slug must describe the task (e.g. `deepline/data/yc-cmo-outbound`, `deepline/data/acme-email-waterfall`). Do NOT use random names like `mktemp` generates — the user needs to find these files later. See [enriching-and-researching.md](enriching-and-researching.md) for full details.

### 3.3 Output policy and User Interaction Pattern

- Always use a Deepline play for list enrichment or discovery at scale (>5 rows) — §2.5 routing. The run's play page lets the user inspect rows and rerun; send that URL.
- Even for company → ICP person flows, plays work: search and filter as part of the process, with providers like Apify to guide.
- Even when you don't have a CSV, create one and run the batch play against it.
- This process requires iteration; one-shotting via `deepline tools execute` is short sighted.
- In chat, send file/run links and render a decision table when rows inform a decision.
- Preserve lineage columns (especially `_metadata`) end-to-end. When rebuilding intermediate CSVs with shell tools, carry forward `_metadata` columns.
- Never overwrite a user-provided source CSV; write outputs to your working directory. Reruns of a play reuse completed cells by default.

See [enriching-and-researching.md](enriching-and-researching.md) for `deepline csv` commands, pre-flight/post-run script templates, and inspection details.

### 3.4 Final file and run check (light)

- Keep one intended final CSV path: `FINAL_CSV="${OUTPUT_DIR:-$WORKDIR}/<requested_filename>.csv"`
- Before finishing: use the post-run inspection script pattern from [enriching-and-researching.md](enriching-and-researching.md). Run it once instead of separate checks.
- **Checkpoint the deliverable.** On multi-phase pipelines (companies → contacts → emails), write `FINAL_CSV` as soon as the first complete rows exist and overwrite it as later phases improve it. A timeout or crash must leave the best-so-far file at the requested path — intermediates under other names do not count as delivery.
- **For a task that ran a Play, include its result.** Give the exact `FINAL_CSV`
  path and play page link; do not invent one for monitor-only, research, or advisory work.

## 4) Credit and approval gate (paid actions)

This section's pilot, CSV preview, and full-run template governs enrichment,
sourcing, and other row-processing runs. Monitor mutations use the workflow in
`recipes/deepline-monitors.md` instead: inspect scope, reuse candidates,
downstream actions/unknown consumers, and price before asking. Keep that
approval decision-first: scope table, recommendation, live Deepline price, and
one question. Because a monitor can incur variable future event charges, require
explicit approval before every paid deploy, reactivate, or historical
widening—even when the user stated the scope. A historical rung is empty only
after its documented provider completion window; leave it intact while that
window is pending. Ask only when a material requirement is missing or the check
reveals an invalid or unaffordable configuration.

### 4.1 Required run order

1. Pilot on a narrow scope: a small CSV slice through the same batch play, or 2-3 scalar runs.
2. If the scope is NOT already approved (see below), request explicit approval.
3. Run full scope, report the pilot's cost and quality findings alongside the deliverable.

**User-stated scope = already approved for bounded row-processing only.** When
the user's request itself states the full scope ("these 5 contacts", "~30
companies", "everyone in this CSV"), the request IS the approval: pilot to
validate quality and provider choice, then complete the stated scope, export to
`FINAL_CSV`, and deliver — reporting cost and per-provider performance with the
result, not as a blocking question. This exception never applies to monitors;
follow the monitor-specific consent gate above.

**Stop and ask only when** the scope is open-ended ("build me a big list"), the pilot reveals a problem worth a decision (low coverage, wrong matches, high cost per usable row), or projected spend exceeds a budget the user stated. Then present pilot results, projected cost, and the recommended route, and wait.

### 4.2 Execution sizing

- Use smaller sequential commands first.
- Keep limits low and windows bounded before scaling.
- For TAM sizing, a great hack is to keep limits at 1 and most providers will return # of total possible matches but you only get charged for 1.
- Prefer providers and plays that charge on returned results or successful hits when coverage is uncertain. If a provider bills per attempt/request/page, prove quality on a tiny pilot before letting it fan out.
- Stop after the pilot when the first rows show low usable coverage, wrong-person/company matches, missing getters, or high cost per usable row. Change route/provider order before buying the same failure at full scale.
- Do not depend on monthly caps as a hard risk control.
- Estimate play pricing before full scale: `deepline plays list --show-cost`, the play's `describe` output, and the pilot's observed cost from `deepline runs get <run-id> --full --json`. State the estimate in the approval message. `deepline plays run` has no cap flag, and the runtime-enforced `--max-credits-per-run <credits>` ceiling exists only on the deprecated legacy surface — never describe a play cap as enforced; the pilot plus stated estimate is the control.

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

1. Play or provider(s)
2. Pilot summary and observed behavior
3. Intent-level assumptions (3–5 one-line bullets)
4. CSV preview from the real pilot: the head of `deepline runs export <pilot-run-id> --out`
5. Credits estimate / range
6. Full-run scope size
7. Max spend cap (stated and monitored; no runtime-enforced play cap exists)
8. Approval question: `Approve full run?`

Strict format contract (blocking):

1. Use the exact four section headers: Assumptions, CSV Preview (ASCII), Credits + Scope + Cap, Approval Question.
2. If any required section is missing, remain in `AWAIT_APPROVAL` and do not run paid/cost-unknown actions.
3. Only transition to `FULL_RUN` after an explicit user confirmation to the approval question.
4. `run_javascript` is the non-AI path. `ai_inference` is for general classification/structured reasoning, and `deeplineagent` is for context gathering / web research / signal extraction.

Approval template:

```markdown
Assumptions

- <intent assumption 1>
- <intent assumption 2>

CSV Preview (ASCII)
<paste verbatim pilot output: the runs export head>
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

- Must run a real pilot against the exact CSV intended for the full run: a small slice through the same batch play.
- Must include the pilot output preview verbatim in approval.
- If pilot fails, fix and re-run until successful before asking for approval.
- Ask for approval in chat after the pilot. Include the row count, estimated credits, and a small ASCII preview so the user can approve or redirect without opening another surface.

### 4.5 Billing commands

```bash
deepline billing balance  # Show current credit balance
deepline billing usage    # Show recent billing activity and grouped recent usage
deepline billing limit    # Show the current monthly billing cap
```

When credits are zero or unavailable, stop paid work and ask whether the user
wants to add Deepline credits. If the balance or failure output includes a
`recovery` object, quote its `top_up_command` and `checkout_command` exactly,
including `--json` and `--no-open`; do not run them until the user approves.
Do not hardcode a USD-to-credit exchange rate in the skill. Use live billing,
pricing, or tool output when quoting credit costs.

## 5) Provider routing (high level)

**Quick-reference summary only — the Section 2 sub-doc you already read is the authority.**

- **Search / discovery** → You MUST have [finding-companies-and-contacts.md](finding-companies-and-contacts.md) open. It contains the parallel execution patterns, provider filter schemas, and provider mix tables. Start with `deepline tools search <intent>` and execute field-matched provider calls in parallel; when the `deepline-list-builder` subagent is available, use subagent-based parallel search orchestration as the preferred pattern. Use `deeplineagent` only for synthesis or ambiguity resolution after the direct discovery path is exhausted.
- **Enrich / waterfall / coalesce** → You MUST have [enriching-and-researching.md](enriching-and-researching.md) open. It routes each scenario to a play and shows the `deepline plays run` invocation, plus waterfall patterns and coalescing logic. Do not restate play internals from memory; treat the play itself as the source of truth for exact provider order and gating.
- **Custom signals / messaging** → Read [enriching-and-researching.md](enriching-and-researching.md) (custom signals section). Use `run_javascript` for deterministic transforms/template logic and `deeplineagent` for AI work. Start from `prompts.json`.
- **Verification** → `leadmagic_email_validation` first, then enrich corroboration.
- **LinkedIn profiles, company employees, posts, comments, and reactions** -> Prefer Deepline's native HarvestAPI provider. Use the documented `harvestapi_*` names as starting hints, then run `deepline tools describe <operation> --schema-only` before execution; broad tool search can be noisy. Use Apify only when HarvestAPI does not expose the required LinkedIn surface.
- For phone recovery, read [enriching-and-researching.md](enriching-and-researching.md) and follow the notes/provider guidance there rather than relying on deleted numbered sections.

Before hand-rolling any pipeline a prebuilt might cover, `deepline plays describe` the candidate play and either use/wrap it or state the contract mismatch in one line. Silently bypassing a fitting prebuilt is a routing failure.

Provider path heuristics:

- Broad first pass: direct tool calls for high-volume discovery.
- Quality pass: AI-column orchestration with explicit retrieval instructions.
- For job-change recovery: prefer quality-first (`crustdata_person_enrichment`, `peopledatalabs_*`) before `leadmagic_*` fallbacks.
- Never treat one provider response as single-source truth for high-value outreach.

## 6) Additional notes

Critical: keep [writing-outreach.md](writing-outreach.md) workflow context active when running any sequence task. It is not optional for ICP-driven messaging.

### Operational troubleshooting: rate limits and CLI health

- Use Deepline plays for heavy row-by-row work whenever possible. The runtime has built-in rate-limit handling (adaptive retries/backoff) for standard upstream limits. If you are building a homegrown script, assume it does not include the same automatic protection unless you explicitly implement it.
- If enrichment or CLI behavior is unstable, update the CLI and reinstall the Deepline skills:

```bash
deepline update
deepline skills
```

**Sites requiring auth:** Don't use Apify. Tell the user to use Claude in Chrome or guide them through Inspect Element to get a curl command with headers (user is non-technical).

1. If user provides actor ID/name/URL: use it directly.
2. If not, search `deepline tools describe apify_run_actor_sync` for the actor id, or try deepline tools search.
3. If not present, run discovery search.
4. Avoid rental-priced actors.
5. For LinkedIn posts and engagers, use the native HarvestAPI operations first: inspect `harvestapi_search_posts`, `harvestapi_get_post`, `harvestapi_get_post_reactions`, and `harvestapi_get_post_comments`. Use `supreme_coder/linkedin-post` only when the native provider does not cover the requested shape. Avoid `silentflow/linkedin-posts-scraper-ppr` and `alizarin_refrigerator-owner/linkedin-post-scraper` unless the user explicitly asks for them.
6. Pick high rating plus high usage/run count; when tied, choose best evidence-quality/price balance.
7. Honor `operatorNotes` over public ratings when conflicting.

```bash
deepline tools execute apify_list_store_actors --input '{"search":"similarweb traffic scraper","sortBy":"relevance","limit":20}'
deepline tools execute apify_get_actor_input_schema --input '{"actorId":"radeance/similarweb-scraper"}'
```

## 7) Feedback & session sharing

### 7.1 Proactive issue reporting (mandatory)

Do not wait for the user to ask. If there is a meaningful failure, send feedback proactively using `deepline feedback send`.

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
deepline feedback send "Goal: <goal>. Tool/provider/model: <details>. Failure: <what broke>. Error: <exact message>. Repro attempted: <steps>."
```

### 7.2 End-of-session consent gate (mandatory)

After the substantive result is resolved, ask exactly one Yes/No question in a
separate message—never beside a table, recommendation, approval request, or
unresolved user decision. Do not ask it after a terminal no-change outcome:
`Change: none — I’m leaving it as is.` must remain the final line of that
response.

`Would you like me to send this session activity to the Deepline team so they can improve the experience? (Yes/No)`

If user says:

- **Yes** -> run:
  ```bash
  deepline sessions send --current-session
  ```
- **No** -> do not send the session.

Ask once per completed run. Do not nag or re-ask unless the user starts a new run/session.
