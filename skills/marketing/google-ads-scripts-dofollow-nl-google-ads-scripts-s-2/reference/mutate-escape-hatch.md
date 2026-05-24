# AdsApp.mutate() — the escape hatch

When the wrapped API does not expose the operation you need, fall back to
`AdsApp.mutate(operation)` for a single write or `AdsApp.mutateAll(operations)`
for a batch. These speak the raw Google Ads API.

## Anatomy of a MutateOperation

```javascript
var operation = {
  // Exactly one of these keys, named after the resource:
  adGroupCriterionOperation: {
    // Exactly one of create / update / remove
    create: {
      // resource fields in camelCase, matching the REST schema
      resourceName: 'customers/.../adGroupCriteria/...~...',
      negative: true,
      ageRange: { type: 'AGE_RANGE_65_UP' },
    },
  },
};

var result = AdsApp.mutate(operation);

if (result.isSuccessful()) {
  Logger.log('OK: ' + result.getResourceName());
} else {
  Logger.log('FAILED: ' + result.getErrorMessages().join('; '));
}
```

The operation key matches the API's mutate method name. Common ones:

| Key | Resource |
|-----|----------|
| `campaignOperation` | Campaign |
| `campaignBudgetOperation` | CampaignBudget |
| `adGroupOperation` | AdGroup |
| `adGroupCriterionOperation` | AdGroupCriterion (keywords, demographics, audiences) |
| `campaignCriterionOperation` | CampaignCriterion (locations, languages, campaign negatives) |
| `adGroupAdOperation` | AdGroupAd (ads) |
| `assetOperation` | Asset |
| `assetGroupOperation` | AssetGroup (PMax / Demand Gen) |
| `assetGroupAssetOperation` | AssetGroupAsset |
| `assetGroupSignalOperation` | AssetGroupSignal |
| `customerLabelOperation` | CustomerLabel |
| `labelOperation` | Label |
| `userListOperation` | UserList |

For `update`, also include `updateMask` (FieldMask string of comma-separated
field paths) at the top level of the operation:

```javascript
{
  adGroupOperation: {
    update: {
      resourceName: 'customers/.../adGroups/...',
      name: 'New name',
      cpcBidMicros: 1500000,
    },
    updateMask: 'name,cpcBidMicros',
  },
}
```

For `remove`, pass the resource name as the string value:

```javascript
{
  adGroupCriterionOperation: {
    remove: 'customers/.../adGroupCriteria/...~...',
  },
}
```

## Resource name format

`customers/{customerId}/{resourceCollection}/{parentId}~{childId}` for
criterion-like resources. Examples:

- AdGroupCriterion: `customers/123/adGroupCriteria/456~789` where 456 is
  the ad group ID and 789 is the criterion ID.
- CampaignCriterion: `customers/123/campaignCriteria/456~789`.
- AssetGroupAsset: `customers/123/assetGroupAssets/456~789~HEADLINE`
  (criterion ID is replaced by the field type for asset group assets).

Get the customer ID stripped of dashes:

```javascript
var customerId = AdsApp.currentAccount().getCustomerId().replace(/-/g, '');
```

## The "field contents don't match" gotcha

When creating an AdGroupCriterion, you can pass either:

- Just `resourceName` (which encodes both ad group and criterion ID), OR
- Just `adGroup` (parent resource name; server allocates a criterion ID).

For demographic criteria you MUST use the first form because the criterion
ID is a well-known constant (see `criterion-ids.md`). Passing both can
work, but if the IDs in `resourceName` and `adGroup` do not align you get:

> The field's contents don't match another field that represents the same
> data. At adGroupCriterionOperation.create.resourceName

Just use `resourceName` alone for the cleanest result.

## Verified payloads

### Exclude age range on an ad group

```javascript
{
  adGroupCriterionOperation: {
    create: {
      resourceName: 'customers/' + customerId + '/adGroupCriteria/' + adGroupId + '~503006',
      negative: true,
      ageRange: { type: 'AGE_RANGE_65_UP' },
    },
  },
}
```

(`503006` is the AGE_RANGE_65_UP criterion ID. See `criterion-ids.md`.)

### Exclude gender on an ad group

```javascript
{
  adGroupCriterionOperation: {
    create: {
      resourceName: 'customers/' + customerId + '/adGroupCriteria/' + adGroupId + '~10',
      negative: true,
      gender: { type: 'MALE' },
    },
  },
}
```

### Exclude an audience on a campaign

```javascript
{
  campaignCriterionOperation: {
    create: {
      campaign: 'customers/' + customerId + '/campaigns/' + campaignId,
      negative: true,
      userList: {
        userList: 'customers/' + customerId + '/userLists/' + userListId,
      },
    },
  },
}
```

Audience criteria do not have well-known IDs — let the server allocate.

### Add a campaign-level location exclusion

```javascript
{
  campaignCriterionOperation: {
    create: {
      campaign: 'customers/' + customerId + '/campaigns/' + campaignId,
      negative: true,
      location: { geoTargetConstant: 'geoTargetConstants/2840' }, // US
    },
  },
}
```

### Pause a keyword (update with field mask)

If wrapping is available, prefer `keyword.pause()`. But for the raw form:

```javascript
{
  adGroupCriterionOperation: {
    update: {
      resourceName: 'customers/' + customerId + '/adGroupCriteria/' + adGroupId + '~' + criterionId,
      status: 'PAUSED',
    },
    updateMask: 'status',
  },
}
```

### Add an asset group signal (PMax audience signal)

```javascript
{
  assetGroupSignalOperation: {
    create: {
      assetGroup: 'customers/' + customerId + '/assetGroups/' + assetGroupId,
      audience: {
        audience: 'customers/' + customerId + '/audiences/' + audienceId,
      },
    },
  },
}
```

## Batch mutates

```javascript
var operations = adGroupIds.map(function (id) {
  return {
    adGroupCriterionOperation: {
      create: {
        resourceName: 'customers/' + customerId + '/adGroupCriteria/' + id + '~503006',
        negative: true,
        ageRange: { type: 'AGE_RANGE_65_UP' },
      },
    },
  };
});

var results = AdsApp.mutateAll(operations, { partialFailure: true });
results.forEach(function (r, i) {
  if (!r.isSuccessful()) {
    Logger.log('AdGroup ' + adGroupIds[i] + ': ' + r.getErrorMessages().join('; '));
  }
});
```

`partialFailure: true` lets successes through even if some entries fail.
With `partialFailure: false` (default), one error aborts the whole batch.

## Error-handling pattern

```javascript
function safeMutate(operation, onAlreadyExists) {
  try {
    var result = AdsApp.mutate(operation);
    if (result.isSuccessful()) return { ok: true };
    var msg = result.getErrorMessages().join('; ');
    if (onAlreadyExists && /already exists|duplicate/i.test(msg)) {
      onAlreadyExists();
      return { ok: false, skipped: true };
    }
    return { ok: false, message: msg };
  } catch (e) {
    return { ok: false, message: String(e) };
  }
}
```

## When to NOT use mutate()

- The SDK wrapper supports it cleanly. `keyword.bidding().setCpc(1.5)` is
  shorter and more readable than the equivalent mutate.
- You only need to read data. Use `AdsApp.search()` instead.
- You are doing 1000+ similar operations: prefer `mutateAll()` with chunks
  of up to 1000 operations per call.

## Validate-only

```javascript
AdsApp.mutate(operation, { validateOnly: true });
```

Runs the operation through the API's validator without applying. Useful
for shape-debugging without spending operations.

## Reference

- Mutate concept: https://developers.google.com/google-ads/scripts/docs/concepts/mutate
- Resource field catalog: https://developers.google.com/google-ads/api/fields/v22/overview
- Mutate best practices (API): https://developers.google.com/google-ads/api/docs/mutating/best-practices
