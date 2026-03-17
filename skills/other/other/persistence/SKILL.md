---
name: iOS Persistence
description: Standards for SwiftData, Core Data, and Local Storage.
metadata:
  labels: [ios, persistence, swiftdata, coredata, sqlite]
  triggers:
    files: ['**/*.xcdatamodeld', '**/*Model.swift']
    keywords:
      [
        PersistentContainer,
        FetchRequest,
        ManagedObject,
        Query,
        ModelContainer,
        Repository,
      ]
---

# iOS Persistence Standards

## **Priority: P0**

## Implementation Guidelines

### SwiftData (iOS 17+)

- **Models**: Use `@Model` macro for pure Swift classes.
- **Container**: Use `ModelContainer` for schema management. Inject into the environment for SwiftUI apps.
- **Queries**: Use `@Query` for declarative data fetching in Views.

### Core Data (Standard)

- **Persistent Stack**: Initialize `NSPersistentContainer` in a dedicated `PersistenceController`.
- **Context Management**: Use `viewContext` for UI tasks and `newBackgroundContext()` for heavy imports to avoid blocking the main thread.
- **FetchedResultsController**: Use `NSFetchedResultsController` for efficient list management with change tracking.

### Best Practices

- **Migration**: Always perform lightweight migrations for minor schema changes. Use versioned models for complex migrations.
- **Threading**: Managed objects are not thread-safe. Always access them on the context's queue (e.g., `perform { ... }`).
- **Batching**: Use `NSBatchUpdateRequest` or `NSBatchDeleteRequest` for large datasets.

## Anti-Patterns

- **Main Thread Blocking**: `**No heavy I/O on ViewContext**: Use private background contexts.`
- **Manual String Keys**: `**No string-based predicates**: Use KeyPaths or generated helpers.`
- **Missing Merge Policies**: `**No merge strategy**: Explicitly set mergePolicy (e.g., mergeByPropertyObjectTrump).`

## References

- [SwiftData & Core Data Implementation](references/implementation.md)
