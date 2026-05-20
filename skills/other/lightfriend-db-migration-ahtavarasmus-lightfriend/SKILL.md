---
name: lightfriend-db-migration
description: Step-by-step guide for modifying database schema using Diesel migrations
---

# Database Migration Workflow

This skill guides you through modifying the Lightfriend database schema using Diesel ORM.

## Prerequisites

- Backend server should be stopped during migrations
- Backup database if modifying production data

## Step-by-Step Process

### 1. Generate Migration

```bash
cd backend && diesel migration generate <descriptive_name>
```

Replace `<descriptive_name>` with a clear description like:
- `add_user_preferences_table`
- `add_email_verified_column`
- `rename_credits_to_balance`

This creates two files in `backend/migrations/<timestamp>_<name>/`:
- `up.sql` - Apply changes
- `down.sql` - Revert changes

### 2. Edit Migration Files

**up.sql** - Write SQL to apply your changes:
```sql
-- Example: Add new column
ALTER TABLE users ADD COLUMN email_verified BOOLEAN NOT NULL DEFAULT 0;

-- Example: Create new table
CREATE TABLE user_preferences (
    id INTEGER PRIMARY KEY NOT NULL,
    user_id INTEGER NOT NULL,
    theme TEXT NOT NULL DEFAULT 'light',
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Example: Create index
CREATE INDEX idx_user_preferences_user_id ON user_preferences(user_id);
```

**down.sql** - Write SQL to revert your changes:
```sql
-- Example: Remove column
ALTER TABLE users DROP COLUMN email_verified;

-- Example: Drop table
DROP TABLE user_preferences;

-- Example: Drop index
DROP INDEX idx_user_preferences_user_id;
```

### 3. Run Migration

```bash
cd backend && diesel migration run
```

This applies the migration and updates the database.

### 4. Update Diesel Models

If you added/modified tables, update `backend/src/models/user_models.rs`:

```rust
#[derive(Queryable, Insertable, Debug)]
#[diesel(table_name = user_preferences)]
pub struct UserPreference {
    pub id: i32,
    pub user_id: i32,
    pub theme: String,
}
```

### 5. Regenerate Schema

**CRITICAL:** Always regenerate the schema after migrations:

```bash
cd backend && diesel print-schema > src/schema.rs
```

This updates `backend/src/schema.rs` with the new table/column definitions that Diesel uses for type checking.

### 6. Update Repository Code

Add repository methods for new tables/columns in the appropriate repository:
- `repositories/user_core.rs` - User authentication, core user data
- `repositories/user_repository.rs` - User features, integrations
- `repositories/user_subscriptions.rs` - Billing, subscriptions
- `repositories/connection_auth.rs` - OAuth connections

Example:
```rust
pub fn update_user_preference(
    conn: &mut SqliteConnection,
    user_id: i32,
    theme: &str,
) -> Result<(), diesel::result::Error> {
    diesel::update(user_preferences::table)
        .filter(user_preferences::user_id.eq(user_id))
        .set(user_preferences::theme.eq(theme))
        .execute(conn)?;
    Ok(())
}
```

### 7. Test Migration

```bash
cd backend && cargo test
```

### 8. Revert If Needed

If something goes wrong:

```bash
cd backend && diesel migration revert
```

This runs the `down.sql` script to undo the migration.

## Common Patterns

### Adding Encrypted Fields

For sensitive data (tokens, passwords), use TEXT fields and encrypt in application code:

```sql
ALTER TABLE connections ADD COLUMN access_token TEXT;
```

Then encrypt/decrypt using `backend/src/utils/encryption.rs`.

### Adding Foreign Keys

```sql
CREATE TABLE events (
    id INTEGER PRIMARY KEY NOT NULL,
    user_id INTEGER NOT NULL,
    event_type TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

### Adding Timestamps

**Always use INTEGER for timestamps (Unix epoch seconds), never TEXT or datetime objects.**

This keeps timestamps simple and ensures all dates are stored as UTC:

```sql
-- Add timestamp as INTEGER (Unix epoch seconds in UTC)
ALTER TABLE users ADD COLUMN updated_at INTEGER NOT NULL DEFAULT (strftime('%s', 'now'));
```

In Rust, use `chrono::Utc::now().timestamp()` to get the current UTC timestamp as i64.

## Important Notes

- **Never edit `schema.rs` manually** - always use `diesel print-schema`
- **Always write `down.sql`** - migrations should be reversible
- **Test migrations on copy of data** before production
- **Migrations are sequential** - order matters
- **SQLite limitations**: Some operations require table recreation (see Diesel docs)
- **Avoid JSON fields**: Prefer simple TEXT fields and parse to JSON in application code after retrieving from the database. This keeps the schema simple and gives more control over serialization.

## Troubleshooting

**"diesel: command not found"**
```bash
cargo install diesel_cli --no-default-features --features sqlite
```

**"schema.rs is out of sync"**
```bash
cd backend && diesel print-schema > src/schema.rs
```

**Migration fails**
- Check SQL syntax in `up.sql`
- Ensure foreign key references exist
- Check for SQLite-specific limitations
- Use `diesel migration revert` to undo
