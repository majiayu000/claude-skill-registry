---
name: db-handler
description: Manage database schemas, Drizzle ORM, migrations, and data modeling. Use when creating tables, modifying columns, or planning database changes.
tools: Read, Write, Edit
model: inherit
---

# Database Handler

## Instructions

### 1. Creating a New Table
1.  **Draft**: Create the `pgTable` definition in `src/db/schema/{domain}.ts`.
2.  **Columns**: Add ID (UUID), timestamps, and data columns.
    - **Mandatory**: Use Zod schema for any JSONB columns.
3.  **Relations**: Define `relations` and Foreign Keys.
4.  **Verification**: Ask the user: "Is this structure correct? Are there any missing relations?"
5.  **Migration**: 
    -   **DO NOT** generate migration files (e.g., `drizzle-kit generate`).
    -   **DO** use `npx drizzle-kit push` to sync schema changes directly to the database.

### 2. Performance & Optimization (CRITICAL)
- **Indexes**: You **MUST** add indexes for:
    - All Foreign Keys (e.g., `userId`, `planId`).
    - Columns frequently used in `WHERE` clauses (e.g., `status`, `email`).
    - Columns used for sorting (e.g., `createdAt`).
- **N+1 Prevention**: 
    - **NEVER** allow fetching data inside a loop. 
    - Use Drizzle's Relational Query API (`with: { ... }`) or explicit `.leftJoin()` to fetch related data in a single query.

### 3. Modifying Columns
- Prefer adding **nullable** columns or columns with **default values**.
- Avoid breaking changes without explicit confirmation.

### 4. Types & Enums
- **Enums**: Export as constants (`export const roleEnum = ...`).
- **Types**: Do NOT export inferred types. Let consumers infer them.

## Reference
For detailed patterns, imports, and best practices, see [reference.md](reference.md).
