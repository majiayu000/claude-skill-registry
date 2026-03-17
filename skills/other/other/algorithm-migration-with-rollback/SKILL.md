---
name: algorithm-migration-with-rollback
description: "Use when replacing a core algorithm (encryption, hashing, ML model) that affects persisted user data and needs rollback safety."
license: MIT
metadata:
  author: shimo4228
  version: "1.0"
  extracted: "2026-02-07"
---
# Algorithm Migration with Rollback Safety

**Extracted:** 2026-02-07
**Context:** Replacing core algorithms (SM2 → FSRS, encryption, hashing, etc.) while preserving rollback capability

## Problem

When replacing a core algorithm that affects user data:
- Legacy code removal risks losing restoration capability
- Data format changes may break existing users
- Rollback becomes difficult after merging
- Testing all edge cases is critical

## Solution

### 4-Phase Migration Strategy

```
Phase 1: Core Implementation (TDD)
├── Add @deprecated markers to old code
├── Implement new algorithm with tests first
└── Target 80%+ coverage

Phase 2: Data Model Migration
├── Extend existing models (don't replace)
├── Implement MigrationStrategy enum
└── Add version detection to parsers

Phase 3: Service Layer Integration
├── Create git tag BEFORE changes
├── Update services to use new algorithm
└── Integration tests

Phase 4: Cleanup & Verification
├── Create final git tag (restoration point)
├── Remove deprecated code
└── Full test suite (500+ tests)
```

### Key Patterns

**1. Deprecation Before Deletion:**
```swift
@available(*, deprecated, renamed: "NewAlgorithm", message: """
    OldAlgorithm is deprecated and will be removed in v2.0.
    Migrate to NewAlgorithm for improved accuracy.
    """)
public enum OldAlgorithm { ... }
```

**2. Transparent Data Migration:**
```swift
public enum MigrationStrategy {
    static func migrate(oldRecord: OldFormat) -> NewFormat {
        NewFormat(
            // Preserve critical fields
            id: oldRecord.id,
            lastModified: oldRecord.lastModified,
            // Transform algorithm-specific fields
            newField: convertOldToNew(oldRecord.oldField)
        )
    }
}
```

**3. Version Detection:**
```swift
public static func detectVersion(_ data: String) -> DataVersion {
    if data.contains("new_field_header") { return .v2 }
    return .v1
}
```

**4. Git Tag Restoration Points:**
```bash
# Before cleanup
git tag v1.x-pre-cleanup

# Emergency restoration
git show v1.x-pre-cleanup:path/to/OldAlgorithm.swift > OldAlgorithm.swift
```

## Example

FSRS Migration (SM2 → FSRS):
- 566 tests total
- 4 phases over 1 day (with TDD automation)
- Zero data loss for existing users
- Transparent migration on first load

## When to Use

- Replacing encryption/hashing algorithms
- Upgrading ML models with different input/output formats
- Migrating database schemas with computed fields
- Any core algorithm affecting persisted user data
