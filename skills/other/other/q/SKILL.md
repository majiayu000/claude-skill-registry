---
description: Fast SQLite-based vault search using FTS5 full-text search index
context: normal
model: haiku
---

# /q - Quick SQLite Search

Fast vault search using the SQLite FTS5 index. Returns results in milliseconds instead of seconds.

## Prerequisites

The SQLite index must be built first:

```bash
npm run vault:index
```

## Usage Patterns

### Full-text Search

```bash
/q architecture patterns
/q "event driven"        # Phrase search
/q kafka integration     # Multiple terms (AND)
```

### Type Filter

```bash
/q type:Adr             # All ADRs
/q type:Project status:active
/q type:Task priority:high
```

### Tag Search

```bash
/q tag:technology/aws
/q tag:project/your-project
```

### Recent Notes

```bash
/q recent               # Modified in last 7 days
/q recent:30            # Modified in last 30 days
```

### Backlinks

```bash
/q backlinks:"Project - Your Project"
/q backlinks:"System - Your System"
```

### Orphans

```bash
/q orphans              # Notes with no backlinks
```

## Implementation

Execute the appropriate SQLite query based on the search pattern.

### Full-text Search Query

```bash
sqlite3 .data/vault.db -markdown "
SELECT n.path, snippet(fts_content,1,'→','←','...',40) as match
FROM fts_content
JOIN notes n ON fts_content.rowid = n.id
WHERE fts_content MATCH '<search_terms>'
ORDER BY rank
LIMIT 20
"
```

### Type Filter Query

```bash
sqlite3 .data/vault.db -markdown "
SELECT path, title, status, priority
FROM notes
WHERE type = '<Type>'
ORDER BY modified DESC
LIMIT 20
"
```

### Tag Search Query

```bash
sqlite3 .data/vault.db -markdown "
SELECT n.path, n.title, n.type
FROM notes n
JOIN tags t ON n.id = t.note_id
WHERE t.tag = '<tag>'
ORDER BY n.modified DESC
LIMIT 20
"
```

### Recent Notes Query

```bash
sqlite3 .data/vault.db -markdown "
SELECT path, title, type, modified
FROM notes
WHERE modified >= date('now', '-<days> days')
ORDER BY modified DESC
LIMIT 30
"
```

### Backlinks Query

```bash
sqlite3 .data/vault.db -markdown "
SELECT n.path, n.title, n.type
FROM notes n
JOIN links l ON n.id = l.source_id
WHERE l.target_path LIKE '%<note_name>%'
ORDER BY n.modified DESC
"
```

### Orphans Query

```bash
sqlite3 .data/vault.db -markdown "
SELECT n.path, n.title, n.type
FROM notes n
LEFT JOIN links l ON n.id = l.target_id
WHERE l.target_id IS NULL
  AND n.type NOT IN ('DailyNote', 'MOC', 'Dashboard', 'Query')
ORDER BY n.modified DESC
"
```

## Performance

| Query Type  | Grep/Glob | SQLite | Improvement |
| ----------- | --------- | ------ | ----------- |
| Full-text   | 5-15 sec  | 0.01s  | ~1000x      |
| Type filter | 3-5 sec   | 0.007s | ~500x       |
| Tag search  | 2-5 sec   | 0.007s | ~500x       |
| Backlinks   | 10+ sec   | 0.01s  | ~1000x      |

## Rebuilding the Index

The index should be rebuilt when vault content changes significantly:

```bash
npm run vault:index      # Full rebuild
npm run vault:stats      # View current statistics
```

## Tips

1. **Combine filters**: `/q type:Adr status:proposed technology/aws`
2. **Use phrases**: `/q "data platform"` for exact matches
3. **Wildcards**: SQLite FTS5 supports `*` wildcards: `/q architect*`
4. **Present results**: Format output as markdown table for readability
