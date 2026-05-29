---
name: swiftui-data
description: Implement data persistence with SwiftData, Core Data, CloudKit sync, and local storage. Use when storing app data, creating database models, syncing with iCloud, or managing user preferences with AppStorage.
user-invocable: false
---

# SwiftUI Data Persistence

## SwiftData (iOS 17+) - Recommended

```swift
import SwiftData

@Model
final class Task {
    var title: String
    var isCompleted: Bool
    var createdAt: Date
    var priority: Priority

    @Relationship(deleteRule: .cascade)
    var subtasks: [Subtask]?

    init(title: String, priority: Priority = .medium) {
        self.title = title
        self.isCompleted = false
        self.createdAt = .now
        self.priority = priority
    }
}

enum Priority: String, Codable, CaseIterable {
    case low, medium, high
}

// App configuration
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .modelContainer(for: Task.self)
    }
}
```

## SwiftData Queries

```swift
struct TaskListView: View {
    @Query(
        filter: #Predicate<Task> { !$0.isCompleted },
        sort: \Task.createdAt,
        order: .reverse
    )
    private var tasks: [Task]

    @Environment(\.modelContext) private var context

    var body: some View {
        List(tasks) { task in
            TaskRow(task: task)
                .swipeActions {
                    Button("Delete", role: .destructive) {
                        context.delete(task)
                    }
                }
        }
    }

    func addTask(_ title: String) {
        let task = Task(title: title)
        context.insert(task)
    }
}
```

## CloudKit Sync with SwiftData

```swift
// Enable in App configuration
@main
struct MyApp: App {
    var container: ModelContainer

    init() {
        let schema = Schema([Task.self, Subtask.self])
        let config = ModelConfiguration(
            schema: schema,
            cloudKitDatabase: .private("iCloud.com.myapp")
        )
        container = try! ModelContainer(
            for: schema,
            configurations: [config]
        )
    }

    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .modelContainer(container)
    }
}
```

## AppStorage & SceneStorage

```swift
struct SettingsView: View {
    // Persists to UserDefaults
    @AppStorage("username") private var username = ""
    @AppStorage("isDarkMode") private var isDarkMode = false
    @AppStorage("fontSize") private var fontSize = 14.0

    // Persists per-scene (window state)
    @SceneStorage("selectedTab") private var selectedTab = 0

    var body: some View {
        Form {
            TextField("Username", text: $username)
            Toggle("Dark Mode", isOn: $isDarkMode)
            Slider(value: $fontSize, in: 10...24)
        }
    }
}
```

## When to Use What

| Solution | Use Case |
|----------|----------|
| `@AppStorage` | Simple preferences, settings |
| `@SceneStorage` | Window/scene-specific UI state |
| **SwiftData** | Complex models, relationships, CloudKit |
| **Core Data** | iOS < 17, advanced migrations |
| **Keychain** | Sensitive data (tokens, passwords) |
| **FileManager** | Documents, large files, exports |
