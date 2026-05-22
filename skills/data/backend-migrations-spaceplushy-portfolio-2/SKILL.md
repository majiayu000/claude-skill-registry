---
name: Backend Migrations
description: Create and manage database schema migrations with reversible changes, clear naming, and safe deployment practices. Use this skill when writing database migration files, modifying database schemas, creating migration scripts, or managing database version control. When working on migration files in database migration directories, files defining schema changes (CREATE TABLE, ALTER TABLE, DROP TABLE), migration rollback/down methods, database index creation scripts, seed data or data migration files, ORM migration configurations (Prisma, Drizzle, TypeORM), or files handling database versioning and migration history.
---

# Backend Migrations

This Skill provides Claude Code with specific guidance on how to adhere to coding standards as they relate to how it should handle backend migrations.

## When to use this skill

- When creating new database migration files or scripts
- When modifying existing database schemas (adding/removing/altering tables or columns)
- When writing migration rollback methods or down migrations for safe reversals
- When creating database indexes, constraints, or foreign keys
- When implementing data migrations or transformations alongside schema changes
- When working with ORM migration tools (Prisma, Drizzle, TypeORM, Sequelize, etc.)
- When planning zero-downtime deployments that require backwards-compatible schema changes
- When managing database migration version history or migration ordering
- When creating seed data files or initial database setup scripts
- When documenting migration dependencies or complex schema changes

## Instructions

For details, refer to the information provided in this file:
[backend migrations](../../../agent-os/standards/backend/migrations.md)
