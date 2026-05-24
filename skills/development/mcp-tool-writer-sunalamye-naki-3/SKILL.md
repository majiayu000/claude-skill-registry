---
name: mcp-tool-writer
description: Create, modify, and manage MCP tools for the Naki mahjong AI assistant. Use when adding new MCP tools, modifying existing tools, or fixing tool-related issues. This skill understands the Protocol-based MCPTool architecture.
allowed-tools: Read, Glob, Grep, Write, Edit, Bash
---

# Naki MCP Tool Writer

Base directory: {baseDir}

<IMPORTANT>
**MCP 調用規則**: 測試新建的 MCP 工具時，使用 `/naki-mcp-proxy` skill 調用。
</IMPORTANT>

This skill helps create and modify MCP (Model Context Protocol) tools for the Naki project using the Protocol-based architecture.

## Architecture Overview

Naki uses a Protocol-based MCP architecture:

```
command/Services/MCP/
├── MCPTool.swift          - Protocol 定義 + Schema 類型
├── MCPContext.swift       - 執行上下文 (async/await 支持)
├── MCPToolRegistry.swift  - 工具註冊表 (單例)
├── MCPHandler.swift       - MCP 協議處理器
└── Tools/
    ├── SystemTools.swift  - 系統類工具 (get_status, get_help, get_logs, clear_logs)
    ├── BotTools.swift     - Bot 控制工具 (bot_status, bot_trigger, bot_ops, bot_deep, bot_chi, bot_pon, bot_sync)
    ├── GameTools.swift    - 遊戲狀態工具 (game_state, game_hand, game_ops, game_discard, game_action)
    └── UITools.swift      - UI 操作工具 (execute_js, detect, explore, test_indicators, click, calibrate, ui_names_*)
```

## Current Registered Tools (47 total)

| Category | Count | Examples |
|----------|-------|----------|
| System | 4 | `get_status`, `get_help`, `get_logs`, `clear_logs` |
| Bot | 7 | `bot_status`, `bot_trigger`, `bot_ops`, `bot_deep`, `bot_chi`, `bot_pon`, `bot_sync` |
| Game | 6 | `game_state`, `game_hand`, `game_ops`, `game_discard`, `game_action`, `game_emoji` |
| Highlight | 6 | `highlight_tile`, `highlight_status`, `show_recommendations`, `hide_highlight` |
| Emoji | 4 | `game_emoji`, `game_emoji_list`, `game_emoji_random` |
| Lobby | 9 | `lobby_status`, `lobby_navigate`, `lobby_start_match`, `lobby_cancel_match` |
| UI | 11 | `execute_js`, `detect`, `explore`, `click`, `calibrate`, `ui_names_*` |

See `/naki-mcp-proxy` for complete tool catalog.

## How to Create a New MCP Tool

### Step 1: Define the Tool Struct

Create a new struct implementing `MCPTool` protocol in the appropriate `Tools/*.swift` file:

```swift
struct MyNewTool: MCPTool {
    // 1. 工具名稱 (唯一標識符)
    static let name = "my_new_tool"

    // 2. 工具描述 (給 AI 看的說明)
    static let description = "描述這個工具做什麼，何時使用"

    // 3. 輸入參數 Schema
    static let inputSchema = MCPInputSchema(
        properties: [
            "param1": .string("參數1的描述"),
            "param2": .integer("參數2的描述")
        ],
        required: ["param1"]  // 必填參數
    )

    // 4. 上下文 (用於訪問 JS、Bot 等)
    private let context: MCPContext

    init(context: MCPContext) {
        self.context = context
    }

    // 5. 執行邏輯
    func execute(arguments: [String: Any]) async throws -> Any {
        guard let param1 = arguments["param1"] as? String else {
            throw MCPToolError.missingParameter("param1")
        }

        // 執行邏輯...

        return ["success": true, "result": "..."]
    }
}
```

### Step 2: Register the Tool

在 `MCPToolRegistry.swift:142-182` 的 `registerBuiltInTools()` 方法中添加：

```swift
register(MyNewTool.self)
```

**注意**: Tools 列表會自動從 Registry 生成，無需手動維護 JSON 檔案。

## Input Schema Types

```swift
// 無參數
static let inputSchema = MCPInputSchema.empty

// 有參數
static let inputSchema = MCPInputSchema(
    properties: [
        "stringParam": .string("字串參數描述"),
        "intParam": .integer("整數參數描述"),
        "numberParam": .number("數字參數描述"),
        "boolParam": .boolean("布林參數描述"),
        "objectParam": .object("物件參數描述")
    ],
    required: ["stringParam"]  // 必填參數列表
)
```

## Context API

工具可以通過 `context` 訪問以下功能（定義在 `MCPContext.swift:15-38`）：

```swift
// 執行 JavaScript（async/await）
let result = try await context.executeJavaScript("return document.title")

// 獲取 Bot 狀態
let status = context.getBotStatus()

// 觸發自動打牌
context.triggerAutoPlay()

// 日誌操作
let logs = context.getLogs()
context.clearLogs()
context.log("記錄訊息")

// 服務器埠號
let port = context.serverPort
```

## ⚠️ JavaScript 執行注意事項

**重要**：`context.executeJavaScript()` 必須使用 `return` 語句才能正確返回值！

```swift
// ✅ 正確：使用 return 語句
let title = try await context.executeJavaScript("return document.title")
let sum = try await context.executeJavaScript("return 1 + 1")
let json = try await context.executeJavaScript("return JSON.stringify({a:1})")

// ❌ 錯誤：沒有 return，結果為 nil
let title = try await context.executeJavaScript("document.title")  // 返回 nil！
```

**常見模式**：

```swift
// 調用遊戲 API 並返回 JSON
let script = "return JSON.stringify(window.__nakiGameAPI.getGameState())"
let result = try await context.executeJavaScript(script)

// 執行操作並返回布林值
let script = "return window.__nakiGameAPI.discardTile(0)"
let success = try await context.executeJavaScript(script) as? Bool ?? false

// 檢查 API 是否存在
let script = "return typeof window.__nakiGameAPI !== 'undefined'"
let exists = try await context.executeJavaScript(script) as? Bool ?? false
```

## Error Handling

使用 `MCPToolError`（定義在 `MCPTool.swift:129-147`）處理錯誤：

```swift
throw MCPToolError.missingParameter("paramName")
throw MCPToolError.invalidParameter("paramName", expected: "string")
throw MCPToolError.executionFailed("原因描述")
throw MCPToolError.notAvailable("資源名稱")
```

## Tool Categories & File Locations

| Category | File | When to Add Here |
|----------|------|-----------------|
| 系統 | `SystemTools.swift` | Server status, logs, help |
| Bot | `BotTools.swift` | Bot control, AI inference |
| 遊戲 | `GameTools.swift` | Game state, hand, actions |
| UI | `UITools.swift` | JS execution, clicks, detection |

## Checklist for New Tools

- [ ] 定義唯一的 `name`（snake_case 格式）
- [ ] 寫清楚的 `description`（給 AI 理解，包含何時使用）
- [ ] 定義正確的 `inputSchema`
- [ ] 實現 `execute()` 方法（async throws）
- [ ] 處理所有錯誤情況（使用 MCPToolError）
- [ ] 在 `MCPToolRegistry.swift:142-182` 中註冊
- [ ] 構建測試通過
- [ ] 使用 MCP 工具測試功能

## Testing

構建並測試：

```bash
# 構建
xcodebuild build -project Naki.xcodeproj -scheme Naki

# 啟動應用後，使用 MCP 工具測試
mcp__naki__<tool_name>
```

## Reference Documentation

For detailed specifications and more examples, see:
- [Protocol Reference](references/reference.md) - Complete MCPTool protocol, context API, schema types, and code examples
