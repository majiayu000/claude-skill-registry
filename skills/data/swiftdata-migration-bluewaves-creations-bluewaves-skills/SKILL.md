---
name: swiftdata-migration
description: Advanced CoreData to SwiftData migration patterns, schema versioning strategies, conflict resolution for iCloud sync, and production migration workflows. Use when user asks about migrating from CoreData, SwiftData schema evolution, versioned migrations, iCloud conflict resolution, or production data migration.
allowed-tools: Bash, Read, Write, Edit
---

# SwiftData Migration Guide

Comprehensive guide for migrating from CoreData to SwiftData, managing schema versions, handling iCloud sync conflicts, and production-grade migration strategies.

## Prerequisites

- iOS 17+ for SwiftData (iOS 26 recommended)
- Xcode 26+
- Familiarity with existing CoreData stack (if migrating)

---

## CoreData to SwiftData Migration

### Migration Strategy Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    MIGRATION APPROACHES                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. COEXISTENCE (Recommended for large apps)                │
│     CoreData ←→ SwiftData running side-by-side              │
│     Gradual feature migration                                │
│                                                              │
│  2. COMPLETE MIGRATION (Smaller apps)                        │
│     CoreData → SwiftData one-time migration                  │
│     Requires downtime or careful orchestration               │
│                                                              │
│  3. FRESH START (New iCloud containers)                      │
│     New SwiftData store, export/import user data             │
│     Cleanest but requires user action                        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Step 1: Audit Your CoreData Model

Before migrating, analyze your existing model:

```swift
// CoreData Model Audit Checklist
/*
 ✓ List all entities and their attributes
 ✓ Document all relationships (to-one, to-many, many-to-many)
 ✓ Identify unique constraints
 ✓ Note transformable attributes and their types
 ✓ Check for derived attributes
 ✓ Review fetch request templates
 ✓ Audit NSManagedObject subclasses for custom logic
*/

// Example: Documenting CoreData entity
/*
 Entity: Note
 Attributes:
   - id: UUID (unique)
   - title: String (not optional)
   - content: String (optional)
   - createdAt: Date
   - isPinned: Bool (default: false)

 Relationships:
   - folder: Folder (to-one, optional, nullify)
   - tags: [Tag] (to-many, ordered)
*/
```

### Step 2: Create Equivalent SwiftData Models

```swift
import SwiftData

// BEFORE: CoreData NSManagedObject
/*
@objc(Note)
class Note: NSManagedObject {
    @NSManaged var id: UUID
    @NSManaged var title: String
    @NSManaged var content: String?
    @NSManaged var createdAt: Date
    @NSManaged var isPinned: Bool
    @NSManaged var folder: Folder?
    @NSManaged var tags: NSOrderedSet?
}
*/

// AFTER: SwiftData @Model
@Model
class Note {
    // SwiftData generates its own persistent ID
    // Don't use @Attribute(.unique) for iCloud compatibility
    var legacyID: UUID?  // Keep for migration reference

    var title: String = ""
    var content: String = ""
    var createdAt: Date = Date()
    var isPinned: Bool = false

    // Relationships MUST be optional for iCloud
    var folder: Folder?
    var tags: [Tag]?  // Use array, not NSOrderedSet

    init(title: String, content: String = "") {
        self.title = title
        self.content = content
        self.createdAt = Date()
    }
}
```

### Step 3: Data Migration Script

```swift
import CoreData
import SwiftData

actor DataMigrator {
    private let coreDataContainer: NSPersistentContainer
    private let swiftDataContainer: ModelContainer

    init(coreDataContainer: NSPersistentContainer, swiftDataContainer: ModelContainer) {
        self.coreDataContainer = coreDataContainer
        self.swiftDataContainer = swiftDataContainer
    }

    func migrateNotes(progressHandler: @escaping (Double) -> Void) async throws {
        let context = coreDataContainer.viewContext
        let swiftDataContext = ModelContext(swiftDataContainer)

        // Fetch all CoreData notes
        let fetchRequest = NSFetchRequest<NSManagedObject>(entityName: "Note")
        fetchRequest.sortDescriptors = [NSSortDescriptor(key: "createdAt", ascending: true)]

        let coreDataNotes = try context.fetch(fetchRequest)
        let totalCount = Double(coreDataNotes.count)

        for (index, cdNote) in coreDataNotes.enumerated() {
            // Map CoreData object to SwiftData model
            let note = Note(
                title: cdNote.value(forKey: "title") as? String ?? "",
                content: cdNote.value(forKey: "content") as? String ?? ""
            )
            note.legacyID = cdNote.value(forKey: "id") as? UUID
            note.createdAt = cdNote.value(forKey: "createdAt") as? Date ?? Date()
            note.isPinned = cdNote.value(forKey: "isPinned") as? Bool ?? false

            swiftDataContext.insert(note)

            // Save in batches to avoid memory pressure
            if index % 100 == 0 {
                try swiftDataContext.save()
                progressHandler(Double(index) / totalCount)
            }
        }

        try swiftDataContext.save()
        progressHandler(1.0)
    }
}
```

### Step 4: Coexistence Pattern

For gradual migration, run both stacks:

```swift
@main
struct MyApp: App {
    // CoreData stack for legacy features
    let coreDataController = CoreDataController.shared

    // SwiftData for new features
    let swiftDataContainer: ModelContainer

    init() {
        let schema = Schema([Note.self, Folder.self, Tag.self])
        let config = ModelConfiguration(
            schema: schema,
            cloudKitDatabase: .automatic
        )

        do {
            swiftDataContainer = try ModelContainer(for: schema, configurations: config)
        } catch {
            fatalError("SwiftData init failed: \(error)")
        }
    }

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(\.managedObjectContext, coreDataController.viewContext)
                .modelContainer(swiftDataContainer)
        }
    }
}

// Feature flag for gradual rollout
enum DataStoreFeature {
    static var useSwiftData: Bool {
        // Check if migration is complete
        UserDefaults.standard.bool(forKey: "swiftDataMigrationComplete")
    }
}
```

---

## Schema Versioning

### Versioned Schema Definition

```swift
// Version 1: Initial schema
enum NotesSchemaV1: VersionedSchema {
    static var versionIdentifier = Schema.Version(1, 0, 0)

    static var models: [any PersistentModel.Type] {
        [Note.self]
    }

    @Model
    class Note {
        var title: String = ""
        var content: String = ""
        var createdAt: Date = Date()

        init(title: String) {
            self.title = title
        }
    }
}

// Version 2: Add isPinned and folder relationship
enum NotesSchemaV2: VersionedSchema {
    static var versionIdentifier = Schema.Version(2, 0, 0)

    static var models: [any PersistentModel.Type] {
        [Note.self, Folder.self]
    }

    @Model
    class Note {
        var title: String = ""
        var content: String = ""
        var createdAt: Date = Date()
        var isPinned: Bool = false  // NEW
        var folder: Folder?         // NEW

        init(title: String) {
            self.title = title
        }
    }

    @Model
    class Folder {
        var name: String = ""
        @Relationship(inverse: \Note.folder)
        var notes: [Note]?

        init(name: String) {
            self.name = name
        }
    }
}

// Version 3: Add tags with many-to-many
enum NotesSchemaV3: VersionedSchema {
    static var versionIdentifier = Schema.Version(3, 0, 0)

    static var models: [any PersistentModel.Type] {
        [Note.self, Folder.self, Tag.self]
    }

    @Model
    class Note {
        var title: String = ""
        var content: String = ""
        var createdAt: Date = Date()
        var isPinned: Bool = false
        var folder: Folder?
        var tags: [Tag]?  // NEW

        init(title: String) {
            self.title = title
        }
    }

    @Model
    class Folder {
        var name: String = ""
        @Relationship(inverse: \Note.folder)
        var notes: [Note]?

        init(name: String) {
            self.name = name
        }
    }

    @Model
    class Tag {
        var name: String = ""
        @Relationship(inverse: \Note.tags)
        var notes: [Note]?

        init(name: String) {
            self.name = name
        }
    }
}
```

### Migration Plan

```swift
enum NotesMigrationPlan: SchemaMigrationPlan {
    static var schemas: [any VersionedSchema.Type] {
        [NotesSchemaV1.self, NotesSchemaV2.self, NotesSchemaV3.self]
    }

    static var stages: [MigrationStage] {
        [migrateV1toV2, migrateV2toV3]
    }

    // Lightweight migration (no data transformation)
    static let migrateV1toV2 = MigrationStage.lightweight(
        fromVersion: NotesSchemaV1.self,
        toVersion: NotesSchemaV2.self
    )

    // Custom migration with data transformation
    static let migrateV2toV3 = MigrationStage.custom(
        fromVersion: NotesSchemaV2.self,
        toVersion: NotesSchemaV3.self,
        willMigrate: { context in
            // Pre-migration: Clean up orphaned data
            let descriptor = FetchDescriptor<NotesSchemaV2.Note>(
                predicate: #Predicate { $0.title.isEmpty }
            )
            let emptyNotes = try context.fetch(descriptor)
            for note in emptyNotes {
                context.delete(note)
            }
            try context.save()
        },
        didMigrate: { context in
            // Post-migration: Set default values or transform data
            let descriptor = FetchDescriptor<NotesSchemaV3.Note>()
            let notes = try context.fetch(descriptor)

            // Create default "Untagged" tag for notes without tags
            let untaggedTag = NotesSchemaV3.Tag(name: "Untagged")
            context.insert(untaggedTag)

            for note in notes where note.tags?.isEmpty ?? true {
                note.tags = [untaggedTag]
            }

            try context.save()
        }
    )
}

// Use migration plan in container
let container = try ModelContainer(
    for: NotesSchemaV3.Note.self, NotesSchemaV3.Folder.self, NotesSchemaV3.Tag.self,
    migrationPlan: NotesMigrationPlan.self
)
```

---

## iCloud Sync Conflict Resolution

### Understanding Sync Conflicts

```
┌─────────────────────────────────────────────────────────────┐
│                   iCLOUD SYNC TIMELINE                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Device A: Edit note.title = "Hello"    ──────┐             │
│                                                │ CONFLICT!   │
│  Device B: Edit note.title = "World"    ──────┘             │
│                                                              │
│  CloudKit Resolution: LAST WRITER WINS                       │
│  (Based on modificationDate)                                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Strategy 1: Last-Writer-Wins (Default)

```swift
@Model
class Note {
    var title: String = ""
    var content: String = ""

    // CloudKit uses this for conflict resolution
    var modificationDate: Date = Date()

    func update(title: String) {
        self.title = title
        self.modificationDate = Date()  // Update timestamp
    }
}
```

### Strategy 2: Field-Level Merge

```swift
@Model
class Note {
    var title: String = ""
    var content: String = ""

    // Track individual field modifications
    var titleModifiedAt: Date = Date()
    var contentModifiedAt: Date = Date()

    func updateTitle(_ newTitle: String) {
        title = newTitle
        titleModifiedAt = Date()
    }

    func updateContent(_ newContent: String) {
        content = newContent
        contentModifiedAt = Date()
    }

    // Merge conflicting versions
    func merge(with other: Note) {
        if other.titleModifiedAt > self.titleModifiedAt {
            self.title = other.title
            self.titleModifiedAt = other.titleModifiedAt
        }
        if other.contentModifiedAt > self.contentModifiedAt {
            self.content = other.content
            self.contentModifiedAt = other.contentModifiedAt
        }
    }
}
```

### Strategy 3: Operational Transformation for Text

```swift
@Model
class CollaborativeNote {
    var title: String = ""

    // Store operations instead of final state
    @Attribute(.externalStorage)
    var operationsData: Data?

    // Computed content from operations
    @Transient
    var content: String = ""

    struct Operation: Codable {
        enum Kind: Codable {
            case insert(position: Int, text: String)
            case delete(range: Range<Int>)
        }
        let kind: Kind
        let timestamp: Date
        let deviceID: String
    }

    var operations: [Operation] {
        get {
            guard let data = operationsData else { return [] }
            return (try? JSONDecoder().decode([Operation].self, from: data)) ?? []
        }
        set {
            operationsData = try? JSONEncoder().encode(newValue)
        }
    }

    func applyOperations() {
        var text = ""
        let sortedOps = operations.sorted { $0.timestamp < $1.timestamp }

        for op in sortedOps {
            switch op.kind {
            case .insert(let position, let insertText):
                let index = text.index(text.startIndex, offsetBy: min(position, text.count))
                text.insert(contentsOf: insertText, at: index)
            case .delete(let range):
                let start = text.index(text.startIndex, offsetBy: range.lowerBound)
                let end = text.index(text.startIndex, offsetBy: min(range.upperBound, text.count))
                text.removeSubrange(start..<end)
            }
        }

        content = text
    }
}
```

### Strategy 4: Soft Deletes for Conflict Prevention

```swift
@Model
class Note {
    var title: String = ""
    var content: String = ""

    // Soft delete instead of hard delete
    var isDeleted: Bool = false
    var deletedAt: Date?
    var deletedBy: String?  // Device identifier

    func softDelete(deviceID: String) {
        isDeleted = true
        deletedAt = Date()
        deletedBy = deviceID
    }

    func restore() {
        isDeleted = false
        deletedAt = nil
        deletedBy = nil
    }
}

// Query only active notes
@Query(filter: #Predicate<Note> { !$0.isDeleted })
var activeNotes: [Note]

// Periodically purge soft-deleted items
func purgeDeletedNotes(olderThan days: Int, context: ModelContext) throws {
    let cutoff = Calendar.current.date(byAdding: .day, value: -days, to: Date())!

    try context.delete(model: Note.self, where: #Predicate { note in
        note.isDeleted && (note.deletedAt ?? Date()) < cutoff
    })
}
```

### Monitoring Sync Status

```swift
import Combine

@Observable
class SyncMonitor {
    var syncState: SyncState = .idle
    var lastSyncDate: Date?
    var pendingChanges: Int = 0

    enum SyncState {
        case idle
        case syncing
        case error(String)
    }

    private var cancellables = Set<AnyCancellable>()

    init() {
        // Monitor CloudKit account status
        NotificationCenter.default.publisher(for: .CKAccountChanged)
            .sink { [weak self] _ in
                Task { await self?.checkAccountStatus() }
            }
            .store(in: &cancellables)

        // Monitor remote changes
        NotificationCenter.default.publisher(
            for: NSPersistentStoreRemoteChange
        )
        .sink { [weak self] notification in
            self?.handleRemoteChange(notification)
        }
        .store(in: &cancellables)
    }

    private func checkAccountStatus() async {
        // Check iCloud availability
    }

    private func handleRemoteChange(_ notification: Notification) {
        lastSyncDate = Date()
        syncState = .idle
    }
}
```

---

## Production Migration Workflow

### Pre-Migration Checklist

```swift
struct MigrationPreflight {

    /// Verify device has sufficient storage
    static func checkStorage() throws {
        let fileManager = FileManager.default
        let documentDirectory = fileManager.urls(for: .documentDirectory, in: .userDomainMask).first!

        let values = try documentDirectory.resourceValues(forKeys: [.volumeAvailableCapacityForImportantUsageKey])
        let availableBytes = values.volumeAvailableCapacityForImportantUsage ?? 0

        // Require at least 500MB for migration
        guard availableBytes > 500_000_000 else {
            throw MigrationError.insufficientStorage
        }
    }

    /// Backup current data before migration
    static func backupCoreDataStore() throws -> URL {
        let fileManager = FileManager.default
        let storeURL = CoreDataController.shared.persistentStoreURL

        let backupDirectory = fileManager.urls(for: .documentDirectory, in: .userDomainMask).first!
            .appendingPathComponent("Backups")

        try fileManager.createDirectory(at: backupDirectory, withIntermediateDirectories: true)

        let backupURL = backupDirectory
            .appendingPathComponent("CoreData_\(Date().ISO8601Format()).sqlite")

        try fileManager.copyItem(at: storeURL, to: backupURL)

        // Also backup -wal and -shm files if they exist
        let walURL = storeURL.appendingPathExtension("wal")
        let shmURL = storeURL.appendingPathExtension("shm")

        if fileManager.fileExists(atPath: walURL.path) {
            try fileManager.copyItem(at: walURL, to: backupURL.appendingPathExtension("wal"))
        }
        if fileManager.fileExists(atPath: shmURL.path) {
            try fileManager.copyItem(at: shmURL, to: backupURL.appendingPathExtension("shm"))
        }

        return backupURL
    }

    /// Verify data integrity before migration
    static func validateCoreDataIntegrity() async throws -> ValidationReport {
        let context = CoreDataController.shared.viewContext

        var report = ValidationReport()

        // Count all entities
        let notesFetch = NSFetchRequest<NSManagedObject>(entityName: "Note")
        report.notesCount = try context.count(for: notesFetch)

        let foldersFetch = NSFetchRequest<NSManagedObject>(entityName: "Folder")
        report.foldersCount = try context.count(for: foldersFetch)

        // Check for orphaned relationships
        let orphanedNotes = try context.fetch(notesFetch).filter { note in
            let folder = note.value(forKey: "folder") as? NSManagedObject
            return folder?.isDeleted ?? false
        }
        report.orphanedRelationships = orphanedNotes.count

        return report
    }
}

struct ValidationReport {
    var notesCount: Int = 0
    var foldersCount: Int = 0
    var orphanedRelationships: Int = 0

    var isValid: Bool {
        orphanedRelationships == 0
    }
}

enum MigrationError: LocalizedError {
    case insufficientStorage
    case backupFailed
    case validationFailed
    case migrationInterrupted

    var errorDescription: String? {
        switch self {
        case .insufficientStorage:
            return "Not enough storage space for migration. Please free up at least 500MB."
        case .backupFailed:
            return "Failed to create backup. Migration aborted."
        case .validationFailed:
            return "Data validation failed. Please contact support."
        case .migrationInterrupted:
            return "Migration was interrupted. Your data is safe in the backup."
        }
    }
}
```

### Migration UI

```swift
struct MigrationView: View {
    @State private var migrationState: MigrationState = .notStarted
    @State private var progress: Double = 0
    @State private var error: MigrationError?

    enum MigrationState {
        case notStarted
        case preparingBackup
        case validating
        case migrating
        case verifying
        case completed
        case failed
    }

    var body: some View {
        VStack(spacing: 24) {
            Image(systemName: stateIcon)
                .font(.system(size: 60))
                .foregroundStyle(stateColor)

            Text(stateTitle)
                .font(.title2.bold())

            Text(stateDescription)
                .foregroundStyle(.secondary)
                .multilineTextAlignment(.center)

            if migrationState == .migrating {
                ProgressView(value: progress)
                    .progressViewStyle(.linear)

                Text("\(Int(progress * 100))%")
                    .font(.caption)
                    .foregroundStyle(.secondary)
            }

            if case .notStarted = migrationState {
                Button("Start Migration") {
                    Task { await startMigration() }
                }
                .buttonStyle(.borderedProminent)
            }

            if case .completed = migrationState {
                Button("Continue to App") {
                    UserDefaults.standard.set(true, forKey: "swiftDataMigrationComplete")
                }
                .buttonStyle(.borderedProminent)
            }

            if let error {
                Text(error.localizedDescription)
                    .foregroundStyle(.red)
                    .font(.caption)
            }
        }
        .padding()
    }

    private func startMigration() async {
        do {
            // Step 1: Backup
            migrationState = .preparingBackup
            _ = try MigrationPreflight.backupCoreDataStore()

            // Step 2: Validate
            migrationState = .validating
            let report = try await MigrationPreflight.validateCoreDataIntegrity()
            guard report.isValid else {
                throw MigrationError.validationFailed
            }

            // Step 3: Migrate
            migrationState = .migrating
            // ... migration logic with progress updates

            // Step 4: Verify
            migrationState = .verifying
            // ... verification logic

            migrationState = .completed

        } catch let migrationError as MigrationError {
            error = migrationError
            migrationState = .failed
        } catch {
            self.error = .migrationInterrupted
            migrationState = .failed
        }
    }

    private var stateIcon: String {
        switch migrationState {
        case .notStarted: return "arrow.triangle.2.circlepath"
        case .preparingBackup: return "externaldrive.badge.timemachine"
        case .validating: return "checkmark.shield"
        case .migrating: return "arrow.right.arrow.left"
        case .verifying: return "magnifyingglass"
        case .completed: return "checkmark.circle.fill"
        case .failed: return "xmark.circle.fill"
        }
    }

    private var stateColor: Color {
        switch migrationState {
        case .completed: return .green
        case .failed: return .red
        default: return .blue
        }
    }

    private var stateTitle: String {
        switch migrationState {
        case .notStarted: return "Ready to Migrate"
        case .preparingBackup: return "Creating Backup..."
        case .validating: return "Validating Data..."
        case .migrating: return "Migrating..."
        case .verifying: return "Verifying..."
        case .completed: return "Migration Complete!"
        case .failed: return "Migration Failed"
        }
    }

    private var stateDescription: String {
        switch migrationState {
        case .notStarted:
            return "We'll upgrade your data to the new format. This may take a few minutes."
        case .preparingBackup:
            return "Creating a backup of your data..."
        case .validating:
            return "Checking data integrity..."
        case .migrating:
            return "Transferring your notes to the new format..."
        case .verifying:
            return "Making sure everything transferred correctly..."
        case .completed:
            return "Your data has been successfully migrated!"
        case .failed:
            return "Something went wrong. Your original data is safe."
        }
    }
}
```

---

## Best Practices Summary

### DO

```swift
// ✓ Version your schemas from day one
enum MySchemaV1: VersionedSchema { ... }

// ✓ Use lightweight migrations when possible
MigrationStage.lightweight(fromVersion: V1.self, toVersion: V2.self)

// ✓ Design models for iCloud from the start
var folder: Folder?  // Optional relationships

// ✓ Keep legacy IDs for reference during migration
var legacyID: UUID?

// ✓ Create backups before migration
try MigrationPreflight.backupCoreDataStore()

// ✓ Use soft deletes for iCloud sync
var isDeleted: Bool = false
```

### DON'T

```swift
// ✗ Don't use unique constraints with iCloud
@Attribute(.unique) var id: String  // NOT iCloud compatible

// ✗ Don't delete properties after shipping
// Instead, keep them but stop using them

// ✗ Don't change property types
var count: Int  // Can't change to String later

// ✗ Don't force-unwrap migrated data
let title = note.title!  // Could be nil during migration

// ✗ Don't skip validation
try container.mainContext.save()  // Always validate first
```

---

## Official Resources

- [SwiftData Documentation](https://developer.apple.com/documentation/swiftdata)
- [Adopting SwiftData for a Core Data app](https://developer.apple.com/documentation/coredata/adopting-swiftdata-for-a-core-data-app)
- [WWDC24: Create a custom data store with SwiftData](https://developer.apple.com/videos/play/wwdc2024/10138/)
- [WWDC23: Migrate to SwiftData](https://developer.apple.com/videos/play/wwdc2023/10189/)
