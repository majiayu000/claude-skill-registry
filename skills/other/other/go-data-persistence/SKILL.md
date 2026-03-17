---
name: go-data-persistence
description: Data persistence patterns in Go covering raw SQL with sqlx/pgx, ORMs like Ent and GORM, connection pooling, migrations with golang-migrate, and transaction management. Use when implementing database access, designing repositories, or managing schema migrations.
---

# Data Persistence in Go

## Quick Reference

| Topic | Reference |
|-------|-----------|
| Connection pool internals, sizing, pgx pools, monitoring | [references/connection-pooling.md](references/connection-pooling.md) |
| golang-migrate setup, file conventions, CI/CD integration | [references/migrations.md](references/migrations.md) |
| Transaction helpers, service-layer transactions, isolation levels | [references/transactions.md](references/transactions.md) |

## Choosing Your Approach

Pick the right tool based on your project's needs:

| Factor | Raw SQL (sqlx/pgx) | ORM (Ent/GORM) |
|--------|-------------------|-----------------|
| Complex queries | Preferred | Awkward |
| Type safety | Manual | Auto-generated |
| Performance control | Full | Limited |
| Rapid prototyping | Slower | Faster |
| Schema migrations | golang-migrate | Built-in (Ent) |
| Learning curve | SQL knowledge | ORM API |

### When to Use Raw SQL (sqlx/pgx)

- You need full control over query performance and execution plans
- Your domain has complex joins, CTEs, window functions, or recursive queries
- You want zero abstraction overhead and direct access to PostgreSQL features
- Your team is comfortable writing and maintaining SQL
- You need advanced PostgreSQL features like `LISTEN/NOTIFY`, advisory locks, or `COPY`

**pgx** is the recommended PostgreSQL driver for Go. It provides native PostgreSQL protocol support, better performance than `database/sql`, and access to PostgreSQL-specific features. Use **sqlx** when you need `database/sql` compatibility or work with multiple database backends.

### When to Use an ORM (Ent/GORM)

- You want type-safe, generated query builders and avoid writing SQL
- Your schema is mostly CRUD with straightforward relationships
- You value generated code, schema-as-code, and automatic migrations (Ent)
- You are prototyping quickly and want to iterate on the schema fast

**Ent** is preferred over GORM for new projects. It uses code generation for type safety, has a declarative schema DSL, built-in migration support, and integrates with GraphQL. GORM is suitable if the team already knows it or if the project is small.

## Connection Setup

Every Go application connecting to a database needs a properly configured connection pool. The `database/sql` package manages pooling automatically, but the defaults are not suitable for production.

```go
db, err := sql.Open("postgres", connStr)
if err != nil {
    return fmt.Errorf("opening db: %w", err)
}

// Connection pool configuration
db.SetMaxOpenConns(25)                 // Max simultaneous connections
db.SetMaxIdleConns(10)                 // Connections kept alive when idle
db.SetConnMaxLifetime(5 * time.Minute) // Recycle connections
db.SetConnMaxIdleTime(1 * time.Minute) // Close idle connections

// Verify connection
if err := db.PingContext(ctx); err != nil {
    return fmt.Errorf("pinging db: %w", err)
}
```

### Pool Settings Explained

**MaxOpenConns** -- The maximum number of open connections to the database. This prevents your application from overwhelming the database with too many concurrent connections. Set to approximately 25 for typical web apps. To calculate: divide your database's `max_connections` (minus a reserve for admin and replication) by the number of application instances. If your DB allows 100 connections, you have 3 app instances, and you reserve 10 for admin, set this to `(100 - 10) / 3 = 30`.

**MaxIdleConns** -- The number of connections kept alive in the pool when not in use. These warm connections avoid the latency of establishing new connections for each request. Set to approximately 10, or roughly 40% of `MaxOpenConns`. Setting this too high wastes database connections; setting it too low causes frequent reconnections.

**ConnMaxLifetime** -- The maximum amount of time a connection can be reused. After this duration, the connection is closed and a new one is created on the next request. This helps pick up DNS changes (important for cloud databases that failover to new IPs), rebalance load across read replicas, and prevent connections from becoming stale. A value of 5 minutes is typical. Set shorter (1-2 min) if your infrastructure uses DNS-based failover.

**ConnMaxIdleTime** -- The maximum amount of time a connection can sit idle before it is closed. This releases connections back to the database during low-traffic periods, freeing resources. A value of 1 minute is typical. This should be shorter than `ConnMaxLifetime`.

For pgx-specific pooling with native PostgreSQL support, see [references/connection-pooling.md](references/connection-pooling.md).

## Repository Pattern

Define a store interface at the consumer for testability. Implement against a concrete database driver. This pattern keeps your domain logic decoupled from the database.

```go
// Store interface for testability
type UserStore interface {
    GetUser(ctx context.Context, id string) (*User, error)
    ListUsers(ctx context.Context, limit, offset int) ([]*User, error)
    CreateUser(ctx context.Context, u *User) error
}

// sqlx implementation
type PostgresUserStore struct {
    db *sqlx.DB
}

func NewPostgresUserStore(db *sqlx.DB) *PostgresUserStore {
    return &PostgresUserStore{db: db}
}

func (s *PostgresUserStore) GetUser(ctx context.Context, id string) (*User, error) {
    var u User
    err := s.db.GetContext(ctx, &u, "SELECT * FROM users WHERE id = $1", id)
    if errors.Is(err, sql.ErrNoRows) {
        return nil, ErrNotFound
    }
    return &u, err
}

func (s *PostgresUserStore) ListUsers(ctx context.Context, limit, offset int) ([]*User, error) {
    var users []*User
    err := s.db.SelectContext(ctx, &users,
        "SELECT * FROM users ORDER BY created_at DESC LIMIT $1 OFFSET $2",
        limit, offset,
    )
    return users, err
}

func (s *PostgresUserStore) CreateUser(ctx context.Context, u *User) error {
    _, err := s.db.NamedExecContext(ctx,
        `INSERT INTO users (id, email, name, created_at, updated_at)
         VALUES (:id, :email, :name, :created_at, :updated_at)`, u)
    return err
}
```

### Model Struct Tags

Use `db` tags for sqlx column mapping and keep models close to the store:

```go
type User struct {
    ID        string    `db:"id"`
    Email     string    `db:"email"`
    Name      string    `db:"name"`
    CreatedAt time.Time `db:"created_at"`
    UpdatedAt time.Time `db:"updated_at"`
}
```

### Sentinel Errors

Define domain-specific errors that callers can check without importing database packages:

```go
var (
    ErrNotFound  = errors.New("not found")
    ErrConflict  = errors.New("conflict")
)
```

Map database errors to domain errors in the store layer:

```go
func (s *PostgresUserStore) CreateUser(ctx context.Context, u *User) error {
    _, err := s.db.NamedExecContext(ctx, query, u)
    if err != nil {
        var pgErr *pgconn.PgError
        if errors.As(err, &pgErr) && pgErr.Code == "23505" {
            return ErrConflict
        }
        return fmt.Errorf("inserting user: %w", err)
    }
    return nil
}
```

## Migrations

Use **golang-migrate** for managing schema changes. Migrations are pairs of SQL files: one for applying changes (`up`) and one for reverting them (`down`).

```
migrations/
├── 000001_create_users.up.sql
├── 000001_create_users.down.sql
├── 000002_add_user_roles.up.sql
└── 000002_add_user_roles.down.sql
```

Run migrations at application startup:

```go
import "github.com/golang-migrate/migrate/v4"

func runMigrations(dbURL string) error {
    m, err := migrate.New("file://migrations", dbURL)
    if err != nil {
        return fmt.Errorf("creating migrator: %w", err)
    }

    if err := m.Up(); err != nil && err != migrate.ErrNoChange {
        return fmt.Errorf("running migrations: %w", err)
    }

    return nil
}
```

Key rules: always write both up and down migrations, use `IF NOT EXISTS` / `IF EXISTS` for idempotency, never modify a migration that has been applied in production. For full migration patterns, CI/CD integration, and safe migration strategies, see [references/migrations.md](references/migrations.md).

## Transactions

Use a transaction helper to ensure consistent commit/rollback handling. Transactions should be managed at the **service layer**, not the store layer, so that multiple store operations can be composed into a single atomic unit.

```go
func WithTx(ctx context.Context, db *sql.DB, fn func(tx *sql.Tx) error) error {
    tx, err := db.BeginTx(ctx, nil)
    if err != nil {
        return fmt.Errorf("beginning transaction: %w", err)
    }

    if err := fn(tx); err != nil {
        if rbErr := tx.Rollback(); rbErr != nil {
            return fmt.Errorf("rollback failed: %v (original error: %w)", rbErr, err)
        }
        return err
    }

    return tx.Commit()
}
```

Store methods accept a `*sql.Tx` parameter so they can participate in a caller-controlled transaction:

```go
func (s *OrderService) PlaceOrder(ctx context.Context, order *Order) error {
    return WithTx(ctx, s.db, func(tx *sql.Tx) error {
        if err := s.orderStore.CreateWithTx(ctx, tx, order); err != nil {
            return fmt.Errorf("creating order: %w", err)
        }
        if err := s.inventoryStore.DecrementWithTx(ctx, tx, order.Items); err != nil {
            return fmt.Errorf("updating inventory: %w", err)
        }
        return nil
    })
}
```

For isolation levels, deadlock prevention, context propagation, and testing strategies, see [references/transactions.md](references/transactions.md).

## When to Load References

Load **connection-pooling.md** when:
- Configuring pgx native pools (`pgxpool.Pool`)
- Sizing connection pools for production workloads
- Working with cloud databases, PgBouncer, or connection limits
- Monitoring pool health and metrics

Load **migrations.md** when:
- Setting up golang-migrate for the first time
- Writing new migration files
- Integrating migrations into CI/CD pipelines
- Dealing with migration failures or rollbacks

Load **transactions.md** when:
- Implementing multi-step operations that must be atomic
- Designing service-layer transaction boundaries
- Choosing transaction isolation levels
- Debugging deadlocks or long-running transactions

## Anti-Patterns

### Using string concatenation for queries

```go
// BAD -- SQL injection vulnerability
query := "SELECT * FROM users WHERE name = '" + name + "'"
```

Always use parameterized queries (`$1`, `$2`, etc.) or named parameters (`:name`).

### Leaking database types into handlers

```go
// BAD -- handler depends on sql.ErrNoRows
func (s *Server) handleGetUser(w http.ResponseWriter, r *http.Request) {
    user, err := s.store.GetUser(ctx, id)
    if errors.Is(err, sql.ErrNoRows) { // handler knows about sql package
        http.NotFound(w, r)
        return
    }
}
```

Return domain errors (`ErrNotFound`) from the store and check those in handlers instead.

### Opening a new connection per request

```go
// BAD -- bypasses connection pooling entirely
func (s *Server) handleGetUser(w http.ResponseWriter, r *http.Request) {
    db, _ := sql.Open("postgres", connStr) // new pool per request!
    defer db.Close()
}
```

Open the database connection once at startup and share the pool across the application.

### SELECT * in production code

```go
// BAD -- fragile, breaks when columns change
err := db.GetContext(ctx, &u, "SELECT * FROM users WHERE id = $1", id)
```

Explicitly list the columns you need. This makes the query resilient to schema changes and avoids fetching unnecessary data.

### Not handling context cancellation

```go
// BAD -- ignores context, query runs even if client disconnects
rows, err := db.Query("SELECT * FROM large_table")
```

Always use the `Context` variants (`QueryContext`, `ExecContext`, `GetContext`) and pass the request context so that queries are cancelled when the caller gives up.

### Transactions in store methods

```go
// BAD -- store controls transaction, caller cannot compose
func (s *UserStore) CreateUser(ctx context.Context, u *User) error {
    tx, _ := s.db.BeginTx(ctx, nil)
    // ... insert user ...
    return tx.Commit()
}
```

Let the service layer manage transactions and pass `*sql.Tx` into store methods. See [references/transactions.md](references/transactions.md) for the correct pattern.
