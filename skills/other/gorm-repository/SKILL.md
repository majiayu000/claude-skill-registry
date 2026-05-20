---
name: gorm-repository
description: GORM ORM, SQLite, and repository patterns
category: Database Persistence
---

# Skill: gorm-repository

## What I do

I provide GORM repository expertise: model definitions, CRUD operations through the repository pattern, migrations, associations, query scopes, and SQLite-specific patterns for Go applications. I ensure maintainable data access layers by abstracting GORM behind clean interfaces and leveraging advanced ORM features.

## When to use me

- Building Go applications with SQL databases (especially SQLite)
- Implementing the repository pattern over GORM ORM
- Defining GORM models with complex tags, constraints, and associations
- Writing reusable queries using chainable scopes and preloading
- Managing database migrations and soft deletes
- Implementing transactions for multi-step data consistency
- Performing complex queries with the GORM query builder or raw SQL

## Core principles

1. **Repository Pattern** - Abstract GORM implementation details behind domain-layer interfaces for testability and isolation.
2. **Model-Driven Design** - Use struct tags to define schemas, constraints, and indices; follow GORM naming conventions.
3. **Query Optimisation** - Prevent N+1 query problems using `Preload` and `Joins`; use `Select` for specific column fetching.
4. **Transaction Consistency** - Wrap all multi-step, related operations in `db.Transaction` to ensure atomicity.
5. **Typed Error Mapping** - Check for GORM errors (e.g., `gorm.ErrRecordNotFound`) and map them to domain-specific errors.

## Patterns & examples

### Repository Interface & Implementation
```go
type UserRepository interface {
  FindByID(ctx context.Context, id string) (*User, error)
  Create(ctx context.Context, user *User) error
}

type gormUserRepo struct { db *gorm.DB }

func (r *gormUserRepo) FindByID(ctx context.Context, id string) (*User, error) {
  var user User
  err := r.db.WithContext(ctx).Preload("Profile").First(&user, "id = ?", id).Error
  if errors.Is(err, gorm.ErrRecordNotFound) { return nil, ErrUserNotFound }
  return &user, err
}
```

### Advanced Model & Scopes
```go
type User struct {
  gorm.Model
  Email string `gorm:"uniqueIndex;not null"`
  Active bool `gorm:"default:true;index"`
}

func IsActive(db *gorm.DB) *gorm.DB {
  return db.Where("active = ?", true)
}

// Usage: db.Scopes(IsActive).Find(&users)
```

### Transaction Pattern
```go
err := db.Transaction(func(tx *gorm.DB) error {
  if err := tx.Create(&order).Error; err != nil { return err }
  return tx.Model(&user).Update("balance", gorm.Expr("balance - ?", total)).Error
})
```

## Anti-patterns to avoid

- ❌ Leaking `*gorm.DB` directly into service layers; always use an interface.
- ❌ N+1 query problem by iterating and querying; use `Preload`.
- ❌ Ignoring database-level errors; always check `.Error` and use `errors.Is`.
- ❌ Missing indexes on frequently queried columns or foreign keys.
- ❌ Using `AutoMigrate` for production environments; prefer versioned migrations.

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Database-Persistence/GORM Repository.md`

## Related skills

- `db-operations` - General database and transaction patterns
- `sql` - SQL query optimisation and best practices
- `migration-strategies` - Safe schema evolution workflows
- `error-handling` - Domain error mapping patterns
- `architecture` - Layer separation with repository pattern
 code
