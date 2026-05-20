---
name: sql-executor
description: 对SQLite、PostgreSQL、MySQL数据库执行SQL查询，支持结果格式化和导出。
metadata:
  short-description: 执行SQL查询
source:
  repository: https://github.com/python/cpython
  license: PSF
---

# SQL Executor Tool

## Description
Execute SQL queries against various databases with formatted output and export capabilities.

## Trigger
- `/sql` command
- User needs to run database queries
- User wants to export query results

## Usage

```bash
# Query SQLite database
python scripts/sql_executor.py database.db "SELECT * FROM users"

# Export to CSV
python scripts/sql_executor.py database.db "SELECT * FROM orders" --output orders.csv

# Execute SQL file
python scripts/sql_executor.py database.db --file queries.sql
```

## Tags
`sql`, `database`, `sqlite`, `query`, `data`

## Compatibility
- Codex: ✅
- Claude Code: ✅
