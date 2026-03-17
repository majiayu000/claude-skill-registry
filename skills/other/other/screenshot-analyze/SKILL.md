---
context: fork
---

# /screenshot-analyze

Perform comprehensive analysis of screenshots using Sonnet sub-agents for detailed visual inspection.

## Usage

```
/screenshot-analyze <image-path>
/screenshot-analyze +Attachments/error-screenshot.png
/screenshot-analyze +Attachments/ui-mockup.png --context "login flow"
```

## Instructions

This skill uses **Sonnet model sub-agents** for thorough image analysis with vision capabilities.

### Phase 1: Image Loading

1. Verify the image exists at the specified path
2. Check file type is supported (PNG, JPG, JPEG, GIF, WebP)
3. Note any context provided by user

### Phase 2: Comprehensive Analysis (Sonnet Sub-Agents)

Launch these sub-agents using `model: "sonnet"`:

**Agent 1: Content Extraction** (Sonnet)
```
Task: Extract all visible content from the image
- Read the image file using the Read tool
- Extract all visible text (OCR)
- Identify UI elements, buttons, labels
- Note any error messages or notifications
- Capture data values, IDs, or codes visible
Return: Complete text extraction with location context
```

**Agent 2: Visual Structure Analysis** (Sonnet)
```
Task: Analyse the visual structure and layout
- Read the image file
- Identify the type of content (UI, diagram, document, error, etc.)
- Map the visual hierarchy and layout
- Note colour schemes, branding elements
- Identify interactive elements
- Assess visual quality and clarity
Return: Structural analysis with element inventory
```

**Agent 3: Context & Purpose Analysis** (Sonnet)
```
Task: Understand the purpose and context
- Read the image file
- Determine what application/system is shown
- Identify the workflow or process stage
- Note any problems or issues visible
- Assess what action might be needed
- Connect to known YourOrg systems if recognisable
Return: Contextual interpretation with system identification
```

### Phase 3: Compile Report

```markdown
# Screenshot Analysis

**Image**: {{filename}}
**Analysed**: {{DATE}}
**Type**: {{UI/Error/Diagram/Document/Other}}

## Summary

{{2-3 sentence overview of what the image shows}}

## Extracted Content

### Text Found
{{all readable text, organised by location}}

### UI Elements
| Element | Type | Label/Text | State |
|---------|------|------------|-------|
{{element inventory}}

### Data Values
{{any IDs, codes, numbers, or data visible}}

## Visual Analysis

### Layout Structure
{{description of visual hierarchy}}

### Application/System
- **Identified as**: {{system name if known}}
- **Screen/Page**: {{specific view or page}}
- **Context**: {{workflow stage}}

## Observations

### Key Findings
{{important observations}}

### Issues Detected
{{any errors, warnings, or problems visible}}

### Recommendations
{{suggested actions based on analysis}}

## Related Notes

{{suggest links to related vault notes if system is recognised}}
```

### Notes

- Sonnet provides superior visual analysis capabilities
- Works with screenshots, UI mockups, error messages, dashboards
- Can recognise YourOrg systems like SAP, MROPlatform, Confluence, etc.
