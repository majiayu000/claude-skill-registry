---
name: pdf-processor
description: Process, extract, and generate PDF documents with text extraction and form handling. Use when working with PDF files or extracting PDF content.
---

# PDF Processor Skill

PDFファイルの作成、編集、解析を行うスキルです。

## 概要

PDFの読み取り、テキスト抽出、フォーム処理、新規PDF作成を支援します。

## 主な機能

- **テキスト抽出**: PDFからテキストとテーブルを抽出
- **PDF生成**: HTMLやMarkdownからPDF作成
- **フォーム処理**: PDFフォームの読み書き
- **分割・結合**: 複数PDFの操作
- **透かし追加**: セキュリティマーク
- **パスワード保護**: 暗号化PDF作成
- **メタデータ編集**: タイトル、作成者等

## 使用方法

### テキスト抽出

```python
# Python + PyPDF2
import PyPDF2

with open('document.pdf', 'rb') as file:
    reader = PyPDF2.PdfReader(file)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    print(text)
```

### PDF生成（HTMLから）

```python
# Python + pdfkit/weasyprint
import pdfkit

pdfkit.from_file('document.html', 'output.pdf')

# または
from weasyprint import HTML
HTML('document.html').write_pdf('output.pdf')
```

### PDF結合

```python
from PyPDF2 import PdfMerger

merger = PdfMerger()
merger.append('file1.pdf')
merger.append('file2.pdf')
merger.write('combined.pdf')
merger.close()
```

### フォーム処理

```python
from PyPDF2 import PdfReader, PdfWriter

reader = PdfReader('form.pdf')
writer = PdfWriter()

# フォームフィールドに値を設定
writer.add_page(reader.pages[0])
writer.update_page_form_field_values(
    writer.pages[0],
    {'name': 'John Doe', 'email': 'john@example.com'}
)

with open('filled_form.pdf', 'wb') as output:
    writer.write(output)
```

### JavaScript/Node.js

```javascript
// pdf-lib
const { PDFDocument } = require('pdf-lib');
const fs = require('fs');

async function createPdf() {
  const pdfDoc = await PDFDocument.create();
  const page = pdfDoc.addPage([600, 400]);

  page.drawText('Hello World!', {
    x: 50,
    y: 350,
    size: 30
  });

  const pdfBytes = await pdfDoc.save();
  fs.writeFileSync('output.pdf', pdfBytes);
}
```

## ライブラリ

### Python
- **PyPDF2**: PDF読み書き
- **pdfplumber**: テーブル抽出
- **ReportLab**: PDF生成
- **WeasyPrint**: HTML→PDF
- **pdfkit**: wkhtmltopdf wrapper

### JavaScript/Node.js
- **pdf-lib**: PDF作成・編集
- **pdfjs-dist**: PDF解析
- **puppeteer**: HTML→PDF
- **jsPDF**: ブラウザでPDF生成

### Go
- **gofpdf**: PDF生成
- **unidoc**: 商用ライブラリ

## バージョン情報

- スキルバージョン: 1.0.0
- 最終更新: 2025-01-22
