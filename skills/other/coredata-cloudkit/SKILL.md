---
name: coredata-cloudkit
description: CoreData and CloudKit patterns for data persistence and sync. Use when working on data models, migrations, sync logic, or query optimization.
---

# CoreData + CloudKit Patterns

## SwiftData Model Definition
```swift
@Model
final class TransactionEntity {
    @Attribute(.unique) var id: UUID
    var amount: Decimal
    var note: String
    var date: Date
    var createdAt: Date
    var updatedAt: Date
    var deletedAt: Date?  // Soft delete for CloudKit sync
    
    @Relationship(deleteRule: .nullify)
    var category: CategoryEntity?
    
    @Relationship(deleteRule: .nullify)
    var account: AccountEntity?
    
    init(id: UUID = UUID(), amount: Decimal, note: String, date: Date) {
        self.id = id
        self.amount = amount
        self.note = note
        self.date = date
        self.createdAt = Date()
        self.updatedAt = Date()
    }
}
```

## Repository Pattern
```swift
protocol TransactionRepository: Sendable {
    func getAll(filter: TransactionFilter?) async throws -> [Transaction]
    func getById(_ id: UUID) async throws -> Transaction?
    func save(_ transaction: Transaction) async throws
    func delete(_ id: UUID) async throws
    func batchImport(_ transactions: [Transaction]) async throws
}
```

## CloudKit Sync Monitoring
```swift
final class SyncMonitor: ObservableObject {
    @Published var syncStatus: SyncStatus = .idle
    
    func startMonitoring() {
        NotificationCenter.default.addObserver(
            forName: NSPersistentCloudKitContainer.eventChangedNotification,
            object: nil, queue: .main
        ) { notification in
            guard let event = notification.userInfo?[
                NSPersistentCloudKitContainer.eventNotificationUserInfoKey
            ] as? NSPersistentCloudKitContainer.Event else { return }
            
            self.syncStatus = SyncStatus(from: event)
        }
    }
}
```

## Performance: Batch Operations
- For > 100 records: use `NSBatchInsertRequest`
- Use `fetchBatchSize` on fetch requests (default 20)
- Create compound indexes for common query patterns
- Use `NSFetchedResultsController` for list views
