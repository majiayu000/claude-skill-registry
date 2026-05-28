# Idempotency patterns

Any script that runs on a schedule MUST be safe to run repeatedly. There
are three common patterns. Pick one (or combine) based on the operation.

## Pattern 1: Label after processing (best for entity-level work)

Apply a marker label to entities you've already processed, then exclude
them from subsequent runs.

```javascript
var LABEL_NAME = 'My-script-processed';

function main() {
  ensureLabel(LABEL_NAME, 'Touched by my-script.js');

  var iter = AdsApp.campaigns()
    .withCondition("Status = ENABLED")
    .withCondition("LabelNames CONTAINS_NONE ['" + LABEL_NAME + "']")
    .get();

  while (iter.hasNext()) {
    var campaign = iter.next();
    doWork(campaign);
    try {
      campaign.applyLabel(LABEL_NAME);
    } catch (e) {
      // Preview mode: createLabel didn't persist. Harmless.
      Logger.log('Label apply skipped: ' + e);
    }
  }
}

function ensureLabel(name, description) {
  if (AdsApp.labels().withCondition("Name = '" + name + "'").get().hasNext()) {
    return;
  }
  AdsApp.createLabel(name, description);
}
```

Pros:
- Cheap: the selector skips processed entities entirely.
- Visible in the UI — useful for humans.
- Works at every level (campaign, ad group, ad, keyword).

Cons:
- `LabelNames CONTAINS_NONE` is not supported on every selector type
  (notably PMax asset groups, some legacy resources). For those, iterate
  `entity.labels()` manually.
- New entities created after the script ran will not be labeled. If the
  user wants those caught too, this pattern is wrong — use Pattern 2.

## Pattern 2: Pre-check via GAQL (best when target state is queryable)

Before mutating, query whether the desired state already exists. Mutate
only if not. This catches newly-added entities automatically.

```javascript
function hasAgeExclusion(adGroupId, ageType) {
  var query =
    "SELECT ad_group_criterion.criterion_id " +
    "FROM ad_group_criterion " +
    "WHERE ad_group_criterion.type = 'AGE_RANGE' " +
    "AND ad_group_criterion.negative = TRUE " +
    "AND ad_group_criterion.age_range.type = '" + ageType + "' " +
    "AND ad_group.id = " + adGroupId;
  return AdsApp.search(query).hasNext();
}

if (!hasAgeExclusion(adGroupId, 'AGE_RANGE_65_UP')) {
  AdsApp.mutate({ /* ... */ });
}
```

Pros:
- Self-healing: works on freshly-created entities too.
- No state to manage.

Cons:
- Extra read per entity. Fine for hundreds, slow for tens of thousands.
- For that scale, fetch ALL exclusions in one GAQL query upfront and
  build a `Set<adGroupId>` to check against.

## Pattern 3: Catch the duplicate error (cheapest, no pre-check)

Many mutate operations return a typed error when the resource already
exists. Treat that as a success-equivalent skip.

```javascript
var result = AdsApp.mutate(operation);
if (!result.isSuccessful()) {
  var msg = result.getErrorMessages().join('; ');
  if (/already exists|duplicate/i.test(msg)) {
    stats.skipped++;
  } else {
    stats.errors++;
    Logger.log(msg);
  }
}
```

Pros:
- One round-trip per entity, no pre-check.
- Trivially self-healing.

Cons:
- Server still does the work of rejecting. Slightly heavier than a
  selector pre-filter.
- Some operations don't surface a clean "already exists" — you might
  need to combine with Pattern 2.

## Combining patterns

For maximum robustness on a script the user will schedule daily:

1. Use Pattern 1 (label) to skip entire campaigns after first processing.
2. Inside each campaign, use Pattern 3 (catch duplicate) on the per-ad-group
   mutate so newly-added ad groups in a "processed" campaign still get
   handled the next time someone re-runs without the label.
3. Reserve Pattern 2 for cases where Patterns 1 and 3 don't cover.

## Preview-mode safety

In preview mode `AdsApp.createLabel()` does not persist. The label-creation
log line appears in the preview output, but a subsequent
`AdsApp.labels()` query or `campaign.applyLabel(name)` will throw because
the label doesn't actually exist server-side.

ALWAYS wrap `applyLabel()` in try/catch when running for the first time.
After the first live (apply) run, the label exists and preview runs work
correctly.

```javascript
try {
  campaign.applyLabel(LABEL_NAME);
} catch (e) {
  Logger.log('Could not apply label (likely preview): ' + e);
}
```
