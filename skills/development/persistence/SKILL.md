---
name: Android Persistence
description: Standards for Room Database and DataStore
metadata:
  labels: [android, persistence, room, database]
  triggers:
    files: ['**/*Dao.kt', '**/*Database.kt', '**/*Entity.kt']
    keywords: ['@Dao', '@Entity', 'RoomDatabase']
---

# Android Persistence Standards

## **Priority: P0**

## Implementation Guidelines

### Room

- **Async**: Return `Flow<List<T>>` for queries, use `suspend` for Write/Insert.
- **Entities**: Keep simple `@Entity` data classes. Map to Domain models in Repository.
- **Transactions**: Use `@Transaction` for multi-table queries (Relations).

### DataStore

- **Usage**: Replace `SharedPreferences` with `ProtoDataStore` (Type-safe) or `PreferencesDataStore`.
- **Scope**: Inject singleton instance via Hilt.

## Anti-Patterns

- **Main Thread**: `**No IO on Main**: Use Dispatchers.IO (Room helper does this, but verify flow collection).`
- **Domain Leak**: `**No Entities in UI**: Map to Domain/UI Models.`

## References

- [DAO Templates](references/implementation.md)
