---
name: database-changes
description: Making database schema changes to the CMS database. Use when adding columns, tables, running migrations, or updating the backend API and TypeScript types for new database fields.
---

# Database Schema Changes

## Overview
End-to-end process for adding new columns or tables to the CMS database.

## Adding a New Column

### 1. Create Migration
```sql
-- migrations/cms/0004_add_my_column.sql
SET search_path TO toygres_cms, public;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_schema = 'toygres_cms'
          AND table_name = 'instances'
          AND column_name = 'my_column'
    ) THEN
        ALTER TABLE instances ADD COLUMN my_column VARCHAR(255);
    END IF;
END;
$$;
```

### 2. Run Migration
```bash
./scripts/db-migrate.sh
```

### 3. Update Backend API
In `toygres-server/src/api.rs`, add to SELECT query:
```rust
let row = sqlx::query(
    "SELECT ..., my_column FROM toygres_cms.instances WHERE ..."
)
```

Add to JSON response:
```rust
Ok(Json(serde_json::json!({
    // existing fields...
    "my_column": row.get::<Option<String>, _>("my_column")
})))
```

### 4. Update TypeScript Types
In `toygres-ui/src/lib/types.ts`:
```typescript
export interface InstanceDetail extends Instance {
  // existing fields...
  my_column: string | null;
}
```

### 5. Update Activities (if needed)
If an activity should set this column:
```rust
sqlx::query("UPDATE toygres_cms.instances SET my_column = $2 WHERE k8s_name = $1")
    .bind(&input.k8s_name)
    .bind(&input.my_column)
    .execute(&pool)
    .await?;
```

## Idempotency Patterns

All CMS activities must be idempotent for Duroxide replay safety:

```sql
-- Upsert pattern
INSERT INTO table (id, value) VALUES ($1, $2)
ON CONFLICT (id) DO UPDATE SET value = $2;

-- Conditional update
UPDATE table SET state = 'new_state'
WHERE id = $1 AND state = 'expected_state';
```
