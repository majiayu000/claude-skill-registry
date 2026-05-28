---
name: Preferences Store Expert
description: Work with Leavn PreferencesStore - SwiftData persistence, snapshot patterns, async observation, entity relationships, migration from UserDefaults
allowed-tools: Read, Edit, Grep
---

# Preferences Store Expert

Expert in PreferencesStore architecture:

**Pattern**:
- Entities in SwiftData
- Snapshots (Sendable, Codable)
- Async observation
- Single source of truth

**Key files**:
- PreferencesStore.swift
- PreferenceModels.swift
- PreferencesStore+{Domain}.swift extensions

**Operations**:
- `loadX()` → snapshot
- `updateX { }` → mutation
- `observeSnapshots()` → AsyncStream

Use when: Preferences issues, settings persistence, SwiftData, user data
