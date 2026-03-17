---
name: knowledge-capture
description: Transform conversations and discussions into structured Notion documentation
---

## Overview

The Knowledge Capture skill transforms conversations, discussions, and unstructured information into organized, structured documentation in Notion. It helps you preserve institutional knowledge by capturing important conversations and converting them into actionable, well-formatted documentation.

## When to Use

Use this skill when you need to:
- Convert transcripts or conversation notes into structured documentation
- Create meeting summaries with action items
- Build knowledge base articles from discussions
- Archive important conversations for future reference
- Extract key insights and decisions from discussions

## Features

- **Smart Content Extraction**: Automatically identifies key points, decisions, and action items from conversations
- **Structured Organization**: Creates well-organized Notion documents with proper hierarchy
- **Metadata Capture**: Preserves participants, dates, and context information
- **Action Item Tracking**: Extracts and formats action items with ownership and deadlines
- **Cross-linking**: Automatically creates links to related documentation and team members

## Requirements

- **Notion API Access**: Integration token with appropriate permissions
- **Target Workspace**: Notion workspace where documentation will be stored
- **Template (Optional)**: Pre-defined Notion template for consistent structure

## Implementation Details

This skill uses the Notion API to:

1. Parse input content (text, transcripts, or discussion notes)
2. Extract key information using structural analysis
3. Format content according to Notion document standards
4. Create or update Notion pages with captured knowledge
5. Maintain cross-references and relationships

### Typical Workflow

```
Input: Conversation/Discussion
  ↓
Parse & Extract
  ↓
Identify: Key Points, Decisions, Action Items
  ↓
Format for Notion
  ↓
Create/Update Notion Document
  ↓
Output: Structured Documentation
```

## Example Use Cases

1. **Team Meeting Notes**
   - Input: Meeting transcript
   - Output: Organized meeting summary with decisions and next steps

2. **Customer Call Documentation**
   - Input: Call notes and transcript
   - Output: Customer interaction record with key requirements

3. **Architecture Discussion**
   - Input: Design discussion notes
   - Output: Architectural decision record with alternatives and rationale

4. **Interview Notes**
   - Input: Interview transcript
   - Output: Structured candidate or user research documentation

## Configuration

Set up these environment variables or Notion settings:

```env
NOTION_API_TOKEN=your_token_here
NOTION_DATABASE_ID=your_database_id
```

## See Also

- [Research Documentation](/skills/research-documentation) - For research-focused documentation
- [Meeting Intelligence](/skills/meeting-intelligence) - For meeting preparation and follow-up
- [Notion API Documentation](https://developers.notion.com)
