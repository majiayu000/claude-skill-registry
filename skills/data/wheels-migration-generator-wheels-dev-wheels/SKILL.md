---
name: Wheels Migration Generator
description: Generate database-agnostic Wheels migrations for creating tables, altering schemas, and managing database changes. Use when creating or modifying database schema, adding tables, columns, indexes, or foreign keys. Prevents database-specific SQL and ensures cross-database compatibility.
---

# Wheels Migration Generator

## When to Use This Skill

Activate automatically when:
- User requests to create a migration (e.g., "create posts table")
- User wants to add/modify/remove columns
- User needs to add indexes or foreign keys
- User is changing database schema
- User mentions: migration, database, table, column, index, schema

## Critical Anti-Pattern to Prevent

### ❌ ANTI-PATTERN: Database-Specific Date Functions

**NEVER use database-specific functions like DATE_SUB(), NOW(), CURDATE()!**

**WRONG:**
```cfm
execute("INSERT INTO posts (publishedAt) VALUES (DATE_SUB(NOW(), INTERVAL 1 DAY))");  ❌ MySQL only!
```

**CORRECT:**
```cfm
var pastDate = DateAdd("d", -1, Now());
execute("INSERT INTO posts (publishedAt) VALUES (TIMESTAMP '#DateFormat(pastDate, "yyyy-mm-dd")# #TimeFormat(pastDate, "HH:mm:ss")#')");  ✅ Cross-database!
```

## Migration Structure

### Basic Migration Template

```cfm
component extends="wheels.migrator.Migration" {

    function up() {
        transaction {
            try {
                // Your migration code here

            } catch (any e) {
                local.exception = e;
            }

            if (StructKeyExists(local, "exception")) {
                transaction action="rollback";
                Throw(
                    errorCode="1",
                    detail=local.exception.detail,
                    message=local.exception.message,
                    type="any"
                );
            } else {
                transaction action="commit";
            }
        }
    }

    function down() {
        // Rollback code here
    }
}
```

## Create Table Migration

```cfm
component extends="wheels.migrator.Migration" {

    function up() {
        transaction {
            try {
                // Create table
                t = createTable(name="posts", force=false);

                // String columns
                t.string(columnNames="title", allowNull=false, limit=200);
                t.string(columnNames="slug", allowNull=false, limit=200);

                // Text columns
                t.text(columnNames="content", allowNull=false);
                t.text(columnNames="excerpt", allowNull=true);

                // Integer columns
                t.integer(columnNames="viewCount", default=0);
                t.integer(columnNames="userId", allowNull=false);

                // Boolean columns
                t.boolean(columnNames="published", default=false);

                // DateTime columns
                t.datetime(columnNames="publishedAt", allowNull=true);

                // Timestamps (createdAt, updatedAt)
                t.timestamps();

                // Create the table
                t.create();

                // Add indexes
                addIndex(table="posts", columnNames="slug", unique=true);
                addIndex(table="posts", columnNames="userId");
                addIndex(table="posts", columnNames="published,publishedAt");

                // Add foreign key
                addForeignKey(
                    table="posts",
                    referenceTable="users",
                    column="userId",
                    referenceColumn="id",
                    onDelete="cascade"
                );

            } catch (any e) {
                local.exception = e;
            }

            if (StructKeyExists(local, "exception")) {
                transaction action="rollback";
                Throw(
                    errorCode="1",
                    detail=local.exception.detail,
                    message=local.exception.message,
                    type="any"
                );
            } else {
                transaction action="commit";
            }
        }
    }

    function down() {
        dropTable("posts");
    }
}
```

## Alter Table Migration

```cfm
component extends="wheels.migrator.Migration" {

    function up() {
        transaction {
            try {
                // Add column
                addColumn(
                    table="posts",
                    columnType="string",
                    columnName="metaDescription",
                    limit=300,
                    allowNull=true
                );

                // Change column
                changeColumn(
                    table="posts",
                    columnName="title",
                    columnType="string",
                    limit=255,  // Changed from 200
                    allowNull=false
                );

                // Rename column
                renameColumn(
                    table="posts",
                    oldColumnName="summary",
                    newColumnName="excerpt"
                );

                // Remove column
                removeColumn(table="posts", columnName="oldField");

                // Add index
                addIndex(table="posts", columnNames="metaDescription");

            } catch (any e) {
                local.exception = e;
            }

            if (StructKeyExists(local, "exception")) {
                transaction action="rollback";
                Throw(
                    errorCode="1",
                    detail=local.exception.detail,
                    message=local.exception.message,
                    type="any"
                );
            } else {
                transaction action="commit";
            }
        }
    }

    function down() {
        removeColumn(table="posts", columnName="metaDescription");
        // Reverse other changes...
    }
}
```

## Data Migration (Seed Data)

### Database-Agnostic Date Formatting

```cfm
component extends="wheels.migrator.Migration" {

    function up() {
        transaction {
            try {
                // CORRECT: Use CFML date functions
                var now = Now();
                var day1 = DateAdd("d", -7, now);
                var day2 = DateAdd("d", -6, now);
                var day3 = DateAdd("d", -5, now);

                // Format dates for SQL
                var nowFormatted = "TIMESTAMP '#DateFormat(now, "yyyy-mm-dd")# #TimeFormat(now, "HH:mm:ss")#'";
                var day1Formatted = "TIMESTAMP '#DateFormat(day1, "yyyy-mm-dd")# #TimeFormat(day1, "HH:mm:ss")#'";
                var day2Formatted = "TIMESTAMP '#DateFormat(day2, "yyyy-mm-dd")# #TimeFormat(day2, "HH:mm:ss")#'";

                // Insert data
                execute("
                    INSERT INTO posts (title, slug, content, published, publishedAt, createdAt, updatedAt)
                    VALUES (
                        'Getting Started with HTMX',
                        'getting-started-with-htmx',
                        '<p>HTMX is a modern approach to building web applications...</p>',
                        1,
                        #day1Formatted#,
                        #day1Formatted#,
                        #day1Formatted#
                    )
                ");

                execute("
                    INSERT INTO posts (title, slug, content, published, publishedAt, createdAt, updatedAt)
                    VALUES (
                        'Tailwind CSS Best Practices',
                        'tailwind-css-best-practices',
                        '<p>Tailwind provides utility-first CSS...</p>',
                        1,
                        #day2Formatted#,
                        #day2Formatted#,
                        #day2Formatted#
                    )
                ");

            } catch (any e) {
                local.exception = e;
            }

            if (StructKeyExists(local, "exception")) {
                transaction action="rollback";
                Throw(
                    errorCode="1",
                    detail=local.exception.detail,
                    message=local.exception.message,
                    type="any"
                );
            } else {
                transaction action="commit";
            }
        }
    }

    function down() {
        execute("DELETE FROM posts WHERE slug IN ('getting-started-with-htmx', 'tailwind-css-best-practices')");
    }
}
```

## Column Types

### Available Column Types

```cfm
// String (VARCHAR)
t.string(columnNames="name", limit=255, allowNull=false, default="");

// Text (TEXT/CLOB)
t.text(columnNames="description", allowNull=true);

// Integer
t.integer(columnNames="count", default=0, allowNull=false);

// Big Integer
t.biginteger(columnNames="largeNumber");

// Float
t.float(columnNames="rating", default=0.0);

// Decimal
t.decimal(columnNames="price", precision=10, scale=2);

// Boolean
t.boolean(columnNames="active", default=true);

// Date
t.date(columnNames="birthDate");

// DateTime
t.datetime(columnNames="publishedAt");

// Time
t.time(columnNames="startTime");

// Binary
t.binary(columnNames="fileData");

// UUID
t.string(columnNames="uuid", limit=36);

// Timestamps (adds createdAt and updatedAt)
t.timestamps();
```

## 🚨 Production-Tested Critical Fixes

### 1. CLI Generator Boolean Parameter Bug (CRITICAL)

**🔴 CRITICAL DISCOVERY:** The CLI generator `wheels g migration` creates migrations with **string boolean values** instead of actual booleans, causing silent failures.

**Problem Generated by CLI:**
```cfm
// ❌ CLI generates this - STRING values that don't work!
t = createTable(name='users', force='false', id='true', primaryKey='id');
```

**Symptoms:**
- Migration reports success but table isn't created correctly
- "NoPrimaryKey" errors even though migration succeeded
- Primary key not properly configured in database
- Wheels ORM can't find primary key column

**✅ SOLUTION: Simplify to Use Defaults**
```cfm
// Remove all explicit boolean parameters - let Wheels use defaults
t = createTable(name='users');  // That's it!
t.string(columnNames='username', allowNull=false, limit='50');
t.timestamps();
t.create();
```

**Why This Works:**
- Wheels `createTable()` has correct default behavior
- Explicit string booleans (`'false'`, `'true'`) break the logic
- Omitting parameters lets Wheels handle it correctly
- Default: creates 'id' as primary key automatically

**MANDATORY Post-CLI-Generation Fix:**
```cfm
// 1. Find this pattern in generated migration:
t = createTable(name='tablename', force='false', id='true', primaryKey='id');

// 2. Replace with:
t = createTable(name='tablename');
```

**Rule:**
```
✅ MANDATORY: After CLI generation, remove force/id/primaryKey parameters from createTable()
❌ NEVER use string boolean values: 'false', 'true'
✅ Use actual booleans IF needed: false, true (but defaults are better)
```

### 2. Migration Development Workflow

**🔴 LESSON LEARNED:** When migrations fail or you need to iterate, always reset before running latest.

**Standard Development Workflow:**
```bash
# 1. Generate migration
wheels g migration CreateUsersTable

# 2. Edit migration file (fix CLI-generated issues!)

# 3. ALWAYS reset before running during development
wheels dbmigrate reset   # Drops all tables, clean slate
wheels dbmigrate latest  # Run all migrations fresh

# 4. If migration fails, fix it then:
wheels dbmigrate reset   # Reset again
wheels dbmigrate latest  # Try again
```

**Why Reset is Important:**
- Failed migrations may leave partial tables
- Partial tables prevent subsequent migrations from running
- Reset ensures clean database state
- Catches migration errors early

**Production Workflow (Different!):**
```bash
# In production, NEVER reset!
wheels dbmigrate latest  # Only run new migrations
```

### 3. Composite Index Ordering (CRITICAL)

**❌ WRONG ORDER - Causes Index Conflicts:**
```cfm
addIndex(table="likes", columnNames="userId");      // ❌ Creates duplicate
addIndex(table="likes", columnNames="tweetId");
addIndex(table="likes", columnNames="userId,tweetId", unique=true);
```

**✅ CORRECT ORDER - Composite First:**
```cfm
// Composite index FIRST - it covers queries on the first column too!
addIndex(table="likes", columnNames="userId,tweetId", unique=true);
// Then add index for second column only
addIndex(table="likes", columnNames="tweetId");
```

**Why:** A composite index on `(userId, tweetId)` can be used for queries filtering by `userId` alone, making a separate `userId` index redundant.

### 2. Foreign Key Naming for Self-Referential Tables

**Problem:** Multiple foreign keys to the same table generate duplicate constraint names in H2:

```cfm
// ❌ Both try to create "FK_FOLLOWS_USERS" - conflict!
addForeignKey(table="follows", referenceTable="users", column="followerId")
addForeignKey(table="follows", referenceTable="users", column="followingId")
```

**Solution A: Explicit Key Names (Preferred for Production)**
```cfm
addForeignKey(
    table="follows",
    referenceTable="users",
    column="followerId",
    referenceColumn="id",
    keyName="FK_follows_follower",  // Explicit unique name
    onDelete="cascade"
);

addForeignKey(
    table="follows",
    referenceTable="users",
    column="followingId",
    referenceColumn="id",
    keyName="FK_follows_following",  // Different unique name
    onDelete="cascade"
);
```

**Solution B: Skip Foreign Keys (Acceptable for Development)**
```cfm
// Rely on application-layer validation instead
// Indexes provide query performance, foreign keys are optional
addIndex(table="follows", columnNames="followerId,followingId", unique=true);
addIndex(table="follows", columnNames="followingId");
// Note: Foreign keys omitted to avoid H2 naming conflicts
// Application validates referential integrity
```

### 3. Migration Retry with force=true

When migrations fail mid-transaction (common during development):

```cfm
// Use force=true to drop and recreate if table exists
t = createTable(name="likes", force=true);  // Drops existing table first
```

**When to use:**
- ✅ After failed migration leaves partial tables
- ✅ During development when iterating on schema
- ❌ NOT recommended for production (use proper versioning)

### 4. Join Table Pattern

For many-to-many relationships (e.g., likes, follows):

```cfm
t = createTable(name="likes", force=true);
t.integer(columnNames="userId", allowNull=false);
t.integer(columnNames="tweetId", allowNull=false);
t.datetime(columnNames="createdAt", allowNull=false);  // Track when relationship created
t.create();

// IMPORTANT: Composite unique index FIRST
addIndex(table="likes", columnNames="userId,tweetId", unique=true);
addIndex(table="likes", columnNames="tweetId");  // For reverse lookups
```

## Index Management

```cfm
// Simple index
addIndex(table="posts", columnNames="title");

// Unique index
addIndex(table="posts", columnNames="slug", unique=true);

// Composite index
addIndex(table="posts", columnNames="published,publishedAt");

// Remove index
removeIndex(table="posts", indexName="idx_posts_title");
```

## Foreign Key Management

```cfm
// Add foreign key
addForeignKey(
    table="posts",
    referenceTable="users",
    column="userId",
    referenceColumn="id",
    onDelete="cascade",  // Options: cascade, setNull, setDefault, restrict
    onUpdate="cascade"
);

// Remove foreign key
removeForeignKey(table="posts", keyName="fk_posts_userId");
```

## Join Table Migration

```cfm
component extends="wheels.migrator.Migration" {

    function up() {
        transaction {
            try {
                // Create join table for many-to-many
                t = createTable(name="postTags", force=false);
                t.integer(columnNames="postId", allowNull=false);
                t.integer(columnNames="tagId", allowNull=false);
                t.timestamps();
                t.create();

                // Add indexes
                addIndex(table="postTags", columnNames="postId");
                addIndex(table="postTags", columnNames="tagId");
                addIndex(table="postTags", columnNames="postId,tagId", unique=true);

                // Add foreign keys
                addForeignKey(
                    table="postTags",
                    referenceTable="posts",
                    column="postId",
                    referenceColumn="id",
                    onDelete="cascade"
                );

                addForeignKey(
                    table="postTags",
                    referenceTable="tags",
                    column="tagId",
                    referenceColumn="id",
                    onDelete="cascade"
                );

            } catch (any e) {
                local.exception = e;
            }

            if (StructKeyExists(local, "exception")) {
                transaction action="rollback";
                Throw(
                    errorCode="1",
                    detail=local.exception.detail,
                    message=local.exception.message,
                    type="any"
                );
            } else {
                transaction action="commit";
            }
        }
    }

    function down() {
        dropTable("postTags");
    }
}
```

## Implementation Checklist

When generating a migration:

- [ ] Extends wheels.migrator.Migration
- [ ] Wrapped in transaction block
- [ ] Try/catch for error handling
- [ ] Rollback on exception
- [ ] Commit on success
- [ ] Use CFML date functions (NOT SQL date functions)
- [ ] Format dates with DateFormat/TimeFormat
- [ ] Include down() method for rollback
- [ ] Add appropriate indexes
- [ ] Add foreign keys where needed
- [ ] Use database-agnostic column types

## Common Patterns

### Adding Soft Delete

```cfm
addColumn(
    table="posts",
    columnType="datetime",
    columnName="deletedAt",
    allowNull=true
);
addIndex(table="posts", columnNames="deletedAt");
```

### Adding Full Text Search

```cfm
// Add column for search
addColumn(
    table="posts",
    columnType="text",
    columnName="searchContent",
    allowNull=true
);

// Create search index (database-specific, document it)
// For PostgreSQL: CREATE INDEX ... USING GIN
// For MySQL: CREATE FULLTEXT INDEX
```

### Adding Versioning

```cfm
addColumn(table="posts", columnType="integer", columnName="version", default=1);
addColumn(table="posts", columnType="integer", columnName="lockVersion", default=0);
```

## Migration Commands

```bash
# Create new migration
wheels g migration CreatePostsTable

# Run pending migrations
wheels dbmigrate latest

# Run single migration
wheels dbmigrate up

# Rollback last migration
wheels dbmigrate down

# Show migration status
wheels dbmigrate info
```

## Related Skills

- **wheels-model-generator**: Creates models for tables
- **wheels-anti-pattern-detector**: Validates migration code

---

**Generated by:** Wheels Migration Generator Skill v1.0
**Framework:** CFWheels 3.0+
**Last Updated:** 2025-10-20
