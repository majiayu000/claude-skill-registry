---
name: pubmed-mcp-tools-reference
description: Complete reference for all 35+ PubMed Search MCP tools. Triggers: 工具列表, all tools, 完整功能, tool reference, 有哪些工具
---

# PubMed Search MCP 工具完整參考

## 描述
所有 35+ 個 MCP 工具的完整參考，包含參數說明和使用範例。

---

## 工具分類總覽

| 類別 | 工具數 | 主要用途 |
|------|--------|----------|
| 🔍 PubMed 搜尋 | 6 | 核心文獻搜尋 |
| 🏥 PICO 臨床搜尋 | 2 | 臨床問題分析 |
| 🔬 論文探索 | 3 | 引用網絡探索 |
| 🧬 NCBI Extended | 7 | 基因/化合物/變異 |
| 🌍 Europe PMC | 4 | 歐洲文獻+全文 |
| 📚 CORE | 5 | 開放取用全文 |
| 🤖 Semantic Scholar | 2 | AI 分析+引用 |
| 📊 OpenAlex | 4 | 學術知識圖譜 |
| 📤 匯出工具 | 3 | 引用格式匯出 |

---

## 🔍 PubMed 搜尋工具

### `search_literature`
基本 PubMed 搜尋

```python
search_literature(
    query="remimazolam sedation",     # 搜尋詞
    limit=20,                          # 結果數量（預設 5）
    min_year=2020,                     # 最早年份
    max_year=2024,                     # 最晚年份
    date_from="2024/01/01",           # 精確起始日（YYYY/MM/DD）
    date_to="2024/06/30",             # 精確結束日
    date_type="edat",                  # edat/pdat/mdat
    article_type="Review",             # Clinical Trial, Review, Meta-Analysis
    strategy="relevance"               # relevance, recent, most_cited, impact
)
```

### `generate_search_queries`
產生 MeSH 擴展搜尋策略

```python
generate_search_queries(
    topic="remimazolam ICU sedation",  # 主題
    strategy="comprehensive",           # comprehensive/focused/exploratory
    check_spelling=True,               # 拼字檢查
    include_suggestions=True           # 包含建議查詢
)
```

### `merge_search_results`
合併多個搜尋結果並去重

```python
merge_search_results(
    results_json='[["12345","67890"],["67890","11111"]]'
)
# 或帶 query_id：
# '[{"query_id":"q1","pmids":["12345"]},{"query_id":"q2","pmids":["67890"]}]'
```

### `expand_search_queries`
結果不足時擴展搜尋

```python
expand_search_queries(
    topic="remimazolam",
    existing_query_ids="q1_title,q2_tiab",  # 已執行的查詢
    expansion_type="mesh"                    # mesh/broader/narrower
)
```

### `fetch_article_details`
取得論文詳細資訊

```python
fetch_article_details(pmids="30217674,28523456")
```

---

## 🏥 PICO 臨床搜尋工具

### `parse_pico`
解析臨床問題為 PICO 元素

```python
# 自然語言解析
parse_pico(description="remimazolam 在 ICU 比 propofol 好嗎？")

# 或直接提供結構化 PICO
parse_pico(
    description="",
    p="ICU patients",
    i="remimazolam",
    c="propofol",
    o="delirium"
)
```

---

## 🔬 論文探索工具

### `find_related_articles`
找相似文章（PubMed Similar Articles）

```python
find_related_articles(pmid="30217674", limit=10)
```

### `find_citing_articles`
找引用這篇的論文

```python
find_citing_articles(pmid="30217674", limit=20)
```

---

## 🧬 NCBI Extended 工具

### `search_ncbi_gene`
搜尋 NCBI Gene 資料庫

```python
search_ncbi_gene(query="BRCA1 breast cancer", limit=10)
```

### `get_ncbi_gene_info`
取得基因詳細資訊

```python
get_ncbi_gene_info(gene_id="672")  # BRCA1
```

### `search_pubchem_compound`
搜尋 PubChem 化合物

```python
search_pubchem_compound(query="remimazolam", limit=10)
```

### `get_pubchem_compound_info`
取得化合物詳細資訊

```python
get_pubchem_compound_info(cid="11526795")
```

### `search_clinvar`
搜尋 ClinVar 變異資料庫

```python
search_clinvar(query="BRCA1 pathogenic", limit=20)
```

### `get_clinvar_variation`
取得變異詳細資訊

```python
get_clinvar_variation(variation_id="17661")
```

### `get_ncbi_cross_references`
取得跨資料庫連結

```python
get_ncbi_cross_references(
    source_db="gene",
    target_db="pubmed",
    ids="672"
)
```

---

## 🌍 Europe PMC 工具

### `search_europe_pmc`
搜尋 Europe PMC

```python
search_europe_pmc(
    query="remimazolam",
    limit=30,
    has_fulltext=True,   # 只找有全文的
    source="preprint"    # 或 "medline", "pmc"
)
```

### `get_europe_pmc_fulltext`
取得 Europe PMC 全文

```python
get_europe_pmc_fulltext(pmcid="PMC6939411")
```

### `get_europe_pmc_citations`
取得引用資料

```python
get_europe_pmc_citations(pmid="30217674")
```

### `get_europe_pmc_references`
取得參考文獻

```python
get_europe_pmc_references(pmid="30217674")
```

---

## 📚 CORE 工具

### `search_core`
搜尋 CORE 開放取用庫

```python
search_core(query="machine learning radiology", limit=30)
```

### `search_core_fulltext`
搜尋全文內容

```python
search_core_fulltext(query="adverse events remimazolam", limit=20)
```

### `get_core_paper`
取得論文詳情

```python
get_core_paper(core_id="12345678")
```

### `get_core_fulltext`
取得全文內容

```python
get_core_fulltext(core_id="12345678")
```

### `find_in_core`
用標題找論文

```python
find_in_core(title="Remimazolam versus midazolam for procedural sedation")
```

---

## 🤖 Semantic Scholar 工具

### `search_semantic_scholar`
搜尋 Semantic Scholar

```python
search_semantic_scholar(
    query="deep learning medical imaging",
    limit=30,
    year="2020-2024",          # 年份範圍
    fields_of_study="Medicine"  # 領域篩選
)
```

### `get_semantic_scholar_paper`
取得論文詳情（含影響力指標）

```python
get_semantic_scholar_paper(paper_id="649def34f8be52c8b66281af98ae884c09aef38b")
```

回傳包含：
- `citationCount`: 總引用數
- `influentialCitationCount`: 有影響力的引用數
- `tldr`: AI 生成摘要

---

## 📊 OpenAlex 工具

### `search_openalex`
搜尋 OpenAlex

```python
search_openalex(
    query="CRISPR gene editing",
    limit=30,
    from_date="2020-01-01",
    filter="is_oa:true"  # OpenAlex filter syntax
)
```

### `get_openalex_work`
取得作品詳情

```python
get_openalex_work(work_id="W2741809807")
```

### `search_openalex_authors`
搜尋作者

```python
search_openalex_authors(query="Jennifer Doudna")
```

### `get_openalex_author`
取得作者詳情

```python
get_openalex_author(author_id="A5023888391")
```

---

## 📤 匯出工具

### `prepare_export`
匯出引用格式

```python
prepare_export(
    pmids="30217674,28523456",  # 或 "last" 使用上次搜尋
    format="ris",               # ris/bibtex/csv/medline/json
    include_abstract=True
)
```

### `get_article_fulltext_links`
取得全文連結

```python
get_article_fulltext_links(pmid="30217674")
```

### `analyze_fulltext_access`
批次分析全文可用性

```python
analyze_fulltext_access(pmids="30217674,28523456")
# 或 "last" 使用上次搜尋結果
```

---

## 常用工作流程

### 快速搜尋
```
search_literature → fetch_article_details → prepare_export
```

### 系統性搜尋
```
generate_search_queries → search_literature × N → merge_search_results
```

### PICO 搜尋
```
parse_pico → generate_search_queries × 4 → search_literature → merge_search_results
```

### 論文探索
```
fetch_article_details → find_related_articles + find_citing_articles
```

### 全文取得
```
analyze_fulltext_access → get_europe_pmc_fulltext 或 get_core_fulltext
```

---

## 參數快速參考

### 常用篩選參數

| 參數 | 說明 | 範例值 |
|------|------|--------|
| `limit` | 結果數量 | 10, 20, 50, 100 |
| `min_year` | 最早年份 | 2020 |
| `max_year` | 最晚年份 | 2024 |
| `article_type` | 文章類型 | "Review", "Clinical Trial", "Meta-Analysis" |
| `strategy` | 排序策略 | "relevance", "recent", "most_cited" |

### 進階篩選參數 (Phase 2.1 新功能)

| 參數 | 說明 | 可用值 |
|------|------|--------|
| `age_group` | 年齡群 | newborn, infant, preschool, child, adolescent, young_adult, adult, middle_aged, aged, aged_80 |
| `sex` | 性別 | male, female |
| `species` | 物種 | humans, animals |
| `language` | 語言 | english, chinese, japanese, german, french, spanish, korean, italian, portuguese, russian |
| `clinical_query` | 臨床查詢 | therapy, diagnosis, prognosis, etiology, clinical_prediction |

### PubMed 欄位標籤

| 標籤 | 說明 |
|------|------|
| `[Title]` | 標題 |
| `[Title/Abstract]` | 標題或摘要 |
| `[tiab]` | 同上（縮寫） |
| `[MeSH]` | MeSH 詞彙 |
| `[Author]` | 作者 |
| `[Journal]` | 期刊 |
| `[PMID]` | PubMed ID |

### Clinical Query Filters

| Filter | 用途 |
|--------|------|
| `therapy[filter]` | 治療效果研究 |
| `diagnosis[filter]` | 診斷研究 |
| `prognosis[filter]` | 預後研究 |
| `etiology[filter]` | 病因研究 |
