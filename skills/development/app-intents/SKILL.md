---
name: app-intents
description: App Intents framework for Siri, Shortcuts, Spotlight, Action Button, and system integration. Use when user asks about Siri, Shortcuts, App Intents, voice commands, Action Button, or system integration.
allowed-tools: Bash, Read, Write, Edit
---

# App Intents Framework

Comprehensive guide to App Intents for Siri integration, Shortcuts, Spotlight, Action Button, and interactive snippets in iOS 26.

## Prerequisites

- iOS 16+ for App Intents (iOS 26 recommended)
- Xcode 26+

---

## Framework Overview

### Core Concepts

- **Intents** = Verbs (actions your app can perform)
- **App Entities** = Dynamic Nouns (content in your app)
- **App Enums** = Static Nouns (fixed options)

### Where App Intents Appear

- **Siri** - Voice-activated commands
- **Shortcuts** - User-created automations
- **Spotlight** - Search suggestions and actions
- **Action Button** - iPhone 15 Pro hardware button
- **Apple Pencil** - Squeeze gesture
- **Focus Filters** - Customize app behavior per focus

### Import

```swift
import AppIntents
```

---

## Creating App Intents

### Basic Intent

```swift
import AppIntents

struct OpenNoteIntent: AppIntent {
    static var title: LocalizedStringResource = "Open Note"
    static var description = IntentDescription("Opens a specific note in the app")

    @Parameter(title: "Note")
    var note: NoteEntity

    func perform() async throws -> some IntentResult {
        // Open the note in your app
        await NoteManager.shared.open(note.id)

        return .result()
    }
}
```

### Intent with Parameters

```swift
struct CreateNoteIntent: AppIntent {
    static var title: LocalizedStringResource = "Create Note"
    static var description = IntentDescription("Creates a new note with the specified content")

    @Parameter(title: "Title")
    var title: String

    @Parameter(title: "Content", default: "")
    var content: String

    @Parameter(title: "Folder", optionsProvider: FolderOptionsProvider())
    var folder: FolderEntity?

    func perform() async throws -> some IntentResult {
        let note = await NoteManager.shared.create(
            title: title,
            content: content,
            in: folder?.id
        )

        return .result(value: NoteEntity(note: note))
    }

    struct FolderOptionsProvider: DynamicOptionsProvider {
        func results() async throws -> [FolderEntity] {
            let folders = await FolderManager.shared.all()
            return folders.map { FolderEntity(folder: $0) }
        }
    }
}
```

### Intent Results

```swift
// Simple result
return .result()

// Result with value
return .result(value: noteEntity)

// Result with dialog (for Siri)
return .result(dialog: "Note created successfully")

// Result with view snippet
return .result(
    dialog: "Here's your note",
    view: NoteSnippetView(note: note)
)

// Result opening app
return .result(opensIntent: OpenNoteIntent(note: noteEntity))
```

---

## App Entities

### Defining an Entity

```swift
import AppIntents

struct NoteEntity: AppEntity {
    static var typeDisplayRepresentation = TypeDisplayRepresentation(name: "Note")

    var id: UUID
    var title: String
    var content: String
    var createdAt: Date

    var displayRepresentation: DisplayRepresentation {
        DisplayRepresentation(
            title: "\(title)",
            subtitle: "\(content.prefix(50))...",
            image: .init(systemName: "doc.text")
        )
    }

    static var defaultQuery = NoteEntityQuery()

    init(note: Note) {
        self.id = note.id
        self.title = note.title
        self.content = note.content
        self.createdAt = note.createdAt
    }
}
```

### Entity Query

```swift
struct NoteEntityQuery: EntityQuery {
    func entities(for identifiers: [UUID]) async throws -> [NoteEntity] {
        let notes = await NoteManager.shared.fetch(ids: identifiers)
        return notes.map { NoteEntity(note: $0) }
    }

    func suggestedEntities() async throws -> [NoteEntity] {
        let recentNotes = await NoteManager.shared.recentNotes(limit: 5)
        return recentNotes.map { NoteEntity(note: $0) }
    }
}
```

### Searchable Entity Query

```swift
struct NoteEntityQuery: EntityStringQuery {
    func entities(for identifiers: [UUID]) async throws -> [NoteEntity] {
        let notes = await NoteManager.shared.fetch(ids: identifiers)
        return notes.map { NoteEntity(note: $0) }
    }

    func entities(matching string: String) async throws -> [NoteEntity] {
        let notes = await NoteManager.shared.search(query: string)
        return notes.map { NoteEntity(note: $0) }
    }

    func suggestedEntities() async throws -> [NoteEntity] {
        let recentNotes = await NoteManager.shared.recentNotes(limit: 5)
        return recentNotes.map { NoteEntity(note: $0) }
    }
}
```

### Property Queries (iOS 17+)

```swift
struct NoteEntityQuery: EntityPropertyQuery {
    static var properties = QueryProperties {
        Property(\NoteEntity.$title) {
            EqualToComparator { $0 }
            ContainsComparator { $0 }
        }
        Property(\NoteEntity.$createdAt) {
            LessThanComparator { $0 }
            GreaterThanComparator { $0 }
        }
    }

    static var sortingOptions = SortingOptions {
        SortableBy(\NoteEntity.$title)
        SortableBy(\NoteEntity.$createdAt)
    }

    func entities(
        matching comparators: [EntityQueryComparator<NoteEntity>],
        mode: ComparatorMode,
        sortedBy: [EntityQuerySort<NoteEntity>],
        limit: Int?
    ) async throws -> [NoteEntity] {
        // Apply filters and sorting
        var notes = await NoteManager.shared.all()

        // Apply comparators
        for comparator in comparators {
            notes = notes.filter { comparator.evaluate($0) }
        }

        // Apply sorting
        for sort in sortedBy {
            notes.sort(by: sort.compare)
        }

        // Apply limit
        if let limit {
            notes = Array(notes.prefix(limit))
        }

        return notes.map { NoteEntity(note: $0) }
    }
}
```

---

## App Enums

### Defining Enums

```swift
import AppIntents

enum NoteCategory: String, AppEnum {
    case personal
    case work
    case ideas
    case todo

    static var typeDisplayRepresentation = TypeDisplayRepresentation(name: "Category")

    static var caseDisplayRepresentations: [NoteCategory: DisplayRepresentation] = [
        .personal: DisplayRepresentation(title: "Personal", image: .init(systemName: "person")),
        .work: DisplayRepresentation(title: "Work", image: .init(systemName: "briefcase")),
        .ideas: DisplayRepresentation(title: "Ideas", image: .init(systemName: "lightbulb")),
        .todo: DisplayRepresentation(title: "To-Do", image: .init(systemName: "checklist"))
    ]
}
```

### Using Enums in Intents

```swift
struct FilterNotesIntent: AppIntent {
    static var title: LocalizedStringResource = "Filter Notes"

    @Parameter(title: "Category")
    var category: NoteCategory

    func perform() async throws -> some IntentResult {
        let notes = await NoteManager.shared.filter(by: category)
        return .result(value: notes.map { NoteEntity(note: $0) })
    }
}
```

---

## App Shortcuts

### AppShortcutsProvider

```swift
import AppIntents

struct MyAppShortcuts: AppShortcutsProvider {
    static var appShortcuts: [AppShortcut] {
        AppShortcut(
            intent: CreateNoteIntent(),
            phrases: [
                "Create a note in \(.applicationName)",
                "New note in \(.applicationName)",
                "Add note to \(.applicationName)"
            ],
            shortTitle: "Create Note",
            systemImageName: "plus.circle"
        )

        AppShortcut(
            intent: OpenRecentNoteIntent(),
            phrases: [
                "Open my recent note in \(.applicationName)",
                "Show last note in \(.applicationName)"
            ],
            shortTitle: "Recent Note",
            systemImageName: "clock"
        )

        AppShortcut(
            intent: SearchNotesIntent(),
            phrases: [
                "Search notes in \(.applicationName)",
                "Find \(\.$query) in \(.applicationName)"
            ],
            shortTitle: "Search",
            systemImageName: "magnifyingglass"
        )
    }
}
```

### Phrase Rules

- Must include `\(.applicationName)` placeholder
- Maximum one parameter reference per phrase
- Parameter must use `\(\.$parameterName)` syntax
- Keep phrases natural and varied

### Automatic Registration

App Shortcuts are automatically registered when:
- App is installed
- App is updated
- AppShortcutsProvider is modified

---

## Interactive Snippets (MicroUI)

### Result Snippets

```swift
struct ShowNoteIntent: AppIntent {
    static var title: LocalizedStringResource = "Show Note"

    @Parameter(title: "Note")
    var note: NoteEntity

    func perform() async throws -> some IntentResult & ShowsSnippetView {
        return .result(
            dialog: "Here's your note",
            view: NoteSnippetView(note: note)
        )
    }
}

struct NoteSnippetView: View {
    let note: NoteEntity

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text(note.title)
                .font(.headline)
            Text(note.content)
                .font(.body)
                .lineLimit(3)
            Text(note.createdAt, style: .relative)
                .font(.caption)
                .foregroundStyle(.secondary)
        }
        .padding()
    }
}
```

### Confirmation Snippets

```swift
struct DeleteNoteIntent: AppIntent {
    static var title: LocalizedStringResource = "Delete Note"

    @Parameter(title: "Note")
    var note: NoteEntity

    func perform() async throws -> some IntentResult {
        try await requestConfirmation(
            result: .result(
                dialog: "Are you sure you want to delete this note?",
                view: DeleteConfirmationView(note: note)
            )
        )

        await NoteManager.shared.delete(note.id)
        return .result(dialog: "Note deleted")
    }
}

struct DeleteConfirmationView: View {
    let note: NoteEntity

    var body: some View {
        VStack(spacing: 12) {
            Image(systemName: "trash")
                .font(.largeTitle)
                .foregroundStyle(.red)

            Text("Delete '\(note.title)'?")
                .font(.headline)

            Text("This action cannot be undone.")
                .font(.caption)
                .foregroundStyle(.secondary)
        }
        .padding()
    }
}
```

### Interactive Snippet Buttons

```swift
struct NoteActionsSnippetView: View {
    let note: NoteEntity

    var body: some View {
        VStack(spacing: 12) {
            Text(note.title)
                .font(.headline)

            HStack(spacing: 16) {
                Button(intent: EditNoteIntent(note: note)) {
                    Label("Edit", systemImage: "pencil")
                }

                Button(intent: ShareNoteIntent(note: note)) {
                    Label("Share", systemImage: "square.and.arrow.up")
                }
            }
            .buttonStyle(.bordered)
        }
        .padding()
    }
}
```

### Snippet Design Guidelines

- Keep snippets compact (fits in Siri/Spotlight card)
- Use larger text for readability
- High contrast colors
- Clear, tappable buttons
- Concise content

---

## Foreground vs Background Execution

### Background Execution (Default)

```swift
struct QuickNoteIntent: AppIntent {
    static var title: LocalizedStringResource = "Quick Note"

    @Parameter(title: "Content")
    var content: String

    // Runs in background without opening app
    func perform() async throws -> some IntentResult {
        await NoteManager.shared.quickCreate(content: content)
        return .result(dialog: "Note saved!")
    }
}
```

### Foreground Execution

```swift
struct EditNoteIntent: AppIntent {
    static var title: LocalizedStringResource = "Edit Note"

    // Opens app when intent runs
    static var openAppWhenRun = true

    @Parameter(title: "Note")
    var note: NoteEntity

    func perform() async throws -> some IntentResult {
        // App is now in foreground
        await NoteManager.shared.openEditor(for: note.id)
        return .result()
    }
}
```

### Conditional Foreground

```swift
struct ViewNoteIntent: AppIntent {
    static var title: LocalizedStringResource = "View Note"

    @Parameter(title: "Note")
    var note: NoteEntity

    @Parameter(title: "Open in App")
    var openInApp: Bool

    static var openAppWhenRun: Bool {
        // Dynamically determined
        return false
    }

    func perform() async throws -> some IntentResult {
        if openInApp {
            // Return result that opens app
            return .result(opensIntent: OpenNoteIntent(note: note))
        } else {
            // Return snippet view
            return .result(view: NoteSnippetView(note: note))
        }
    }
}
```

---

## Dependency Injection

### @Dependency Property Wrapper

```swift
struct CreateNoteIntent: AppIntent {
    static var title: LocalizedStringResource = "Create Note"

    @Dependency
    var noteService: NoteService

    @Parameter(title: "Title")
    var title: String

    func perform() async throws -> some IntentResult {
        let note = try await noteService.create(title: title)
        return .result(value: NoteEntity(note: note))
    }
}
```

### Registering Dependencies

Register dependencies early in app lifecycle:

```swift
@main
struct MyApp: App {
    init() {
        // Register dependencies for App Intents
        AppDependencyManager.shared.add(dependency: NoteService.shared)
        AppDependencyManager.shared.add(dependency: FolderService.shared)
    }

    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}
```

---

## Focus Filters

### Defining a Focus Filter

```swift
import AppIntents

struct NoteFocusFilter: SetFocusFilterIntent {
    static var title: LocalizedStringResource = "Set Note Filter"
    static var description = IntentDescription("Filter notes during this Focus")

    @Parameter(title: "Show Categories")
    var categories: [NoteCategory]?

    @Parameter(title: "Hide Work Notes")
    var hideWork: Bool?

    var displayRepresentation: DisplayRepresentation {
        DisplayRepresentation(title: "Note Filter")
    }

    func perform() async throws -> some IntentResult {
        // Apply filter settings
        if let categories {
            FocusState.shared.visibleCategories = categories
        }
        if let hideWork {
            FocusState.shared.hideWorkNotes = hideWork
        }
        return .result()
    }
}
```

---

## Spotlight Integration

### Featured in Spotlight

Intents automatically appear in Spotlight when:
- User searches for related terms
- App Shortcuts are defined
- Entities match search queries

### Donating Activities

```swift
import Intents

func userViewedNote(_ note: Note) {
    let activity = NSUserActivity(activityType: "com.app.viewNote")
    activity.title = note.title
    activity.userInfo = ["noteId": note.id.uuidString]
    activity.isEligibleForSearch = true
    activity.isEligibleForPrediction = true

    // Associate with App Intent
    activity.shortcutAvailability = .sleepInBed

    UIApplication.shared.currentUserActivity = activity
}
```

---

## Action Button & Apple Pencil

### Action Button Intent

```swift
struct QuickCaptureIntent: AppIntent {
    static var title: LocalizedStringResource = "Quick Capture"
    static var description = IntentDescription("Quickly capture a thought")

    // Good for Action Button - fast execution
    func perform() async throws -> some IntentResult & OpensIntent {
        // Create new capture and open editor
        let capture = await CaptureManager.shared.createQuick()
        return .result(opensIntent: OpenCaptureIntent(capture: capture))
    }
}
```

Users configure Action Button in Settings → Action Button → Shortcut → [Your App Shortcut]

### Apple Pencil Squeeze

Same intents work for Apple Pencil squeeze gesture on supported devices.

---

## Testing Intents

### Testing in Shortcuts App

1. Build and run your app
2. Open Shortcuts app
3. Create new shortcut
4. Search for your app's intents
5. Configure parameters
6. Run shortcut

### Testing with Siri

1. Build and run app
2. Say: "Hey Siri, [your phrase]"
3. Verify Siri understands and executes

### Programmatic Testing

```swift
import Testing
import AppIntents

@Test
func testCreateNoteIntent() async throws {
    var intent = CreateNoteIntent()
    intent.title = "Test Note"
    intent.content = "Test content"

    let result = try await intent.perform()

    // Verify result
    #expect(result != nil)
}
```

---

## Best Practices

### 1. Natural Phrases

```swift
// GOOD: Natural language
"Create a note in \(.applicationName)"
"Add \(\.$title) to my notes"

// AVOID: Technical language
"Execute CreateNote command in \(.applicationName)"
```

### 2. Meaningful Dialogs

```swift
// GOOD: Contextual confirmation
return .result(dialog: "Created note '\(title)' in your Ideas folder")

// AVOID: Generic responses
return .result(dialog: "Done")
```

### 3. Fast Background Execution

```swift
// Keep background intents fast
func perform() async throws -> some IntentResult {
    // Quick operation
    await quickSave(data)
    return .result(dialog: "Saved!")
}
```

### 4. Graceful Error Handling

```swift
func perform() async throws -> some IntentResult {
    guard let note = await NoteManager.shared.find(id: noteId) else {
        throw IntentError.noteNotFound
    }
    // Continue...
}

enum IntentError: Error, CustomLocalizedStringResourceConvertible {
    case noteNotFound

    var localizedStringResource: LocalizedStringResource {
        switch self {
        case .noteNotFound:
            return "Note not found. It may have been deleted."
        }
    }
}
```

---

## Official Resources

- [App Intents Documentation](https://developer.apple.com/documentation/appintents)
- [App Shortcuts Documentation](https://developer.apple.com/documentation/appintents/app-shortcuts)
- [WWDC23: Explore enhancements to App Intents](https://developer.apple.com/videos/play/wwdc2023/10103/)
- [WWDC22: Dive into App Intents](https://developer.apple.com/videos/play/wwdc2022/10032/)
- [WWDC25: Get to know App Intents](https://developer.apple.com/videos/play/wwdc2025/244/)
