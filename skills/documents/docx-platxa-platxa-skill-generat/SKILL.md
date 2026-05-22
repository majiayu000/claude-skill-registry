---
name: docx
description: >-
  Use when the user asks to create, edit, analyze, or review Word documents
  (.docx files). Covers three workflows: creating new documents with docx-js
  (JavaScript), editing existing documents via OOXML manipulation with a Python
  Document library, and redlining (tracked changes) for professional document
  review. Also handles text extraction with pandoc and conversion to PDF/images.
allowed-tools:
  - Bash
  - Edit
  - Read
  - Task
  - Write
metadata:
  version: "1.0.0"
  author: "platxa-skill-generator"
  tags:
    - guide
    - document-processing
    - docx
    - ooxml
    - tracked-changes
  provenance:
    upstream_source: "docx"
    upstream_sha: "c0e08fdaa8ed6929110c97d1b867d101fd70218f"
    regenerated_at: "2026-02-04T22:00:00Z"
    generator_version: "1.0.0"
    intent_confidence: 0.61
---

# DOCX Creation, Editing, and Analysis

Work with Word documents: create from scratch, edit existing content, add tracked changes for professional review, extract text, and convert to PDF or images.

## Overview

A .docx file is a ZIP archive of XML files and resources. Different tasks require different tools:

| Task | Tool | Workflow |
|------|------|----------|
| **Create new document** | docx-js (JavaScript) | Write JS/TS, export with `Packer.toBuffer()` |
| **Edit existing document** | Document library (Python) | Unpack, manipulate XML, repack |
| **Redline / tracked changes** | Document library (Python) | Unpack, apply `<w:ins>`/`<w:del>` tags, repack |
| **Extract text** | pandoc | `pandoc --track-changes=all file.docx -o out.md` |
| **Convert to images** | LibreOffice + pdftoppm | DOCX to PDF to JPEG |

## When to Use

- User asks to create a new Word document from content or data
- User asks to edit, modify, or update an existing .docx file
- User asks to review a document with tracked changes (redlining)
- User asks to add comments to a Word document
- User asks to extract or read text from a .docx file
- User asks to convert a .docx to PDF or images for visual inspection

## Workflow Decision Tree

```
User request
 |- "Create a new document"
 |   -> Creating workflow (docx-js)
 |- "Edit my own document" + simple changes
 |   -> Basic OOXML editing workflow
 |- "Review someone else's document"
 |   -> Redlining workflow (recommended default)
 |- "Legal, academic, business, or government docs"
 |   -> Redlining workflow (required)
 |- "Read/analyze document content"
 |   -> Text extraction with pandoc
 |- "Show me what the document looks like"
     -> Convert to images workflow
```

## Creating a New Document (docx-js)

Use the docx-js library to create Word documents in JavaScript/TypeScript.

### Steps

1. **Read the docx-js reference**: Load `references/docx-js-patterns.md` for syntax, formatting rules, and common pitfalls
2. **Write a JS/TS file** using `Document`, `Paragraph`, `TextRun`, `Table`, and other components
3. **Export** with `Packer.toBuffer()` and write to disk

### Key Rules

- Never use `\n` for line breaks; use separate `Paragraph` elements
- Always use `LevelFormat.BULLET` constant for bullet lists (not unicode symbols or string "bullet")
- Always specify `type` parameter for `ImageRun` (png, jpg, gif, bmp, svg)
- Set `columnWidths` array AND individual cell widths on tables
- Use `ShadingType.CLEAR` for table cell shading (never `SOLID`)
- `PageBreak` must always be inside a `Paragraph`; standalone creates invalid XML
- Override built-in heading styles using exact IDs: `"Heading1"`, `"Heading2"`, `"Heading3"`
- Include `outlineLevel` on heading styles for Table of Contents compatibility
- Set a default font via `styles.default.document.run.font` (Arial recommended)

```javascript
const { Document, Packer, Paragraph, TextRun } = require('docx');
const fs = require('fs');

const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 24 } } }
  },
  sections: [{
    properties: {
      page: { margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } }
    },
    children: [
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("Section Title")]
      }),
      new Paragraph({
        children: [new TextRun("Body text in Arial 12pt.")]
      })
    ]
  }]
});

Packer.toBuffer(doc).then(buf => fs.writeFileSync("output.docx", buf));
```

## Editing an Existing Document (OOXML)

Use the Document library (Python) for editing existing Word documents via XML manipulation.

### Steps

1. **Read the OOXML reference**: Load `references/ooxml-patterns.md` for the Document library API and XML patterns
2. **Unpack**: `python ooxml/scripts/unpack.py <file.docx> <output_dir>`
3. **Write a Python script** using the Document class for manipulation
4. **Repack**: `python ooxml/scripts/pack.py <dir> <output.docx>`

### Document Library Basics

```python
from scripts.document import Document

doc = Document('unpacked')
# Find nodes by text, line number, or attributes
node = doc["word/document.xml"].get_node(tag="w:r", contains="target text")
# Replace content
doc["word/document.xml"].replace_node(node, "<w:r><w:t>new text</w:t></w:r>")
doc.save()
```

Set PYTHONPATH to the skill root directory before running:

```bash
PYTHONPATH=/path/to/docx-skill python your_script.py
```

## Redlining Workflow (Tracked Changes)

For professional document review with tracked changes. This is the recommended default for editing another person's document and required for legal, academic, business, or government documents.

### Principle: Minimal, Precise Edits

Only mark text that actually changes. Keep unchanged text outside `<w:del>`/`<w:ins>` tags. Preserve the original run's RSID for unchanged text.

```python
# BAD - replaces entire sentence
'<w:del>..entire sentence..</w:del><w:ins>..entire sentence..</w:ins>'

# GOOD - only marks what changed: "30 days" -> "60 days"
'<w:r w:rsidR="00AB12CD"><w:t>within </w:t></w:r>'
'<w:del><w:r><w:delText>30</w:delText></w:r></w:del>'
'<w:ins><w:r><w:t>60</w:t></w:r></w:ins>'
'<w:r w:rsidR="00AB12CD"><w:t> days</w:t></w:r>'
```

### Steps

1. **Convert to markdown**: `pandoc --track-changes=all file.docx -o current.md`
2. **Identify and group changes** into batches of 3-10 related changes (by section, type, or proximity)
3. **Read OOXML reference** and **unpack**: `python ooxml/scripts/unpack.py file.docx unpacked`
4. **Implement each batch**: Use `get_node()` to find nodes, apply tracked changes with `replace_node()`, `suggest_deletion()`, or `insert_after()`
5. **Repack**: `python ooxml/scripts/pack.py unpacked reviewed.docx`
6. **Verify**: Convert back to markdown and grep for expected changes

### Method Selection

| Scenario | Method |
|----------|--------|
| Change regular text | `replace_node()` with `<w:del>`/`<w:ins>` |
| Delete entire run or paragraph | `suggest_deletion(node)` |
| Reject another author's insertion | `revert_insertion(ins_node)` |
| Restore another author's deletion | `revert_deletion(del_node)` |
| Add comment | `doc.add_comment(start, end, text)` |
| Reply to comment | `doc.reply_to_comment(parent_id, text)` |

## Reading and Analyzing Content

### Text Extraction

```bash
# Convert to markdown preserving tracked changes
pandoc --track-changes=all document.docx -o output.md
# Options: --track-changes=accept/reject/all
```

### Raw XML Access

For comments, complex formatting, metadata, or embedded media:

```bash
python ooxml/scripts/unpack.py document.docx unpacked/
```

Key files inside the unpacked archive:

| Path | Content |
|------|---------|
| `word/document.xml` | Main document body |
| `word/comments.xml` | Comments referenced in document.xml |
| `word/media/` | Embedded images and media |
| `word/styles.xml` | Document styles |
| `word/settings.xml` | Document settings |

## Converting to Images

Two-step process for visual inspection:

```bash
# Step 1: DOCX to PDF
soffice --headless --convert-to pdf document.docx

# Step 2: PDF to JPEG images
pdftoppm -jpeg -r 150 document.pdf page
# Creates page-1.jpg, page-2.jpg, etc.

# Specific page range:
pdftoppm -jpeg -r 150 -f 2 -l 5 document.pdf page
```

## Best Practices

### Do

- Read the appropriate reference file before starting any document task
- Use separate `Paragraph` elements for each line (never `\n`)
- Set a default font and establish visual hierarchy with styles
- Group tracked changes into batches of 3-10 for manageable debugging
- Grep `word/document.xml` before each script to get current line numbers
- Preserve original run formatting (`<w:rPr>`) when making tracked changes
- Use `defusedxml` for secure XML parsing

### Do Not

- Use unicode bullets (`"bullet"` string or `SymbolRun` for lists); use `LevelFormat.BULLET`
- Mix up `<w:ins>`/`<w:del>` closing tags
- Use markdown line numbers to locate content in XML (they do not map)
- Modify text inside another author's `<w:ins>` or `<w:del>` directly; use nested deletions
- Skip validation after repacking (`doc.save()` validates by default)

## Dependencies

| Package | Install | Purpose |
|---------|---------|---------|
| pandoc | `sudo apt-get install pandoc` | Text extraction |
| docx | `npm install -g docx` | Creating new documents |
| defusedxml | `pip install defusedxml` | Secure XML parsing |
| LibreOffice | `sudo apt-get install libreoffice` | PDF conversion |
| poppler-utils | `sudo apt-get install poppler-utils` | PDF to images (`pdftoppm`) |

## Examples

### Example 1: Create a Simple Report

```
User: Create a Word document with a title "Q4 Report", two sections with
      headings, and a bullet list of key metrics.

Action: Read references/docx-js-patterns.md, then write a JS file using
        Document with Heading1 style override, numbered sections, and a
        bullet list via numbering config with LevelFormat.BULLET. Export
        with Packer.toBuffer().
```

### Example 2: Redline a Contract

```
User: Review this NDA and change the confidentiality period from 2 years
      to 3 years, and update the governing law from California to Delaware.

Action: Use the redlining workflow. Convert to markdown first to understand
        the document, then unpack, read references/ooxml-patterns.md, find
        the target text with get_node(), apply minimal tracked changes
        (only mark "2 years" -> "3 years" and "California" -> "Delaware"),
        repack, and verify with pandoc.
```

### Example 3: Extract Text from a Document

```
User: What does this contract say about termination clauses?

Action: Run pandoc --track-changes=all contract.docx -o contract.md,
        then read the markdown file and search for termination-related
        sections.
```

## Output Checklist

- [ ] Correct workflow selected based on decision tree
- [ ] Reference file read before starting implementation
- [ ] Document opens without errors in Word or LibreOffice
- [ ] Tracked changes display correctly (for redlining tasks)
- [ ] No unintended formatting changes introduced
- [ ] All changes verified via markdown conversion