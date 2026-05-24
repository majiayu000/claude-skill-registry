# Gotchas

Things that have burned someone in production. Read this before writing.

## Preview mode is partially simulated

- Mutates are not persisted, but the operation IS validated against the
  API. So you can use preview to validate payload shape without applying.
- `AdsApp.createLabel()` does not persist in preview, so any subsequent
  `applyLabel()` throws. Wrap in try/catch.
- Time spent in preview counts against the 30-minute runtime limit.
- Logger output is shown even when changes don't apply, so use it.

## Runtime limits

| Limit | Value |
|-------|-------|
| Single-account script | 30 min |
| MCC script total | 60 min |
| Concurrent parallel accounts | 50 |
| Total entities per script | 250,000 |
| `mutateAll()` batch size | 1,000 ops per call |
| Operations per day per account | varies by account |

Scripts hitting the runtime cap usually iterate when they should batch.
Prefer `mutateAll()` over `mutate()` in a loop, and prefer single GAQL
reads over per-entity selectors.

## AdsApp.campaigns() omits Shopping/Video/PMax

`AdsApp.campaigns()` returns only Search and Display campaigns. To touch
every type:

```javascript
var entry = [
  AdsApp.campaigns(),
  AdsApp.shoppingCampaigns(),
  AdsApp.videoCampaigns(),
  AdsApp.performanceMaxCampaigns(),
];
```

## Bid modifier ranges

- Devices: -100% (exclude) to +900%
- Demographics (age, gender, parental status, household income): **-90%** to +900%
  (cannot exclude via modifier; use a negative criterion instead)
- Audiences: -90% to +900%
- Locations: -90% to +900%

If you try to set a -100% modifier on demographics, the API rejects it.

## Demographic criteria are auto-enabled

When an ad group is created, all age ranges, genders, parental statuses,
and income ranges are implicitly targeted (positive). To "exclude" you
ADD a negative criterion for the unwanted value. You do NOT remove a
positive one — they don't exist as explicit positive rows.

This is why `SELECT ad_group_criterion.criterion_id FROM ad_group_criterion
WHERE ad_group_criterion.type = 'AGE_RANGE' AND ad_group.id = X` returns 0
rows for a freshly-created ad group, even though all age ranges are
effectively targeted.

## The 'negative' field is immutable on AdGroupCriterion

You cannot flip a positive criterion to negative via update. To switch:
remove, then re-create as negative.

## Customer IDs come with dashes

`AdsApp.currentAccount().getCustomerId()` returns `"123-456-7890"`. Resource
names need it stripped:

```javascript
var customerId = AdsApp.currentAccount().getCustomerId().replace(/-/g, '');
```

## Money is in micros (sometimes)

- GAQL `metrics.cost_micros` and `cpc_bid_micros`: micros (divide by 1,000,000).
- Selector `Cost`, `AverageCpc`: account currency units (already divided).
- `mutate()` payloads with `cpcBidMicros`: micros.
- Wrapped APIs like `keyword.bidding().setCpc(1.5)`: account currency.

When in doubt: check whether the field name ends in `Micros`.

## Selectors are LAZY

`.withCondition()` calls are stacked. Nothing hits the API until `.get()`.
Modifying a selector after `.get()` returns the iterator does not affect
that iterator.

## Selectors can return stale data inside a long-running loop

If your script mutates ad groups while iterating campaigns, child selectors
on already-iterated campaigns will reflect the new state — but the
campaign iterator itself was materialized at `.get()` time. Usually fine,
but be careful with cascading mutations.

## report() is deprecated

`AdsApp.report(query)` still works but Google has steered users to
`AdsApp.search(query)`. New code should use `search()`. They take the
same GAQL query.

## Date format inconsistency

- `forDateRange()` selector: `"YYYYMMDD"` strings or objects, OR named
  preset strings.
- GAQL `BETWEEN`: `'YYYY-MM-DD'` strings.
- GAQL `DURING`: bare preset identifiers (`DURING LAST_30_DAYS`, no quotes).

## URL fetching is restricted

`UrlFetchApp.fetch()` works but only against allowlisted hosts (any HTTPS
endpoint, plus some Google services). If you need to call your own API,
make sure it's HTTPS and reachable from Google's IP ranges.

## Spreadsheet integration is the easiest persistence

For storing state across runs, append to a Google Sheet via
`SpreadsheetApp`. Scripts have implicit access to sheets owned by the
running user.

## "Field's contents don't match" on mutate

You included both a redundant parent reference (e.g. `adGroup`) AND a
`resourceName` that doesn't agree. Pick one. For criterion-style
resources, `resourceName` alone is usually cleanest.

## Operation count quota

Each `mutate()` or `mutateAll()` call counts against your daily operation
quota. Heavy scripts can hit limits. If you see quota errors, batch with
`mutateAll()` and consider running less often.

## Logger.log() truncation

Lines over ~5KB get truncated. For dumping large structures, prefer
appending to a sheet or splitting into multiple lines.

## Email notifications

Use `MailApp.sendEmail({...})` for alerts. No setup needed; the email
comes from the user's Google account.

```javascript
MailApp.sendEmail({
  to: 'marketing@example.com',
  subject: 'Channable exclusion script — ' + stats.errors + ' errors',
  htmlBody: '<pre>' + JSON.stringify(stats, null, 2) + '</pre>',
});
```
