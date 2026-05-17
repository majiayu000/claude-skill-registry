---
name: google-ads-scripts
description: >
  Write, debug, and ship Google Ads Scripts (AdsApp / AdsManagerApp) correctly
  the first time. Covers selectors, GAQL search, the AdsApp.mutate() escape
  hatch for resources the SDK does not wrap, demographic exclusions, MCC
  parallel execution, preview-mode gotchas, idempotency patterns, and
  common error messages. Use when the user says "Google Ads Script",
  "AdsApp", "AdsManagerApp", "ads script", "AdWordsApp", "automate Google
  Ads", "mutate ad group criterion", or pastes JavaScript that imports
  AdsApp. NOT for auditing Google Ads accounts — for that see ads-google.
---

# Google Ads Scripts

You are helping the user write or modify a Google Ads Script. These run inside
Google's sandboxed JavaScript runtime and are accessed via the Ads UI under
Tools and settings -> Bulk actions -> Scripts.

Read this whole file before writing code. Most "this didn't work" loops come
from skipping a section that warned about it.

## What Google Ads Scripts is (and is not)

- A JavaScript (ES2017+ subset) runtime that exposes `AdsApp` (account-level)
  and `AdsManagerApp` (MCC-level) globals.
- NOT the Google Ads API. It is a thin, opinionated wrapper around it. Some
  resources have first-class wrappers (`AdsApp.campaigns()`,
  `AdsApp.keywords()`). Many do not. When the wrapper is missing, you fall
  back to `AdsApp.search()` (read) and `AdsApp.mutate()` (write) which speak
  the raw API.
- Runtime limit: 30 minutes per single-account run, 60 minutes per MCC run.
- Preview mode does not persist changes. Some operations behave weirdly in
  preview (see `reference/gotchas.md`).
- API version used by `AdsApp.search()` / `AdsApp.mutate()` follows the
  current Google Ads API version. Field names in GAQL are snake_case;
  field names in `mutate()` payloads are camelCase.

## Before you write code: decide the shape

Ask yourself:

1. **Single account or MCC?** If MCC, use `AdsManagerApp.accounts()...executeInParallel()`.
   See `reference/mcc-scripts.md`.
2. **Read-only or mutating?** Read-only scripts can rely entirely on
   `AdsApp.search()` (GAQL). Mutating scripts use either the wrappers
   (`adGroup.pause()`, `keyword.bidding().setCpc(1.5)`) or `AdsApp.mutate()`.
3. **Is the resource wrapped by the SDK?** Campaigns, ad groups, keywords,
   ads, labels, audiences-on-ad-group are wrapped. Demographic criteria
   (age, gender, parental status, income) are mostly NOT wrapped outside
   of video campaigns. Asset groups, asset group signals, listing groups,
   experiment arms, recommendations: not wrapped — use mutate.
4. **Idempotency.** If the script will be scheduled, it MUST be safe to run
   repeatedly. Use labels (`reference/idempotency.md`) or pre-check via
   `AdsApp.search()`.

## The selector pattern

Every read in the wrapped API uses the selector pattern: build, filter,
order, limit, then call `.get()` for an iterator.

```javascript
var iterator = AdsApp.campaigns()
  .withCondition("Status = ENABLED")
  .withCondition("CampaignName CONTAINS_IGNORE_CASE 'channable'")
  .orderBy("Cost DESC")
  .forDateRange("LAST_30_DAYS")
  .withLimit(50)
  .get();

while (iterator.hasNext()) {
  var campaign = iterator.next();
  // ...
}
```

Cheatsheet of conditions and field names lives in `reference/selectors.md`.
Note: selector field names (e.g. `CampaignName`, `Status`) are NOT the same
as GAQL field names (`campaign.name`, `campaign.status`).

## The mutate escape hatch

When the SDK has no wrapper, use `AdsApp.mutate()` (single) or
`AdsApp.mutateAll()` (batch). The payload is a JSON `MutateOperation` with
camelCase field names matching the Google Ads API REST schema.

```javascript
var result = AdsApp.mutate({
  adGroupCriterionOperation: {
    create: {
      resourceName: 'customers/' + customerId + '/adGroupCriteria/' + adGroupId + '~503006',
      negative: true,
      ageRange: { type: 'AGE_RANGE_65_UP' },
    },
  },
});

if (!result.isSuccessful()) {
  Logger.log(result.getErrorMessages().join('; '));
}
```

CRITICAL gotcha: when creating an `adGroupCriterion` for a demographic, pass
the full `resourceName` (which encodes the criterion ID) and DO NOT also pass
`adGroup`. The API computes one from the other and rejects mismatches with:

> The field's contents don't match another field that represents the same
> data. At adGroupCriterionOperation.create.resourceName

The `~` in resource names is a literal separator: `customers/{cid}/adGroupCriteria/{adGroupId}~{criterionId}`.

Full reference: `reference/mutate-escape-hatch.md`.

## Reading with GAQL

`AdsApp.search()` runs raw GAQL against the current account.

```javascript
var rows = AdsApp.search(
  "SELECT ad_group.id, ad_group.name, ad_group_criterion.age_range.type " +
  "FROM ad_group_criterion " +
  "WHERE ad_group_criterion.type = 'AGE_RANGE' " +
  "AND ad_group_criterion.negative = TRUE"
);
while (rows.hasNext()) {
  var row = rows.next();
  Logger.log(row.adGroup.name + ': ' + row.adGroupCriterion.ageRange.type);
}
```

Field names in GAQL are snake_case in the query string but the returned
objects use camelCase. Resource is plural for the query (`ad_group_criterion`)
but field paths nest naturally.

Full reference: `reference/gaql-cheatsheet.md`.

## Well-known criterion IDs

Some criterion IDs are global constants (same across every account). You
NEED these when building resource names for `mutate()`:

| Type | ID |
|------|----|
| AGE_RANGE_18_24 | 503001 |
| AGE_RANGE_25_34 | 503002 |
| AGE_RANGE_35_44 | 503003 |
| AGE_RANGE_45_54 | 503004 |
| AGE_RANGE_55_64 | 503005 |
| AGE_RANGE_65_UP | 503006 |
| AGE_RANGE_UNDETERMINED | 503999 |
| GENDER_MALE | 10 |
| GENDER_FEMALE | 11 |
| GENDER_UNDETERMINED | 20 |
| PARENTAL_STATUS_PARENT | 300 |
| PARENTAL_STATUS_NOT_A_PARENT | 301 |
| PARENTAL_STATUS_UNDETERMINED | 302 |

Income brackets, device types, and more in `reference/criterion-ids.md`.

## Idempotency: label everything you touch

For any script that will run on a schedule, mark processed entities so the
next run skips them. Labels are the easiest mechanism for campaigns, ad
groups, ads, and keywords. Pattern:

1. `ensureLabel(name)` — create if missing.
2. Selector excludes labeled entities, or check `entity.labels()` per item.
3. After mutating an entity, `entity.applyLabel(name)`.

In preview mode `AdsApp.createLabel()` does not persist, so a subsequent
`applyLabel()` in the same preview run throws. Wrap `applyLabel()` in
try/catch and log a soft warning. On a live run the label is created and
applied normally.

Full pattern: `reference/idempotency.md`.

## Templates

Start from `templates/` and modify. They include the boilerplate every
script needs (customer ID handling, structured stats logging, error
handling, summary at the end):

- `templates/single-account.js` — most scripts start here
- `templates/mcc-parallel.js` — run across many accounts under an MCC
- `templates/mutate-with-search.js` — the read-then-mutate pattern with
  idempotency via search

## Worked examples

`examples/` contains scripts the user has actually shipped:

- `examples/exclude-age-demographic.js` — exclude an age range from every
  ad group in matching campaigns, with label-based idempotency and the
  mutate escape hatch.

## Workflow rules when writing for the user

1. **Pick the right tool.** Wrapped operation? Use the wrapper. Not wrapped?
   `mutate()` with a hand-built payload. Reading? Prefer `AdsApp.search()`
   over `report()` (the latter is deprecated).
2. **Run a probe before bulk writes.** When unsure of the payload shape,
   write a one-off "diagnostic" version that picks one entity, dumps its
   current state via `search()`, and tries 2–3 candidate payloads with
   try/catch. Then write the production version from what worked. This is
   way faster than guessing.
3. **Handle preview mode.** Don't crash the script when an apply-only
   operation (label creation, mutate side effects) fails in preview.
4. **Log structured stats.** Maintain a `stats` object with named counters,
   print a single summary block at the end. Don't make the user grep
   100-line logs.
5. **Use `withCondition("Status = ENABLED")`** unless the user explicitly
   wants paused/removed entities. By default they almost certainly only
   care about live stuff.
6. **No em dashes in any output.** This is a user preference.
7. **Never claim success without verifying.** If you can run the script
   yourself, do so. If you can't, say "ready to run, do a preview first".

## Reference files (read on demand)

- `reference/selectors.md` — selector conditions, field names, operators,
  date ranges, ordering, limits.
- `reference/gaql-cheatsheet.md` — GAQL query language: SELECT, FROM,
  WHERE, segments, common resources, field naming.
- `reference/mutate-escape-hatch.md` — every common mutate operation with
  verified payload shape. Includes the demographic-exclusion case.
- `reference/criterion-ids.md` — well-known criterion IDs you must hard-code.
- `reference/mcc-scripts.md` — AdsManagerApp, executeInParallel, accounts
  selector, return value protocol.
- `reference/idempotency.md` — label patterns, search-before-mutate, GAQL
  pre-checks.
- `reference/gotchas.md` — preview mode, runtime limits, immutable fields,
  bid modifier ranges, criterion auto-creation, timezone quirks.
- `reference/error-handling.md` — interpreting common API errors:
  PERMISSION_DENIED, DUPLICATE_AD_GROUP_CRITERION, RESOURCE_NAME_MALFORMED,
  CRITERION_TYPE_TARGETING_NOT_SUPPORTED, the "field contents don't match"
  error and its causes.

External canonical references the user can pull up:

- Google Ads Scripts overview: https://developers.google.com/google-ads/scripts
- AdsApp reference: https://developers.google.com/google-ads/scripts/docs/reference/adsapp
- Mutate concept: https://developers.google.com/google-ads/scripts/docs/concepts/mutate
- Google Ads API field reference (for GAQL + mutate payloads):
  https://developers.google.com/google-ads/api/fields/v22/overview
- "Try this" interactive query builder:
  https://developers.google.com/google-ads/api/docs/query/overview
