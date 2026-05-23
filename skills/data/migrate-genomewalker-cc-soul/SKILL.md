---
name: migrate
description: Import soul data from SQLite or shared chitta files
execution: task
---

# Migrate

```ssl
[migrate] incremental import | via Task agent

sources:
  SQLite soul.db: legacy cc-soul→chitta_migrate
  shared chitta: from another user→chitta_import

process:
  1. ask user: "(1) SQLite soul.db or (2) shared chitta files?"
  2. find binaries@plugin/build/{chitta_migrate,chitta_import}
  3. dry-run first→show what will import
  4. if approved→run import
  5. verify: soul_context + recall("wisdom")

report: source type+path | nodes imported by type | current soul state
```
