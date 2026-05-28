# MCC (manager account) scripts

When a script runs at the MCC level, the global is `AdsManagerApp` instead
of `AdsApp`. The MCC entry point selects child accounts; inside each
account's execution context you have access to the normal `AdsApp` global.

## Selecting accounts

```javascript
var accounts = AdsManagerApp.accounts()
  .withCondition("Status = ENABLED")
  .withCondition("LabelNames CONTAINS 'Run age-exclusion'")
  .withLimit(50)
  .get();
```

Common conditions:

- `Status` (ENABLED, CANCELED, SUSPENDED, CLOSED)
- `Name`
- `CustomerId`
- `LabelNames`
- `ManagerCustomer` (boolean — exclude sub-MCCs)

## executeInParallel — the right way

`AdsManagerApp.accounts().executeInParallel(functionName, callbackName)`
runs `functionName(account)` against every account in the selector,
**in parallel** (up to 50 concurrent), then calls `callbackName(results)`
once with the aggregated results.

```javascript
function main() {
  AdsManagerApp.accounts()
    .withCondition("Status = ENABLED")
    .executeInParallel('processAccount', 'finalize');
}

function processAccount() {
  // AdsApp is bound to the account this invocation runs against.
  var customerId = AdsApp.currentAccount().getCustomerId();
  var count = 0;
  // ... do work, return a serializable summary as a STRING ...
  return JSON.stringify({ customerId: customerId, processed: count });
}

function finalize(results) {
  // results is an Array<ExecutionResult>
  for (var i = 0; i < results.length; i++) {
    var r = results[i];
    if (r.getStatus() === 'OK') {
      Logger.log(r.getCustomerId() + ': ' + r.getReturnValue());
    } else {
      Logger.log(r.getCustomerId() + ' FAILED: ' + r.getError());
    }
  }
}
```

## Critical rules

1. The function passed to `executeInParallel` MUST be a top-level function,
   not anonymous. The runtime resolves it by name.
2. The return value MUST be a **string** (typically `JSON.stringify(obj)`).
   Returning an object directly throws.
3. The callback is optional but recommended. Use it to aggregate.
4. Per-account runtime limit: still 30 minutes.
5. Total MCC runtime limit: 60 minutes.
6. Maximum 50 accounts running in parallel at once. The selector can
   contain more — they queue.
7. Inside the per-account function you must NOT reference `AdsManagerApp`.

## Without executeInParallel (sequential)

For small MCCs or when ordering matters:

```javascript
function main() {
  var iter = AdsManagerApp.accounts().withCondition("Status = ENABLED").get();
  while (iter.hasNext()) {
    var account = iter.next();
    AdsManagerApp.select(account);   // switch context
    // Now AdsApp targets this account.
    processAccount();
  }
}
```

Sequential is simpler to debug but slow. Use `executeInParallel` for
anything beyond a handful of accounts.

## Labeling accounts (idempotency at MCC level)

```javascript
function main() {
  var accounts = AdsManagerApp.accounts()
    .withCondition("LabelNames CONTAINS_NONE ['Channable-exclusion-applied']")
    .get();
  // ... only unprocessed accounts ...
}

function processAccount() {
  // ... do work ...
  AdsManagerApp.currentAccount().applyLabel('Channable-exclusion-applied');
  return JSON.stringify({ ok: true });
}
```

MCC-level labels exist separately from account-level labels and must be
created via `AdsManagerApp.createLabel(name)` before use.

## Cross-account reads (no select)

For reporting that aggregates across accounts WITHOUT mutating anything,
you can still use `executeInParallel` to fan out read-only work, then
aggregate in the callback.

## Common errors

- "The function 'X' could not be found" — the parallel function isn't a
  top-level function in the script.
- "Return value must be a String" — wrap the return in `JSON.stringify`.
- "An error occurred running script for customer ID X" — wrap the
  per-account body in try/catch and return the error message as part of
  the JSON so it surfaces in the callback.

## Reference

- AdsManagerApp reference:
  https://developers.google.com/google-ads/scripts/docs/reference/adsmanagerapp
- executeInParallel concept:
  https://developers.google.com/google-ads/scripts/docs/features/parallel
