# GAQL: Google Ads Query Language

`AdsApp.search(query)` runs raw GAQL against the current account. It is the
authoritative way to read data when:

- The SDK has no wrapper for what you need (asset groups, asset signals,
  recommendations, change history, audiences with details, etc.).
- You need a field the selector doesn't expose.
- You want efficient bulk reads (join-like behaviour via segments).
- You are pre-checking state before a `mutate()` call.

## Basic shape

```sql
SELECT
  campaign.id,
  campaign.name,
  campaign.status,
  metrics.cost_micros,
  metrics.clicks
FROM campaign
WHERE
  campaign.status = 'ENABLED'
  AND campaign.advertising_channel_type = 'SEARCH'
  AND segments.date DURING LAST_30_DAYS
ORDER BY metrics.cost_micros DESC
LIMIT 100
```

In Google Ads Scripts:

```javascript
var rows = AdsApp.search(query);
while (rows.hasNext()) {
  var row = rows.next();
  Logger.log(row.campaign.name + ' = ' + row.metrics.costMicros);
}
```

Field naming:

- IN the query string: `snake_case` (`campaign.advertising_channel_type`).
- IN the returned object: `camelCase` (`row.campaign.advertisingChannelType`).
- Resource enums are bare strings in the WHERE clause: `'ENABLED'`, `'SEARCH'`.

## Common FROM resources

| Resource | What it contains |
|----------|------------------|
| `campaign` | Campaign-level data and stats |
| `ad_group` | Ad group-level data and stats |
| `ad_group_ad` | Ad group + ad join |
| `ad_group_criterion` | Keywords, audiences, demographics, etc. on ad groups |
| `campaign_criterion` | Targeting on campaigns (locations, languages, negatives) |
| `keyword_view` | Keyword-focused report |
| `search_term_view` | What people actually searched for |
| `asset` | All assets (images, headlines, etc.) |
| `asset_group` | PMax / Demand Gen asset groups |
| `asset_group_signal` | Audience signals on PMax asset groups |
| `customer` | Account-level info |
| `change_event` | Recent changes (90 days) |
| `recommendation` | Active recommendations |
| `geographic_view`, `gender_view`, `age_range_view`, `parental_status_view` | Demographic performance |

## WHERE operators

- `=`, `!=`, `<`, `<=`, `>`, `>=`
- `IN (...)`, `NOT IN (...)`
- `LIKE`, `NOT LIKE` (use `%` wildcards)
- `CONTAINS ANY (...)`, `CONTAINS ALL (...)`, `CONTAINS NONE (...)` for repeated fields
- `IS NULL`, `IS NOT NULL`
- `BETWEEN x AND y`
- `DURING <date_range>` for `segments.date`

## Date ranges

```sql
WHERE segments.date DURING LAST_30_DAYS
WHERE segments.date BETWEEN '2026-01-01' AND '2026-01-31'
WHERE segments.date >= '2026-01-01'
```

Supported `DURING` presets include `TODAY`, `YESTERDAY`, `LAST_7_DAYS`,
`LAST_14_DAYS`, `LAST_30_DAYS`, `THIS_MONTH`, `LAST_MONTH`,
`LAST_BUSINESS_WEEK`, `THIS_QUARTER`, `LAST_QUARTER`, `THIS_YEAR`,
`LAST_YEAR`, `ALL_TIME`.

## Segments

Including any `segments.*` field expands rows by that dimension.

```sql
SELECT campaign.name, segments.device, metrics.clicks
FROM campaign
WHERE segments.date DURING LAST_7_DAYS
```

Common segments:

- `segments.date`
- `segments.device` (MOBILE, DESKTOP, TABLET, CONNECTED_TV, OTHER)
- `segments.day_of_week`
- `segments.hour`
- `segments.search_term_match_type`
- `segments.ad_network_type`
- `segments.click_type`
- `segments.conversion_action`, `segments.conversion_action_name`

WARNING: every segment multiplies row count. Filter aggressively.

## Resource names and IDs

Some fields return full resource names:

```sql
SELECT ad_group_criterion.resource_name, ad_group_criterion.criterion_id
FROM ad_group_criterion
WHERE ad_group.id = 1234567890
```

Resource name format: `customers/{cid}/adGroupCriteria/{adGroupId}~{criterionId}`.
The `~` separates parent ID from criterion ID. Use this for `mutate()`
payloads.

## Micros

Money fields are in micros: `metrics.cost_micros = 1230000` means €1.23.
Divide by 1,000,000 (or use `metrics.average_cost`/`metrics.average_cpc` if
you want unit values directly).

## Patterns

### Pre-check before mutate (idempotency)

```javascript
function hasNegativeAge(adGroupId, ageType) {
  var query =
    "SELECT ad_group_criterion.criterion_id " +
    "FROM ad_group_criterion " +
    "WHERE ad_group_criterion.type = 'AGE_RANGE' " +
    "AND ad_group_criterion.negative = TRUE " +
    "AND ad_group_criterion.age_range.type = '" + ageType + "' " +
    "AND ad_group.id = " + adGroupId;
  return AdsApp.search(query).hasNext();
}
```

### Bulk fetch into a map

```javascript
var query = "SELECT ad_group.id, ad_group.name FROM ad_group " +
            "WHERE ad_group.status = 'ENABLED'";
var rows = AdsApp.search(query);
var byId = {};
while (rows.hasNext()) {
  var r = rows.next();
  byId[r.adGroup.id] = r.adGroup.name;
}
```

### Search term mining

```sql
SELECT
  search_term_view.search_term,
  metrics.clicks,
  metrics.cost_micros,
  metrics.conversions
FROM search_term_view
WHERE segments.date DURING LAST_30_DAYS
  AND metrics.clicks >= 5
  AND metrics.conversions = 0
ORDER BY metrics.cost_micros DESC
LIMIT 200
```

### Change history (recent edits)

```sql
SELECT
  change_event.change_date_time,
  change_event.user_email,
  change_event.resource_change_operation,
  change_event.changed_fields
FROM change_event
WHERE change_event.change_date_time DURING LAST_7_DAYS
ORDER BY change_event.change_date_time DESC
LIMIT 100
```

## Validate-only

```javascript
var rows = AdsApp.search(query, { validateOnly: true });
```

Returns no rows but throws on syntax errors. Useful when developing.

## Common errors

- `INVALID_VALUE_WITH_DURING_OPERATOR` — `DURING` only works with
  `segments.date`. Use `>=` / `BETWEEN` for other date fields.
- `RESOURCE_NAME_NOT_AVAILABLE` — querying a relationship that does not
  exist on this resource.
- `INCOMPATIBLE_FIELDS_IN_SELECT_CLAUSE` — mixing fields from incompatible
  resources. Split into two queries.
- `REQUIRED_FIELD_MISSING` — querying ad_group fields from a resource
  that does not surface them; add the segment or change the FROM.

## Reference

Full field catalog (per API version):
https://developers.google.com/google-ads/api/fields/v22/overview
