---
name: attach-content
description: |
  Attach generated content to the current issue as a file.
  MANDATORY TRIGGERS: attach, save as file, create attachment, export, download, save this
  Use when you've created substantial content (guides, reports, analysis, code, documentation) that should be preserved as an attachment on the issue.
---

# Attach Content Skill

When you generate substantial content that would be valuable to save, use the `attachContent` tool to attach it to the issue.

## When to Attach Content

Attach content when you've created:
- Optimization guides or recommendations (e.g., AIO/GEO optimization output)
- Technical documentation or specifications
- Code files or configuration examples
- Analysis reports or research findings
- Checklists or implementation guides
- Any content the user explicitly asks to save/attach

## How to Use

1. Generate the content first (e.g., an optimization guide)
2. Call the `attachContent` tool with:
   - `content`: The full content to save
   - `filename`: A descriptive filename with appropriate extension
   - `mimeType`: Optional, defaults to "text/markdown"

## Filename Conventions

Use descriptive, kebab-case filenames:
- `aio-geo-optimization-guide.md` - For optimization guides
- `technical-specification.md` - For technical docs
- `implementation-checklist.md` - For checklists
- `config-example.json` - For configuration files
- `analysis-report.md` - For analysis/research

## Example Workflow

When using the AIO-GEO-Optimizer skill:

1. Follow the optimization workflow to generate optimized content
2. After generating the output, automatically attach it:
   ```
   attachContent({
     content: "# Optimized Article\n\n...",
     filename: "aio-geo-optimization-guide.md"
   })
   ```
3. Inform the user the guide has been attached to the issue

## Integration with Other Skills

When another skill produces substantial output (like AIO-GEO-Optimizer), you should:
1. Complete that skill's workflow
2. Automatically attach the generated content
3. Notify the user that the content is now attached to the issue for future reference
