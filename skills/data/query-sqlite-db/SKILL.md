---
name: query-sqlite-db
description: Use when needing to inspect SQLite database directly, when debugging data issues, when environment variable expansion fails with APPDATA or similar paths, or when sqlite3 query returns "unable to open database"
---

# Query SQLite Database

## Overview

Direct SQLite queries for debugging data state. **Critical:** Environment variables don't expand in bash - always use full paths.

## Database Paths

| Environment | Path |
|-------------|------|
| **Dev** | `C:/Users/Dodo/AppData/Roaming/com.notavailable.kniha-jazd.dev/kniha-jazd.db` |
| **Prod** | `C:/Users/Dodo/AppData/Roaming/com.notavailable.kniha-jazd/kniha-jazd.db` |

## Quick Reference

```bash
# Query
sqlite3 "C:/Users/Dodo/AppData/Roaming/com.notavailable.kniha-jazd.dev/kniha-jazd.db" "SELECT * FROM vehicles;"

# Schema
sqlite3 "..." ".schema receipts"

# Tables
sqlite3 "..." ".tables"
```

## Key Tables

| Table | Key Columns |
|-------|-------------|
| `vehicles` | `id`, `name`, `tp_consumption` |
| `trips` | `id`, `vehicle_id`, `start_datetime`, `end_datetime`, `fuel_liters` |
| `receipts` | `id`, `trip_id`, `receipt_datetime`, `liters`, `total_price_eur` |

## Common Mistakes

| Error | Fix |
|-------|-----|
| `%APPDATA%` doesn't expand | Use full path `C:/Users/Dodo/AppData/Roaming/...` |
| `$env:APPDATA` fails | Use full path (PowerShell vars don't work either) |
| Column `date` not found | Use `receipt_datetime` or `start_datetime` |
| "unable to open database" | Check path for typos, use forward slashes |
