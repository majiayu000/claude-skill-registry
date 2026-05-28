---
name: healthkit-code-review
description: Reviews HealthKit code for authorization patterns, query usage, background delivery, and data type handling. Use when reviewing code with import HealthKit, HKHealthStore, HKSampleQuery, HKObserverQuery, or HKQuantityType.
---

# HealthKit Code Review

## Quick Reference

| Issue Type | Reference |
|------------|-----------|
| HKHealthStore, permissions, status checks, privacy | [references/authorization.md](references/authorization.md) |
| HKQuery types, predicates, anchored queries, statistics | [references/queries.md](references/queries.md) |
| Background delivery, observer queries, completion handlers | [references/background.md](references/background.md) |
| HKQuantityType, HKCategoryType, workouts, units | [references/data-types.md](references/data-types.md) |

## Review Checklist

- [ ] `HKHealthStore.isHealthDataAvailable()` called before any HealthKit operations
- [ ] Authorization requested only for needed data types (minimal permissions)
- [ ] `requestAuthorization` completion handler not misinterpreted as permission granted
- [ ] No attempt to determine read permission status (privacy by design)
- [ ] Query results dispatched to main thread for UI updates
- [ ] `HKObjectQueryNoLimit` used only with bounded predicates
- [ ] `HKStatisticsQuery` used for aggregations instead of manual summing
- [ ] Observer query `completionHandler()` always called (use `defer`)
- [ ] Background delivery registered in `application(_:didFinishLaunchingWithOptions:)`
- [ ] Background delivery entitlement added (iOS 15+)
- [ ] Correct units used for quantity types (e.g., `count/min` for heart rate)
- [ ] Long-running queries stored as properties and stopped in `deinit`

## When to Load References

- Reviewing authorization/permissions flow -> authorization.md
- Reviewing HKSampleQuery, HKAnchoredObjectQuery, or predicates -> queries.md
- Reviewing HKObserverQuery or `enableBackgroundDelivery` -> background.md
- Reviewing HKQuantityType, HKCategoryType, or HKWorkout -> data-types.md

## Review gates

Run in order. **Do not state a finding in a later step until the pass condition for the current step is satisfied** (each pass condition is answerable from the codebase under review).

1. **Scope** — **Pass:** Name the file path(s) and types/symbols using `HealthKit`, `HKHealthStore`, or `HK*` APIs (or state clearly that the diff touches none).
2. **Availability and store** — **Pass:** Cite the call site of `isHealthDataAvailable()` before HealthKit use, or document why omission is acceptable for the scoped code; cite where `HKHealthStore` is created or injected.
3. **Authorization semantics** — **Pass:** For each `requestAuthorization` / `getRequestStatusForAuthorization`, cite handler branches per [references/authorization.md](references/authorization.md) (e.g. success does not prove read access); do not infer read permission from `authorizationStatus` alone.
4. **Queries and limits** — **Pass:** For each query, cite predicate + limit (`HKObjectQueryNoLimit` only with a bounded predicate); for totals/aggregates, cite `HKStatisticsQuery` / collection vs manual summing per [references/queries.md](references/queries.md).
5. **Observers and background** — **Pass:** If `HKObserverQuery` or `enableBackgroundDelivery` appears, cite where the observer is started/stopped and where background delivery is registered; cite entitlements/Info.plist or flag missing config per [references/background.md](references/background.md). If absent, **Pass:** one line “no observer/background in scope.”
6. **Threading and lifecycle** — **Pass:** Cite main-queue (or documented pattern) for UI updates from query callbacks; cite retention/`stop()`/`deinit` for long-running queries per checklist above.

## Review Questions

1. Is `isHealthDataAvailable()` checked before creating HKHealthStore?
2. Does the code gracefully handle denied permissions (empty results)?
3. Are observer query completion handlers called in all code paths?
4. Is work in background handlers minimal (~15 second limit)?
5. Are HKQueryAnchors persisted per sample type (not shared)?
