---
# ═══════════════════════════════════════════════════════════════════════════════
# CLAUDE OFFICE SKILL - Enhanced Metadata v2.0
# ═══════════════════════════════════════════════════════════════════════════════

# Basic Information
name: office-to-md
description: ">"
version: "1.0"
author: claude-office-skills
license: MIT

# Categorization
category: conversion
tags:
  - office
  - markdown
  - conversion
  - markitdown
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
    - docx_to_md

# Skill Capabilities
capabilities:
  - office_conversion
  - markdown_export

# Language Support
languages:
  - en
  - zh
---

# Office to Markdown Skill

## Overview

This skill enables conversion from various Office formats to Markdown using **markitdown** - Microsoft's open-source tool for converting documents to Markdown. Perfect for making Office content searchable, version-controllable, and AI-friendly.

## How to Use

1. Provide the Office file (Word, Excel, PowerPoint, PDF, etc.)
2. Optionally specify conversion options
3. I'll convert it to clean Markdown

**Example prompts:**
- "Convert this Word document to Markdown"
- "Turn this PowerPoint into Markdown notes"
- "Extract content from this PDF as Markdown"
- "Convert this Excel file to Markdown tables"

## Domain Knowledge

### markitdown Fundamentals

```python
from markitdown import MarkItDown

# Initialize converter
md = MarkItDown()

# Convert file
result = md.convert("document.docx")
print(result.text_content)

# Save to file
with open("output.md", "w") as f:
    f.write(result.text_content)
```

### Supported Formats

| Format | Extension | Notes |
|--------|-----------|-------|
| Word | .docx | Full text, tables, basic formatting |
| Excel | .xlsx | Converts to Markdown tables |
| PowerPoint | .pptx | Slides as sections |
| PDF | .pdf | Text extraction |
| HTML | .html | Clean markdown |
| Images | .jpg, .png | OCR with vision model |
| Audio | .mp3, .wav | Transcription |
| ZIP | .zip | Processes contained files |

### Basic Usage

#### Python API
```python
from markitdown import MarkItDown

# Simple conversion
md = MarkItDown()
result = md.convert("document.docx")

# Access content
markdown_text = result.text_content

# With options
md = MarkItDown(
    llm_client=None,      # Optional LLM for enhanced processing
    llm_model=None        # Model name if using LLM
)
```

#### Command Line
```bash
# Install
pip install markitdown

# Convert file
markitdown document.docx > output.md

# Or with output file
markitdown document.docx -o output.md
```

### Word Document Conversion

```python
from markitdown import MarkItDown

md = MarkItDown()

# Convert Word document
result = md.convert("report.docx")

# Output preserves:
# - Headings (as # headers)
# - Bold/italic formatting
# - Lists (bulleted and numbered)
# - Tables (as markdown tables)
# - Hyperlinks

print(result.text_content)
```

**Example Output:**
```markdown
# Annual Report 2024

## Executive Summary

This report summarizes the key achievements and challenges...

### Key Metrics

| Metric | 2023 | 2024 | Change |
|--------|------|------|--------|
| Revenue | $10M | $12M | +20% |
| Users | 50K | 75K | +50% |

## Detailed Analysis

The following sections provide...
```

### Excel Conversion

```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("data.xlsx")

# Each sheet becomes a section
# Data becomes markdown tables
print(result.text_content)
```

**Example Output:**
```markdown
## Sheet1

| Name | Department | Salary |
|------|------------|--------|
| John | Engineering | $80,000 |
| Jane | Marketing | $75,000 |

## Sheet2

| Product | Q1 | Q2 | Q3 | Q4 |
|---------|----|----|----|----|
| Widget A | 100 | 120 | 150 | 180 |
```

### PowerPoint Conversion

```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("presentation.pptx")

# Each slide becomes a section
# Speaker notes included if present
print(result.text_content)
```

**Example Output:**
```markdown
# Slide 1: Company Overview

Our mission is to...

## Key Points
- Innovation first
- Customer focused
- Global reach

---

# Slide 2: Market Analysis

The market opportunity is significant...

**Notes:** Mention the competitor analysis here
```

### PDF Conversion

```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("document.pdf")

# Extracts text content
# Tables converted where detected
print(result.text_content)
```

### Image Conversion (with Vision Model)

```python
from markitdown import MarkItDown
import anthropic

# Use Claude for image description
client = anthropic.Anthropic()

md = MarkItDown(
    llm_client=client,
    llm_model="claude-sonnet-4-20250514"
)

result = md.convert("diagram.png")
print(result.text_content)

# Output: Description of the image content
```

### Batch Conversion

```python
from markitdown import MarkItDown
from pathlib import Path

def batch_convert(input_dir, output_dir):
    """Convert all Office files to Markdown."""
    md = MarkItDown()
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    extensions = ['.docx', '.xlsx', '.pptx', '.pdf']
    
    for ext in extensions:
        for file in input_path.glob(f'*{ext}'):
            try:
                result = md.convert(str(file))
                output_file = output_path / f"{file.stem}.md"
                
                with open(output_file, 'w') as f:
                    f.write(result.text_content)
                
                print(f"Converted: {file.name}")
            except Exception as e:
                print(f"Error converting {file.name}: {e}")

batch_convert('./documents', './markdown')
```

## Best Practices

1. **Check Output Quality**: Review converted Markdown for accuracy
2. **Handle Tables**: Complex tables may need manual adjustment
3. **Preserve Structure**: Use consistent heading levels in source docs
4. **Image Handling**: Consider using vision models for important images
5. **Version Control**: Store converted Markdown in Git for tracking

## Common Patterns

### Document Archive
```python
import os
from datetime import datetime
from markitdown import MarkItDown

def archive_document(doc_path, archive_dir):
    """Convert and archive Office document to Markdown."""
    md = MarkItDown()
    result = md.convert(doc_path)
    
    # Create archive structure
    date_str = datetime.now().strftime('%Y-%m-%d')
    filename = os.path.basename(doc_path)
    base_name = os.path.splitext(filename)[0]
    
    # Save with metadata
    output_content = f"""---
source: {filename}
converted: {date_str}
---

{result.text_content}
"""
    
    output_path = os.path.join(archive_dir, f"{base_name}.md")
    with open(output_path, 'w') as f:
        f.write(output_content)
    
    return output_path
```

### AI-Ready Corpus
```python
from markitdown import MarkItDown
from pathlib import Path
import json

def create_ai_corpus(doc_folder, output_file):
    """Convert documents to JSON corpus for AI training/RAG."""
    md = MarkItDown()
    corpus = []
    
    for doc in Path(doc_folder).glob('**/*'):
        if doc.suffix in ['.docx', '.pdf', '.pptx', '.xlsx']:
            try:
                result = md.convert(str(doc))
                corpus.append({
                    'source': str(doc),
                    'filename': doc.name,
                    'content': result.text_content,
                    'type': doc.suffix[1:]
                })
            except Exception as e:
                print(f"Skipped {doc.name}: {e}")
    
    with open(output_file, 'w') as f:
        json.dump(corpus, f, indent=2)
    
    print(f"Created corpus with {len(corpus)} documents")
    return corpus
```

## Examples

### Example 1: Convert Documentation Suite
```python
from markitdown import MarkItDown
from pathlib import Path

def convert_docs_to_wiki(docs_folder, wiki_folder):
    """Convert all Office docs to markdown wiki structure."""
    md = MarkItDown()
    docs_path = Path(docs_folder)
    wiki_path = Path(wiki_folder)
    
    # Create wiki structure
    wiki_path.mkdir(exist_ok=True)
    
    # Create index
    index_content = "# Documentation Index\n\n"
    
    for doc in sorted(docs_path.glob('**/*.docx')):
        try:
            result = md.convert(str(doc))
            
            # Create relative path in wiki
            rel_path = doc.relative_to(docs_path)
            output_file = wiki_path / rel_path.with_suffix('.md')
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Write markdown
            with open(output_file, 'w') as f:
                f.write(result.text_content)
            
            # Add to index
            link = str(rel_path.with_suffix('.md')).replace('\\', '/')
            index_content += f"- [{doc.stem}]({link})\n"
            
            print(f"Converted: {doc.name}")
            
        except Exception as e:
            print(f"Error: {doc.name} - {e}")
    
    # Write index
    with open(wiki_path / 'index.md', 'w') as f:
        f.write(index_content)

convert_docs_to_wiki('./company_docs', './wiki')
```

### Example 2: Meeting Notes Processor
```python
from markitdown import MarkItDown
import re
from datetime import datetime

def process_meeting_notes(pptx_path):
    """Extract and structure meeting notes from PowerPoint."""
    md = MarkItDown()
    result = md.convert(pptx_path)
    
    # Parse the markdown
    content = result.text_content
    
    # Extract sections
    sections = {
        'attendees': [],
        'agenda': [],
        'decisions': [],
        'action_items': []
    }
    
    current_section = None
    
    for line in content.split('\n'):
        line_lower = line.lower()
        
        if 'attendee' in line_lower or 'participant' in line_lower:
            current_section = 'attendees'
        elif 'agenda' in line_lower:
            current_section = 'agenda'
        elif 'decision' in line_lower:
            current_section = 'decisions'
        elif 'action' in line_lower:
            current_section = 'action_items'
        elif line.strip().startswith(('-', '*', '•')) and current_section:
            sections[current_section].append(line.strip()[1:].strip())
    
    # Generate structured output
    output = f"""# Meeting Notes

**Date:** {datetime.now().strftime('%Y-%m-%d')}
**Source:** {pptx_path}

## Attendees
{chr(10).join('- ' + a for a in sections['attendees'])}

## Agenda
{chr(10).join('- ' + a for a in sections['agenda'])}

## Decisions Made
{chr(10).join('- ' + d for d in sections['decisions'])}

## Action Items
{chr(10).join('- [ ] ' + a for a in sections['action_items'])}
"""
    
    return output

notes = process_meeting_notes('team_meeting.pptx')
print(notes)
```

### Example 3: Excel to Documentation
```python
from markitdown import MarkItDown

def excel_to_data_dictionary(xlsx_path):
    """Convert Excel data model to data dictionary documentation."""
    md = MarkItDown()
    result = md.convert(xlsx_path)
    
    # Add documentation structure
    doc = f"""# Data Dictionary

Generated from: `{xlsx_path}`

{result.text_content}

## Usage Notes

- All tables are derived from the source Excel file
- Review data types and constraints before use
- Contact data team for clarifications

## Change Log

| Date | Change | Author |
|------|--------|--------|
| {datetime.now().strftime('%Y-%m-%d')} | Initial generation | Auto |
"""
    
    return doc

documentation = excel_to_data_dictionary('data_model.xlsx')
with open('data_dictionary.md', 'w') as f:
    f.write(documentation)
```

## Limitations

- Complex formatting may be simplified
- Images are not embedded (use vision model for descriptions)
- Some table structures may not convert perfectly
- Track changes in Word are not preserved
- Comments may not be extracted

## Installation

```bash
pip install markitdown

# For image/audio processing
pip install markitdown[all]

# For specific features
pip install markitdown[images]  # Image OCR
pip install markitdown[audio]   # Audio transcription
```

## Resources

- [GitHub Repository](https://github.com/microsoft/markitdown)
- [PyPI Package](https://pypi.org/project/markitdown/)
- [Supported Formats](https://github.com/microsoft/markitdown#supported-formats)
