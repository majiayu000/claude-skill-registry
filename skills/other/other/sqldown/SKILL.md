---
name: sqldown
description: Bidirectional markdown ↔ SQLite conversion with column limit protection and smart section extraction. Import with Python, query with sqlite3.
---

# SQLDown Skill

## Core Concept

**Load with sqldown. Query with sqlite3. Dump when needed.**

This skill handles bidirectional markdown ↔ SQLite conversion with intelligent column limit protection. For queries, use `sqlite3` directly - it's already perfect.

## When to Use

- Need to query across many markdown files efficiently
- Want SQL-powered filtering, aggregation, sorting
- Working with structured markdown (YAML frontmatter + H2 sections)
- Need context-efficient progressive disclosure

## Commands

### Import: Create or Update Tables

Use `sqldown load` - loads markdown files into SQLite database.

**Command:**
```bash
sqldown load PATH [OPTIONS]
```

**What it does:**
- Scans markdown files recursively
- Parses YAML frontmatter → database columns
- Extracts H2 sections → `section_*` columns
- Creates schema dynamically based on discovered fields
- Upserts into SQLite (idempotent - safe to run multiple times)
- Respects `.gitignore` patterns automatically

**Options:**
- `-d, --db PATH` - Database file (default: `sqldown.db`)
- `-t, --table NAME` - Table name (default: `docs`)
- `-p, --pattern GLOB` - File pattern (default: `**/*.md`)
- `--max-columns N` - Maximum allowed columns (default: 1800, SQLite limit: 2000)
- `--top-sections N` - Extract only top N most common sections (default: 20, 0=all)
- `-w, --watch` - Watch for file changes and auto-update
- `-v, --verbose` - Show detailed progress

**Examples:**
```bash
# Load markdown files into SQLite
sqldown load ~/tasks

# Specify database and table
sqldown load ~/tasks -d cache.db -t tasks

# Load notes
sqldown load ~/notes -d cache.db -t notes

# Load with specific pattern
sqldown load ~/.claude/skills -d cache.db -t skills -p "*/SKILL.md"

# Watch mode: auto-update on file changes
sqldown load ~/tasks -w

# Column limit protection - extract only top 10 sections
sqldown load ~/tasks --top-sections 10

# Extract all sections (may hit 2000 column limit with diverse docs)
sqldown load ~/tasks --top-sections 0

# Check column breakdown with verbose output
sqldown load ~/tasks -v
# Output shows: Base columns: 7, Frontmatter: 89, Sections: 20, Total: 116
```

### Query: Use sqlite3 Directly

For ALL queries, use `sqlite3` command directly:

```bash
# List available tables
sqlite3 cache.db ".tables"

# Show table schema
sqlite3 cache.db ".schema tasks"

# Query
sqlite3 cache.db "SELECT title, status FROM tasks WHERE status='active'"

# Aggregate
sqlite3 cache.db "SELECT status, COUNT(*) FROM tasks GROUP BY status"

# Complex queries
sqlite3 cache.db "
  SELECT project, COUNT(*) as count,
         SUM(CASE WHEN status='active' THEN 1 ELSE 0 END) as active
  FROM tasks
  GROUP BY project
  ORDER BY count DESC
"
```

## Dynamic Schema

**Core fields** (always present):
```sql
_id TEXT PRIMARY KEY        -- SHA1 of file path
_path TEXT                   -- Relative path
_sections TEXT               -- JSON array of H2 names
title TEXT                   -- H1 heading
body TEXT                    -- Full content
lead TEXT                    -- First paragraph
file_modified FLOAT          -- Timestamp
```

**Dynamic fields** (auto-generated):
- YAML frontmatter: `status`, `project`, `priority`, `tags`, etc.
- H2 sections: `section_objective`, `section_implementation_plan`, etc.

**Example:** 87 tasks with varied structure → 181 columns generated automatically.

## Column Limit Protection

SQLite has a hard limit of 2000 columns per table. The `--top-sections` flag prevents hitting this limit:

**How it works:**
1. Analyzes all documents to count section frequency
2. Extracts only the N most common sections as columns
3. All other sections remain in the `body` field

**Real-world example:**
- 5,225 tasks with diverse sections = 6,694 unique columns (exceeds limit!)
- With `--top-sections 20` (default) = 116 columns ✅

**Top extracted sections (from Mike's tasks):**
`overview`, `usage`, `objective`, `notes`, `next_steps`, `troubleshooting`, `installation`, `configuration`, `requirements`, `testing`, etc.

**When to adjust:**
- `--top-sections 10` - Fewer columns for very diverse collections
- `--top-sections 50` - More columns if you need more queryable sections
- `--top-sections 0` - Extract all (only for homogeneous collections)

**What about rare sections?**
- Still in `body` field - nothing is lost
- Use FTS5 or `LIKE '%text%'` to search across all content
- Only the top N become directly queryable columns

## Common Query Patterns

```bash
# Find active tasks
sqlite3 cache.db "SELECT title FROM tasks WHERE status='active'"

# Recent updates
sqlite3 cache.db "SELECT title, updated FROM tasks ORDER BY updated DESC LIMIT 10"

# Count by status
sqlite3 cache.db "SELECT status, COUNT(*) FROM tasks GROUP BY status"

# Search content
sqlite3 cache.db "SELECT title, _path FROM tasks WHERE body LIKE '%SQLite%'"

# High priority items
sqlite3 cache.db "SELECT title FROM tasks WHERE priority='high' AND status!='completed'"

# Project summary
sqlite3 cache.db "
  SELECT project,
         COUNT(*) as total,
         SUM(CASE WHEN status='completed' THEN 1 ELSE 0 END) as done
  FROM tasks
  GROUP BY project
"

# Find related documents
sqlite3 cache.db "
  SELECT title FROM tasks
  WHERE section_related_tasks LIKE '%AG-22%'
"
```

## Progressive Disclosure Pattern

1. **Query metadata first** (fast, context-efficient):
   ```bash
   sqlite3 cache.db "SELECT title, _path, status FROM tasks WHERE priority='high'"
   ```

2. **Read full markdown only when needed** (slower, more context):
   ```bash
   # After finding relevant tasks, read the actual files
   cat ~/tasks/AG-22_feat_add-configuration/README.md
   ```

This keeps context usage low while still finding what you need.

## Multiple Tables Strategy

Keep different document types in separate tables:

```bash
# Load each type
sqldown load ~/tasks -d cache.db -t tasks
sqldown load ~/notes -d cache.db -t notes
sqldown load ~/.claude/skills -d cache.db -t skills

# Query across them
sqlite3 ~/cache.db "
  SELECT 'task' as type, title FROM tasks WHERE body LIKE '%cache%'
  UNION ALL
  SELECT 'note' as type, title FROM notes WHERE body LIKE '%cache%'
"
```

## Refresh Strategy

**One-time load (manual refresh):**

Load is idempotent - run after file changes:

```bash
sqldown load ~/tasks -d cache.db -t tasks -v
```

**Watch mode (automatic refresh):**

Use `--watch` to automatically update when files change:

```bash
# Starts watching - runs until Ctrl-C
sqldown load ~/tasks -d cache.db -t tasks -w

# Output shows real-time updates:
# [2025-01-15 10:23:45] Updated: AG-22_feat_add-configuration/README.md
# [2025-01-15 10:24:12] Added: AG-31_feat_new-feature/README.md
# [2025-01-15 10:25:03] Deleted: AG-19_feat_old-feature/README.md
```

Watch mode is ideal for development workflows where you want the cache to stay in sync as you edit files.

## Why sqlite3 Instead of Python Wrappers?

**sqlite3 gives you:**
- Full SQL power (no wrapper limitations)
- Standard tool (no custom command syntax to learn)
- Better output formats (`.mode csv`, `.mode json`, `.mode column`)
- Interactive shell with history and tab completion
- Better performance (no Python startup overhead)

**sqldown load gives you:**
- Markdown + YAML frontmatter parsing
- Dynamic schema generation
- H2 section extraction
- Automatic .gitignore filtering
- Watch mode for auto-updates

This division of responsibility keeps tools simple and powerful.

## Workflow Guidelines

1. **Start with schema inspection:**
   ```bash
   sqlite3 cache.db ".schema tasks"
   ```
   Shows what columns are available (critical for dynamic schemas).

2. **Use simple queries first:**
   ```bash
   sqlite3 cache.db "SELECT title, status FROM tasks LIMIT 5"
   ```

3. **Build up complexity:**
   ```bash
   sqlite3 cache.db "SELECT status, COUNT(*) FROM tasks GROUP BY status"
   ```

4. **Read full files last:**
   Only after identifying relevant documents via SQL.

5. **Trust .gitignore filtering:**
   By default, sqldown load respects .gitignore automatically.

## Requirements

**Prerequisites:**
- Python 3.10+ (includes sqlite3 module - standard library)
- sqlite3 CLI (built-in on macOS 10.4+ and most Linux distributions)

**Installation:**

```bash
# Install from PyPI
pip install sqldown

# Or use uv for faster installation
uv pip install sqldown
```

## Limitations

- Best for <100K documents
- SQLite column limit: 2000 columns max (sqldown detects and reports)
- No built-in full-text search (though SQLite FTS5 could be added)

## Additional Commands

### Dump: Export Back to Markdown

```bash
sqldown dump -d DATABASE -o OUTPUT_DIR [OPTIONS]
```

**What it does:**
- Exports database rows back to markdown files
- Reconstructs original markdown structure with frontmatter
- Preserves file paths from original import
- Skips unchanged files (smart change detection)
- Supports SQL filtering to export subsets

**Options:**
- `-d, --db PATH` - Database file (required)
- `-t, --table NAME` - Table name (default: `docs`)
- `-o, --output PATH` - Output directory (required)
- `-f, --filter WHERE` - SQL WHERE clause to filter rows
- `--force` - Always write files, even if unchanged
- `--dry-run` - Preview what would be exported without writing
- `-v, --verbose` - Show detailed progress

**Examples:**
```bash
# Export all documents
sqldown dump -d cache.db -o ~/restored

# Export only active tasks
sqldown dump -d cache.db -t tasks -o ~/active --filter "status='active'"

# Preview export without writing files
sqldown dump -d cache.db -o ~/export --dry-run
```

### Info: Database Statistics

```bash
sqldown info [OPTIONS]
```

**What it does:**
- Shows database statistics and table information
- Lists all tables with document counts
- Displays column breakdown (frontmatter vs sections)
- Provides schema details for specific tables

**Options:**
- `-d, --db PATH` - Database file (default: `sqldown.db` if exists)
- `-t, --table NAME` - Show detailed info for specific table

**Examples:**
```bash
# Show database overview
sqldown info

# Show info for specific database
sqldown info -d cache.db

# Show detailed table information
sqldown info -d cache.db -t tasks
```

## Technical Details

**Automatic .gitignore Support:**
- Reads .gitignore from root directory by default
- Uses pathspec library for gitignore pattern matching
- Filters files before import to avoid unwanted content

**Column Limit Protection:**
- Uses `--top-sections` to extract only the N most common H2 sections
- Prevents hitting SQLite's 2000 column limit
- Rare sections remain in `body` field - nothing is lost

## Related Files

- `bin/sqldown` - Main CLI tool
- `README.md` - Human-facing documentation
- `SPECIFICATION.md` - Technical specification
