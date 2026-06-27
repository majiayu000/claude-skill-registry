---
name: deepline-ads-audiences
description: "Use this skill when building, enriching, auditing, or uploading B2B paid ads audiences to Google Customer Match, Meta/Facebook Custom Audiences, or LinkedIn Matched Audiences. Triggers on phrases like '/deepline-ads-audience', '/deepline-ads-audiences', 'upload this audience', 'create custom audiences', 'personal email hashes', 'increase Facebook match rate', 'Google ads audience', 'Meta audience', 'FB audience', or any workflow that turns CRM/customer/contact data into paid ads upload lists. Skip for outbound prospecting sequences, cold email, or pure campaign copywriting."
---

# Deepline Ads Audiences

Build high-quality ABM paid ads audiences from first-party customer or prospect lists. This skill is for paid ads audience upload and evaluation, not outbound.

Names in this skill are starting hints. Run `deepline tools search audience --json` and `deepline tools get <tool_id> --json` before executing because tool names and payload shapes can change.

## Before You Start

Use the full recipe when the user asks to enrich and upload audiences to Facebook/Meta and Google:

→ Read `recipes/enrich-and-upload-facebook-google.md`.

Use the max-coverage recipe when the user asks for "max coverage", "maximum match rate", "keep increasing coverage", "get to 75% coverage", or asks to exhaust LinkedIn/personal-email/hash options:

→ Read `recipes/max-coverage-audience.md`.

This skill is not for cold outbound, sequencing, or copywriting. Personal emails here are used to improve paid ads matching, not to contact people directly.

## Decision Matrix

| User says                                                             | Do this                                                          | Read                                                      |
| --------------------------------------------------------------------- | ---------------------------------------------------------------- | --------------------------------------------------------- |
| "max coverage", "highest match rate", "keep increasing coverage"      | Run the explicit max-coverage ladder with budget gates.          | `recipes/max-coverage-audience.md`                        |
| `/deepline-ads-audience`, "enrich and upload to FB/Google"            | Run the full paid ads audience recipe.                           | `recipes/enrich-and-upload-facebook-google.md`            |
| "sample ABM segment", "do the example workflow"                       | Follow the reusable high-priority ABM segment recipe.            | `recipes/sample-abm-segment-example.md`                   |
| "Make sure hashes are not double hashed"                              | Run the no-double-hash audit play before upload.                 | `plays/audit-no-double-hash.play.ts`                      |
| "Compare enriched versus unenriched"                                  | Build both hash-only datasets and report lift.                   | `plays/build-hash-only-audience.play.ts`                  |
| "Upload to Google"                                                    | Validate hash-only rows, create Google audience, sync, readback. | `plays/upload-google-hash-only-audience.play.ts`          |
| "Upload to Facebook and Google", "upload to FB/Google", "Meta + GAds" | Validate once, then upload to Google and Meta.                   | `plays/upload-facebook-google-hash-only-audience.play.ts` |

## Default Workflow

1. Confirm rights, use case, and geography.
2. Discover uploadable ad accounts.
3. Build baseline and enriched audience objects.
4. Validate identifiers and expected match-rate lift.
5. Create separate platform audiences.
6. Upload rows.
7. Check status and report IDs, uploaded counts, invalid rows, and current build state.

## Coverage Modes

Choose the coverage mode before spending credits. Record it in the run notes.

| Mode | Use when | Waterfall | Stop condition |
| --- | --- | --- | --- |
| `cost_effective` | User asks for the default, low-cost, or first-pass enrichment. | Work-email baseline → Aviato personal hashes on all eligible rows → LimaData personal hashes on remaining personal-hash misses. | Stop after Aviato/LimaData, report contacts still missing personal hashes, then ask before expanded fallback. |
| `max_coverage` | User asks for highest match rate, max coverage, or to keep increasing coverage. | Work-email baseline → phone hashes already present → LinkedIn repair → Aviato personal hashes for all eligible rows → LimaData personal hashes → raw personal-email waterfall → platform upload variants. | Stop when no approved provider remains, budget cap is hit, marginal lift is below threshold, or rights/geo constraints block more enrichment. |

Never silently downgrade a `max_coverage` request to `cost_effective`. If a provider or credential is unavailable, report the gap and continue with the next approved provider rather than stopping early.

## Shareable Plays

This skill includes copyable play templates under `plays/`. Use them when the user asks for a repeatable or shareable workflow, not just a one-off CLI run.

Use the V2 play path when `deepline plays --help` is available. Use the V1 command path in `recipes/enrich-and-upload-facebook-google.md` when the installed CLI only supports `deepline enrich`, `deepline tools`, or legacy workflow commands. If neither path can run, stop and ask for the Deepline CLI or SDK CLI to be installed instead of approximating the upload.

| Play                                                      | Purpose                                                                                                                                                        | Input                                                                                                                                                                     |
| --------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `plays/build-hash-only-audience.play.ts`                  | Build baseline and enriched hash-only datasets from source CSV rows. Raw emails are normalized and hashed once. Provider hashes pass through as lowercase hex. | `{ "file": "input.csv" }`                                                                                                                                                 |
| `plays/audit-no-double-hash.play.ts`                      | Verify the final upload payload is hash-only, deduped, populated, includes provider hashes as-is, and does not contain hash-of-hash mistakes.                  | `{ "payloadFile": "upload.csv", "providerHashFile": "provider-hashes.csv", "providerHashColumns": ["aviato_hash", "limadata_hash"] }`                                     |
| `plays/upload-google-hash-only-audience.play.ts`          | Create a Google Customer Match list, upload hash-only rows, and read status back.                                                                              | `{ "file": "upload.csv", "account_id": "1234567890", "audience_name": "Segment enriched 2026-06-09" }`                                                                    |
| `plays/upload-facebook-google-hash-only-audience.play.ts` | Upload the same validated hash-only rows to Google and an existing Meta/Facebook Custom Audience.                                                              | `{ "file": "upload.csv", "google_account_id": "1234567890", "meta_ad_account_id": "act_123", "meta_audience_id": "456", "audience_name": "Segment enriched 2026-06-09" }` |
| `plays/report-google-coverage-lift.play.ts`               | After Google match rates populate, calculate coverage lift, estimated matched identifiers, spend efficiency, and a follow-up note.                             | `{ "account_name": "Customer Google Ads", "account_id": "1234567890", "baseline": {...}, "comparisons": [...] }`                                                           |

Recommended sequence:

```bash
deepline plays check .skills/deepline-ads-audiences/plays/build-hash-only-audience.play.ts
deepline plays run --file .skills/deepline-ads-audiences/plays/build-hash-only-audience.play.ts --input '{"file":"source.csv"}' --watch

deepline plays check .skills/deepline-ads-audiences/plays/audit-no-double-hash.play.ts
deepline plays run --file .skills/deepline-ads-audiences/plays/audit-no-double-hash.play.ts --input '{"payloadFile":"enriched_hash_only.csv","providerHashFile":"provider_hashes.csv","providerHashColumns":["aviato_hash","limadata_hash"]}' --watch

deepline plays check .skills/deepline-ads-audiences/plays/upload-google-hash-only-audience.play.ts
deepline plays run --file .skills/deepline-ads-audiences/plays/upload-google-hash-only-audience.play.ts --input '{"file":"enriched_hash_only.csv","account_id":"1234567890","audience_name":"ABM enriched hash-only 2026-06-09"}' --watch

deepline plays check .skills/deepline-ads-audiences/plays/upload-facebook-google-hash-only-audience.play.ts
deepline plays run --file .skills/deepline-ads-audiences/plays/upload-facebook-google-hash-only-audience.play.ts --input '{"file":"enriched_hash_only.csv","audience_name":"ABM enriched hash-only 2026-06-09","google_account_id":"1234567890","meta_ad_account_id":"act_123","meta_audience_id":"456"}' --watch

deepline plays check .skills/deepline-ads-audiences/plays/report-google-coverage-lift.play.ts
deepline plays run --file .skills/deepline-ads-audiences/plays/report-google-coverage-lift.play.ts --input '{"account_name":"Customer Google Ads","account_id":"1234567890","segment_name":"High-priority target-account audience","source_rows":20000,"baseline":{"label":"L1 work hash-only","audience_id":"1111111111","match_rate_pct":23,"uploaded_rows":13935},"comparisons":[{"label":"L2 Lima+Aviato hash-only","audience_id":"2222222222","match_rate_pct":35,"uploaded_rows":18386,"deepline_spend_usd":51.47},{"label":"L3 all hashes only","audience_id":"3333333333","match_rate_pct":43,"uploaded_rows":24787},{"label":"L4 all hashes + details","audience_id":"4444444444","match_rate_pct":42,"uploaded_rows":24787},{"label":"L5 LeadMagic top100 fallback","audience_id":"5555555555","match_rate_pct":44,"uploaded_rows":17016},{"label":"L6 GTM LinkedIn + Lima/Aviato","audience_id":"6666666666","match_rate_pct":45,"uploaded_rows":17064}],"spend":{"low_cost_hash_usd":51.47,"contact_fallback_usd":218.37,"total_usd":269.84},"recommendation_label":"L6 GTM LinkedIn + Lima/Aviato"}' --watch
```

Export dataset outputs after a run with:

```bash
deepline runs export <run-id> --out audience-output.csv
```

Before using the upload play, run account discovery from Step 2 and confirm the selected Google Ads account name and ID with the user.

## Step 1: Confirm Rights

Ask for explicit confirmation when the source data belongs to a customer workspace or third party. The minimum confirmation is:

- The source list can be used for paid ads audience creation.
- Any enrichment identifiers can be used for paid ads matching.
- The requested platforms are allowed for this use case.
- Geography is in scope. Default to US-only when personal identifiers are being enriched unless the user specifies otherwise and confirms compliance.

Do not use this skill for outbound email, phone, or sequencing. The output is audience upload data and platform audience IDs.

## Step 2: Discover Uploadable Accounts

Run account discovery before every live upload. Agents often guess account IDs from prior context, app IDs, or UI labels. That creates audiences in the wrong account or fails after enrichment spend has already happened.

Use this discovery ladder:

1. Search for live account tools:

```bash
deepline tools search "ads audience account discovery google meta linkedin" --json
deepline tools list | grep -Ei "account|audience"
```

2. If a platform exposes a direct account discovery tool or endpoint, use it first. Record account name, account ID, platform, permission status, and whether customer list upload is supported.

3. If no direct discovery tool is exposed, ask the user for the account ID and name, then validate it before upload:

```bash
deepline tools execute google_ads_audiences_list_audiences --payload '{"account_id":"1234567890","page_size":10}' --json
deepline tools execute meta_audiences_list_audiences --payload '{"ad_account_id":"1234567890"}' --json
deepline tools execute linkedin_ads_audiences_list_audiences --payload '{"account_id":"urn:li:sponsoredAccount:123456789"}' --json
```

4. Show the discovered choices back to the user as `Account Name (Account ID)`, grouped by platform. If there is more than one plausible account, ask which one to use before creating audiences.

5. Keep the selected account IDs in the run notes and final answer. Never use a Meta app ID as an ad account ID. Meta upload IDs should look like `act_123...` or a numeric ad account ID that Deepline can prefix.

## Step 3: Build Baseline and Enriched Objects

Create two separate objects when evaluating lift:

- `unenriched`: first-party source identifiers only, usually work email plus name, company, country, postal code, and LinkedIn URL context.
- `enriched`: source identifiers plus paid-ads-safe enrichment. Prefer hashed personal email providers first, then raw personal-email providers that can be normalized and hashed locally.

Default personal-email waterfall for B2B paid ads:

1. Baseline first-party identifiers: valid work emails, names, company, country, postal code, LinkedIn URLs, and stable external IDs.
2. Aviato `aviato_pull_email_hash`: run on all eligible rows with enough identity context, including rows that already have work emails. Use it when the goal is ad upload and the provider returns paid-ads-ready personal email hashes. If the output cell is a JSON object, extract the scalar hash from `matched_result`, `result.data.hashedEmails[0]`, `result.data.hashed_email`, or equivalent hash fields. Do not treat the JSON object string as the upload value.
3. LimaData `limadata_find_audience_identifiers`: run on rows still missing a personal hash after Aviato, or run it first when the user asks for the most cost-effective expansion pass. Extract only normalized 64-character SHA-256 hashes from `matched_result`, `result.data.hashed_emails[].normalized_hash`, `hash`, or `sha256` fields.

Stop after Aviato and LimaData by default. Report attempted rows, row hits, unique hashes added, contacts still missing personal hashes, and Deepline spend. Then ask whether the user wants to pay about 0.08 USD/contact in additional Deepline spend to increase coverage with broader raw personal-email providers.

Only run the expanded coverage pass after explicit approval. In that pass, try providers such as LeadMagic, ContactOut, Wiza, Datagma, Crustdata, Prospeo, FullEnrich, PDL, or Deepline native personal-email waterfalls on rows still missing personal hashes. Normalize and SHA-256 hash raw personal emails exactly once, record provider-level lift and Deepline spend, and keep the default upload payload hash-only.

Do not buy mobile phones for this workflow unless the user explicitly asks. They are usually too expensive for this ads-audience test.

For `max_coverage`, the user has already approved the goal but not unlimited spend. Ask for or infer a budget cap before paid fallback beyond Aviato/LimaData. If the user gave a cap, run the expanded pass until the cap or marginal-lift stop condition is reached.

For native waterfall outputs, include only provider-specific fields that are confirmed personal-email responses, such as `first_personal_email`, `personal_email`, `personal_emails[]`, or Wiza email values where `email_type` is personal. Do not include an untyped final scalar just because it contains an email address. Untyped final values can be work emails.

Keep row lineage in both objects:

- `external_id`
- `source_row_number`
- `person_linkedin_url`
- `company_name`
- `company_domain`
- `provider_used`
- `identifier_type`

This lets the user evaluate whether enrichment improved upload coverage without losing the source list.

### LinkedIn URL Backfill for Audience Enrichment

When LinkedIn URLs are needed before personal-email/hash enrichment, use a measured query ladder instead of one exact-company query. In a high-priority ABM eval sample, exact account-name search recovered the known URL in the top five for `51.7%` of rows, while the account-or-LinkedIn-company query recovered `65.8%`. Quoted domain search was much worse (`5.8%`) and should not be a first-pass default.

Start with the native `name_to_linkedin_url_waterfall` / `name-to-linkedin-url` play when available. It cleans company anchors with the same helper used by the API:

- `RTX Corporation` → `RTX`
- `Lockheed Martin Corporation` → `Lockheed Martin`
- `NASA - National Aeronautics and Space Administration` → `NASA` plus a secondary long-form alias
- `L3Harris (formerly Aerojet Rocketdyne)` → `L3Harris`
- `Siemens Energy Global GmbH & Co. KG` → `Siemens Energy`
- `Airbus EMEA` → `Airbus`

The first Serper query should use the cleaned account/LinkedIn company aliases:

```text
"{{full_name}}" ("{{account_name}}" OR "{{linkedin_company_name}}") site:linkedin.com/in -inurl:dir -inurl:pub
```

Then validate candidates before using them:

1. Keep only `linkedin.com/in/` URLs and strip query params/trailing slashes.
2. Reject search results where the profile title does not contain a first-name match and a last-name match. Allow common nicknames and meaningful first-name prefixes; do not accept single-letter last-name initials as validated.
3. Use company/title evidence as supporting evidence, not as identity proof.
4. For ambiguous candidates, scrape the profile with Apify or another LinkedIn profile-detail provider and validate scraped `first_name`, `last_name`, current company, and headline before merging. This catches snippet false positives such as a search result mentioning the target name in another person's experience section.

Use follow-up queries only after the first pass misses:

```text
"{{full_name}}" "{{title}}" "{{linkedin_company_name}}" site:linkedin.com/in -inurl:dir -inurl:pub
"{{full_name}}" "{{account_name}}" site:linkedin.com/in -inurl:dir -inurl:pub
```

Do not make quoted domain (`"{{domain}}"`) the first query. It can help occasional rows, but in the eval sample it reduced recall and caused more provider failures.

## Step 4: Validate Identifiers

Before upload, remove empty strings and malformed hashes from the payload. Deepline platform validators reject empty `email` fields and non-64-character `email_sha256` values.

Valid upload row fields include:

- `email`
- `email_sha256`
- `phone`
- `phone_sha256`
- `first_name`
- `last_name`
- `country_code`
- `postal_code`
- `company_name`
- `title`
- `company_domain`
- `person_linkedin_url`
- `external_id`

Prefer `email_sha256` when a provider returns a paid-ads-ready hash. Provider hashes must pass through exactly as lowercase 64-character hex. Do not double-hash provider hashes.

When a provider returns raw personal email:

1. Trim whitespace.
2. Lowercase the email.
3. Validate it with a normal email pattern.
4. Hash the normalized email with SHA-256 exactly once.
5. Upload only `email_sha256` unless the user explicitly asked to upload raw email fields.

Before live upload, write a small audit with:

- source row count
- valid baseline work-email count
- provider row hits
- hashes seen by provider
- unique hashes added by provider
- invalid hash rows
- whether any raw `email` field remains in the upload payload

## Step 5: Create and Upload

Create one audience per platform per object. Name them so the account UI makes the test clear:

- `<customer or segment> enriched <date>`
- `<customer or segment> unenriched <date>`

Then upload each object separately.

Current starting hints:

```bash
deepline tools execute google_ads_audiences_create_audience --payload '{"account_id":"1234567890","name":"Example enriched hash-only","membership_life_span_days":540,"upload_key_types":["CONTACT_ID"]}' --json
deepline tools execute google_ads_audiences_sync_audience_members --payload '{"account_id":"1234567890","audience_id":"1111111111","mode":"append","terms_of_service_accepted":true,"consent":{"ad_user_data":"GRANTED","ad_personalization":"GRANTED"},"rows":[{"email_sha256":"973dfe463ec85785f5f95af5ba3906eedb2d931c24e69824a89ea65dba4e813b"}]}' --json

deepline tools execute meta_audiences_create_audience --payload '{"ad_account_id":"1234567890","name":"Example enriched hash-only","customer_file_source":"BOTH_USER_AND_PARTNER_PROVIDED"}' --json
deepline tools execute meta_audiences_sync_audience_members --payload '{"ad_account_id":"1234567890","audience_id":"1111111111","mode":"replace","rows":[{"email_sha256":"973dfe463ec85785f5f95af5ba3906eedb2d931c24e69824a89ea65dba4e813b"}]}' --json

deepline tools execute linkedin_ads_audiences_create_audience --payload '{"account_id":"urn:li:sponsoredAccount:123456789","name":"Example enriched hash-only","audience_kind":"contacts"}' --json
deepline tools execute linkedin_ads_audiences_sync_audience_members --payload '{"account_id":"urn:li:sponsoredAccount:123456789","audience_id":"1111111111","mode":"replace","rows":[{"email_sha256":"973dfe463ec85785f5f95af5ba3906eedb2d931c24e69824a89ea65dba4e813b"}]}' --json
```

Use `append` for Google when uploading into a newly created empty audience if `replace` returns provider-side Data Manager payload errors. Report that clearly because it indicates connector behavior that should be fixed.

## Step 6: Verify and Report

Run status checks after upload:

```bash
deepline tools execute google_ads_audiences_get_audience_status --payload '{"account_id":"1234567890","audience_id":"1111111111"}' --json
deepline tools execute meta_audiences_get_audience_status --payload '{"ad_account_id":"1234567890","audience_id":"1111111111"}' --json
deepline tools execute linkedin_ads_audiences_get_audience_status --payload '{"account_id":"urn:li:sponsoredAccount:123456789","audience_id":"1111111111"}' --json
```

Final answer format:

- Platform and account name plus ID.
- Audience name and audience ID.
- Object type: enriched or unenriched.
- Uploaded count.
- Invalid count.
- Request IDs or session IDs.
- Current status. Note that match size and match-rate ranges may stay null while platforms process the audience.

If upload fails, report the provider error category and request ID. Do not say the audience worked unless create, sync, and readback status all succeeded.

### Google Coverage Follow-Up Reporting

After Google match rates populate, use `plays/report-google-coverage-lift.play.ts` to prevent hand-calculation drift. The play should be run from the same match-rate readback that listed the Google account name and ID. It calculates:

- percentage-point lift versus baseline
- relative lift versus baseline
- estimated matched identifiers from uploaded rows and match rate
- incremental matched identifiers versus baseline
- Deepline spend and blended cost per incremental matched identifier when spend is provided
- a ready-to-send follow-up note

Use anonymized or customer-approved values in customer-facing follow-up notes. Keep account IDs, audience IDs, match rates, spend, and provider-layer labels tied to the current run artifact rather than copying old example values.

Do not expose provider-side unit costs in customer-facing messages. Report Deepline spend only.
