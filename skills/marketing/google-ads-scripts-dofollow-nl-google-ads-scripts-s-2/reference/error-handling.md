# Error handling

## Reading errors from a mutate result

```javascript
var result = AdsApp.mutate(operation);
if (!result.isSuccessful()) {
  Logger.log(result.getErrorMessages().join('; '));
}
```

`getErrorMessages()` returns a `string[]`. The first element is usually
the human-readable message; subsequent ones (rare) are nested context.

## Common error messages decoded

### "The field's contents don't match another field that represents the same data. At adGroupCriterionOperation.create.resourceName"

You supplied both `resourceName` and `adGroup` (or another redundant
parent field) and they disagree. Either:

- Drop `adGroup`, keep only `resourceName`. Recommended for criterion
  resources where you know the criterion ID (demographics, devices).
- Drop `resourceName`, keep only `adGroup`. Recommended when the server
  should allocate the criterion ID (keywords, audiences).

### "Duplicate ad group criterion" / "already exists"

The criterion already exists. In an idempotent script, treat this as a
skip:

```javascript
if (/already exists|duplicate/i.test(msg)) {
  stats.skipped++;
  return;
}
```

### "Resource name is not well-formed"

Resource name doesn't match the expected pattern. Check:

- Customer ID is stripped of dashes.
- Path uses camelCase collection names: `adGroupCriteria` not `ad_group_criteria`.
- The `~` separator is present for criterion resources.

### "Criterion type targeting is not supported for this campaign type"

Some criteria can't be applied to certain campaign types. Examples:

- Age/gender exclusions are not supported on Hotel campaigns.
- Keyword criteria can't go on Display-only campaigns.

### "Cannot set CPC bid on a campaign with portfolio bidding strategy"

The keyword/ad group belongs to a campaign using a portfolio strategy.
Set bids on the portfolio strategy, not the keyword.

### "PERMISSION_DENIED"

The script lacks permission. For MCC scripts, ensure the manager account
has access to the child account. For Script auth, ensure the script was
authorized by a user with appropriate access.

### "Quota exceeded"

You've burned your operations-per-day or operations-per-script quota.
Reduce frequency, batch with `mutateAll()`, or split the workload.

### "RPC failed"

Transient. Retry with backoff:

```javascript
function withRetry(fn, attempts) {
  attempts = attempts || 3;
  var lastErr;
  for (var i = 0; i < attempts; i++) {
    try { return fn(); }
    catch (e) {
      lastErr = e;
      Utilities.sleep(1000 * Math.pow(2, i));
    }
  }
  throw lastErr;
}
```

### "The function 'X' could not be found"

In MCC `executeInParallel('X', 'Y')`: `X` is not a top-level function.
The runtime resolves by string lookup against the global scope. Move
the function to top level (not nested inside another function).

### "Return value must be a String"

In MCC `executeInParallel`: the per-account function returned a non-string.
Wrap in `JSON.stringify(...)`.

## Per-operation error reporting

For `mutateAll()` with `partialFailure: true`, each result corresponds to
the operation at the same index:

```javascript
var results = AdsApp.mutateAll(operations, { partialFailure: true });
results.forEach(function (r, i) {
  if (!r.isSuccessful()) {
    Logger.log('Op ' + i + ': ' + r.getErrorMessages().join('; '));
  }
});
```

## Try/catch for non-mutate operations

Wrapped operations (`adGroup.pause()`, `keyword.bidding().setCpc()`) throw
instead of returning a result object. Use try/catch:

```javascript
try {
  keyword.bidding().setCpc(1.5);
} catch (e) {
  Logger.log('Failed to set CPC on keyword ' + keyword.getId() + ': ' + e);
}
```

## Surface errors loudly

For scheduled scripts, terminal logs are easy to miss. End the script
with a structured summary and email if anything went wrong:

```javascript
Logger.log('--- Summary ---');
Logger.log(JSON.stringify(stats, null, 2));

if (stats.errors > 0) {
  MailApp.sendEmail({
    to: 'marketing@example.com',
    subject: '[Ads Script] ' + stats.errors + ' errors',
    htmlBody: '<pre>' + JSON.stringify(stats, null, 2) + '</pre>',
  });
}
```
