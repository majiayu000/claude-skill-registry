---
context: fork
---

# /search

Smart search using BM25 relevance ranking. Queries the graph index first with ranked results, then falls back to grep for content search.

## Usage

```
/search kafka
/search "API gateway"
/search type:Adr status:proposed
/search backlinks:Project - MyProject
```

## Instructions

When the user invokes `/search <query>`:

### Phase 1: Parse Query Type

Determine what kind of search this is:

| Pattern | Search Type | Action |
|---------|-------------|--------|
| `type:<Type>` | Type filter | Use graph `--type` |
| `status:<status>` | Status filter | Use graph `--status` |
| `priority:<priority>` | Priority filter | Use graph `--priority` |
| `backlinks:<note>` | Backlink search | Use graph `--backlinks` |
| Simple keyword | Keyword search | Use graph `--search`, then grep |
| Regex pattern | Content search | Skip to grep |

### Phase 2: Query Graph Index First

**Always start with the graph index** (unless it's a regex):

```bash
# Check index exists
if [ ! -f ".graph/index.json" ]; then
  npm run graph:build
fi

# Run graph query
node scripts/graph-query.js --search "<query>"
```

### Phase 3: Evaluate Results

After running the graph query:

1. **If results found**: Present them formatted as a table
2. **If no results OR user needs content search**: Fall back to grep

```bash
# Grep fallback for content search
grep -r "<query>" --include="*.md" --exclude-dir=".git" --exclude-dir=".obsidian" --exclude-dir="node_modules" --exclude-dir=".smart-env"
```

### Phase 4: Present Combined Results

Format output with BM25 relevance scores:

```markdown
## Search Results for "<query>"

### Graph Index Results (BM25 ranked)
Found **X** notes matching in graph index:

| Score | Type | Title |
|-------|------|-------|
| 14.65 | Page | Kafka to SAP Integration |
| 11.32 | Adr | ADR - Kafka Integration |
| 9.45 | Meeting | Data Platform Discussion |

*Results ranked by relevance (higher score = better match)*

### Content Search Results (full-text)
Found **Y** additional matches in note content:

- `Page - Kafka Architecture.md:45` - "...kafka cluster configuration..."
- `Meeting - 2025-01-10 Data Team.md:12` - "...discussed kafka..."
```

## Query Shortcuts

| Shortcut | Expands To |
|----------|------------|
| `/search t:Adr` | `--type Adr` |
| `/search s:active` | `--status active` |
| `/search p:high` | `--priority high` |
| `/search b:Note` | `--backlinks "Note"` |
| `/search orphans` | `--orphans` |
| `/search broken` | `--broken-links` |
| `/search stale` | `--stale` |

## Examples

```
/search kafka                    # Keyword in graph + content
/search type:Meeting kafka       # Meetings mentioning kafka
/search backlinks:Project - MyProject # Notes linking to project
/search status:proposed          # All proposed items
/search orphans                  # Orphaned notes
/search "event.*driven"          # Regex - grep only
```

## Performance Notes

- **Graph search (BM25)**: ~50ms for 1500 notes (pre-indexed with ranking)
- **Grep search**: ~2-5s depending on vault size
- **Combined**: Graph first catches 80%+ of searches instantly
- **Relevance ranking**: Results are sorted by BM25 score, so top results are most relevant
- **IDF weighting**: Rare terms like "kafka" score higher than common terms like "the"

## Related

- `/graph-query` - Direct graph queries with more options
- `/orphans` - Dedicated orphan analysis
- `/broken-links` - Dedicated broken link analysis
