---
name: pdf-reader
description: |
  Read and extract content from PDF files using multiple methods.
  LOAD THIS SKILL WHEN: User says "讀取 PDF", "read PDF", "打開論文", "看這篇" | has PDF file path | needs to extract text from PDF.
  CAPABILITIES: PDF to markdown conversion, text extraction, figure detection, citation extraction.
---

# PDF 讀取技能 (PDF Reader)

## 描述

使用多種方法讀取 PDF 檔案並轉換為結構化文字，支援本地檔案和網路 URL。

## 觸發條件

- 「讀取 PDF」「打開這篇論文」「看這個檔案」
- "read PDF", "open paper", "extract from PDF"
- 提供 PDF 檔案路徑或 URL

## 可用 Tools

### MCP Tools (microsoft-mar)

| Tool | 用途 | 參數 |
|------|------|------|
| `convert_to_markdown` | 將 PDF 轉換為 Markdown | uri (file:// 或 http://) |

### MCP Tools (pubmed-search)

| Tool | 用途 | 參數 |
|------|------|------|
| `get_article_fulltext_links` | 取得全文連結 | pmid |

### Python Scripts (可選)

```python
# scripts/pdf_utils.py

import fitz  # PyMuPDF

def extract_text(pdf_path: str) -> str:
    """提取 PDF 文字"""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_images(pdf_path: str, output_dir: str) -> list:
    """提取 PDF 圖片"""
    # ...實作
    pass

def extract_references(pdf_path: str) -> list:
    """提取參考文獻"""
    # ...實作
    pass
```

## 執行流程

### 1. 本地 PDF 讀取

```
用戶提供本地路徑: C:\papers\article.pdf
    ↓
convert_to_markdown(uri="file:///C:/papers/article.pdf")
    ↓
返回 Markdown 格式文字
```

### 2. 網路 PDF 讀取

```
用戶提供 URL 或 PMID
    ↓
(如果是 PMID) get_article_fulltext_links(pmid)
    ↓
取得 PDF URL
    ↓
convert_to_markdown(uri="https://...")
    ↓
返回 Markdown 格式文字
```

### 3. 批次處理模式

```python
# 處理多個 PDF
pdf_files = [
    "C:/papers/paper1.pdf",
    "C:/papers/paper2.pdf",
    "C:/papers/paper3.pdf"
]

for pdf in pdf_files:
    content = convert_to_markdown(uri=f"file:///{pdf}")
    save_to_notes(content, pdf)
    # Checkpoint: 記錄處理進度
    update_checkpoint(processed=pdf)
```

## 輸出格式

```markdown
## PDF 讀取結果

**檔案**: article.pdf
**頁數**: 12
**處理時間**: 3.2s

---

### 提取內容

# [論文標題]

## Abstract
[摘要內容...]

## Introduction
[介紹內容...]

## Methods
[方法內容...]

## Results
[結果內容...]

## Discussion
[討論內容...]

## References
1. Author et al. (2024). Title...
2. ...

---

### 圖表清單

| 圖表 | 頁碼 | 說明 |
|------|------|------|
| Figure 1 | p.3 | Study flowchart |
| Table 1 | p.5 | Baseline characteristics |
```

## 使用範例

**範例 1：本地 PDF**
```
用戶：「讀取 C:\papers\remimazolam-study.pdf」
執行：convert_to_markdown(uri="file:///C:/papers/remimazolam-study.pdf")
```

**範例 2：從 PMID 取得 PDF**
```
用戶：「讀取 PMID 38353755 的全文」
執行：
1. get_article_fulltext_links(pmid="38353755")
2. convert_to_markdown(uri=pmc_url)
```

**範例 3：批次讀取**
```
用戶：「讀取 papers/ 資料夾中的所有 PDF」
執行：
1. 列出資料夾中的 PDF 檔案
2. 迴圈處理每個檔案
3. 建立 Checkpoint 追蹤進度
```

## 錯誤處理

| 錯誤 | 處理方式 |
|------|----------|
| PDF 加密 | 提示用戶提供密碼或使用其他版本 |
| 圖片 PDF (掃描) | 提示需要 OCR，建議使用其他工具 |
| 網路錯誤 | 重試 3 次，失敗後提示用戶下載 |

## 相關技能

- `note-writer` - 撰寫筆記
- `report-writing` - 組合技能：讀取 + 撰寫
