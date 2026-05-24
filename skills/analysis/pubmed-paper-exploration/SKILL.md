---
name: pubmed-paper-exploration
description: Deep exploration from a key paper. Triggers: 這篇論文的相關研究, 誰引用這篇, 類似文章, related articles, citation tree, paper exploration
---

# 論文深度探索

## 描述
從一篇關鍵論文出發，探索引用網絡和相關研究，適合深入了解某個領域或追蹤研究發展脈絡。

## 觸發條件
- 「這篇文章的相關研究」
- 「有誰引用這篇？」
- 「類似的文章」
- 「這個領域的發展脈絡」
- 提供 PMID 或論文標題

---

## 探索方向

```
                    ┌──────────────────┐
                    │   Key Paper      │
                    │   PMID: 12345    │
                    └────────┬─────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
          ▼                  ▼                  ▼
    ┌───────────┐     ┌───────────┐     ┌───────────┐
    │ References │     │  Related  │     │  Citing   │
    │   (過去)   │     │  (相似)   │     │  (未來)   │
    └───────────┘     └───────────┘     └───────────┘
```

| 工具 | 用途 | 時間軸 |
|------|------|--------|
| `fetch_article_details` | 取得參考文獻列表 | ← 過去（這篇引用誰） |
| `find_related_articles` | PubMed 演算法找相似文章 | ↔ 相似（主題接近） |
| `find_citing_articles` | 找引用這篇的論文 | → 未來（誰引用這篇） |

---

## 探索工具

### 1. 取得論文詳情與參考文獻

```python
fetch_article_details(pmids="30217674")
```

### 回傳：

```json
{
  "articles": [{
    "pmid": "30217674",
    "title": "Remimazolam versus midazolam...",
    "abstract": "...",
    "authors": ["Doi M", "Hirata N", "..."],
    "journal": "Anesthesiology",
    "pub_date": "2020 Jan",
    "mesh_terms": ["Benzodiazepines", "Conscious Sedation", "..."],
    "references": ["12345678", "87654321", "..."]  // ← 這篇引用的論文
  }]
}
```

---

### 2. 找相關文章（PubMed Similar Articles）

```python
find_related_articles(pmid="30217674", limit=10)
```

這使用 PubMed 的 **Related Articles** 演算法，基於：
- MeSH 詞彙相似度
- 標題/摘要的詞彙重疊
- 引用模式

### 回傳：

```json
{
  "source_pmid": "30217674",
  "related_articles": [
    {
      "pmid": "33105432",
      "title": "Efficacy of remimazolam versus...",
      "journal": "Br J Anaesth",
      "relevance_score": 0.95
    },
    // ...
  ]
}
```

---

### 3. 找引用文章（Citation Tracking）

```python
find_citing_articles(pmid="30217674", limit=20)
```

### 回傳：

```json
{
  "source_pmid": "30217674",
  "citing_articles": [
    {
      "pmid": "35678901",
      "title": "Real-world experience with remimazolam...",
      "pub_date": "2023",
      "is_review": false
    },
    // ...
  ],
  "total_citations": 156
}
```

**重要**: 引用追蹤可找到：
- 後續驗證研究
- 系統性回顧
- 臨床指引更新

---

## 建立引用樹（Citation Tree）

從一篇種子論文開始，逐層探索引用網絡：

### 第一層：直接相關

```python
# 並行呼叫
find_related_articles(pmid="30217674", limit=5)    # 相似文章
find_citing_articles(pmid="30217674", limit=10)    # 引用文章
```

### 第二層：擴展到重要引用

```python
# 對第一層的重要論文再次探索
for important_pmid in ["35678901", "34567890"]:
    find_citing_articles(pmid=important_pmid, limit=5)
```

---

## 跨來源探索

### Europe PMC（歐洲版 PubMed，更多全文）

```python
search_europe_pmc(query="remimazolam", limit=20)
get_europe_pmc_citations(pmid="30217674")  # 引用資料
```

### CORE（開放取用全文庫）

```python
find_in_core(title="Remimazolam versus midazolam for procedural sedation")
# → 找到後可取得全文
get_core_fulltext(core_id="12345678")
```

### Semantic Scholar（學術知識圖譜）

```python
search_semantic_scholar(query="remimazolam sedation", limit=10)
get_semantic_scholar_paper(paper_id="...")  # 包含影響力指標
```

---

## 完整探索範例

### 情境：研究 remimazolam 的臨床應用發展

```python
# Step 1: 找到種子論文（關鍵臨床試驗）
results = search_literature(
    query="remimazolam randomized controlled trial",
    article_type="Clinical Trial",
    limit=5
)
seed_pmid = results["articles"][0]["pmid"]  # 假設是 30217674

# Step 2: 取得完整資訊
details = fetch_article_details(pmids=seed_pmid)

# Step 3: 三方向探索（並行）
related = find_related_articles(pmid=seed_pmid, limit=10)
citing = find_citing_articles(pmid=seed_pmid, limit=20)

# Step 4: 識別重要論文
# - 在 related 和 citing 都出現的 → 核心文獻
# - citing 中標記為 review 的 → 綜述文章
# - citing 中最近發表的 → 最新進展

# Step 5: 深入重要論文
important_pmids = ["35678901", "34567890", "33456789"]
for pmid in important_pmids:
    fetch_article_details(pmids=pmid)
```

---

## 研究脈絡重建

### 縱向時間軸

```
2015 ──┬── Phase 1 trial (safety)
       │
2017 ──┼── Phase 2 trial (dosing)
       │
2019 ──┼── Phase 3 RCT (efficacy) ← 種子論文
       │
2020 ──┼── Systematic review
       │
2021 ──┼── Real-world studies
       │
2022 ──┼── Guideline recommendations
       │
2023 ──┴── Current best evidence
```

### 如何建立：

```python
# 1. 從種子論文取得參考文獻（向過去追溯）
details = fetch_article_details(pmids="30217674")
past_papers = details["articles"][0]["references"]

# 2. 從種子論文找引用（向未來追蹤）
citing = find_citing_articles(pmid="30217674", limit=50)
future_papers = [a["pmid"] for a in citing["citing_articles"]]

# 3. 合併並按時間排序
all_pmids = past_papers + ["30217674"] + future_papers
all_details = fetch_article_details(pmids=",".join(all_pmids))
# 按 pub_date 排序即可得到時間軸
```

---

## 小技巧

### 1. 找到領域的 Landmark Paper

```python
# 搜尋高引用的綜述文章
search_literature(
    query="remimazolam review",
    article_type="Review",
    strategy="most_cited"
)
```

### 2. 追蹤最新進展

```python
# 最近引用種子論文的研究
citing = find_citing_articles(pmid="30217674", limit=50)
recent = [a for a in citing["citing_articles"] if a["pub_date"] >= "2023"]
```

### 3. 找爭議或相反結論

在 related articles 中找標題含 "versus", "comparison", "no difference" 的論文
