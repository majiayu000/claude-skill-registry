---
# ═══════════════════════════════════════════════════════════════════════════════
# CLAUDE OFFICE SKILL - Enhanced Metadata v2.0
# ═══════════════════════════════════════════════════════════════════════════════

# Basic Information
name: html-to-ppt
description: "Convert HTML/Markdown to PowerPoint presentations using Marp"
version: "1.0"
author: claude-office-skills
license: MIT

# Categorization
category: conversion
tags:
  - html
  - pptx
  - conversion
  - slides
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
    - pptx_to_html

# Skill Capabilities
capabilities:
  - html_conversion
  - slide_generation

# Language Support
languages:
  - en
  - zh
---

# HTML/Markdown to PowerPoint Skill

## Overview

This skill enables conversion from Markdown or HTML to professional PowerPoint presentations using **Marp** (Markdown Presentation Ecosystem). Create beautiful, consistent slides using simple Markdown syntax with CSS-based themes.

## How to Use

1. Provide Markdown content structured for slides
2. Optionally specify a theme or custom styling
3. I'll convert it to PowerPoint, PDF, or HTML slides

**Example prompts:**
- "Convert this markdown to a PowerPoint presentation"
- "Create slides from this outline using Marp"
- "Turn my notes into a presentation with the gaia theme"
- "Generate a PDF slide deck from this markdown"

## Domain Knowledge

### Marp Fundamentals

Marp uses a simple syntax where `---` separates slides:

```markdown
---
marp: true
theme: default
---

# Slide 1 Title

Content for first slide

---

# Slide 2 Title

Content for second slide
```

### Command Line Usage

```bash
# Convert to PowerPoint
marp slides.md -o presentation.pptx

# Convert to PDF
marp slides.md -o presentation.pdf

# Convert to HTML
marp slides.md -o presentation.html

# With specific theme
marp slides.md --theme gaia -o presentation.pptx
```

### Slide Structure

#### Basic Slide
```markdown
---
marp: true
---

# Title

- Bullet point 1
- Bullet point 2
- Bullet point 3
```

#### Title Slide
```markdown
---
marp: true
theme: gaia
class: lead
---

# Presentation Title

## Subtitle

Author Name
Date
```

### Frontmatter Options

```yaml
---
marp: true
theme: default          # default, gaia, uncover
size: 16:9              # 4:3, 16:9, or custom
paginate: true          # Show page numbers
header: 'Company Name'  # Header text
footer: 'Confidential'  # Footer text
backgroundColor: #fff
backgroundImage: url('bg.png')
---
```

### Themes

#### Built-in Themes
```markdown
---
marp: true
theme: default   # Clean, minimal
---

---
marp: true
theme: gaia      # Colorful, modern
---

---
marp: true
theme: uncover   # Bold, presentation-focused
---
```

#### Theme Classes
```markdown
---
marp: true
theme: gaia
class: lead     # Centered title slide
---

---
marp: true
theme: gaia
class: invert   # Inverted colors
---
```

### Formatting

#### Text Styling
```markdown
# Heading 1
## Heading 2

**Bold text** and *italic text*

`inline code`

> Blockquote for emphasis
```

#### Lists
```markdown
- Unordered item
- Another item
  - Nested item

1. Ordered item
2. Second item
   1. Nested numbered
```

#### Code Blocks
```markdown
# Code Example

\`\`\`python
def hello():
    print("Hello, World!")
\`\`\`
```

#### Tables
```markdown
| Feature | Status |
|---------|--------|
| Tables  | ✅     |
| Charts  | ✅     |
| Images  | ✅     |
```

### Images

#### Basic Image
```markdown
![](image.png)
```

#### Sized Image
```markdown
![width:500px](image.png)
![height:300px](image.png)
![width:80%](image.png)
```

#### Background Image
```markdown
---
marp: true
backgroundImage: url('background.jpg')
---

# Slide with Background
```

### Advanced Layout

#### Two Columns
```markdown
---
marp: true
style: |
  .columns {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }
---

# Two Column Layout

<div class="columns">
<div>

## Left Column
- Point 1
- Point 2

</div>
<div>

## Right Column
- Point A
- Point B

</div>
</div>
```

#### Split Background
```markdown
---
marp: true
theme: gaia
class: gaia
---

<!-- 
_backgroundImage: linear-gradient(to right, #4a90a4, #4a90a4 50%, white 50%)
-->

<div class="columns">
<div style="color: white;">

# Dark Side

</div>
<div>

# Light Side

</div>
</div>
```

### Directives

#### Local Directives (per slide)
```markdown
---
marp: true
---

<!-- 
_backgroundColor: #123
_color: white
_paginate: false
-->

# Special Slide
```

#### Scoped Styles
```markdown
---
marp: true
---

<style scoped>
h1 {
  color: red;
}
</style>

# This Title is Red
```

### Python Integration

```python
import subprocess
import tempfile
import os

def markdown_to_pptx(md_content, output_path, theme='default'):
    """Convert Markdown to PowerPoint using Marp."""
    
    # Add marp directive if not present
    if '---\nmarp: true' not in md_content:
        md_content = f"---\nmarp: true\ntheme: {theme}\n---\n\n" + md_content
    
    # Write to temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(md_content)
        temp_path = f.name
    
    try:
        # Convert using marp
        subprocess.run([
            'marp', temp_path, '-o', output_path
        ], check=True)
        
        return output_path
    finally:
        os.unlink(temp_path)

# Usage
md = """
# Welcome

Introduction slide

---

# Agenda

- Topic 1
- Topic 2
- Topic 3
"""

markdown_to_pptx(md, 'presentation.pptx')
```

### Node.js/marp-cli API

```javascript
const { marpCli } = require('@marp-team/marp-cli');

// Convert file
marpCli(['slides.md', '-o', 'output.pptx']).then(exitCode => {
    console.log('Done:', exitCode);
});
```

## Best Practices

1. **One Idea Per Slide**: Keep slides focused
2. **Use Visual Hierarchy**: Consistent heading levels
3. **Limit Text**: 6 bullets max per slide
4. **Include Images**: Visual content enhances retention
5. **Test Output**: Preview before final export

## Common Patterns

### Presentation Generator
```python
def create_presentation(title, sections, output_path, theme='gaia'):
    """Generate presentation from structured data."""
    
    md_content = f"""---
marp: true
theme: {theme}
paginate: true
---

<!-- _class: lead -->

# {title}

{sections.get('subtitle', '')}

{sections.get('author', '')}

"""
    
    for section in sections.get('slides', []):
        md_content += f"""---

# {section['title']}

"""
        for point in section.get('points', []):
            md_content += f"- {point}\n"
        
        if section.get('notes'):
            md_content += f"\n<!-- Notes: {section['notes']} -->\n"
    
    md_content += """---

<!-- _class: lead -->

# Thank You!

Questions?
"""
    
    return markdown_to_pptx(md_content, output_path, theme)
```

### Batch Slide Generation
```python
def generate_report_slides(data_list, template, output_dir):
    """Generate multiple presentations from data."""
    import os
    
    for data in data_list:
        content = template.format(**data)
        output_path = os.path.join(output_dir, f"{data['name']}_report.pptx")
        markdown_to_pptx(content, output_path)
```

## Examples

### Example 1: Tech Presentation
```markdown
---
marp: true
theme: gaia
class: lead
paginate: true
---

# API Documentation

## REST API Best Practices

Engineering Team
January 2024

---

# Agenda

1. Authentication
2. Endpoints Overview
3. Error Handling
4. Rate Limiting
5. Examples

---

# Authentication

All requests require an API key:

```http
Authorization: Bearer YOUR_API_KEY
```

- Keys expire after 90 days
- Store securely, never commit to git
- Rotate regularly

---

# Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /users | List all users |
| POST | /users | Create user |
| GET | /users/:id | Get user details |
| PUT | /users/:id | Update user |
| DELETE | /users/:id | Delete user |

---

# Error Handling

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format",
    "details": ["email must be valid"]
  }
}
```

---

<!-- _class: lead -->

# Questions?

api-support@company.com
```

### Example 2: Business Pitch
```python
def create_pitch_deck(company_data):
    """Generate investor pitch deck."""
    
    md = f"""---
marp: true
theme: uncover
paginate: true
---

<!-- _class: lead -->
<!-- _backgroundColor: #2d3748 -->
<!-- _color: white -->

# {company_data['name']}

{company_data['tagline']}

---

# The Problem

{company_data['problem_statement']}

**Market Pain Points:**
"""
    
    for pain in company_data['pain_points']:
        md += f"- {pain}\n"
    
    md += f"""
---

# Our Solution

{company_data['solution']}

![width:600px]({company_data.get('product_image', 'product.png')})

---

# Market Opportunity

- **TAM:** {company_data['tam']}
- **SAM:** {company_data['sam']}
- **SOM:** {company_data['som']}

---

# Traction

| Metric | Value |
|--------|-------|
| Monthly Revenue | {company_data['mrr']} |
| Customers | {company_data['customers']} |
| Growth Rate | {company_data['growth']} |

---

# The Ask

**Seeking:** {company_data['funding_ask']}

**Use of Funds:**
- Product Development: 40%
- Sales & Marketing: 35%
- Operations: 25%

---

<!-- _class: lead -->

# Let's Build the Future Together

{company_data['contact']}
"""
    
    return md

# Generate deck
pitch_data = {
    'name': 'TechStartup Inc',
    'tagline': 'AI-Powered Document Processing',
    'problem_statement': 'Businesses waste 20% of time on manual document work',
    'pain_points': ['Manual data entry', 'Error-prone processes', 'Slow turnaround'],
    'solution': 'Automated document processing with 99.5% accuracy',
    'tam': '$50B',
    'sam': '$10B',
    'som': '$500M',
    'mrr': '$100K',
    'customers': '50',
    'growth': '20% MoM',
    'funding_ask': '$5M Series A',
    'contact': 'founders@techstartup.com'
}

md_content = create_pitch_deck(pitch_data)
markdown_to_pptx(md_content, 'pitch_deck.pptx', theme='uncover')
```

## Limitations

- Complex animations not supported
- Some PowerPoint-specific features unavailable
- Custom fonts require CSS configuration
- Video embedding limited
- Speaker notes have basic support

## Installation

```bash
# Using npm
npm install -g @marp-team/marp-cli

# Using Homebrew
brew install marp-cli

# Verify installation
marp --version
```

## Resources

- [Marp Documentation](https://marp.app/)
- [Marp CLI GitHub](https://github.com/marp-team/marp-cli)
- [Marpit Framework](https://marpit.marp.app/)
- [Theme CSS Guide](https://marpit.marp.app/theme-css)
