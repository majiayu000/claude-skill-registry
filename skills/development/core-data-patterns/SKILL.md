---
name: core-data-patterns
description: "Expert Core Data decisions for iOS/tvOS: when Core Data vs alternatives, context architecture for multi-threading, migration strategy selection, and performance optimization trade-offs. Use when choosing persistence layer, debugging save failures, or optimizing fetch performance. Trigger keywords: Core Data, NSManagedObject, NSPersistentContainer, NSFetchRequest, FetchRequest, migration, lightweight migration, background context, merge policy, faulting"
version: "3.0.0"
---

# Core Data Patterns — Expert Decisions

Expert decision frameworks for Core Data choices. Claude knows NSPersistentContainer and fetch requests — this skill provides judgment calls for when Core Data fits and architecture trade-offs.

---

## Decision Trees

### Core Data vs Alternatives

```
What's your persistence need?
├─ Simple key-value storage
│  └─ UserDefaults or @AppStorage
│     Don't use Core Data for preferences
│
├─ Flat list of Codable objects
│  └─ Is query complexity needed?
│     ├─ NO → File-based (JSON/Plist) or SwiftData
│     └─ YES → Core Data or SQLite
│
├─ Complex relationships + queries
│  └─ How many objects?
│     ├─ < 10,000 → SwiftData (simpler) or Core Data
│     └─ > 10,000 → Core Data (more control)
│
├─ iCloud sync required
│  └─ NSPersistentCloudKitContainer
│     Built-in sync with Core Data
│
└─ Cross-platform (non-Apple)
   └─ SQLite directly or Realm
      Core Data is Apple-only
```

**The trap**: Using Core Data for simple lists. If you don't need relationships, queries, or undo, consider simpler options like SwiftData or file storage.

### Context Architecture

```
How many contexts do you need?
├─ Simple app, UI-only operations
│  └─ viewContext only
│     Single context for reads and small writes
│
├─ Background imports/exports
│  └─ viewContext + newBackgroundContext()
│     Background for writes, viewContext for UI
│
├─ Complex with multiple writers
│  └─ Parent-child context hierarchy
│     Rarely needed — adds complexity
│
└─ Sync with server
   └─ Dedicated sync context
      performBackgroundTask for sync operations
```

### Migration Strategy

```
What changed in your model?
├─ Added optional attribute
│  └─ Lightweight migration (automatic)
│
├─ Renamed attribute/entity
│  └─ Lightweight with mapping model hints
│     Set renaming identifier in model
│
├─ Changed attribute type
│  └─ Depends on conversion possibility
│     Int → String: lightweight
│     String → Date: may need custom
│
├─ Added required attribute (no default)
│  └─ Custom migration required
│     Or add default value to make lightweight
│
└─ Complex schema restructuring
   └─ Staged migration
      Multiple model versions, migrate step by step
```

### Merge Policy Selection

```
What happens on save conflicts?
├─ UI context always wins
│  └─ NSMergeByPropertyObjectTrumpMergePolicy
│     Most common for view context
│
├─ Store (persisted) always wins
│  └─ NSMergeByPropertyStoreTrumpMergePolicy
│     For background sync contexts
│
├─ Need custom resolution
│  └─ Custom merge policy
│     Complex — avoid if possible
│
└─ Fail on conflict
   └─ NSErrorMergePolicy (default)
      Rarely want this
```

---

## NEVER Do

### Context Management

**NEVER** use viewContext for heavy operations:
```swift
// ❌ Blocks main thread during import
func importUsers(_ data: [UserData]) {
    let context = persistenceController.container.viewContext
    for item in data {
        let user = User(context: context)
        user.name = item.name
    }
    try? context.save()  // UI frozen!
}

// ✅ Use background context
func importUsers(_ data: [UserData]) async throws {
    try await persistenceController.container.performBackgroundTask { context in
        for item in data {
            let user = User(context: context)
            user.name = item.name
        }
        try context.save()
    }
}
```

**NEVER** pass NSManagedObjects between contexts:
```swift
// ❌ Object belongs to different context — crash or undefined behavior
let user = fetchUser(in: backgroundContext)
viewContext.delete(user)  // Wrong context!

// ✅ Re-fetch in target context using objectID
let user = fetchUser(in: backgroundContext)
let userInViewContext = viewContext.object(with: user.objectID) as! User
viewContext.delete(userInViewContext)
```

**NEVER** access managed objects off their context's queue:
```swift
// ❌ Thread violation — data corruption possible
let user = fetchUser(in: backgroundContext)
DispatchQueue.main.async {
    print(user.name)  // Accessing background object on main thread!
}

// ✅ Use context.perform for thread-safe access
backgroundContext.perform {
    let user = fetchUser(in: backgroundContext)
    let name = user.name
    DispatchQueue.main.async {
        print(name)  // Safe — using local copy
    }
}
```

### Save Operations

**NEVER** ignore save errors:
```swift
// ❌ Silent data loss
try? context.save()

// ✅ Handle errors properly
do {
    try context.save()
} catch {
    context.rollback()
    Logger.coreData.error("Save failed: \(error)")
    throw error
}
```

**NEVER** save after every single change:
```swift
// ❌ Performance disaster — disk I/O per object
for item in largeDataset {
    let entity = Entity(context: context)
    entity.value = item
    try context.save()  // 10,000 saves!
}

// ✅ Batch changes, save once (or periodically)
for (index, item) in largeDataset.enumerated() {
    let entity = Entity(context: context)
    entity.value = item

    // Save every 1000 objects to manage memory
    if index % 1000 == 0 {
        try context.save()
        context.reset()  // Release memory
    }
}
try context.save()  // Final batch
```

**NEVER** call save on context with no changes:
```swift
// ❌ Unnecessary disk I/O
func periodicSave() {
    try? context.save()  // No-op but still has overhead
}

// ✅ Check for changes first
func saveIfNeeded() throws {
    guard context.hasChanges else { return }
    try context.save()
}
```

### Fetch Optimization

**NEVER** fetch all objects when you need a count:
```swift
// ❌ Loads all objects into memory just to count
let users = try context.fetch(User.fetchRequest())
let count = users.count  // May fetch thousands!

// ✅ Use count fetch
let request = User.fetchRequest()
let count = try context.count(for: request)
```

**NEVER** fetch everything without limits:
```swift
// ❌ May load entire database
let request = User.fetchRequest()
let allUsers = try context.fetch(request)

// ✅ Set appropriate limits
let request = User.fetchRequest()
request.fetchLimit = 50
request.fetchBatchSize = 20  // Loads in batches
```

**NEVER** forget to prefetch relationships you'll access:
```swift
// ❌ N+1 problem — each post access triggers fault
let request = User.fetchRequest()
let users = try context.fetch(request)
for user in users {
    print(user.posts.count)  // Separate fetch per user!
}

// ✅ Prefetch relationships
let request = User.fetchRequest()
request.relationshipKeyPathsForPrefetching = ["posts"]
let users = try context.fetch(request)
```

### Migration

**NEVER** assume lightweight migration will work:
```swift
// ❌ Crashes on incompatible changes
container.loadPersistentStores { _, error in
    if let error = error {
        fatalError("Failed: \(error)")  // User data lost!
    }
}

// ✅ Handle migration failure gracefully
container.loadPersistentStores { description, error in
    if let error = error as NSError? {
        if error.code == NSMigrationMissingSourceModelError {
            // Offer data reset or crash gracefully
            Self.resetStore()
        }
    }
}
```

---

## Essential Patterns

### Modern Persistence Controller

```swift
@MainActor
final class PersistenceController {
    static let shared = PersistenceController()
    static let preview = PersistenceController(inMemory: true)

    let container: NSPersistentContainer

    init(inMemory: Bool = false) {
        container = NSPersistentContainer(name: "Model")

        if inMemory {
            container.persistentStoreDescriptions.first?.url = URL(fileURLWithPath: "/dev/null")
        }

        // Enable lightweight migration
        let description = container.persistentStoreDescriptions.first
        description?.shouldMigrateStoreAutomatically = true
        description?.shouldInferMappingModelAutomatically = true

        container.loadPersistentStores { _, error in
            if let error = error {
                // In production: log and handle gracefully
                fatalError("Core Data load failed: \(error)")
            }
        }

        // View context configuration
        container.viewContext.automaticallyMergesChangesFromParent = true
        container.viewContext.mergePolicy = NSMergeByPropertyObjectTrumpMergePolicy
        container.viewContext.undoManager = nil  // Disable if not needed
    }

    func saveViewContext() {
        let context = container.viewContext
        guard context.hasChanges else { return }

        do {
            try context.save()
        } catch {
            Logger.coreData.error("View context save failed: \(error)")
        }
    }
}
```

### Background Import Pattern

```swift
extension PersistenceController {
    func importData<T: Decodable>(
        _ items: [T],
        transform: @escaping (T, NSManagedObjectContext) -> Void
    ) async throws {
        try await container.performBackgroundTask { context in
            context.mergePolicy = NSMergeByPropertyObjectTrumpMergePolicy

            for (index, item) in items.enumerated() {
                transform(item, context)

                // Batch save to manage memory
                if index > 0 && index % 500 == 0 {
                    try context.save()
                    context.reset()
                }
            }

            if context.hasChanges {
                try context.save()
            }
        }
    }
}

// Usage
try await persistenceController.importData(userDTOs) { dto, context in
    let user = User(context: context)
    user.id = dto.id
    user.name = dto.name
}
```

### Efficient Fetch with @FetchRequest

```swift
struct UserListView: View {
    // Basic fetch — automatically updates on changes
    @FetchRequest(
        sortDescriptors: [SortDescriptor(\.name)],
        animation: .default
    )
    private var users: FetchedResults<User>

    var body: some View {
        List(users) { user in
            Text(user.name ?? "Unknown")
        }
    }
}

// Dynamic predicate fetch
struct FilteredUserList: View {
    @FetchRequest private var users: FetchedResults<User>

    init(searchText: String) {
        _users = FetchRequest(
            sortDescriptors: [SortDescriptor(\.name)],
            predicate: searchText.isEmpty ? nil : NSPredicate(
                format: "name CONTAINS[cd] %@", searchText
            ),
            animation: .default
        )
    }

    var body: some View {
        List(users) { user in
            Text(user.name ?? "")
        }
    }
}
```

---

## Quick Reference

### Core Data vs Alternatives

| Need | Solution |
|------|----------|
| Simple preferences | UserDefaults |
| Small Codable lists | JSON file or SwiftData |
| Complex queries + relationships | Core Data |
| iCloud sync | NSPersistentCloudKitContainer |
| Cross-platform | SQLite or Realm |

### Context Types

| Context | Use For | Thread |
|---------|---------|--------|
| viewContext | UI reads, small writes | Main |
| newBackgroundContext() | Heavy writes, imports | Background |
| performBackgroundTask | One-off background work | Background |

### Merge Policies

| Policy | Winner | Use Case |
|--------|--------|----------|
| ObjectTrump | In-memory changes | View context |
| StoreTrump | Persisted data | Sync context |
| ErrorMerge | Neither (fails) | Rarely wanted |

### Lightweight Migration Support

| Change | Automatic? |
|--------|------------|
| Add optional attribute | ✅ Yes |
| Add attribute with default | ✅ Yes |
| Remove attribute | ✅ Yes |
| Rename (with identifier) | ✅ Yes |
| Change type (compatible) | ✅ Maybe |
| Add required (no default) | ❌ No |
| Change relationship type | ❌ No |

### Red Flags

| Smell | Problem | Fix |
|-------|---------|-----|
| viewContext for imports | Main thread blocked | Use background context |
| NSManagedObject across contexts | Wrong thread access | Re-fetch via objectID |
| try? context.save() | Silent data loss | Handle errors |
| Save per object in loop | Disk I/O explosion | Batch saves |
| fetch() for count | Memory waste | context.count(for:) |
| No fetchLimit | Loads entire DB | Set reasonable limits |
| Missing prefetch | N+1 fetches | relationshipKeyPathsForPrefetching |
