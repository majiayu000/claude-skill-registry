---
name: tables
description: Preview denmark statistics fact tables and inspect their metadata
---

# tables CLI

Inspect a denmark statistics fact table before loading it into Postgres and view its official table metadata.

Run the CLI from `.claude/skills/tables`:

```bash
python scripts/tables.py --help
```

## `view` — preview a fact table

```bash
python scripts/tables.py view FOLK1A --rows 5
python scripts/tables.py view FOLK1A --db-format   # show the DB-ready schema
```

- `--rows/-n` controls how many rows to display (default 10).
- `--db-format/-d` runs the same processing used during ingestion (renames to lower-case, normalizes dtypes, parses date strings).

Output is always a `column|dtype` list followed by a pipe-delimited preview (`TABLE.head(n)`), which stays consistent whether you use the raw or DB-formatted view.

## `info` — metadata snapshot

```bash
python scripts/tables.py info FOLK1A
```

Prints metadata for a single table, including id, title, description, unit and every dimension (text plus the coded values present in the metadata). The metadata is printed as XML. The XML is easy to feed into other tools or to scan quickly when deciding which dimensions to join.

```bash
python scripts/tables.py info FOLK1A --column "område"
```

Will print only the coded values ("id") and the text titles for the column specifiec. All unique values will be printed.

```bash
python scripts/tables.py info FOLK1A --normalize-col-names
```

Will normalize column names so they match the database schema. This means lowercasing col names and replacing å -> a, ø -> o, æ -> ae. So OMRÅDE becomes omrade.