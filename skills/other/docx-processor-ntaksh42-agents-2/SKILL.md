---
name: docx-processor
description: Process and generate Word documents with formatting, tables, and images. Use when working with Word documents or generating reports.
---

# Word Document Processor Skill

Word文書（.docx）の作成・編集を行うスキルです。

## 主な機能

- **文書作成**: ヘッダー、フッター、段落
- **スタイル**: フォント、色、書式
- **テーブル**: 表作成
- **画像**: 画像挿入
- **変換**: Markdown → DOCX

## Python (python-docx)

```python
from docx import Document
from docx.shared import Inches, Pt, RGBColor

doc = Document()

# タイトル
title = doc.add_heading('レポートタイトル', 0)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER

# 段落
p = doc.add_paragraph('これは本文です。')
p.add_run(' 太字テキスト').bold = True
p.add_run(' 斜体テキスト').italic = True

# テーブル
table = doc.add_table(rows=3, cols=3)
table.style = 'Light Grid Accent 1'

hdr_cells = table.rows[0].cells
hdr_cells[0].text = '名前'
hdr_cells[1].text = '年齢'
hdr_cells[2].text = '職業'

# 画像
doc.add_picture('image.png', width=Inches(4))

doc.save('report.docx')
```

## バージョン情報
- Version: 1.0.0
