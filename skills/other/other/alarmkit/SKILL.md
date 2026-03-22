---
name: alarmkit
description: "Implement AlarmKit alarms and countdown timers for iOS and iPadOS with Lock Screen, Dynamic Island, and Apple Watch system UI. Covers AlarmManager scheduling, AlarmAttributes and AlarmPresentation, AlarmButton stop and snooze actions, authorization, state observation, and Live Activity integration. Use when building wake-up alarms, countdown timers, or alarm-style alerts that need Apple's system alarm experience."
---

# AlarmKit

Schedule prominent alarms and countdown timers that surface on the Lock Screen,
Dynamic Island, and Apple Watch. AlarmKit requires iOS 26+ / iPadOS 26+. Alarms override
Focus and Silent mode automatically.

AlarmKit builds on Live Activities -- every alarm creates a system-managed Live
Activity with templated UI. You configure the presentation via `AlarmAttributes`
and `AlarmPresentation` rather than building custom widget views.

See `references/alarmkit-patterns.md` for complete code patterns including
authorization, scheduling, countdown timers, snooze handling, and widget setup.

```swift
import AlarmKit
```

## Contents

- [Workflow](#workflow)
- [Authorization](#authorization)
- [Alarm vs Timer Decision](#alarm-vs-timer-decision)
- [Scheduling Alarms](#scheduling-alarms)
- [Countdown Timers](#countdown-timers)
- [Alarm States](#alarm-states)
- [AlarmAttributes and AlarmPresentation](#alarmattributes-and-alarmpresentation)
- [AlarmButton](#alarmbutton)
- [Live Activity Integration](#live-activity-integration)
- [Common Mistakes](#common-mistakes)
- [Review Checklist](#review-checklist)
- [References](#references)

## Workflow

### 1. Create a new alarm or timer

1. Add `NSAlarmKitUsageDescription` to Info.plist with a user-facing string.
2. Request authorization with `AlarmManager.shared.requestAuthorization()`.
3. Configure `AlarmPresentation` (alert, countdown, paused states).
4. Create `AlarmAttributes` with the presentation, optional metadata, and tint color.
5. Build an `AlarmManager.AlarmConfiguration` (.alarm or .timer).
6. Schedule with `AlarmManager.shared.schedule(id:configuration:)`.
7. Observe state changes via `alarmManager.alarmUpdates`.
8. If using countdown, add a widget extension target for non-alerting Live Activity UI.

### 2. Review existing alarm code

Run through the Review Checklist at the end of this document.

## Authorization

AlarmKit requires explicit user authorization. Without it, alarms silently
fail to schedule. Request early (e.g., at onboarding) or let AlarmKit prompt
automatically on first schedule.

```swift
let manager = AlarmManager.shared

// Request authorization explicitly
let state = try await manager.requestAuthorization()
guard state == .authorized else { return }

// Check current state synchronously
let current = manager.authorizationState // .authorized, .denied, .notDetermined

// Observe authorization changes
for await state in manager.authorizationUpdates {
    switch state {
    case .authorized: print("Alarms enabled")
    case .denied:     print("Alarms disabled")
    case .notDetermined: break
    @unknown default: break
    }
}
```

## Alarm vs Timer Decision

| Feature | Alarm (`.alarm`) | Timer (`.timer`) |
|---|---|---|
| Fires at | Specific time (schedule) | After duration elapses |
| Countdown UI | Optional | Always shown |
| Recurring | Yes (weekly days) | No |
| Use case | Wake-up, scheduled reminders | Cooking, workout intervals |

Use `.alarm(schedule:...)` when firing at a clock time. Use `.timer(duration:...)`
when firing after a duration from now.

## Scheduling Alarms

### Alarm.Schedule

Alarms use `Alarm.Schedule` to define when they fire.

```swift
// Fixed: fire at an exact Date (one-time only)
let fixed: Alarm.Schedule = .fixed(myDate)

// Relative one-time: fire at 7:30 AM in device time zone, no repeat
let oneTime: Alarm.Schedule = .relative(.init(
    time: .init(hour: 7, minute: 30),
    repeats: .never
))

// Recurring: fire at 6:00 AM on weekdays
let weekday: Alarm.Schedule = .relative(.init(
    time: .init(hour: 6, minute: 0),
    repeats: .weekly([.monday, .tuesday, .wednesday, .thursday, .friday])
))
```

### Schedule and Configure

```swift
let id = UUID()

let configuration = AlarmManager.AlarmConfiguration.alarm(
    schedule: .relative(.init(
        time: .init(hour: 7, minute: 0),
        repeats: .never
    )),
    attributes: attributes,
    stopIntent: StopAlarmIntent(alarmID: id.uuidString),
    secondaryIntent: SnoozeIntent(alarmID: id.uuidString),
    sound: .default
)

let alarm = try await AlarmManager.shared.schedule(
    id: id,
    configuration: configuration
)
```

### Alarm State Transitions

```text
cancel(id:)
    |
scheduled --> countdown --> alerting
    |             |             |
    |         pause(id:)    stop(id:) / countdown(id:)
    |             |
    |         paused ----> countdown (via resume(id:))
    |
cancel(id:) removes from system entirely
```

- `cancel(id:)` -- remove the alarm completely (any state)
- `pause(id:)` -- pause a counting-down alarm
- `resume(id:)` -- resume a paused alarm
- `stop(id:)` -- stop an alerting alarm
- `countdown(id:)` -- restart countdown from alerting state (snooze)

## Countdown Timers

Timers fire after a duration and always show a countdown UI. Use
`Alarm.CountdownDuration` to control pre-alert and post-alert durations.

```swift
// Simple timer: 5-minute countdown, no snooze
let timerConfig = AlarmManager.AlarmConfiguration.timer(
    duration: 300,
    attributes: attributes,
    stopIntent: StopTimerIntent(timerID: id.uuidString),
    sound: .default
)

let alarm = try await AlarmManager.shared.schedule(
    id: UUID(),
    configuration: timerConfig
)
```

### CountdownDuration

`Alarm.CountdownDuration` controls the visible countdown phases:

- `preAlert` -- seconds to count down before the alarm fires (the main countdown)
- `postAlert` -- seconds for a repeat/snooze countdown after the alarm fires

```swift
let countdown = Alarm.CountdownDuration(
    preAlert: 600,   // 10-minute countdown before alert
    postAlert: 300   // 5-minute snooze countdown if user taps Repeat
)

let config = AlarmManager.AlarmConfiguration(
    countdownDuration: countdown,
    schedule: .relative(.init(
        time: .init(hour: 8, minute: 0),
        repeats: .never
    )),
    attributes: attributes,
    stopIntent: stopIntent,
    secondaryIntent: snoozeIntent,
    sound: .default
)
```

## Alarm States

Each `Alarm` has a `state` property reflecting its current lifecycle position.

| State | Meaning |
|---|---|
| `.scheduled` | Waiting to fire (alarm mode) or waiting to start countdown |
| `.countdown` | Actively counting down (timer or pre-alert phase) |
| `.paused` | Countdown paused by user or app |
| `.alerting` | Alarm is firing -- sound playing, UI prominent |

### Observing State Changes

```swift
let manager = AlarmManager.shared

// Get all current alarms
let alarms = manager.alarms

// Observe changes as an async sequence
for await updatedAlarms in manager.alarmUpdates {
    for alarm in updatedAlarms {
        switch alarm.state {
        case .scheduled:  print("\(alarm.id) waiting")
        case .countdown:  print("\(alarm.id) counting down")
        case .paused:     print("\(alarm.id) paused")
        case .alerting:   print("\(alarm.id) alerting!")
        @unknown default: break
        }
    }
}
```

An alarm that disappears from `alarmUpdates` has been cancelled or fully stopped
and is no longer tracked by the system.

## AlarmAttributes and AlarmPresentation

`AlarmAttributes` conforms to `ActivityAttributes` and defines the static
data for the alarm's Live Activity. It is generic over a `Metadata` type
conforming to `AlarmMetadata`.

### AlarmPresentation

Defines the UI content for each alarm state. The system renders a templated
Live Activity using this data -- you do not build custom SwiftUI views for the
alarm itself.

```swift
// Alert state (required) -- shown when alarm is firing
let alert = AlarmPresentation.Alert(
    title: "Wake Up",
    secondaryButton: AlarmButton(
        text: "Snooze",
        textColor: .white,
        systemImageName: "bell.slash"
    ),
    secondaryButtonBehavior: .countdown  // snooze restarts countdown
)

// Countdown state (optional) -- shown during pre-alert countdown
let countdown = AlarmPresentation.Countdown(
    title: "Morning Alarm",
    pauseButton: AlarmButton(
        text: "Pause",
        textColor: .orange,
        systemImageName: "pause.fill"
    )
)

// Paused state (optional) -- shown when countdown is paused
let paused = AlarmPresentation.Paused(
    title: "Paused",
    resumeButton: AlarmButton(
        text: "Resume",
        textColor: .green,
        systemImageName: "play.fill"
    )
)

let presentation = AlarmPresentation(
    alert: alert,
    countdown: countdown,
    paused: paused
)
```

### AlarmAttributes

```swift
struct CookingMetadata: AlarmMetadata {
    var recipeName: String
    var stepNumber: Int
}

let attributes = AlarmAttributes(
    presentation: presentation,
    metadata: CookingMetadata(recipeName: "Pasta", stepNumber: 3),
    tintColor: .blue
)
```

### AlarmPresentationState

`AlarmPresentationState` is the system-managed `ContentState` of the alarm
Live Activity. It contains the alarm ID and a `Mode` enum:

- `.alert(Alert)` -- alarm is firing, includes the scheduled time
- `.countdown(Countdown)` -- actively counting down, includes fire date and durations
- `.paused(Paused)` -- countdown paused, includes elapsed and total durations

The widget extension reads `AlarmPresentationState.mode` to decide which UI to
render in the Dynamic Island and Lock Screen for non-alerting states.

## AlarmButton

`AlarmButton` defines the appearance of action buttons in the alarm UI.

```swift
let stopButton = AlarmButton(
    text: "Stop",
    textColor: .red,
    systemImageName: "stop.fill"
)

let snoozeButton = AlarmButton(
    text: "Snooze",
    textColor: .white,
    systemImageName: "bell.slash"
)
```

### Secondary Button Behavior

The secondary button on the alert UI has two behaviors:

| Behavior | Effect |
|---|---|
| `.countdown` | Restarts a countdown using `postAlert` duration (snooze) |
| `.custom` | Triggers the `secondaryIntent` (e.g., open app) |

## Live Activity Integration

AlarmKit alarms automatically appear as Live Activities on the Lock Screen
and Dynamic Island on iPhone, and in the Smart Stack on Apple Watch. The
system manages the alerting UI. For countdown and paused states, add a
widget extension that reads `AlarmAttributes` and `AlarmPresentationState`.

A widget extension is **required** if your alarm uses countdown presentation.
Without it, the system may dismiss alarms unexpectedly.

```swift
struct AlarmWidgetBundle: WidgetBundle {
    var body: some Widget {
        AlarmActivityWidget()
    }
}

struct AlarmActivityWidget: Widget {
    var body: some WidgetConfiguration {
        ActivityConfiguration(for: AlarmAttributes<CookingMetadata>.self) { context in
            // Lock Screen presentation for countdown/paused states
            AlarmLockScreenView(context: context)
        } dynamicIsland: { context in
            DynamicIsland {
                DynamicIslandExpandedRegion(.center) {
                    Text(context.attributes.presentation.alert.title)
                }
                DynamicIslandExpandedRegion(.bottom) {
                    // Show countdown or paused info based on mode
                    AlarmExpandedView(state: context.state)
                }
            } compactLeading: {
                Image(systemName: "alarm.fill")
            } compactTrailing: {
                AlarmCompactTrailing(state: context.state)
            } minimal: {
                Image(systemName: "alarm.fill")
            }
        }
    }
}
```

## Common Mistakes

**DON'T:** Forget `NSAlarmKitUsageDescription` in Info.plist.
**DO:** Add a descriptive usage string. Without it, AlarmKit cannot schedule alarms at all.

**DON'T:** Skip authorization and assume alarms will schedule.
**DO:** Call `requestAuthorization()` early and handle `.denied` gracefully.

**DON'T:** Use `.timer` when you need a recurring schedule.
**DO:** Use `.alarm` with `.weekly([...])` for recurring alarms. Timers are one-shot.

**DON'T:** Omit the widget extension when using countdown presentation.
**DO:** Add a widget extension target. AlarmKit requires it for countdown/paused Live Activity UI.
**Why:** Without a widget extension, the system may dismiss alarms before they alert.

**DON'T:** Ignore `alarmUpdates` and track alarm state manually.
**DO:** Observe `alarmManager.alarmUpdates` to stay synchronized with the system.
**Why:** Alarm state can change while your app is backgrounded.

**DON'T:** Forget to provide a `stopIntent` -- it cannot be nil in practice.
**DO:** Always provide a `LiveActivityIntent` for stop so the button performs cleanup.

**DON'T:** Store large data in `AlarmMetadata`. It is serialized with the Live Activity.
**DO:** Keep metadata lightweight. Store large data in your app and reference by ID.

**DON'T:** Use deprecated `stopButton` parameter on `AlarmPresentation.Alert`.
**DO:** Use the current `init(title:secondaryButton:secondaryButtonBehavior:)` initializer.

## Review Checklist

- [ ] `NSAlarmKitUsageDescription` present in Info.plist with non-empty string
- [ ] Authorization requested and `.denied` state handled in UI
- [ ] `AlarmPresentation` covers all relevant states (alert, countdown, paused)
- [ ] Widget extension target added if countdown presentation is used
- [ ] `AlarmAttributes` metadata type conforms to `AlarmMetadata`
- [ ] Alarm ID stored for later cancel/pause/resume/stop operations
- [ ] `alarmUpdates` async sequence observed to track state changes
- [ ] `stopIntent` and `secondaryIntent` are valid `LiveActivityIntent` implementations
- [ ] `postAlert` duration set on `CountdownDuration` if snooze (`.countdown` behavior) is used
- [ ] Tint color set on `AlarmAttributes` to differentiate from other apps
- [ ] Error handling for `AlarmManager.AlarmError.maximumLimitReached`
- [ ] Tested on device (alarm sound/vibration differs from Simulator)

## References

- Patterns and code: `references/alarmkit-patterns.md`
- Apple docs: [AlarmKit](https://sosumi.ai/documentation/alarmkit) |
  [AlarmManager](https://sosumi.ai/documentation/alarmkit/alarmmanager) |
  [AlarmAttributes](https://sosumi.ai/documentation/alarmkit/alarmattributes) |
  [Scheduling an alarm](https://sosumi.ai/documentation/alarmkit/scheduling-an-alarm-with-alarmkit)
