# Selectors

Every wrapped read in Google Ads Scripts uses the selector pattern. Build a
selector, chain conditions, optionally order/limit/forDateRange, then call
`.get()` for an iterator.

## Anatomy

```javascript
var iter = AdsApp.campaigns()       // entry point — what kind of entity?
  .withCondition("...")             // filter (chainable, AND-combined)
  .withCondition("...")
  .forDateRange("LAST_30_DAYS")     // affects stats columns referenced in conditions
  .orderBy("Cost DESC")
  .withLimit(50)
  .withIds([12345, 67890])          // direct ID lookup (alternative to conditions)
  .get();
```

Selectors are immutable: each chained method returns a NEW selector. You can
reuse the same selector to .get() again later.

## Entry points (selectors)

Account-level:

- `AdsApp.campaigns()` — Search + Display campaigns (NOT Shopping/Video/PMax)
- `AdsApp.shoppingCampaigns()`
- `AdsApp.videoCampaigns()`
- `AdsApp.performanceMaxCampaigns()`
- `AdsApp.adGroups()`
- `AdsApp.shoppingAdGroups()`
- `AdsApp.videoAdGroups()`
- `AdsApp.ads()` — text and responsive search ads
- `AdsApp.shoppingAds()`
- `AdsApp.videoAds()`
- `AdsApp.keywords()`
- `AdsApp.negativeKeywords()` (ad group level)
- `AdsApp.campaignNegativeKeywords()`
- `AdsApp.sharedNegativeKeywordLists()`
- `AdsApp.labels()`
- `AdsApp.userLists()` — remarketing/customer-match lists
- `AdsApp.budgets()`
- `AdsApp.biddingStrategies()` — portfolio bid strategies
- `AdsApp.extensions().sitelinks()` etc. (deprecated path — prefer assets)
- `AdsApp.assets()` and `AdsApp.assetGroups()`
- `AdsApp.experiments()`

Off a parent entity:

- `campaign.adGroups()`, `campaign.ads()`, `campaign.keywords()`
- `adGroup.ads()`, `adGroup.keywords()`, `adGroup.audiences()`
- `adGroup.devices()` (returns the four device platforms)
- `adGroup.targeting()` — wrapper over targetable criteria
- `campaign.targeting()` — same at campaign level
- `entity.labels()` — labels applied to the entity

## Condition operators

`withCondition(string)` accepts a SQL-like string. Operators differ from GAQL:

| Operator | Use | Example |
|----------|-----|---------|
| `=` | exact match | `Status = ENABLED` |
| `!=` | not equal | `Status != REMOVED` |
| `<` `<=` `>` `>=` | numeric/date | `Cost > 100` |
| `IN [...]` | one of | `Status IN [ENABLED, PAUSED]` |
| `NOT IN [...]` | none of | `Status NOT IN [REMOVED]` |
| `CONTAINS` | substring (case-sensitive) | `CampaignName CONTAINS 'Brand'` |
| `CONTAINS_IGNORE_CASE` | substring (case-insensitive) | `CampaignName CONTAINS_IGNORE_CASE 'channable'` |
| `DOES_NOT_CONTAIN` | inverse | `Name DOES_NOT_CONTAIN 'test'` |
| `STARTS_WITH` / `STARTS_WITH_IGNORE_CASE` | prefix | |
| `CONTAINS_ANY [...]` / `CONTAINS_ALL [...]` / `CONTAINS_NONE [...]` | for arrays like LabelNames | `LabelNames CONTAINS_NONE ['Processed']` |

String values are single-quoted. Enums (Status, etc.) are bare identifiers.

## Common selector fields

These are the selector field names (NOT the GAQL field names).

Campaigns (`AdsApp.campaigns()`):

- `Id`, `Name`, `Status` (ENABLED, PAUSED, REMOVED)
- `ServingStatus`
- `AdvertisingChannelType`
- `LabelNames`
- `Cost`, `Impressions`, `Clicks`, `Ctr`, `Conversions`, `ConversionValue`,
  `AverageCpc`, `CostPerConversion` (need `forDateRange`)
- `BiddingStrategyType`
- `BudgetId`

Ad groups (`AdsApp.adGroups()`):

- `Id`, `Name`, `Status`, `CampaignName`, `CampaignStatus`, `CampaignId`
- Stats fields same as campaigns

Keywords (`AdsApp.keywords()`):

- `Id`, `Text`, `MatchType` (BROAD, PHRASE, EXACT), `Status`
- `AdGroupName`, `AdGroupStatus`, `CampaignName`, `CampaignStatus`
- `QualityScore`, `MaxCpc`, `FirstPageCpc`, `TopOfPageCpc`
- Stats fields

Ads (`AdsApp.ads()`):

- `Id`, `Status`, `Type`, `AdGroupName`, `AdGroupStatus`, `CampaignName`
- `LabelNames`

When in doubt, the canonical field list lives in the
[AdsApp reference](https://developers.google.com/google-ads/scripts/docs/reference/adsapp)
under the relevant Selector class.

## Date ranges

`forDateRange()` accepts:

- A preset: `'TODAY'`, `'YESTERDAY'`, `'LAST_7_DAYS'`, `'LAST_14_DAYS'`,
  `'LAST_30_DAYS'`, `'THIS_MONTH'`, `'LAST_MONTH'`, `'ALL_TIME'`, plus a
  handful more.
- Two strings: `forDateRange('20260101', '20260131')` (YYYYMMDD).
- Two objects: `forDateRange({year: 2026, month: 1, day: 1}, {year: 2026, month: 1, day: 31})`.

Stats columns referenced in `withCondition` require a date range. If you do
not call `forDateRange`, you can still filter on non-stats fields like
`Status` and `Name`.

## Ordering and limits

```javascript
.orderBy("Cost DESC")
.orderBy("CampaignName ASC")  // chain multiple
.withLimit(100)
```

`withLimit` is applied AFTER `orderBy`. Useful for "top N" patterns.

## .get() vs iteration

`.get()` returns an iterator with `.hasNext()`, `.next()`, `.totalNumEntities()`.

```javascript
var iter = AdsApp.keywords().withCondition("Status = ENABLED").get();
Logger.log('Found ' + iter.totalNumEntities() + ' enabled keywords');
while (iter.hasNext()) {
  var kw = iter.next();
  // ...
}
```

## Gotchas

- `AdsApp.campaigns()` returns ONLY Search and Display campaigns. To process
  every campaign type, iterate over `AdsApp.campaigns()`,
  `AdsApp.shoppingCampaigns()`, `AdsApp.videoCampaigns()`, and
  `AdsApp.performanceMaxCampaigns()` separately.
- `LabelNames CONTAINS_NONE` works only on selectors that surface label
  metadata. If your selector type does not support it, filter manually by
  iterating `entity.labels()`.
- The selector field name and the GAQL field name are different. `Status`
  in a selector becomes `campaign.status` in GAQL.
- Stats fields are scoped to the date range. `Cost = 0` over LAST_30_DAYS
  is NOT the same as never having any cost.
