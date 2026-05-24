---
name: cc-harness-patterns
description: "Harness Engineering 設計模式 — 基於 Claude Code 原始碼逆向分析的 12 條可遷移原則。Use when: 設計 agent 系統架構、實作 tool orchestration、設計 context 管理策略、建構 agent loop。"
version: 202603
context: fork
---

# Harness Engineering 設計模式

`Harness = Tools + Knowledge + Observation + Action Interfaces + Permissions`

基於 Claude Code v2.1.88（92,500 行 TypeScript）逆向分析。

## 1. Agent Loop：Async Generator 模式

Claude Code 的 agent loop 用 async generator 實作：

```typescript
async function* queryModel(...): AsyncGenerator<StreamEvent | AssistantMessage> {
  // yield 每個 stream event，呼叫端按需消費
}
```

**核心循環**：`queryModel()` → 檢查 `stop_reason` → `tool_use` 時呼叫 `runTools()` → 結果回注 messages → 再次 `queryModel()`

**stop_reason 分支**：`end_turn`（結束）、`tool_use`（執行工具）、`max_tokens`（context 滿了，觸發 compaction）

## 2. Tool Orchestration：讀寫分離

```typescript
function isConcurrencySafe(input): boolean {
  // 工具自己聲明是否可並行
}
```

- `partitionToolCalls()` 把一批工具呼叫分成可並行組和必須串行組
- **讀工具自動合批並行**（FileRead、Grep、Glob）
- **寫工具強制串行**（FileEdit、FileWrite、Bash）
- 決策權在工具端（Single Responsibility），不在 orchestrator

## 3. 工具執行 7 層管道

```
Schema Validation → Custom validateInput() → Input Sanitization
→ PreToolUse Hooks → Permission Resolution → Execution → PostToolUse Hooks
```

每層只問一個問題：「能否拒絕？」拒絕即停，不往下走。執行邏輯永遠在最後一層。

## 4. Cache 穩定性模式

**Sticky Latch**：影響 cache key 的欄位一旦啟用就不在 session 內關閉。
```typescript
if (!fastModeHeaderLatched && isFastMode) {
  fastModeHeaderLatched = true  // 永遠 latched
}
```

**確定性 ID**：注入 context 的 ID 從穩定輸入衍���，不隨機生成。

**靜態/動態邊界**：`SYSTEM_PROMPT_DYNAMIC_BOUNDARY` 把 prompt 分成可全域快取的靜態段和 session 特定的動態段，防 2^N 快取桶爆炸。

**Attachment > Inline**：動態 agent 列表從 tool description 移到 attachment message，避免 MCP 連接/plugin 載入導致 tool schema cache bust。省 fleet 10.2% cache creation tokens。

## 5. Context Engineering

**原則**：什麼進 context、什麼順序、何時壓縮。

- **訊息處理管道** `normalizeMessagesForAPI`：10 步處理（過濾空訊息、合併連續同角色、注入 system-reminder、truncate 過長結果...）
- **Compaction 三模式**：BASE（全壓）、PARTIAL_FROM（從某點壓）、PARTIAL_UP_TO（壓到某點）
- **`<analysis>` 草稿**：讓模型在 scratchpad 思考，結果不進 context
- **Deferred Tool Loading**：36 個工具不全塞 prompt，ToolSearch 按需載入 schema

## 6. Multi-session Continuity

- **Forked Agent**：子 agent 繼承父 session 的 prompt cache（Memory extraction、AgentSummary、Dream 都用此模式）
- **progress log**：跨 context window 的進度檔（claude-progress.txt）
- **AutoDream**：背景記憶整合，三層閘門（時間≥24h + session≥5 + 檔案鎖），四階段 consolidation prompt

## 7. Observability

- **三層追��**：Analytics（業務事件）/ OpenTelemetry（效能）/ DiagnosticTracking（per-turn 計數器）
- **PII 安全型別**：`PiiSafeString<T>` 型別系統，編譯期防止 PII 進入遙測
- **Frustration Signal**：追蹤使用者 swearing、重複 "continue" prompt，路由至 Datadog

## 參考

詳見 `references/design-principles.md`。
