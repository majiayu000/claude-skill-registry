---
context: fork
---

# /graph-query

Query the vault's knowledge graph index using natural language or structured queries.

## Usage

```
/graph-query ADRs with status proposed
/graph-query high priority tasks
/graph-query orphaned notes
/graph-query broken links
/graph-query backlinks to Project - MyProject
/graph-query --type=Adr --status=accepted
```

## Instructions

When the user invokes `/graph-query` or asks to query the graph index:

### Phase 1: Ensure Index Exists

Before executing any query, check if the graph index exists:

1. Check if `.graph/index.json` exists
2. If **not found**, inform the user and offer to build it:
   ```
   The graph index needs to be generated first.
   Running: npm run graph:build
   ```
   Execute: `npm run graph:build`

3. If index exists but is stale (>1 day old), optionally suggest rebuilding

### Phase 2: Parse the Query

Understand what the user is asking for. The query system supports:

**Natural Language Patterns:**
| Pattern | Interpretation |
|---------|----------------|
| "ADRs with status proposed" | `--type=Adr --status=proposed` |
| "high priority tasks" | `--type=Task --priority=high` |
| "active projects" | `--type=Project --status=active` |
| "orphaned notes" | `--orphans` |
| "broken links" | `--broken-links` |
| "stale notes" | `--stale` |
| "meetings about kafka" | `--type=Meeting --search=kafka` |
| "backlinks to X" | `--backlinks="X"` |
| "notes mentioning aws" | `--search=aws` |

**Structured Parameters:**
| Parameter | Description | Example |
|-----------|-------------|---------|
| `--type=` | Filter by note type | `--type=Adr`, `--type=Project` |
| `--status=` | Filter by status | `--status=proposed`, `--status=active` |
| `--priority=` | Filter by priority | `--priority=high` |
| `--search=` | BM25 relevance search (ranked results) | `--search="kafka integration"` |
| `--backlinks=` | Find notes linking to target | `--backlinks="Project - MyProject"` |
| `--orphans` | List orphaned notes | |
| `--broken-links` | List broken wiki-links | |
| `--stale` | List notes >6 months old | |
| `--stats` | Show index statistics | |
| `--json` | Output as JSON with scores | |

### Phase 3: Execute Query via CLI

Run the appropriate command:

```bash
# Natural language query
node scripts/graph-query.js "ADRs with status proposed"

# Structured query
node scripts/graph-query.js --type=Adr --status=proposed

# Special queries
node scripts/graph-query.js --orphans
node scripts/graph-query.js --broken-links
node scripts/graph-query.js --stats

# JSON output (for further processing)
node scripts/graph-query.js --type=Task --priority=high --json
```

### Phase 4: Format Response

Present results as a markdown table. For search queries, results are ranked by **BM25 relevance score**:

```markdown
## Search Results

Found **X** result(s) for: "kafka integration"

| Score | Type | Title |
|-------|------|-------|
| 14.65 | Page | Kafka Integration Solution Architecture |
| 11.32 | Integration | ERP → Data Lake |
| 9.45 | System | Data Platform |

*Results ranked by BM25 relevance score (higher = more relevant)*
```

For type/status queries (no search term), show standard format:

```markdown
## Query Results

Found **X** result(s) for: "ADRs with status proposed"

| Type | Status | Priority | Title |
|------|--------|----------|-------|
| Adr | proposed | high | ADR - API Gateway Selection |
| Adr | proposed | medium | ADR - Event Streaming Platform |

### Quick Actions
- View a note: `[[ADR - API Gateway Selection]]`
- Find related: `/graph-query backlinks to "ADR - API Gateway Selection"`
- Check quality: `/graph-query --stats`
```

For special queries like orphans or broken links, format appropriately:

```markdown
## Orphaned Notes Report

Found **8** orphaned notes (notes with no backlinks)

| Type | Title | Last Modified |
|------|-------|---------------|
| Page | Database Migration Checklist | 2025-11-15 |
| Project | Research - Event-Driven Architecture | 2025-10-20 |

### Recommendations
- Consider linking from relevant MOCs
- Archive if no longer needed
- Use `/archive <note>` to soft-archive
```

## Query Examples

### By Type
```
/graph-query all ADRs
/graph-query projects
/graph-query active tasks
/graph-query meetings
```

### By Status/Priority
```
/graph-query ADRs with status proposed
/graph-query high priority tasks
/graph-query completed projects
/graph-query draft ADRs
```

### Search
```
/graph-query notes about kafka
/graph-query mentions of aws bedrock
/graph-query "integration pattern"
```

### Relationships
```
/graph-query backlinks to Project - MyProject
/graph-query orphaned notes
/graph-query broken links
```

### Quality
```
/graph-query stale notes
/graph-query --stats
```

## Notes

- The graph index is stored in `.graph/` directory (git-ignored)
- Index is automatically excluded from vault searches
- Rebuild index after major changes: `npm run graph:build`
- Use `npm run graph:watch` for automatic rebuilding during active work
- Results are limited to 50 items by default; use `--json` for full results
- **Search uses BM25 ranking** - results are sorted by relevance score, not just filtered
- BM25 weights rare terms higher (IDF) and normalises for document length
- JSON output includes relevance scores for programmatic use

## Related Skills

- `/orphans` - Dedicated orphan analysis with recommendations
- `/broken-links` - Detailed broken link analysis with fixes
- `/quality-report` - Comprehensive vault quality report
- `/vault-maintenance` - Full maintenance check including graph analysis
