---
name: implement-schema-evolution
description: Implement schema evolution features including semantic versioning, migration planning, breaking change detection, and schema history tracking
license: MIT
compatibility: opencode,claude
metadata:
  created_at: "2026-01-29T22:55:16.161Z"
  updated_at: "2026-01-29T22:55:16.161Z"
  version: "1"
  tags: "transformation,schema,versioning,migration"
  complexity: "high"
  dependencies: "vibe_piper.types, vibe_piper.decorators"
  stability: "stable"
  examples: "Semantic versioning, schema migration, breaking change detection"
---
<!-- BEGIN:compound:skill-managed -->
# Implement Schema Evolution for Vibe Piper

This skill provides comprehensive schema evolution capabilities for data pipelines.

## When To Use

- User requests schema versioning, migration, or evolution features
- Ticket requires schema evolution implementation
- Need to track schema versions and changes over time


## Implementation Guide

### Core Components

1. **SemanticVersion**: Semantic versioning (MAJOR.MINOR.PATCH)
   ```python
   from vibe_piper.schema_evolution import SemanticVersion

   v = SemanticVersion(1, 2, 3)  # 1.2.3
   v.is_compatible()  # Check version compatibility
   v.next_major()  # Increment major version
   ```

2. **SchemaDiff**: Compare schemas and detect changes
   ```python
   from vibe_piper.schema_evolution import BreakingChangeDetector, SchemaDiff

   detector = BreakingChangeDetector()
   diff = detector.detect(old_schema, new_schema)
   diff.changes  # List of SchemaChange objects
   diff.has_breaking_changes  # Boolean
   ```

3. **MigrationPlan**: Generate and execute migration plans
   ```python
   from vibe_piper.schema_evolution import MigrationPlanner, MigrationPlan

   planner = MigrationPlanner()
   plan = planner.generate(diff)
   migrated_data = plan.execute(old_data)
   ```

4. **SchemaHistory**: Track schema versions over time
   ```python
   from vibe_piper.schema_evolution import SchemaHistory, get_schema_history

   history = get_schema_history()
   history.add_entry(entry)
   ```

5. **@schema_version decorator**: Declarative versioning
   ```python
   from vibe_piper import define_schema, schema_version

   @define_schema
   @schema_version("1.2.0", description="Add email field")
   class UserSchema:
       email: String = String(max_length=255)
   ```

## Key Patterns

- Breaking changes are detected when:
  - Fields are removed
  - Field types change (e.g., INT to STRING)
  - Fields become required (optional → required)
  - Fields become non-nullable (nullable → not nullable)
  - Constraints tighten (e.g., max_value decreases)

- Non-breaking changes:
  - Fields are added
  - Fields become optional (required → optional)
  - Fields become nullable (not nullable → nullable)
  - Constraints relax

- Migration steps are auto-generated based on schema diffs
- Custom migration functions can be provided for complex transformations


## Testing Strategy

```python
import pytest
from vibe_piper import SemanticVersion, define_schema, schema_version

def test_schema_evolution():
    # Test version parsing and comparison
    v1 = SemanticVersion.parse("1.2.0")
    v2 = SemanticVersion(1, 3, 0)
    assert v2 > v1

    # Test breaking change detection
    detector = BreakingChangeDetector()
    diff = detector.detect(old_schema, new_schema)
    assert diff.has_breaking_changes

    # Test migration plan execution
    plan = MigrationPlanner().generate(diff)
    migrated = plan.execute(old_data)
    ```

## Acceptance Criteria
- [ ] @schema_version decorator working
- [ ] Automatic migration when schema changes
- [ ] Backward compatibility validation
- [ ] Breaking change warnings
- [ ] Schema diff visualization (MigrationPlan.to_dict)
- [ ] Migration plan generation
- [ ] Rollback to previous version (SchemaHistory.rollback_to_version)
- [ ] Schema history in metadata store (needs integration)
- [ ] Integration with @asset decorator (works but needs verification)
- [ ] Tests with schema evolution scenarios
- [ ] 80%+ coverage
- [ ] Documentation

## Dependencies

- vibe_piper.types (Schema, SchemaField, DataType)
- vibe_piper.schema_definitions (define_schema, Field types)
- vibe_piper.decorators (@asset decorator)
- Python 3.14+ (for type annotations)

## Notes

- This is a core transformation feature that integrates with @asset decorator
- Schema history is currently in-memory; metadata store integration is a future enhancement
- MigrationPlan.to_dict() provides JSON serialization of migration steps
- Rollback functionality is available but requires data backup strategy
<!-- END:compound:skill-managed -->

## Manual notes

_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._
