---
name: using-delta-lab
description: How to use the Delta Lab client in Wayfinder Paths for basis APY discovery, delta-neutral pair finding, and opportunity analysis across protocols.
metadata:
  tags: wayfinder, delta-lab, basis, delta-neutral, apy, opportunities
---

## What you need to know (TL;DR)

**Delta Lab = Multi-protocol APY discovery tool**

```python
from wayfinder_paths.core.clients import DELTA_LAB_CLIENT

# Find all yield opportunities for an asset
await DELTA_LAB_CLIENT.get_basis_apy_sources(basis_symbol="BTC", lookback_days=7)

# Find best delta-neutral pairs (carry + hedge)
await DELTA_LAB_CLIENT.get_best_delta_neutral_pairs(basis_symbol="ETH", limit=20)

# Look up asset metadata
await DELTA_LAB_CLIENT.get_asset(asset_id=1)
```

**Critical gotchas:**
- Use uppercase symbols: `"BTC"` not `"bitcoin"` or `"btc"`
- APY can be `null` - always filter: `[o for o in opps if o["apy"]["value"] is not None]`
- Delta Lab is **read-only** (no execution, just discovery)

## When to use

Use this skill when you are:
- Discovering basis opportunities for a given asset (BTC, ETH, etc.)
- Finding best delta-neutral pair candidates
- Analyzing APY sources across different protocols and venues
- Understanding risk metrics and carry/hedge leg compositions
- Comparing rates across Hyperliquid, Moonwell, Boros, Pendle, etc.

## How to use

- [rules/what-is-delta-lab.md](rules/what-is-delta-lab.md) - Mental model: what Delta Lab is, basis symbols, and data sources
- [rules/high-value-reads.md](rules/high-value-reads.md) - Core queries: APY sources, delta-neutral pairs, asset lookups
- [rules/response-structures.md](rules/response-structures.md) - Understanding opportunities, APY components, and risk metrics
- [rules/gotchas.md](rules/gotchas.md) - Common mistakes, symbol resolution, and filtering
