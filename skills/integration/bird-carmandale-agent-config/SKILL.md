---
name: bird
description: Read and search X/Twitter posts via CLI. Use when user shares x.com or twitter.com links, asks to read a tweet, search Twitter/X, read a thread, or post/reply on X. Handles URLs like https://x.com/user/status/123 or https://twitter.com/user/status/123.
metadata: {"clawdbot":{"emoji":"🐦","requires":{"bins":["bird"]},"install":[{"id":"brew","kind":"brew","formula":"steipete/tap/bird","bins":["bird"],"label":"Install bird (brew)"}]}}
---

# bird

Use `bird` to read/search X and post tweets/replies.

Quick start
- `bird whoami`
- `bird read <url-or-id>`
- `bird thread <url-or-id>`
- `bird search "query" -n 5`

Posting (confirm with user first)
- `bird tweet "text"`
- `bird reply <id-or-url> "text"`

Auth sources
- Browser cookies (default: Firefox/Chrome)
- Sweetistics API: set `SWEETISTICS_API_KEY` or use `--engine sweetistics`
- Check sources: `bird check`
