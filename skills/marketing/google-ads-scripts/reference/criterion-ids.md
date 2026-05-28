# Well-known criterion IDs

Some Google Ads criteria have global, account-independent IDs. You need
these when constructing `resourceName` strings for `AdsApp.mutate()`,
because the ID is part of the resource name and the API will reject
mismatches.

Format: `customers/{cid}/adGroupCriteria/{adGroupId}~{criterionId}`

## Age ranges

| Enum | ID |
|------|----|
| AGE_RANGE_18_24 | 503001 |
| AGE_RANGE_25_34 | 503002 |
| AGE_RANGE_35_44 | 503003 |
| AGE_RANGE_45_54 | 503004 |
| AGE_RANGE_55_64 | 503005 |
| AGE_RANGE_65_UP | 503006 |
| AGE_RANGE_UNDETERMINED | 503999 |

## Gender

| Enum | ID |
|------|----|
| GENDER_MALE | 10 |
| GENDER_FEMALE | 11 |
| GENDER_UNDETERMINED | 20 |

## Parental status

| Enum | ID |
|------|----|
| PARENTAL_STATUS_PARENT | 300 |
| PARENTAL_STATUS_NOT_A_PARENT | 301 |
| PARENTAL_STATUS_UNDETERMINED | 302 |

## Income range (US/CA only)

| Enum | ID |
|------|----|
| INCOME_RANGE_0_50 | 503100 |
| INCOME_RANGE_50_60 | 503101 |
| INCOME_RANGE_60_70 | 503102 |
| INCOME_RANGE_70_80 | 503103 |
| INCOME_RANGE_80_90 | 503104 |
| INCOME_RANGE_90_UP | 503105 |
| INCOME_RANGE_UNDETERMINED | 503999 |

## Device

Used in campaign criteria (bid modifiers):

| Enum | ID |
|------|----|
| MOBILE | 30001 |
| TABLET | 30002 |
| DESKTOP | 30000 |
| CONNECTED_TV | 30004 |
| OTHER | 30003 |

## How to discover others

Most other criterion types (keywords, audiences, placements, locations)
do NOT have well-known IDs. The server assigns an ID when you create them.
For those, pass the parent resource name in the operation and omit
`resourceName`. The server returns the allocated resource name on the
result object via `result.getResourceName()`.

Geo target IDs (for `location` criteria) are constants. Look them up at:
https://developers.google.com/google-ads/api/data/geotargets

Example: United States = `geoTargetConstants/2840`, Netherlands =
`geoTargetConstants/2528`, United Kingdom = `geoTargetConstants/2826`.

## Verification trick

If you're unsure of an ID, query an existing criterion and inspect:

```javascript
var rows = AdsApp.search(
  "SELECT ad_group_criterion.criterion_id, ad_group_criterion.age_range.type " +
  "FROM ad_group_criterion " +
  "WHERE ad_group_criterion.type = 'AGE_RANGE' " +
  "LIMIT 10"
);
while (rows.hasNext()) {
  var r = rows.next();
  Logger.log(r.adGroupCriterion.ageRange.type + ' = ' + r.adGroupCriterion.criterionId);
}
```
