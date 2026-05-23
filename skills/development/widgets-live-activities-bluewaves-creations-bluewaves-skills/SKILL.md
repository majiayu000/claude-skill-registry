---
name: widgets-live-activities
description: WidgetKit for Home Screen widgets, Live Activities, Dynamic Island, and Control Center widgets. Use when user asks about widgets, WidgetKit, Live Activities, Dynamic Island, or interactive widgets.
allowed-tools: Bash, Read, Write, Edit
---

# WidgetKit and Live Activities

Comprehensive guide to WidgetKit for Home Screen widgets, Live Activities, Dynamic Island, and Control Center integration in iOS 26.

## Prerequisites

- iOS 17+ for interactive widgets (iOS 26 recommended)
- Xcode 26+
- Widget Extension target

---

## Widget Extension Setup

### Creating Widget Target

1. File → New → Target
2. Select "Widget Extension"
3. Name your widget
4. Enable "Include Live Activity" if needed
5. Enable "Include Configuration App Intent" for configurable widgets

### Basic Widget Structure

```swift
import WidgetKit
import SwiftUI

struct SimpleWidget: Widget {
    let kind: String = "SimpleWidget"

    var body: some WidgetConfiguration {
        StaticConfiguration(kind: kind, provider: Provider()) { entry in
            SimpleWidgetEntryView(entry: entry)
                .containerBackground(.fill.tertiary, for: .widget)
        }
        .configurationDisplayName("My Widget")
        .description("Shows important information")
        .supportedFamilies([.systemSmall, .systemMedium, .systemLarge])
    }
}
```

### Timeline Provider

```swift
struct Provider: TimelineProvider {
    func placeholder(in context: Context) -> SimpleEntry {
        SimpleEntry(date: Date(), message: "Loading...")
    }

    func getSnapshot(in context: Context, completion: @escaping (SimpleEntry) -> Void) {
        let entry = SimpleEntry(date: Date(), message: "Snapshot")
        completion(entry)
    }

    func getTimeline(in context: Context, completion: @escaping (Timeline<SimpleEntry>) -> Void) {
        var entries: [SimpleEntry] = []

        let currentDate = Date()
        for hourOffset in 0..<5 {
            let entryDate = Calendar.current.date(byAdding: .hour, value: hourOffset, to: currentDate)!
            let entry = SimpleEntry(date: entryDate, message: "Hour \(hourOffset)")
            entries.append(entry)
        }

        let timeline = Timeline(entries: entries, policy: .atEnd)
        completion(timeline)
    }
}

struct SimpleEntry: TimelineEntry {
    let date: Date
    let message: String
}
```

### Widget View

```swift
struct SimpleWidgetEntryView: View {
    var entry: Provider.Entry

    @Environment(\.widgetFamily) var family

    var body: some View {
        switch family {
        case .systemSmall:
            SmallWidgetView(entry: entry)
        case .systemMedium:
            MediumWidgetView(entry: entry)
        case .systemLarge:
            LargeWidgetView(entry: entry)
        default:
            Text(entry.message)
        }
    }
}

struct SmallWidgetView: View {
    let entry: SimpleEntry

    var body: some View {
        VStack {
            Text(entry.message)
                .font(.headline)
            Text(entry.date, style: .time)
                .font(.caption)
        }
    }
}
```

---

## iOS 26 Glass Presentation

### Accented Rendering

Widgets on iOS 26 use the new glass presentation system:

```swift
struct GlassWidget: Widget {
    var body: some WidgetConfiguration {
        StaticConfiguration(kind: "GlassWidget", provider: Provider()) { entry in
            GlassWidgetView(entry: entry)
                .containerBackground(.fill.tertiary, for: .widget)
        }
        .supportedFamilies([.systemSmall, .systemMedium])
    }
}

struct GlassWidgetView: View {
    let entry: SimpleEntry

    var body: some View {
        VStack {
            Image(systemName: "star.fill")
                .font(.largeTitle)
                // Accented rendering for glass background
                .widgetAccentedRenderingMode(.accentedDesaturated)

            Text(entry.message)
                .font(.headline)
        }
    }
}
```

### Widget Accented Rendering Modes

```swift
// For images in widgets
Image("CustomIcon")
    .widgetAccentedRenderingMode(.desaturated)        // Blend with home screen
    .widgetAccentedRenderingMode(.accentedDesaturated) // Blend with accent
    .widgetAccentedRenderingMode(.fullColor)          // Full color (media only)
```

---

## Interactive Widgets

### Button Actions

```swift
import AppIntents

struct InteractiveWidget: Widget {
    var body: some WidgetConfiguration {
        StaticConfiguration(kind: "Interactive", provider: Provider()) { entry in
            InteractiveWidgetView(entry: entry)
                .containerBackground(.fill.tertiary, for: .widget)
        }
        .supportedFamilies([.systemSmall, .systemMedium])
    }
}

struct InteractiveWidgetView: View {
    let entry: TaskEntry

    var body: some View {
        VStack(alignment: .leading) {
            Text(entry.task.title)
                .font(.headline)

            Button(intent: ToggleTaskIntent(taskId: entry.task.id)) {
                Label(
                    entry.task.isComplete ? "Completed" : "Mark Done",
                    systemImage: entry.task.isComplete ? "checkmark.circle.fill" : "circle"
                )
            }
            .buttonStyle(.bordered)
        }
    }
}

struct ToggleTaskIntent: AppIntent {
    static var title: LocalizedStringResource = "Toggle Task"

    @Parameter(title: "Task ID")
    var taskId: String

    func perform() async throws -> some IntentResult {
        await TaskManager.shared.toggle(taskId)
        return .result()
    }
}
```

### Toggle Actions

```swift
struct ToggleWidgetView: View {
    let entry: SettingEntry

    var body: some View {
        Toggle(isOn: entry.isEnabled, intent: ToggleSettingIntent(settingId: entry.id)) {
            Label("Enable Feature", systemImage: "gear")
        }
        .toggleStyle(.button)
    }
}
```

---

## Configurable Widgets

### App Intent Configuration

```swift
import AppIntents

struct ConfigurableWidget: Widget {
    var body: some WidgetConfiguration {
        AppIntentConfiguration(
            kind: "ConfigurableWidget",
            intent: ConfigureWidgetIntent.self,
            provider: ConfigurableProvider()
        ) { entry in
            ConfigurableWidgetView(entry: entry)
                .containerBackground(.fill.tertiary, for: .widget)
        }
        .configurationDisplayName("Custom Widget")
        .description("Configure which data to show")
        .supportedFamilies([.systemSmall, .systemMedium])
    }
}

struct ConfigureWidgetIntent: WidgetConfigurationIntent {
    static var title: LocalizedStringResource = "Configure Widget"
    static var description = IntentDescription("Choose what to display")

    @Parameter(title: "Category")
    var category: WidgetCategory?

    @Parameter(title: "Show Count")
    var showCount: Bool
}

enum WidgetCategory: String, AppEnum {
    case recent, favorites, all

    static var typeDisplayRepresentation = TypeDisplayRepresentation(name: "Category")
    static var caseDisplayRepresentations: [WidgetCategory: DisplayRepresentation] = [
        .recent: "Recent",
        .favorites: "Favorites",
        .all: "All"
    ]
}
```

### Configurable Provider

```swift
struct ConfigurableProvider: AppIntentTimelineProvider {
    func placeholder(in context: Context) -> ConfigurableEntry {
        ConfigurableEntry(date: Date(), configuration: ConfigureWidgetIntent())
    }

    func snapshot(for configuration: ConfigureWidgetIntent, in context: Context) async -> ConfigurableEntry {
        ConfigurableEntry(date: Date(), configuration: configuration)
    }

    func timeline(for configuration: ConfigureWidgetIntent, in context: Context) async -> Timeline<ConfigurableEntry> {
        let entry = ConfigurableEntry(date: Date(), configuration: configuration)
        return Timeline(entries: [entry], policy: .after(Date().addingTimeInterval(3600)))
    }
}

struct ConfigurableEntry: TimelineEntry {
    let date: Date
    let configuration: ConfigureWidgetIntent
}
```

---

## Live Activities

### Activity Attributes

```swift
import ActivityKit

struct DeliveryAttributes: ActivityAttributes {
    public struct ContentState: Codable, Hashable {
        var status: DeliveryStatus
        var estimatedArrival: Date
        var driverName: String
    }

    var orderNumber: String
    var restaurantName: String
}

enum DeliveryStatus: String, Codable {
    case preparing
    case onTheWay
    case arriving
    case delivered
}
```

### Live Activity View

```swift
struct DeliveryActivityView: View {
    let context: ActivityViewContext<DeliveryAttributes>

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                Text(context.attributes.restaurantName)
                    .font(.headline)
                Spacer()
                Text(context.state.status.displayName)
                    .font(.caption)
                    .foregroundStyle(.secondary)
            }

            ProgressView(value: context.state.status.progress)

            HStack {
                Label(context.state.driverName, systemImage: "person.circle")
                Spacer()
                Text(context.state.estimatedArrival, style: .timer)
            }
            .font(.caption)
        }
        .padding()
    }
}
```

### Dynamic Island

```swift
struct DeliveryLiveActivity: Widget {
    var body: some WidgetConfiguration {
        ActivityConfiguration(for: DeliveryAttributes.self) { context in
            // Lock screen presentation
            DeliveryActivityView(context: context)
        } dynamicIsland: { context in
            DynamicIsland {
                // Expanded regions
                DynamicIslandExpandedRegion(.leading) {
                    Image(systemName: "bag.fill")
                }
                DynamicIslandExpandedRegion(.trailing) {
                    Text(context.state.estimatedArrival, style: .timer)
                }
                DynamicIslandExpandedRegion(.center) {
                    Text(context.attributes.restaurantName)
                        .font(.headline)
                }
                DynamicIslandExpandedRegion(.bottom) {
                    ProgressView(value: context.state.status.progress)
                }
            } compactLeading: {
                Image(systemName: "bag.fill")
            } compactTrailing: {
                Text(context.state.estimatedArrival, style: .timer)
            } minimal: {
                Image(systemName: "bag.fill")
            }
        }
    }
}
```

### Starting a Live Activity

```swift
func startDeliveryActivity(order: Order) async throws {
    guard ActivityAuthorizationInfo().areActivitiesEnabled else {
        throw ActivityError.notAuthorized
    }

    let attributes = DeliveryAttributes(
        orderNumber: order.id,
        restaurantName: order.restaurant
    )

    let initialState = DeliveryAttributes.ContentState(
        status: .preparing,
        estimatedArrival: order.estimatedArrival,
        driverName: "Assigning..."
    )

    let activity = try Activity.request(
        attributes: attributes,
        content: .init(state: initialState, staleDate: nil),
        pushType: .token  // Enable push updates
    )

    // Store activity ID for later updates
    UserDefaults.standard.set(activity.id, forKey: "currentDeliveryActivity")

    // Get push token for server updates
    for await token in activity.pushTokenUpdates {
        let tokenString = token.map { String(format: "%02x", $0) }.joined()
        await sendTokenToServer(tokenString)
    }
}
```

### Updating Live Activity

```swift
func updateDeliveryStatus(to status: DeliveryStatus, driver: String? = nil) async {
    guard let activityId = UserDefaults.standard.string(forKey: "currentDeliveryActivity"),
          let activity = Activity<DeliveryAttributes>.activities.first(where: { $0.id == activityId })
    else { return }

    var newState = activity.content.state
    newState.status = status
    if let driver {
        newState.driverName = driver
    }

    await activity.update(
        ActivityContent(state: newState, staleDate: nil)
    )
}
```

### Ending Live Activity

```swift
func endDeliveryActivity() async {
    guard let activityId = UserDefaults.standard.string(forKey: "currentDeliveryActivity"),
          let activity = Activity<DeliveryAttributes>.activities.first(where: { $0.id == activityId })
    else { return }

    let finalState = DeliveryAttributes.ContentState(
        status: .delivered,
        estimatedArrival: Date(),
        driverName: activity.content.state.driverName
    )

    await activity.end(
        ActivityContent(state: finalState, staleDate: nil),
        dismissalPolicy: .after(.now + 3600)  // Dismiss after 1 hour
    )

    UserDefaults.standard.removeObject(forKey: "currentDeliveryActivity")
}
```

---

## iOS 26 Live Activity Updates

### CarPlay Support

Live Activities now appear on CarPlay in iOS 26:

```swift
struct CarPlayDeliveryActivity: Widget {
    var body: some WidgetConfiguration {
        ActivityConfiguration(for: DeliveryAttributes.self) { context in
            // Lock screen
            DeliveryActivityView(context: context)
        } dynamicIsland: { context in
            // Dynamic Island config...
        }
        .supplementalActivityFamilies([.small])  // CarPlay support
    }
}
```

### macOS Support

Live Activities now work on macOS Tahoe:

```swift
#if os(macOS)
struct MacDeliveryActivity: Widget {
    var body: some WidgetConfiguration {
        ActivityConfiguration(for: DeliveryAttributes.self) { context in
            MacDeliveryView(context: context)
        }
    }
}
#endif
```

---

## Control Center Widgets

### Control Widget

```swift
import WidgetKit
import AppIntents

struct QuickToggleControl: ControlWidget {
    var body: some ControlWidgetConfiguration {
        StaticControlConfiguration(kind: "QuickToggle") {
            ControlWidgetToggle(
                "Dark Mode",
                isOn: DarkModeBinding(),
                action: ToggleDarkModeIntent()
            ) { isOn in
                Label(isOn ? "On" : "Off", systemImage: isOn ? "moon.fill" : "sun.max")
            }
        }
        .displayName("Dark Mode")
        .description("Toggle dark mode")
    }
}

struct DarkModeBinding: ControlValueProvider {
    var previewValue: Bool { false }

    func currentValue() async throws -> Bool {
        await SettingsManager.shared.isDarkMode
    }
}

struct ToggleDarkModeIntent: SetValueIntent {
    static var title: LocalizedStringResource = "Toggle Dark Mode"

    @Parameter(title: "Dark Mode")
    var value: Bool

    func perform() async throws -> some IntentResult {
        await SettingsManager.shared.setDarkMode(value)
        return .result()
    }
}
```

### Control Widget Button

```swift
struct QuickActionControl: ControlWidget {
    var body: some ControlWidgetConfiguration {
        StaticControlConfiguration(kind: "QuickAction") {
            ControlWidgetButton(action: QuickNoteIntent()) {
                Label("Quick Note", systemImage: "note.text.badge.plus")
            }
        }
        .displayName("Quick Note")
        .description("Create a quick note")
    }
}
```

---

## Widget Relevance (watchOS 26)

### Relevance Configuration

```swift
struct RelevantWidget: Widget {
    var body: some WidgetConfiguration {
        StaticConfiguration(kind: "Relevant", provider: RelevantProvider()) { entry in
            RelevantWidgetView(entry: entry)
        }
        .supportedFamilies([.accessoryRectangular])
    }
}

struct RelevantProvider: TimelineProvider {
    func relevances() async -> WidgetRelevances<Void> {
        // Define when widget is most relevant
        return WidgetRelevances(
            // Show during workout
            RelevantContext.workout: .defaultLarge,
            // Show in morning
            RelevantContext.date(from: morning, to: noon): .defaultMedium
        )
    }

    // Other provider methods...
}
```

---

## Widget Data Sharing

### App Groups

```swift
// In both app and widget extension
let sharedDefaults = UserDefaults(suiteName: "group.com.yourapp.shared")
sharedDefaults?.set(data, forKey: "widgetData")

// In widget
let data = UserDefaults(suiteName: "group.com.yourapp.shared")?.data(forKey: "widgetData")
```

### Shared Container

```swift
let containerURL = FileManager.default.containerURL(
    forSecurityApplicationGroupIdentifier: "group.com.yourapp.shared"
)
```

### Triggering Widget Refresh

```swift
import WidgetKit

// Refresh specific widget
WidgetCenter.shared.reloadTimelines(ofKind: "MyWidget")

// Refresh all widgets
WidgetCenter.shared.reloadAllTimelines()
```

---

## Best Practices

### 1. Efficient Timeline Updates

```swift
func getTimeline(in context: Context, completion: @escaping (Timeline<Entry>) -> Void) {
    // Generate only necessary entries
    let entries = generateRelevantEntries()

    // Use appropriate refresh policy
    let policy: TimelineReloadPolicy
    if hasUpcomingEvents {
        policy = .after(nextEventDate)
    } else {
        policy = .atEnd
    }

    completion(Timeline(entries: entries, policy: policy))
}
```

### 2. Handle Widget Families

```swift
struct AdaptiveWidgetView: View {
    @Environment(\.widgetFamily) var family

    var body: some View {
        switch family {
        case .systemSmall:
            CompactView()
        case .systemMedium:
            MediumView()
        case .systemLarge, .systemExtraLarge:
            DetailedView()
        case .accessoryCircular:
            CircularView()
        case .accessoryRectangular:
            RectangularView()
        default:
            DefaultView()
        }
    }
}
```

### 3. Test with Widget Development Mode

```swift
// In scheme arguments
-widgetKitDevMode YES
```

### 4. Memory Efficiency

```swift
// Load images efficiently
Image("icon")
    .resizable()
    .aspectRatio(contentMode: .fit)

// Avoid heavy computations in view body
// Pre-calculate in provider
```

---

## Official Resources

- [WidgetKit Documentation](https://developer.apple.com/documentation/widgetkit)
- [ActivityKit Documentation](https://developer.apple.com/documentation/activitykit)
- [WWDC23: Bring widgets to new places](https://developer.apple.com/videos/play/wwdc2023/10027/)
- [WWDC25: What's new in widgets](https://developer.apple.com/videos/play/wwdc2025/278/)
- [Adding interactivity to widgets](https://developer.apple.com/documentation/widgetkit/adding-interactivity-to-widgets-and-live-activities)
