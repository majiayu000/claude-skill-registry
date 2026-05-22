---
name: document-processing-docx
description: Process, parse, create, and manipulate Microsoft Word (.docx) documents programmatically using libraries like docx or mammoth.js for document generation and data extraction. Use when generating Word documents from templates, extracting text and formatting from .docx files, creating reports and invoices, parsing resumes and forms, converting Word to HTML, creating mail merge documents, or automating document workflows.
---

# Document Processing - DOCX Files

## When to use this skill

- Generating Word documents from templates
- Extracting text content from .docx files
- Creating automated reports and invoices
- Parsing resumes and job applications
- Converting Word documents to HTML or Markdown
- Creating mail merge documents programmatically
- Extracting tables and data from Word files
- Automating document generation workflows
- Creating contracts or agreements from templates
- Processing bulk document uploads
- Extracting metadata from Word documents
- Building document management systems

## When to use this skill

- Creating, editing Word documents programmatically.
- When working on related tasks or features
- During development that requires this expertise

**Use when**: Creating, editing Word documents programmatically.

## Example
\`\`\`typescript
import { Document, Packer, Paragraph } from 'docx';

const doc = new Document({
  sections: [{
    children: [new Paragraph("Hello World")]
  }]
});
\`\`\`

## Resources
- [docx npm package](https://www.npmjs.com/package/docx)
