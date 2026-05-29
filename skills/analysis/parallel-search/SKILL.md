---
name: parallel-search
description: 使用多組關鍵字並行搜尋，提高文獻覆蓋率。觸發：並行搜尋、parallel search、批量搜尋、擴展搜尋、多組搜尋、同時搜、找更多、廣泛搜尋、comprehensive search。
---

# 並行文獻搜尋技能

## 概述

利用 Agent 的並行呼叫能力來加速文獻搜尋，提高覆蓋率。

**核心概念**：
1. 預設搜尋策略（日期、排除詞、文章類型）
2. 策略工具返回多組搜尋語法（自動整合策略設定）
3. Agent 並行呼叫搜尋工具
4. 合併工具整合結果

---

## 可用工具

### 🔍 pubmed-search MCP 搜尋工具

| 工具 | 用途 | 關鍵參數 |
|------|------|----------|
| `generate_search_queries` | 從主題生成 MeSH + 同義詞材料 | `topic`, `strategy`, `check_spelling` |
| `search_literature` | 執行 PubMed 搜尋（可並行多次）| `query`, `limit`, `min_year`, `article_type` |
| `merge_search_results` | 合併多組搜尋結果並去重 | `results_json` |
| `expand_search_queries` | 結果不足時擴展搜尋 | `topic`, `expansion_type` |
| `parse_pico` | 解析 PICO 臨床問題 | `description` 或 `p`, `i`, `c`, `o` |

### 📊 結果處理工具

| 工具 | 用途 | 關鍵參數 |
|------|------|----------|
| `fetch_article_details` | 取得完整文章資訊 | `pmids` (逗號分隔) |
| `get_citation_metrics` | 取得 iCite 引用指標 (RCR) | `pmids`, `sort_by`, `min_rcr` |
| `find_related_articles` | 找相似文章 | `pmid` |
| `find_citing_articles` | 找引用此文章的研究 | `pmid` |

### 💾 Session 管理工具

| 工具 | 用途 | 說明 |
|------|------|------|
| `get_session_pmids` | 取得 session 中的 PMID | `search_index=-1` 取最近搜尋 |
| `get_session_summary` | 查看 session 狀態 | 確認快取和搜尋歷史 |
| `list_search_history` | 列出搜尋歷史 | 回溯過往搜尋 |

### 📚 儲存文獻工具（⚠️ 注意優先級）

| 工具 | 資料來源 | 使用時機 |
|------|----------|----------|
| `save_reference_mcp` | pubmed-search HTTP API | **永遠優先使用** ✅ |
| `save_reference` | Agent 傳遞 | 僅當 API 不可用時 fallback ⚠️ |

## 工作流程

### Step 0: （可選）設定搜尋策略

```
呼叫：configure_search_strategy(criteria_json={
    "date_range": "2019-2024",
    "exclusions": ["animal", "review"],
    "article_types": ["Clinical Trial", "Randomized Controlled Trial"]
})
```

### Step 1: 生成搜尋策略

```
呼叫：generate_search_queries(
    topic="remimazolam ICU sedation",
    strategy="comprehensive",
    use_saved_strategy=True
)
```

返回 5 組 queries，策略已自動整合。

### Step 2: Agent 並行執行搜尋

Agent 看到 instruction 後，會並行呼叫：

```xml
<parallel_tool_calls>
  <tool_call id="1">
    <name>search_literature</name>
    <args>{"query": "...", "limit": 20}</args>
  </tool_call>
  <tool_call id="2">
    <name>search_literature</name>
    <args>{"query": "...", "limit": 20}</args>
  </tool_call>
  <!-- ... 更多並行呼叫 ... -->
</parallel_tool_calls>
```

### Step 3: 合併結果

```
呼叫：merge_search_results(results_json='[
  {"query_id": "q1_title", "pmids": ["123", "456"]},
  {"query_id": "q2_tiab", "pmids": ["456", "012"]}
]')
```

返回去重後的結果，標記高相關性文獻（出現在多個搜尋中）。

## 迭代式搜尋擴展

當初始搜尋結果不夠時：

```
Phase 1: 初始搜尋
  → generate_search_queries(topic="...")
  → 並行執行 5 組查詢
  → merge_search_results → 只找到 15 篇，不夠！

Phase 2: 擴展搜尋
  → expand_search_queries(
      topic="...",
      existing_query_ids="q1,q2,q3,q4,q5",
      expansion_type="synonyms"
    )
  → 並行執行新查詢
  → merge_search_results → 共 32 篇

Phase 3: 如果還不夠
  → expand_search_queries(..., expansion_type="related")
  → 繼續...
```

### 擴展類型選擇指南

| 情況 | expansion_type | 預期效果 |
|------|----------------|----------|
| 擔心遺漏不同術語 | `synonyms` | sedation → conscious sedation |
| 想找類似比較研究 | `related` | remimazolam → propofol |
| 結果太少 | `broader` | 使用 OR、移除限制 |
| 結果太多 | `narrower` | 限定 RCT、最近 2 年 |

## 流程圖

```
generate_search_queries(topic)
        │ 5 組查詢
        ▼
並行執行 search_literature
        │
        ▼
merge_search_results
        │
        ▼
┌───────┴───────┐
│ 結果足夠嗎？  │
└───────┬───────┘
        │ No
        ▼
expand_search_queries(type=...)
        │ 新查詢
        ▼
並行執行新查詢
        │
        ▼
merge（含所有結果）
        │
        └──→ 重複直到足夠
```

## 優點

1. **更快**：多個搜尋同時執行
2. **更全面**：不同角度的關鍵字組合
3. **可追蹤**：知道每篇文獻來自哪個搜尋
4. **可重現**：策略被記錄下來
5. **策略整合**：日期/排除詞自動套用

---

## 搜尋後儲存文獻

完成搜尋和篩選後，儲存選中的文獻：

```
# ✅ PRIMARY：使用 MCP-to-MCP 驗證（永遠優先）
呼叫：save_reference_mcp(
    pmid="12345678",
    agent_notes="Key paper on parallel search methodology"
)

# ⚠️ FALLBACK：僅當 pubmed-search API 不可用時
呼叫：save_reference(article={完整 metadata dict})
```

**為什麼 `save_reference_mcp` 優先？**
- `save_reference_mcp`：mdpaper 直接從 pubmed-search API 取得驗證資料，Agent 無法篡改
- `save_reference`：Agent 傳遞 metadata，可能被修改或幻覺

---

## Session 工具使用技巧

搜尋結果自動暫存在 session 中，不需要記住所有 PMID：

```
# 取得最近搜尋的 PMID
呼叫：get_session_pmids(search_index=-1)

# 取得前一次搜尋的 PMID
呼叫：get_session_pmids(search_index=-2)

# 在其他工具中使用 "last" 快捷方式
呼叫：get_citation_metrics(pmids="last", sort_by="relative_citation_ratio")
呼叫：prepare_export(pmids="last", format="ris")
```

---

## 相關技能

- `literature-review` - 完整的文獻回顧流程
- `concept-development` - 搜尋後發展概念
