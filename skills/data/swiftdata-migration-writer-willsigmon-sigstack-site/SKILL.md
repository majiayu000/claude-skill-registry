---
name: SwiftData Migration Writer
description: Write UserDefaults to SwiftData migration logic for Leavn app with data preservation, rollback, and validation
allowed-tools: Read, Write, Edit
---

# SwiftData Migration Writer

Create migration from UserDefaults to SwiftData:

1. **Map keys to entity fields**
2. **Write migration method**:
   ```swift
   func migrateXIfNeeded() async throws {
       guard !hasMigrated("X") else { return }
       // Read UserDefaults
       // Create/update entity
       // Archive old keys
       // Mark migrated
   }
   ```

3. **Add to PreferencesStore extension**
4. **Call on first load**
5. **Test data preservation**

Use when: Creating SwiftData entities, migrating preferences, data persistence
