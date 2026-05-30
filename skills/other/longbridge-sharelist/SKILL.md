---
name: longbridge-sharelist
description: |
  Community stock lists (Sharelist) via Longbridge Securities — browse popular and personal lists, view list details and constituents, create/delete/manage your own lists, and add/remove symbols. Like a public watchlist that other users can subscribe to. Read operations require no login; write operations (create/delete/add/remove/sort) require login. Triggers: "股票清单", "公开清单", "热门清单", "社区选股", "选股清单", "股票列表", "清单管理", "股票清單", "公開清單", "熱門清單", "社區選股", "選股清單", "訂閱清單", "sharelist", "stock list", "public watchlist", "popular list", "community picks", "stock collection", "create list", "manage list", "subscribe list".
license: MIT
metadata:
  author: longbridge
  version: "1.0.0"
  risk_level: read_only
  requires_login: false
  default_install: true
  requires_mcp: false
  tier: read
---

# longbridge-sharelist

Community stock lists (Sharelist): browse, create, and manage public curated stock collections that other Longbridge users can subscribe to.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

- *"看看热门股票清单"*, *"熱門清單"*, *"show popular share lists"* → `longbridge sharelist popular`
- *"我的清单"*, *"我的股票列表"*, *"my share lists"* → `longbridge sharelist` (requires login)
- *"查看清单 123 的成分股"*, *"查看清單詳情"*, *"list detail"* → `longbridge sharelist detail <ID>`
- *"创建一个清单叫精选科技股"*, *"建立清單"*, *"create a list"* → `longbridge sharelist create` (requires login, two-step confirm)
- *"把 TSLA 加到清单 123"*, *"新增股票到清單"*, *"add stock to list"* → `longbridge sharelist add` (requires login, two-step confirm)
- *"从清单里移除 AAPL"*, *"移除股票"*, *"remove from list"* → `longbridge sharelist remove` (requires login, two-step confirm)
- *"删除清单 123"*, *"刪除清單"*, *"delete list"* → `longbridge sharelist delete` (requires login, two-step confirm)

For personal watchlist management (non-public, private), defer to `longbridge-watchlist-admin`.

## Write operation protocol

**All mutating operations (create / add / remove / delete / sort) require a two-step preview + confirm protocol:**

1. **Preview**: Show the user exactly what will change (list name, symbols affected, action).
2. **Wait for explicit confirmation** ("确认" / "確認" / "confirm" / "yes").
3. Only then execute the CLI command.

Never combine preview and execution in one step.

## Workflow

**Read (no login needed):**
1. For popular lists: call `longbridge sharelist popular --count N`.
2. For a specific list: call `longbridge sharelist detail <ID>`.
3. Render a table of lists (ID / name / owner / subscriber count / symbol count) or a constituent table (symbol / name / last price / change%).

**Write (login required):**
1. Check the user intent is unambiguous. If vague (e.g. "整理一下我的清单"), ask for specifics.
2. Preview the operation clearly.
3. After user confirms, execute the CLI command.
4. Report success or relay any error verbatim.

## CLI

> Run `longbridge sharelist --help` before constructing calls — it is the canonical source for flags and subcommands.

```bash
# Read operations (no login required)
longbridge sharelist --format json                          # My lists and subscribed lists
longbridge sharelist popular --count 10 --format json      # Popular community lists
longbridge sharelist detail <ID> --format json             # List details + constituents

# Write operations (login required — two-step confirm first)
longbridge sharelist create --name "我的精选" --format json
longbridge sharelist add <ID> TSLA.US AAPL.US --format json
longbridge sharelist remove <ID> TSLA.US --format json
longbridge sharelist delete <ID> --format json
longbridge sharelist sort <ID> TSLA.US AAPL.US 700.HK --format json

# Always check flags first
longbridge sharelist --help
```

## Output

**List roster** — table: ID / name / owner / subscribers / symbols / created date.

**List detail / constituents** — table: rank / symbol / company name / last price / change% / market cap (if available).

**Write result** — confirm success with the list ID and action taken; show the updated constituent count.

Cite **Longbridge Securities** as the data source.

## Error handling

| 情形 | 简体回复 | 繁體回覆 / English reply |
|---|---|---|
| `command not found: longbridge` | 请安装 longbridge-terminal | 請安裝 longbridge-terminal / Install longbridge-terminal |
| `not logged in` / 写操作未登录 | 写操作需要登录，请运行 `longbridge auth login` | 請執行 `longbridge auth login` / Run `longbridge auth login` |
| List ID 不存在 | 清单 ID 不存在，请确认后重试 | 清單 ID 不存在 / List ID not found — verify and retry |
| 股票代码格式错误 | 请使用 CODE.MARKET 格式，如 TSLA.US | 請使用 CODE.MARKET 格式 / Use CODE.MARKET format |
| 操作指令不明确 | 请明确说明要执行的操作 | 請明確說明操作 / Please specify the exact action |
| 其他 stderr | 原样返回错误，不静默重试 | 原樣返回 / Surface verbatim, never retry |

## MCP fallback

When the CLI binary is missing, fall back via the equivalent MCP tool:

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime — do not rely on hardcoded tool names.

If the tool name does not resolve, ask the user to install the CLI.

## Related skills

| Skill | Why |
|-------|-----|
| `longbridge-watchlist` | Read-only access to private personal watchlist groups. |
| `longbridge-watchlist-admin` | Mutating operations on private personal watchlist groups. |
| `longbridge-constituent` | Index/ETF constituent lists (not community-curated). |
| `longbridge-quote` | Real-time quotes for symbols found in a list. |

## File layout

```
longbridge-sharelist/
└── SKILL.md          # prompt-only, no scripts/
```
