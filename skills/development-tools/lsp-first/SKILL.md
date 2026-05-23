---
name: lsp-first
description: "LSP 優先開發策略工具。用於：(1) 查詢 LSP 操作指令, (2) 配置新語言 LSP 插件, (3) LSP vs MCP 工具選擇決策, (4) 自建 LSP 插件指南"
---

# LSP 優先開發策略

---

## 核心原則

**LSP 能解決的問題必須優先使用 LSP**

### 優先使用 LSP 的理由

| 優勢 | 說明 | 效益 |
|------|------|------|
| **效能** | ~50ms vs ~45 秒 | 900x 加速 |
| **Token 效率** | 結構化資料輸出 | 降低 API 成本 |
| **語意精準** | 語言伺服器分析 | 非文字比對 |

---

## LSP 環境自動檢查

**Session 啟動時自動執行 LSP 環境檢查**

### 檢查項目

1. **基本 LSP**（所有專案必備）
   - marksman (Markdown)
   - yaml-language-server (YAML)

2. **語言特定 LSP**（根據專案類型）
   - Flutter/Dart: Dart SDK 內建 LSP
   - TypeScript/JavaScript: vtsls
   - Python: pyright
   - Go: gopls
   - Rust: rust-analyzer

### 跨平台支援

| 平台 | 安裝工具 |
|------|---------|
| macOS | Homebrew, npm |
| Linux | apt/dnf/pacman, Homebrew, npm |
| Windows | winget, scoop, npm |

### 相關檔案

- **檢查腳本**: `.claude/hooks/lsp-environment-check.py`
- **配置檔案**: `.claude/hooks/lsp-check-config.json`
- **整合位置**: `.claude/hooks/startup-check-hook.sh` (步驟 6.6)

---

## LSP 9 種操作詳解

### 1. goToDefinition - 跳轉定義

**用途**：找到符號的定義位置

**使用場景**：
- 追蹤函式來源
- 查看類別定義
- 理解變數宣告

**範例**：
```
LSP(operation="goToDefinition", filePath="lib/main.dart", line=15, character=10)
```

### 2. findReferences - 查找引用

**用途**：找出所有引用某符號的位置

**使用場景**：
- 重構前影響分析
- 變更影響評估
- 了解 API 使用情況

**範例**：
```
LSP(operation="findReferences", filePath="lib/domains/book/book.dart", line=26, character=6)
```

### 3. hover - 懸停資訊

**用途**：取得符號的型別資訊和文件

**使用場景**：
- 查看 API 文件
- 確認參數型別
- 理解返回值

**Dart MCP 替代**：
```
mcp__dart__hover(uri="file:///path/to/file.dart", line=10, column=5)
```

### 4. documentSymbol - 文件符號

**用途**：列出檔案中所有符號

**使用場景**：
- 快速理解檔案結構
- 找出類別中的方法
- 瀏覽模組 API

### 5. workspaceSymbol - 工作區搜尋

**用途**：跨檔案搜尋符號

**使用場景**：
- 找出類別定義
- 搜尋全域函式
- 模糊符號查詢

**Dart MCP 替代**：
```
mcp__dart__resolve_workspace_symbol(query="ClassName")
```

### 6. goToImplementation - 實作查找

**用途**：找出介面或抽象類別的所有實作

**使用場景**：
- 追蹤抽象類別實作
- 理解多態架構
- 驗證介面契約

### 7. prepareCallHierarchy - 呼叫層級準備

**用途**：準備呼叫層級分析

**使用場景**：
- 準備函式呼叫分析
- 取得呼叫層級項目

### 8. incomingCalls - 呼叫來源

**用途**：找出誰呼叫了這個函式

**使用場景**：
- 重構前影響分析
- 追蹤事件傳遞
- 了解依賴關係

### 9. outgoingCalls - 呼叫目標

**用途**：找出這個函式呼叫了誰

**使用場景**：
- 理解函式依賴
- 分析執行流程
- 追蹤呼叫鏈

---

## 工具選擇決策樹

```
需求分析：
├─ 需要呼叫層級分析？ → LSP (incomingCalls / outgoingCalls)
├─ 需要查找介面實作？ → LSP (goToImplementation)
├─ 需要符號定義？ → LSP (goToDefinition) / Dart MCP
├─ 需要引用追蹤？ → LSP (findReferences) / Serena
├─ 需要 Hover 資訊？ → Dart MCP (mcp__dart__hover)
├─ 需要工作區搜尋？ → Dart MCP (mcp__dart__resolve_workspace_symbol)
├─ 需要執行測試？ → Dart MCP (mcp__dart__run_tests)
├─ 需要 Hot Reload？ → Dart MCP (mcp__dart__hot_reload)
├─ 需要精準符號編輯？ → Serena (replace_symbol_body)
└─ LSP 不可用？ → Serena (備援方案)
```

### 工具優先順序

1. **優先**: LSP 工具 / 語言 MCP 工具
2. **次選**: Serena MCP（LSP 功能等效替代）
3. **備援**: 傳統 Grep/Glob 搜尋

---

## 當前可用的 MCP LSP 功能

### Dart MCP 工具

| 工具 | 功能 | 對應 LSP 操作 |
|------|------|-------------|
| `mcp__dart__hover` | 懸停資訊 | hover |
| `mcp__dart__resolve_workspace_symbol` | 工作區搜尋 | workspaceSymbol |
| `mcp__dart__signature_help` | 簽名提示 | signatureHelp |
| `mcp__dart__analyze_files` | 專案分析 | diagnostics |

### Serena MCP 工具（備援）

| 工具 | 功能 | 對應 LSP 操作 |
|------|------|-------------|
| `mcp__serena__get_symbols_overview` | 符號概覽 | documentSymbol |
| `mcp__serena__find_symbol` | 符號查找 | goToDefinition |
| `mcp__serena__find_referencing_symbols` | 引用追蹤 | findReferences |

---

## 支援的語言和 LSP 伺服器

### 自建插件（已配置）

| 語言 | LSP 伺服器 | 插件位置 |
|------|-----------|---------|
| Dart/Flutter | dart language-server | `.claude/plugins/dart-lsp/` |
| Markdown | marksman | `.claude/plugins/marksman-lsp/` |
| YAML | yaml-language-server | `.claude/plugins/yaml-lsp/` |

### 官方插件市場

```bash
# 新增插件市場
/plugin marketplace add boostvolt/claude-code-lsps
```

| 語言 | LSP 伺服器 | 安裝指令 |
|------|-----------|---------|
| Dart/Flutter | dart-analyzer | `/plugin install dart-analyzer@claude-code-lsps` |
| TypeScript/JavaScript | vtsls | `/plugin install vtsls@claude-code-lsps` |
| Python | pyright | `/plugin install pyright@claude-code-lsps` |
| Go | gopls | `/plugin install gopls@claude-code-lsps` |
| Rust | rust-analyzer | `/plugin install rust-analyzer@claude-code-lsps` |
| Java | jdtls | `/plugin install jdtls@claude-code-lsps` |
| C/C++ | clangd | `/plugin install clangd@claude-code-lsps` |
| C# | omnisharp | `/plugin install omnisharp@claude-code-lsps` |
| PHP | intelephense | `/plugin install intelephense@claude-code-lsps` |
| Kotlin | kotlin | `/plugin install kotlin@claude-code-lsps` |
| Ruby | solargraph | `/plugin install solargraph@claude-code-lsps` |
| HTML/CSS | vscode-langservers | `/plugin install html-css@claude-code-lsps` |

---

## 自建 LSP 插件指南

### 目錄結構

```
.claude/plugins/<plugin-name>/
├── .claude-plugin/
│   └── plugin.json          # 插件清單
└── .lsp.json                 # LSP 配置
```

### plugin.json 範本

```json
{
  "name": "<plugin-name>",
  "version": "1.0.0",
  "description": "LSP plugin for <language>",
  "author": "Your Name"
}
```

### .lsp.json 範本

```json
{
  "<language-id>": {
    "command": "<lsp-server-command>",
    "args": ["--stdio"],
    "extensionToLanguage": {
      ".<ext>": "<language-id>"
    }
  }
}
```

### 範例：Markdown LSP 插件

**plugin.json**：
```json
{
  "name": "marksman-lsp",
  "version": "1.0.0",
  "description": "Marksman Markdown LSP for Claude Code",
  "author": "Project Team"
}
```

**.lsp.json**：
```json
{
  "markdown": {
    "command": "marksman",
    "args": ["server"],
    "extensionToLanguage": {
      ".md": "markdown",
      ".markdown": "markdown"
    }
  }
}
```

---

## 效能對比數據

| 操作 | LSP | 傳統方法 | 效能提升 |
|------|-----|---------|---------|
| 查找引用 | ~50ms | ~45 秒（grep） | 900x |
| 跳轉定義 | ~10ms | ~5 秒（搜尋） | 500x |
| 符號概覽 | ~20ms | ~10 秒（解析） | 500x |
| 呼叫層級 | ~100ms | 無法自動化 | ∞ |

### Token 效率對比

| 工具 | 輸出類型 | 預估 Token |
|------|---------|-----------|
| **LSP findReferences** | 結構化位置列表 | ~100-500 |
| **Dart MCP hover** | 結構化資訊 | ~200-500 |
| Serena find_referencing_symbols | 完整上下文 | ~2000-5000 |
| Grep 搜尋 | 完整行內容 | ~3000-10000 |

---

## 常見問題和故障排除

### Q1: "No LSP server available for file type"

**可能原因**：
1. 該語言的 LSP 插件未配置
2. LSP 伺服器未安裝
3. 環境變數未設定

**解決方案**：
```bash
# 1. 確認 LSP 伺服器已安裝
which marksman
which yaml-language-server

# 2. 啟用 LSP 功能（如需要）
export ENABLE_LSP_TOOL=1

# 3. 執行 LSP 環境檢查
./.claude/hooks/lsp-environment-check.py
```

### Q2: LSP 操作返回空結果

**可能原因**：
1. 座標位置不正確（LSP 使用 0-based）
2. 檔案尚未被 LSP 索引
3. LSP 伺服器尚未啟動

**解決方案**：
1. 確認 line 和 column 使用 0-based（第一行是 0）
2. 等待幾秒讓 LSP 完成索引
3. 重新啟動 Claude Code

### Q3: 自建插件無法運作

**檢查清單**：
- [ ] LSP 伺服器已安裝且在 PATH 中
- [ ] `.lsp.json` 格式正確
- [ ] `extensionToLanguage` 對應正確
- [ ] 插件目錄結構正確

---

## 相關工具和文件

### 相關 Skills
- `/ticket-create` - Atomic Ticket 建立
- `/ticket-track` - Ticket 狀態追蹤
- `/startup-check` - Session 啟動檢查

### 相關文件
- [CLAUDE.md - LSP 優先策略章節](./../../CLAUDE.md)
- [boostvolt/claude-code-lsps](https://github.com/boostvolt/claude-code-lsps)
- [Marksman (Markdown LSP)](https://github.com/artempyanykh/marksman)
- [yaml-language-server](https://github.com/redhat-developer/yaml-language-server)

### LSP 環境檢查相關
- **檢查腳本**: `.claude/hooks/lsp-environment-check.py`
- **配置檔案**: `.claude/hooks/lsp-check-config.json`
- **權限白名單**: `.claude/settings.local.json`

