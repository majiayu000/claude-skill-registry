---
name: pubmed-export-citations
description: Export citations to reference managers. Triggers: 匯出, export, RIS, BibTeX, EndNote, Zotero, Mendeley, 引用格式, reference manager
---

# 引用匯出指南

## 快速決策樹

```
需要匯出引用？
├── EndNote/Zotero/Mendeley → prepare_export(pmids="last", format="ris")
├── LaTeX/Overleaf → prepare_export(pmids="last", format="bibtex", source="local")
├── Excel 分析 → prepare_export(pmids="last", format="csv", source="local")
└── 程式處理 → prepare_export(pmids="last", format="csl")
```

---

## 工具簽名

```python
prepare_export(
    pmids: str | list,      # "last" | "12345678,87654321" | ["12345678"]
    format: str = "ris",    # ris, medline, csl, bibtex, csv, json
    include_abstract: bool = True,
    source: str = "official"  # "official" (推薦) | "local"
)
```

---

## 來源選項對比

| 來源 | 支援格式 | 品質 | 何時使用 |
|------|----------|------|----------|
| **official** (預設) | ris, medline, csl | ★★★★★ | 📌 優先選擇，官方 API |
| **local** | ris, bibtex, csv, medline, json | ★★★★ | BibTeX/CSV 專用 |

> **💡 建議**: 除非需要 BibTeX 或 CSV，否則使用預設的 `source="official"`

---

## 格式選擇指南

| 用途 | 格式 | 來源 | 範例 |
|------|------|------|------|
| EndNote/Zotero/Mendeley | ris | official | `prepare_export(pmids="last", format="ris")` |
| LaTeX/Overleaf | bibtex | local | `prepare_export(pmids="last", format="bibtex", source="local")` |
| Excel/數據分析 | csv | local | `prepare_export(pmids="last", format="csv", source="local")` |
| 程式處理 (styled) | csl | official | `prepare_export(pmids="last", format="csl")` |
| 備份保存 | medline | official | `prepare_export(pmids="last", format="medline")` |

---

## 常用範例

### 1. 匯出上次搜尋結果 (最常用)

```python
# 先搜尋
search_literature(query="remimazolam sedation", limit=30)

# 匯出到 EndNote/Zotero（官方 API，最佳品質）
prepare_export(pmids="last", format="ris")
```

### 2. 匯出指定 PMID

```python
prepare_export(pmids="30217674,28523456,35678901", format="ris")
```

### 3. LaTeX 專用 BibTeX

```python
# BibTeX 只支援 local source
prepare_export(pmids="last", format="bibtex", source="local")
```

### 4. 資料分析 CSV

```python
prepare_export(pmids="last", format="csv", source="local")
```

---

## 輸出格式

### 成功回應

```json
{
    "status": "success",
    "article_count": 10,
    "format": "ris",
    "source": "official",
    "export_text": "TY  - JOUR\nAU  - Doi, Mitsuharu\n..."
}
```

### 大量匯出（>20篇）

```json
{
    "status": "success",
    "article_count": 50,
    "format": "ris",
    "source": "official",
    "file_path": "/tmp/pubmed_exports/pubmed_export_50_20250126.ris"
}
```

---

## RIS 格式範例（官方 API 輸出）

```
TY  - JOUR
DB  - PubMed
AU  - Doi, Mitsuharu
AU  - Hirata, Nobuhiro
T1  - Remimazolam versus midazolam for procedural sedation
LA  - eng
SN  - 1528-1175
Y1  - 2020/01/01
AB  - BACKGROUND: Remimazolam is a novel benzodiazepine...
SP  - 63
EP  - 74
VL  - 132
AN  - 30217674
UR  - https://pubmed.ncbi.nlm.nih.gov/30217674
DO  - 10.1097/ALN.0000000000002435
ER  -
```

---

## 各軟體匯入

| 軟體 | 步驟 |
|------|------|
| **EndNote** | File → Import → 選 RIS → Import Option: "RefMan RIS" |
| **Zotero** | File → Import → 選 RIS (自動識別) |
| **Mendeley** | File → Import → RIS |
| **Overleaf** | 上傳 .bib 檔案 → `\cite{Author2020}` |

---

## 完整工作流程

```python
# Step 1: 搜尋
search_literature(query="remimazolam ICU sedation", limit=50)

# Step 2: 匯出到 EndNote（官方 API）
prepare_export(pmids="last", format="ris")

# Step 3: 同時匯出 CSV 到 Excel 篩選
prepare_export(pmids="last", format="csv", source="local")
```

---

## 常見問題

| 問題 | 解決方案 |
|------|----------|
| 需要 BibTeX | 使用 `source="local"` |
| 匯出失敗 | 系統會自動 fallback 到 local |
| 缺少摘要 | 確認 `include_abstract=True` (預設) |
| 大量匯出 | >20篇自動存檔，回傳 file_path |
