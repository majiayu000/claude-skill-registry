---
name: data-importer
description: Import Synnovator platform data from .synnovator/*.md files into SQLite database via SQLAlchemy models. Use when need to populate test data, initialize database from file-based data, or migrate .synnovator content to relational database. Triggers include "import synnovator data", "populate database from .synnovator", "fill database with test data", or when user needs to test FastAPI endpoints with real data.
---

# Data Importer

Import `.synnovator/*.md` files (YAML frontmatter + Markdown body) into SQLite database via SQLAlchemy models.

## Quick Start

```bash
# Import all data
python cli.py import \
  --source .synnovator \
  --db data/synnovator.db \
  --models backend/models

# Import specific types only
python cli.py import \
  --source .synnovator \
  --db data/synnovator.db \
  --models backend/models \
  --types user,post

# Full import (clear and reimport)
python cli.py import \
  --source .synnovator \
  --db data/synnovator.db \
  --models backend/models \
  --mode full
```

## Workflow

1. **Validate inputs** - Check paths exist and models can be loaded
2. **Load models** - Dynamically import SQLAlchemy models module
3. **Import in order** - Follow dependency graph (see [import-order.md](references/import-order.md))
4. **Parse files** - Extract YAML frontmatter and Markdown body
5. **Convert types** - Map values to database column types
6. **Insert records** - Batch insert with error handling
7. **Report results** - Show imported/skipped/failed counts

## Import Order

Data must be imported following foreign key dependencies:

1. **Phase 1**: user, event, rule (independent types)
2. **Phase 2**: group, post, resource (depend on user)
3. **Phase 3**: interaction (depends on user and targets)
4. **Phase 4**: All relations (depend on content types)

See [references/import-order.md](references/import-order.md) for complete dependency graph.

## Field Mapping

.md files use YAML frontmatter for structured fields and Markdown content for body text. The importer maps these to SQLAlchemy model columns with automatic type conversion:

- **datetime**: ISO 8601 strings → datetime objects
- **JSON**: Lists/dicts → JSON strings
- **enum**: Validates against allowed values
- **integer/float**: Strings → numbers
- **boolean**: "true"/"false" → bool

See [references/mapping.md](references/mapping.md) for complete field mappings for all 7 content types and 7 relation types.

## Error Handling

- **Duplicate IDs**: Skips records that already exist (incremental mode)
- **Missing fields**: Reports validation errors
- **Foreign key violations**: Reports missing references
- **Type errors**: Shows conversion failures
- **Partial success**: Continues importing after individual failures

## Testing

Run the test suite:

```bash
cd scripts/
python test_importer.py
```

Tests validate:
- Parsing .md files with YAML frontmatter
- Type conversion logic
- Import order correctness

## Requirements

- Python 3.8+
- SQLAlchemy
- PyYAML
- SQLite database with tables matching .synnovator schema

## Limitations

- Only supports SQLite databases
- Requires SQLAlchemy models to be importable
- Does not generate missing tables (use Alembic migrations first)
- Incremental mode skips duplicates by ID only
