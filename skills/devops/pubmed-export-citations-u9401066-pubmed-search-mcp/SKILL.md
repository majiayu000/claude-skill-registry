---
name: pubmed-export-citations
description: 'Export citations to reference managers. Triggers: 匯出, export, RIS, BibTeX,
  EndNote, Zotero, Mendeley, 引用格式, reference manager'
---

---
name: pubmed-export-citations
description: Export citations to reference managers. Triggers: 匯出, export, RIS, BibTeX, EndNote, Zotero, Mendeley, 引用格式, reference manager
---

# 引用匯出指南

## 描述
將搜尋結果匯出為各種引用格式，支援 EndNote、Zotero、Mendeley 等常見文獻管理軟體。

## 觸發條件
- 「匯出這些文獻」
- 「轉成 RIS/BibTeX 格式」
- 「我要匯入 EndNote/Zotero/Mendeley」
- 「下載引用格式」

---

## 支援格式

| 格式 | 副檔名 | 支援軟體 | 推薦用途 |
|------|--------|----------|----------|
| **RIS** | .ris | EndNote, Zotero, Mendeley | 📌 通用首選 |
| **BibTeX** | .bib | LaTeX, JabRef, Overleaf | 📌 學術寫作 |
| **CSV** | .csv | Excel, 數據分析 | 資料整理 |
| **MEDLINE** | .txt | PubMed 原生格式 | 備份保存 |
| **JSON** | .json | 程式處理 | 自動化流程 |

---

## 基本用法

### 匯出指定 PMID

```python
prepare_export(pmids="30217674,28523456,35678901", format="ris")
```

### 匯出上次搜尋結果

```python
# 先搜尋
search_literature(query="remimazolam", limit=30)

# 再匯出（使用 "last"）
prepare_export(pmids="last", format="ris")
```

---

## 格式範例

### RIS 格式（EndNote/Zotero/Mendeley）

```
TY  - JOUR
AU  - Doi, Mitsuharu
AU  - Hirata, Nobuhiro
TI  - Remimazolam versus midazolam for procedural sedation
JO  - Anesthesiology
PY  - 2020
VL  - 132
IS  - 1
SP  - 63
EP  - 74
DO  - 10.1097/ALN.0000000000002435
PM  - 30217674
AB  - Background: Remimazolam is a novel...
ER  -
```

### BibTeX 格式（LaTeX）

```bibtex
@article{Doi2020,
  author = {Doi, Mitsuharu and Hirata, Nobuhiro and ...},
  title = {Remimazolam versus midazolam for procedural sedation},
  journal = {Anesthesiology},
  year = {2020},
  volume = {132},
  number = {1},
  pages = {63--74},
  doi = {10.1097/ALN.0000000000002435},
  pmid = {30217674}
}
```

### CSV 格式

```csv
PMID,Title,Authors,Journal,Year,DOI
30217674,"Remimazolam versus midazolam...","Doi M, Hirata N, ...","Anesthesiology",2020,"10.1097/..."
28523456,"Phase 2 study of...","Author A, Author B, ...","J Clin Pharm",2019,"10.1002/..."
```

### MEDLINE 格式

```
PMID- 30217674
OWN - NLM
STAT- MEDLINE
DCOM- 20200115
LR  - 20200115
IS  - 1528-1175 (Electronic)
VI  - 132
IP  - 1
DP  - 2020 Jan
TI  - Remimazolam versus midazolam for procedural sedation.
PG  - 63-74
AB  - Background: Remimazolam is a novel...
AU  - Doi M
AU  - Hirata N
...
```

---

## 匯出選項

### 包含/排除摘要

```python
# 包含摘要（預設）
prepare_export(pmids="30217674", format="ris", include_abstract=True)

# 不包含摘要（檔案較小）
prepare_export(pmids="30217674", format="ris", include_abstract=False)
```

---

## 各軟體匯入指南

### EndNote

1. 匯出 RIS 格式
2. EndNote → File → Import → File
3. 選擇 .ris 檔案
4. Import Option: "RefMan RIS"

### Zotero

1. 匯出 RIS 格式
2. Zotero → File → Import
3. 選擇 .ris 檔案
4. 自動識別格式

### Mendeley

1. 匯出 RIS 格式
2. Mendeley → File → Import → RIS
3. 選擇 .ris 檔案

### LaTeX (Overleaf)

1. 匯出 BibTeX 格式
2. 上傳 .bib 檔案到專案
3. 使用 `\cite{Doi2020}`

### JabRef

1. 匯出 BibTeX 格式
2. JabRef → File → Open
3. 選擇 .bib 檔案

---

## 完整工作流程

### 情境：系統性文獻回顧的引用管理

```python
# Step 1: 執行系統性搜尋
materials = generate_search_queries(topic="remimazolam ICU sedation")

# Step 2: 多策略搜尋
r1 = search_literature(query="remimazolam ICU sedation[Title]", limit=100)
r2 = search_literature(query="remimazolam sedation[MeSH]", limit=100)

# Step 3: 合併去重
merged = merge_search_results(results_json='[...]')

# Step 4: 取得詳細資訊
details = fetch_article_details(pmids=",".join(merged["unique_pmids"]))

# Step 5: 匯出到 EndNote
export_ris = prepare_export(pmids=",".join(merged["unique_pmids"]), format="ris")

# Step 6: 同時匯出 Excel（方便篩選）
export_csv = prepare_export(pmids=",".join(merged["unique_pmids"]), format="csv")
```

---

## 大量匯出

### 超過 20 篇論文

```python
# 大量匯出會返回檔案路徑而非內容
result = prepare_export(pmids="pm1,pm2,...,pm100", format="ris")
# result = {"file_path": "/tmp/pubmed_export_20240115.ris", "count": 100}
```

### 批次處理建議

```python
# 分批匯出（每批 50 篇）
all_pmids = [...]  # 500 篇
batch_size = 50

for i in range(0, len(all_pmids), batch_size):
    batch = all_pmids[i:i+batch_size]
    prepare_export(pmids=",".join(batch), format="ris")
```

---

## 特殊用途

### 資料分析

```python
# 匯出 CSV 到 Excel
prepare_export(pmids="last", format="csv")

# 或 JSON 給程式處理
prepare_export(pmids="last", format="json")
```

### 備份原始資料

```python
# MEDLINE 格式保留最完整資訊
prepare_export(pmids="last", format="medline")
```

### 自動化流程

```python
# JSON 格式方便程式解析
data = prepare_export(pmids="30217674,28523456", format="json")
# 可以直接 json.loads(data) 使用
```

---

## 引用格式對照

### 同一篇論文在不同格式

| 欄位 | RIS | BibTeX | CSV |
|------|-----|--------|-----|
| 作者 | AU | author | Authors |
| 標題 | TI | title | Title |
| 期刊 | JO | journal | Journal |
| 年份 | PY | year | Year |
| DOI | DO | doi | DOI |
| PMID | PM | pmid | PMID |

---

## 小技巧

### 1. 快速匯出上次搜尋

```python
# 搜尋後直接用 "last"
search_literature(query="...", limit=50)
prepare_export(pmids="last", format="ris")
```

### 2. 選擇正確格式

```
EndNote/Zotero/Mendeley → RIS
LaTeX/Overleaf → BibTeX
Excel 分析 → CSV
程式處理 → JSON
備份保存 → MEDLINE
```

### 3. 驗證匯出

匯入前建議先：
1. 確認筆數正確
2. 抽查幾篇的 DOI/PMID
3. 檢查作者、標題是否完整

### 4. 去重後再匯出

```python
# 合併多次搜尋後再匯出
merged = merge_search_results(results_json='[...]')
prepare_export(pmids=",".join(merged["unique_pmids"]), format="ris")
```

---

## 常見問題

### Q: 匯入後缺少摘要？

A: 確認使用 `include_abstract=True`（預設）

### Q: 特殊字符亂碼？

A: RIS/BibTeX 使用 UTF-8 編碼，確認軟體支援

### Q: BibTeX citation key 重複？

A: 預設使用 `AuthorYear` 格式，如 `Doi2020`，同年同作者會加後綴 `Doi2020a`, `Doi2020b`

### Q: 要引用幾百篇？

A: 建議分批匯出，或使用 MEDLINE 格式（最穩定）
