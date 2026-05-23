---
name: literature-search
description: |
  Search and retrieve academic literature from multiple databases.
  LOAD THIS SKILL WHEN: User says "搜尋文獻", "search literature", "find papers", "PubMed", "學術搜尋" | needs to find research articles | starting literature review.
  CAPABILITIES: PubMed search, MeSH term expansion, citation metrics, batch retrieval.
---

# 文獻搜尋技能 (Literature Search)

## 描述

使用多種 MCP Tools 搜尋學術文獻，支援關鍵字搜尋、MeSH 詞彙擴展、引用指標排序。

## 觸發條件

- 「搜尋文獻」「找論文」「PubMed 搜尋」
- "search papers", "find articles", "literature search"
- 開始文獻回顧或系統性評讀

## 可用 Tools

### MCP Tools (pubmed-search)

| Tool | 用途 | 參數 |
|------|------|------|
| `search_literature` | 基本搜尋 | query, limit, min_year, article_type |
| `generate_search_queries` | MeSH 詞彙擴展 | topic |
| `merge_search_results` | 合併多次搜尋結果 | results_json |
| `get_citation_metrics` | 取得引用指標 (RCR) | pmids, sort_by |
| `fetch_article_details` | 取得文章詳細資訊 | pmids |

### MCP Tools (zotero-keeper)

| Tool | 用途 | 參數 |
|------|------|------|
| `check_articles_owned` | 檢查是否已收藏 | pmids |
| `batch_import_from_pubmed` | 批次匯入到 Zotero | pmids, collection_name |

## 執行流程

### 1. 快速搜尋模式

```
用戶提供關鍵字
    ↓
search_literature(query, limit=20)
    ↓
返回 PMID 清單 + 摘要
```

### 2. 精確搜尋模式 (推薦用於系統性回顧)

```
用戶提供主題
    ↓
generate_search_queries(topic)  ← 取得 MeSH 詞彙
    ↓
選擇最佳搜尋策略
    ↓
search_literature(query=MeSH_query)
    ↓
get_citation_metrics(pmids, sort_by="relative_citation_ratio")
    ↓
返回按 RCR 排序的結果
```

### 3. 多策略合併模式

```python
# 並行執行多個搜尋策略
results = []
results.append(search_literature(query="keyword1"))
results.append(search_literature(query="keyword2"))
results.append(search_literature(query="MeSH[Mesh]"))

# 合併並去重
merged = merge_search_results(results)
# high_relevance_pmids = 出現在多個搜尋結果中的文章
```

## 輸出格式

```markdown
## 搜尋結果摘要

- **搜尋策略**: [描述使用的策略]
- **總筆數**: N 篇
- **高相關性**: M 篇 (出現在多個搜尋中)

### 文獻清單

| # | PMID | 標題 | 年份 | RCR | 
|---|------|------|------|-----|
| 1 | 12345678 | Title... | 2024 | 2.5 |
| 2 | ... | ... | ... | ... |
```

## 使用範例

**範例 1：快速搜尋**
```
用戶：「搜尋 remimazolam 在 ICU 的應用」
執行：search_literature(query="remimazolam ICU", limit=15)
```

**範例 2：精確搜尋**
```
用戶：「我要做 AI 麻醉的系統性回顧」
執行：
1. generate_search_queries("artificial intelligence anesthesiology")
2. search_literature(query='"Artificial Intelligence"[MeSH] AND "Anesthesiology"[MeSH]')
3. get_citation_metrics(pmids="last", sort_by="relative_citation_ratio")
```

## 相關技能

- `literature-filter` - 過濾與確認文獻
- `literature-retrieval` - 組合技能：搜尋 + 過濾
