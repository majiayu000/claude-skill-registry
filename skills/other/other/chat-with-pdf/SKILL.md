---
# ═══════════════════════════════════════════════════════════════════════════════
# CLAUDE OFFICE SKILL - Enhanced Metadata v2.0
# ═══════════════════════════════════════════════════════════════════════════════

# Basic Information
name: Chat with PDF
description: "Answer questions about PDF content, summarize, and extract information"
version: "1.0"
author: claude-office-skills
license: MIT

# Categorization
category: pdf
tags:
  - pdf
  - chat
  - qa
  - extraction
department: All

# AI Model Compatibility
models:
  recommended:
    - claude-sonnet-4
    - claude-opus-4
  compatible:
    - claude-3-5-sonnet
    - gpt-4
    - gpt-4o

# MCP Tools Integration
mcp:
  server: office-mcp
  tools:
    - extract_text_from_pdf
    - get_pdf_metadata

# Skill Capabilities
capabilities:
  - pdf_qa
  - content_extraction
  - summarization

# Language Support
languages:
  - en
  - zh
---

# Chat with PDF

Have intelligent conversations about PDF documents - ask questions, get summaries, and extract specific information.

## Overview

This skill enables you to:
- Ask questions about PDF content
- Get summaries at various detail levels
- Extract specific data points
- Compare information across multiple PDFs
- Find relevant sections quickly

## How to Use

### Basic Interaction
1. Share or upload the PDF document
2. Ask your question or request
3. Get contextual answers with citations

### Question Types

**Factual Questions**
```
"What is the contract value mentioned in this document?"
"Who are the parties involved in this agreement?"
"What are the key dates mentioned?"
```

**Summarization**
```
"Summarize this document in 3 bullet points"
"Give me an executive summary"
"What are the main topics covered?"
```

**Extraction**
```
"Extract all names and titles mentioned"
"List all financial figures in the document"
"Find all action items or deliverables"
```

**Analysis**
```
"What are the risks mentioned in this contract?"
"Are there any ambiguous terms?"
"What obligations does Party A have?"
```

## Output Formats

### Q&A Format
```markdown
**Question**: [Your question]

**Answer**: [Direct answer to your question]

**Source**: Page [X], Section [Y]
> "[Relevant quote from document]"

**Confidence**: [High/Medium/Low]
```

### Summary Format
```markdown
## Document Summary

**Type**: [Contract/Report/Manual/etc.]
**Pages**: [X]
**Date**: [If mentioned]

### Key Points
1. [Main point 1]
2. [Main point 2]
3. [Main point 3]

### Important Details
- [Detail 1]
- [Detail 2]
```

### Extraction Format
```markdown
## Extracted Information

### [Category 1]
| Item | Value | Location |
|------|-------|----------|
| [Item 1] | [Value] | Page X |
| [Item 2] | [Value] | Page Y |

### [Category 2]
...
```

## Best Practices

### For Better Answers
1. **Be specific**: "What is the termination clause?" vs "Tell me about the contract"
2. **Reference sections**: "What does Section 5.2 say about liability?"
3. **Ask follow-ups**: Build on previous answers for deeper understanding

### For Better Extraction
1. **Specify format**: "Extract as a table" or "List as bullet points"
2. **Name the fields**: "Extract: name, date, amount, description"
3. **Set criteria**: "Only extract amounts over $10,000"

### For Better Summaries
1. **Specify length**: "Summarize in 100 words" or "3 bullet points"
2. **Focus area**: "Summarize the financial terms only"
3. **Audience**: "Summarize for a legal team" vs "for executives"

## Example Workflows

### Contract Review
```
1. "What type of contract is this?"
2. "Who are the parties and what are their roles?"
3. "What are the key obligations for each party?"
4. "What is the term and renewal process?"
5. "What are the termination conditions?"
6. "Are there any unusual or concerning clauses?"
```

### Research Paper Analysis
```
1. "What is the main thesis or hypothesis?"
2. "What methodology was used?"
3. "What are the key findings?"
4. "What are the limitations mentioned?"
5. "What future research do they suggest?"
```

### Financial Report
```
1. "What is the total revenue reported?"
2. "How does this compare to last year?"
3. "What are the main expense categories?"
4. "What guidance is given for next quarter?"
5. "Extract all financial metrics into a table"
```

## Multi-Document Support

When working with multiple PDFs:

```
"Compare the terms in Contract A vs Contract B"
"Which document mentions [topic]?"
"Create a summary table comparing key points across all documents"
```

### Comparison Output
```markdown
## Document Comparison

| Aspect | Document A | Document B |
|--------|------------|------------|
| Term Length | 2 years | 3 years |
| Value | $50,000 | $75,000 |
| Termination | 30 days notice | 60 days notice |

### Key Differences
1. [Difference 1]
2. [Difference 2]

### Similarities
1. [Similarity 1]
2. [Similarity 2]
```

## Handling Challenges

### Scanned PDFs (Image-based)
- OCR will be applied automatically
- Quality depends on scan quality
- May have recognition errors

### Complex Layouts
- Tables may need reformatting
- Multi-column text is processed left-to-right
- Footnotes processed separately

### Long Documents
- Ask about specific sections for accuracy
- Request page-by-page summaries for overview
- Use targeted questions over broad ones

## Limitations

- Cannot execute code embedded in PDFs
- Password-protected PDFs need password
- Very large PDFs (500+ pages) may need chunking
- Handwritten content recognition is limited
- Cannot guarantee 100% accuracy on scanned documents
- Charts and images are described, not analyzed numerically

## Privacy Note

Document contents are processed according to the AI provider's privacy policy. For sensitive documents, consider:
- Using on-premise solutions
- Redacting sensitive information first
- Checking data retention policies
