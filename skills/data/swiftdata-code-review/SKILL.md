---
name: swiftdata-code-review
description: Reviews SwiftData code for model design, queries, concurrency, and migrations. Use when reviewing .swift files with import SwiftData, @Model, @Query, @ModelActor, or VersionedSchema.
---

# SwiftData Code Review

## Quick Reference

| Issue Type | Reference |
|------------|-----------|
| @Model, @Attribute, @Relationship, delete rules | [references/model-design.md](references/model-design.md) |
| @Query, #Predicate, FetchDescriptor, #Index | [references/queries.md](references/queries.md) |
| @ModelActor, ModelContext, background operations | [references/concurrency.md](references/concurrency.md) |
| VersionedSchema, MigrationStage, lightweight/custom | [references/migrations.md](references/migrations.md) |

## Review Checklist

- [ ] Models marked `final` (subclassing crashes)
- [ ] @Relationship decorator on ONE side only (not both)
- [ ] Delete rules explicitly set (not relying on default .nullify)
- [ ] Relationships initialized to empty arrays, not default objects
- [ ] Batch operations used for bulk inserts (`append(contentsOf:)`)
- [ ] @Query not loading thousands of items on main thread
- [ ] External values in predicates captured in local variables
- [ ] Scalar comparisons in predicates (not object references)
- [ ] @ModelActor used for background operations
- [ ] PersistentIdentifier/DTOs used to pass data between actors
- [ ] VersionedSchema defined for each shipped version
- [ ] MigrationPlan passed to ModelContainer

## When to Load References

- Reviewing @Model or relationships -> model-design.md
- Reviewing @Query or #Predicate -> queries.md
- Reviewing @ModelActor or background work -> concurrency.md
- Reviewing schema changes or migrations -> migrations.md

## Review Questions

1. Could this relationship assignment cause NULL foreign keys?
2. Is @Relationship on both sides creating circular references?
3. Could this @Query block the main thread with large datasets?
4. Are model objects being passed between actors unsafely?
5. Would schema changes require a migration plan?
