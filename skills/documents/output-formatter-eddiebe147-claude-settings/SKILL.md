---
name: Output Formatter
slug: output-formatter
description: Format AI outputs for different contexts and audiences
category: meta
complexity: simple
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "format this output"
  - "format as"
  - "convert to"
  - "reformat this"
  - "change format"
tags:
  - formatting
  - output-design
  - presentation
---

# Output Formatter

The Output Formatter skill transforms AI-generated content into the right format for your specific context. Whether you need markdown for documentation, JSON for APIs, tables for analysis, or prose for presentations, this skill ensures outputs are structured appropriately and consistently.

This skill understands format requirements across different platforms (GitHub, Notion, Slack, email), use cases (technical docs, user guides, reports, code comments), and audiences (developers, stakeholders, end users). It helps you avoid manual reformatting and ensures professional, consistent presentation.

Use this skill whenever AI output needs to be transformed for a specific platform, integrated into existing documentation, or presented to a particular audience.

## Core Workflows

### Workflow 1: Convert Between Formats
1. **Identify** source format:
   - Current structure
   - Content type
   - Data hierarchy
2. **Understand** target format requirements:
   - Platform constraints
   - Syntax rules
   - Conventions
3. **Map** content structure:
   - Headers → equivalent elements
   - Lists → appropriate format
   - Code blocks → proper syntax
   - Links → platform-specific
4. **Transform** content:
   - Preserve semantic meaning
   - Adapt to target syntax
   - Maintain readability
5. **Validate** output:
   - Syntax correctness
   - Completeness
   - Visual consistency
6. **Provide** formatted result

### Workflow 2: Format for Specific Platform
1. **Identify** target platform:
   - GitHub (markdown)
   - Notion (blocks)
   - Slack (mrkdwn)
   - Email (HTML/plain text)
   - Confluence (wiki)
   - Jira (markup)
2. **Apply** platform-specific conventions:
   - Syntax variations
   - Supported features
   - Best practices
   - Limitations
3. **Optimize** for platform:
   - Use platform-native features
   - Respect character limits
   - Add appropriate formatting
4. **Test** rendering (if possible)
5. **Provide** ready-to-paste output

### Workflow 3: Structure Data for Presentation
1. **Analyze** data content:
   - Type of information
   - Relationships
   - Importance hierarchy
2. **Choose** optimal structure:
   - Table for comparisons
   - List for sequences
   - Tree for hierarchies
   - Graph for relationships
3. **Format** accordingly:
   - Clear headers
   - Consistent alignment
   - Appropriate nesting
   - Visual hierarchy
4. **Add** context:
   - Title/caption
   - Column descriptions
   - Units/scales
   - Footnotes if needed
5. **Validate** readability

### Workflow 4: Adapt for Audience
1. **Identify** target audience:
   - Technical expertise level
   - Domain knowledge
   - Role/responsibility
   - Context/goals
2. **Adjust** content appropriately:
   - Technical depth
   - Jargon usage
   - Detail level
   - Examples chosen
3. **Restructure** for clarity:
   - Executive summary for leadership
   - Details for implementers
   - Context for newcomers
4. **Format** to match expectations:
   - Business: Charts and summaries
   - Technical: Code and diagrams
   - User-facing: Simple and clear
5. **Review** for appropriateness

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| Convert to markdown | "Format as markdown" |
| Convert to JSON | "Format as JSON" |
| Convert to table | "Format as table" |
| Format for GitHub | "Format for GitHub" |
| Format for Notion | "Format for Notion" |
| Format for Slack | "Format for Slack" |
| Make it technical | "Format for developers" |
| Make it non-technical | "Format for stakeholders" |
| Create summary | "Format as executive summary" |

## Best Practices

- **Preserve Meaning**: Don't lose information during transformation
  - Keep all substantive content
  - Maintain logical structure
  - Preserve relationships and context

- **Follow Conventions**: Use format-specific best practices
  - Markdown: ATX headers, fenced code blocks
  - JSON: Proper escaping, consistent indentation
  - Tables: Aligned columns, clear headers

- **Optimize Readability**: Format for human consumption
  - Use whitespace effectively
  - Break up long sections
  - Add visual hierarchy
  - Include context clues

- **Validate Output**: Ensure format correctness
  - Test with parsers when possible
  - Check rendering preview
  - Verify syntax highlighting

- **Be Consistent**: Maintain uniform style
  - Same header levels for same importance
  - Consistent list formatting
  - Uniform code block languages
  - Standardized terminology

- **Consider Context**: Format appropriately for use case
  - Documentation: Clear, detailed, structured
  - Communication: Concise, scannable, actionable
  - Code: Properly commented, syntax-highlighted
  - Reports: Data-rich, visual, summarized

## Format Templates

### Markdown Documentation
```markdown
# Main Title

## Overview
Brief introduction to the topic.

## Key Concepts
- **Concept 1**: Description
- **Concept 2**: Description

## Usage
\`\`\`language
code example
\`\`\`

## Reference
| Parameter | Type | Description |
|-----------|------|-------------|
| param1 | string | What it does |
```

### JSON API Response
```json
{
  "status": "success",
  "data": {
    "items": [],
    "pagination": {
      "page": 1,
      "totalPages": 10,
      "totalItems": 100
    }
  },
  "metadata": {
    "timestamp": "2026-01-06T00:00:00Z",
    "version": "1.0"
  }
}
```

### Comparison Table
```markdown
| Feature | Option A | Option B | Option C |
|---------|----------|----------|----------|
| Speed | Fast | Medium | Slow |
| Cost | High | Medium | Low |
| Ease | Easy | Medium | Complex |
| **Recommend** | ✓ | | |
```

### Executive Summary
```markdown
## Executive Summary

**Objective**: [One-line goal]

**Status**: [Current state]

**Key Results**:
- Result 1
- Result 2
- Result 3

**Next Steps**:
1. Action item 1
2. Action item 2

**Blockers**: [Issues requiring escalation]
```

### Technical Specification
```markdown
## [Component Name]

**Purpose**: [What it does]

**Dependencies**: [What it requires]

**Interface**:
\`\`\`typescript
interface ComponentProps {
  prop1: string;
  prop2?: number;
}
\`\`\`

**Behavior**:
1. Step-by-step description

**Error Handling**:
- Error type: Response

**Examples**:
\`\`\`typescript
// Usage example
\`\`\`
```

### Slack Message
```markdown
*Project Update* :rocket:

*Status*: On track
*Completed*:
• Feature A deployed
• Bug fixes merged

*Next*:
• Feature B review
• Performance testing

*Blockers*: None

<link|Full details>
```

## Format Conversion Guide

### From Prose to List
**Before**: "The system supports authentication through OAuth, API keys, and session tokens. It also provides role-based access control."

**After**:
```markdown
## Authentication Methods
- OAuth 2.0
- API Keys
- Session Tokens

## Authorization
- Role-based Access Control (RBAC)
```

### From List to Table
**Before**:
```
- JavaScript: 45%
- TypeScript: 30%
- CSS: 15%
- HTML: 10%
```

**After**:
```markdown
| Language | Percentage |
|----------|------------|
| JavaScript | 45% |
| TypeScript | 30% |
| CSS | 15% |
| HTML | 10% |
```

### From Code to Documentation
**Before**:
```typescript
function processData(input: string[], options?: ProcessOptions): Result
```

**After**:
```markdown
### processData

Processes input data according to specified options.

**Parameters**:
- `input` (string[]): Array of strings to process
- `options` (ProcessOptions, optional): Configuration object

**Returns**: `Result` - Processed data result

**Example**:
\`\`\`typescript
const result = processData(['a', 'b', 'c'], { sort: true });
\`\`\`
```

## Platform-Specific Formatting

### GitHub Markdown
- Use `diff` syntax for code changes
- Use `[!NOTE]` for callouts
- Use `<details>` for collapsible sections
- Use emoji sparingly (`:rocket:`)
- Link to issues/PRs with `#123`

### Notion
- Use toggle blocks for long content
- Use callout blocks for important info
- Use database views for structured data
- Use two-column layouts for comparisons

### Slack
- Use `*bold*` and `_italic_`
- Use `>` for quotes
- Use ``` for code blocks
- Keep messages scannable
- Use threads for details
- Add emoji for visual cues

### Email
- Use plain text or simple HTML
- Keep paragraphs short
- Use clear subject lines
- Include summary at top
- Make CTAs obvious

## Audience Adaptation

### For Executives
- Lead with impact and outcomes
- Use business metrics
- Minimize technical jargon
- Include visuals (charts, graphs)
- Provide clear recommendations
- Keep it concise

### For Developers
- Include technical details
- Show code examples
- Link to relevant documentation
- Explain architecture decisions
- Provide reproduction steps
- Be precise with terminology

### For End Users
- Use simple language
- Include screenshots/visuals
- Provide step-by-step instructions
- Explain "why" not just "how"
- Anticipate questions
- Offer support resources

### For Stakeholders
- Focus on progress and timeline
- Highlight risks and mitigations
- Connect to business goals
- Use metrics and data
- Provide options and recommendations
- Be honest about challenges
