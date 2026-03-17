---
name: pptx-skill
description: Expert in creating, editing, and automating PowerPoint presentations using python-pptx and PptxGenJS. Use when generating slides programmatically, modifying presentations, or building report automation. Triggers include "PowerPoint", "PPTX", "slides", "presentation", "python-pptx", "PptxGenJS", "slide deck".
---

# PPTX Skill

## Purpose
Provides expertise in programmatic PowerPoint presentation creation, editing, and automation. Specializes in using python-pptx (Python) and PptxGenJS (JavaScript) for generating dynamic slide decks and automating presentation workflows.

## When to Use
- Generating presentations programmatically
- Creating slides from data sources
- Modifying existing PowerPoint files
- Building automated report generators
- Adding charts and tables to slides
- Applying templates and branding
- Extracting content from presentations
- Batch processing multiple presentations

## Quick Start
**Invoke this skill when:**
- Creating PowerPoint files from code
- Automating slide generation
- Modifying existing PPTX files
- Building presentation templates
- Extracting data from slides

**Do NOT invoke when:**
- PDF generation → use `/pdf-skill`
- Word documents → use `/docx-skill`
- Excel files → use `/xlsx-skill`
- Manual presentation design → use appropriate design tools

## Decision Framework
```
PPTX Operation?
├── Generate from Scratch
│   ├── Python → python-pptx
│   └── JavaScript → PptxGenJS
├── Modify Existing
│   └── python-pptx (read + modify)
├── Template-Based
│   └── Load template, fill placeholders
└── Extract Content
    └── python-pptx for reading
```

## Core Workflows

### 1. Presentation Generation (python-pptx)
1. Install python-pptx
2. Create Presentation object
3. Add slides from layouts
4. Add content (text, images, tables)
5. Apply formatting
6. Save presentation

### 2. Chart Creation
1. Prepare data for chart
2. Create chart data object
3. Add chart to slide
4. Configure chart type and options
5. Style chart elements
6. Position and size appropriately

### 3. Template-Based Generation
1. Create master template with placeholders
2. Load template in code
3. Identify placeholder shapes
4. Replace placeholder content
5. Add dynamic slides as needed
6. Save as new file

## Best Practices
- Use slide layouts from the template
- Keep text within placeholder boundaries
- Use appropriate chart types for data
- Maintain consistent styling
- Test output in PowerPoint
- Handle missing fonts gracefully

## Anti-Patterns
| Anti-Pattern | Problem | Correct Approach |
|--------------|---------|------------------|
| Ignoring layouts | Inconsistent formatting | Use slide layouts |
| Hardcoded positions | Layout breaks | Use placeholders |
| Too much text per slide | Unreadable | Limit content, use bullets |
| Missing templates | Reinventing styling | Create reusable templates |
| No error handling | Corrupted files | Validate and handle errors |
