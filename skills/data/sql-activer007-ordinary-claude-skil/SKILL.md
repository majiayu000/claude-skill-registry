---
name: sql
description: Run SQL queries against the WordPress development database. Use when querying database tables, inspecting Simple History events, checking WordPress data, or debugging database issues.
---

# Run SQL Queries

You are tasked with running SQL queries against the WordPress development database.

## Prerequisites

- Database credentials are stored in `CLAUDE.local.md` under "Database Access"
- Docker compose services must be running
- Commands must be run from the docker-compose project directory

## Command Pattern

```bash
docker compose exec mariadb mysql -u<USER> -p<PASSWORD> <DATABASE> -e "YOUR_SQL_HERE"
```

Refer to `CLAUDE.local.md` for the actual credentials and connection details.

## Examples

### Show all tables
```bash
docker compose exec mariadb mysql -u<USER> -p<PASSWORD> <DATABASE> -e "SHOW TABLES;"
```

### Query Simple History events
```bash
docker compose exec mariadb mysql -u<USER> -p<PASSWORD> <DATABASE> -e "SELECT * FROM wp_simple_history ORDER BY id DESC LIMIT 10;"
```

### Describe a table structure
```bash
docker compose exec mariadb mysql -u<USER> -p<PASSWORD> <DATABASE> -e "DESCRIBE wp_simple_history;"
```

### Count records
```bash
docker compose exec mariadb mysql -u<USER> -p<PASSWORD> <DATABASE> -e "SELECT COUNT(*) FROM wp_posts;"
```

## Table Prefixes

The database contains multiple WordPress installations with different prefixes:

| Prefix | Installation |
|--------|--------------|
| `wp_` | Main install (wordpress_mariadb) |
| `wp_nightly_` | Nightly build |
| `wp_6_0_` to `wp_6_6_` | Version-specific installs |
| `wp_multisite_` | Multisite install |
| `wp_php74_` | PHP 7.4 install |
| `wp_subfolder_` | Subfolder install |

## Simple History Tables

The main Simple History tables (using `wp_` prefix):

- `wp_simple_history` - Main events table
- `wp_simple_history_contexts` - Event context/metadata

## Instructions

1. Read credentials from `CLAUDE.local.md`
2. Ask the user what SQL query they want to run (if not specified)
3. Run the query using the command pattern above
4. Display the results
5. Offer to run follow-up queries if needed

## Notes

- For complex queries, consider using `\G` at the end for vertical output
- Be careful with UPDATE/DELETE queries - always confirm with user first
