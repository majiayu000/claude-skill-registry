---
name: aim-jira-search
description: 'Search Jira issues and comments with semantic search and filters'
allowed-tools: Read, Bash
---

# Search Jira - Semantic Search for Jira Content

Search the jira-data collection for issues and comments using semantic similarity with advanced filtering.

## Usage

```bash
# Basic semantic search
/aim-jira-search "authentication bug"

# Filter by project
/aim-jira-search "API errors" --project BMAD

# Filter by type (issue or comment)
/aim-jira-search "implementation details" --type jira_comment

# Filter by issue type
/aim-jira-search "bugs" --issue-type Bug

# Filter by status
/aim-jira-search "in progress work" --status "In Progress"

# Filter by priority
/aim-jira-search "critical issues" --priority High

# Filter by author (comments) or reporter (issues)
/aim-jira-search "alice's comments" --author alice@company.com

# Issue lookup mode (issue + all comments)
/aim-jira-search --issue BMAD-42

# Combine filters
/aim-jira-search "database" --project BMAD --issue-type Bug --status Done --limit 10
```

## Options

- `--project <key>` - Filter by Jira project key (e.g., BMAD, PROJ)
- `--type <type>` - Filter by document type (jira_issue or jira_comment)
- `--issue-type <type>` - Filter by issue type (Bug, Story, Task, Epic)
- `--status <status>` - Filter by issue status (To Do, In Progress, Done, etc.)
- `--priority <priority>` - Filter by priority (Highest, High, Medium, Low, Lowest)
- `--author <email>` - Filter by comment author or issue reporter
- `--issue <key>` - Lookup mode: retrieve issue + all comments (e.g., BMAD-42)
- `--limit <n>` - Maximum results to return (default: 5)

## Result Format

Each result includes:
- **Jira URL** - Direct link to issue/comment
- **Metadata badges** - Type, Status, Priority, Author/Reporter
- **Content snippet** - First ~300 characters
- **Relevance score** - Semantic similarity (0-100%)

---

## Qdrant Connection Details

The jira-data collection is stored in the local Qdrant instance:

| Parameter | Value |
|-----------|-------|
| **Host** | `localhost` |
| **Port** | `26350` (NOT the default 6333) |
| **API Key** | Required. Read from env: `QDRANT_API_KEY` |
| **Collection** | `jira-data` |
| **URL** | `http://localhost:26350` |

To get the API key:
```bash
export QDRANT_API_KEY="$(grep QDRANT_API_KEY ~/.ai-memory/docker/.env | cut -d= -f2)"
```

---

## Qdrant Payload Schema

Every point in `jira-data` has the following payload fields. Use these **exact names** for filtering — do NOT guess field names like `project_key` or `issue_key`.

### Common Fields (all points)

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `content` | string | Full text content of issue/comment | `"[PROJ-123] Fix login bug..."` |
| `type` | string | Document type | `"jira_issue"` or `"jira_comment"` |
| `group_id` | string | Jira instance hostname (tenant isolation) | `"hidden-history.atlassian.net"` |
| `session_id` | string | Always `"jira_sync"` | `"jira_sync"` |
| `jira_project` | string | Project key | `"BMAD"` |
| `jira_issue_key` | string | Full issue key | `"BMAD-42"` |
| `jira_issue_type` | string | Issue type name | `"Bug"`, `"Story"`, `"Task"`, `"Epic"` |
| `jira_status` | string | Issue status | `"To Do"`, `"In Progress"`, `"Done"` |
| `jira_priority` | string or null | Priority level | `"High"`, `"Medium"`, `"Low"`, `null` |
| `jira_updated` | string | ISO 8601 timestamp | `"2026-02-10T14:30:00.000+0000"` |
| `jira_url` | string | Full Jira URL | `"https://company.atlassian.net/browse/BMAD-42"` |

### Issue-Only Fields (`type: "jira_issue"`)

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `jira_reporter` | string | Issue reporter display name | `"Alice Smith"` |
| `jira_labels` | list[string] | Issue labels | `["backend", "auth"]` |

### Comment-Only Fields (`type: "jira_comment"`)

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `jira_comment_id` | string | Jira comment ID | `"10042"` |
| `jira_author` | string | Comment author display name | `"Bob Jones"` |

### Chunking Metadata (if content was chunked)

| Field | Type | Description |
|-------|------|-------------|
| `chunk_index` | int | Chunk sequence number (0-based) |
| `total_chunks` | int | Total chunks for this document |
| `chunking_strategy` | string | Strategy used (e.g., `"topical"`) |

---

## Direct Query Examples

The Python search module (`src/memory/connectors/jira/search.py`) is NOT importable from other project directories. Use these direct Qdrant API patterns instead.

### Curl-to-File-to-Python Pattern

**Important**: Save curl output to a temp file first, then process with Python. Do NOT pipe directly to `python3` — it can cause encoding issues.

#### Search by project key

```bash
# Step 1: Get API key
export QDRANT_API_KEY="$(grep QDRANT_API_KEY ~/.ai-memory/docker/.env | cut -d= -f2)"

# Step 2: Query Qdrant and save to temp file
curl -s -H "Api-Key: $QDRANT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {
      "must": [
        {"key": "jira_project", "match": {"value": "BMAD"}}
      ]
    },
    "limit": 10,
    "with_payload": true
  }' \
  http://localhost:26350/collections/jira-data/points/scroll > /tmp/jira_results.json

# Step 3: Process with Python
python3 -c "
import json
data = json.load(open('/tmp/jira_results.json'))
points = data.get('result', {}).get('points', [])
print(f'Found {len(points)} points')
for p in points:
    pl = p.get('payload', {})
    print(f\"  {pl.get('jira_issue_key', '?')} [{pl.get('type', '?')}] - {pl.get('jira_status', '?')} - {pl.get('content', '')[:80]}...\")
"
```

#### Filter by issue type and status

```bash
curl -s -H "Api-Key: $QDRANT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {
      "must": [
        {"key": "jira_project", "match": {"value": "BMAD"}},
        {"key": "jira_issue_type", "match": {"value": "Bug"}},
        {"key": "jira_status", "match": {"value": "Done"}}
      ]
    },
    "limit": 20,
    "with_payload": true
  }' \
  http://localhost:26350/collections/jira-data/points/scroll > /tmp/jira_results.json
```

#### Count points in collection

```bash
curl -s -H "Api-Key: $QDRANT_API_KEY" \
  http://localhost:26350/collections/jira-data | python3 -c "
import json, sys
data = json.load(sys.stdin)
info = data.get('result', {})
print(f\"Points: {info.get('points_count', 0)}, Vectors: {info.get('vectors_count', 0)}\")
"
```

#### Get all comments for a specific issue

```bash
curl -s -H "Api-Key: $QDRANT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {
      "must": [
        {"key": "jira_issue_key", "match": {"value": "BMAD-42"}},
        {"key": "type", "match": {"value": "jira_comment"}}
      ]
    },
    "limit": 50,
    "with_payload": true
  }' \
  http://localhost:26350/collections/jira-data/points/scroll > /tmp/jira_results.json
```

---

## Python Implementation Reference

This skill uses functions from `src/memory/connectors/jira/search.py`:

```python
from src.memory.connectors.jira.search import search_jira, lookup_issue

# Semantic search
results = search_jira(
    query="authentication bug",
    group_id="company.atlassian.net",
    project="BMAD",
    issue_type="Bug",
    limit=5
)

# Issue lookup
context = lookup_issue(
    issue_key="BMAD-42",
    group_id="company.atlassian.net"
)
```

## Technical Details

- **Semantic Search**: Uses jina-embeddings-v2-base-en for vector similarity
- **Tenant Isolation**: Mandatory group_id filter prevents cross-instance leakage
- **Performance**: < 2s for typical searches
- **Collection**: jira-data (issues and comments)
- **Score Threshold**: Configurable via SIMILARITY_THRESHOLD (default 0.7)
- **Port**: 26350 (NOT the Qdrant default of 6333)
- **API Key**: Required — stored in `~/.ai-memory/docker/.env` as `QDRANT_API_KEY`

## Notes

- Jira instance URL is auto-detected from project configuration
- Results sorted by relevance score (highest first)
- Issue lookup mode returns chronologically sorted comments
- All filters are optional except query (or --issue for lookup mode)
- Use **exact field names** from the schema above — `jira_project` NOT `project_key`, `jira_issue_key` NOT `issue_key`
