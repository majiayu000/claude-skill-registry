---
name: kagi-search
description: Search the web using Kagi. Use for web searches with Quick Answer AI summaries.
---

# Usage

```bash
# Basic search (shows Quick Answer summary only)
kagi-search "what is the capital of France"

# Include search result links (default: 3 links)
kagi-search -l "search query"

# Include more links
kagi-search -l -n 10 "search query"

# JSON output for parsing
kagi-search -j "search query" | jq '.results[0].url'
```

See [README.md](../../kagi-search/README.md) for setup and configuration.
