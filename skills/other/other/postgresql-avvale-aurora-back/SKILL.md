---
name: postgresql
description: >
  PostgreSQL expert skill - Advanced SQL, extensions, data types, indexing, performance tuning, and PostgreSQL-specific features.
  Trigger: When writing SQL queries, designing schemas, optimizing performance, using PostgreSQL extensions, or working with advanced data types.
license: MIT
metadata:
  author: aurora
  version: "1.1"
  auto_invoke: "SQL queries, database design, PostgreSQL extensions, performance optimization, JSONB, arrays, full-text search"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch
---

## When to Use

Use this skill when:
- Writing raw SQL queries for PostgreSQL
- Designing database schemas and tables
- Creating or optimizing indexes
- Working with JSONB, arrays, or composite types
- Implementing full-text search (tsvector/tsquery)
- Using PostgreSQL extensions (pg_trgm, uuid-ossp, etc.)
- Performance tuning and query optimization
- Writing stored procedures/functions
- Working with CTEs, window functions, or recursive queries
- Implementing constraints, triggers, or rules

## Detailed References

- [Data Types Reference](data-types.md) — All PostgreSQL types (numeric, text, date, UUID, JSONB, arrays, enum, composite, range)
- [Indexing Strategies](indexing.md) — B-Tree, GIN, GiST, BRIN, Hash indexes
- [Advanced Queries](queries.md) — Full-text search, CTEs, window functions, UPSERT, LATERAL, GROUPING SETS
- [Performance & Schema Design](performance.md) — EXPLAIN, optimization, extensions, partitioning, constraints

## Decision Trees

### Choosing Data Types

```
Storing identifiers?
├─ Distributed system → UUID
├─ Single database, high volume → BIGSERIAL
└─ Single database, moderate → SERIAL/INTEGER

Storing text?
├─ Need case-insensitive → CITEXT (with extension)
├─ Fixed max length required → VARCHAR(n)
└─ Variable/unlimited → TEXT

Storing numbers?
├─ Money/financial → NUMERIC(precision, scale)
├─ Counts/IDs → INTEGER or BIGINT
└─ Scientific/approximate → DOUBLE PRECISION

Storing dates?
├─ Date only → DATE
├─ Time only → TIME
└─ Date + time → TIMESTAMPTZ (always with timezone!)

Storing structured data?
├─ Schema-less, queryable → JSONB
├─ List of values → ARRAY
├─ Fixed structure → Composite type or separate table
└─ Key-value pairs → JSONB or hstore
```

### Choosing Index Type

```
Query pattern?
├─ Equality (=) only → HASH (or B-tree)
├─ Range (<, >, BETWEEN) → B-tree
├─ Pattern matching (LIKE '%x%') → GIN with pg_trgm
├─ Full-text search → GIN (faster) or GiST (smaller)
├─ JSONB containment (@>) → GIN
├─ Array operations (@>, &&) → GIN
├─ Geometric/range → GiST
└─ Time-series (ordered inserts) → BRIN

Table size?
├─ Small (< 100K rows) → B-tree usually sufficient
├─ Medium (100K-10M) → Consider partial indexes
└─ Large (> 10M) → Consider partitioning + BRIN
```

## Aurora/Sequelize Integration

### DataTypes Mapping

```typescript
// In Aurora/Sequelize models
import { DataTypes } from 'sequelize';

// UUID
type: DataTypes.UUID,
defaultValue: DataTypes.UUIDV4

// JSONB
type: DataTypes.JSONB,
defaultValue: {}

// Array
type: DataTypes.ARRAY(DataTypes.STRING(64))
type: DataTypes.ARRAY(DataTypes.UUID)
type: DataTypes.ARRAY(DataTypes.INTEGER)

// Enum
type: DataTypes.ENUM('PENDING', 'ACTIVE', 'COMPLETED')

// Numeric
type: DataTypes.DECIMAL(10, 2)
type: DataTypes.BIGINT
type: DataTypes.INTEGER

// Text
type: DataTypes.TEXT
type: DataTypes.STRING(255)

// Date/Time
type: DataTypes.DATE  // TIMESTAMP WITH TIME ZONE
type: DataTypes.DATEONLY  // DATE

// Boolean
type: DataTypes.BOOLEAN
```

### Index Definition in Models

```typescript
@Table({
    modelName: 'MyModel',
    indexes: [
        { fields: ['email'], unique: true },
        { fields: ['tags'], using: 'GIN' },
        { fields: ['metadata'], using: 'GIN' },
        { fields: ['status'], where: { deletedAt: null } },
        { fields: ['tenantId', 'code'], unique: true },
    ],
})
```

## Commands Reference

```bash
# Connect to database
psql -h localhost -U postgres -d database_name

# Execute SQL file
psql -h localhost -U postgres -d database_name -f script.sql

# Dump database
pg_dump -h localhost -U postgres database_name > backup.sql
pg_dump -h localhost -U postgres -Fc database_name > backup.dump

# Restore database
psql -h localhost -U postgres -d database_name < backup.sql
pg_restore -h localhost -U postgres -d database_name backup.dump

# Check PostgreSQL version
psql -c "SELECT version();"

# Show running queries
psql -c "SELECT pid, now() - pg_stat_activity.query_start AS duration, query FROM pg_stat_activity WHERE state = 'active';"

# Kill query
psql -c "SELECT pg_cancel_backend(pid);"      -- Graceful
psql -c "SELECT pg_terminate_backend(pid);"   -- Force
```

## Resources

- **Templates**: See [assets/](assets/) for SQL templates
- **Aurora Criteria**: See `aurora-criteria` skill for QueryStatement patterns
- **Aurora Models**: See `src/@app/*/infrastructure/sequelize/*.model.ts` for examples
