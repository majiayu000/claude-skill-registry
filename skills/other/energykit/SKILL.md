---
name: energykit
description: "Query grid electricity forecasts and submit load events using EnergyKit to help users optimize home electricity usage. Use when building smart home apps, EV charger controls, HVAC scheduling, or energy management dashboards that guide users to use power during cleaner or cheaper grid periods."
---

# EnergyKit

Provide grid electricity forecasts to help users choose when to use electricity.
EnergyKit identifies times when there is relatively cleaner or less expensive
electricity on the grid, enabling apps to shift or reduce load accordingly.
Targets Swift 6.2 / iOS 26+.

## Contents

- [Setup](#setup)
- [Core Concepts](#core-concepts)
- [Querying Electricity Guidance](#querying-electricity-guidance)
- [Working with Guidance Values](#working-with-guidance-values)
- [Energy Venues](#energy-venues)
- [Submitting Load Events](#submitting-load-events)
- [Electricity Insights](#electricity-insights)
- [Common Mistakes](#common-mistakes)
- [Review Checklist](#review-checklist)
- [References](#references)

## Setup

### Entitlement

EnergyKit requires the `com.apple.developer.energykit` entitlement. Add it
to your app's entitlements file.

### Import

```swift
import EnergyKit
```

**Platform availability:** iOS 26+, iPadOS 26+.

## Core Concepts

EnergyKit provides two main capabilities:

1. **Electricity Guidance** -- time-weighted forecasts telling apps when
   electricity is cleaner or cheaper, so devices can shift or reduce consumption
2. **Load Events** -- telemetry from devices (EV chargers, HVAC) submitted back
   to the system to track how well the app follows guidance

### Key Types

| Type | Role |
|---|---|
| `ElectricityGuidance` | Forecast data with weighted time intervals |
| `ElectricityGuidance.Service` | Interface for obtaining guidance data |
| `ElectricityGuidance.Query` | Query specifying shift or reduce action |
| `ElectricityGuidance.Value` | A time interval with a rating (0.0-1.0) |
| `EnergyVenue` | A physical location (home) registered for energy management |
| `ElectricVehicleLoadEvent` | Load event for EV charger telemetry |
| `ElectricHVACLoadEvent` | Load event for HVAC system telemetry |
| `ElectricityInsightService` | Service for querying energy/runtime insights |
| `ElectricityInsightRecord` | Historical energy data broken down by cleanliness/tariff |
| `ElectricityInsightQuery` | Query for historical insight data |

### Suggested Actions

| Action | Use Case |
|---|---|
| `.shift` | Devices that can move consumption to a different time (EV charging) |
| `.reduce` | Devices that can lower consumption without stopping (HVAC setback) |

## Querying Electricity Guidance

Use `ElectricityGuidance.Service` to get a forecast stream for a venue.

```swift
import EnergyKit

func observeGuidance(venueID: UUID) async throws {
    let query = ElectricityGuidance.Query(suggestedAction: .shift)
    let service = ElectricityGuidance.sharedService  // Verify access pattern against Xcode 26 SDK

    let guidanceStream = service.guidance(using: query, at: venueID)

    for try await guidance in guidanceStream {
        print("Guidance token: \(guidance.guidanceToken)")
        print("Interval: \(guidance.interval)")
        print("Venue: \(guidance.energyVenueID)")

        // Check if rate plan information is available
        if guidance.options.contains(.guidanceIncorporatesRatePlan) {
            print("Rate plan data incorporated")
        }
        if guidance.options.contains(.locationHasRatePlan) {
            print("Location has a rate plan")
        }

        processGuidanceValues(guidance.values)
    }
}
```

## Working with Guidance Values

Each `ElectricityGuidance.Value` contains a time interval and a rating
from 0.0 to 1.0. Lower ratings indicate better times to use electricity.

```swift
func processGuidanceValues(_ values: [ElectricityGuidance.Value]) {
    for value in values {
        let interval = value.interval
        let rating = value.rating  // 0.0 (best) to 1.0 (worst)

        print("From \(interval.start) to \(interval.end): rating \(rating)")
    }
}

// Find the best time to charge
func bestChargingWindow(
    in values: [ElectricityGuidance.Value]
) -> ElectricityGuidance.Value? {
    values.min(by: { $0.rating < $1.rating })
}

// Find all "good" windows below a threshold
func goodWindows(
    in values: [ElectricityGuidance.Value],
    threshold: Double = 0.3
) -> [ElectricityGuidance.Value] {
    values.filter { $0.rating <= threshold }
}
```

### Displaying Guidance in SwiftUI

```swift
import SwiftUI
import EnergyKit

struct GuidanceTimelineView: View {
    let values: [ElectricityGuidance.Value]

    var body: some View {
        List(values, id: \.interval.start) { value in
            HStack {
                VStack(alignment: .leading) {
                    Text(value.interval.start, style: .time)
                    Text(value.interval.end, style: .time)
                        .foregroundStyle(.secondary)
                }
                Spacer()
                RatingIndicator(rating: value.rating)
            }
        }
    }
}

struct RatingIndicator: View {
    let rating: Double

    var color: Color {
        if rating <= 0.3 { return .green }
        if rating <= 0.6 { return .yellow }
        return .red
    }

    var label: String {
        if rating <= 0.3 { return "Good" }
        if rating <= 0.6 { return "Fair" }
        return "Avoid"
    }

    var body: some View {
        Text(label)
            .padding(.horizontal, 8)
            .padding(.vertical, 4)
            .background(color.opacity(0.2))
            .foregroundStyle(color)
            .clipShape(Capsule())
    }
}
```

## Energy Venues

An `EnergyVenue` represents a physical location registered for energy management.

```swift
// List all venues
func listVenues() async throws -> [EnergyVenue] {
    try await EnergyVenue.venues()
}

// Get a specific venue by ID
func getVenue(id: UUID) async throws -> EnergyVenue {
    try await EnergyVenue.venue(for: id)
}

// Get a venue matching a HomeKit home
func getVenueForHome(homeID: UUID) async throws -> EnergyVenue {
    try await EnergyVenue.venue(matchingHomeUniqueIdentifier: homeID)
}
```

### Venue Properties

```swift
let venue = try await EnergyVenue.venue(for: venueID)
print("Venue ID: \(venue.id)")
print("Venue name: \(venue.name)")
```

## Submitting Load Events

Report device consumption data back to the system. This helps the system
improve future guidance accuracy.

### EV Charger Load Events

```swift
func submitEVChargingEvent(
    at venue: EnergyVenue,
    guidanceToken: UUID,
    deviceID: String
) async throws {
    let session = ElectricVehicleLoadEvent.Session(
        id: UUID(),
        state: .begin,
        guidanceState: ElectricVehicleLoadEvent.Session.GuidanceState(
            wasFollowingGuidance: true,
            guidanceToken: guidanceToken
        )
    )

    let measurement = ElectricVehicleLoadEvent.ElectricalMeasurement(
        stateOfCharge: 45,
        direction: .imported,
        power: Measurement(value: 7.2, unit: .kilowatts),
        energy: Measurement(value: 0, unit: .kilowattHours)
    )

    let event = ElectricVehicleLoadEvent(
        timestamp: Date(),
        measurement: measurement,
        session: session,
        deviceID: deviceID
    )

    try await venue.submitEvents([event])
}
```

### HVAC Load Events

```swift
func submitHVACEvent(
    at venue: EnergyVenue,
    guidanceToken: UUID,
    stage: Int,
    deviceID: String
) async throws {
    let session = ElectricHVACLoadEvent.Session(
        id: UUID(),
        state: .active,
        guidanceState: ElectricHVACLoadEvent.Session.GuidanceState(
            wasFollowingGuidance: true,
            guidanceToken: guidanceToken
        )
    )

    let measurement = ElectricHVACLoadEvent.ElectricalMeasurement(stage: stage)

    let event = ElectricHVACLoadEvent(
        timestamp: Date(),
        measurement: measurement,
        session: session,
        deviceID: deviceID
    )

    try await venue.submitEvents([event])
}
```

### Session States

| State | When to Use |
|---|---|
| `.begin` | Device starts consuming electricity |
| `.active` | Device is actively consuming (periodic updates) |
| `.end` | Device stops consuming electricity |

## Electricity Insights

Query historical energy and runtime data for devices using
`ElectricityInsightService`.

```swift
func queryEnergyInsights(deviceID: String, venueID: UUID) async throws {
    let query = ElectricityInsightQuery(
        options: [.cleanliness, .tariff],
        range: DateInterval(
            start: Calendar.current.date(byAdding: .day, value: -7, to: Date())!,
            end: Date()
        ),
        granularity: .daily,
        flowDirection: .imported
    )

    let service = ElectricityInsightService.shared
    let stream = try await service.energyInsights(
        forDeviceID: deviceID, using: query, atVenue: venueID
    )

    for await record in stream {
        if let total = record.totalEnergy { print("Total: \(total)") }
        if let cleaner = record.dataByGridCleanliness?.cleaner {
            print("Cleaner: \(cleaner)")
        }
    }
}
```

Use `runtimeInsights(forDeviceID:using:atVenue:)` for runtime data instead
of energy. Granularity options: `.hourly`, `.daily`, `.weekly`, `.monthly`,
`.yearly`. See `references/energykit-patterns.md` for full insight examples.

## Common Mistakes

### DON'T: Forget the EnergyKit entitlement

Without the entitlement, all EnergyKit calls fail silently or throw errors.

```swift
// WRONG: No entitlement configured
let service = ElectricityGuidance.sharedService  // Will fail

// CORRECT: Add com.apple.developer.energykit to entitlements
// Then use the service
let service = ElectricityGuidance.sharedService
```

### DON'T: Ignore unsupported regions

EnergyKit is not available in all regions. Handle the `.unsupportedRegion`
and `.guidanceUnavailable` errors.

```swift
// WRONG: Assume guidance is always available
for try await guidance in service.guidance(using: query, at: venueID) {
    updateUI(guidance)
}

// CORRECT: Handle region-specific errors
do {
    for try await guidance in service.guidance(using: query, at: venueID) {
        updateUI(guidance)
    }
} catch let error as EnergyKitError {
    switch error {
    case .unsupportedRegion:
        showUnsupportedRegionMessage()
    case .guidanceUnavailable:
        showGuidanceUnavailableMessage()
    case .venueUnavailable:
        showNoVenueMessage()
    case .permissionDenied:
        showPermissionDeniedMessage()
    case .serviceUnavailable:
        retryLater()
    case .rateLimitExceeded:
        backOff()
    default:
        break
    }
}
```

### DON'T: Discard the guidance token

The `guidanceToken` links load events to the guidance that influenced them.
Always store and pass it through to load event submissions.

```swift
// WRONG: Ignore the guidance token
for try await guidance in guidanceStream {
    startCharging()
}

// CORRECT: Store the token for load events
for try await guidance in guidanceStream {
    let token = guidance.guidanceToken
    startCharging(followingGuidanceToken: token)
}
```

### DON'T: Submit load events without a session lifecycle

Always submit `.begin`, then `.active` updates, then `.end` events.

```swift
// WRONG: Only submit one event
let event = ElectricVehicleLoadEvent(/* state: .active */)
try await venue.submitEvents([event])

// CORRECT: Full session lifecycle
try await venue.submitEvents([beginEvent])
// ... periodic active events ...
try await venue.submitEvents([activeEvent])
// ... when done ...
try await venue.submitEvents([endEvent])
```

### DON'T: Query guidance without a venue

EnergyKit requires a venue ID. List venues first and select the appropriate one.

```swift
// WRONG: Use a hardcoded UUID
let fakeID = UUID()
service.guidance(using: query, at: fakeID)  // Will fail

// CORRECT: Discover venues first
let venues = try await EnergyVenue.venues()
guard let venue = venues.first else {
    showNoVenueSetup()
    return
}
let guidanceStream = service.guidance(using: query, at: venue.id)
```

## Review Checklist

- [ ] `com.apple.developer.energykit` entitlement added to the project
- [ ] `EnergyKitError.unsupportedRegion` handled with user-facing message
- [ ] `EnergyKitError.permissionDenied` handled gracefully
- [ ] Guidance token stored and passed to load event submissions
- [ ] Venues discovered via `EnergyVenue.venues()` before querying guidance
- [ ] Load event sessions follow `.begin` -> `.active` -> `.end` lifecycle
- [ ] `ElectricityGuidance.Value.rating` interpreted correctly (lower is better)
- [ ] `SuggestedAction` matches the device type (`.shift` for EV, `.reduce` for HVAC)
- [ ] Insight queries use appropriate granularity for the time range
- [ ] Rate limiting handled via `EnergyKitError.rateLimitExceeded`
- [ ] Service unavailability handled with retry logic

## References

- Extended patterns (full app architecture, SwiftUI dashboard): `references/energykit-patterns.md`
- [EnergyKit framework](https://sosumi.ai/documentation/energykit)
- [ElectricityGuidance](https://sosumi.ai/documentation/energykit/electricityguidance)
- [ElectricityGuidance.Service](https://sosumi.ai/documentation/energykit/electricityguidance/service)
- [ElectricityGuidance.Query](https://sosumi.ai/documentation/energykit/electricityguidance/query)
- [ElectricityGuidance.Value](https://sosumi.ai/documentation/energykit/electricityguidance/value)
- [EnergyVenue](https://sosumi.ai/documentation/energykit/energyvenue)
- [ElectricVehicleLoadEvent](https://sosumi.ai/documentation/energykit/electricvehicleloadevent)
- [ElectricHVACLoadEvent](https://sosumi.ai/documentation/energykit/electrichvacloadevent)
- [ElectricityInsightService](https://sosumi.ai/documentation/energykit/electricityinsightservice)
- [ElectricityInsightRecord](https://sosumi.ai/documentation/energykit/electricityinsightrecord)
- [ElectricityInsightQuery](https://sosumi.ai/documentation/energykit/electricityinsightquery)
- [EnergyKitError](https://sosumi.ai/documentation/energykit/energykiterror)
- [Optimizing home electricity usage](https://sosumi.ai/documentation/energykit/optimizing-home-electricity-usage)
