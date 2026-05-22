---
name: docx
description: "Comprehensive document creation, editing, and analysis with support for tracked changes, comments, formatting preservation, and text extraction. When Claude needs to work with professional documents (.docx files) for: (1) Creating new documents, (2) Modifying or editing content, (3) Working with tracked changes, (4) Adding comments, or any other document tasks"
---

# DOCX Creation, Editing, and Analysis

## Overview

Work with .docx files which are ZIP archives containing XML files. Different tools and workflows available for different tasks.

## Workflow Decision Tree

### Reading/Analyzing Content
Use text extraction or raw XML access

### Creating New Document
Use docx-js workflow

### Editing Existing Document
- **Your own document + simple changes**: Basic OOXML editing
- **Someone else's document**: Redlining workflow (recommended)
- **Legal, academic, business docs**: Redlining workflow (required)

## Reading and Analyzing Content

### Text Extraction
```bash
# Convert to markdown with tracked changes
pandoc --track-changes=all path-to-file.docx -o output.md
```

### Raw XML Access
For comments, complex formatting, document structure, embedded media, and metadata:

```bash
# Unpack document
python ooxml/scripts/unpack.py <office_file> <output_directory>
```

Key file structures:
- `word/document.xml` - Main document contents
- `word/comments.xml` - Comments
- `word/media/` - Embedded images and media

## Creating New Documents

Use **docx-js** (JavaScript/TypeScript):

```javascript
import { Document, Paragraph, TextRun, Packer } from 'docx';

const doc = new Document({
  sections: [{
    properties: {},
    children: [
      new Paragraph({
        children: [new TextRun("Hello World!")],
      }),
    ],
  }],
});

// Export
const buffer = await Packer.toBuffer(doc);
```

## Editing Existing Documents

Use the Document library (Python) for OOXML manipulation:

1. Unpack: `python ooxml/scripts/unpack.py <file.docx> <dir>`
2. Create Python script using Document library
3. Pack: `python ooxml/scripts/pack.py <dir> <file.docx>`

## Redlining Workflow

For tracked changes:

1. Convert to markdown: `pandoc --track-changes=all file.docx -o current.md`
2. Identify and group changes
3. Unpack document
4. Implement changes in batches using Document library
5. Pack the document
6. Verify all changes applied correctly

## Dependencies

- **pandoc**: For text extraction
- **docx**: `npm install -g docx` for creating new documents
- **LibreOffice**: For PDF conversion
- **defusedxml**: For secure XML parsing
