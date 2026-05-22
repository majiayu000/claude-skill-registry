---
name: database-design
slug: database-design
version: 1.0.0
category: core
description: Design database schemas using Drizzle ORM from natural language descriptions
triggers:
  - pattern: "database|schema|table|entity|model|migration"
    confidence: 0.6
    examples:
      - "create a database schema"
      - "design tables for a blog"
      - "I need entity models for my app"
      - "create a migration for users"
      - "design a schema with users and posts"
mcp_dependencies:
  - server: supabase
    required: false
    capabilities:
      - "query"
      - "schema"
  - server: context7
    required: false
    capabilities:
      - "search"
---

# Database Design Skill

Automatically design database schemas using Drizzle ORM from natural language descriptions. This skill analyzes user requirements, extracts entities, detects relationships, and generates production-ready Drizzle schema files with proper TypeScript types.

## Overview

This skill transforms natural language database requirements into:
- **Drizzle ORM schema files** (TypeScript)
- **TypeScript type definitions** (Insert/Select types)
- **Migration SQL** (PostgreSQL)
- **Relationship mappings** (foreign keys, joins)

## When to Use This Skill

Activate this skill when the user requests:
- Database schema design
- Table creation
- Entity modeling
- Data model design
- Database migrations
- Schema modifications

## Key Features

### 1. Entity Extraction
Automatically identifies entities (tables) from natural language:
- "Create a schema with **users** and **posts**"
- "I need **products**, **orders**, and **customers** tables"
- Table names extracted from nouns and context

### 2. Field Detection
Extracts fields and properties for each entity:
- "users have **id**, **name**, **email**, and **createdAt**"
- Infers field types from context (text, integer, boolean, timestamp)
- Adds common fields automatically (id, createdAt, updatedAt)

### 3. Relationship Detection
Understands relationships from verbs and relationship indicators:

**One-to-Many:**
- "users **write** posts" → posts.userId references users.id
- "posts **have** comments" → comments.postId references posts.id
- "X **has many** Y" → Y has foreign key to X

**Many-to-One:**
- "comments **belong to** posts" → comments.postId references posts.id
- "X **belongs to** Y" → X has foreign key to Y

**Many-to-Many:**
- "users can have many roles, and roles can have many users"
- Creates join table: userRoles(userId, roleId)

### 4. Drizzle ORM Schema Generation
Generates production-ready Drizzle schemas:

```typescript
import { pgTable, text, timestamp } from 'drizzle-orm/pg-core'

export const users = pgTable('users', {
  id: text('id').primaryKey(),
  name: text('name').notNull(),
  email: text('email').notNull(),
  createdAt: timestamp('created_at').defaultNow().notNull(),
  updatedAt: timestamp('updated_at').defaultNow().notNull(),
})

export const posts = pgTable('posts', {
  id: text('id').primaryKey(),
  title: text('title').notNull(),
  content: text('content'),
  userId: text('user_id').notNull().references(() => users.id, { onDelete: 'cascade' }),
  createdAt: timestamp('created_at').defaultNow().notNull(),
  updatedAt: timestamp('updated_at').defaultNow().notNull(),
})
```

### 5. TypeScript Type Generation
Automatically creates Insert and Select types:

```typescript
export type User = typeof users.$inferSelect
export type InsertUser = typeof users.$inferInsert

export type Post = typeof posts.$inferSelect
export type InsertPost = typeof posts.$inferInsert
```

### 6. Migration SQL Generation
Creates PostgreSQL migration scripts:

```sql
CREATE TABLE users (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW() NOT NULL,
  updated_at TIMESTAMP DEFAULT NOW() NOT NULL
);

CREATE TABLE posts (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  content TEXT,
  user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  created_at TIMESTAMP DEFAULT NOW() NOT NULL,
  updated_at TIMESTAMP DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_posts_user_id ON posts(user_id);
```

## Execution Steps

When this skill is activated, it will:

1. **Parse User Requirements**
   - Extract entity names from prompt
   - Identify fields for each entity
   - Detect field types from context

2. **Detect Relationships**
   - Analyze verbs and relationship keywords
   - Determine relationship types (1:1, 1:N, N:M)
   - Identify foreign keys and join tables

3. **Generate Drizzle Schemas**
   - Create TypeScript schema files
   - Add proper imports and exports
   - Include relationship definitions

4. **Create TypeScript Types**
   - Generate Insert types
   - Generate Select types
   - Export all types

5. **Generate Migration SQL**
   - Create table definitions
   - Add foreign key constraints
   - Create indexes for foreign keys

6. **Write Output Files**
   - `lib/db/schema/{entity}.ts` - Individual schema files
   - `lib/db/schema/index.ts` - Barrel export
   - `migrations/{timestamp}_create_{entities}.sql` - Migration file

## Usage Examples

### Example 1: Simple Blog Schema
**User Prompt:**
"Create a database schema for a blog with users and posts. Users write posts."

**Generated Output:**
- `lib/db/schema/users.ts` - Users table schema
- `lib/db/schema/posts.ts` - Posts table with userId foreign key
- `lib/db/schema/index.ts` - Exports both schemas
- `migrations/001_create_blog_schema.sql` - Migration SQL

### Example 2: E-commerce Schema
**User Prompt:**
"Design a schema for an e-commerce app with products, orders, and customers. Customers place orders, and orders contain products."

**Generated Output:**
- Schemas for: customers, orders, products, orderItems (join table)
- Foreign keys: orders.customerId, orderItems.orderId, orderItems.productId
- Complete migration SQL with indexes

### Example 3: Social Media Schema
**User Prompt:**
"I need a schema with users, posts, comments, and likes. Users write posts and comments. Users can like posts and comments."

**Generated Output:**
- 5 schemas: users, posts, comments, postLikes, commentLikes
- Complex relationships with multiple foreign keys
- Composite primary keys for like tables

## Field Type Inference

The skill automatically infers PostgreSQL/Drizzle types:

| Context Keywords | Drizzle Type | PostgreSQL Type |
|-----------------|-------------|-----------------|
| "id", "ID" | text | TEXT |
| "name", "title", "email", "username" | text | TEXT |
| "description", "content", "bio" | text | TEXT |
| "age", "count", "quantity" | integer | INTEGER |
| "price", "amount" | numeric | NUMERIC |
| "isActive", "hasPermission", "enabled" | boolean | BOOLEAN |
| "createdAt", "updatedAt", "publishedAt" | timestamp | TIMESTAMP |
| "date", "birthday" | timestamp | TIMESTAMP |
| "tags", "roles" | jsonb | JSONB (array) |

## Best Practices

### Naming Conventions
- **Tables:** Plural, snake_case (users, user_profiles)
- **Fields:** camelCase in TypeScript, snake_case in SQL
- **Foreign Keys:** {entity}Id (userId, postId)
- **Join Tables:** {entity1}{Entity2} (userRoles, postTags)

### Default Fields
Automatically added to all tables:
- `id: text('id').primaryKey()` - UUID primary key
- `createdAt: timestamp('created_at').defaultNow().notNull()`
- `updatedAt: timestamp('updated_at').defaultNow().notNull()`

### Foreign Key Options
- `onDelete: 'cascade'` - Delete child records when parent is deleted
- `onUpdate: 'cascade'` - Update child records when parent ID changes
- Indexes automatically created for foreign keys

### Schema Organization
- One file per entity in `lib/db/schema/`
- Barrel export in `lib/db/schema/index.ts`
- Shared types in separate file if needed

## MCP Integration

### Supabase (Optional)
When Supabase MCP is available:
- Directly create tables in Supabase database
- Run migrations automatically
- Sync schema with remote database

### Context7 (Optional)
When Context7 MCP is available:
- Search Drizzle ORM documentation
- Find schema examples from codebase
- Reference existing patterns

## Error Handling

The skill handles:
- **Ambiguous entities:** Asks for clarification
- **Unknown types:** Uses TEXT as default, suggests options
- **Circular references:** Detects and reports
- **Invalid relationships:** Suggests corrections

## Output Format

All generated files follow this structure:

```
lib/db/schema/
  ├── users.ts
  ├── posts.ts
  ├── comments.ts
  └── index.ts

migrations/
  └── 001_create_blog_schema.sql
```

## Success Criteria

The skill execution is successful when:
1. All entities are extracted from prompt
2. Relationships are correctly identified
3. Generated schemas are valid TypeScript
4. Migration SQL is valid PostgreSQL
5. All files are written to correct locations
6. No syntax errors in generated code

## Limitations

- PostgreSQL only (uses pgTable from Drizzle)
- Text-based IDs (can be customized to use UUID/serial)
- Basic field types (can be extended for advanced types)
- English language prompts only

## Future Enhancements

- Support for MySQL/SQLite via Drizzle
- Advanced field types (arrays, JSON, enums)
- Schema validation and linting
- Automatic test data generation
- Schema visualization (ERD diagrams)
- Schema diffing and migration generation

---

**Skill Version:** 1.0.0
**Last Updated:** 2026-01-04
**Maintainer:** Turbocat Agent System
