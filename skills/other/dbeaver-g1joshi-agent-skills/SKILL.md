---
name: dbeaver
description: DBeaver universal database tool. Use for database management.
---

# DBeaver

DBeaver is the free, open-source universal database manager. 2025 updates add **Gemini AI** integration to write SQL for you.

## When to Use

- **Universal Access**: Connect to Oracle, DB2, MySQL, PostgreSQL, and SQLite in one app.
- **ER Diagrams**: Generates Entity-Relationship diagrams from existing schemas.
- **Data Transfer**: Powerful import/export wizard (CSV, Excel).

## Core Concepts

### Drivers

Downloads JDBC drivers on demand.

### Projects

Organize connections and scripts into projects.

### Spatial View

Visualizes GIS data on a map.

## Best Practices (2025)

**Do**:

- **Use AI Assistant**: "Show me users capable of admin" -> Generates SQL.
- **Use Mock Data Generator**: Populate tables with realistic dummy data for testing.
- **Transaction Mode**: Set connection to "Manual Commit" for production DBs to avoid accidents.

**Don't**:

- **Don't run heavy queries on prod**: DBeaver can hang if you fetch 1M rows. Use "Result Set Fetch Size".

## References

- [DBeaver Documentation](https://dbeaver.com/docs/wiki/)
