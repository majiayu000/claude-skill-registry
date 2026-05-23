---
name: pubmed-quick-search
description: Quick literature search on PubMed. Triggers: 搜尋, 找論文, search papers, find articles, PubMed, 文獻搜尋, 快速搜尋
---

# PubMed 快速搜尋

## 描述
在 PubMed 上快速搜尋特定主題的文獻，適合快速瀏覽或初步探索。

## 觸發條件
- 「幫我找...的論文」、「搜尋...」
- 「有沒有關於...的文章」
- 「search papers about...」、「find articles on...」

---

## 基本用法

### 簡單搜尋
```python
search_literature(query="remimazolam ICU sedation", limit=10)
```

### 使用 PubMed 官方語法

#### MeSH 標準詞彙
```python
search_literature(query='"Diabetes Mellitus"[MeSH]')
```

#### 欄位限定搜尋
```python
# 標題搜尋
search_literature(query='COVID-19[Title]')

# 標題 + 摘要
search_literature(query='machine learning[Title/Abstract]')

# 作者搜尋
search_literature(query='Smith J[Author]')
```

#### 日期範圍
```python
search_literature(query='propofol sedation AND 2023:2024[dp]')
```

#### 文章類型
```python
search_literature(query='diabetes treatment AND Review[pt]')
search_literature(query='COVID-19 vaccine AND Clinical Trial[pt]')
```

---

## PubMed 欄位標籤速查

| 標籤 | 說明 | 範例 |
|------|------|------|
| `[Title]` 或 `[ti]` | 標題 | `COVID-19[ti]` |
| `[Title/Abstract]` 或 `[tiab]` | 標題+摘要 | `sedation[tiab]` |
| `[MeSH]` 或 `[mh]` | MeSH 標準詞彙 | `"Diabetes Mellitus"[MeSH]` |
| `[Author]` 或 `[au]` | 作者 | `Smith J[au]` |
| `[Journal]` 或 `[ta]` | 期刊縮寫 | `Nature[ta]` |
| `[Publication Type]` 或 `[pt]` | 文章類型 | `Review[pt]` |
| `[Date - Publication]` 或 `[dp]` | 出版日期 | `2024[dp]` |

---

## 進階篩選

### 篩選策略
```python
# 最新文獻
search_literature(query="...", strategy="recent")

# 高引用論文
search_literature(query="...", strategy="most_cited")

# 高影響力期刊
search_literature(query="...", strategy="impact")
```

### 年份篩選
```python
search_literature(query="...", min_year=2020, max_year=2024)
```

### 精確日期範圍
```python
search_literature(
    query="COVID-19",
    date_from="2024/01/01",
    date_to="2024/06/30"
)
```

### 進階臨床篩選 (Phase 2.1 新功能)

#### 年齡群篩選
```python
# 只找老年人研究
search_literature(query="diabetes treatment", age_group="aged")

# 只找兒童研究
search_literature(query="asthma", age_group="child")

# 可用選項：
# newborn (0-1月), infant (1-23月), preschool (2-5歲)
# child (6-12歲), adolescent (13-18歲), young_adult (19-24歲)
# adult (19+), middle_aged (45-64歲), aged (65+), aged_80 (80+)
```

#### 性別篩選
```python
# 只找女性研究
search_literature(query="breast cancer", sex="female")

# 只找男性研究
search_literature(query="prostate cancer", sex="male")
```

#### 物種篩選
```python
# 只找人類研究
search_literature(query="gene therapy", species="humans")

# 只找動物研究
search_literature(query="CRISPR", species="animals")
```

#### 語言篩選
```python
# 只找英文論文
search_literature(query="COVID-19", language="english")

# 只找中文論文
search_literature(query="針灸", language="chinese")
```

#### 臨床證據篩選 (Clinical Queries)
```python
# 治療效果研究 (RCT 優先)
search_literature(query="remimazolam", clinical_query="therapy")

# 診斷研究
search_literature(query="lung cancer", clinical_query="diagnosis")

# 預後研究
search_literature(query="heart failure", clinical_query="prognosis")

# 病因學研究
search_literature(query="diabetes", clinical_query="etiology")
```

#### 組合篩選
```python
# 找老年女性的糖尿病治療 RCT
search_literature(
    query="diabetes treatment",
    age_group="aged",
    sex="female",
    species="humans",
    clinical_query="therapy",
    min_year=2020
)
```

---

## 輸出格式

搜尋結果會自動包含：
- PMID
- 標題
- 作者
- 期刊
- 出版日期
- 摘要（如有）
- DOI（如有）
- PMC ID（如有，表示有全文）

---

## 後續動作建議

搜尋完成後，可以：
1. **深入探索**: `find_related_articles(pmid="...")` - 找相似文章
2. **取得全文**: `get_fulltext(pmcid="PMC...")` - 讀取全文
3. **匯出引用**: `prepare_export(pmids="last", format="ris")` - 匯出到 EndNote/Zotero
4. **分析開放取用**: `analyze_fulltext_access(pmids="last")` - 看哪些有免費全文

---

## 常見問題

### Q: 搜尋結果太少？
嘗試使用 `generate_search_queries()` 來擴展同義詞和 MeSH 詞彙。

### Q: 搜尋結果太多？
加入更多限定條件：年份、文章類型、MeSH 主要主題 `[majr]`。

### Q: 想找開放取用的論文？
使用 `search_europe_pmc(query="...", open_access_only=True, has_fulltext=True)`
