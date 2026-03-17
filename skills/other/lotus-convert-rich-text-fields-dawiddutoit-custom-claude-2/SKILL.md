---
name: lotus-convert-rich-text-fields
description: |
  Converts Lotus Notes rich text fields to standard formats (HTML, markdown, plain text).
  Use when migrating formatted content, extracting text styling and formatting,
  handling embedded objects (images, attachments, tables), or preparing rich text data
  for new systems.
allowed-tools:
  - Read
  - Bash
  - Grep
---

Works with rich text content extraction, format conversion, embedded media handling, and formatting preservation strategies.
# Convert Lotus Notes Rich Text Fields

## Table of Contents

**Quick Start** → [What Is This](#purpose) | [When to Use](#when-to-use) | [Simple Example](#examples)

**How to Implement** → [Step-by-Step](#instructions) | [Expected Outcomes](#quick-start)

**Reference** → [Requirements](#requirements) | [Related Skills](#see-also)

## Purpose

Lotus Notes rich text fields store complex formatted content including bold, italic, colors, fonts, tables, embedded images, and attachments. These formats aren't compatible with modern systems. This skill guides you through extracting and converting this rich content to standard formats (HTML, markdown, or plain text) while preserving important information and maintaining usability.

## When to Use

Use this skill when you need to:

- **Migrate formatted content** - Convert rich text fields to modern formats (HTML, markdown, plain text)
- **Extract text styling and formatting** - Preserve bold, italic, fonts, colors, and structure
- **Handle embedded objects** - Process images, attachments, and tables within rich text
- **Prepare data for new systems** - Ensure rich text data is compatible with target platforms
- **Assess formatting complexity** - Determine which formatting needs to be preserved vs. simplified
- **Validate conversion quality** - Test that converted content maintains critical information

This skill is essential for data migration projects where Lotus Notes rich text fields contain important formatted information that must be preserved.

## Quick Start

To convert rich text fields:

1. Identify all rich text fields in your NSF database
2. Assess formatting complexity (simple text vs. tables/images/embedded objects)
3. Choose target format (HTML for maximum fidelity, markdown for readability, plain text for simplicity)
4. Implement extraction and conversion logic
5. Test with real data to validate formatting
6. Handle edge cases: embedded images, broken formatting, very long content
7. Validate output quality and completeness

## Instructions

### Step 1: Identify Rich Text Fields

Locate all rich text fields in your Lotus Notes database:

**Search for:**
- Form definitions with field type "RichText" or "RT"
- Documentation listing rich text usage
- Backend code that creates or modifies rich text fields

**Document for each field:**
- Field name and form it appears on
- What content does it store? (notes, descriptions, comments, documentation)
- How important is formatting? (critical vs. nice-to-have)
- Typical content size (small notes vs. large documents)
- Do documents contain embedded images or attachments?
- Are tables used?

Example inventory:

```
Form: Order
  - NotesField (RichText)
    Purpose: Internal notes about order
    Formatting: Bold, italics, sometimes tables
    Images: Occasionally (scanned receipts)
    Average size: 1-5 KB

Form: ComplianceDocument
  - DocumentContent (RichText)
    Purpose: Official compliance documentation
    Formatting: Extensive (multi-level headers, formatted lists, tables)
    Images: Many (regulatory documents, photographs)
    Average size: 100-500 KB
    Critical: Yes—formatting must be preserved
```

### Step 2: Analyze Formatting Requirements

Assess how much formatting needs to be preserved:

**For each rich text field, determine:**

1. **Formatting complexity level:**
   - **Simple** (Bold, italic, underline only)
     → Markdown or simple HTML is sufficient
   - **Moderate** (Multiple fonts, colors, structured lists)
     → HTML with CSS is needed
   - **Complex** (Tables, nested lists, images, special formatting)
     → Full HTML with embedded media handling

2. **Content types present:**
   - Plain text only
   - Text with basic formatting
   - Tables or structured data
   - Embedded images
   - Attached files
   - Multi-level lists or outlines

3. **Target system requirements:**
   - Can target system handle HTML?
   - Is markdown supported?
   - Must formatting be stripped?
   - Can target system store images/attachments?

Example assessment:

```
Field: OrderNotes
  Formatting complexity: Simple
  Content types: Text, bold, italics
  Target system: Supports HTML
  Strategy: Convert to HTML with basic tags (strong, em, p)

Field: TechnicalSpec
  Formatting complexity: Complex
  Content types: Text, headers, code blocks, images, tables
  Target system: Markdown rendering engine
  Strategy: Convert to markdown with inline images as base64
```

### Step 3: Choose Conversion Strategy

Select the appropriate target format:

**HTML (Maximum Fidelity):**
- Preserves all formatting, fonts, colors
- Can embed images directly or store as data URIs
- Target system must support HTML rendering
- Best for: Complex formatted documents

```html
<p><strong>Order Status:</strong> <em>Approved</em></p>
<table>
  <tr>
    <td>Item 1</td>
    <td>$100</td>
  </tr>
</table>
```

**Markdown (Readable & Portable):**
- Simplifies formatting to essential elements
- Easy to version control and diff
- Works in many modern systems
- Best for: Documentation, notes with moderate formatting

```markdown
**Order Status:** _Approved_

| Item | Price |
|------|-------|
| Item 1 | $100 |
```

**Plain Text (Simplest):**
- Removes all formatting
- Maximum compatibility
- Loss of structure
- Best for: Legacy systems, when formatting isn't important

```
Order Status: Approved

Item 1 - $100
```

### Step 4: Extract Rich Text Content

Get the raw rich text data from NSF documents:

**For small migrations**, manually export:
1. Open NSF in Lotus Notes Designer
2. Use "Export" to save documents as XML or text files
3. Extract rich text content from export

**For larger data sets**, programmatically extract:

```python
# If using Domino HTTP API or LotusScript export
def extract_rich_text_from_domino(doc_id: str, field_name: str) -> str:
    """
    Extract rich text content from Domino document via HTTP API.

    Returns raw rich text markup (RTF-like format from Lotus).
    """
    # This depends on your Domino API access
    # Typically returns something like:
    # {RTFFIELD "OrderNotes" "This is a note with \f formatting"}
    pass
```

**Understanding Lotus Rich Text format:**

Lotus stores rich text in a proprietary binary format. When exported, it may appear as:
- RTF (Rich Text Format)
- MIME with embedded formatting
- Custom Lotus markup

Example exported format:

```
{\rtf1\ansi\ansicpg1252
{\fonttbl\f0\fswiss Helvetica;}
{\colortbl;\red0\green0\blue0;}
\uc1\pard\plain\deftab720\f0\fs20
Order Status: \b Approved\b0\par
Items:\par
\trowd\trgaph108\trleft-108\trbrdrl\brdrs
\trbrdrt\brdrs\trbrdrb\brdrs\trbrdrr\brdrs
\trbrdrh\brdrs\trbrdrv\brdrs\tbrdrva\brdrs
\clbrdrl\brdrs\clbrdrt\brdrs\clbrdrb\brdrs
\clbrdrr\brdrs \cellx1440\f0\fs20 Item 1\cell
\cellx2880\f0\fs20 $100\cell\row\pard
\plain\f0\fs20\par}
```

### Step 5: Implement Conversion Functions

Create converters for your chosen format:

**Example: Convert to HTML**

```python
from typing import Optional
import re
import html as html_module

class RichTextConverter:
    """Convert Lotus Notes rich text to HTML."""

    @staticmethod
    def rtf_to_html(rtf_content: str) -> str:
        """
        Convert RTF (Rich Text Format) to HTML.

        This is a simplified converter. For production, use a library
        like 'striprtf' or 'pylibreoffice'.
        """
        # Remove RTF control sequences
        html = re.sub(r'\\\*?[a-z]+\d*[ ]?', '', rtf_content)

        # Clean up curly braces
        html = html.replace('{', '').replace('}', '')

        # Convert formatting codes
        replacements = {
            r'\\b\s': '<strong>',      # Bold start
            r'\\b0': '</strong>',       # Bold end
            r'\\i\s': '<em>',           # Italic start
            r'\\i0': '</em>',           # Italic end
            r'\\par': '</p><p>',        # Paragraph break
        }

        for pattern, replacement in replacements.items():
            html = re.sub(pattern, replacement, html)

        # Wrap in paragraph tags
        html = f'<p>{html}</p>'

        # Escape any raw HTML characters
        html = html_module.escape(html)

        return html

    @staticmethod
    def lotus_markup_to_html(content: str) -> str:
        """
        Convert Lotus-exported markup to HTML.

        Handles common Lotus text field exports.
        """
        # Replace common formatting markers
        html = content.replace('[B]', '<strong>')
        html = html.replace('[/B]', '</strong>')
        html = html.replace('[I]', '<em>')
        html = html.replace('[/I]', '</em>')
        html = html.replace('[U]', '<u>')
        html = html.replace('[/U]', '</u>')

        # Handle line breaks
        html = html.replace('\n', '<br/>')

        # Wrap paragraphs
        lines = html.split('<br/>')
        html = ''.join(f'<p>{line}</p>' for line in lines if line.strip())

        return html

    @staticmethod
    def html_to_markdown(html_content: str) -> str:
        """
        Convert HTML to Markdown.

        For production, use 'markdownify' or 'html2text' library.
        """
        markdown = html_content

        # Convert HTML tags to markdown
        replacements = {
            r'<strong>(.*?)</strong>': r'**\1**',
            r'<em>(.*?)</em>': r'*\1*',
            r'<u>(.*?)</u>': r'__\1__',
            r'<h1>(.*?)</h1>': r'# \1\n',
            r'<h2>(.*?)</h2>': r'## \1\n',
            r'<h3>(.*?)</h3>': r'### \1\n',
            r'<p>(.*?)</p>': r'\1\n\n',
            r'<li>(.*?)</li>': r'- \1\n',
            r'<br\s*/?>', r'\n',
        }

        for pattern, replacement in replacements.items():
            markdown = re.sub(pattern, replacement, markdown, flags=re.IGNORECASE)

        # Remove remaining HTML tags
        markdown = re.sub(r'<[^>]+>', '', markdown)

        return markdown.strip()
```

**Using existing libraries (recommended for production):**

```python
# Option 1: Use striprtf for RTF conversion
from striprtf.rtf import rtf_to_text

def convert_rtf_field(rtf_content: str) -> str:
    """Extract plain text from RTF content."""
    return rtf_to_text(rtf_content)

# Option 2: Use markdownify for HTML to markdown
from markdownify import markdownify as md_convert

def convert_html_to_markdown(html: str) -> str:
    """Convert HTML to markdown."""
    return md_convert(html)

# Option 3: Use html2text for another HTML→markdown approach
import html2text

def convert_with_html2text(html: str) -> str:
    h = html2text.HTML2Text()
    h.ignore_links = False
    return h.handle(html)
```

### Step 6: Handle Embedded Media

Manage images and attachments in rich text:

**Strategy 1: Embed as base64 (smaller documents)**

```python
import base64
from pathlib import Path

def embed_image_as_data_uri(image_path: str) -> str:
    """Convert image to base64 data URI for embedding in HTML."""
    with open(image_path, 'rb') as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')

    # Determine MIME type
    ext = Path(image_path).suffix.lower()
    mime_types = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.svg': 'image/svg+xml',
    }
    mime_type = mime_types.get(ext, 'application/octet-stream')

    return f'data:{mime_type};base64,{image_data}'

def html_with_embedded_images(html: str, image_dir: str) -> str:
    """Replace image paths in HTML with embedded base64 data URIs."""
    def replace_src(match):
        src = match.group(1)
        if src.startswith('data:'):
            return match.group(0)  # Already embedded

        image_path = Path(image_dir) / src
        if image_path.exists():
            data_uri = embed_image_as_data_uri(str(image_path))
            return f'<img src="{data_uri}"'
        return match.group(0)

    return re.sub(r'<img\s+src="([^"]+)"', replace_src, html)
```

**Strategy 2: Save files separately and link (larger documents)**

```python
import uuid

def extract_and_link_attachments(
    html: str,
    attachments: list,
    output_dir: str
) -> str:
    """
    Extract attachments and replace with file links.

    Args:
        html: HTML content with embedded references
        attachments: List of attachment data
        output_dir: Where to save extracted files

    Returns:
        HTML with file links
    """
    for attachment in attachments:
        file_name = attachment['filename']
        file_data = attachment['data']
        unique_name = f"{uuid.uuid4()}_{file_name}"

        # Save file
        output_path = Path(output_dir) / unique_name
        output_path.write_bytes(file_data)

        # Replace reference in HTML
        html = html.replace(f'[ATTACHMENT:{file_name}]',
                          f'<a href="/attachments/{unique_name}">{file_name}</a>')

    return html
```

### Step 7: Validate and Test Conversion

Verify the conversion preserves important information:

```python
def validate_conversion(
    original_content: str,
    converted_content: str,
    format_type: str
) -> list:
    """
    Check conversion quality.

    Returns list of issues found (empty = valid).
    """
    issues = []

    # Check content length difference (warn if >50% lost)
    original_len = len(original_content)
    converted_len = len(converted_content)
    loss_pct = ((original_len - converted_len) / original_len) * 100

    if loss_pct > 50:
        issues.append(f"Significant content loss: {loss_pct:.1f}%")

    # For HTML, check for unclosed tags
    if format_type == 'html':
        open_tags = len(re.findall(r'<([a-z]+)>', converted_content))
        close_tags = len(re.findall(r'</([a-z]+)>', converted_content))
        if open_tags != close_tags:
            issues.append(f"Unclosed HTML tags: {open_tags} open, {close_tags} closed")

    # Check for orphaned formatting markers
    if '[' in converted_content or '{' in converted_content:
        issues.append("Unconverted formatting markers detected")

    return issues

# Example usage
issues = validate_conversion(lotus_rtf, converted_html, 'html')
if issues:
    print("Conversion issues found:")
    for issue in issues:
        print(f"  - {issue}")
else:
    print("Conversion validation passed")
```

## Examples

### Example 1: Simple Notes Field Conversion

**Lotus Notes Field Content:**

```
Order approved by Manager.
Important: Rush delivery requested.
Contact supplier: John Smith (john@supplier.com)
```

**HTML Output:**

```html
<p>Order approved by Manager.</p>
<p><strong>Important:</strong> Rush delivery requested.</p>
<p>Contact supplier: John Smith (john@supplier.com)</p>
```

**Markdown Output:**

```markdown
Order approved by Manager.

**Important:** Rush delivery requested.

Contact supplier: John Smith (john@supplier.com)
```

### Example 2: Complex Document with Table

**Lotus Notes RTF Content:**

```rtf
{\rtf1\ansi{\fonttbl\f0\fswiss Helvetica;}
{\colortbl;\red255\green0\blue0;}
{\*\listtable{\list\listtemplateid1{\listlevel\levelnfc23\levelnfcn23
\levelfollow0\levelstartat1\levelspace0\levelindent0{\*\levelmarker \{bullet\}}{\leveltext \'01\bullet;}}}
\margl1440\margr1440\vieww11900\viewh8605\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\pardirnatural\partightenfactor100
\f0\fs24 \cf0 {\*\listoverride\listid1\levelnfc23\levelnfcn23\levelstartat1\levelspace0\listindent0{\*\levelmarker \{bullet\}}{\leveltext \'01\bullet;}{\levelnumbers;}}\ls1
{\listtext \bullet }Item 1: Description\par
{\listtext \bullet }Item 2: Description\par
\par
{\*\fldinst HYPERLINK "https://example.com"}{\fldrslt https://example.com}\par}
```

**HTML Output:**

```html
<ul>
  <li>Item 1: Description</li>
  <li>Item 2: Description</li>
</ul>
<p><a href="https://example.com">https://example.com</a></p>
```

**Markdown Output:**

```markdown
- Item 1: Description
- Item 2: Description

[https://example.com](https://example.com)
```

### Example 3: Document with Embedded Image

**Conversion Code:**

```python
# Export rich text field with embedded image
lotus_doc = get_lotus_document("Order-123")
rich_text_field = lotus_doc['DocumentNotes']
embedded_image = lotus_doc.attachments[0]

# Convert to HTML with embedded image
html = convert_rtf_to_html(rich_text_field)
html_with_image = embed_image_as_data_uri_in_html(html, embedded_image)

# Result: HTML with base64-encoded PNG embedded
print(html_with_image)
# Output:
# <p>Order documentation:</p>
# <img src="data:image/png;base64,iVBORw0KGgoAAAANS..."/>
```

## Requirements

- **For RTF parsing**: `striprtf` library
  - Install: `pip install striprtf`

- **For HTML to Markdown**: `markdownify` or `html2text`
  - Install: `pip install markdownify` or `pip install html2text`

- **For image handling**: PIL/Pillow for image operations
  - Install: `pip install Pillow`

- **Development tools**: Text editor or IDE for testing conversions
  - Recommended: VS Code, PyCharm

- **Source data access**: Method to extract rich text from Lotus Notes
  - Lotus Notes Designer export
  - Domino HTTP API
  - Direct NSF file export tools

## See Also

- [lotus-analyze-nsf-structure](../lotus-analyze-nsf-structure/SKILL.md) - Understanding field types in NSF databases
- [lotus-migration](../lotus-migration/SKILL.md) - Overall migration approach
- [lotus-replace-odbc-direct-writes](../lotus-replace-odbc-direct-writes/SKILL.md) - API patterns for data operations
