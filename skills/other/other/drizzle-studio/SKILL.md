---
name: drizzle-studio
description: >-
  Explore and manage databases with Drizzle Studio. Use when a user asks to
  browse database contents visually, inspect tables and data, run ad-hoc queries,
  manage database records through a GUI, debug database issues, or use a
  lightweight alternative to pgAdmin or DBeaver. Covers setup with Drizzle ORM,
  standalone usage, data browsing, filtering, and inline editing.
license: Apache-2.0
compatibility: 'Node.js 18+ (PostgreSQL, MySQL, SQLite)'
metadata:
  author: terminal-skills
  version: 1.0.0
  category: data-ai
  tags:
    - drizzle
    - database
    - gui
    - admin
    - studio
---

# Drizzle Studio

## Overview

Drizzle Studio is a visual database browser and admin tool that runs in your browser. Unlike heavyweight tools like pgAdmin or DBeaver, it starts in one command and works with any Drizzle ORM project. Browse tables, filter data, edit records inline, run SQL queries, and inspect relationships — all through a clean web interface. It supports PostgreSQL, MySQL, and SQLite.

## Instructions

### Step 1: Setup with Drizzle ORM

```bash
# If you already have a Drizzle ORM project:
npx drizzle-kit studio

# Opens http://localhost:4983
# Reads your drizzle.config.ts for database connection
```

```typescript
// drizzle.config.ts — Configuration that Studio reads
import { defineConfig } from 'drizzle-kit'

export default defineConfig({
  schema: './src/db/schema.ts',
  driver: 'pg',
  dbCredentials: {
    connectionString: process.env.DATABASE_URL!,
  },
})
```

### Step 2: Standalone Usage (Without Drizzle ORM)

```bash
# Connect to any PostgreSQL database
npx drizzle-kit studio --host 0.0.0.0 --port 4983

# With explicit connection
DATABASE_URL=postgresql://user:pass@localhost:5432/mydb npx drizzle-kit studio
```

### Step 3: Features

**Data browsing:**
- View all tables and their schemas
- Browse rows with pagination
- Filter by column values
- Sort by any column
- View relationships between tables

**Inline editing:**
- Click any cell to edit its value
- Add new rows directly in the UI
- Delete rows with confirmation
- Changes are applied to the database immediately

**SQL runner:**
- Execute arbitrary SQL queries
- View results in a table format
- Export results

## Examples

### Example 1: Debug production data issues
**User prompt:** "I need to quickly inspect the users table and find all accounts created in the last 24 hours that haven't verified their email."

The agent will:
1. Start Drizzle Studio connected to the production database (read-only credentials).
2. Navigate to the users table.
3. Apply filters: `created_at > yesterday` AND `email_verified = false`.
4. Review the results and export if needed.

## Guidelines

- Use read-only database credentials when browsing production data to prevent accidental modifications.
- Drizzle Studio is designed for development and debugging — for production admin panels, build a proper admin UI with access controls.
- It reads your `drizzle.config.ts` automatically — ensure the config points to the correct database for the environment you want to inspect.
