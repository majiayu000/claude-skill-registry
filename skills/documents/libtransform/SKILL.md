---
name: libtransform
description: >
  libtransform - Resource transformation utilities. pdfToHtml converts PDF
  documents to HTML using LLM vision capabilities, splitting pages to images and
  processing with multimodal models. Use for document conversion, PDF
  processing, and knowledge extraction from documents.
---

# libtransform Skill

## When to Use

- Converting PDF documents to HTML
- Extracting content from scanned documents
- Processing documents with LLM vision models
- Building document transformation pipelines

## Key Concepts

**pdfToHtml**: Splits PDF into page images, sends to vision-capable LLM, and
assembles HTML output with semantic structure.

## Usage Patterns

### Pattern 1: Convert PDF to HTML

```javascript
import { pdfToHtml } from "@copilot-ld/libtransform";

const pdfBuffer = await fs.readFile("document.pdf");
const html = await pdfToHtml(pdfBuffer, {
  model: "gpt-4-vision-preview",
  maxPages: 50,
});
```

## Integration

Used by libingest pipeline for document processing. Requires LLM with vision
capabilities.
