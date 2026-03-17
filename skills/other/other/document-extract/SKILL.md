---
context: fork
---

# /document-extract

Extract and analyse content from scanned documents, PDFs, and document images using Sonnet sub-agents.

## Usage

```
/document-extract <file-path>
/document-extract +Attachments/meeting-whiteboard.jpg
/document-extract +Attachments/spec-document.pdf
/document-extract +Attachments/handwritten-notes.png --type "meeting notes"
```

## Instructions

This skill uses **Sonnet model sub-agents** for comprehensive document analysis and text extraction.

### Phase 1: Document Loading

1. Verify the file exists at the specified path
2. Identify document type (PDF, image, photo of document)
3. Note any context about document purpose

### Phase 2: Comprehensive Analysis (Sonnet Sub-Agents)

Launch these sub-agents using `model: "sonnet"`:

**Agent 1: Text Extraction** (Sonnet)
```
Task: Extract all text content from the document
- Read the file using the Read tool
- Perform comprehensive OCR on all visible text
- Preserve structure (headings, paragraphs, lists)
- Handle multiple columns if present
- Extract text from tables maintaining structure
- Note any text that is unclear or uncertain
Return: Complete text extraction with structure preserved
```

**Agent 2: Structure Analysis** (Sonnet)
```
Task: Analyse document structure and formatting
- Read the file
- Identify document type (letter, form, spec, notes, etc.)
- Map section hierarchy
- Identify tables, lists, and special formatting
- Note headers, footers, page numbers
- Identify logos, stamps, signatures
Return: Document structure map
```

**Agent 3: Content Classification** (Sonnet)
```
Task: Classify and categorise the content
- Read the file
- Determine document purpose
- Identify key entities (people, projects, dates, systems)
- Extract action items or tasks
- Find decisions or commitments
- Note any deadlines or dates mentioned
- Identify references to YourOrg projects or systems
Return: Classified content with entity extraction
```

**Agent 4: Quality Assessment** (Sonnet)
```
Task: Assess extraction quality and completeness
- Read the file
- Evaluate image/scan quality
- Identify areas with low confidence extraction
- Note any missing or obscured content
- Assess if re-scan might be needed
- Check for multiple pages
Return: Quality report with confidence scores
```

### Phase 3: Compile Report

```markdown
# Document Extraction

**Source**: {{filename}}
**Extracted**: {{DATE}}
**Document Type**: {{type}}
**Quality Score**: {{High/Medium/Low}}

## Summary

{{Brief description of document content and purpose}}

## Extracted Content

### Full Text

{{complete extracted text with formatting preserved}}

---

## Structured Data

### Key Information
| Field | Value |
|-------|-------|
| Date | {{if found}} |
| Author | {{if found}} |
| Subject | {{if found}} |
| Reference | {{if found}} |

### People Mentioned
{{list of names with context}}

### Dates & Deadlines
| Date | Context |
|------|---------|
{{dates found}}

### Projects/Systems Referenced
{{links to matching vault notes}}

## Tables Extracted

{{any tables found, formatted as markdown}}

## Action Items Found

- [ ] {{action items extracted from document}}

## Decisions/Commitments

{{any decisions or commitments mentioned}}

## Extraction Notes

### Confidence Assessment
- Overall quality: {{assessment}}
- Unclear sections: {{list any problematic areas}}
- Recommendations: {{re-scan suggestions if needed}}

### Areas of Uncertainty
{{text that couldn't be confidently extracted}}

## Suggested Actions

1. **Create Note**: {{suggest note type and title}}
2. **Link to**: {{suggest related notes}}
3. **Follow up**: {{any actions needed}}
```

### Integration

After extraction, offer to:
1. Create a new vault note from the content
2. Append to an existing meeting or project note
3. Create tasks from action items found

### Notes

- Works with photos of whiteboards, handwritten notes, printed documents
- PDF support for text extraction
- Can recognise organization-specific terminology and systems
