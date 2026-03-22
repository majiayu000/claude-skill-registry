---
name: Backend Migrations
description: Alembic database migration management for stock_picker_bot. Covers creating schema changes, managing migrations for stock portfolios and historical data, and ensuring database consistency across environments.
---

# Backend Migrations

This Skill provides Claude Code with specific guidance on how to adhere to coding standards as they relate to Alembic database migrations in the stock_picker_bot backend.

## When to use this skill

Use this skill when:

1. Creating new Alembic migration files in `alembic/versions/` for database schema changes
2. Adding new tables for portfolio management, stock watchlists, or user tracking
3. Modifying SQLAlchemy model definitions and generating corresponding migrations
4. Handling migration of historical stock market data storage and schema updates
5. Implementing database constraints for portfolio tracking and stock relationships
6. Managing migrations across development, testing, and production environments with aiosqlite
7. Reverting or rolling forward migrations in the Alembic revision chain
8. Testing migrations with pytest to ensure data integrity during schema changes

## Instructions

For details, refer to the information provided in this file:
[backend migrations](../../../agent-os/standards/backend/migrations.md)
