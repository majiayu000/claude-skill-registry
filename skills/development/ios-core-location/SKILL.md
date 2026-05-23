---
name: ios-core-location
description: "Use for Core Location implementation decisions: authorization strategy, monitoring mode, accuracy selection, geofencing, and background location lifecycle."
license: MIT
compatibility: iOS 17+, iPadOS 17+, macOS 14+, watchOS 10+
metadata:
  version: "1.0.0"
  last-updated: "2026-01-03"
---

# Core Location Patterns

Implementation discipline for location features: correct authorization, battery-aware tracking, and reliable background behavior.

## Related Skills

- [references/api-reference.md](./references/api-reference.md) - API reference

## Anti-Patterns (and cost)

### 1) Premature Always authorization

```swift
// Wrong
manager.requestAlwaysAuthorization()

// Right
CLServiceSession(authorization: .whenInUse)
// upgrade to .always only when user starts background feature
```

- Cost: fast code, poor adoption (high denial rates)
- Rule: start minimal, escalate with contextual user intent

### 2) Continuous updates for geofencing

```swift
// Wrong: polling location to emulate geofencing
for try await update in CLLocationUpdate.liveUpdates() { ... }

// Right: system geofencing
let monitor = await CLMonitor("Geofences")
await monitor.add(CLMonitor.CircularGeographicCondition(center: target, radius: 100), identifier: "Target")
for try await event in monitor.events { ... }
```

- Cost: major battery waste
- Rule: use `CLMonitor` for entry/exit semantics

### 3) Ignoring stationary behavior

```swift
for try await update in CLLocationUpdate.liveUpdates() {
    if let location = update.location { processLocation(location) }
    if update.isStationary { saveLastKnownLocation(update.location) }
}
```

- Cost: unnecessary processing while stationary
- Rule: respect stationary/pause behavior

### 4) No graceful denial path

```swift
for try await update in CLLocationUpdate.liveUpdates() {
    if update.authorizationDenied { showManualLocationPicker(); break }
    if update.authorizationDeniedGlobally { showSystemLocationDisabledMessage(); break }
    if let location = update.location { processLocation(location) }
}
```

- Cost: silent failure + broken UX
- Rule: always branch explicit denial states

### 5) Wrong accuracy for use case

```swift
// Wrong for weather app
CLLocationUpdate.liveUpdates(.automotiveNavigation)

// Better by intent
CLLocationUpdate.liveUpdates(.default) // weather/store-finder
CLLocationUpdate.liveUpdates(.fitness) // activity
CLLocationUpdate.liveUpdates(.automotiveNavigation) // turn-by-turn
```

| Use case | Config | Typical accuracy | Battery |
|---|---|---|---|
| Navigation | `.automotiveNavigation` | ~5m | Highest |
| Fitness | `.fitness` | ~10m | High |
| Store finder | `.default` | ~10-100m | Medium |
| Weather | `.default` | city-level | Low |

### 6) Not stopping updates

```swift
private var locationTask: Task<Void, Error>?

func startTracking() {
    locationTask = Task {
        for try await update in CLLocationUpdate.liveUpdates() {
            if Task.isCancelled { break }
            updateMap(update.location)
        }
    }
}

func stopTracking() {
    locationTask?.cancel()
    locationTask = nil
}
```

- Cost: battery drain + persistent location indicator
- Rule: explicit start/stop lifecycle

### 7) Ignoring `CLServiceSession` (iOS 18+)

```swift
let session = CLServiceSession(authorization: .whenInUse)
let navSession = CLServiceSession(
    authorization: .whenInUse,
    fullAccuracyPurposeKey: "Navigation"
)

for try await diag in session.diagnostics {
    if diag.authorizationDenied { handleDenial() }
}
```

- Cost: manual state machine complexity
- Rule: declare needs; observe diagnostics

## Decision Trees

### Authorization

1. Need background location?
- no -> `.whenInUse`
- yes -> start `.whenInUse`, upgrade `.always` at first background feature action

2. Need precise location?
- always -> full accuracy purpose key
- sometimes -> temporary full-accuracy session only during relevant feature

### Monitoring mode

1. Track continuous position?
- use `CLLocationUpdate.liveUpdates()` with matching `LiveConfiguration`

2. Entry/exit geofence?
- use `CLMonitor.CircularGeographicCondition` (20-condition cap)

3. Beacon proximity?
- use `CLMonitor.BeaconIdentityCondition` with needed granularity

4. Low-power broad movement only?
- use significant-change monitoring (legacy API)

### Accuracy selection

- pick lowest accuracy that still satisfies feature requirements
- high speed driving -> `.automotiveNavigation`
- walking/cycling -> `.otherNavigation`
- general/stationary -> `.default`

Higher accuracy always increases energy cost.

## Pressure Scenarios

### "Request Always on first launch"

Response:
- upfront Always requests commonly increase denial
- use staged ask: `.whenInUse` first, upgrade on feature trigger
- reference CLServiceSession guidance for contextual asks

### "Background location not working"

Checklist:
1. background capability present
2. `CLBackgroundActivitySession` retained
3. session started in foreground
4. relaunch recovery restores session + update stream

### "Geofence unreliable in production"

Checklist:
1. <=20 conditions
2. radius >=100m
3. always await `monitor.events`
4. recreate monitor on app launch
5. inspect `lastEvent` and `accuracyLimited`

## Pre-Release Checklist

### Info.plist
- [ ] `NSLocationWhenInUseUsageDescription`
- [ ] `NSLocationAlwaysAndWhenInUseUsageDescription` (if applicable)
- [ ] `NSLocationDefaultAccuracyReduced` (if acceptable)
- [ ] `NSLocationTemporaryUsageDescriptionDictionary` (if requesting temporary full accuracy)
- [ ] `UIBackgroundModes` includes `location` (if background tracking)

### Authorization and UX
- [ ] Start with minimal auth
- [ ] Upgrade only at feature trigger
- [ ] Denial and global-disable paths handled
- [ ] Reduced-accuracy path tested

### Runtime lifecycle
- [ ] Appropriate `LiveConfiguration`
- [ ] Stationary behavior handled
- [ ] Tasks canceled when inactive
- [ ] Geofencing not implemented via continuous polling

### Testing
- [ ] Deny/re-enable flow tested
- [ ] Background/foreground transitions tested
- [ ] Termination + relaunch recovery tested

## Background Location Checklist

### Setup
- [ ] Capability enabled: Location updates
- [ ] `CLBackgroundActivitySession` retained strongly
- [ ] Created in foreground
- [ ] Relaunch path rehydrates tracking state

### Lifecycle
- [ ] Persist "tracking active" state
- [ ] Restore session and update stream on launch
- [ ] Reinitialize `CLMonitor` with same name

## Version Guidance

| Feature | Minimum iOS | Note |
|---|---:|---|
| `CLLocationUpdate` | 17 | AsyncSequence API |
| `CLMonitor` | 17 | Region/beacon monitoring |
| `CLBackgroundActivitySession` | 17 | Background with indicator |
| `CLServiceSession` | 18 | Declarative authorization |

- iOS 14-16: use `CLLocationManager` delegate style.
- iOS 17+: prefer `CLLocationUpdate` and `CLMonitor`.
- iOS 18+: add `CLServiceSession`.

## Resources

- WWDC: 2023-10180, 2023-10147, 2024-10212
- Docs: `/corelocation`, `/corelocation/clmonitor`, `/corelocation/cllocationupdate`, `/corelocation/clservicesession`
- Reference: [references/api-reference.md](./references/api-reference.md)
