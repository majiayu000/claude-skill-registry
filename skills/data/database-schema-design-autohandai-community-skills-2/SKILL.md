---
name: database-schema-design
description: Database schema design patterns for SQL and NoSQL databases
license: MIT
compatibility: postgresql 14+, drizzle-orm 0.28+, prisma 5+
allowed-tools: read_file write_file apply_patch run_command
---

# Database Schema Design

## Core Principles

1. **Normalize first, denormalize for performance**
2. **Use appropriate data types** - smallest type that fits
3. **Index strategically** - based on query patterns
4. **Plan for growth** - consider partitioning early

## Naming Conventions

```sql
-- Tables: plural, snake_case
users, order_items, user_addresses

-- Columns: snake_case
first_name, created_at, is_active

-- Primary keys: id
id SERIAL PRIMARY KEY

-- Foreign keys: singular_table_id
user_id REFERENCES users(id)

-- Indexes: idx_table_column(s)
CREATE INDEX idx_users_email ON users(email);

-- Constraints: chk_/uq_/fk_ prefix
CONSTRAINT uq_users_email UNIQUE (email)
CONSTRAINT chk_orders_amount CHECK (amount > 0)
```

## Common Patterns

### Users Table
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  name VARCHAR(100) NOT NULL,
  role VARCHAR(20) DEFAULT 'user' CHECK (role IN ('user', 'admin', 'moderator')),
  is_active BOOLEAN DEFAULT true,
  email_verified_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role) WHERE is_active = true;
```

### One-to-Many Relationship
```sql
CREATE TABLE posts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title VARCHAR(255) NOT NULL,
  content TEXT,
  status VARCHAR(20) DEFAULT 'draft',
  published_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_posts_user_id ON posts(user_id);
CREATE INDEX idx_posts_status_published ON posts(status, published_at DESC)
  WHERE status = 'published';
```

### Many-to-Many Relationship
```sql
CREATE TABLE tags (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) NOT NULL UNIQUE,
  slug VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE post_tags (
  post_id UUID REFERENCES posts(id) ON DELETE CASCADE,
  tag_id INTEGER REFERENCES tags(id) ON DELETE CASCADE,
  PRIMARY KEY (post_id, tag_id)
);

CREATE INDEX idx_post_tags_tag_id ON post_tags(tag_id);
```

### Polymorphic Associations
```sql
-- Using separate tables (preferred)
CREATE TABLE post_comments (
  id UUID PRIMARY KEY,
  post_id UUID REFERENCES posts(id),
  content TEXT NOT NULL,
  user_id UUID REFERENCES users(id)
);

CREATE TABLE image_comments (
  id UUID PRIMARY KEY,
  image_id UUID REFERENCES images(id),
  content TEXT NOT NULL,
  user_id UUID REFERENCES users(id)
);

-- Alternative: Single table with type column
CREATE TABLE comments (
  id UUID PRIMARY KEY,
  commentable_type VARCHAR(50) NOT NULL,
  commentable_id UUID NOT NULL,
  content TEXT NOT NULL,
  user_id UUID REFERENCES users(id),
  CONSTRAINT uq_comments_target UNIQUE (commentable_type, commentable_id, id)
);
```

## Drizzle ORM Schema

```typescript
import { pgTable, uuid, varchar, text, timestamp, boolean, index } from 'drizzle-orm/pg-core';
import { relations } from 'drizzle-orm';

export const users = pgTable('users', {
  id: uuid('id').primaryKey().defaultRandom(),
  email: varchar('email', { length: 255 }).notNull().unique(),
  name: varchar('name', { length: 100 }).notNull(),
  passwordHash: varchar('password_hash', { length: 255 }).notNull(),
  isActive: boolean('is_active').default(true),
  createdAt: timestamp('created_at', { withTimezone: true }).defaultNow(),
  updatedAt: timestamp('updated_at', { withTimezone: true }).defaultNow(),
}, (table) => ({
  emailIdx: index('idx_users_email').on(table.email),
}));

export const posts = pgTable('posts', {
  id: uuid('id').primaryKey().defaultRandom(),
  userId: uuid('user_id').notNull().references(() => users.id, { onDelete: 'cascade' }),
  title: varchar('title', { length: 255 }).notNull(),
  content: text('content'),
  status: varchar('status', { length: 20 }).default('draft'),
  publishedAt: timestamp('published_at', { withTimezone: true }),
  createdAt: timestamp('created_at', { withTimezone: true }).defaultNow(),
});

export const usersRelations = relations(users, ({ many }) => ({
  posts: many(posts),
}));

export const postsRelations = relations(posts, ({ one }) => ({
  author: one(users, {
    fields: [posts.userId],
    references: [users.id],
  }),
}));
```

## Indexing Strategies

```sql
-- Single column index
CREATE INDEX idx_users_email ON users(email);

-- Composite index (order matters!)
CREATE INDEX idx_posts_user_status ON posts(user_id, status);

-- Partial index (smaller, faster)
CREATE INDEX idx_posts_published ON posts(published_at DESC)
  WHERE status = 'published';

-- Expression index
CREATE INDEX idx_users_email_lower ON users(LOWER(email));

-- JSONB index
CREATE INDEX idx_users_metadata ON users USING GIN(metadata);
```

## Soft Deletes

```sql
CREATE TABLE posts (
  id UUID PRIMARY KEY,
  -- other columns...
  deleted_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Query active records
SELECT * FROM posts WHERE deleted_at IS NULL;

-- Partial index for performance
CREATE INDEX idx_posts_active ON posts(created_at DESC)
  WHERE deleted_at IS NULL;
```

## Audit Trail

```sql
CREATE TABLE audit_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  table_name VARCHAR(100) NOT NULL,
  record_id UUID NOT NULL,
  action VARCHAR(20) NOT NULL, -- INSERT, UPDATE, DELETE
  old_data JSONB,
  new_data JSONB,
  user_id UUID REFERENCES users(id),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Trigger function
CREATE OR REPLACE FUNCTION audit_trigger_func()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO audit_logs (table_name, record_id, action, old_data, new_data, user_id)
  VALUES (
    TG_TABLE_NAME,
    COALESCE(NEW.id, OLD.id),
    TG_OP,
    CASE WHEN TG_OP != 'INSERT' THEN row_to_json(OLD) END,
    CASE WHEN TG_OP != 'DELETE' THEN row_to_json(NEW) END,
    current_setting('app.current_user_id', true)::uuid
  );
  RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;
```

## Best Practices

1. **Always use UUIDs** for public-facing IDs
2. **Add timestamps** (created_at, updated_at) to all tables
3. **Use foreign key constraints** for referential integrity
4. **Create indexes based on queries** not assumptions
5. **Use ENUM types sparingly** - prefer check constraints
6. **Plan for soft deletes** if business requires audit trail
7. **Use transactions** for multi-table operations
8. **Partition large tables** by time or category
