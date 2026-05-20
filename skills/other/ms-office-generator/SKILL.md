---
name: ms-office-generator
description: "Generate Microsoft Office documents (.docx, .pptx) from markdown or structured data. Applies 45Black Saville Edition branding when appropriate. Use for: converting markdown to Word, creating branded documents, generating reports, creating brand guidelines. Triggers on: create docx, word document, convert to word, generate office doc, brand guidelines docx."
version: "1.0"
tier: utility
token_budget: 1800
requires: []
---

# MS Office Document Generator

Convert markdown to Microsoft Office documents (.docx, .pptx) with optional 45Black Saville Edition branding.

## When To Use

**Primary triggers:**
- User wants to convert markdown to .docx
- User requests "create word document" or "generate docx"
- Converting brand guidelines or documentation to Office format
- Creating reports or specifications that need Word format
- User mentions: "word doc", "office document", "docx", "pptx"

**Context indicators:**
- Markdown files that need professional formatting
- Brand guidelines that need to be distributed as .docx
- Documentation intended for non-technical stakeholders
- Reports that need to match corporate templates

**Don't use when:**
- PDFs are more appropriate (use pdf-generator skill instead)
- Plain text is sufficient
- Content stays in markdown format
- User specifically requests other formats (HTML, LaTeX, etc.)

## Prerequisites

Ensure python-docx is installed:
```bash
pip install python-docx python-docx-template
```

For PowerPoint generation:
```bash
pip install python-pptx
```

## Core Capabilities

### 1. Markdown to DOCX Conversion

**Basic conversion script**:
```python
#!/usr/bin/env python3
"""
Convert markdown to Word document with basic formatting.
Usage: python md_to_docx.py input.md output.docx [--branded]
"""

from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import re
import sys
import argparse

# Saville Edition colors (v4.3)
COLORS = {
    'saville_blue': RGBColor(21, 101, 192),
    'saville_purple': RGBColor(123, 31, 162),
    'saville_teal': RGBColor(46, 139, 139),
    'saville_green': RGBColor(74, 124, 89),
    'saville_coral': RGBColor(230, 81, 0),
    'saville_orange': RGBColor(245, 124, 0),
    'charcoal': RGBColor(26, 26, 26),
    'dark_gray': RGBColor(66, 66, 66),
}

def apply_saville_branding(doc):
    """Apply 45Black Saville Edition branding to document."""
    # Set default font to IBM Plex Sans
    style = doc.styles['Normal']
    font = style.font
    font.name = 'IBM Plex Sans'
    font.size = Pt(11)
    font.color.rgb = COLORS['dark_gray']

    # Heading 1 - Bold, Charcoal
    h1_style = doc.styles['Heading 1']
    h1_style.font.name = 'IBM Plex Sans'
    h1_style.font.size = Pt(28)
    h1_style.font.bold = True
    h1_style.font.color.rgb = COLORS['charcoal']

    # Heading 2 - SemiBold, Saville Blue
    h2_style = doc.styles['Heading 2']
    h2_style.font.name = 'IBM Plex Sans'
    h2_style.font.size = Pt(20)
    h2_style.font.bold = True
    h2_style.font.color.rgb = COLORS['saville_blue']

    # Heading 3 - SemiBold, Charcoal
    h3_style = doc.styles['Heading 3']
    h3_style.font.name = 'IBM Plex Sans'
    h3_style.font.size = Pt(16)
    h3_style.font.bold = True
    h3_style.font.color.rgb = COLORS['charcoal']

def parse_markdown(md_text, doc, branded=False):
    """Parse markdown and add to Word document."""
    lines = md_text.split('\n')

    for line in lines:
        line = line.rstrip()

        # Skip empty lines
        if not line:
            continue

        # Heading 1
        if line.startswith('# '):
            doc.add_heading(line[2:], level=1)
        # Heading 2
        elif line.startswith('## '):
            doc.add_heading(line[3:], level=2)
        # Heading 3
        elif line.startswith('### '):
            doc.add_heading(line[4:], level=3)
        # Heading 4
        elif line.startswith('#### '):
            doc.add_heading(line[5:], level=4)
        # Bullet list
        elif line.startswith('- ') or line.startswith('* '):
            doc.add_paragraph(line[2:], style='List Bullet')
        # Numbered list
        elif re.match(r'^\d+\. ', line):
            text = re.sub(r'^\d+\. ', '', line)
            doc.add_paragraph(text, style='List Number')
        # Bold text
        elif '**' in line:
            p = doc.add_paragraph()
            parts = re.split(r'\*\*(.*?)\*\*', line)
            for i, part in enumerate(parts):
                if i % 2 == 0:  # Normal text
                    p.add_run(part)
                else:  # Bold text
                    p.add_run(part).bold = True
        # Code block marker (ignore)
        elif line.startswith('```'):
            continue
        # Regular paragraph
        else:
            doc.add_paragraph(line)

def convert_md_to_docx(md_file, docx_file, branded=False):
    """Convert markdown file to Word document."""
    # Read markdown
    with open(md_file, 'r', encoding='utf-8') as f:
        md_text = f.read()

    # Create document
    doc = Document()

    # Apply branding if requested
    if branded:
        apply_saville_branding(doc)

    # Parse markdown
    parse_markdown(md_text, doc, branded)

    # Save document
    doc.save(docx_file)
    print(f"✓ Converted {md_file} → {docx_file}")
    if branded:
        print("  Applied Saville Edition branding")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert markdown to Word document')
    parser.add_argument('input', help='Input markdown file')
    parser.add_argument('output', help='Output docx file')
    parser.add_argument('--branded', action='store_true', help='Apply Saville Edition branding')

    args = parser.parse_args()
    convert_md_to_docx(args.input, args.output, args.branded)
```

### 2. Brand Guidelines Generator

**For 45Black brand guidelines specifically**:
```python
#!/usr/bin/env python3
"""
Generate 45Black Brand Guidelines as a Word document.
Usage: python brand_guidelines_to_docx.py v4.3.md output.docx
"""

from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

def create_brand_guidelines_docx(md_file, output_file):
    """Create branded Word doc from brand guidelines markdown."""
    doc = Document()

    # Set up Saville Edition styles
    # ... (use apply_saville_branding function from above)

    # Add custom table style for color palette
    # Add sections with appropriate formatting

    doc.save(output_file)
    print(f"✓ Created brand guidelines: {output_file}")
```

### 3. Template-Based Generation

For complex documents, use python-docx-template:
```python
from docxtpl import DocxTemplate

doc = DocxTemplate("template.docx")
context = {
    'company_name': '45Black Limited',
    'date': '14 January 2026',
    'items': [
        {'name': 'Item 1', 'description': 'Description 1'},
        {'name': 'Item 2', 'description': 'Description 2'},
    ]
}
doc.render(context)
doc.save("generated_document.docx")
```

## Usage Patterns

### Pattern 1: Quick Markdown Conversion
```bash
# Basic conversion
python md_to_docx.py README.md README.docx

# With Saville branding
python md_to_docx.py README.md README.docx --branded
```

### Pattern 2: Brand Guidelines Generation
```bash
# Convert v4.3 brand guidelines to Word
python brand_guidelines_to_docx.py \
  ~/Downloads/_TRIAGE/To_SharePoint_Business/45black_Brand_Guidelines_v4.3.md \
  ~/Downloads/_TRIAGE/To_SharePoint_Business/45black_Brand_Guidelines_v4.3.docx
```

### Pattern 3: Batch Conversion
```bash
# Convert all markdown files in directory
for md in *.md; do
  python md_to_docx.py "$md" "${md%.md}.docx" --branded
done
```

## Integration with Gemini CLI

This skill works with both Claude Code and Gemini CLI through the unified skills library at `~/.skillz/`.

**For Gemini CLI users**, ensure the skillz extension is installed:
```bash
gemini extensions install https://github.com/intellectronica/gemini-cli-skillz
```

## Accessibility Compliance

When generating branded documents:
- ✅ Use Charcoal (#1A1A1A) for body text
- ✅ Use Saville Blue (#1565C0) for headings (sufficient contrast on white)
- ❌ **Never** use Saville Blue text on Charcoal backgrounds
- ✅ Ensure all colors meet WCAG AA standards (4.5:1)

## Output Quality Checklist

Before delivering generated documents:
- [ ] IBM Plex Sans font applied (or system fallback noted)
- [ ] Heading hierarchy is logical (H1 → H2 → H3)
- [ ] Colors match Saville Edition v4.3 palette
- [ ] Tables and lists are properly formatted
- [ ] Document metadata is set (title, author, company)
- [ ] File is saved in location user specified

## Troubleshooting

**Issue**: "IBM Plex Sans not found"
**Solution**: Font will fall back to system default. User can manually change font in Word.

**Issue**: "python-docx not installed"
**Solution**: Run `pip install python-docx python-docx-template`

**Issue**: "Complex markdown not converting properly"
**Solution**: Simplify markdown or use manual formatting in Word after conversion.

## Related Skills

- `apply-saville.SKILL.md` - For web-based Saville Edition implementation
- `pdf-generator` (if available) - For PDF generation from documents
- `output-verification.SKILL.md` - For quality checking generated documents

## Version History

- **1.0** (2026-01-14) - Initial release
  - Markdown to DOCX conversion
  - Saville Edition branding support
  - Brand guidelines generator template
  - WCAG AA compliance checks

## Examples

### Example 1: Convert Brand Guidelines
```bash
cd ~/Downloads/_TRIAGE/To_SharePoint_Business/
python md_to_docx.py 45black_Brand_Guidelines_v4.3.md 45black_Brand_Guidelines_v4.3.docx --branded
```

### Example 2: Create Meeting Notes
```bash
python md_to_docx.py meeting-notes-2026-01-14.md meeting-notes.docx
```

### Example 3: Generate Branded Report
```python
# Custom script for specific report format
from docx import Document
from docx.shared import RGBColor, Pt

doc = Document()

# Add title page with Saville Blue
title = doc.add_paragraph()
title.add_run('45Black Consulting Report').bold = True
title.runs[0].font.size = Pt(32)
title.runs[0].font.color.rgb = RGBColor(21, 101, 192)

# Add content sections
# ...

doc.save('report.docx')
```

## Notes

- This skill requires Python 3.7+ and python-docx library
- For PowerPoint generation, see separate PPTX examples
- For Excel generation, use `openpyxl` or `xlsxwriter` libraries
- Template files should be stored in `~/Projects/45black/templates/`
