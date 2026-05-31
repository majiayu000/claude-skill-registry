---
name: deepline-sdk
description: "Use for Deepline SDK/CLI GTM work: build/run/debug plays, find companies or contacts, enrich emails/phones/LinkedIn, size TAMs, route providers, use getters, recover from tool/play shape issues, control spend, and export CSVs."
---

# Deepline SDK Search Discipline

This skill teaches GTM search as paid uncertainty reduction. The goal is not fewer provider calls; the goal is making every useful paid call reusable, inspectable, and tied to a final row the user can trust.

A good Deepline search run has a shape: discover the live provider contract, put the first useful provider call into a scratchpad play, pilot a few rows, inspect declared getters, narrow with evidence, enrich only survivors, validate known channels, and export flat rows with provenance and miss reasons.

The play is the notebook. Stable step ids are the cache. Getter contracts are the interface. The CSV is only the final surface.

Build a notebook, not a masterpiece. Start with a probe. Checkpoint what costs money. Add gates before fanout. Climb the ladder only when the receipts look good.

## Command Discipline

Run Deepline commands as direct commands. Do not add shell helpers around them.
Do not search parent repos or unrelated worktrees for old `*.play.ts` scratch files.

Good:

```bash
deepline health --json && deepline auth status --json && deepline billing balance --json
deepline plays list --origin prebuilt --json
deepline plays grep email --origin prebuilt --json
deepline tools list --categories email_finder --json
deepline tools describe dropleads_email_finder --json
```

Bad:

```bash
deepline health --json 2>&1
deepline plays search email --json | head
deepline tools describe dropleads_email_finder --json | jq '.cost'
deepline tools search "email finder" --json &
```

If you need structured data, request Deepline JSON and read that command's output directly. Do not pipe, redirect, slice, parse with Python, background, or wrap commands in shell fallbacks. A short `&&` preflight is fine for cheap status checks; do not chain paid executes, play runs, or discovery commands whose output you need to inspect. Shell parsing turns a typed contract into disposable rendered text and slows the run.

## Vocabulary

Use these terms consistently.

- **Scratchpad play** — the local `.play.ts` file where paid provider work becomes replayable state, not disposable console output. A scratchpad is always a play, not a loose CLI transcript or notes file.
- **Notebook** — the play as a learning surface. It can contain tiny runs, inspection comments, pure scoring steps, gates, and export projections because each rerun preserves useful knowledge.
- **Probe** — the smallest useful run: usually 1-2 rows, one source, one getter, one hypothesis. A probe is allowed to be incomplete; its job is to make the next edit less speculative.
- **Checkpoint** — a stable `ctx.tools.execute`, `ctx.runPlay`, or `ctx.map(...).step(...)` id that turns paid or slow work into reusable state. If a rerun should not rebuy it, checkpoint it.
- **Gate** — a pure step that decides whether paid fanout is allowed: domain match, title fit, category evidence, placeholder filter, max rows, max fallback legs, or balance floor.
- **Ladder** — the scale path: 1 row -> 5 rows -> 25 rows -> full. Do not jump from unknown shape to full fanout unless a prebuilt play exactly covers a tiny input.
- **Receipt** — row-level evidence that explains why a result is trustworthy: source, provider/play, getter used, fit evidence, status, and miss reason.
- **Source call** — a provider call that creates candidate companies, people, domains, or accounts.
- **Pilot** — a tiny run that proves row shape, getter availability, null behavior, relevance, and cost before scale.
- **Getter contract** — the semantic output interface declared by `deepline tools describe`, such as `extractedLists.people.get()` or `extractedValues.email_status.get()`.
- **Evidence column** — a field that explains why the row belongs: category, domain source, title match, company fit, signal text.
- **Fanout** — row-level enrichment where provider calls multiply by row count.
- **Branch** — a meaningfully different source hypothesis, not another tiny edit to the same provider payload.
- **Validation** — checking an already found email or phone, not discovering one.
- **Miss reason** — a deliberate output explaining why a row lacks a desired field.

## Operating Model

Search is an economic narrowing loop:

1. Run one compact preflight command for health, auth, and balance.
2. List and describe prebuilt plays before provider tools; plays are waterfalls and often already encode the right route.
3. If a play fits, run it directly or wrap it in a scratchpad with `ctx.runPlay(...)`.
4. Drop to provider tools only after naming the play mismatch: missing input, wrong output, wrong scale, or custom gating/validation needed.
5. Discover fallback tools by capability tags/categories, then describe exact contracts, getters, cost, and failure modes.
6. Put useful custom provider work into a scratchpad play with stable ids.
7. Probe 1-2 rows first, then ladder up only after receipts prove shape and fit.
8. Add gates before paid fanout; enrich only survivors.
9. Export flat user-facing rows with provenance and miss reasons.

Put any provider call that might contribute final rows into a `.play.ts` file before continuing exploration. The scratchpad play is the artifact; rendered CLI output is only a transient inspection aid.

## Cost Checkpoint Before Scale

Borrow the GTM execution-plan habit: separate the pilot from the full run, then pause before paid scale with a concrete plan. Real cost hides in multiplication. Seven final rows can still burn a full budget if the play bought hundreds of people candidates and discarded most of them downstream.

Get cost from the live contract, not memory:

```bash
deepline plays describe prebuilt/<play-name> --json
deepline tools describe <fallback-source-tool-id> --json
deepline tools describe <fallback-people-search-tool-id> --json
deepline tools describe <fallback-email-finder-tool-id> --json
deepline billing balance --json
```

For tools, read `cost.pricingModel`, `deeplineCreditsPerPricingUnit`, `deeplineUsdPerPricingUnit`, `billingMode`, `inputSchema`, and declared getters. For plays, read the described inputs/outputs and pricing estimate if present; if the play is a waterfall, estimate the expected range by its stop condition: best case pays the first successful leg, worst case pays every fallback leg that can run for a row. If pricing is missing, ambiguous, or per-result with unclear result count, treat it as cost-unknown and ask before scaling.

Before any mapped paid enrichment beyond the pilot, show the user:

```text
Plan before paid scale:
- Goal: <target rows and required fields>
- Pilot result: <rows inspected, useful rows, declared getters, miss reasons>
- Source size: <candidate companies/people available after cheap filters>
- Limits: <max source rows, max people per account, max fallback legs>
- Route: <prebuilt play used/wrapped, or exact mismatch that forced custom tools>
- Paid fanout estimate: <rows> * <play/waterfall calls per row> * <fallback legs that can run>
- Expected credit range: <low-high credits>, based on `plays describe` and fallback `tools describe`
- Stop conditions: <balance floor, max misses, max spend, max rows>
- Visual inspection: open <DEEPLINE_HOST_URL>/dashboard/plays/<play-name> or use `deepline runs get <run-id> --json --full`
```

Then ask for approval to continue unless the user already gave a budget or the run stays within a tiny pilot. This is not ceremony: it prevents a broad people search from buying candidates that never survive title, domain, or email checks.

Inside the play, put response-size gates before `ctx.map`. First source calls can return far more rows than the user asked for. After the pilot reveals shape and counts, add cheap pure steps or source `limit`/`size`/`numResults` fields so mapped enrichment only sees a bounded candidate set.

```text
const source = await ctx.tools.execute({
  id: 'company_seed',
  tool: '<company-search-tool-id>',
  input: {
    query: input.query,
    numResults: Math.min(Number(input.source_limit ?? 25), 50),
  },
  description: 'Bounded source seed before paid people/email fanout.',
});

const candidates = source.extractedLists.companies.get();

// Cheap notebook logic: inspect, dedupe, score, and cap before any mapped paid calls.
const accounts = candidates
  .map(normalizeCompany)
  .filter((account) => account.domain && account.fit_score >= 0.6)
  .slice(0, Math.min(Number(input.account_limit ?? input.target ?? 10), 100));

const estimatedPeopleCalls = accounts.length * Math.min(Number(input.people_per_account ?? 3), 5);
if (estimatedPeopleCalls > Number(input.max_people_calls ?? 50)) {
  throw new Error(`Paid fanout too large: ${estimatedPeopleCalls} people calls before email lookup.`);
}

const contacts = await ctx
  .map('bounded_people_search', accounts)
  // paid row-level work starts only after the account set is bounded
  .step('people_search', async (row, rowCtx) => { /* ... */ })
  .run({ key: (row) => row.domain });
```

When a run starts, give the user the visual inspection path. If the CLI prints a local URL, link that exact URL. If it only prints a run id, link the play page, which shows the latest runs and lets the user inspect the sheet/trace visually:

```text
Inspect visually: <DEEPLINE_HOST_URL>/dashboard/plays/<play-name>
Run details:
deepline runs get <run-id> --json --full
```

## Judgment Tests

- **Fast Route Test** — if the user asks only for route selection or a smoke check, do not audit every provider. Use a few live `plays search` / `tools search` calls, choose the route family, and write a concise route memo. Do not include provider catalogs, tables, or a full getter inventory unless the user asked for that depth.
- **Rerun Test** — if the next change is filtering, scoring, getter usage, placeholder cleanup, or export shape, should provider calls rerun? Usually no. Move that work downstream in the scratchpad play.
- **Pilot Test** — before scaling, can you name the getter, expected row shape, response size, likely cost multiplier, and failure mode?
- **Getter Contract Test** — if `tools describe` declares a getter, call it directly. Optional-chain payload archaeology is a smell.
- **Spend Multiplication Test** — before row-level enrichment, can you estimate `input rows * paid calls per row * fallback legs`?
- **Limit Test** — before `ctx.map`, did you cap source rows and people-per-account based on the pilot response size?
- **Source-Fit Test** — for account-scoped contacts, can every contact point back to a sourced account/domain with fit evidence?
- **Branch Test** — are you adding a genuinely different source hypothesis, or just thrashing the same paid query?
- **Validation Test** — are validators checking known emails/phones rather than being used as finders?
- **Domain Search Test** — are domain-search tools being treated as domain/company discovery, not named-person email finding?
- **Scratchpad Deletion Test** — if you deleted the play and kept only final rows, what expensive knowledge would disappear?

## Prebuilt Plays Before Manual Providers

Plays before tools. Prebuilt plays are waterfalls: they already encode provider ordering, fallback stop conditions, getter handling, and common export shape. If a prebuilt play covers the job, use it directly or wrap it in the scratchpad with `ctx.runPlay(...)`. Drop to manual `ctx.tools.execute` provider chains only when the play is missing, too broad, missing required outputs, or you need custom ordering, extraction, gating, or validation behavior.

```bash
deepline plays list --origin prebuilt --json
deepline plays grep email --origin prebuilt --json
deepline plays grep phone --origin prebuilt --json
deepline plays grep "company contact persona" --origin prebuilt --json
deepline plays describe prebuilt/<play-name> --json
deepline plays run prebuilt/<play-name> --input '{...}' --watch
```

Prefer `origin: "prebuilt"` results unless you intentionally want an org-owned scratchpad. Always run `plays describe` before choosing or rejecting a play; retrieval aliases are intentionally broad and can return adjacent jobs.

For a normal GTM task, the first commands should look like this:

```bash
deepline health --json && deepline auth status --json && deepline billing balance --json
deepline plays list --origin prebuilt --json
deepline plays describe prebuilt/company-to-contact --json
```

Only after the play contract fails the task should you look for provider tools:

```bash
deepline tools list --categories company_search --json
deepline tools grep "people search title seniority linkedin" --categories people_search --json
deepline tools describe <tool-id> --json
```

`deepline play run` / `deepline plays run` may return after starting the run unless `--watch` is present. For eval and deliverable work, run with `--watch` so success or failure is observed before continuing. After a watched run fails, inspect the run with the exact `runs get` command printed by the CLI; do not infer success from a returned `runId`.

| Scenario | Use when | Start with | Required input | Notes |
|---|---|---|---|---|
| Name + domain -> work email | You have first name, last name, and company domain | `prebuilt/name-and-domain-to-email-waterfall` | `first_name`, `last_name`, `domain` | Canonical work-email route. Include `company_name` and `linkedin_url` when known. |
| CSV name + domain -> work email | You have a CSV with first/last/domain columns | `prebuilt/name-and-domain-to-email-waterfall-batch` | `csv` | Fastest bulk work-email route. Pass a workspace-relative CSV path such as `data/leads.csv`, not an absolute local path. |
| LinkedIn profile -> work email | You have a standard LinkedIn `/in/` profile URL | `prebuilt/person-linkedin-to-email` | `linkedin_url` | Do not use Sales Navigator `/sales/lead/` URLs as profile URLs; resolve company/domain first. |
| Person -> LinkedIn profile | You have name plus company/domain/email context and need the profile URL | `prebuilt/person-to-linkedin` | `first_name`, `last_name` | Mechanical identity lookup before LinkedIn-backed enrichment. |
| Company -> persona contacts | You have a target account and need candidate people by role or seniority | `prebuilt/company-to-contact` | `roles` | Prefer exact roles plus account identifiers: `domain`, `company_name`, or `linkedin_company_url`. Validate title fit before email/phone fanout. |
| Person -> phone | You have a verified person identity and want one phone number | `prebuilt/person-to-phone` | `first_name`, `last_name` | Phone comes after identity. Add `domain`, `email`, or `linkedin_url` when available. Validate known phones after recovery. |
| Personal email | User explicitly asks for personal emails, not work emails | `prebuilt/personal-email` | `first_name`, `last_name` | Do not substitute work-email plays or providers when the requested channel is personal email. |
| LinkedIn post -> engagers | You have a LinkedIn post URL and need reactors/commenters | `prebuilt/linkedin-post-to-engagers` | `post_url` | Use this for post-level audience capture, then qualify or enrich later. |
| Engager/person -> ICP tier | You have person rows with position/headline and an ICP definition | `prebuilt/engagers-to-icp-qualification` | `first_name`, `last_name`, `position`, `icp_description` | Classification only. If qualification needs company size, funding, or web research, use a custom research step. |

Prebuilt plays are not tools. In the CLI, call them with `deepline plays run`. Inside a scratchpad play, compose them with `ctx.runPlay(key, playRef, input, { description })`; inside `ctx.map`, use the row context: `rowCtx.runPlay(...)`.

Keep each child play call behind a stable key just like a provider call. The key is scoped to the parent run and row, so reruns can reuse completed child work.

When you bypass a likely prebuilt play, write the mismatch before writing custom provider code:

```text
Prebuilt route rejected:
- Play: prebuilt/company-to-contact
- Contract checked with: deepline plays describe prebuilt/company-to-contact --json
- Mismatch: <missing input/output, wrong scale, wrong persona control, or custom validation needed>
- Custom route: <provider tools and why they are necessary>
```

```text
const email = await rowCtx.runPlay(
  'name_domain_email',
  'prebuilt/name-and-domain-to-email-waterfall',
  {
    first_name: row.first_name,
    last_name: row.last_name,
    domain: row.domain,
    company_name: row.company_name,
    linkedin_url: row.linkedin_url,
  },
  {
    description: 'Canonical name + domain work-email waterfall.',
  },
);

const workEmail = email?.email ?? null;
```

Use row-scoped child plays inside maps for bulk enrichment:

```text
const contacts = await ctx
  .map('contact_email_rows', rows)
  .step('work_email', (row, rowCtx) =>
    rowCtx.runPlay(
      'name_domain_email',
      'prebuilt/name-and-domain-to-email-waterfall',
      {
        first_name: row.first_name,
        last_name: row.last_name,
        domain: row.domain,
        company_name: row.company_name,
        linkedin_url: row.linkedin_url,
      },
      {
        description: 'Resolve a work email with the canonical prebuilt play.',
      },
    ),
  )
  .step('export_row', (row) => ({
    company_name: row.company_name,
    domain: row.domain,
    contact_name: `${row.first_name} ${row.last_name}`.trim(),
    email: row.work_email?.email ?? null,
    source: 'prebuilt/name-and-domain-to-email-waterfall',
    status: row.work_email?.email ? 'found' : 'missing',
  }))
  .run({
    key: (row) => `${row.first_name}:${row.last_name}:${row.domain}`,
    description: 'One reusable child play call per contact identity.',
  });
```

For CSV-backed prebuilt plays, keep the CSV path relative to the eval/project working directory so the SDK can stage the file for the worker:

```bash
deepline plays describe prebuilt/name-and-domain-to-email-waterfall-batch --json
deepline plays run prebuilt/name-and-domain-to-email-waterfall-batch --input '{"csv":"data/leads.csv"}' --watch
deepline runs export <run-id> --out leads_with_emails.csv
```

Do not pass `/Users/.../data/leads.csv` or another absolute local path to a prebuilt play unless `plays describe` explicitly says absolute local files are supported.

## Provider Discovery By Capability

Names rot. Tags are the live map; `describe` is the contract. Use provider names as examples only after discovering the current tool universe.

- company search: `adyntel_facebook`, `adyntel_facebook_ad_search`, `adyntel_google`, `adyntel_linkedin`, `adyntel_tiktok_search`, `ai_ark_company_search`, `apollo_company_search`, `attio_query_company_records`, `attio_query_records`, `attio_search_records`, `bloomberry_get_current_customers`, `bloomberry_list_vendors`, +50 more
- people search: `ai_ark_export_people`, `ai_ark_export_results`, `ai_ark_people_search`, `apollo_people_search`, `apollo_people_search_paid`, `apollo_search_people`, `apollo_search_people_with_match`, `attio_query_person_records`, `attio_query_records`, `attio_search_records`, `contactout_search_people`, `crustdata_people_search`, +42 more
- company enrichment: `apollo_bulk_organization_enrichment`, `apollo_enrich_company`, `apollo_get_complete_organization_info`, `apollo_organization_enrich`, `attio_assert_record`, `bloomberry_get_company_tech_stack`, `contactout_enrich_domain`, `crustdata_company_enrichment`, `crustdata_enrich_company`, `crustdata_v2_enrich_company`, `datagma_enrich_company`, `datagma_full_enrichment`, +36 more
- people enrichment: `ai_ark_mobile_phone_finder`, `ai_ark_personality_analysis`, `ai_ark_reverse_lookup`, `apollo_bulk_people_enrichment`, `apollo_enrich_person`, `apollo_people_match`, `apollo_reveal_person`, `apollo_search_people_with_match`, `attio_assert_record`, `bettercontact_bulk_enrich`, `bettercontact_enrich`, `bettercontact_get_result`, +63 more
- email finder: `ai_ark_find_emails`, `datagma_find_email`, `dropleads_email_finder`, `findymail_find_from_business_profile`, `findymail_find_from_name`, `forager_person_contacts_lookup_personal_emails`, `forager_person_contacts_lookup_work_emails`, `hunter_email_finder`, `leadmagic_b2b_social_email`, `leadmagic_email_finder`, `leadmagic_personal_email_finder`, `openmart_lookup_business_email`, +1 more
- phone finder: `ai_ark_mobile_phone_finder`, `datagma_search_phone_numbers`, `dropleads_mobile_finder`, `enrich_phone`, `enrich_phone_finder`, `findymail_find_phone`, `forager_person_contacts_lookup_phone_numbers`, `leadmagic_mobile_finder`, `upcell_enrich_contact`
- email verify: `dropleads_email_verifier`, `findymail_verify_email`, `hunter_email_verifier`, `icypeas_email_verification`, `ipqs_batch_email_verify`, `ipqs_email_verify`, `leadmagic_email_validation`, `zerobounce_validate`
- phone verify: `ipqs_batch_phone_validate`, `ipqs_phone_validate`, `trestle_phone_validation`, `trestle_real_contact`
- domain search: `findymail_find_from_domain`, `hunter_domain_search`, `icypeas_domain_search`, `zerobounce_domain_search`
- research: `ai_ark_personality_analysis`, `builtwith_recommendations`, `builtwith_vector_search`, `dataforseo_backlinks_anchors_live`, `dataforseo_backlinks_backlinks_live`, `dataforseo_backlinks_bulk_backlinks_live`, `dataforseo_backlinks_bulk_new_lost_backlinks_live`, `dataforseo_backlinks_bulk_new_lost_referring_domains_live`, `dataforseo_backlinks_bulk_pages_summary_live`, `dataforseo_backlinks_bulk_ranks_live`, `dataforseo_backlinks_bulk_referring_domains_live`, `dataforseo_backlinks_bulk_spam_score_live`, +82 more
- autocomplete: `crustdata_companydb_autocomplete`, `crustdata_persondb_autocomplete`, `crustdata_v2_companydb_autocomplete`, `crustdata_v2_filters_autocomplete`, `crustdata_v2_persondb_autocomplete`, `forager_industry_autocomplete`, `forager_location_autocomplete`, `forager_organization_autocomplete`, `forager_organization_keyword_autocomplete`, `forager_person_skill_autocomplete`, `forager_web_technology_autocomplete`, `openwebninja_localbusiness_autocomplete`, +3 more

Use provider tools as a fallback after play routing. `tools list` is inventory; `tools grep ... --categories <category>` is category-filtered retrieval. Use at most two tool retrieval calls before describing a real tool. Provider names like `apollo`, `crustdata`, `hunter`, or `fullenrich` are not tool ids.

```bash
deepline tools list --categories company_search --json
deepline tools grep "company search" --categories company_search --search_terms "funding headcount hq" --json
deepline tools grep "people search title seniority linkedin" --categories people_search --json
deepline tools describe <company-search-tool-id> --json
deepline tools describe <people-search-tool-id> --json
deepline tools describe <email-finder-tool-id> --json
deepline tools describe <phone-verify-tool-id> --json
```

Use `describe` for inputs, Deepline-facing cost, target getters, list getters, sample shape, enum hints, and failure modes.

Never scrape `describe` with shell helpers. Bad: `deepline tools describe dropleads_email_finder 2>&1 | python3 -c ...`, `... | grep deeplineUsdPerPricingUnit`, `... | head -80`. Good: `deepline tools describe dropleads_email_finder --json`, then read the `cost`, `deeplineUsdPerPricingUnit`, `inputSchema`, and `toolResult` fields from that command output.

## Getter Discipline

Code should mirror `deepline tools describe`: list tools use `extractedLists.*.get()`, scalar finder/enrichment tools use `extractedValues.*.get()`, validators use normalized status getters like `email_status` and `phone_status` when declared.

```text
// Search/list tools return extractedLists. The list name is declared by `deepline tools describe`.
const companies = result.extractedLists.companies.get();
const people = result.extractedLists.people.get();

// Finder/enrichment tools usually return scalar extractedValues.
const email = emailResult.extractedValues.email.get();
const phone = phoneResult.extractedValues.phone.get();

// Validators validate known channels after discovery; they do not find channels.
const emailStatus = emailVerifier.extractedValues.email_status.get();
const phoneStatus = phoneVerifier.extractedValues.phone_status.get();

// Batch validators return rows. Check the list getter keys from `deepline tools describe`.
const phoneRows = batchPhoneVerifier.extractedLists.phone_batch.get();
```

Optional-chain payload archaeology is not a sample pattern. If the workflow needs a field that `describe` does not expose as a getter, fix the provider metadata or choose a tool with the getter the workflow needs.

Getter errors are real runtime failures. `Cannot read properties of undefined (reading 'get')` means the code called a getter that was not declared or not present for that tool result; stop and fix the tool choice, provider metadata, or getter usage before scaling. Do not hide this with `?.get?.()` or raw payload fallbacks. Transient provider failures are different: wrap flaky paid fallback legs in `try/catch` and return a row-level `{ status: 'missing', source, miss_reason: 'provider_error' }` so one provider outage does not kill the whole map.

Each provider leg must use its own described input names and declared getters. Do not assume all email-ish tools accept `first_name`, `last_name`, `domain`, or expose the same getter set. A tool belongs in a name+domain work-email waterfall only when `describe` proves it accepts person identity plus company/domain context and declares `extractedValues.email.get()`.

The complete generated getter catalog for this checkout:

Scalar getters use `result.extractedValues.<target>.get()`. These are the complete scalar target names the SDK knows about:

| Getter group | Every possible scalar target in that group |
| --- | --- |
| Identity values | `id`, `name`, `email`, `phone`, `linkedin`, `linkedin_url`, `domain`, `first_name`, `last_name`, `full_name`, `company`, `company_name`, `organization_name`, `company_domain`, `company_website`, `company_linkedin_url`, `website` |
| Context values | `title` |
| Validator/status values | `status`, `email_status`, `phone_status` |

List getters use `result.extractedLists.<listName>.get()`. Current generated catalog list names:

`ads`, `audiences`, `changes`, `channels`, `companies`, `company`, `contacts`, `content`, `data`, `departments`, `domain_associations`, `domains`, `email_batch`, `emails`, `employees`, `experiences`, `groups`, `Inbound`, `interim_results`, `items`, `job_title_suggestions`, `jobs`, `Keywords`, `leads`, `links`, `listings`, `lists`, `location_suggestions`, `matched`, `matches`, `messages`, `monitors`, `monthly_headcounts`, `organic`, `organizations`, `Outbound`, `patterns`, `people`, `person`, `persons`, `phone_batch`, `phones`, `pipelines`, `posts`, `profiles`, `prospects`, `records`, `Relationships`, `result`, `results`, `Results`, `rows`, `search_results`, `shops`, `signals`, `skills`, `social_media`, `speakers`, `suggestions`, `technologies`, `topCompetitors`, `users`, `vendors`, `web`, `website_technologies`

## Scratchpad Play Notebook

The scratchpad must be a play. It is more than spend control: it is the notebook allowance that lets you learn by writing code. Once a source or enrichment step has run with a stable id, reruns can reuse that provider output for instant extraction, new scoring, new getters, new export columns, and new evidence concepts without another provider call.

Stable IDs are notebook handles. Keep source and enrichment step IDs stable while editing downstream logic. Rename a paid step only when you deliberately want a fresh provider call.

Before editing a play, identify whether the change is upstream paid source work, row-level paid fanout, or downstream cheap logic. Getter fixes, filters, scoring, placeholder cleanup, and export shape must happen downstream of paid steps.

- Direct `tools execute` probes before a play: max 3 total, including autocomplete/count.
- Probe free/count first, then `limit: 1-3`.
- Once a probe returns useful rows or a plausible count, move that call into a play with a stable `id`.
- In plays, `ctx.tools.execute` shape is `{ id, tool, input, description }`; provider request fields go inside `input`, not beside it.
- Not every play step should execute a tool. Use pure `.step(...)` stages for normalization, scoring, fit checks, placeholder cleanup, fanout estimates, and final export projection.
- The first play version should copy the exact probe payload that worked. Do not make filters fancier inside the play.
- A pilot is not complete until you have verified row shape, declared getters, null semantics, status fields, provider errors, and the fanout shape.
- No mapped paid enrichment until the code contains or logs the estimated fanout: candidate rows * paid providers * fallback legs.
- If a map step's logic changes but row keys and inputs stay the same, change that step `id` before the next run. This includes placeholder filtering, exception handling, getter-path fixes, scoring, and export-shape changes.
- After one source-shape correction to the same provider, stop tuning that provider for count. Add a disjoint branch, relax downstream filters, or export partials with miss reasons.

## Source Patterns

Choose the route before choosing the provider.

- **Company-first contacts** — source companies, fit/dedupe domains, then people search inside that domain set. Use this when account category, ICP, portfolio, or vertical matters.
- **People-first markets** — valid only when account fit is broad, already supplied, or irrelevant. Otherwise people search drifts into off-ICP accounts.
- **Known-person enrichment** — use the strongest supplied identifier: standard LinkedIn `/in/`, name + domain, or email/phone to validate.
- **Niche account seeding** — use evidence-grade semantic or research sources when structured taxonomies are empty, broad, or noisy.
- **Firmographic TAM** — use structured company search when stage, headcount, funding, country, or exact category controls the market.
- **Email waterfall** — find email after person/domain fit. Prefer prebuilt name/domain email plays; in manual waterfalls use strict person+domain finders first, one fallback, then nullable miss reason.
- **Phone waterfall** — find phone after fit; validate known phones with `phone_verify` tools, do not use validators as finders.
- **Domain search** — discover domain-level patterns or inventory. It is not named-person email discovery.

For name + company/domain work-email tasks, choose tools by contract, not just by lowest price. Strong first legs require explicit person fields plus domain/company context, for example `first_name`/`last_name`/`company_domain`, `first_name`/`last_name`/`domain`, or `name`/`domain`. Async/search-shaped tools such as `icypeas_email_search` can be useful recovery legs only after `describe` proves the exact input and getter contract; do not put them first solely because `email_finder` search ranks them cheaper. Domain-search tools are never name+domain email finders.

Manual work-email fallback shape:

```text
const tryEmailLeg = async (
  rowCtx: any,
  id: string,
  tool: string,
  input: Record<string, any>,
  source: string,
) => {
  try {
    const result = await rowCtx.tools.execute({
      id,
      tool,
      input,
      description: `${source} work-email lookup for a fitted person/domain.`,
    });
    // This getter must be copied from `deepline tools describe <tool> --json`.
    const email = result.extractedValues.email.get();
    return email
      ? { email, source, status: 'found' }
      : { email: null, source, status: 'missing', miss_reason: 'email_not_found' };
  } catch (error) {
    return { email: null, source, status: 'missing', miss_reason: 'provider_error' };
  }
};
```

For account-scoped people tasks, write the play in this order: company seed -> inspect/fit/dedupe domains -> people search with the described domain/account identifier -> final map for email/status/export. After people search, require the contact's current company domain to match the seeded domain set before email enrichment/export.

Do not turn every requested criterion into a source filter. Hard-filter on stable facets that control TAM and required columns: geography, company size, funding/stage, domain/account set, seniority. Compute fuzzy/niche criteria as evidence columns: hiring titles, category fit, tech mention, clinical/ops relevance, intent phrases, recent news.

## Recovery Patterns

When target count is short, avoid rebuying the same confusion.

- **Zero rows** — source strategy or filtering failed. Change source, relax input, or add a disjoint branch. Do not inspect raw receipts for normal GTM work.
- **Short count** — relax fuzzy filters first and keep `signal_status` / `miss_reason` columns.
- **Off-category rows** — switch source or add stricter fit evidence before people/email fanout.
- **Empty required getter** — check provider capability and `describe`; add a supplement tool only if the source row is otherwise worth enriching.
- **Placeholder emails/names** — treat values like `email_not_unlocked@...` or obfuscated names as null with `miss_reason`.
- **Expensive fanout** — score/filter before enrichment, batch where possible, cap the run, or export a labeled partial.
- **Broad taxonomy** — do not accept parent categories like Software, Health Care, Financial Services, or IT Services as niche proof without evidence.
- **Pagination** — if a source has `page`/`per_page`, unroll enough pages with static IDs in the first play; do not discover pagination through multiple full reruns.

## Code Recipes

Keep code compact, typed, and commented where the contract matters.

```text
const compact = (o: Record<string, any>) =>
  Object.fromEntries(Object.entries(o).filter(([, v]) => v !== null && v !== undefined && v !== ''));

const cleanDomain = (v: any) =>
  String(v ?? '').trim().toLowerCase().replace(/^https?:\/\//, '').replace(/^www\./, '').split('/')[0];

const companyDomain = (r: any) =>
  cleanDomain(r.domain ?? r.domains?.[0] ?? r.primary_domain ?? r.company_domain ?? r.website ?? r.website_url ?? r.url);

const companyName = (r: any) => r.company_name ?? r.name;
const companyFunding = (r: any) => r.funding_round ?? r.last_funding_round_type ?? r.latest_funding_stage;
const companyHeadcount = (r: any) =>
  r.headcount ?? r.employee_count ?? r.num_employees ?? r.employee_metrics?.latest_count ?? r.employee_metrics?.latest_headcount;
```

Company-first contact scratchpad with row keys. Write it iteratively, but keep the final file runnable:

```typescript
import { definePlay, when } from 'deepline';

const compact = (o: Record<string, any>) =>
  Object.fromEntries(Object.entries(o).filter(([, v]) => v !== null && v !== undefined && v !== ''));

const cleanDomain = (v: any) =>
  String(v ?? '').trim().toLowerCase().replace(/^https?:\/\//, '').replace(/^www\./, '').split('/')[0];

const missing = (miss_reason: string, source = 'scratchpad') => ({
  status: 'missing',
  source,
  miss_reason,
});

const toAccount = (result: any) => {
  const company = result.entities?.find((e: any) => e.type === 'company')?.properties ?? {};
  return compact({
    domain: cleanDomain(result.url),
    company_name: company.name ?? result.title,
    company_fit_evidence: company.description ?? result.text ?? result.title,
    hq_country: company.headquarters?.country,
  });
};

const scoreAccountFit = (account: any) => {
  const evidence = String(account.company_fit_evidence ?? '').toLowerCase();
  const hasFit =
    account.domain &&
    String(account.hq_country ?? account.company_fit_evidence).toLowerCase().includes('united states') &&
    /fintech|payments|bank|api|platform/.test(evidence);

  return {
    status: hasFit ? 'fit' : 'needs_review',
    category: hasFit ? 'target_category' : null,
    fit_score: hasFit ? 1 : 0.4,
    miss_reason: hasFit ? null : 'weak_company_fit_evidence',
  };
};

const pickBestPerson = (people: any[]) => {
  const person = people.find((p: any) => /founder|ceo|marketing/i.test(String(p.title ?? '')));
  return person
    ? compact({
        status: 'found',
        contact_name: person.name ?? person.full_name,
        title: person.title,
        linkedin_url: person.linkedin_url ?? person.linkedin,
        first_name: person.first_name,
        last_name: person.last_name,
        current_domain: cleanDomain(person.organization?.domain ?? person.company_domain),
      })
    : missing('no_matching_person', 'people_search');
};

export default definePlay('company-first-contact-scratchpad', async (ctx, input: any = {}) => {
  const target = Math.max(1, Math.min(Number(input.target ?? 5), 25));

  // Draft 1: buy the reusable source rows. Run here first and inspect this
  // getter before adding fanout. Keep this id stable while editing below.
  const seed = await ctx.tools.execute({
    id: 'semantic_account_seed',
    tool: 'exa_company_search',
    input: {
      query: `US ${input.category ?? input.query ?? ''} companies ${input.use_case ?? ''}`,
      type: 'fast',
      numResults: Math.min(target * 3, 25),
      userLocation: 'US',
    },
    description: 'Evidence-grade niche account seed before domain-scoped people search.',
  });

  const seedRows: any[] = seed.extractedLists.results.get();

  // Draft 2: add cheap notebook logic downstream of the source call. Reruns can
  // improve account normalization, scoring, and export columns without rebuying
  // Exa because `semantic_account_seed` stayed stable.
  const contacts = await ctx
    .map('company_first_contacts', seedRows)
    .step('account', toAccount)
    .step('account_fit', (row: any) => scoreAccountFit(row.account))
    // Draft 3: add paid fanout only after fit is visible. `when` skips the
    // provider call unless the cheap step proved the row is worth spending on.
    .step('people_search', when(
      (row: any) => row.account_fit?.status === 'fit',
      async (row: any, rowCtx: any) => {
        const people = await rowCtx.tools.execute({
          id: 'domain_people_search',
          tool: 'apollo_people_search',
          input: {
            q_organization_domains_list: [row.account.domain],
            person_titles: input.roles ?? ['founder', 'ceo', 'head of marketing', 'vp marketing'],
            per_page: 3,
          },
          description: 'Find persona contacts at a sourced company domain.',
        });
        return pickBestPerson(people.extractedLists.people.get());
      },
    ))
    .step('work_email', async (row: any, rowCtx: any) => {
      const person = row.people_search;
      if (person?.status !== 'found') return missing(person?.miss_reason ?? row.account_fit?.miss_reason ?? 'no_matching_person', 'people_search');
      if (person.current_domain && person.current_domain !== row.account.domain) {
        return { email: null, source: 'domain_check', status: 'missing', miss_reason: 'out_of_seed_domain' };
      }

      // Keep paid finder ids stable. Add new scoring/export steps later without
      // rebuying successful email lookups.
      const first = await rowCtx.tools.execute({
        id: 'email_primary',
        tool: 'dropleads_email_finder',
        input: { first_name: person.first_name, last_name: person.last_name, company_domain: row.account.domain },
        description: 'Primary work email finder for fitted person/domain.',
      });
      const firstEmail = first.extractedValues.email.get();
      if (firstEmail) return { email: firstEmail, source: 'dropleads_email_finder', status: 'found' };

      const second = await rowCtx.tools.execute({
        id: 'email_fallback',
        tool: 'hunter_email_finder',
        input: { first_name: person.first_name, last_name: person.last_name, domain: row.account.domain },
        description: 'Fallback work email finder only for still-missing rows.',
      });
      const secondEmail = second.extractedValues.email.get();
      return secondEmail
        ? { email: secondEmail, source: 'hunter_email_finder', status: 'found' }
        : { email: null, source: 'email_waterfall', status: 'missing', miss_reason: 'email_not_found' };
    })
    .step('export_row', (row: any) => ({
      company_name: row.account.company_name,
      domain: row.account.domain,
      category: row.account_fit?.category ?? null,
      company_fit_evidence: row.account.company_fit_evidence,
      fit_score: row.account_fit?.fit_score ?? null,
      contact_name: row.people_search?.contact_name ?? null,
      title: row.people_search?.title ?? null,
      linkedin_url: row.people_search?.linkedin_url ?? null,
      email: row.work_email?.email ?? null,
      source: row.work_email?.source ?? 'company_first_contacts',
      status: row.work_email?.status ?? row.people_search?.status ?? row.account_fit?.status ?? 'missing',
      miss_reason: row.work_email?.miss_reason ?? row.people_search?.miss_reason ?? row.account_fit?.miss_reason ?? null,
    }))
    .run({
      key: (row: any) => cleanDomain(row.url),
      description: 'One idempotent row per sourced account domain; reruns can add new steps without rebuying completed provider work.',
    });

  return { contacts };
});
```

Map steps can be pure computation or provider calls. Use tool steps only when the row needs external data; use pure steps for shaping, gating, scoring, and export. Step outputs nest under the step name: after `.step('leader', ...)`, read `row.leader?.email`, not `row.email`. Object-returning steps export as `step.field` columns. If the user needs clean `email` or `name` columns, make the final step return those exact flat fields.

`ctx.map` is a builder, not an array mapper. The value returned by `.run()` is a `PlayDataset` export handle; do not call `.find`, `.map`, `.filter`, spread it, index it, or cast it to `any` to build a second map. Put enrichment and final export columns in one map when possible.

## Anti-Patterns

- **Console Panning** — running one-off executes and visually harvesting rendered output. Correction: move any useful provider call into the scratchpad `.play.ts` immediately.
- **Unstable Paid IDs** — renaming source, enrichment, or map step IDs while editing cheap downstream logic. Correction: keep paid step IDs stable; only rename to intentionally invalidate/rebuy.
- **Spend-Blind Fanout** — mapping paid enrichment over noisy rows without calculating the multiplier. Correction: dedupe/filter/score first; estimate rows * providers * fallback legs.
- **Same-Source Thrashing** — repeatedly tweaking one paid provider query to chase count. Correction: after one source-shape fix, branch, relax downstream filters, or export misses.
- **Getter Archaeology** — writing `?.get?.() ?? raw?.result?.data` style code. Correction: call declared getters directly; if a getter is missing, repair metadata or choose a tool that declares the needed getter.
- **Validation As Discovery** — using email/phone validators to find channels. Correction: validators only check known emails/phones; use finder tags for discovery.
- **People-First Category Drift** — searching people before account fit is established for company-scoped tasks. Correction: seed companies/domains first, then search/enrich people inside that set.
- **Domain Search Confusion** — treating domain search as named-person email finding. Correction: domain search discovers domains/patterns; email finders find person emails.
- **Silent Null Collapse** — dropping rows or blanking fields without explanation. Correction: emit `status`, `source`, and `miss_reason`.
- **Raw Export Leakage** — shipping nested provider objects or provider-shaped column names. Correction: project to flat user-facing columns with evidence and provenance.

## Export Contract

If the user asked for CSV/export, make the final rows an exportable dataset: return rows from `ctx.map(...).run`, not a plain array.

Final CSVs must use user-facing columns, not provider-shaped aliases. Contact deliverables use the requested `name` or `contact_name`, plus `title`, `linkedin_url`, `email`, `source`, `status`, and `miss_reason`. Category/account deliverables include `category` or `<vertical>_category` even when source taxonomy is also exported as `industry`.

Do not return full provider objects from map steps at scale. Extract compact scalars inside the step and return only fields needed downstream.

## Final Self-Review

Before handing results back, check:

- The source calls that bought useful rows live in the scratchpad play.
- Paid source/enrichment IDs are stable unless intentionally rebuying.
- The code uses declared getters directly.
- Validators only validate known channels.
- Account-scoped contacts are inside the seeded domain set.
- Fanout cost was estimated before scale.
- Final rows are flat, user-facing, and include evidence/provenance/status/miss reasons.
