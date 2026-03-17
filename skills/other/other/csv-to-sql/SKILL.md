---
context: fork
description: Convert CSV files to SQLite databases for efficient querying
model: sonnet
---

# /csv-to-sql

Convert CSV files into SQLite databases stored in `.data/` for efficient querying by Claude Code.

**Why SQLite?** Large CSV data converted to markdown tables creates files too large for Claude Code to read efficiently. SQLite enables:

- Direct SQL queries via `sqlite3` CLI
- Aggregations (AVG, COUNT, SUM, GROUP BY)
- Full-text search on long content
- Filtered retrieval (WHERE clauses)
- JSON or markdown output formats

## Usage

```
/csv-to-sql <csv-path>
/csv-to-sql Inbox/data.csv
/csv-to-sql Inbox/rfi.csv --start-row 14 --fts
/csv-to-sql Inbox/survey.csv --db-name survey-2026.db --table responses
```

## Instructions

### Phase 1: CSV Analysis

1. **Verify the CSV file exists** at the specified path
2. **Run with --dry-run** to preview schema:
   ```bash
   node scripts/csv-to-sqlite.js "<csv-path>" --dry-run --verbose
   ```
3. **Review the output** to identify:
   - Column names and inferred types
   - Which columns will be indexed
   - If --start-row is needed to skip metadata

### Phase 2: Database Creation

Run the conversion:

```bash
node scripts/csv-to-sqlite.js "<csv-path>" --start-row <n> --fts --verbose
```

**Script Options:**

| Option            | Description                                       |
| ----------------- | ------------------------------------------------- |
| `--db-name <n>`   | Custom database filename (default: from CSV name) |
| `--table <name>`  | Table name (default: 'data')                      |
| `--start-row <n>` | Skip first N rows (0-indexed, for metadata)       |
| `--fts`           | Create full-text search index on long text cols   |
| `--dry-run`       | Preview schema without creating database          |
| `--verbose`       | Show detailed progress and schema                 |

### Phase 3: Verify and Query

After creation, test the database:

```bash
# Show table structure
sqlite3 .data/<db-name>.db ".schema"

# Preview data
sqlite3 .data/<db-name>.db -markdown -header "SELECT * FROM data LIMIT 5;"

# Count rows
sqlite3 .data/<db-name>.db "SELECT COUNT(*) FROM data;"
```

### Phase 4: Summary Report

Provide user with:

````markdown
## CSV to SQLite Complete

**Database**: `.data/<db-name>.db`
**Table**: `<table-name>`

**Statistics**:

- Rows: <count>
- Columns: <count>
- Indexes: <list>
- FTS enabled: Yes/No

**Quick Queries**:

```bash
# List all records
sqlite3 ".data/<db>.db" -markdown -header "SELECT * FROM <table>;"

# Aggregate by category
sqlite3 ".data/<db>.db" -markdown -header "SELECT category, COUNT(*) FROM <table> GROUP BY category;"

# Search text (if FTS enabled)
sqlite3 ".data/<db>.db" "SELECT * FROM <table>_fts WHERE <table>_fts MATCH 'keyword';"
```
````

````

## Common Query Patterns

### For RFI/Survey Data

```sql
-- Average score by category
SELECT category, ROUND(AVG(score), 2) as avg_score, COUNT(*) as questions
FROM data GROUP BY category ORDER BY avg_score DESC;

-- Questions with lowest scores
SELECT id, question, category, score
FROM data WHERE score < 6 ORDER BY score ASC;

-- Score distribution
SELECT score, COUNT(*) as count
FROM data GROUP BY score ORDER BY score;

-- Search responses for keyword
SELECT id, question, response
FROM data_fts WHERE data_fts MATCH 'integration pattern';
````

### For General Data

```sql
-- Distinct values in a column
SELECT DISTINCT category FROM data;

-- Records matching criteria
SELECT * FROM data WHERE status = 'active' AND priority = 'high';

-- Export to JSON
-- Use: sqlite3 .data/db.db -json "SELECT * FROM data;"
```

## Output Formats

The sqlite3 CLI supports multiple output formats:

| Format   | Flag                | Use Case                    |
| -------- | ------------------- | --------------------------- |
| Markdown | `-markdown -header` | Display in Obsidian/Claude  |
| JSON     | `-json`             | Parsing, further processing |
| Table    | `-table -header`    | Human-readable terminal     |
| CSV      | `-csv -header`      | Export/import workflows     |
| Plain    | (default)           | Simple output               |

## Database Location

All databases are stored in `.data/` directory:

```
YourVault/
├── .data/
│   ├── vendor-rfi-scoring.db
│   ├── vendor-evaluation.db
│   └── survey-results.db
└── Inbox/
    └── source-data.csv
```

## Schema Inference

The script automatically detects column types:

| CSV Content             | SQLite Type | Notes                     |
| ----------------------- | ----------- | ------------------------- |
| Integers (1, 42, -5)    | INTEGER     | Enables numeric ops       |
| Decimals (3.14, 99.9)   | REAL        | For scores, percentages   |
| Currency (£100, $50.00) | REAL        | Symbols stripped          |
| Text, long responses    | TEXT        | FTS-indexed if --fts used |
| Empty cells             | NULL        | Properly handled          |

## Automatic Indexing

Indexes are created on columns containing:

- `id` - Primary key lookups
- `category` - Common filter criteria
- `type` - Classification queries
- `status` - Workflow filtering

## Full-Text Search (FTS)

When `--fts` is used, a virtual FTS5 table is created for text columns >200 characters:

```sql
-- Search in any text column
SELECT * FROM data_fts WHERE data_fts MATCH 'middleware integration';

-- Search with ranking
SELECT *, rank FROM data_fts WHERE data_fts MATCH 'API design' ORDER BY rank;

-- Phrase search
SELECT * FROM data_fts WHERE data_fts MATCH '"backward compatibility"';
```

## Integration with Claude Code

Once the database exists, query it directly:

```bash
# From Claude Code, run queries via Bash tool
sqlite3 .data/vendor-rfi-scoring.db -markdown -header "
SELECT category, COUNT(*) as questions, ROUND(AVG(score),1) as avg
FROM data
GROUP BY category
ORDER BY avg DESC;"
```

**Tip**: For complex analysis, create a query, run it, then iterate based on results.

## Example Workflow

```
User: /csv-to-sql Inbox/vendor-rfi-responses.csv

Claude:
1. Runs: node scripts/csv-to-sqlite.js "..." --dry-run --verbose
2. Identifies start-row needed (14)
3. Runs: node scripts/csv-to-sqlite.js "..." --start-row 14 --fts --verbose
4. Verifies: sqlite3 .data/... -markdown -header "SELECT * FROM data LIMIT 3;"
5. Reports summary with example queries
```
