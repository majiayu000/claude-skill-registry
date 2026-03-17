---
name: literature-retrieval
description: |
  Complete literature retrieval capability combining search and filter skills.
  LOAD THIS SKILL WHEN: User needs "文獻檢索", "找文獻", "retrieve literature", "系統性搜尋" | starting systematic review | comprehensive literature search.
  CAPABILITIES: Multi-database search, MeSH expansion, quality filtering, PRISMA-compliant workflow.
  COMPOSITE SKILL: Combines literature-search + literature-filter.
---

# 文獻檢索能力 (Literature Retrieval)

## 描述

**組合能力**：整合文獻搜尋和文獻過濾，提供完整的文獻檢索流程。

```
┌─────────────────────────────────────────────────────────┐
│             Literature Retrieval (組合能力)              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────────┐    ┌─────────────────────┐    │
│  │  literature-search  │ →  │  literature-filter  │    │
│  │  (搜尋技能)          │    │  (過濾技能)          │    │
│  └─────────────────────┘    └─────────────────────┘    │
│           │                          │                  │
│           ▼                          ▼                  │
│      搜尋結果 (N篇)            篩選後清單 (M篇)         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 觸發條件

- 「文獻檢索」「系統性搜尋」「找相關文獻」
- "literature retrieval", "systematic search", "find all relevant papers"
- 需要完整的搜尋和篩選流程

## 組成技能

| 順序 | 技能 | 路徑 | 迴圈 |
|------|------|------|------|
| 1 | `literature-search` | `.claude/skills/literature-search/SKILL.md` | 可能多次（多策略） |
| 2 | `literature-filter` | `.claude/skills/literature-filter/SKILL.md` | 單次 |

## 執行流程

### 標準流程

```
Step 1: 定義搜尋策略
    ↓
    用戶提供主題/PICO
    ↓
Step 2: 執行搜尋 (literature-search)
    ↓
    ├── 策略 1: 關鍵字搜尋
    ├── 策略 2: MeSH 詞彙搜尋
    └── 策略 3: 相關文獻搜尋 (optional)
    ↓
Step 3: 合併結果
    ↓
    merge_search_results() → 去重、標記高相關
    ↓
Step 4: 過濾篩選 (literature-filter)
    ↓
    ├── 自動過濾（引用指標、可用性）
    └── Agent 判斷（相關性、品質）
    ↓
Step 5: 輸出最終清單
    ↓
    PRISMA 流程圖 + 篩選後文獻清單
```

### 迴圈處理

```python
# 當結果不足時，自動擴展搜尋
while len(results) < min_required:
    # 擴展搜尋策略
    expanded_queries = expand_search_queries(original_query)
    new_results = search_literature(expanded_queries)
    results = merge_search_results([results, new_results])
    
    # 檢查是否達到上限
    if iteration >= max_iterations:
        break
```

## 輸出格式

```markdown
## 文獻檢索報告

### 搜尋策略

| 策略 | 查詢語句 | 結果數 |
|------|----------|--------|
| 關鍵字 | remimazolam AND ICU | 45 |
| MeSH | "Intensive Care Units"[Mesh] AND remimazolam | 32 |
| 擴展 | CNS7056 OR remimazolam | 12 |
| **合併去重** | — | **67** |

### PRISMA 流程

```
Identification: 89 篇 (含重複)
        ↓ 去重 (-22)
Screening: 67 篇
        ↓ 標題/摘要篩選 (-25)
Eligibility: 42 篇
        ↓ 全文篩選 (-12)
Included: 30 篇
```

### 最終納入文獻

| # | PMID | 標題 | 年份 | RCR | 全文 |
|---|------|------|------|-----|------|
| 1 | 38353755 | Remimazolam for... | 2024 | 3.2 | PMC ✓ |
| 2 | ... | ... | ... | ... | ... |

### 排除文獻摘要

- 病例報告: 8 篇
- 動物研究: 4 篇
- 不相關: 12 篇
- 全文不可用: 6 篇
```

## Checkpoint 機制

長任務使用 checkpoint 追蹤進度：

```json
{
  "capability": "literature-retrieval",
  "status": "in-progress",
  "progress": {
    "total_strategies": 3,
    "completed_strategies": 2
  },
  "currentStep": "filter",
  "data": {
    "search_results": ["pmid1", "pmid2", ...],
    "filtered_results": ["pmid1", ...]
  }
}
```

## 使用範例

**範例 1：快速檢索**

```
用戶：「幫我找 remimazolam 在 ICU 的文獻」
執行：
1. literature-search: 關鍵字搜尋
2. literature-filter: 自動過濾低品質
輸出：篩選後清單
```

**範例 2：系統性檢索**

```
用戶：「我要做系統性回顧，主題是 AI 麻醉」
執行：
1. 定義 PICO
2. literature-search: 多策略搜尋 (MeSH + 關鍵字)
3. merge_search_results: 合併去重
4. literature-filter: 套用納入/排除標準
5. 產出 PRISMA 流程圖
輸出：完整檢索報告
```

## 相關能力

- `report-writing` - 讀寫報告能力
- `literature-review` (cp.write_report) - 文獻評讀能力 = 本能力 + report-writing
