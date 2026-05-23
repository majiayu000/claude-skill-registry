---
name: spotlight-discovery
description: CoreSpotlight for content indexing, NSUserActivity for handoff and search, and making app content discoverable. Use when user asks about Spotlight search, CoreSpotlight, NSUserActivity, content indexing, or app discoverability.
allowed-tools: Bash, Read, Write, Edit
---

# Spotlight and Content Discovery

Comprehensive guide to CoreSpotlight for content indexing, NSUserActivity for handoff and search, and making your app's content discoverable in iOS 26.

## Prerequisites

- iOS 9+ for CoreSpotlight (iOS 26 recommended)
- Xcode 26+

---

## Overview

### Two Indexing Approaches

1. **CoreSpotlight** - Index any content at any time (comprehensive)
2. **NSUserActivity** - Index content user actually views (usage-based)

### When to Use Each

| Feature | CoreSpotlight | NSUserActivity |
|---------|--------------|----------------|
| Timing | Any time | When user views content |
| Scope | All content | Viewed content |
| Handoff | No | Yes |
| Web indexing | No | Yes |
| Ranking | Default | Usage-boosted |

---

## CoreSpotlight

### Import

```swift
import CoreSpotlight
import MobileCoreServices
```

### Basic Indexing

```swift
import CoreSpotlight

func indexNote(_ note: Note) {
    // Create searchable item attributes
    let attributes = CSSearchableItemAttributeSet(contentType: .text)
    attributes.title = note.title
    attributes.contentDescription = note.content
    attributes.lastUsedDate = note.modifiedAt
    attributes.keywords = note.tags

    // Optional: thumbnail
    if let thumbnailData = note.thumbnailData {
        attributes.thumbnailData = thumbnailData
    }

    // Create searchable item
    let item = CSSearchableItem(
        uniqueIdentifier: note.id.uuidString,
        domainIdentifier: "com.yourapp.notes",
        attributeSet: attributes
    )

    // Optional: Set expiration
    item.expirationDate = Date().addingTimeInterval(30 * 24 * 60 * 60) // 30 days

    // Index the item
    CSSearchableIndex.default().indexSearchableItems([item]) { error in
        if let error {
            print("Indexing failed: \(error)")
        }
    }
}
```

### Async Indexing

```swift
func indexNote(_ note: Note) async throws {
    let attributes = CSSearchableItemAttributeSet(contentType: .text)
    attributes.title = note.title
    attributes.contentDescription = note.content

    let item = CSSearchableItem(
        uniqueIdentifier: note.id.uuidString,
        domainIdentifier: "com.yourapp.notes",
        attributeSet: attributes
    )

    try await CSSearchableIndex.default().indexSearchableItems([item])
}
```

### Batch Indexing

```swift
func indexAllNotes(_ notes: [Note]) async throws {
    let items = notes.map { note -> CSSearchableItem in
        let attributes = CSSearchableItemAttributeSet(contentType: .text)
        attributes.title = note.title
        attributes.contentDescription = note.content
        attributes.lastUsedDate = note.modifiedAt

        return CSSearchableItem(
            uniqueIdentifier: note.id.uuidString,
            domainIdentifier: "com.yourapp.notes",
            attributeSet: attributes
        )
    }

    try await CSSearchableIndex.default().indexSearchableItems(items)
}
```

### Rich Attribute Set

```swift
func createRichAttributes(for note: Note) -> CSSearchableItemAttributeSet {
    let attributes = CSSearchableItemAttributeSet(contentType: .text)

    // Basic info
    attributes.title = note.title
    attributes.contentDescription = note.content
    attributes.displayName = note.title

    // Dates
    attributes.contentCreationDate = note.createdAt
    attributes.contentModificationDate = note.modifiedAt
    attributes.lastUsedDate = note.lastViewedAt

    // Keywords and categorization
    attributes.keywords = note.tags
    attributes.subject = note.category

    // Media (if applicable)
    if let imageData = note.thumbnailData {
        attributes.thumbnailData = imageData
    }

    // Contact info (for contact-related content)
    attributes.authorNames = [note.author]
    attributes.authorEmailAddresses = [note.authorEmail]

    // Location (if applicable)
    if let location = note.location {
        attributes.latitude = location.latitude as NSNumber
        attributes.longitude = location.longitude as NSNumber
        attributes.namedLocation = location.name
    }

    // Custom attributes
    attributes.identifier = note.id.uuidString
    attributes.relatedUniqueIdentifier = note.folder?.id.uuidString

    return attributes
}
```

### Deleting from Index

```swift
// Delete specific item
func deleteFromIndex(noteId: UUID) async throws {
    try await CSSearchableIndex.default().deleteSearchableItems(
        withIdentifiers: [noteId.uuidString]
    )
}

// Delete by domain
func deleteAllNotes() async throws {
    try await CSSearchableIndex.default().deleteSearchableItems(
        withDomainIdentifiers: ["com.yourapp.notes"]
    )
}

// Delete all indexed content
func deleteAllIndexedContent() async throws {
    try await CSSearchableIndex.default().deleteAllSearchableItems()
}
```

### Updating Index

```swift
func updateNoteInIndex(_ note: Note) async throws {
    // Simply re-index with same identifier
    // CoreSpotlight replaces existing item
    try await indexNote(note)
}
```

---

## NSUserActivity

### Basic Setup

```swift
import UIKit

class NoteViewController: UIViewController {
    var note: Note!

    override func viewDidAppear(_ animated: Bool) {
        super.viewDidAppear(animated)
        setupUserActivity()
    }

    func setupUserActivity() {
        let activity = NSUserActivity(activityType: "com.yourapp.viewNote")

        // Basic properties
        activity.title = note.title
        activity.userInfo = ["noteId": note.id.uuidString]

        // Enable features
        activity.isEligibleForSearch = true        // Spotlight search
        activity.isEligibleForPrediction = true    // Siri suggestions
        activity.isEligibleForHandoff = true       // Handoff to other devices

        // Search attributes
        let attributes = CSSearchableItemAttributeSet(contentType: .text)
        attributes.title = note.title
        attributes.contentDescription = note.content
        activity.contentAttributeSet = attributes

        // Keywords
        activity.keywords = Set(note.tags)

        // Associate with view controller
        userActivity = activity
        activity.becomeCurrent()
    }
}
```

### SwiftUI Integration

```swift
struct NoteDetailView: View {
    let note: Note

    var body: some View {
        ScrollView {
            VStack(alignment: .leading) {
                Text(note.title)
                    .font(.largeTitle)
                Text(note.content)
            }
        }
        .userActivity("com.yourapp.viewNote") { activity in
            activity.title = note.title
            activity.userInfo = ["noteId": note.id.uuidString]
            activity.isEligibleForSearch = true
            activity.isEligibleForHandoff = true

            let attributes = CSSearchableItemAttributeSet(contentType: .text)
            attributes.title = note.title
            attributes.contentDescription = note.content
            activity.contentAttributeSet = attributes
        }
    }
}
```

### Web Page Integration

```swift
func setupWebEligibleActivity() {
    let activity = NSUserActivity(activityType: "com.yourapp.viewArticle")
    activity.title = article.title
    activity.webpageURL = URL(string: "https://yourapp.com/articles/\(article.id)")

    activity.isEligibleForSearch = true
    activity.isEligibleForPublicIndexing = true  // Can appear in public search
    activity.isEligibleForHandoff = true

    userActivity = activity
    activity.becomeCurrent()
}
```

### Correlating with CoreSpotlight

```swift
// Use same identifier in both
let uniqueId = note.id.uuidString

// CoreSpotlight item
let spotlightItem = CSSearchableItem(
    uniqueIdentifier: uniqueId,
    domainIdentifier: "com.yourapp.notes",
    attributeSet: attributes
)

// NSUserActivity
let activity = NSUserActivity(activityType: "com.yourapp.viewNote")
activity.contentAttributeSet?.relatedUniqueIdentifier = uniqueId
```

---

## Handling Spotlight Results

### In App Delegate

```swift
class AppDelegate: UIResponder, UIApplicationDelegate {
    func application(
        _ application: UIApplication,
        continue userActivity: NSUserActivity,
        restorationHandler: @escaping ([UIUserActivityRestoring]?) -> Void
    ) -> Bool {
        // Handle NSUserActivity
        if userActivity.activityType == "com.yourapp.viewNote" {
            if let noteId = userActivity.userInfo?["noteId"] as? String {
                navigateToNote(id: noteId)
                return true
            }
        }

        // Handle CoreSpotlight result
        if userActivity.activityType == CSSearchableItemActionType {
            if let uniqueId = userActivity.userInfo?[CSSearchableItemActivityIdentifier] as? String {
                navigateToNote(id: uniqueId)
                return true
            }
        }

        return false
    }
}
```

### In Scene Delegate

```swift
class SceneDelegate: UIResponder, UIWindowSceneDelegate {
    func scene(
        _ scene: UIScene,
        continue userActivity: NSUserActivity
    ) {
        handleUserActivity(userActivity)
    }

    func handleUserActivity(_ activity: NSUserActivity) {
        switch activity.activityType {
        case "com.yourapp.viewNote":
            if let noteId = activity.userInfo?["noteId"] as? String {
                navigateToNote(id: noteId)
            }
        case CSSearchableItemActionType:
            if let uniqueId = activity.userInfo?[CSSearchableItemActivityIdentifier] as? String {
                navigateToNote(id: uniqueId)
            }
        default:
            break
        }
    }
}
```

### In SwiftUI

```swift
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
                .onContinueUserActivity("com.yourapp.viewNote") { activity in
                    handleNoteActivity(activity)
                }
                .onContinueUserActivity(CSSearchableItemActionType) { activity in
                    handleSpotlightActivity(activity)
                }
        }
    }

    func handleNoteActivity(_ activity: NSUserActivity) {
        guard let noteId = activity.userInfo?["noteId"] as? String else { return }
        // Navigate to note
        router.navigateTo(.note(id: noteId))
    }

    func handleSpotlightActivity(_ activity: NSUserActivity) {
        guard let uniqueId = activity.userInfo?[CSSearchableItemActivityIdentifier] as? String else { return }
        router.navigateTo(.note(id: uniqueId))
    }
}
```

---

## Query Indexing Status

### Check Index Status

```swift
func checkIndexStatus() async throws {
    let index = CSSearchableIndex.default()

    // Check if indexing is enabled
    let status = try await index.fetchLastClientState()
    print("Last indexed: \(status)")
}
```

### Client State for Incremental Updates

```swift
class IndexManager {
    func performIncrementalUpdate() async throws {
        let index = CSSearchableIndex.default()

        // Get last sync state
        let lastState = try await index.fetchLastClientState()

        // Fetch changes since last state
        let changes = try await fetchChangesSince(lastState)

        // Index new/modified items
        let newItems = changes.added + changes.modified
        if !newItems.isEmpty {
            let searchableItems = newItems.map { createSearchableItem(for: $0) }
            try await index.indexSearchableItems(searchableItems)
        }

        // Delete removed items
        if !changes.deleted.isEmpty {
            try await index.deleteSearchableItems(withIdentifiers: changes.deleted)
        }

        // Save new state
        let newState = createCurrentState()
        try await index.beginBatch()
        try await index.endBatch(withClientState: newState)
    }
}
```

---

## Spotlight Delegate

### Index Maintenance

```swift
import CoreSpotlight

class SpotlightDelegate: NSObject, CSSearchableIndexDelegate {
    func searchableIndex(
        _ searchableIndex: CSSearchableIndex,
        reindexAllSearchableItemsWithAcknowledgementHandler acknowledgementHandler: @escaping () -> Void
    ) {
        // System requested full reindex
        Task {
            try? await reindexAllContent()
            acknowledgementHandler()
        }
    }

    func searchableIndex(
        _ searchableIndex: CSSearchableIndex,
        reindexSearchableItemsWithIdentifiers identifiers: [String],
        acknowledgementHandler: @escaping () -> Void
    ) {
        // System requested reindex of specific items
        Task {
            try? await reindexItems(withIds: identifiers)
            acknowledgementHandler()
        }
    }

    func data(for searchableIndex: CSSearchableIndex, itemIdentifier: String, typeIdentifier: String) throws -> Data {
        // Provide data for a searchable item (e.g., for preview)
        guard let note = NoteManager.shared.find(id: itemIdentifier) else {
            throw IndexError.itemNotFound
        }
        return note.content.data(using: .utf8) ?? Data()
    }

    func fileURL(for searchableIndex: CSSearchableIndex, itemIdentifier: String, typeIdentifier: String, inPlace: Bool) throws -> URL {
        // Provide file URL for item
        throw IndexError.notSupported
    }
}
```

### Registering Delegate

```swift
@main
struct MyApp: App {
    let spotlightDelegate = SpotlightDelegate()

    init() {
        CSSearchableIndex.default().indexDelegate = spotlightDelegate
    }

    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}
```

---

## Best Practices

### 1. Index on Data Changes

```swift
class NoteManager {
    func save(_ note: Note) async throws {
        try await database.save(note)

        // Index immediately after save
        try? await SpotlightIndexer.shared.index(note)
    }

    func delete(_ note: Note) async throws {
        // Remove from index first
        try? await SpotlightIndexer.shared.removeFromIndex(note.id)

        try await database.delete(note)
    }
}
```

### 2. Set Appropriate Expiration

```swift
// Short-lived content
item.expirationDate = Date().addingTimeInterval(7 * 24 * 60 * 60) // 7 days

// Long-lived content
item.expirationDate = Date().addingTimeInterval(365 * 24 * 60 * 60) // 1 year

// Never expire
item.expirationDate = nil
```

### 3. Use Domain Identifiers

```swift
// Group related content
CSSearchableItem(
    uniqueIdentifier: note.id.uuidString,
    domainIdentifier: "com.yourapp.notes",  // Easy bulk operations
    attributeSet: attributes
)

// Delete all notes at once
try await index.deleteSearchableItems(withDomainIdentifiers: ["com.yourapp.notes"])
```

### 4. Provide Rich Metadata

```swift
// Include all relevant attributes
attributes.title = note.title
attributes.contentDescription = note.content
attributes.keywords = note.tags
attributes.lastUsedDate = note.lastViewedAt
attributes.thumbnailData = note.thumbnail

// Better search relevance
```

### 5. Handle Edge Cases

```swift
func safeIndex(_ note: Note) async {
    do {
        try await indexNote(note)
    } catch {
        // Log but don't crash
        logger.error("Failed to index note: \(error)")
    }
}
```

### 6. Test with Spotlight

```swift
// In simulator/device:
// 1. Index content
// 2. Pull down on home screen
// 3. Search for indexed content
// 4. Tap result to verify deep linking
```

---

## Official Resources

- [CoreSpotlight Documentation](https://developer.apple.com/documentation/corespotlight)
- [NSUserActivity Documentation](https://developer.apple.com/documentation/foundation/nsuseractivity)
- [Making content searchable](https://developer.apple.com/documentation/corespotlight/making-content-searchable)
- [WWDC15: Introducing Search APIs](https://developer.apple.com/videos/play/wwdc2015/709/)
