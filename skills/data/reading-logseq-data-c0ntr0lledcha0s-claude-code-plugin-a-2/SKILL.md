---
name: reading-logseq-data
version: 1.0.0
description: >
  Expert in reading data from Logseq DB graphs via HTTP API or CLI.
  Auto-invokes when users want to fetch pages, blocks, or properties from Logseq,
  execute Datalog queries against their graph, search content, or retrieve
  backlinks and relationships. Provides the logseq-client library for operations.
allowed-tools: Read, Bash, Grep, Glob
---

# Reading Logseq Data

## When to Use This Skill

This skill auto-invokes when:
- User wants to read pages or blocks from their Logseq graph
- Fetching properties or metadata from Logseq entities
- Executing Datalog queries against the graph
- Searching for content in Logseq
- Finding backlinks or references
- User mentions "get from logseq", "fetch page", "query logseq"

**Client Library**: See `{baseDir}/scripts/logseq-client.py` for the unified API.

## Available Operations

| Operation | Description |
|-----------|-------------|
| `get_page(title)` | Get page content and properties |
| `get_block(uuid)` | Get block with children |
| `search(query)` | Full-text search across graph |
| `datalog_query(query)` | Execute Datalog query |
| `list_pages()` | List all pages |
| `get_backlinks(title)` | Find pages linking to this one |
| `get_graph_info()` | Get current graph metadata |

## Quick Examples

### Get a Page

```python
from logseq_client import LogseqClient

client = LogseqClient()
page = client.get_page("My Page")
print(f"Title: {page['title']}")
print(f"Properties: {page['properties']}")
```

### Execute Datalog Query

```python
# Find all books with rating >= 4
results = client.datalog_query('''
    [:find (pull ?b [:block/title :user.property/rating])
     :where
     [?b :block/tags ?t]
     [?t :block/title "Book"]
     [?b :user.property/rating ?r]
     [(>= ?r 4)]]
''')

for book in results:
    print(f"{book['block/title']}: {book['user.property/rating']} stars")
```

### Search Content

```python
# Search for mentions of "project"
results = client.search("project")
for block in results:
    print(f"Found in: {block['page']}")
    print(f"Content: {block['content'][:100]}...")
```

## Datalog Query Patterns

### Find All Pages

```clojure
[:find (pull ?p [:block/title])
 :where
 [?p :block/tags ?t]
 [?t :db/ident :logseq.class/Page]]
```

### Find Blocks with Tag

```clojure
[:find (pull ?b [*])
 :where
 [?b :block/tags ?t]
 [?t :block/title "Book"]]
```

### Find by Property

```clojure
[:find ?title ?author
 :where
 [?b :block/title ?title]
 [?b :user.property/author ?author]
 [?b :block/tags ?t]
 [?t :block/title "Book"]]
```

### Find Tasks by Status

```clojure
[:find (pull ?t [:block/title :logseq.property/status])
 :where
 [?t :block/tags ?tag]
 [?tag :db/ident :logseq.class/Task]
 [?t :logseq.property/status ?s]
 [?s :block/title "In Progress"]]
```

### Find Backlinks

```clojure
[:find (pull ?b [:block/title {:block/page [:block/title]}])
 :in $ ?page-title
 :where
 [?p :block/title ?page-title]
 [?b :block/refs ?p]]
```

### Aggregations

```clojure
;; Count books per author
[:find ?author (count ?b)
 :where
 [?b :block/tags ?t]
 [?t :block/title "Book"]
 [?b :user.property/author ?author]]
```

## Using the Client Library

### Initialization

```python
from logseq_client import LogseqClient

# Auto-detect backend
client = LogseqClient()

# Force specific backend
client = LogseqClient(backend="http")

# Custom URL/token
client = LogseqClient(
    url="http://localhost:12315",
    token="your-token"
)
```

### Error Handling

```python
try:
    page = client.get_page("Nonexistent Page")
except client.NotFoundError:
    print("Page doesn't exist")
except client.ConnectionError:
    print("Cannot connect to Logseq")
except client.AuthError:
    print("Invalid token")
```

### Batch Operations

```python
# Get multiple pages efficiently
pages = ["Page1", "Page2", "Page3"]
results = [client.get_page(p) for p in pages]

# Or use a single query
query = '''
    [:find (pull ?p [*])
     :in $ [?titles ...]
     :where
     [?p :block/title ?titles]]
'''
results = client.datalog_query(query, [pages])
```

## Performance Tips

1. **Use specific queries** - Don't fetch more than needed
2. **Prefer pull syntax** - `(pull ?e [:needed :fields])` vs `[*]`
3. **Put selective clauses first** - Filter early in query
4. **Use parameters** - Pass values via `:in` clause
5. **Batch when possible** - Multiple items in one query

## CLI Fallback

If HTTP API unavailable, the client falls back to CLI:

```python
# CLI mode (automatic if HTTP fails)
client = LogseqClient(backend="cli", graph_path="/path/to/graph")

# Query still works the same way
results = client.datalog_query("[:find ?title :where [?p :block/title ?title]]")
```

## Output Formats

### Raw (default)

Returns Python dicts/lists directly from API.

### Normalized

```python
# Get normalized output
page = client.get_page("My Page", normalize=True)
# Returns: {"title": "...", "uuid": "...", "properties": {...}, "blocks": [...]}
```

## Reference Materials

- See `{baseDir}/references/read-operations.md` for all operations
- See `{baseDir}/templates/query-template.edn` for query patterns
