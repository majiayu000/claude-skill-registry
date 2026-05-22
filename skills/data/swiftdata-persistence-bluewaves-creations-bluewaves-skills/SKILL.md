---
name: swiftdata-persistence
description: SwiftData framework with @Model macro, @Query, relationships, and NATIVE iCloud sync. Use when user asks about data persistence, SwiftData, @Model, @Query, database storage, iCloud sync, or CoreData migration.
allowed-tools: Bash, Read, Write, Edit
---

# SwiftData Persistence

Comprehensive guide to SwiftData framework, the @Model macro, reactive queries, relationships, and native iCloud synchronization for iOS 26 development.

## Prerequisites

- iOS 17+ for SwiftData (iOS 26 recommended)
- Xcode 26+

---

## @Model Macro Basics

### Defining a Model

```swift
import SwiftData

@Model
class Note {
    var title: String
    var content: String
    var createdAt: Date
    var isPinned: Bool

    init(title: String, content: String = "") {
        self.title = title
        self.content = content
        self.createdAt = Date()
        self.isPinned = false
    }
}
```

### What @Model Provides

The `@Model` macro automatically:
- Makes the class persistable
- Tracks property changes
- Enables SwiftUI observation
- Generates schema metadata

### Model Requirements

```swift
@Model
class Item {
    // All stored properties must be:
    // - Codable types (String, Int, Date, Data, etc.)
    // - Other @Model types (relationships)
    // - Arrays/optionals of the above

    var name: String           // ✓ Codable
    var count: Int             // ✓ Codable
    var timestamp: Date        // ✓ Codable
    var data: Data             // ✓ Codable
    var tags: [String]         // ✓ Array of Codable
    var metadata: [String: String]  // ✓ Dictionary of Codable
    var related: RelatedItem?  // ✓ Optional @Model relationship

    // Computed properties are NOT persisted
    var displayName: String {
        name.uppercased()
    }

    init(name: String) {
        self.name = name
        self.count = 0
        self.timestamp = Date()
        self.data = Data()
        self.tags = []
    }
}
```

---

## Model Attributes

### @Attribute Macro

```swift
@Model
class User {
    // Unique constraint (NOT compatible with iCloud sync)
    @Attribute(.unique)
    var email: String

    // Spotlight indexing
    @Attribute(.spotlight)
    var name: String

    // External storage for large data
    @Attribute(.externalStorage)
    var profileImage: Data?

    // Encryption (device-only, not synced to iCloud)
    @Attribute(.encrypt)
    var sensitiveData: String?

    // Preserve value when nil assigned
    @Attribute(.preserveValueOnDeletion)
    var archiveReason: String?

    // Ephemeral (not persisted)
    @Attribute(.ephemeral)
    var temporaryState: String?

    // Custom original name for migration
    @Attribute(originalName: "userName")
    var displayName: String

    init(email: String, name: String) {
        self.email = email
        self.name = name
        self.displayName = name
    }
}
```

### @Transient Macro

```swift
@Model
class Document {
    var title: String
    var content: String

    // Not persisted, recalculated
    @Transient
    var wordCount: Int = 0

    init(title: String, content: String) {
        self.title = title
        self.content = content
        self.wordCount = content.split(separator: " ").count
    }
}
```

---

## Relationships

### One-to-Many Relationship

```swift
@Model
class Folder {
    var name: String

    // One folder has many notes
    @Relationship(deleteRule: .cascade)
    var notes: [Note] = []

    init(name: String) {
        self.name = name
    }
}

@Model
class Note {
    var title: String
    var content: String

    // Many notes belong to one folder (inverse)
    var folder: Folder?

    init(title: String, content: String = "", folder: Folder? = nil) {
        self.title = title
        self.content = content
        self.folder = folder
    }
}
```

### Many-to-Many Relationship

```swift
@Model
class Note {
    var title: String

    // Note can have many tags
    @Relationship(inverse: \Tag.notes)
    var tags: [Tag] = []

    init(title: String) {
        self.title = title
    }
}

@Model
class Tag {
    var name: String

    // Tag can be on many notes
    var notes: [Note] = []

    init(name: String) {
        self.name = name
    }
}
```

### Delete Rules

```swift
@Relationship(deleteRule: .cascade)   // Delete related objects
@Relationship(deleteRule: .nullify)   // Set relationship to nil (default)
@Relationship(deleteRule: .deny)      // Prevent deletion if related exist
@Relationship(deleteRule: .noAction)  // Do nothing
```

### iCloud-Compatible Relationships

**Important:** For iCloud sync, all relationships MUST be optional:

```swift
@Model
class Note {
    var title: String

    // REQUIRED for iCloud: Optional relationships
    var folder: Folder?
    var tags: [Tag]?  // Optional array

    init(title: String) {
        self.title = title
    }
}
```

---

## ModelContainer Configuration

### Basic Setup

```swift
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .modelContainer(for: [Note.self, Folder.self, Tag.self])
    }
}
```

### Custom Configuration

```swift
@main
struct MyApp: App {
    let container: ModelContainer

    init() {
        let schema = Schema([Note.self, Folder.self, Tag.self])

        let config = ModelConfiguration(
            schema: schema,
            isStoredInMemoryOnly: false,
            allowsSave: true
        )

        do {
            container = try ModelContainer(for: schema, configurations: config)
        } catch {
            fatalError("Failed to configure SwiftData: \(error)")
        }
    }

    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .modelContainer(container)
    }
}
```

### Multiple Configurations

```swift
let userConfig = ModelConfiguration(
    "UserData",
    schema: Schema([User.self]),
    url: userDataURL
)

let cacheConfig = ModelConfiguration(
    "Cache",
    schema: Schema([CachedItem.self]),
    isStoredInMemoryOnly: true
)

let container = try ModelContainer(
    for: Schema([User.self, CachedItem.self]),
    configurations: userConfig, cacheConfig
)
```

---

## Native iCloud Sync

### Enabling iCloud Sync (One Line!)

SwiftData includes **native** iCloud sync - no CloudKit code required:

```swift
@main
struct MyApp: App {
    let container: ModelContainer

    init() {
        let schema = Schema([Note.self, Tag.self])

        let config = ModelConfiguration(
            schema: schema,
            cloudKitDatabase: .automatic  // That's it!
        )

        do {
            container = try ModelContainer(for: schema, configurations: config)
        } catch {
            fatalError("Failed to configure SwiftData: \(error)")
        }
    }

    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .modelContainer(container)
    }
}
```

### cloudKitDatabase Options

```swift
// Automatic iCloud sync (recommended)
cloudKitDatabase: .automatic

// Specific CloudKit container
cloudKitDatabase: .private("iCloud.com.yourcompany.yourapp")

// No iCloud sync (local only)
cloudKitDatabase: .none
```

### Xcode Setup for iCloud

1. Select your target in Xcode
2. Go to "Signing & Capabilities"
3. Click "+ Capability"
4. Add "iCloud"
5. Check "CloudKit"
6. Select or create a CloudKit container
7. Add "Background Modes" capability
8. Check "Remote notifications"

### iCloud-Compatible Model Requirements

**Critical rules for iCloud sync:**

```swift
@Model
class Note {
    // ✓ Default values for non-optional properties
    var title: String = ""
    var content: String = ""
    var createdAt: Date = Date()

    // ✓ Optional relationships
    var folder: Folder?
    var tags: [Tag]?

    // ✗ NO unique constraints (not supported by CloudKit)
    // @Attribute(.unique) var id: String  // DON'T DO THIS

    // ✗ NO deny delete rules
    // @Relationship(deleteRule: .deny)    // DON'T DO THIS

    init(title: String = "", content: String = "") {
        self.title = title
        self.content = content
        self.createdAt = Date()
    }
}
```

### Schema Migration for iCloud

After shipping to production:

```swift
// DO:
// - Add new optional properties with defaults
// - Add new optional relationships

// DON'T:
// - Delete properties (data loss)
// - Rename properties (treated as delete + add)
// - Change property types
// - Add required properties without defaults
```

### Initialize CloudKit Schema

Before first production release:

```swift
#if DEBUG
// Run once to create CloudKit schema
try container.mainContext.initializeCloudKitSchema()
#endif
```

---

## @Query Macro

### Basic Query

```swift
struct NotesListView: View {
    @Query var notes: [Note]

    var body: some View {
        List(notes) { note in
            Text(note.title)
        }
    }
}
```

### Sorted Query

```swift
// Single sort
@Query(sort: \Note.createdAt, order: .reverse)
var notes: [Note]

// Multiple sorts
@Query(sort: [
    SortDescriptor(\Note.isPinned, order: .reverse),
    SortDescriptor(\Note.createdAt, order: .reverse)
])
var notes: [Note]
```

### Filtered Query

```swift
// Static predicate
@Query(filter: #Predicate<Note> { note in
    note.isPinned == true
})
var pinnedNotes: [Note]

// Complex predicate
@Query(filter: #Predicate<Note> { note in
    note.title.contains("Swift") && !note.content.isEmpty
})
var swiftNotes: [Note]
```

### Dynamic Filtering

```swift
struct SearchableNotesView: View {
    @State private var searchText = ""

    var body: some View {
        FilteredNotesView(searchText: searchText)
            .searchable(text: $searchText)
    }
}

struct FilteredNotesView: View {
    @Query var notes: [Note]

    init(searchText: String) {
        let predicate = #Predicate<Note> { note in
            searchText.isEmpty || note.title.localizedStandardContains(searchText)
        }
        _notes = Query(filter: predicate, sort: \.createdAt, order: .reverse)
    }

    var body: some View {
        List(notes) { note in
            Text(note.title)
        }
    }
}
```

### Query with Limit

```swift
@Query(sort: \Note.createdAt, order: .reverse)
var recentNotes: [Note]

// In view, limit manually
List(recentNotes.prefix(10)) { note in
    Text(note.title)
}
```

### Query Animations

```swift
@Query(sort: \Note.title, animation: .default)
var notes: [Note]
```

---

## ModelContext Operations

### Accessing Context

```swift
struct ContentView: View {
    @Environment(\.modelContext) private var modelContext

    // ...
}
```

### Creating Objects

```swift
func createNote() {
    let note = Note(title: "New Note")
    modelContext.insert(note)
    // Auto-saved on SwiftUI lifecycle events
}
```

### Explicit Save

```swift
func saveChanges() {
    do {
        try modelContext.save()
    } catch {
        print("Save failed: \(error)")
    }
}
```

### Deleting Objects

```swift
func deleteNote(_ note: Note) {
    modelContext.delete(note)
}

func deleteNotes(at offsets: IndexSet) {
    for index in offsets {
        modelContext.delete(notes[index])
    }
}
```

### Fetching with Descriptor

```swift
func fetchRecentNotes() throws -> [Note] {
    let descriptor = FetchDescriptor<Note>(
        predicate: #Predicate { $0.isPinned },
        sortBy: [SortDescriptor(\.createdAt, order: .reverse)]
    )
    return try modelContext.fetch(descriptor)
}

// With limit
func fetchTopNotes(limit: Int) throws -> [Note] {
    var descriptor = FetchDescriptor<Note>(
        sortBy: [SortDescriptor(\.createdAt, order: .reverse)]
    )
    descriptor.fetchLimit = limit
    return try modelContext.fetch(descriptor)
}
```

### Batch Operations

```swift
// Delete all matching predicate
try modelContext.delete(model: Note.self, where: #Predicate { note in
    note.createdAt < cutoffDate
})

// Enumerate for batch processing
let descriptor = FetchDescriptor<Note>()
try modelContext.enumerate(descriptor) { note in
    note.processedAt = Date()
}
```

---

## #Predicate Macro

### Basic Predicates

```swift
// Equality
#Predicate<Note> { $0.isPinned == true }

// Comparison
#Predicate<Note> { $0.createdAt > someDate }

// String contains
#Predicate<Note> { $0.title.contains("Swift") }

// Case-insensitive contains
#Predicate<Note> { $0.title.localizedStandardContains(searchText) }
```

### Compound Predicates

```swift
// AND
#Predicate<Note> { note in
    note.isPinned && note.title.contains("Important")
}

// OR
#Predicate<Note> { note in
    note.isPinned || note.folder?.name == "Favorites"
}

// NOT
#Predicate<Note> { note in
    !note.content.isEmpty
}
```

### Optional Handling

```swift
#Predicate<Note> { note in
    note.folder?.name == "Work"
}

// Check for nil
#Predicate<Note> { note in
    note.folder != nil
}
```

### Array Predicates

```swift
// Array contains
#Predicate<Note> { note in
    note.tags?.contains(where: { $0.name == "Important" }) ?? false
}

// Array is empty
#Predicate<Note> { note in
    note.tags?.isEmpty ?? true
}
```

---

## Model Inheritance (iOS 26)

### Base and Derived Models

```swift
@Model
class MediaItem {
    var title: String
    var createdAt: Date

    init(title: String) {
        self.title = title
        self.createdAt = Date()
    }
}

@Model
final class Photo: MediaItem {
    var imageData: Data?
    var resolution: String?

    init(title: String, imageData: Data?) {
        super.init(title: title)
        self.imageData = imageData
    }
}

@Model
final class Video: MediaItem {
    var duration: TimeInterval
    var thumbnailData: Data?

    init(title: String, duration: TimeInterval) {
        super.init(title: title)
        self.duration = duration
    }
}
```

### Polymorphic Queries

```swift
// Query all media items (photos and videos)
@Query var allMedia: [MediaItem]

// Query only photos
@Query var photos: [Photo]
```

---

## Background Operations

### Background Context

```swift
func importData() async {
    let container = modelContainer

    await Task.detached {
        let context = ModelContext(container)

        // Perform operations
        for item in largeDataSet {
            let note = Note(title: item.title)
            context.insert(note)
        }

        try? context.save()
    }.value
}
```

### Actor Isolation

```swift
@ModelActor
actor DataImporter {
    func importNotes(from data: [ImportData]) throws {
        for item in data {
            let note = Note(title: item.title, content: item.content)
            modelContext.insert(note)
        }
        try modelContext.save()
    }
}

// Usage
let importer = DataImporter(modelContainer: container)
try await importer.importNotes(from: importData)
```

---

## Migration

### Lightweight Migration (Automatic)

SwiftData handles lightweight migrations automatically:
- Adding new properties with defaults
- Removing properties
- Adding optional relationships

### Custom Migration

```swift
enum MySchemaV1: VersionedSchema {
    static var versionIdentifier = Schema.Version(1, 0, 0)

    static var models: [any PersistentModel.Type] {
        [Note.self]
    }

    @Model
    class Note {
        var title: String
        var content: String

        init(title: String, content: String) {
            self.title = title
            self.content = content
        }
    }
}

enum MySchemaV2: VersionedSchema {
    static var versionIdentifier = Schema.Version(2, 0, 0)

    static var models: [any PersistentModel.Type] {
        [Note.self]
    }

    @Model
    class Note {
        var title: String
        var content: String
        var createdAt: Date  // New property

        init(title: String, content: String) {
            self.title = title
            self.content = content
            self.createdAt = Date()
        }
    }
}

enum MyMigrationPlan: SchemaMigrationPlan {
    static var schemas: [any VersionedSchema.Type] {
        [MySchemaV1.self, MySchemaV2.self]
    }

    static var stages: [MigrationStage] {
        [migrateV1toV2]
    }

    static let migrateV1toV2 = MigrationStage.lightweight(
        fromVersion: MySchemaV1.self,
        toVersion: MySchemaV2.self
    )
}

// Use in container
let container = try ModelContainer(
    for: Note.self,
    migrationPlan: MyMigrationPlan.self
)
```

---

## Testing

### In-Memory Testing

```swift
import Testing
import SwiftData

@Test
func testNoteCreation() throws {
    let config = ModelConfiguration(isStoredInMemoryOnly: true)
    let container = try ModelContainer(for: Note.self, configurations: config)
    let context = ModelContext(container)

    let note = Note(title: "Test", content: "Content")
    context.insert(note)

    let descriptor = FetchDescriptor<Note>()
    let notes = try context.fetch(descriptor)

    #expect(notes.count == 1)
    #expect(notes.first?.title == "Test")
}
```

### SwiftUI Preview with Sample Data

```swift
@MainActor
let previewContainer: ModelContainer = {
    let config = ModelConfiguration(isStoredInMemoryOnly: true)
    let container = try! ModelContainer(for: Note.self, configurations: config)

    // Insert sample data
    let context = container.mainContext
    let sampleNotes = [
        Note(title: "First Note", content: "Content 1"),
        Note(title: "Second Note", content: "Content 2")
    ]
    sampleNotes.forEach { context.insert($0) }

    return container
}()

#Preview {
    NotesListView()
        .modelContainer(previewContainer)
}
```

---

## Best Practices

### 1. Design for iCloud from the Start

```swift
// GOOD: iCloud-compatible model
@Model
class Note {
    var title: String = ""
    var content: String = ""
    var folder: Folder?      // Optional relationship
    var tags: [Tag]?         // Optional array

    init(title: String = "") {
        self.title = title
    }
}

// AVOID: iCloud-incompatible
@Model
class Note {
    @Attribute(.unique) var id: String  // Not supported
    var folder: Folder                   // Non-optional relationship
}
```

### 2. Use @Query for Reactive Data

```swift
// GOOD: Reactive updates
@Query(sort: \Note.createdAt)
var notes: [Note]

// AVOID: Manual fetching in views
@State private var notes: [Note] = []
func loadNotes() {
    notes = try? context.fetch(FetchDescriptor<Note>())
}
```

### 3. Explicit Save for Critical Data

```swift
func saveImportantChange() {
    modelContext.insert(criticalData)
    do {
        try modelContext.save()
    } catch {
        // Handle error appropriately
    }
}
```

### 4. Use Background Contexts for Heavy Work

```swift
func importLargeDataset() async {
    await Task.detached {
        let context = ModelContext(container)
        // Heavy operations
        try? context.save()
    }.value
}
```

---

## Official Resources

- [SwiftData Documentation](https://developer.apple.com/documentation/swiftdata)
- [Syncing model data across devices](https://developer.apple.com/documentation/swiftdata/syncing-model-data-across-a-persons-devices)
- [WWDC23: Meet SwiftData](https://developer.apple.com/videos/play/wwdc2023/10187/)
- [WWDC23: Model your schema with SwiftData](https://developer.apple.com/videos/play/wwdc2023/10195/)
- [WWDC24: What's new in SwiftData](https://developer.apple.com/videos/play/wwdc2024/10137/)
