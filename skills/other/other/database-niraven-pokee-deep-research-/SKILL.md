---
name: database
version: 1.0.0
description: Database operations, queries, migrations, and optimization.
metadata:
  openclaw:
    emoji: 🗄️
    category: infrastructure
---

# Database

Database operations, queries, migrations, and optimization.

## Supported Databases

| Database | Connection | Common Use |
|----------|------------|------------|
| **PostgreSQL** | `psql` or connection string | Production apps |
| **SQLite** | File-based | Local/dev, embedded |
| **MySQL/MariaDB** | `mysql` CLI | Legacy apps |
| **Redis** | `redis-cli` | Caching, sessions |
| **MongoDB** | `mongosh` | Document stores |

## Basic Operations

### PostgreSQL

```bash
# Connect
psql -h localhost -U username -d database

# Run query
psql -c "SELECT * FROM users LIMIT 10;"

# Execute file
psql -f migration.sql
```

### SQLite

```bash
# Create/open database
sqlite3 data.db

# Run query
sqlite3 data.db "SELECT * FROM logs;"
```

## Common Tasks

### 1. Schema Inspection

```sql
-- PostgreSQL: List tables
\dt

-- SQLite: List tables
.tables

-- MySQL: List tables
SHOW TABLES;
```

### 2. Backup/Restore

```bash
# PostgreSQL backup
pg_dump -h localhost -U user dbname > backup.sql

# PostgreSQL restore
psql -h localhost -U user dbname < backup.sql

# SQLite backup
sqlite3 source.db ".backup backup.db"
```

### 3. Migration Pattern

```
migrations/
  001_create_users.sql
  002_add_email_index.sql
  003_create_orders.sql
```

Run in order:
```bash
for f in migrations/*.sql; do
  psql -f "$f"
done
```

## Query Optimization

### Check Slow Queries (PostgreSQL)

```sql
SELECT query, mean_time, calls 
FROM pg_stat_statements 
ORDER BY mean_time DESC 
LIMIT 10;
```

### Add Index

```sql
CREATE INDEX CONCURRENTLY idx_users_email ON users(email);
```

## Best Practices

1. **Use connection pooling** — Don't open connections per query
2. **Parameterized queries** — Prevent SQL injection
3. **Index foreign keys** — Automatic in most DBs, verify
4. **Regular backups** — Automate with cron
5. **Monitor slow queries** — Catch performance issues early
6. **Migrations** — Version control your schema

## Security

- Never commit credentials
- Use `.env` files for connection strings
- Restrict database user permissions
- Enable SSL for remote connections
