---
name: using-alpha-lab
description: How to use the Alpha Lab client in Wayfinder Paths for discovering alpha insights — scored tweets, chain flows, top APYs, and delta-neutral opportunities.
metadata:
  tags: wayfinder, alpha-lab, alpha, insights, twitter, chain-flows
---

## What you need to know (TL;DR)

**Alpha Lab = Scored alpha insight feed**

```python
from wayfinder_paths.core.clients import ALPHA_LAB_CLIENT

# Search all insights (sorted by score)
await ALPHA_LAB_CLIENT.search()

# Filter by type
await ALPHA_LAB_CLIENT.search(scan_type="twitter_post", min_score=0.7)

# Text search
await ALPHA_LAB_CLIENT.search(search="ETH funding", limit=10)

# List available scan types
await ALPHA_LAB_CLIENT.get_types()
```

**MCP quick access:**

```
wayfinder://alpha-lab/search/_/all/_/_/20                          # Top 20 insights
wayfinder://alpha-lab/search/_/twitter_post/_/_/10                 # Top 10 tweets
wayfinder://alpha-lab/search/ETH/all/_/_/10                        # Search "ETH"
wayfinder://alpha-lab/search/_/all/2026-03-06T00:00:00Z/_/20       # Today's insights
wayfinder://alpha-lab/types                                        # List scan types
```

URI format: `wayfinder://alpha-lab/search/{query}/{scan_type}/{created_after}/{created_before}/{limit}`
- `query`: text search, `_` for none
- `scan_type`: filter by type, `all` for none
- `created_after` / `created_before`: ISO 8601 datetime bounds, `_` to skip
- `limit`: max results (default 20, max 200)

**Critical gotchas:**
- Client returns data directly (not tuples) — `data = await ALPHA_LAB_CLIENT.search()`
- Scores are 0-1 floats (1 = most insightful)
- MCP resource is sorted by score descending (highest first); use Python client for custom sort/pagination
- Max 200 results per call; use `offset` for pagination (Python client only)

## When to use

- "What's the latest alpha?" / "Show me today's insights"
- "Any interesting tweets about ETH?"
- "What chain flows are happening?"
- "What are the highest-scored insights?"

**Alpha Lab is self-contained for alpha requests.** It already includes `delta_lab_top_apy` and `delta_lab_best_delta_neutral` scan types, so do NOT also query Delta Lab separately. Only use Delta Lab directly when the user asks for raw rates, historical timeseries, or detailed screening — not for "today's alpha".

## How to use

- [rules/what-is-alpha-lab.md](rules/what-is-alpha-lab.md) - What Alpha Lab is and its scan types
- [rules/high-value-reads.md](rules/high-value-reads.md) - Core queries and MCP URIs
- [rules/response-structures.md](rules/response-structures.md) - Response shapes
- [rules/gotchas.md](rules/gotchas.md) - Common mistakes
