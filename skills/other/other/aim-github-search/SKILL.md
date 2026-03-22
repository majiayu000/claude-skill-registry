---
name: aim-github-search
description: 'Search GitHub issues, PRs, commits, and CI results with semantic search and filters'
allowed-tools: Read, Bash
---

# Search GitHub - Semantic Search for GitHub Content

Search the discussions collection for GitHub-sourced content using semantic similarity with advanced filtering.

## Usage

```bash
# Basic semantic search
/aim-github-search "authentication bug"

# Filter by type
/aim-github-search "API refactoring" --type github_pr
/aim-github-search "CI failures" --type github_ci_result

# Filter by state
/aim-github-search "deployment fix" --state merged

# Combine filters
/aim-github-search "security" --type github_issue --limit 10
```

## Options

- `--type <type>` - Filter by GitHub document type: `github_issue`, `github_pr`, `github_commit`, `github_ci_result`, `github_code_blob`, `github_issue_comment`, `github_pr_review`, `github_pr_diff`
- `--state <state>` - Filter by state: `open`, `closed`, `merged`
- `--limit <n>` - Maximum results to return (default: 5)

## Result Format

Each result includes:
- **GitHub URL** - Direct link
- **Metadata badges** - Type, State, Date
- **Content snippet** - First ~300 characters
- **Relevance score** - Semantic similarity with decay (0-100%)

---

## Qdrant Connection Details

GitHub content is stored in the discussions collection:

| Parameter | Value |
|-----------|-------|
| **Host** | `localhost` |
| **Port** | `26350` (NOT the default 6333) |
| **API Key** | Required. Read from env: `QDRANT_API_KEY` |
| **Collection** | `discussions` |
| **URL** | `http://localhost:26350` |

To get the API key:
```bash
export QDRANT_API_KEY="$(grep QDRANT_API_KEY ~/.ai-memory/docker/.env | cut -d= -f2)"
```

---

## Qdrant Payload Schema

Every GitHub point in `discussions` has the following payload fields. Use these **exact names** for filtering.

### Common Fields (all GitHub points)

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `content` | string | Composed document text | `"[PR #42] Add decay scoring..."` |
| `type` | string | Document type | `"github_pr"`, `"github_issue"` |
| `source` | string | Always `"github"` | `"github"` |
| `group_id` | string | `owner/repo` | `"Hidden-History/ai-memory"` |
| `github_id` | int | Issue/PR number | `42` |
| `state` | string | Current state | `"open"`, `"closed"`, `"merged"` |
| `url` | string | GitHub URL | `"https://github.com/..."` |
| `github_updated_at` | string | ISO 8601 from GitHub API | `"2026-02-16T..."` |
| `files_changed` | list[string] | Files touched (PRs, commits) | `["src/memory/decay.py"]` |
| `labels` | list[string] | Issue/PR labels | `["bug", "v2.0.6"]` |
| `merged_at` | string or null | PR merge timestamp | `"2026-02-16T..."` |
| `is_current` | bool | Versioning: latest version | `true` |

---

## Direct Query Examples

Use the curl-to-file-to-python pattern for direct Qdrant queries.

**Important**: Save curl output to a temp file first, then process with Python. Do NOT pipe directly to `python3`.

### Search by source

```bash
# Step 1: Get API key
export QDRANT_API_KEY="$(grep QDRANT_API_KEY ~/.ai-memory/docker/.env | cut -d= -f2)"

# Step 2: Query Qdrant and save to temp file
# Replace "owner/repo-name" with your GITHUB_REPO value (e.g., "Hidden-History/ai-memory")
curl -s -H "Api-Key: $QDRANT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {
      "must": [
        {"key": "source", "match": {"value": "github"}},
        {"key": "group_id", "match": {"value": "owner/repo-name"}}
      ]
    },
    "limit": 10,
    "with_payload": true
  }' \
  http://localhost:26350/collections/discussions/points/scroll > /tmp/github_results.json

# Step 3: Process with Python
python3 -c "
import json
data = json.load(open('/tmp/github_results.json'))
points = data.get('result', {}).get('points', [])
print(f'Found {len(points)} points')
for p in points:
    pl = p.get('payload', {})
    print(f\"  [{pl.get('type', '?')}] {pl.get('state', '?')} - {pl.get('url', '?')} - {pl.get('content', '')[:80]}...\")
"
```

### Filter by type and state

```bash
# Replace "owner/repo-name" with your GITHUB_REPO value
curl -s -H "Api-Key: $QDRANT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {
      "must": [
        {"key": "source", "match": {"value": "github"}},
        {"key": "group_id", "match": {"value": "owner/repo-name"}},
        {"key": "type", "match": {"value": "github_pr"}},
        {"key": "state", "match": {"value": "merged"}}
      ]
    },
    "limit": 20,
    "with_payload": true
  }' \
  http://localhost:26350/collections/discussions/points/scroll > /tmp/github_results.json
```

### Count GitHub points in collection

```bash
# Replace "owner/repo-name" with your GITHUB_REPO value
curl -s -H "Api-Key: $QDRANT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {
      "must": [
        {"key": "source", "match": {"value": "github"}},
        {"key": "group_id", "match": {"value": "owner/repo-name"}}
      ]
    },
    "exact": true
  }' \
  http://localhost:26350/collections/discussions/points/count | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(f\"GitHub points: {data.get('result', {}).get('count', 0)}\")
"
```

---

## Python Implementation Reference

This skill uses the `source="github"` filter pattern against the discussions collection:

```python
# Key filter patterns
from qdrant_client.models import FieldCondition, Filter, MatchValue

must_conditions = [
    FieldCondition(key="source", match=MatchValue(value="github")),
    FieldCondition(key="group_id", match=MatchValue(value=group_id)),
]
if type_filter:
    must_conditions.append(
        FieldCondition(key="type", match=MatchValue(value=type_filter))
    )
if state_filter:
    must_conditions.append(
        FieldCondition(key="state", match=MatchValue(value=state_filter))
    )
```

## Technical Details

- **Semantic Search**: Uses jina-embeddings-v2-base-en for vector similarity
- **Tenant Isolation**: Mandatory group_id filter prevents cross-repo leakage
- **Performance**: < 2s for typical searches
- **Collection**: discussions (GitHub content stored alongside conversation data)
- **Score Threshold**: Configurable via SIMILARITY_THRESHOLD (default 0.7)
- **Port**: 26350 (NOT the Qdrant default of 6333)
- **API Key**: Required -- stored in `~/.ai-memory/docker/.env` as `QDRANT_API_KEY`
- **Decay Scoring**: Applied to results via existing search path

## Notes

- GitHub repo is auto-detected from project configuration
- Results sorted by relevance score (highest first)
- All filters are optional except the search query
- Use **exact field names** from the schema above -- `source` NOT `namespace`, `type` NOT `doc_type`
- The `source="github"` filter is always applied to restrict results to GitHub content
- The `group_id` filter is always applied for mandatory tenant isolation (prevents cross-repo leakage)
