---
name: longbridge-watchlist
description: |
  Read-only access to the user's Longbridge watchlist groups and the symbols inside each group. Mutations (create / rename / add / remove) belong in longbridge-watchlist-admin. Requires longbridge login. Triggers: "我的自选股", "自选股有哪些", "我关注的股票", "我的分组", "自選股", "關注的股票", "分組", "watchlist", "my watchlist", "favorited stocks", "watch groups".
license: MIT
metadata:
  author: longbridge
  version: "1.0.0"
  risk_level: account_read
  requires_login: true
  default_install: true
---

# longbridge-watchlist

Read-only listing of watchlist groups and member symbols. For mutations use `longbridge-watchlist-admin`.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.
>
> **Privacy**: a watchlist reveals trading interest. Only return detailed lists in direct conversation.

## When to use

- *"我的自选股"*, *"watchlist contents"* → list everything
- *"我的「科技股」分组"*, *"my Tech group"* → list everything, then filter by group name
- *"分组 ID 12345 里有什么"* → list everything, then filter by group id

The CLI returns all groups in one call; the LLM filters in-memory based on the user's intent.

## Chained workflows (very common)

After getting symbols from this skill, route to other skills for the actual data:

| User asks | Flow |
|---|---|
| *"我自选股的港股涨幅"* | this skill → filter `.HK` → `longbridge-quote` (batch) |
| *"我自选最近一周走势"* | this skill → all symbols → `longbridge-kline` (loop) |
| *"我自选的总市值"* | this skill → all symbols → `longbridge-quote` with `--include-static` |

**Get symbols here, then route the data query to the appropriate skill.** Do not try to compute change rates or charts inside this skill.

## CLI

```bash
longbridge watchlist --format json
```

This lists every watchlist group plus the securities inside each group.

## Output

Array of group objects, each with `{id, name, securities: [{symbol, name, ...}]}`. No matching filter (after LLM-side filtering) → empty array.

## Error handling

If `longbridge` is missing, fall back to MCP. The watchlist read endpoint does not require trade scope, only login — if stderr says `not logged in`, tell the user to run `longbridge auth login`.

## MCP fallback

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime — do not rely on hardcoded tool names.

MCP-only extensions are available; discover them from the MCP server's tool list at runtime.

## Related skills

- Watchlist mutations → `longbridge-watchlist-admin`
- Per-symbol quote / chart → `longbridge-quote`, `longbridge-kline`

## File layout

```
longbridge-watchlist/
└── SKILL.md          # prompt-only, no scripts/
```
