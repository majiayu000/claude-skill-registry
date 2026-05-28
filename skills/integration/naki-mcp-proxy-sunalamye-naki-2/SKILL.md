---
name: naki-mcp-proxy
description: Token-efficient proxy for Naki's 47 MCP tools. Routes user intent to optimal MCP tool via agent isolation, saving 40-70% tokens. Use for any Naki game control, bot status, or UI operation.
allowed-tools:
  - Task
  - Read
  - Bash
---

# Naki MCP Proxy

Base directory: {baseDir}

## Core Mission

Provide token-efficient access to Naki's 47 MCP tools through agent-based proxy pattern. Main context stays lightweight (~100-200 tokens) while tool schemas load only in agent context.

## Architecture

```
User Intent → Skill Router → Agent (tool discovery + execution) → Result
     ↓              ↓                    ↓                          ↓
  ~50 tokens    ~50 tokens        ~500-1500 tokens (isolated)   Formatted output
```

**Token Savings**: 40-70% compared to direct MCP tool loading.

## Execution Protocol

### Step 1: Intent Classification

Classify user request into tool category:

| Category | Keywords | Primary Tools |
|----------|----------|---------------|
| **Bot 控制** | 推薦、AI、自動打、觸發 | `bot_status`, `bot_trigger` |
| **遊戲狀態** | 手牌、遊戲、出牌、動作 | `game_state`, `game_hand`, `game_action` |
| **高亮** | 高亮、顏色、推薦顯示 | `highlight_tile`, `show_recommendations` |
| **大廳** | 匹配、段位、大廳 | `lobby_start_match`, `lobby_status` |
| **表情** | 表情、emoji | `game_emoji`, `game_emoji_list` |
| **UI** | 點擊、JS、玩家名稱 | `execute_js`, `click`, `ui_names_*` |
| **系統** | 日誌、狀態、幫助 | `get_logs`, `get_status`, `get_help` |

### Step 2: Agent Dispatch

Launch agent with tool execution prompt:

```
Task tool with subagent_type="general-purpose":
prompt: |
  Execute Naki MCP tool for: [user intent]

  Available tools (port 8765):
  - [relevant tools based on category]

  Steps:
  1. Call mcp__naki__[tool_name] with appropriate parameters
  2. Parse and format response
  3. Return concise result

  If tool fails, try alternative or report error.
```

### Step 3: Result Formatting

Return agent result to user with:
- Key data points (hand tiles, recommendations, status)
- Action taken confirmation
- Error explanation if failed

## Tool Quick Reference

### Most Used Tools

| Intent | Tool | Example |
|--------|------|---------|
| 查看 AI 推薦 | `bot_status` | 顯示手牌和推薦動作 |
| 觸發自動打牌 | `bot_trigger` | 執行 AI 推薦的動作 |
| 查看遊戲狀態 | `game_state` | 當前局面完整信息 |
| 執行遊戲動作 | `game_action` | 出牌、吃、碰、槓 |
| 高亮手牌 | `highlight_tile` | 指定牌高亮顯示 |
| 開始匹配 | `lobby_start_match` | 段位場匹配 |
| 執行 JS | `execute_js` | 遊戲內 JavaScript |
| 查看日誌 | `get_logs` | Debug 日誌記錄 |

### Tool Categories (47 total)

| Category | Count | See Reference |
|----------|-------|---------------|
| 系統類 | 4 | `{baseDir}/references/tool-catalog.md` |
| Bot 控制 | 7 | |
| 遊戲狀態 | 6 | |
| 高亮控制 | 6 | |
| 表情 | 4 | |
| 大廳 | 9 | |
| UI 控制 | 11 | |

## Common Workflows

### 1. 自動段位場流程

```
1. lobby_status      → 確認在大廳
2. lobby_navigate    → 前往段位場 (page: 1)
3. lobby_start_match → 開始匹配 (match_mode: 5 = 銀半)
4. bot_status        → 等待並查看推薦
```

### 2. 手牌調試流程

```
1. game_state   → 獲取完整遊戲狀態
2. game_hand    → 查看手牌詳情
3. bot_status   → 查看 AI 分析
4. get_logs     → 檢查操作日誌
```

### 3. 高亮測試流程

```
1. highlight_status  → 查看當前狀態
2. highlight_tile    → 高亮指定牌 (tileIndex, color)
3. hide_highlight    → 清除所有高亮
```

## Match Mode Reference

| ID | 段位場 |
|----|-------|
| 1, 2 | 銅東, 銅半 |
| 4, 5 | 銀東, 銀半 |
| 7, 8 | 金東, 金半 |
| 10, 11 | 玉東, 玉半 |
| 13, 14 | 王座東, 王座半 |

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Tool not found | Naki 未啟動 | 啟動 Naki app |
| Port 8765 unavailable | 埠被佔用 | `lsof -i :8765` 檢查 |
| Game API unavailable | 遊戲未載入 | 使用 `detect` 檢查 |
| Bot not active | 未在遊戲中 | 等待遊戲開始 |

## Resource Index

| Resource | Purpose | Load When |
|----------|---------|-----------|
| `{baseDir}/references/tool-catalog.md` | 完整 47 工具列表和參數 | 需要查找工具參數 |
| `{baseDir}/references/usage-patterns.md` | 進階使用模式 | 複雜操作場景 |

---

**Naki MCP Proxy v1.0** - Token-Efficient Game Control
