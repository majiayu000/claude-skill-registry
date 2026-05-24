---
name: pubmed-systematic-search
description: Comprehensive systematic search using MeSH and synonyms. Triggers: 系統性搜尋, 完整搜尋, 文獻回顧, systematic search, comprehensive, MeSH expansion, 同義詞
---

# 系統性文獻搜尋

## 描述
使用 MeSH 詞彙擴展和同義詞來執行完整的系統性搜尋，適合文獻回顧或需要全面涵蓋的研究。

## 觸發條件
- 「系統性搜尋」、「完整搜尋」、「文獻回顧」
- 「找所有關於...的論文」
- 「comprehensive search」、「systematic review」
- 提到 MeSH、同義詞、專業搜尋策略

---

## 工作流程

```
┌─────────────────────────────────────────────────────────────┐
│  Step 1: generate_search_queries(topic)                     │
│  → 取得 MeSH 詞彙 + 同義詞 + 建議查詢                        │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│  Step 2: search_literature() × N (並行執行多個策略)          │
│  → 標題搜尋、標題/摘要、MeSH、同義詞搜尋                     │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│  Step 3: merge_search_results()                             │
│  → 合併 + 去重 + 標記高相關性文章                            │
└─────────────────────────────────────────────────────────────┘
```

---

## Step 1: 產生搜尋素材

```python
generate_search_queries(topic="remimazolam ICU sedation")
```

### 回傳內容：

```json
{
  "corrected_topic": "remimazolam icu sedation",  // 拼字校正後
  "mesh_terms": [
    {
      "input": "remimazolam",
      "preferred": "remimazolam [Supplementary Concept]",
      "synonyms": ["CNS 7056", "ONO 2745"]
    },
    {
      "input": "sedation",
      "preferred": "Deep Sedation",
      "synonyms": ["Sedation, Deep", "Conscious Sedation"]
    }
  ],
  "all_synonyms": ["CNS 7056", "ONO 2745", "Sedation, Deep", ...],
  "suggested_queries": [
    {"id": "q1_title", "query": "(remimazolam icu sedation)[Title]"},
    {"id": "q2_tiab", "query": "(remimazolam icu sedation)[Title/Abstract]"},
    {"id": "q4_mesh", "query": "\"remimazolam [Supplementary Concept]\"[MeSH]"},
    {"id": "q6_syn", "query": "(CNS 7056 OR ONO 2745)[Title/Abstract]"}
  ]
}
```

---

## Step 2: 並行執行搜尋

根據 `suggested_queries` 執行多個搜尋策略（並行！）：

```python
# 並行執行這些搜尋
search_literature(query="(remimazolam icu sedation)[Title]")
search_literature(query="(remimazolam icu sedation)[Title/Abstract]")
search_literature(query='"remimazolam [Supplementary Concept]"[MeSH]')
search_literature(query="(CNS 7056 OR ONO 2745)[tiab]")
```

---

## Step 3: 合併結果

```python
merge_search_results(
    results_json='[["12345","67890"],["67890","11111"],["11111","22222"]]'
)
```

### 回傳內容：

```json
{
  "unique_pmids": ["12345", "67890", "11111", "22222"],
  "high_relevance_pmids": ["67890", "11111"],  // ⭐ 多個策略都找到的！
  "statistics": {
    "total_before_dedup": 6,
    "total_after_dedup": 4,
    "duplicates_removed": 2
  }
}
```

**重點**: `high_relevance_pmids` 是最重要的論文，因為多種搜尋策略都找到它們！

---

## MeSH 擴展的價值

### 為什麼需要 MeSH？

| 使用者輸入 | PubMed 可能漏掉 | MeSH 會找到 |
|-----------|-----------------|------------|
| heart attack | Myocardial Infarction | ✅ 標準化詞彙 |
| sugar disease | Diabetes Mellitus | ✅ 標準化詞彙 |
| blood pressure drug | Antihypertensive Agents | ✅ 標準化詞彙 |

### Query Analysis 的價值

`generate_search_queries` 會顯示 PubMed 實際如何解讀你的查詢：

```json
{
  "query": "(remimazolam AND sedation)",
  "estimated_count": 561,
  "pubmed_translation": "(\"remimazolam\"[Supplementary Concept] OR \"remimazolam\"[All Fields]) AND (\"sedate\"[All Fields] OR ...)"
}
```

你以為搜 2 個詞，PubMed 實際上擴展到 Supplementary Concept + synonyms！

---

## 搜尋策略選項

```python
# 全面搜尋（預設）
generate_search_queries(topic="...", strategy="comprehensive")

# 精準搜尋（加入 RCT 篩選）
generate_search_queries(topic="...", strategy="focused")

# 探索性搜尋（更多同義詞）
generate_search_queries(topic="...", strategy="exploratory")
```

---

## 進階臨床篩選 (Phase 2.1 新功能)

系統性搜尋可結合進階篩選：

```python
# 步驟 1: 產生搜尋素材
materials = generate_search_queries(topic="diabetes treatment elderly")

# 步驟 2: 執行搜尋，加入進階篩選
results = []
for sq in materials["suggested_queries"]:
    r = search_literature(
        query=sq["query"],
        limit=50,
        age_group="aged",           # 只找老年人
        species="humans",           # 只找人類
        clinical_query="therapy",   # 治療研究
        language="english"          # 英文
    )
    results.append(r["pmids"])

# 步驟 3: 合併
merged = merge_search_results(results_json=json.dumps(results))
```

### 可用的進階篩選

| 篩選類型 | 參數 | 可用值 |
|---------|------|--------|
| 年齡群 | `age_group` | newborn, infant, child, adolescent, adult, aged, aged_80 |
| 性別 | `sex` | male, female |
| 物種 | `species` | humans, animals |
| 語言 | `language` | english, chinese, japanese, etc. |
| 臨床查詢 | `clinical_query` | therapy, diagnosis, prognosis, etiology |

---

## 完整範例

```python
# Step 1: 取得搜尋材料
materials = generate_search_queries(topic="machine learning diagnosis radiology")

# Step 2: 並行搜尋（使用 suggested_queries）
results = []
for sq in materials["suggested_queries"]:
    r = search_literature(query=sq["query"], limit=50)
    results.append(r["pmids"])

# Step 3: 合併
merged = merge_search_results(results_json=json.dumps(results))

# Step 4: 取得高相關性論文的詳情
fetch_article_details(pmids=",".join(merged["high_relevance_pmids"]))
```

---

## 結果不足時？

使用 `expand_search_queries` 來擴展搜尋：

```python
expand_search_queries(
    topic="remimazolam ICU sedation",
    existing_query_ids="q1_title,q2_tiab",
    expansion_type="mesh"  # 或 "broader" 或 "narrower"
)
```

- `mesh`: 使用更多 MeSH 同義詞
- `broader`: 放寬條件（OR 代替 AND）
- `narrower`: 加入篩選（RCT、近五年）
