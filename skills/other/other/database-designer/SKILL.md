---
name: database-designer
description: 设计和优化数据库模式，支持PostgreSQL、MySQL、SQLite和MongoDB。包括ER建模、规范化、索引优化和迁移脚本生成。
metadata:
  short-description: 设计数据库模式和迁移脚本
---

# Database Designer Skill

## Description
Design and optimize database schemas with Entity-Relationship modeling, normalization, and migration scripts.

## Trigger
- `/db-design` command
- User requests database schema design
- User needs migration scripts

## Prompt

You are a database architect that designs efficient, scalable database schemas.

### PostgreSQL Schema Example

```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    avatar_url TEXT,
    email_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create index for email lookups
CREATE INDEX idx_users_email ON users(email);

-- Posts table with foreign key
CREATE TABLE posts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    status VARCHAR(20) DEFAULT 'draft' CHECK (status IN ('draft', 'published', 'archived')),
    published_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Composite index for user's posts
CREATE INDEX idx_posts_user_status ON posts(user_id, status);

-- Full-text search index
CREATE INDEX idx_posts_search ON posts USING GIN(to_tsvector('english', title || ' ' || content));

-- Updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

### Entity Framework Core Migration

```csharp
public class CreateUsersTable : Migration
{
    protected override void Up(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.CreateTable(
            name: "Users",
            columns: table => new
            {
                Id = table.Column<Guid>(nullable: false, defaultValueSql: "gen_random_uuid()"),
                Email = table.Column<string>(maxLength: 255, nullable: false),
                PasswordHash = table.Column<string>(maxLength: 255, nullable: false),
                Name = table.Column<string>(maxLength: 100, nullable: false),
                CreatedAt = table.Column<DateTime>(nullable: false, defaultValueSql: "NOW()")
            },
            constraints: table =>
            {
                table.PrimaryKey("PK_Users", x => x.Id);
            });

        migrationBuilder.CreateIndex(
            name: "IX_Users_Email",
            table: "Users",
            column: "Email",
            unique: true);
    }

    protected override void Down(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.DropTable(name: "Users");
    }
}
```

### Index Optimization Guidelines

```sql
-- Good: Selective index on frequently queried column
CREATE INDEX idx_orders_status ON orders(status) WHERE status = 'pending';

-- Good: Covering index for common query
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at DESC) INCLUDE (total, status);

-- Avoid: Index on low-cardinality column
-- CREATE INDEX idx_users_active ON users(is_active); -- Only 2 values!
```

## Tags
`database`, `sql`, `schema`, `design`, `optimization`, `migration`

## Compatibility
- Codex: ✅
- Claude Code: ✅
