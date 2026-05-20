---
name: db-operations
description: Database operations following repository patterns with GORM and SQLite
category: Database Persistence
---

# Skill: db-operations

## What I do

I provide database operations expertise: transaction management, batch operations, query optimisation, migration strategies, connection pooling, and SQLite-specific patterns for Go applications using GORM. I ensure structured data access using the repository pattern to isolate business logic from persistence concerns.

## When to use me

- Implementing data access layers with the repository pattern
- Managing database transactions and error recovery
- Optimising queries (indexes, batch inserts, pagination, N+1 prevention)
- Writing and running database migrations
- Configuring connection pools and SQLite pragmas (WAL, foreign keys)
- Handling concurrent database access safely
- Building testable data access code with mock repositories

## Core principles

1. **Repository Pattern** - Abstraction of implementation details via interfaces in the domain layer.
2. **Transactions for atomicity** - Multi-step writes in transactions; always return domain-specific errors.
3. **Batch operations** - Insert/update in batches for performance (avoid row-by-row loops).
4. **Query Optimisation** - Use eager loading (Preload) to prevent N+1 queries and leverage indices.
5. **SQLite Best Practices** - Use WAL mode, foreign keys, and appropriate busy timeouts.

## Patterns & examples

### SQLite Configuration & Repository
```go
func OpenDatabase(path string) (*gorm.DB, error) {
  db, err := gorm.Open(sqlite.Open(path), &gorm.Config{
    Logger: logger.Default.LogMode(logger.Warn),
    PrepareStmt: true,
  })
  if err != nil { return nil, err }

  sqlDB, _ := db.DB()
  sqlDB.SetMaxOpenConns(1) // SQLite single writer

  // SQLite pragmas
  db.Exec("PRAGMA journal_mode=WAL")
  db.Exec("PRAGMA foreign_keys=ON")
  db.Exec("PRAGMA busy_timeout=5000")

  return db, nil
}
```

### Transaction Management
```go
func (s *Service) Process(ctx context.Context, data Data) error {
  return s.db.WithContext(ctx).Transaction(func(tx *gorm.DB) error {
    repo := NewRepo(tx)
    if err := repo.Create(ctx, data); err != nil { return err }
    return repo.UpdateStats(ctx)
  })
}
```

### Batch Operations & Pagination
```go
// Batch Insert
db.CreateInBatches(users, 100)

// Paginated List with Preloading
func (r *repo) List(ctx context.Context, page, size int) ([]User, error) {
  var users []User
  err := r.db.WithContext(ctx).
    Preload("Profile").
    Offset((page - 1) * size).
    Limit(size).
    Find(&users).Error
  return users, err
}
```

## Anti-patterns to avoid

- ❌ Leaking ORM details (e.g., `gorm.Model`) to the service layer.
- ❌ Row-by-row inserts in loops; always use `CreateInBatches`.
- ❌ N+1 query problem; use `Preload` for associations.
- ❌ Missing SQLite pragmas; WAL mode and foreign keys are essential for performance/integrity.
- ❌ Ignoring transaction boundaries for multi-step operations.

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Database-Persistence/DB Operations.md`

## Related skills

- `gorm-repository` - Detailed GORM ORM patterns
- `migration-strategies` - Safe database migration workflows
- `sql` - SQL query optimisation and best practices
- `error-handling` - Domain error mapping
- `architecture` - Layered architecture and separation of concerns
