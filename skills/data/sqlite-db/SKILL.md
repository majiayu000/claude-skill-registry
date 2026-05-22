---
name: sqlite-db
description: SQLite database operations and queries
allowed-tools: [Bash, Read]
---

# SQLite Database Skill

## Overview

SQLite database operations for local development. 90%+ context savings.

## Tools (Progressive Disclosure)

### Query Operations

| Tool    | Description                  | Confirmation |
| ------- | ---------------------------- | ------------ |
| query   | Execute SELECT query         | No           |
| execute | Execute INSERT/UPDATE/DELETE | Yes          |
| schema  | Show table schema            | No           |
| tables  | List all tables              | No           |

### Database Management

| Tool         | Description       | Confirmation |
| ------------ | ----------------- | ------------ |
| create-table | Create new table  | Yes          |
| drop-table   | Drop table        | **REQUIRED** |
| vacuum       | Optimize database | Yes          |
| backup       | Create backup     | No           |

### BLOCKED

| Tool          | Status      |
| ------------- | ----------- |
| DROP DATABASE | **BLOCKED** |

## Agent Integration

- **developer** (primary): Database operations
- **database-architect** (secondary): Schema design

## Security

⚠️ DROP operations require confirmation
