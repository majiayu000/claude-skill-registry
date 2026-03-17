---
name: Backend Migrations
description: Create reversible, focused database migrations with proper naming, version control practices, and zero-downtime deployment considerations. Use this skill when creating or editing migration files in database/migrations/, when writing schema changes (creating/modifying tables, columns, indexes, foreign keys), when implementing migration rollback methods, when managing database version control, when adding or modifying indexes on large tables, or when separating schema changes from data migrations for safer deployments.
---

# Backend Migrations

This Skill provides Claude Code with specific guidance on how to adhere to coding standards as they relate to how it should handle backend migrations.

## When to use this skill

- When creating new migration files in `database/migrations/` directory
- When editing existing migration files (with caution for deployed migrations)
- When writing table creation or modification logic using Schema builder
- When implementing migration rollback/down methods for reversibility
- When adding or modifying database columns, indexes, or constraints
- When creating or dropping foreign key relationships
- When renaming tables or columns
- When adding indexes to tables, especially large production tables
- When separating schema changes from data migrations
- When considering zero-downtime deployment strategies for migrations
- When writing data migrations or seeders that modify existing records
- When planning backwards-compatible database changes

## Instructions

For details, refer to the information provided in this file:
[backend migrations](../../../agent-os/standards/backend/migrations.md)
