---
name: docx
description: Expert in creating, editing, and automating Word documents (.docx) using python-docx and docx.js. Use when generating Word documents, modifying existing docx files, or automating document workflows.
---

# DOCX Skill

## Purpose
Provides expertise in programmatic Word document creation and manipulation. Handles document generation, template filling, style management, and batch document processing using python-docx and JavaScript libraries.

## When to Use
- Generating Word documents programmatically
- Filling document templates with data
- Modifying existing .docx files
- Extracting content from Word documents
- Applying styles and formatting
- Creating mail merge workflows
- Converting data to formatted documents

## Quick Start
**Invoke this skill when:**
- Generating Word documents programmatically
- Filling document templates with data
- Modifying existing .docx files
- Extracting content from Word documents
- Automating document workflows

**Do NOT invoke when:**
- Writing document content (use document-writer)
- Creating PDFs (use pdf-skill)
- Creating spreadsheets (use xlsx-skill)
- Creating presentations (use pptx-skill)

## Decision Framework
```
Library Selection:
├── Python backend → python-docx
├── Node.js backend → docx (npm)
├── Browser-based → docx.js
├── Complex templates → docxtemplater
└── Simple text extraction → mammoth

Task Type:
├── Generate from scratch → Build document programmatically
├── Fill template → Use placeholder replacement
├── Modify existing → Load, edit, save
└── Batch processing → Loop with template
```

## Core Workflows

### 1. Document Generation (python-docx)
1. Create Document object
2. Add heading with level
3. Add paragraphs with text
4. Apply styles (built-in or custom)
5. Add tables if needed
6. Insert images
7. Save document

### 2. Template Processing
1. Load template document
2. Find placeholders ({{variable}})
3. Replace with actual values
4. Handle conditional sections
5. Process repeating sections
6. Save as new document

### 3. Batch Document Generation
1. Load template once
2. Iterate over data records
3. Clone template for each
4. Fill placeholders
5. Generate unique filenames
6. Save each document

## Best Practices
- Use paragraph styles, not direct formatting
- Create templates with placeholders for reuse
- Handle missing placeholder values gracefully
- Preserve original template, save to new file
- Test with complex content (tables, images)
- Validate output opens correctly

## Anti-Patterns
| Anti-Pattern | Problem | Correct Approach |
|--------------|---------|------------------|
| Direct formatting | Hard to maintain | Use styles |
| Modifying template | Corrupts original | Save to new file |
| No error handling | Fails on bad input | Validate data first |
| Hardcoded paths | Not portable | Use relative paths |
| Ignoring encoding | Character issues | Use UTF-8 strings |
