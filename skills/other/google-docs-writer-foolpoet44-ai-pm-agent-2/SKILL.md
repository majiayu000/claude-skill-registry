---
name: google-docs-writer
description: Google Docs document creation and formatting from Markdown. Use when converting Markdown to Google Docs, formatting documents for sharing, or creating professional PM deliverables. Triggers on "Google Docs", "export to Docs", "share document", "format for stakeholders".
allowed-tools: Read, Write, Edit
model: inherit
---

# Google Docs Writer Skill - Professional Document Creation

This Skill helps convert Markdown documents (PRDs, User Stories, Idea Reports) into well-formatted Google Docs for sharing with stakeholders.

## When to Use This Skill

Use this Skill when you need to:
- Convert Markdown documents to Google Docs
- Format PM deliverables professionally
- Create shareable stakeholder documents
- Apply consistent styling and branding
- Generate presentation-ready materials

## Core Process

### Step 1: Input Analysis

**Required Inputs:**
- Markdown document (PRD, User Stories, Idea Report)
- Document type (determines formatting)
- Target audience (affects style/detail level)

**Optional:**
- Company branding guidelines
- Custom styles/templates
- Access permissions

### Step 2: Document Type Templates

#### PRD Document Style

**Formatting:**
- Title: 24pt, Bold, Dark Blue (#1A237E)
- H1 (##): 18pt, Bold, Dark Gray (#424242)
- H2 (###): 14pt, Bold, Medium Gray (#616161)
- H3 (####): 12pt, Bold, Light Gray (#757575)
- Body: 11pt, Normal, Black
- Code: 10pt, Courier New, Light Gray Background
- Tables: Bordered, Header Row Shaded (#E3F2FD)
- Lists: Bullet points with proper indentation

**Page Setup:**
- Margins: 1 inch all sides
- Line Spacing: 1.15
- Page Numbers: Bottom right
- Header: Document title and version
- Footer: Confidential notice (if applicable)

#### User Story Document Style

**Formatting:**
- Epic Title: 20pt, Bold, Purple (#6A1B9A)
- Story Title: 14pt, Bold, Dark Blue (#1976D2)
- Story ID: 12pt, Bold, Monospace, Light Blue (#42A5F5)
- Acceptance Criteria: Indented, Gray Background (#F5F5F5)
- Tasks: Checkboxes, 11pt
- Priority Labels: Color-coded badges
  - P0: Red background (#FFCDD2)
  - P1: Orange background (#FFE0B2)
  - P2: Yellow background (#FFF9C4)
  - P3: Green background (#C8E6C9)

#### Idea Validation Report Style

**Formatting:**
- Title: 22pt, Bold, Teal (#00796B)
- Section Headers: 16pt, Bold, Dark Teal (#004D40)
- Subsections: 13pt, Bold, Medium Teal (#00897B)
- Callout Boxes: Light Teal Background (#B2DFDB)
- Key Metrics: Large Bold Numbers, Teal Color
- Tables: Alternating row colors for readability

### Step 3: Markdown to Google Docs Conversion

**Current Limitation:**
Google Drive MCP is not currently configured in this project. This Skill provides the framework and instructions for when MCP is available.

**When Google Drive MCP is Available:**

```python
# Pseudocode for conversion process

def markdown_to_google_docs(markdown_content, doc_type):
    """
    Convert Markdown to Google Docs

    Args:
        markdown_content: String with Markdown formatting
        doc_type: 'prd' | 'userstory' | 'idea' | 'general'

    Returns:
        google_docs_url: Shareable link to created document
    """

    # Step 1: Parse Markdown
    parsed = parse_markdown(markdown_content)

    # Step 2: Apply style template
    if doc_type == 'prd':
        style = PRD_STYLE_TEMPLATE
    elif doc_type == 'userstory':
        style = USERSTORY_STYLE_TEMPLATE
    elif doc_type == 'idea':
        style = IDEA_STYLE_TEMPLATE
    else:
        style = DEFAULT_STYLE_TEMPLATE

    # Step 3: Create Google Doc
    doc = create_google_doc(title, style)

    # Step 4: Convert elements
    for element in parsed:
        if element.type == 'heading':
            add_heading(doc, element.text, element.level, style)
        elif element.type == 'paragraph':
            add_paragraph(doc, element.text, style)
        elif element.type == 'table':
            add_table(doc, element.data, style)
        elif element.type == 'list':
            add_list(doc, element.items, style)
        elif element.type == 'code':
            add_code_block(doc, element.code, style)

    # Step 5: Add metadata
    add_header(doc, title, version)
    add_footer(doc, confidential_notice)
    add_toc(doc) # Table of Contents

    # Step 6: Set permissions
    set_sharing(doc, permissions)

    # Step 7: Return URL
    return doc.url
```

### Step 4: Formatting Guidelines

#### Tables
```markdown
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data 1   | Data 2   | Data 3   |
```

**Google Docs Format:**
- Header row: Bold, Shaded background
- Borders: All cells bordered
- Alignment: Left for text, Right for numbers
- Alt row shading for readability

#### Lists

**Markdown:**
```markdown
- Item 1
  - Sub-item 1.1
  - Sub-item 1.2
- Item 2
```

**Google Docs Format:**
- Bullet style: Filled circle for level 1
- Bullet style: Empty circle for level 2
- Bullet style: Square for level 3
- Proper indentation (0.5 inch per level)

#### Code Blocks

**Markdown:**
```markdown
```python
def example():
    return "code"
```
```

**Google Docs Format:**
- Font: Courier New or Consolas
- Background: Light gray (#F5F5F5)
- Border: 1pt solid gray
- Padding: 0.1 inch
- Preserve line breaks and indentation

#### Callout Boxes

**Markdown:**
```markdown
> **Important Note:**
> This is a callout
```

**Google Docs Format:**
- Background: Light color based on type
  - Info: Blue (#E3F2FD)
  - Warning: Yellow (#FFF9C4)
  - Success: Green (#C8E6C9)
  - Error: Red (#FFCDD2)
- Left border: 4pt solid, darker shade
- Padding: 0.15 inch
- Italic text for emphasis

### Step 5: Document Structure

**Every Document Should Include:**

1. **Cover Page** (for formal documents)
   - Title (large, centered)
   - Subtitle/Product name
   - Version number
   - Author name(s)
   - Date
   - Confidentiality notice
   - Company logo (if available)

2. **Table of Contents** (for docs >5 pages)
   - Auto-generated from headings
   - Clickable links
   - Page numbers

3. **Document Body**
   - Formatted per templates above
   - Consistent styling throughout
   - Clear hierarchy

4. **Appendix** (if needed)
   - Supporting materials
   - References
   - Glossary

### Step 6: Accessibility

**Ensure Documents Are:**
- [ ] Screen reader friendly (proper heading structure)
- [ ] Alt text for images
- [ ] High contrast (WCAG AA minimum)
- [ ] Readable font size (min 11pt)
- [ ] Clear link text (not "click here")
- [ ] Table headers defined
- [ ] List structure preserved

### Step 7: Sharing and Permissions

**Permission Levels:**
- **Viewer**: Can view and comment (stakeholders, external)
- **Commenter**: Can suggest edits (reviewers)
- **Editor**: Can edit directly (team members)

**Sharing Best Practices:**
- Set appropriate default permissions
- Add expiration dates for sensitive docs
- Require sign-in for confidential materials
- Track version history
- Enable notifications for changes

## Workaround (Until Google Drive MCP Available)

**Current Approach:**

1. **Generate Clean Markdown**
   - Well-formatted with proper headings
   - Tables using Markdown syntax
   - Clear section breaks

2. **Provide Conversion Instructions**
   ```
   To convert this Markdown to Google Docs:

   Option 1: Direct Import
   1. Save this as a .md file
   2. Go to Google Docs
   3. File → Open → Upload → Select .md file
   4. Google Docs will auto-convert
   5. Apply formatting manually using styles above

   Option 2: Use Pandoc
   1. Install Pandoc: https://pandoc.org/
   2. Run: pandoc input.md -o output.docx
   3. Upload .docx to Google Drive
   4. Open with Google Docs

   Option 3: Copy-Paste with Formatting
   1. Copy Markdown content
   2. Paste into Docs
   3. Use Docs formatting toolbar to style
   ```

3. **Provide Formatting Checklist**
   ```
   Formatting Checklist:
   - [ ] Apply heading styles (Heading 1, 2, 3)
   - [ ] Format tables with borders and header shading
   - [ ] Convert code blocks to monospace font with background
   - [ ] Add bullet points to lists
   - [ ] Bold important terms
   - [ ] Add page numbers
   - [ ] Insert table of contents
   - [ ] Add cover page (for PRDs)
   - [ ] Set sharing permissions
   ```

4. **Export-Ready Markdown**
   - Use standard Markdown (not GitHub-flavored)
   - Avoid complex formatting (nested tables, etc.)
   - Use simple, compatible syntax
   - Include clear section breaks

## Output Template

```markdown
---
DOCUMENT METADATA:
- Type: [PRD | User Stories | Idea Report]
- Title: [Document Title]
- Version: [1.0]
- Author: [Name]
- Date: [YYYY-MM-DD]
- Status: [Draft | Review | Final]
---

# [Document Title]

**Version:** [1.0]
**Author:** [Name]
**Date:** [Date]
**Status:** [Draft]

---

## Table of Contents

1. [Section 1](#section-1)
2. [Section 2](#section-2)
3. [Section 3](#section-3)

---

## Section 1

[Content]

### Subsection 1.1

[Content]

## Section 2

[Content with table]

| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data     | Data     | Data     |

## Section 3

[Content with list]

- Item 1
  - Sub-item 1.1
  - Sub-item 1.2
- Item 2

---

**Document End**

---

## Conversion Instructions

[Include steps for converting to Google Docs]

## Formatting Checklist

[Include checklist as shown above]
```

## Best Practices

### For Stakeholder Documents
✅ **Do:**
- Use executive summary at top
- Include visual elements (tables, charts)
- Highlight key metrics
- Use clear, non-technical language
- Add table of contents for long docs
- Include next steps/action items

❌ **Don't:**
- Use excessive technical jargon
- Create walls of text
- Skip visual hierarchy
- Forget to define acronyms
- Ignore branding guidelines

### For Team Documents
✅ **Do:**
- Be comprehensive and detailed
- Include technical specifications
- Link to related docs
- Use consistent terminology
- Version control clearly

❌ **Don't:**
- Assume everyone has context
- Skip implementation details
- Forget to update status
- Leave questions unanswered

## Future Enhancement

When Google Drive MCP is configured:

```bash
# Install Google Drive MCP
# Add to Claude Code configuration
# Test authentication
# Implement automated conversion
# Set up style templates
# Configure sharing permissions
```

Then this Skill will be fully automated.

## Integration Points

This Skill works with:
- **prd-agent**: Formats PRD documents
- **userstory-agent**: Formats user story documents
- **idea-agent**: Formats idea validation reports
- **presentation-generator**: Provides content for slides

## Success Criteria

Documents should be:
- [ ] Professionally formatted
- [ ] Easy to read and navigate
- [ ] Properly styled with hierarchy
- [ ] Accessible (screen readers, contrast)
- [ ] Shareable with appropriate permissions
- [ ] Consistent with brand guidelines
- [ ] Export-ready for PDF if needed

---

Use this Skill to create polished, professional documents that effectively communicate PM deliverables to all stakeholders.
