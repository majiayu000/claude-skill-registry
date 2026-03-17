---
name: pubmed-fulltext-access
description: Full text access via Europe PMC, CORE, and other open access sources. Triggers: 全文, fulltext, PDF, open access, 免費下載, PMC, 開放取用
---

# 全文取得指南

## 描述
透過 Europe PMC、CORE 等開放取用來源取得論文全文，包含 PDF 連結和全文內容。

## 觸發條件
- 「我要看全文」
- 「有 PDF 嗎？」
- 「開放取用」、「免費下載」
- 「這篇有全文嗎？」
- 提到 PMC、open access

---

## 全文來源比較

| 來源 | 收錄量 | 特色 | 全文格式 |
|------|--------|------|----------|
| **PubMed Central** | 8M+ | 美國官方 OA 庫 | HTML, PDF |
| **Europe PMC** | 33M+ | 歐洲版，含預印本 | HTML, PDF, XML |
| **CORE** | 200M+ | 最大 OA 聚合器 | PDF, TXT |
| **Semantic Scholar** | 200M+ | AI 摘要、引用 | 連結為主 |

---

## 檢查全文可用性

### 單篇論文

```python
get_article_fulltext_links(pmid="30217674")
```

### 回傳：

```json
{
  "pmid": "30217674",
  "title": "Remimazolam versus midazolam...",
  "access_type": "open_access",
  "links": {
    "pubmed": "https://pubmed.ncbi.nlm.nih.gov/30217674/",
    "pmc": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6939411/",
    "pmc_pdf": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6939411/pdf/",
    "doi": "https://doi.org/10.1097/ALN.0000000000002435"
  },
  "full_text_available": true
}
```

### 批次分析

```python
analyze_fulltext_access(pmids="30217674,28523456,35678901")
# 或使用上次搜尋結果
analyze_fulltext_access(pmids="last")
```

### 回傳：

```json
{
  "total": 50,
  "statistics": {
    "open_access": 23,
    "subscription_required": 20,
    "abstract_only": 7
  },
  "open_access_pmids": ["30217674", "35678901", "..."],
  "subscription_required_pmids": ["28523456", "..."],
  "abstract_only_pmids": ["..."]
}
```

---

## Europe PMC 全文

### 搜尋（含預印本）

```python
search_europe_pmc(
    query="remimazolam sedation",
    limit=20,
    has_fulltext=True  # 只找有全文的
)
```

### 取得全文內容

```python
get_europe_pmc_fulltext(pmcid="PMC6939411")
```

### 回傳：

```json
{
  "pmcid": "PMC6939411",
  "title": "Remimazolam versus midazolam...",
  "sections": {
    "abstract": "Background: ...",
    "introduction": "Procedural sedation...",
    "methods": "This was a multicenter...",
    "results": "A total of 461 patients...",
    "discussion": "This study demonstrates...",
    "conclusions": "Remimazolam provided..."
  },
  "figures": [
    {"id": "fig1", "caption": "Study flow diagram"},
    {"id": "fig2", "caption": "Primary endpoint results"}
  ],
  "tables": [
    {"id": "table1", "caption": "Baseline characteristics"}
  ],
  "references_count": 45
}
```

---

## CORE 全文

### 搜尋開放取用

```python
search_core(query="machine learning radiology", limit=30)
```

### 用標題找論文

```python
find_in_core(title="Remimazolam versus midazolam for procedural sedation")
```

### 回傳：

```json
{
  "found": true,
  "core_id": "12345678",
  "title": "Remimazolam versus midazolam...",
  "download_url": "https://core.ac.uk/download/pdf/12345678.pdf",
  "fulltext_available": true
}
```

### 取得全文

```python
get_core_fulltext(core_id="12345678")
```

### 回傳：

```json
{
  "core_id": "12345678",
  "title": "...",
  "fulltext": "Full text content here...",
  "fulltext_length": 45678,
  "language": "en"
}
```

---

## 全文搜尋

### CORE 全文搜尋

```python
search_core_fulltext(
    query="remimazolam hemodynamic stability",
    limit=20
)
```

這會搜尋論文的**全文內容**，不只是標題和摘要！

### 回傳：

```json
{
  "results": [
    {
      "core_id": "12345678",
      "title": "...",
      "snippet": "...remimazolam showed better hemodynamic stability compared to...",
      "relevance_score": 0.89
    }
  ]
}
```

---

## 全文取得策略

### 策略 1：快速查詢 PMC

```python
# 最簡單，如果有 PMC 版本
links = get_article_fulltext_links(pmid="30217674")
if links["links"]["pmc"]:
    fulltext = get_europe_pmc_fulltext(pmcid=links["links"]["pmc_id"])
```

### 策略 2：多來源搜尋

```python
# 先查 Europe PMC
epmc = search_europe_pmc(query="remimazolam", has_fulltext=True)

# 再查 CORE
core = search_core(query="remimazolam")

# 合併結果
```

### 策略 3：標題匹配

```python
# 有標題但不確定來源
result = find_in_core(title="Remimazolam versus midazolam for procedural sedation")
if result["found"]:
    fulltext = get_core_fulltext(core_id=result["core_id"])
```

---

## 完整工作流程

### 情境：搜尋並取得全文

```python
# Step 1: PubMed 搜尋
results = search_literature(query="remimazolam RCT", limit=30)
pmids = [a["pmid"] for a in results["articles"]]

# Step 2: 分析全文可用性
access = analyze_fulltext_access(pmids=",".join(pmids))

# Step 3: 優先處理 Open Access
for pmid in access["open_access_pmids"]:
    links = get_article_fulltext_links(pmid=pmid)
    if links["links"]["pmc"]:
        fulltext = get_europe_pmc_fulltext(pmcid=links["links"]["pmc_id"])
        # 處理全文...

# Step 4: 嘗試 CORE 找其他
for pmid in access["subscription_required_pmids"]:
    details = fetch_article_details(pmids=pmid)
    title = details["articles"][0]["title"]
    core_result = find_in_core(title=title)
    if core_result["found"]:
        fulltext = get_core_fulltext(core_id=core_result["core_id"])
```

---

## 處理全文內容

### 提取特定段落

```python
fulltext = get_europe_pmc_fulltext(pmcid="PMC6939411")

# 只看方法
print(fulltext["sections"]["methods"])

# 只看結果
print(fulltext["sections"]["results"])
```

### 搜尋全文中的關鍵詞

```python
# CORE 支援全文搜尋
results = search_core_fulltext(query="adverse events remimazolam")
# 回傳包含 snippet 顯示匹配位置
```

---

## 全文來源對照表

| PMID | PMC | Europe PMC | CORE | Semantic Scholar |
|------|-----|------------|------|------------------|
| 30217674 | PMC6939411 | ✅ | ✅ | ✅ |
| 28523456 | ❌ | ✅ (preprint) | ✅ | ✅ |
| 35678901 | ❌ | ❌ | ❌ | ⚠️ (link only) |

### 取得策略：

1. **有 PMC** → `get_europe_pmc_fulltext(pmcid="...")`
2. **無 PMC** → `find_in_core(title="...")` → `get_core_fulltext(...)`
3. **都沒有** → 只能用摘要或聯繫圖書館

---

## 預印本處理

### Europe PMC 含預印本

```python
search_europe_pmc(
    query="COVID-19 vaccine",
    source="preprint",  # 只搜預印本
    limit=30
)
```

### 預印本來源：
- bioRxiv
- medRxiv
- arXiv (部分)

---

## 小技巧

### 1. 判斷是否有全文

```python
# 快速檢查
links = get_article_fulltext_links(pmid="30217674")
has_fulltext = links["full_text_available"]
```

### 2. 批次處理

```python
# 搜尋後直接分析
results = search_literature(query="...", limit=50)
access = analyze_fulltext_access(pmids="last")  # 使用上次搜尋結果
```

### 3. DOI 優先

```python
# 有些新論文可能 PMC 還沒收錄
# 但 DOI 可以連到出版社頁面（可能需訂閱）
links = get_article_fulltext_links(pmid="35678901")
print(links["links"]["doi"])  # https://doi.org/10.xxxx/xxxxx
```

### 4. 引用格式

如果取得全文，記得正確引用：

```python
# 匯出引用格式
prepare_export(pmids="30217674", format="ris")
```
