---
name: pubmed-multi-source-search
description: Cross-database search using multiple academic sources. Triggers: 跨資料庫, multi-source, Semantic Scholar, OpenAlex, CORE, Europe PMC, 綜合搜尋
---

# 多來源綜合搜尋

## 描述
整合 PubMed、Europe PMC、CORE、Semantic Scholar、OpenAlex 等多個學術資料庫，進行全面的跨來源搜尋。

## 觸發條件
- 「搜尋所有來源」
- 「跨資料庫搜尋」
- 「找更多來源」
- 提到 Semantic Scholar、OpenAlex、CORE
- 需要開放取用論文

---

## 資料庫特色比較

| 資料庫 | 收錄量 | 特色 | 最適合 |
|--------|--------|------|--------|
| **PubMed** | 35M+ | 生物醫學權威 | 臨床/基礎醫學 |
| **Europe PMC** | 33M+ | 含預印本、全文 | 歐洲研究、預印本 |
| **CORE** | 200M+ | 最大 OA 庫 | 開放取用全文 |
| **Semantic Scholar** | 200M+ | AI 分析、引用圖譜 | 跨領域、影響力分析 |
| **OpenAlex** | 250M+ | 開放學術圖譜 | 大規模分析、趨勢研究 |

---

## 各資料庫工具

### PubMed（核心）

```python
search_literature(query="remimazolam sedation", limit=30)
generate_search_queries(topic="remimazolam")  # MeSH 擴展
```

### Europe PMC

```python
# 搜尋（含預印本）
search_europe_pmc(query="remimazolam", limit=30)

# 取得全文
get_europe_pmc_fulltext(pmcid="PMC6939411")

# 引用資料
get_europe_pmc_citations(pmid="30217674")
```

### CORE

```python
# 搜尋
search_core(query="machine learning radiology", limit=30)

# 全文搜尋
search_core_fulltext(query="adverse events", limit=20)

# 取得全文
get_core_fulltext(core_id="12345678")

# 用標題找
find_in_core(title="Remimazolam versus midazolam...")
```

### Semantic Scholar

```python
# 搜尋
search_semantic_scholar(query="deep learning medical imaging", limit=30)

# 論文詳情（含引用分析）
get_semantic_scholar_paper(paper_id="...")
```

### OpenAlex

```python
# 搜尋
search_openalex(query="CRISPR gene editing", limit=30)

# 作品詳情
get_openalex_work(work_id="W2741809807")

# 作者資訊
search_openalex_authors(query="Jennifer Doudna")
```

---

## 跨來源搜尋策略

### 策略 1：互補搜尋

不同資料庫強項不同，互相補充：

```python
# PubMed：生物醫學文獻（權威性）
pm_results = search_literature(query="COVID-19 vaccine efficacy", limit=50)

# Europe PMC：預印本（最新研究）
epmc_results = search_europe_pmc(query="COVID-19 vaccine efficacy", source="preprint", limit=30)

# Semantic Scholar：跨領域（含 CS、工程）
ss_results = search_semantic_scholar(query="COVID-19 vaccine efficacy", limit=30)

# CORE：開放取用全文
core_results = search_core(query="COVID-19 vaccine efficacy", limit=30)
```

### 策略 2：全文優先

需要全文時的搜尋順序：

```python
# Step 1: PubMed 搜尋建立基礎列表
results = search_literature(query="...", limit=50)

# Step 2: 分析全文可用性
access = analyze_fulltext_access(pmids="last")

# Step 3: Europe PMC 補充全文
for pmid in access["subscription_required_pmids"]:
    epmc = search_europe_pmc(query=f"EXT_ID:{pmid}")
    
# Step 4: CORE 最後嘗試
for pmid in still_missing:
    details = fetch_article_details(pmids=pmid)
    core = find_in_core(title=details["articles"][0]["title"])
```

### 策略 3：影響力分析

結合 Semantic Scholar 的引用分析：

```python
# PubMed 搜尋
pm = search_literature(query="...", limit=30)

# 取得 Semantic Scholar 的影響力指標
for article in pm["articles"]:
    ss = search_semantic_scholar(query=article["title"], limit=1)
    if ss["papers"]:
        details = get_semantic_scholar_paper(paper_id=ss["papers"][0]["paperId"])
        print(f"Citations: {details['citationCount']}")
        print(f"Influential Citations: {details['influentialCitationCount']}")
```

---

## 完整跨來源工作流程

### 情境：全面搜尋某主題

```python
# Step 1: PubMed 核心搜尋
pm_results = search_literature(
    query="machine learning drug discovery",
    limit=50
)

# Step 2: 並行搜尋其他來源
epmc_results = search_europe_pmc(query="machine learning drug discovery", limit=30)
core_results = search_core(query="machine learning drug discovery", limit=30)
ss_results = search_semantic_scholar(query="machine learning drug discovery", limit=30)
oa_results = search_openalex(query="machine learning drug discovery", limit=30)

# Step 3: 整合結果
all_titles = set()
unique_papers = []

for source, results in [
    ("PubMed", pm_results),
    ("Europe PMC", epmc_results),
    ("CORE", core_results),
    ("Semantic Scholar", ss_results),
    ("OpenAlex", oa_results)
]:
    for paper in results["articles"]:
        title_key = paper["title"].lower()[:50]  # 標題前50字作為key
        if title_key not in all_titles:
            all_titles.add(title_key)
            paper["source"] = source
            unique_papers.append(paper)

print(f"Total unique papers: {len(unique_papers)}")
```

---

## 各來源的獨特功能

### Europe PMC 獨有

```python
# 預印本搜尋
search_europe_pmc(query="...", source="preprint")

# 註解/評論
search_europe_pmc(query="...", has_annotations=True)

# 資料補充材料
get_europe_pmc_supplementary(pmcid="PMC...")
```

### CORE 獨有

```python
# 全文內容搜尋
search_core_fulltext(query="specific methodology term")

# 大規模開放取用
search_core(query="...", open_access=True)
```

### Semantic Scholar 獨有

```python
# 影響力引用（不只是數量，而是「有影響力的」引用）
paper = get_semantic_scholar_paper(paper_id="...")
print(paper["influentialCitationCount"])

# AI 生成摘要
print(paper["tldr"])  # Too Long; Didn't Read

# 引用意圖分析
for citation in paper["citations"]:
    print(citation["intent"])  # methodology, background, result
```

### OpenAlex 獨有

```python
# 作者分析
author = search_openalex_authors(query="Jennifer Doudna")[0]
print(f"h-index: {author['hIndex']}")
print(f"Works count: {author['worksCount']}")

# 機構分析
works = search_openalex(query="...", institution="Harvard")

# 開放取用狀態詳情
work = get_openalex_work(work_id="...")
print(work["open_access"]["oa_status"])  # gold, green, hybrid, closed
```

---

## 結果整合技巧

### 去重方法

```python
def deduplicate_papers(all_results):
    """基於標題相似度去重"""
    seen_titles = {}
    unique = []
    
    for paper in all_results:
        # 正規化標題
        title_key = paper["title"].lower()
        title_key = re.sub(r'[^\w\s]', '', title_key)[:100]
        
        if title_key not in seen_titles:
            seen_titles[title_key] = paper
            unique.append(paper)
        else:
            # 合併來源資訊
            seen_titles[title_key]["sources"].append(paper["source"])
    
    return unique
```

### 排序優先級

```python
def score_paper(paper):
    """計算論文優先分數"""
    score = 0
    
    # 多來源找到 = 更重要
    score += len(paper.get("sources", [])) * 10
    
    # 有全文 = 更有用
    if paper.get("fulltext_available"):
        score += 20
    
    # 高引用 = 更有影響力
    score += min(paper.get("citation_count", 0) / 10, 50)
    
    # 最近發表 = 更新穎
    if paper.get("year", 0) >= 2023:
        score += 15
    
    return score

# 排序
papers.sort(key=score_paper, reverse=True)
```

---

## 使用場景建議

| 需求 | 推薦來源組合 |
|------|-------------|
| 臨床研究 | PubMed + Europe PMC |
| 跨領域研究 | Semantic Scholar + OpenAlex |
| 開放取用優先 | CORE + Europe PMC |
| 最新研究 | Europe PMC (preprint) |
| 影響力分析 | Semantic Scholar + OpenAlex |
| 全面覆蓋 | 全部五個來源 |

---

## 小技巧

### 1. 並行搜尋

```python
# 同時搜尋多個來源（並行呼叫）
# 大幅減少等待時間
```

### 2. 先 PubMed 後擴展

```python
# PubMed 結果最權威
# 其他來源用於補充和取得全文
```

### 3. 標題匹配找全文

```python
# PubMed 找到但無全文 → 用標題在 CORE 搜尋
find_in_core(title="exact paper title")
```

### 4. 引用分析用 Semantic Scholar

```python
# 它的 influentialCitationCount 比單純計數更有意義
```
