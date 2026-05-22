---
name: postgresql-fundamentals
description: Master PostgreSQL SQL fundamentals - data types, tables, constraints, schema design
version: "3.0.0"
sasmp_version: "1.3.0"
bonded_agent: 01-postgresql-fundamentals
bond_type: PRIMARY_BOND
category: database
difficulty: beginner
estimated_time: 2h
---

# PostgreSQL Fundamentals Skill

> Atomic skill for SQL foundations and schema design

## Overview

Production-ready patterns for PostgreSQL 16+ data modeling, including type selection, constraint design, and schema organization.

## Prerequisites

- PostgreSQL 16+ installed
- Basic SQL knowledge
- Database access with CREATE privileges

## Parameters

```yaml
parameters:
  operation:
    type: string
    required: true
    enum: [create_table, add_constraint, select_type, design_schema]
  table_name:
    type: string
    pattern: "^[a-z][a-z0-9_]*$"
  schema:
    type: string
    default: "public"
```

## Quick Reference

### Data Type Selection
| Use Case | Recommended | Avoid |
|----------|-------------|-------|
| Primary key | `BIGINT GENERATED ALWAYS AS IDENTITY` | `SERIAL` |
| Monetary | `NUMERIC(19,4)` | `FLOAT` |
| Timestamps | `TIMESTAMPTZ` | `TIMESTAMP` |
| UUID | `UUID` | `VARCHAR(36)` |
| JSON data | `JSONB` | `JSON` |

### Table Template
```sql
CREATE TABLE schema_name.table_name (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

### Constraint Patterns
```sql
-- Foreign key
CONSTRAINT fk_name FOREIGN KEY (col) REFERENCES other(id) ON DELETE CASCADE;
-- Check
CONSTRAINT chk_positive CHECK (amount > 0);
-- Unique
CONSTRAINT uq_email UNIQUE (email);
```

## Validation Rules

| Rule | Pattern |
|------|---------|
| Table names | `^[a-z][a-z0-9_]{2,62}$` |
| Column names | `^[a-z][a-z0-9_]{1,62}$` |

## Test Template

```sql
DO $$ BEGIN
    DROP TABLE IF EXISTS test_users;
    CREATE TABLE test_users (id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY);
    ASSERT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'test_users');
    DROP TABLE test_users;
END $$;
```

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| `42P07` | Table exists | Use IF NOT EXISTS |
| `23505` | Duplicate key | Check constraints |
| `42703` | Column not found | Verify names |

## Usage

```
Skill("postgresql-fundamentals")
```
