---
name: cc-cost-engineering
description: "AI Agent 成本工程 — 基於 Claude Code 的成本追蹤、prompt cache 最佳化、token 預算控制逆向分析。Use when: 優化 token 消耗、設計成本控制機制、分析 cache 效率、選擇模型配置。"
version: 202603
context: fork
---

# AI Agent 成本工程

基於 Claude Code v2.1.88 的成本控制機制逆向分析。

## 模型成本矩陣

| 模型 | Input/MTok | Output/MTok | 相對成本 |
|------|-----------|-------------|----------|
| Haiku 3.5 | $0.80 | $4.00 | 1x |
| Sonnet 4.6 | $3.00 | $15.00 | 3.75x |
| Opus 4.6 | $15.00 | $75.00 | 18.75x |
| Opus 4.6 Fast | $30.00 | $150.00 | **37.5x** |

**Cached tokens 便宜 75-90%。** 這是 Claude Code 整個架構圍繞 cache 設計的原因。

## Cost Envelope 模式

```typescript
// Claude Code 的 cost-tracker.ts 核心邏輯
function addToTotalSessionCost(inputTokens, outputTokens, model, speed) {
  const costPerInputToken = MODEL_COSTS[model]?.input ?? UNKNOWN_FALLBACK
  const cost = inputTokens * costPerInputToken + outputTokens * costPerOutputToken
  sessionCost += cost
  // 支援 advisor 模型遞迴計費、Fast Mode OTEL 標記
}
```

**實作要點**：
1. 每個任務設預算上限，累計追蹤，超限就停
2. 未知模型用 fallback 費率 + analytics 警告
3. Session 成本持久化到 project config（以 sessionId 隔離）

## Prompt Cache 12 種 Break 原因

| # | 原因 | 影響 | 防禦 |
|---|------|------|------|
| 1 | System prompt 內容變化 | 全 bust | 靜態/動態邊界 |
| 2 | Tool schema 變化 | 全 bust | 不排序工具陣列 |
| 3 | MCP 工具動態載入 | 部分 bust | Deferred loading |
| 4 | Agent list 變化 | 全 bust | 移到 attachment |
| 5 | `currentDate` 跨日 | 全 bust | **已知缺陷，應移到 dynamic zone** |
| 6 | Compaction 改寫訊息 | 全 bust | 不可避免，但可用 fork 繼承 |
| 7 | Feature flag 切換 | 全 bust | Sticky Latch |
| 8 | Beta header 變化 | Server-side bust | Latch 機制 |
| 9 | 版本更新 | 全 bust | 不可避免 |
| 10 | Permission mode 變化 | Tool schema bust | 避免 mid-session 切換 |
| 11 | Plugin/MCP 重載 | Tool bust | 避免 `/reload-plugins` |
| 12 | 使用者切換 cwd | env_info bust | 固定工作目錄 |

## 使用者端避坑清單

| 坑 | 成本影響 | 避法 |
|----|----------|------|
| Auto Mode + Max 訂閱 | 每次工具操作用 Opus 分類，佔 15-28% | 關 Auto Mode 或改手動 |
| Agent SDK 的 file modification injection | 每輪吃 5-15% context | 用 CLI；或壓短 session |
| 跨午夜長 session | 整段 cache 全滅 | 午夜前結束 |
| 頻繁開關 session | 每次 `max_tokens:1` 探測 | 用長 session + `/compact` |
| 裝太多 MCP server | 每輪注入不快取指令 | 只裝需要的 |
| 工作中切目錄 | env_info bust cache | 固定目錄，用絕對路徑 |
| 大量改檔後繼續對話 | file modification diff 每輪注入 | 改完 `/compact` 或開新 session |
| Resume 舊 session | stale check 必觸發 | 不 resume，開新的 |

## Token Estimation 三策略

```
1. API countTokens（精確，需 API call）
2. Haiku fallback（近似，便宜）
3. length / 4（粗估，免費）
JSON 用 bytes / 2；圖片/PDF 固定 2000 tokens
```

## Compaction 成本陷阱

- 壓縮後第一輪以 **125% 費率**重建 cache（input token 全是 cache_creation）
- 可觸發最多 **3 次連鎖** compaction
- Compaction 用的 forked agent 帶全部 36 工具（**已知缺陷，應帶 0 個**）
- `NO_TOOLS_PREAMBLE` 解決 Sonnet 4.6 壓縮時 2.79% 誤呼叫工具

## 參考

詳見 `references/cache-break-causes.md` 和 `references/cost-matrix.md`。
