---
id: skill-migration-strategies
tier: T2
category: Database-Persistence
---

# Skill: migration-strategies

## What I do
- **Schema Evolution**: Plan and execute schema changes (adding/modifying/removing tables, columns, constraints).
- **Data Transformation**: Perform data migrations between schemas or systems.
- **Zero-Downtime Planning**: Implement multi-phase strategies (Expand/Contract) for high-availability systems.
- **Rollback Design**: Ensure every migration is reversible with tested rollback paths.
- **Performance Optimisation**: Minimise table locks and use batching for large-scale data changes.

## When to use me
- Planning schema changes for production databases.
- Implementing zero-downtime deployment strategies.
- Refactoring database structure whilst maintaining backward compatibility.
- Coordinating schema changes with application deployments.

## Core principles
- **Safety First**: Every migration must be reversible and tested on production-like data.
- **Backward Compatibility**: Ensure old application versions work during migration phases.
- **Incremental Changes**: Break large migrations into smaller, safer steps (Expand/Contract pattern).
- **Performance Awareness**: Use batch processing and non-locking index creation.

## Patterns & examples

### Batch Processing (Go/GORM)
```go
func (m *Migration) Up(db *gorm.DB) error {
    batchSize := 1000
    for {
        res := db.Exec("UPDATE users SET status = 'active' WHERE status IS NULL LIMIT ?", batchSize)
        if res.Error != nil || res.RowsAffected == 0 { return res.Error }
        time.Sleep(100 * time.Millisecond)
    }
}
```

## Anti-patterns to avoid
❌ **Non-Reversible Migrations**: Not providing a `Down` method or rollback path.
❌ **Direct Schema Changes**: Running `AutoMigrate` in application startup instead of managed migration files.
❌ **Dropping Columns Immediately**: Breaking running application versions that still expect the column.

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Delivery/Migration Strategies.md`

