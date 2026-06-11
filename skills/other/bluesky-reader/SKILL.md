---
name: bluesky-reader
description: "Read public Bluesky feeds via AT Protocol API."
user-invocable: false
agent: python-general-engineer
allowed-tools:
  - Bash
  - Read
routing:
  triggers:
    - "read Bluesky"
    - "fetch Bluesky posts"
    - "AT Protocol"
    - "Bluesky feed"
    - "bsky"
  category: research
  pairs_with:
    - content-engine
---

# Bluesky Reader Skill

Read public Bluesky profiles via the AT Protocol public API. No auth needed.

## Commands

```bash
# Fetch recent posts
python3 ~/.claude/scripts/bluesky_reader.py feed --handle HANDLE --limit 20

# Search posts by keyword (fetches feed, filters locally)
python3 ~/.claude/scripts/bluesky_reader.py search --handle HANDLE --query "search terms"

# JSON output for pipeline consumption
python3 ~/.claude/scripts/bluesky_reader.py feed --handle HANDLE --json

# Pagination
python3 ~/.claude/scripts/bluesky_reader.py feed --handle HANDLE --cursor CURSOR_STRING
```

## API Details

- **Endpoint**: `https://public.api.bsky.app/xrpc/app.bsky.feed.getAuthorFeed`
- **Auth**: None (public endpoint)
- **Limit**: 1-100 posts per request
- **Search**: Local keyword filter -- all query words must appear (case-insensitive)

## When to Use

- Gathering recent Bluesky posts from a specific person for research
- Searching a profile's posts for mentions of a topic
- Feeding Bluesky content into a news or content pipeline

## Reference Loading

| Task type | Load this reference |
|-----------|-------------------|
| Endpoint details, data shapes, pagination | `references/at-protocol-api.md` |
| Debugging fetch errors, wrong output, missing posts | `references/at-protocol-preferred-patterns.md` |
| Extending the script with new endpoints or search | `references/at-protocol-api.md` |
| Code review of AT Protocol Python code | `references/at-protocol-preferred-patterns.md` |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0    | Success |
| 1    | Error (network failure, invalid handle, no posts found) |

## Reference Loading Table

| Signal | Load These Files | Why |
|---|---|---|
| Endpoint details, data shapes, pagination | `at-protocol-api.md` | Routes to the matching deep reference |
| Debugging fetch errors, wrong output, missing posts | `at-protocol-preferred-patterns.md` | Routes to the matching deep reference |
| Extending the script with new endpoints or search | `at-protocol-api.md` | Routes to the matching deep reference |
| Code review of AT Protocol Python code | `at-protocol-preferred-patterns.md` | Routes to the matching deep reference |
