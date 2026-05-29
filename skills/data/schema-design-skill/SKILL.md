---
document_name: "schema-design.skill.md"
location: ".claude/skills/schema-design.skill.md"
codebook_id: "CB-SKILL-SCHEMA-001"
version: "1.0.0"
date_created: "2026-01-04"
date_last_edited: "2026-01-04"
document_type: "skill"
purpose: "Procedures for database schema design"
skill_metadata:
  category: "development"
  complexity: "advanced"
  estimated_time: "varies"
  prerequisites:
    - "Database fundamentals"
    - "SQL knowledge"
category: "skills"
status: "active"
tags:
  - "skill"
  - "database"
  - "schema"
  - "design"
ai_parser_instructions: |
  This skill defines procedures for schema design.
  Used by Database Engineer agent.
---

# Schema Design Skill

=== PURPOSE ===

Procedures for designing and documenting database schemas.

=== USED BY ===

| Agent | Purpose |
|-------|---------|
| @agent(database-engineer) @ref(CB-AGENT-DATABASE-001) | Primary skill for schema work |

=== PROCEDURE: Naming Conventions ===

**Tables:**
```
✓ users              (plural, lowercase)
✓ order_items        (snake_case for multi-word)
✓ user_roles         (join tables: table1_table2)
✗ User, Users        (no PascalCase)
✗ tbl_users          (no prefixes)
```

**Columns:**
```
✓ created_at         (snake_case)
✓ user_id            (foreign key: table_id)
✓ is_active          (boolean: is_ prefix)
✓ has_verified       (boolean: has_ prefix)
✗ createdAt          (no camelCase)
✗ ID, Id             (no inconsistent casing)
```

**Indexes:**
```
idx_{table}_{column}           # Single column
idx_{table}_{col1}_{col2}      # Composite
uniq_{table}_{column}          # Unique constraint
```

**Foreign Keys:**
```
fk_{table}_{referenced_table}
```

=== PROCEDURE: Required Columns ===

**Every Table Must Have:**
```sql
id          UUID PRIMARY KEY DEFAULT gen_random_uuid()
created_at  TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
updated_at  TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
```

**For Soft Delete:**
```sql
deleted_at  TIMESTAMP WITH TIME ZONE  -- NULL = active
```

**Update Trigger (PostgreSQL):**
```sql
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_updated_at
  BEFORE UPDATE ON {table_name}
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at();
```

=== PROCEDURE: Data Types ===

**Type Selection Guide:**

| Data | Recommended Type | Notes |
|------|------------------|-------|
| ID | UUID | Use gen_random_uuid() |
| Short text | VARCHAR(n) | Specify max length |
| Long text | TEXT | No length limit |
| Boolean | BOOLEAN | NOT NULL, default value |
| Integer | INTEGER | 4 bytes, ±2 billion |
| Big integer | BIGINT | 8 bytes, for IDs from external systems |
| Decimal | DECIMAL(p,s) | For money, exact values |
| Timestamp | TIMESTAMPTZ | Always with timezone |
| Date | DATE | When time not needed |
| JSON | JSONB | Binary JSON, indexable |
| Enum | VARCHAR + CHECK | Or native ENUM type |

**Money Handling:**
```sql
-- Use DECIMAL for money, never FLOAT
amount DECIMAL(19, 4) NOT NULL
```

=== PROCEDURE: Relationship Design ===

**One-to-Many:**
```sql
-- Parent table
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(100) NOT NULL
);

-- Child table
CREATE TABLE posts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title VARCHAR(255) NOT NULL
);

CREATE INDEX idx_posts_user_id ON posts(user_id);
```

**Many-to-Many:**
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid()
);

CREATE TABLE roles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid()
);

-- Join table
CREATE TABLE user_roles (
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  role_id UUID NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
  assigned_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (user_id, role_id)
);
```

**Self-Referential:**
```sql
CREATE TABLE categories (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(100) NOT NULL,
  parent_id UUID REFERENCES categories(id) ON DELETE SET NULL
);

CREATE INDEX idx_categories_parent_id ON categories(parent_id);
```

=== PROCEDURE: Index Strategy ===

**When to Index:**
- Primary keys (automatic)
- Foreign keys (always)
- Columns in WHERE clauses (frequently queried)
- Columns in ORDER BY (if sorted often)
- Columns in JOIN conditions
- Unique constraints

**Composite Indexes:**
```sql
-- Order matters! Most selective column first
CREATE INDEX idx_orders_status_date
  ON orders(status, created_at);

-- This index supports:
-- WHERE status = 'pending'
-- WHERE status = 'pending' AND created_at > '2024-01-01'
-- NOT: WHERE created_at > '2024-01-01' (use separate index)
```

**Partial Indexes:**
```sql
-- Index only active records
CREATE INDEX idx_users_email_active
  ON users(email)
  WHERE deleted_at IS NULL;
```

=== PROCEDURE: Constraints ===

**Types:**
```sql
-- NOT NULL
email VARCHAR(255) NOT NULL

-- UNIQUE
email VARCHAR(255) UNIQUE NOT NULL

-- CHECK
age INTEGER CHECK (age >= 0 AND age <= 150)
status VARCHAR(20) CHECK (status IN ('pending', 'active', 'closed'))

-- FOREIGN KEY with actions
user_id UUID REFERENCES users(id)
  ON DELETE CASCADE    -- Delete children when parent deleted
  ON DELETE SET NULL   -- Nullify when parent deleted
  ON DELETE RESTRICT   -- Prevent deletion if children exist
```

=== PROCEDURE: Schema Documentation ===

**Document Each Table:**
```markdown
## users

User accounts in the system.

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| id | UUID | NO | gen_random_uuid() | Primary key |
| email | VARCHAR(255) | NO | - | Unique email address |
| name | VARCHAR(100) | NO | - | Display name |
| role | VARCHAR(20) | NO | 'user' | User role (user/admin) |
| created_at | TIMESTAMPTZ | NO | now() | Creation timestamp |

### Indexes
- `idx_users_email` - Unique index on email
- `idx_users_role` - For role-based queries

### Relationships
- Has many `posts` (user_id)
- Has many `comments` (user_id)
```

=== RELATED SKILLS ===

| Skill | Relationship |
|-------|--------------|
| @skill(migration-management) | Schema changes |
| @skill(backend-patterns) | Data layer integration |
