---
name: working-with-sqlite
description: Preferences and tricks for working with SQLite databases
---

You're already an expert in SQL, and especially SQLite. Here are our preferences:

```
PRAGMA journal_mode = WAL;
PRAGMA busy_timeout = 5000;
PRAGMA synchronous = NORMAL;
PRAGMA cache_size = 1000000000;
PRAGMA foreign_keys = true;
PRAGMA temp_store = memory;
```

Also:

  - Use `BEGIN IMMEDIATE` transactions.
  - Use `STRICT` tables.


When creating tables with lots of data:
1. create table,
2. insert rows in large transactions, with 10s of thousands of rows a time,
3. then create indices at the end.
4. `ANALYZE` and `VACUUM` if necessary

Use read-only connections when appropriate:
```python
conn = sqlite3.connect('file:database.db?mode=ro', uri=True)
```

