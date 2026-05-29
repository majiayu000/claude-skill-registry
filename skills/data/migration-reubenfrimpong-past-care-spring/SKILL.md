---
name: migration
description: Create a Flyway database migration with MySQL syntax
disable-model-invocation: true
argument-hint: [description of schema change]
---

# Database Migration Skill

Create a Flyway migration for: $ARGUMENTS

## Process

1. **Get Next Version Number**
   ```bash
   ls src/main/resources/db/migration/ | grep -E '^V[0-9]+' | sort -V | tail -1
   ```
   Use the NEXT sequential number. NEVER guess.

2. **Verify Table/Column Names**
   - Check JPA Entity: `@Table(name = "...")` and `@Column(name = "...")`
   - If no annotation: JPA uses class/field name (Church → church)
   - NEVER assume plural/singular - verify!

   ```bash
   # Find table name
   grep -r "CREATE TABLE.*tablename" src/main/resources/db/migration/ | head -5
   # Check entity annotation
   grep -A2 "@Table" src/main/java/com/reuben/pastcare_spring/models/EntityName.java
   ```

3. **Write Migration (MySQL Syntax ONLY)**

   **Create Table:**
   ```sql
   CREATE TABLE IF NOT EXISTS table_name (
       id BIGINT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(255) NOT NULL,
       is_active TINYINT(1) DEFAULT 1,
       amount DECIMAL(19,2),
       created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
       church_id BIGINT NOT NULL,
       CONSTRAINT fk_table_church FOREIGN KEY (church_id) REFERENCES church(id)
   ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
   ```

   **Alter Table:**
   ```sql
   ALTER TABLE table_name ADD COLUMN new_column VARCHAR(255);
   ALTER TABLE table_name MODIFY COLUMN existing_column VARCHAR(500);
   ALTER TABLE table_name DROP COLUMN old_column;
   ```

   **Create Index:**
   ```sql
   CREATE INDEX idx_table_column ON table_name(column_name);
   -- NEVER use WHERE clause (MySQL doesn't support partial indexes)
   ```

4. **Verify Migration**
   ```bash
   ./mvnw compile  # Verify Flyway can parse
   ./mvnw spring-boot:run -Dspring-boot.run.profiles=dev  # Apply migration
   # Look for: "Successfully applied X migration(s)"
   ```

## MySQL Syntax Requirements

| Use | Don't Use |
|-----|-----------|
| `TINYINT(1)` | `BOOLEAN` |
| `DATETIME` / `TIMESTAMP` | `TIMESTAMPTZ` |
| `AUTO_INCREMENT` | `SERIAL` |
| `VARCHAR(255)` | `TEXT` for indexed columns |
| Backticks for reserved words | Unquoted reserved words |
| `ENGINE=InnoDB` | (missing for FK tables) |

## Common Errors to Avoid

- Wrong version number (always check last migration)
- PostgreSQL syntax (SERIAL, BOOLEAN, WHERE in CREATE INDEX)
- Missing `IF NOT EXISTS` for CREATE TABLE
- Missing `ENGINE=InnoDB` for tables with foreign keys
- Missing `DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci`
- Referencing non-existent columns
- Changing table names (breaks production!)

## Known Table Names

| Entity | Table Name |
|--------|------------|
| Church | `church` |
| Member | `member` |
| User | `users` |
| Fellowship | `fellowship` |
| Location | `locations` |

## FORBIDDEN Operations

- `DROP DATABASE`
- `TRUNCATE TABLE`
- Clearing all data
- Deleting migration files
- Any operation causing data loss
