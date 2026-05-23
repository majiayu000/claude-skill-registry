---
name: UserDefaults Migrator
description: Find UserDefaults.standard usage in Leavn, migrate to PreferencesStore/SwiftData, create entities, ensure single source of truth
allowed-tools: Read, Write, Edit, Grep
---

# UserDefaults Migrator

Migrate UserDefaults to SwiftData:

1. **Find usage**: `grep -r "UserDefaults.standard"`
2. **Categorize**:
   - Keep: Tests, debug flags, widgets
   - Migrate: User preferences, stats, settings

3. **Create entity if needed**
4. **Update code to use PreferencesStore**
5. **Write migration logic**
6. **Archive old keys**

Use when: UserDefaults cleanup, preference migration, SwiftData entities
