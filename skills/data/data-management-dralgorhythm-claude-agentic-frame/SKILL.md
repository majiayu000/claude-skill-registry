---
name: data-management
description: Design and manage data storage effectively. Use when working with databases, schemas, or data migrations. Covers schema design, migrations, and data integrity.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Data Management

## Workflows

- [ ] **Schema Design**: Define tables, relationships, constraints
- [ ] **Migrations**: Version control schema changes
- [ ] **Indexing**: Add indexes for query performance
- [ ] **Backup**: Ensure data recovery capability

## Schema Design Principles

### Normalization
- **1NF**: Atomic values, no repeating groups
- **2NF**: No partial dependencies
- **3NF**: No transitive dependencies

### When to Denormalize
- Read-heavy workloads
- Reporting/analytics
- Caching layers

## Migration Best Practices

### Forward-Only Migrations
Each migration should be a single forward step.

```sql
-- migrations/001_create_users.sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) NOT NULL UNIQUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
```

### Safe Migrations
- Add columns as nullable first
- Create indexes concurrently
- Never drop columns in the same deploy

## Indexing Strategy

```sql
-- B-tree (default): Equality and range queries
CREATE INDEX idx_users_email ON users(email);

-- Partial index: When you query a subset
CREATE INDEX idx_active_users ON users(id) WHERE active = true;

-- Composite index: Multiple columns
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at DESC);
```

## Connection Management

```typescript
// Use connection pooling
const pool = new Pool({
  max: 20,                    // Max connections
  idleTimeoutMillis: 30000,   // Close idle connections
  connectionTimeoutMillis: 2000
});
```

## Data Integrity

- Use foreign key constraints
- Add NOT NULL where appropriate
- Use CHECK constraints for validation
- Consider using ENUM types for fixed values
