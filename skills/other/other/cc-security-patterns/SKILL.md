---
name: cc-security-patterns
description: "AI Agent 安全設計模式 — 基於 Claude Code 七層縱深防禦架構的逆向分析。Use when: 設計工具安全機制、實作命令過濾、建構權限模型、設計 sandbox。"
version: 202603
context: fork
---

# AI Agent 安全設計模式

基於 Claude Code v2.1.88 的安全機制逆向分析（bashSecurity 2592 行 + bashPermissions 2621 行 + 3 份 readOnlyValidation）。

## 1. 七層縱深防禦

```
[1] Schema Validation (Zod)        — 型別正確嗎
[2] Custom validateInput()         — 業務邏輯合理嗎
[3] Input Sanitization             — 有危險字元嗎
[4] PreToolUse Hooks               — 外部規則要攔嗎
[5] Permission Resolution          — 使用者授權了嗎
[6] Actual Execution               — 最後才執行
[7] PostToolUse Hooks              — 執行後通知/記錄
```

**原則**：每層只問「能否拒絕」。拒絕即停。執行邏輯永遠在最後一層。

## 2. Parser Differential — 核心威脅模型

Claude Code 安全系統最重要的威脅模型：**harness 的 parser 和實際執行環境的 parser 對同一個字串有不同理解**。

```
shell-quote 解析：  FOO=bar rm -rf /  → 三個 token
bash 實際執行：     FOO=bar rm -rf /  → 設定環境變數後執行 rm
```

23 個 Bash validator 中超過一半是針對這種差異。

**防禦原則**：
- 永遠用更嚴格的解析（寧可誤殺）
- 正在遷移到 Tree-sitter AST（`TREE_SITTER_BASH` feature flag）取代字串解析
- 對 deny 規則使用更激進的 env var 剝除（全部剝除 vs allow 時的白名單剝除）

## 3. 白名單 > 黑名單

Claude Code 的 Bash 安全：
- **命令白名單**：SAFE_ENV_VARS 列出允許的環境變數
- **旗標白名單**：每個安全命令有允許的旗標集合
- **路徑白名單**：檔案系統權限用 5 種前綴規則

```
例：git 命令的 -S 旗標
-S 在 git log 中是安全的（搜尋 diff）
-S 在 git diff 中可能不安全（接受程式碼作為引數）
→ 旗標白名單需要 per-command 定義
```

## 4. Deny 規則的激進策略

```typescript
// Allow 路徑：只剝除非白名單的 env vars
const sanitized = stripNonWhitelistedEnvVars(command, SAFE_ENV_VARS)

// Deny 路徑：剝除所有 env vars（更激進）
const sanitized = stripAllEnvVars(command)
```

**原因**：`FOO=bar denied_cmd` 可以繞過基於命令名稱的 deny 檢查。Deny 時全部剝除，再檢查剝除後的命令。

## 5. 唯讀模式三層實作

| 層 | 檔案 | 行數 | 覆蓋 |
|---|------|------|------|
| Bash | `readOnlyValidation.ts` | 1990 | Unix shell 命令 |
| Shell 共用庫 | `readOnlyCommandValidation.ts` | 1893 | 跨 shell 通用邏輯 |
| PowerShell | `readOnlyValidation.ts` | 1823 | Windows PS 命令 |

每份都獨立維護一套白名單，因為不同 shell 的命令語義差異太大。

## 6. Sandbox 設計

| 平台 | 技術 | 特點 |
|------|------|------|
| Linux | bubblewrap (bwrap) | namespace 隔離、唯讀 bind mount |
| macOS | sandbox-exec | seatbelt profile，Apple 原生 |

**兩套路徑語義差異**（已知問題 #30067）：
- Permission rule：用 glob pattern（`~/project/**`）
- Sandbox config：用 literal path（`/home/user/project`）

**裸 repo 逃脫防護**：偵測 `.git` 是檔案（非目錄）時，追蹤 `gitdir:` 指向的實際 repo 路徑。

## 7. Permission Hook 系統

```typescript
// 5 個並發決策源，ResolveOnce 保護
const decision = await ResolveOnce.race([
  classifierDecision,      // AI 分類器
  hookDecision,            // 使用者 hook
  ruleDecision,            // 預設規則
  channelDecision,         // 手機批准
  interactiveDecision,     // 終端 UI
])
```

第一個回應的決策源贏，其餘取消。

## 8. 安全 Prompt 指令

`cyberRiskInstruction.ts` 的設計：
- 對開發者：「DO NOT MODIFY THIS FILE」
- 對 Claude（程式碼層）：「DO NOT modify, move, or edit this file when working in the codebase」
- 作為模型指令：「Assist with authorized security testing, defensive security, CTF challenges. Refuse requests for destructive techniques, DoS, mass targeting.」

## 參考

詳見 `references/validator-rules.md` 和 `references/threat-model.md`。
