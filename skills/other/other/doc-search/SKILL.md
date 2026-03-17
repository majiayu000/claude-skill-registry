---
name: doc-search
description: Token-efficient documentation search using Serena Document Index. 90%+ token savings vs reading full files. Use BEFORE reading README.md or docs/ files. Triggers on architecture questions, pattern lookups, and project-specific documentation needs.
---

# Document Search

Search project documentation efficiently using the Serena Document Index system.

## Why This Matters

| Approach | Tokens | Use Case |
|----------|--------|----------|
| Read full README.md | 3000-8000 | Never (wasteful) |
| Read docs/*.md | 2000-5000 each | Rarely needed |
| **Document Index Search** | 100-500 | Always prefer |
| **Section Retrieval** | 200-800 | After finding relevant section |

**Rule**: Never read documentation files until the document index fails to answer.

## Document Index Location

```
.serena/cache/documents/document_index.json
```

**Index Types Available:**
- `tag_index` - Search by tags (architecture, api, testing, etc.)
- `title_index` - Search by section titles
- `project_index` - Filter by project (basecamp-server, interface-cli, etc.)
- `doc_type_index` - Filter by document type (readme, guide, api-reference, etc.)
- `content_index` - Keyword-based content search

## Workflow Pattern

### Step 1: Search Document Index (Python CLI)

```bash
# Search for relevant documentation sections
cd /Users/kun/github/1ambda/dataops-platform
python3 scripts/serena/document_indexer.py --search "hexagonal architecture" --max-results 5
```

### Step 2: Read Specific Section Only

After finding relevant section from search:

```python
# Use section coordinates from search result
# Example: project-basecamp-server/docs/PATTERNS.md#module-placement-rules
# Read only that section (lines 45-80) instead of entire file
Read(file_path="project-basecamp-server/docs/PATTERNS.md", offset=45, limit=35)
```

### Step 3: Alternative - Direct JSON Query

```python
# For programmatic access in agent workflows
import json
from pathlib import Path

cache_path = Path(".serena/cache/documents/document_index.json")
index = json.loads(cache_path.read_text())

# Search by tag
architecture_docs = index['tag_index'].get('architecture', [])

# Search by project
server_docs = index['project_index'].get('project-basecamp-server', [])

# Get section content
for ref in architecture_docs[:3]:
    print(f"Section: {ref['section_title']}")
    print(f"File: {ref['relative_path']}")
    print(f"Lines: {ref['line_start']}-{ref['line_end']}")
```

## Decision Tree

```
Need documentation?
|
+-- What patterns exist for X?
|   +-- doc-search: tag_index["patterns"] or tag_index["architecture"]
|
+-- How to implement feature in project Y?
|   +-- doc-search: project_index["project-Y"] + tag_index["implementation"]
|
+-- What does README say about Z?
|   +-- doc-search: title_index["Z"] or content_index["keyword"]
|
+-- Full context needed?
    +-- Read specific section (lines from search result)
    +-- LAST RESORT: Read full file
```

## Integration with mcp-efficiency

Document search is the **first step** before Serena symbol queries:

```python
# 1. Search docs for patterns/context
doc_search("hexagonal architecture", max_results=3)

# 2. Use Serena for code structure
serena.get_symbols_overview("module-core-domain/")

# 3. Find specific symbols
serena.find_symbol("RepositoryJpa", depth=1)
```

## Common Search Queries

| Need | Search Query |
|------|-------------|
| Architecture patterns | `"hexagonal" OR "architecture"` |
| API endpoints | `"api" OR "endpoint" OR "controller"` |
| Testing patterns | `"test" OR "testing" OR "fixture"` |
| Entity relationships | `"entity" OR "repository" OR "jpa"` |
| CLI commands | `"command" OR "cli" OR "dli"` |
| Configuration | `"config" OR "environment" OR "settings"` |

## Token Savings Examples

| Task | Without Doc Search | With Doc Search | Savings |
|------|-------------------|-----------------|---------|
| Find architecture pattern | 5000 tokens (full PATTERNS.md) | 300 tokens | 94% |
| Check entity rules | 3000 tokens (full README) | 400 tokens | 87% |
| Find API reference | 4000 tokens (full docs) | 250 tokens | 94% |
| Implementation guide | 6000 tokens (multiple files) | 500 tokens | 92% |

## Updating the Index

```bash
# Rebuild after documentation changes
python3 scripts/serena/update-symbols.py --with-docs

# Incremental update (changed files only)
python3 scripts/serena/update-symbols.py --changed-only --with-docs

# Full rebuild
python3 scripts/serena/document_indexer.py --project-root . --rebuild
```

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Read full README.md first | 3000+ tokens wasted | Search index, read section |
| Read all docs/*.md | 10000+ tokens wasted | Search by tag/title |
| Skip doc search, use web | Slower, less relevant | Use indexed local docs |
| Guess file locations | Miss relevant docs | Use project_index filter |

## Quick Reference

```bash
# CLI search (recommended)
python3 scripts/serena/document_indexer.py --search "QUERY" --max-results 5

# Build/rebuild index
python3 scripts/serena/update-symbols.py --with-docs

# Check index stats
python3 -c "import json; d=json.load(open('.serena/cache/documents/document_index.json')); print(d['metadata'])"
```
