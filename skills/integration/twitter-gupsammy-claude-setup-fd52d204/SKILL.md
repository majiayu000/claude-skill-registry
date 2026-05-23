---
name: twitter
description: >
  Use when user asks to "search Twitter", "read a tweet", "check my bookmarks",
  "find mentions", "get tweets from a list", "see who I follow", "extract tweets",
  or needs programmatic access to X/Twitter for research and information synthesis.
  Handles reading, searching, bookmarks, lists, and social graph queries.
allowed-tools:
  - Bash(bird:*)
  - Read
  - Write
---

# Twitter / X Research & Extraction

Programmatic access to Twitter/X via `bird` CLI. Primary use: search, read, extract, and synthesize information.

## Core Commands

### Reading & Threads
```bash
bird read <url-or-id>           # Single tweet
bird read <url> --json          # JSON output for processing
bird thread <url>               # Full conversation thread
bird replies <url> -n 20        # Replies to a tweet
```

### Search
```bash
bird search "query" -n 10       # Search tweets
bird search "from:user topic"   # User-specific search
bird search "query" --json      # JSON for processing
```

### Bookmarks & Likes
```bash
bird bookmarks                  # Your saved tweets
bird bookmarks -n 50 --json     # Bulk export
bird likes                      # Your liked tweets
bird unbookmark <url>           # Remove bookmark
```

### Lists
```bash
bird lists                      # Your lists
bird list-timeline <list-id>    # Tweets from a list
```

### Social Graph
```bash
bird following                  # Who you follow
bird followers                  # Who follows you
bird mentions                   # Tweets mentioning you
```

## Extraction Workflows

### Save tweets to file
```bash
bird search "topic" -n 50 --json > tweets.json
bird bookmarks --json > bookmarks.json
bird thread <url> --json > thread.json
```

### Synthesize from search
1. `bird search "topic" -n 20 --json > results.json`
2. Read results.json
3. Extract key insights, summarize themes

### Export bookmarks for review
1. `bird bookmarks -n 100 --json > bookmarks.json`
2. Parse and categorize by topic
3. Create summary or reading list

## Auth & Troubleshooting

Check auth status:
```bash
bird whoami                     # Current account
bird check                      # Credential sources
```

Auth sources (checked in order):
- Browser cookies (Firefox/Chrome)
- `SWEETISTICS_API_KEY` env var
- Explicit `--auth-token` and `--ct0` flags

Common issues:
- **Rate limits**: Wait and retry; reduce `-n` count
- **Auth expired**: Re-login to Twitter in browser, cookies auto-refresh
- **No results**: Check query syntax; try broader terms

## Output Formats

- Default: Human-readable with emoji
- `--plain`: Stable text output, no emoji/color
- `--json`: Machine-readable for processing
- `--json-full`: Includes raw API response

Always use `--json` when extracting for synthesis.
