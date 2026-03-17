---
name: pdf-tools
description: Manipulate PDF files using PyMuPDF (fitz). Use when searching/highlighting text in PDFs, merging multiple PDFs, extracting pages, or any PDF manipulation task.
---

# PDF Tools

Manipulate PDFs using PyMuPDF (fitz).

## Setup

```bash
pip3 install --user --break-system-packages pymupdf
```

## Search and Highlight Text

```python
import fitz

doc = fitz.open("input.pdf")
for page in doc:
    instances = page.search_for("text to find")
    for inst in instances:
        highlight = page.add_highlight_annot(inst)
        highlight.set_colors(stroke=(1, 1, 0))  # Yellow
        highlight.update()
doc.save("output.pdf")
```

## Merge PDFs

```python
import fitz

merged = fitz.open()
for pdf_path in ["doc1.pdf", "doc2.pdf"]:
    merged.insert_pdf(fitz.open(pdf_path))
merged.save("merged.pdf")
```

## Extract Pages

```python
import fitz

doc = fitz.open("input.pdf")
new_doc = fitz.open()
new_doc.insert_pdf(doc, from_page=5, to_page=10)  # Pages 6-11 (0-indexed)
new_doc.save("extract.pdf")
```

## Extract Text

```python
import fitz

doc = fitz.open("input.pdf")
for page in doc:
    text = page.get_text()
    print(text)
```

## Add Text Annotation

```python
import fitz

doc = fitz.open("input.pdf")
page = doc[0]
rect = fitz.Rect(100, 100, 200, 120)
page.insert_textbox(rect, "Added text", fontsize=12)
doc.save("output.pdf")
```
