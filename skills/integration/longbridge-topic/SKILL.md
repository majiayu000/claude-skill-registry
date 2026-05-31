---
name: longbridge-topic
description: |
  Longbridge community topics for stocks — list topics by symbol, search by keyword, view topic detail and replies, browse your own topics, and post new topics or replies. Read operations require no login; posting requires login. Triggers: "社区话题", "股票讨论", "社区讨论", "发帖", "话题", "评论", "社群", "市场看法", "帖子", "社區話題", "股票討論", "社區討論", "發帖", "話題", "評論", "社群", "社區看法", "community topic", "stock discussion", "community post", "market opinion", "post comment", "TSLA community", "AAPL discussion", "我的话题", "我的帖子", "发布话题", "回复话题", "發布話題", "回覆話題", "发表看法", "community reply".
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

# longbridge-topic

Browse and participate in Longbridge community discussions — list topics for a stock, search by keyword, read detail and replies, view your own posts, and publish new content.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

- *"TSLA 社区在聊什么"*, *"NVDA 話題"*, *"AAPL discussion"*
- *"搜索关于 AI 的话题"*, *"search community for earnings"*
- *"查看话题 12345 的详情和回复"*, *"topic detail 12345"*
- *"我的话题"*, *"my posts"*, *"我的帖子"*
- *"发一条关于 NVDA 的帖子"*, *"post a comment on 700.HK"* (requires login)
- *"回复话题 12345"*, *"reply to topic"* (requires login)

## Workflow

1. Identify the operation: list / search / detail / replies / mine / create / create-reply.
2. For **list**: resolve symbol to `<CODE>.<MARKET>`.
3. For **search**: use the keyword directly.
4. For **detail / replies / create-reply**: use the topic ID from context or ask for it.
5. For **create / create-reply**: check login first; if not logged in, tell user to run `longbridge auth login`.
6. Call the CLI (preferred) or MCP fallback; present results in a readable format.

## CLI

Run `longbridge topic --help` to discover available subcommands and flags before use.

```bash
# Discover available subcommands and flags
longbridge topic --help

# Example: list topics for a stock (verify subcommand name via --help)
longbridge topic <SYMBOL> --format json

# Example: search, detail, replies, my topics, post, reply — run --help to find exact subcommand names and flags
```

## Output

**Topic list** — for each item, render: title, author, like count, comment count, creation time, topic ID.

**Topic detail** — render body text, author, publish time, likes, view count, and a short content summary.

**Replies** — render each reply: author, content, time, likes.

**Create / create-reply** — confirm success and return the new topic/reply ID.

Field translations:

| Field (likely) | 简体 | 繁體 | English |
|---|---|---|---|
| `title` | 标题 | 標題 | Title |
| `body / content` | 内容 | 內容 | Content |
| `author` | 作者 | 作者 | Author |
| `like_count` | 点赞数 | 點贊數 | Likes |
| `comment_count` | 评论数 | 評論數 | Comments |
| `created_at` | 发布时间 | 發布時間 | Published |

## Error handling

| Situation | 简体 | 繁體 | English |
|---|---|---|---|
| `command not found: longbridge` | 退回 MCP；如未配置，提示安装 longbridge-terminal | 退回 MCP；如未設定，提示安裝 longbridge-terminal | Fall back to MCP; if unavailable, ask user to install longbridge-terminal |
| `not logged in` / `unauthorized` | 发布/回复需要登录，请运行 `longbridge auth login` | 發布/回覆需要登入，請執行 `longbridge auth login` | Posting requires login — run `longbridge auth login` |
| Symbol not found | 无法识别股票代码，请确认格式如 TSLA.US / 700.HK | 無法識別股票代碼，請確認格式如 TSLA.US / 700.HK | Cannot resolve symbol — check format e.g. TSLA.US / 700.HK |
| Topic ID not found | 话题不存在或已删除 | 話題不存在或已刪除 | Topic not found or deleted |
| Other stderr | 原文转达，不做静默重试 | 原文轉達，不作靜默重試 | Relay verbatim; never retry silently |

## MCP fallback

If `longbridge` CLI is not installed (`command not found`), use MCP tools:

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime — do not rely on hardcoded tool names.

## Related skills

- News and filings → `longbridge-news`
- Community sentiment as part of omnibus digest → `longbridge-news` (includes `topic` in full mode)
- Real-time quote → `longbridge-quote`

## File layout

```
longbridge-topic/
└── SKILL.md          # prompt-only, no scripts/
```
