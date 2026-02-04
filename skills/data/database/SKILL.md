---
name: Database
description: Standards for database interaction, connection pooling, and repository patterns in Golang.
metadata:
  labels: [golang, database, sql, postgres, repository]
  triggers:
    files: ['internal/adapter/repository/**']
    keywords: [database, sql, postgres, gorm, sqlc, pgx]
---

# Golang Database Standards

## **Priority: P0 (CRITICAL)**

## Principles

- **Prefer Raw SQL/Builders over ORMs**: Go structs map well to SQL. ORMs (GORM) can obscure performance. Recommended: `sqlc` (type-safe SQL generation).
- **Repository Pattern**: Abstract DB access behind interfaces in `internal/port/` (e.g., `UserRepository`).
- **Connection Pooling**: Always configure `SetMaxOpenConns`, `SetMaxIdleConns`, `SetConnMaxLifetime`.
- **Transactions**: Logic requiring ACID MUST use transactions. Pass `context.Context` everywhere.

## Drivers

- **PostgreSQL**: `jackc/pgx` (Prefer `pgx/v5` for performance and features).
- **MySQL**: `go-sql-driver/mysql`.
- **SQLite**: `mattn/go-sqlite3` or `modernc.org/sqlite` (pure Go).

## Anti-Patterns

- **Global DB Connection**: Do not use global `var db *sql.DB`. Inject it.
- **Ignoring Context**: Always use `db.QueryContext` or `db.ExecContext` to handle timeouts.
- **Leaking Rows**: ALWAYS `defer rows.Close()` and check `rows.Err()`.

## References

- [Repository Pattern Implementation](references/repository-pattern.md)
- [Connection Tuning](references/connection-tuning.md)
