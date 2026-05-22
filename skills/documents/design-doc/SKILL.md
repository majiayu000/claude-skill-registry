---
name: design-doc
description: Create an engineering design document from conversation context using the Google Drive template.
user-invocable: true
---

# Design Document Generator

Create an engineering design document based on the current conversation context, following the team's standard template from Google Drive.

## Prerequisites

Requires Google Drive OAuth setup. See `claude/skills/SETUP.md` for instructions.

## When to Use

Use this skill when the user:
- Asks to create a design doc
- Wants to document a technical decision or architecture
- Needs to write up a feature proposal
- Says `/design-doc`

## Workflow

### 1. Find the Template in Google Drive

Search for the engineering design doc template:

```bash
ACCESS_TOKEN=$(google-oauth-token)

curl -s -G "https://www.googleapis.com/drive/v3/files" \
  --data-urlencode "q=name contains 'engineering design doc template'" \
  --data-urlencode "fields=files(id,name,mimeType,webViewLink)" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```

If multiple results, pick the one that's a Google Doc (`mimeType = 'application/vnd.google-apps.document'`).

### 2. Read the Template

Export the template as plain text to understand its structure:

```bash
DOC_ID="<template-doc-id>"
curl -s "https://www.googleapis.com/drive/v3/files/${DOC_ID}/export?mimeType=text/plain" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```

### 3. Analyze the Template

The template will contain:
- Section headings (e.g., Summary, Background, Goals, Non-Goals, Design, Alternatives, etc.)
- Instructions or placeholders for what to include in each section
- Formatting guidance

Extract the structure and understand what each section should contain.

### 4. Generate the Design Document

Using the conversation history as context, create a design document that:
- Follows the exact section structure from the template
- Fills in each section with relevant content from the conversation
- Uses appropriate technical detail for each section
- Maintains a professional, clear writing style

If the conversation doesn't contain enough information for certain sections:
- Mark them with `[TODO: <what's needed>]`
- Or ask the user for the missing information before generating

### 5. Determine the Filename

Ask the user what to name the file, or derive it from the document title/summary:
- Use kebab-case: `feature-name-design.md`
- Default location: current working directory

### 6. Write the Document

Write the generated design doc as a markdown file:

```bash
# Example - the actual content will be generated based on conversation
cat > ./my-feature-design.md << 'EOF'
# Design Document: My Feature

## Summary
...

## Background
...

[rest of sections from template]
EOF
```

### 7. Report to User

After writing the file:
- Tell the user the file path
- Mention any `[TODO]` sections that need to be filled in
- Remind them how to paste into Google Docs with formatting:

**Pasting into Google Docs:**

Standard pasting (Ctrl+V or Cmd+V) will only paste plain text. To convert the Markdown into formatted Google Docs content:

1. Copy the Markdown content to your clipboard from the file
2. In your Google Docs document, right-click where you want to paste
3. From the context menu, select **"Paste from Markdown"**

The Markdown will be converted to rich text (headings, bold text, lists, tables) and inserted with the correct formatting.

## Example Output

```markdown
# Design Document: User Authentication Refactor

## Summary
Refactor the authentication system to use JWT tokens instead of session cookies...

## Background
The current session-based auth has scaling issues because...

## Goals
- Support horizontal scaling without sticky sessions
- Reduce auth latency by 50%
- Maintain backwards compatibility during migration

## Non-Goals
- Changing the user-facing login flow
- Adding new auth methods (OAuth, SSO)

## Design
### Architecture
...

### API Changes
...

## Alternatives Considered
### Keep session-based auth with Redis
Rejected because...

## Security Considerations
...

## Timeline
...
```

## Notes

- The template structure may vary - always read the actual template first
- Keep the generated doc concise but complete
- If the conversation was exploratory, focus on the decisions that were made
- Include relevant code snippets or diagrams if discussed in the conversation
