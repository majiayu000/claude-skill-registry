---
name: word
description: Create, read, edit, and manipulate Microsoft Word documents (.docx files). Use when users ask to work with Word files, create documents, read .docx files, or format text documents.
allowed-tools: Read, Write, Bash
---

# Word Document Tool

This skill allows you to work with Microsoft Word documents using Node.js tools.

## Capabilities

- **Read** existing Word documents and extract text content
- **Create** new Word documents with formatted text, headings, paragraphs, and tables
- **Modify** existing documents by appending content
- **Extract** document structure and formatting

## When to Use

Invoke this skill when the user:
- Mentions Word documents, .docx files, or document creation
- Asks to read, create, modify, or format text documents
- Needs to generate reports, letters, or formatted documents
- Wants to extract text from existing Word files

## How to Use

The Word tool is implemented as a TypeScript script at `src/tools/word-tool.ts`. You can invoke it using the Bash tool:

### Reading a Document
```bash
ts-node src/tools/word-tool.ts read "/path/to/document.docx"
```

### Creating a Document
```bash
ts-node src/tools/word-tool.ts create "/path/to/new-document.docx" '{"title":"My Document","paragraphs":["First paragraph","Second paragraph"]}'
```

## JSON Structure for Creating Documents

When creating documents, use this JSON format:
```json
{
  "title": "Document Title",
  "paragraphs": ["Paragraph 1", "Paragraph 2"],
  "headings": [{"text": "Section 1", "level": 1}],
  "tables": [{"headers": ["Col1", "Col2"], "rows": [["A", "B"]]}]
}
```

## Implementation

Uses the `docx` and `mammoth` npm libraries for reading and writing Word documents.
